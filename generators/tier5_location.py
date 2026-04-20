"""Tier 5 — Location generator.

Produces seven Core_DB address/locator tables from the pre-built AddressRecord pool.
Geography FKs in AddressRecord are placeholder values (Step 4) and are ignored here;
coherent FK chains are re-derived by sampling from Tier 1 tables (PRD §7.9 conflict note).
Core_DB.GEOSPATIAL is skipped — ST_Geometry has no CSV representation (PRD §7.9).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

import numpy as np
import pandas as pd

from config.settings import HISTORY_START, SKIPPED_TABLES
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

assert 'Core_DB.GEOSPATIAL' in SKIPPED_TABLES, 'GEOSPATIAL must remain in SKIPPED_TABLES'

_TIER5_DI_START_TS = '2000-01-01 00:00:00.000000'

_REQUIRED_TABLES = (
    'Core_DB.CITY',
    'Core_DB.COUNTY',
    'Core_DB.TERRITORY',
    'Core_DB.POSTAL_CODE',
    'Core_DB.COUNTRY',
    'Core_DB.ADDRESS_SUBTYPE',
    'Core_DB.DIRECTION_TYPE',
    'Core_DB.STREET_SUFFIX_TYPE',
)

_COLS_ADDRESS = [
    'Address_Id',
    'Address_Subtype_Cd',
]

_COLS_STREET_ADDRESS = [
    'Street_Address_Id',
    'Address_Line_1_Txt',
    'Address_Line_2_Txt',
    'Address_Line_3_Txt',
    'Dwelling_Type_Cd',
    'Census_Block_Id',
    'City_Id',
    'County_Id',
    'Territory_Id',
    'Postal_Code_Id',
    'Country_Id',
    'Carrier_Route_Txt',
]

# DDL §7430 wins over summary §2148 — includes Mail_Pickup_Tm and Mail_Delivery_Tm TIME columns.
_COLS_STREET_ADDRESS_DETAIL = [
    'Street_Address_Id',
    'Street_Address_Num',
    'Street_Address_Number_Modifier_Val',
    'Street_Direction_Type_Cd',
    'Street_Num',
    'Street_Name',
    'Street_Suffix_Cd',
    'Building_Num',
    'Unit_Num',
    'Floor_Val',
    'Workspace_Num',
    'Route_Num',
    'Mail_Pickup_Tm',
    'Mail_Delivery_Tm',
    'Mail_Stop_Num',
    'Mail_Box_Num',
]

_COLS_PARCEL_ADDRESS = [
    'Parcel_Address_Id',
    'Page_Num',
    'Map_Num',
    'Parcel_Num',
    'City_Id',
    'County_Id',
    'Country_Id',
    'Postal_Code_Id',
    'Territory_Id',
]

_COLS_POST_OFFICE_BOX_ADDRESS = [
    'Post_Office_Box_Id',
    'Post_Office_Box_Num',
    'City_Id',
    'County_Id',
    'Country_Id',
    'Postal_Code_Id',
    'Territory_Id',
]

_COLS_GEOSPATIAL_POINT = [
    'Geospatial_Point_Id',
    'Latitude_Meas',
    'Longitude_Meas',
    'Elevation_Meas',
    'Elevation_UOM_Cd',
]

_COLS_LOCATOR_RELATED = [
    'Locator_Id',
    'Related_Locator_Id',
    'Locator_Related_Reason_Cd',
    'Locator_Related_Start_Dt',
    'Locator_Related_End_Dt',
]

_LOCATOR_RELATED_COUNT = 20
_PARCEL_COUNT = 15
_POBOX_COUNT = 15


def _resolve_fk_chain(
    rng: np.random.Generator,
    us_cities: pd.DataFrame,
    terr_to_country: Dict[int, int],
    terr_to_counties: Dict[int, List[int]],
    country_to_postals: Dict[int, List[int]],
) -> Dict[str, Optional[int]]:
    """Return a coherent {city_id, territory_id, country_id, county_id, postal_code_id} dict.

    All IDs are drawn deterministically from Tier 1 tables via *rng*.
    county_id and postal_code_id may be None if no rows exist for the sampled territory/country.
    """
    city_row = us_cities.iloc[int(rng.integers(0, len(us_cities)))]
    city_id = int(city_row['City_Id'])
    territory_id = int(city_row['Territory_Id'])
    country_id = int(terr_to_country[territory_id])

    counties = terr_to_counties.get(territory_id, [])
    county_id: Optional[int] = int(rng.choice(counties)) if counties else None

    postals = country_to_postals.get(country_id, [])
    postal_code_id: Optional[int] = int(rng.choice(postals)) if postals else None

    return {
        'city_id': city_id,
        'territory_id': territory_id,
        'country_id': country_id,
        'county_id': county_id,
        'postal_code_id': postal_code_id,
    }


class Tier5Location(BaseGenerator):
    """Generate Core_DB address and locator tables from the AddressRecord pool."""

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # --- Guards ---
        if not ctx.addresses:
            raise RuntimeError('Tier5Location requires ctx.addresses — run UniverseBuilder.build() first')
        for key in _REQUIRED_TABLES:
            if key not in ctx.tables:
                raise RuntimeError(f'Tier5Location requires {key} in ctx.tables')

        # --- Pre-build Tier 1 lookup structures (built once, used per address row) ---
        city_df = ctx.tables['Core_DB.CITY']
        terr_df = ctx.tables['Core_DB.TERRITORY']
        county_df = ctx.tables['Core_DB.COUNTY']
        postal_df = ctx.tables['Core_DB.POSTAL_CODE']
        iso_df = ctx.tables.get('Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD')

        # US territory IDs from ISO_3166_COUNTRY_SUBDIVISION_STANDARD (US states)
        if iso_df is not None and len(iso_df) > 0:
            us_terr_ids = set(iso_df['Territory_Id'].values)
        else:
            us_terr_ids = set(terr_df['Territory_Id'].values)

        us_cities = city_df[city_df['Territory_Id'].isin(us_terr_ids)].reset_index(drop=True)
        if len(us_cities) == 0:
            raise RuntimeError('Tier5Location: no US cities found in Core_DB.CITY after filtering by ISO territory IDs')

        terr_to_country: Dict[int, int] = dict(
            zip(terr_df['Territory_Id'].values, terr_df['Country_Id'].values)
        )
        terr_to_counties: Dict[int, List[int]] = (
            county_df.groupby('Territory_Id')['County_Id'].apply(list).to_dict()
        )
        country_to_postals: Dict[int, List[int]] = (
            postal_df.groupby('Country_Id')['Postal_Code_Id'].apply(list).to_dict()
        )

        # --- Build FK chain per AddressRecord (placeholder geography fields on ar are ignored) ---
        address_fks: Dict[int, Dict[str, Optional[int]]] = {}
        for ar in ctx.addresses:
            address_fks[ar.address_id] = _resolve_fk_chain(
                ctx.rng, us_cities, terr_to_country, terr_to_counties, country_to_postals
            )

        # --- ADDRESS ---
        addr_rows = [
            {'Address_Id': ar.address_id, 'Address_Subtype_Cd': ar.address_subtype_cd}
            for ar in ctx.addresses
        ]
        df_address = pd.DataFrame(addr_rows, columns=_COLS_ADDRESS)
        df_address['Address_Id'] = df_address['Address_Id'].astype('int64')

        # --- STREET_ADDRESS ---
        street_rows = []
        for ar in ctx.addresses:
            fk = address_fks[ar.address_id]
            street_rows.append({
                'Street_Address_Id':  ar.address_id,
                'Address_Line_1_Txt': ar.street_line_1,
                'Address_Line_2_Txt': ar.street_line_2,
                'Address_Line_3_Txt': None,
                'Dwelling_Type_Cd':   None,
                'Census_Block_Id':    None,
                'City_Id':            fk['city_id'],
                'County_Id':          fk['county_id'],
                'Territory_Id':       fk['territory_id'],
                'Postal_Code_Id':     fk['postal_code_id'],
                'Country_Id':         fk['country_id'],
                'Carrier_Route_Txt':  None,
            })
        df_street = pd.DataFrame(street_rows, columns=_COLS_STREET_ADDRESS)
        df_street['Street_Address_Id'] = df_street['Street_Address_Id'].astype('int64')
        for col in ('Census_Block_Id', 'City_Id', 'County_Id', 'Territory_Id', 'Postal_Code_Id', 'Country_Id'):
            df_street[col] = df_street[col].astype('Int64')

        # --- STREET_ADDRESS_DETAIL ---
        detail_rows = []
        for ar in ctx.addresses:
            detail_rows.append({
                'Street_Address_Id':                ar.address_id,
                'Street_Address_Num':               ar.house_num,
                'Street_Address_Number_Modifier_Val': None,
                'Street_Direction_Type_Cd':         ar.street_direction_type_cd,
                'Street_Num':                       None,
                'Street_Name':                      ar.street_name,
                'Street_Suffix_Cd':                 ar.street_suffix_cd,
                'Building_Num':                     None,
                'Unit_Num':                         None,
                'Floor_Val':                        None,
                'Workspace_Num':                    None,
                'Route_Num':                        None,
                'Mail_Pickup_Tm':                   '09:00:00',
                'Mail_Delivery_Tm':                 '15:00:00',
                'Mail_Stop_Num':                    'N/A',
                'Mail_Box_Num':                     'N/A',
            })
        df_detail = pd.DataFrame(detail_rows, columns=_COLS_STREET_ADDRESS_DETAIL)
        df_detail['Street_Address_Id'] = df_detail['Street_Address_Id'].astype('int64')

        # --- PARCEL_ADDRESS (15 independent rows) ---
        parcel_rows = []
        for idx in range(_PARCEL_COUNT):
            fk = _resolve_fk_chain(ctx.rng, us_cities, terr_to_country, terr_to_counties, country_to_postals)
            parcel_rows.append({
                'Parcel_Address_Id': ctx.ids.next('parcel_address'),
                'Page_Num':   f'P{idx:03d}',
                'Map_Num':    f'M{idx:03d}',
                'Parcel_Num': f'APN-{idx:06d}',
                'City_Id':          fk['city_id'],
                'County_Id':        fk['county_id'],
                'Country_Id':       fk['country_id'],
                'Postal_Code_Id':   fk['postal_code_id'],
                'Territory_Id':     fk['territory_id'],
            })
        df_parcel = pd.DataFrame(parcel_rows, columns=_COLS_PARCEL_ADDRESS)
        for col in ('Parcel_Address_Id', 'City_Id', 'County_Id', 'Country_Id', 'Postal_Code_Id', 'Territory_Id'):
            df_parcel[col] = df_parcel[col].astype('Int64')

        # --- POST_OFFICE_BOX_ADDRESS (15 independent rows) ---
        pobox_rows = []
        for idx in range(_POBOX_COUNT):
            fk = _resolve_fk_chain(ctx.rng, us_cities, terr_to_country, terr_to_counties, country_to_postals)
            pobox_rows.append({
                'Post_Office_Box_Id':  ctx.ids.next('post_office_box'),
                'Post_Office_Box_Num': f'PO Box {1000 + idx}',
                'City_Id':             fk['city_id'],
                'County_Id':           fk['county_id'],
                'Country_Id':          fk['country_id'],
                'Postal_Code_Id':      fk['postal_code_id'],
                'Territory_Id':        fk['territory_id'],
            })
        df_pobox = pd.DataFrame(pobox_rows, columns=_COLS_POST_OFFICE_BOX_ADDRESS)
        for col in ('Post_Office_Box_Id', 'City_Id', 'County_Id', 'Country_Id', 'Postal_Code_Id', 'Territory_Id'):
            df_pobox[col] = df_pobox[col].astype('Int64')

        # --- GEOSPATIAL_POINT (reuse Address_Id as PK — 1:1 inheritance) ---
        geo_rows = [
            {
                'Geospatial_Point_Id': ar.address_id,
                'Latitude_Meas':       round(ar.latitude, 4),
                'Longitude_Meas':      round(ar.longitude, 4),
                'Elevation_Meas':      None,
                'Elevation_UOM_Cd':    None,
            }
            for ar in ctx.addresses
        ]
        df_geo = pd.DataFrame(geo_rows, columns=_COLS_GEOSPATIAL_POINT)
        df_geo['Geospatial_Point_Id'] = df_geo['Geospatial_Point_Id'].astype('int64')

        # --- LOCATOR_RELATED (20 distinct pairs from the address pool) ---
        addr_id_list = [ar.address_id for ar in ctx.addresses]
        pairs: set = set()
        while len(pairs) < _LOCATOR_RELATED_COUNT:
            a, b = ctx.rng.choice(addr_id_list, size=2, replace=False)
            pair = (int(a), int(b))
            if pair[0] != pair[1]:
                pairs.add(pair)
        history_start_str = str(HISTORY_START)
        loc_rel_rows = [
            {
                'Locator_Id':                a,
                'Related_Locator_Id':        b,
                'Locator_Related_Reason_Cd': 'mailing_for_physical',
                'Locator_Related_Start_Dt':  history_start_str,
                'Locator_Related_End_Dt':    None,
            }
            for a, b in pairs
        ]
        df_loc_rel = pd.DataFrame(loc_rel_rows, columns=_COLS_LOCATOR_RELATED)
        df_loc_rel['Locator_Id'] = df_loc_rel['Locator_Id'].astype('Int64')
        df_loc_rel['Related_Locator_Id'] = df_loc_rel['Related_Locator_Id'].astype('Int64')

        # --- Stamp DI on all 7 tables (Core_DB only — no stamp_valid) ---
        df_address  = self.stamp_di(df_address,  start_ts=_TIER5_DI_START_TS)
        df_street   = self.stamp_di(df_street,   start_ts=_TIER5_DI_START_TS)
        df_detail   = self.stamp_di(df_detail,   start_ts=_TIER5_DI_START_TS)
        df_parcel   = self.stamp_di(df_parcel,   start_ts=_TIER5_DI_START_TS)
        df_pobox    = self.stamp_di(df_pobox,    start_ts=_TIER5_DI_START_TS)
        df_geo      = self.stamp_di(df_geo,      start_ts=_TIER5_DI_START_TS)
        df_loc_rel  = self.stamp_di(df_loc_rel,  start_ts=_TIER5_DI_START_TS)

        return {
            'Core_DB.ADDRESS':                 df_address,
            'Core_DB.STREET_ADDRESS':          df_street,
            'Core_DB.STREET_ADDRESS_DETAIL':   df_detail,
            'Core_DB.PARCEL_ADDRESS':          df_parcel,
            'Core_DB.POST_OFFICE_BOX_ADDRESS': df_pobox,
            'Core_DB.GEOSPATIAL_POINT':        df_geo,
            'Core_DB.LOCATOR_RELATED':         df_loc_rel,
        }

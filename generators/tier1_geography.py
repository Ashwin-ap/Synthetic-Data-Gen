from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import pandas as pd

from generators.base import BaseGenerator
from seed_data.geography_ref import get_geography_seed_data

if TYPE_CHECKING:
    from registry.context import GenerationContext

# Verbatim literal required by references/02_data-mapping-reference.md Step 3 #19.
# Every row in ISO_3166_COUNTRY_SUBDIVISION_STANDARD must carry this exact string.
_ISO_3166_2_SUBDIVISION_STD = 'ISO 3166-2 Country Subdivision Standard'

_TIER0_PREREQS = [
    'Core_DB.CURRENCY',
    'Core_DB.CALENDAR_TYPE',
    'Core_DB.CITY_TYPE',
    'Core_DB.TERRITORY_TYPE',
]

# DDL column order (business columns only — stamp_di() appends the 5 DI columns).
_COLS_COUNTRY = ['Country_Id', 'Calendar_Type_Cd', 'Country_Group_Id']
_COLS_ISO_COUNTRY = ['Country_Id', 'Country_Code_Standard_Type_Cd', 'ISO_3166_Country_3_Num']
_COLS_REGION = ['Region_Id', 'Country_Id']
_COLS_TERRITORY = ['Territory_Id', 'Territory_Type_Cd', 'Country_Id', 'Region_Id']
_COLS_ISO_SUBDIV = [
    'Territory_Id', 'Territory_Standard_Type_Cd',
    'ISO_3166_Country_Alpha_2_Cd', 'ISO_3166_Country_Subdivision_Cd',
]
_COLS_COUNTY = ['County_Id', 'Territory_Id', 'MSA_Id']
_COLS_CITY = ['City_Id', 'City_Type_Cd', 'Territory_Id']
_COLS_POSTAL = ['Postal_Code_Id', 'County_Id', 'Country_Id', 'Postal_Code_Num', 'Time_Zone_Cd']
_COLS_GEO_AREA = [
    'Geographical_Area_Id', 'Geographical_Area_Subtype_Cd',
    'Geographical_Area_Short_Name', 'Geographical_Area_Name',
    'Geographical_Area_Desc', 'Geographical_Area_Start_Dt',
    'Geographical_Area_End_Dt',
]
# Fixed load timestamp for all Tier 1 geography tables — reference data never changes,
# so a deterministic constant avoids di_start_ts variation between runs.
_GEO_DI_START_TS = '2000-01-01 00:00:00.000000'

_COLS_GEO_CURR = [
    'Geographical_Area_Id', 'Currency_Cd',
    'Geographical_Area_Currency_Start_Dt',
    'Geographical_Area_Currency_Role_Cd',
    'Geographical_Area_Currency_End_Dt',
]


class Tier1Geography(BaseGenerator):
    """Generates the 10 Core_DB geography tables from hand-authored seed data.

    IDs are minted via ctx.ids (IdFactory) — seed data carries no surrogate PKs.
    All FK wiring is done via in-memory index dicts for O(1) resolution.
    Does NOT mutate ctx.tables; caller does ctx.tables.update(result).
    """

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # ── Prereq guard ──────────────────────────────────────────────────────
        for key in _TIER0_PREREQS:
            if key not in ctx.tables:
                raise RuntimeError(
                    f'Tier1Geography requires Tier 0 table {key} to be loaded first'
                )

        seed = get_geography_seed_data()

        # ── COUNTRY ───────────────────────────────────────────────────────────
        country_rows: List[Dict] = []
        country_id_by_iso3: Dict[str, int] = {}
        for c in seed['countries']:
            cid = ctx.ids.next('country')
            country_id_by_iso3[c['iso_alpha_3']] = cid
            country_rows.append({
                'Country_Id':       cid,
                'Calendar_Type_Cd': c['calendar_type_cd'],
                'Country_Group_Id': pd.NA,
            })
        df_country = pd.DataFrame(country_rows, columns=_COLS_COUNTRY)
        df_country = df_country.astype({'Country_Id': 'Int64', 'Country_Group_Id': 'Int64'})
        df_country = self.stamp_di(df_country, start_ts=_GEO_DI_START_TS)

        # ── ISO_3166_COUNTRY_STANDARD ─────────────────────────────────────────
        iso_country_rows: List[Dict] = []
        for c in seed['countries']:
            iso_country_rows.append({
                'Country_Id':                    country_id_by_iso3[c['iso_alpha_3']],
                'Country_Code_Standard_Type_Cd': 'ISO 3166-1 numeric',
                'ISO_3166_Country_3_Num':        c['iso_numeric_3'],
            })
        df_iso_country = pd.DataFrame(iso_country_rows, columns=_COLS_ISO_COUNTRY)
        df_iso_country = df_iso_country.astype({'Country_Id': 'Int64'})
        df_iso_country = self.stamp_di(df_iso_country, start_ts=_GEO_DI_START_TS)

        # ── REGION (one per country) ──────────────────────────────────────────
        region_rows: List[Dict] = []
        region_id_by_iso3: Dict[str, int] = {}
        for c in seed['countries']:
            rid = ctx.ids.next('region')
            region_id_by_iso3[c['iso_alpha_3']] = rid
            region_rows.append({
                'Region_Id':  rid,
                'Country_Id': country_id_by_iso3[c['iso_alpha_3']],
            })
        df_region = pd.DataFrame(region_rows, columns=_COLS_REGION)
        df_region = df_region.astype({'Region_Id': 'Int64', 'Country_Id': 'Int64'})
        df_region = self.stamp_di(df_region, start_ts=_GEO_DI_START_TS)

        # ── TERRITORY (US states + DC + foreign territories) ──────────────────
        territory_rows: List[Dict] = []
        territory_id_by_usps: Dict[str, int] = {}
        territory_id_by_foreign: Dict[str, int] = {}

        usa_iso3 = 'USA'
        for s in seed['us_states']:
            tid = ctx.ids.next('territory')
            territory_id_by_usps[s['usps_2']] = tid
            territory_rows.append({
                'Territory_Id':    tid,
                'Territory_Type_Cd': 'STATE',
                'Country_Id':      country_id_by_iso3[usa_iso3],
                'Region_Id':       region_id_by_iso3[usa_iso3],
            })

        for ft in seed['foreign_territories']:
            tid = ctx.ids.next('territory')
            territory_id_by_foreign[ft['name']] = tid
            territory_rows.append({
                'Territory_Id':    tid,
                'Territory_Type_Cd': ft['territory_type_cd'],
                'Country_Id':      country_id_by_iso3[ft['country_iso_alpha_3']],
                'Region_Id':       region_id_by_iso3[ft['country_iso_alpha_3']],
            })

        df_territory = pd.DataFrame(territory_rows, columns=_COLS_TERRITORY)
        df_territory = df_territory.astype({
            'Territory_Id': 'Int64', 'Country_Id': 'Int64', 'Region_Id': 'Int64',
        })
        df_territory = self.stamp_di(df_territory, start_ts=_GEO_DI_START_TS)

        # ── ISO_3166_COUNTRY_SUBDIVISION_STANDARD (US states only) ────────────
        iso_subdiv_rows: List[Dict] = []
        for s in seed['us_states']:
            iso_subdiv_rows.append({
                'Territory_Id':                  territory_id_by_usps[s['usps_2']],
                'Territory_Standard_Type_Cd':    _ISO_3166_2_SUBDIVISION_STD,
                'ISO_3166_Country_Alpha_2_Cd':   s['usps_2'],
                'ISO_3166_Country_Subdivision_Cd': s['iso_subdivision_3'],
            })
        df_iso_subdiv = pd.DataFrame(iso_subdiv_rows, columns=_COLS_ISO_SUBDIV)
        df_iso_subdiv = df_iso_subdiv.astype({'Territory_Id': 'Int64'})
        df_iso_subdiv = self.stamp_di(df_iso_subdiv, start_ts=_GEO_DI_START_TS)

        # ── COUNTY ───────────────────────────────────────────────────────────
        county_rows: List[Dict] = []
        county_id_by_name_state: Dict[Tuple[str, str], int] = {}
        for co in seed['counties']:
            coid = ctx.ids.next('county')
            county_id_by_name_state[(co['name'], co['state_usps_2'])] = coid
            county_rows.append({
                'County_Id':    coid,
                'Territory_Id': territory_id_by_usps[co['state_usps_2']],
                'MSA_Id':       pd.NA,
            })
        df_county = pd.DataFrame(county_rows, columns=_COLS_COUNTY)
        df_county = df_county.astype({
            'County_Id': 'Int64', 'Territory_Id': 'Int64', 'MSA_Id': 'Int64',
        })
        df_county = self.stamp_di(df_county, start_ts=_GEO_DI_START_TS)

        # ── CITY ─────────────────────────────────────────────────────────────
        city_rows: List[Dict] = []
        for ci in seed['cities']:
            city_id = ctx.ids.next('city')
            terr_id: Optional[int]
            if ci['state_usps_2'] is not None:
                terr_id = territory_id_by_usps[ci['state_usps_2']]
            elif ci['territory_name'] is not None:
                terr_id = territory_id_by_foreign[ci['territory_name']]
            else:
                terr_id = None
            city_rows.append({
                'City_Id':      city_id,
                'City_Type_Cd': ci['city_type_cd'],
                'Territory_Id': terr_id if terr_id is not None else pd.NA,
            })
        df_city = pd.DataFrame(city_rows, columns=_COLS_CITY)
        df_city = df_city.astype({'City_Id': 'Int64', 'Territory_Id': 'Int64'})
        df_city = self.stamp_di(df_city, start_ts=_GEO_DI_START_TS)

        # ── POSTAL_CODE ───────────────────────────────────────────────────────
        # Build per-state first-county lookup for sparse county wiring.
        county_id_by_state: Dict[str, int] = {}
        for co in seed['counties']:
            state = co['state_usps_2']
            if state not in county_id_by_state:
                county_id_by_state[state] = county_id_by_name_state[(co['name'], state)]

        postal_rows: List[Dict] = []
        seen_postal_codes: set = set()
        for ci in seed['cities']:
            country_id = country_id_by_iso3[ci['country_iso_alpha_3']]
            county_id_val: Optional[int] = None
            if ci['state_usps_2'] is not None:
                county_id_val = county_id_by_state.get(ci['state_usps_2'])
            for pc_num in ci['postal_codes']:
                if pc_num in seen_postal_codes:
                    continue
                seen_postal_codes.add(pc_num)
                postal_rows.append({
                    'Postal_Code_Id': ctx.ids.next('postal_code'),
                    'County_Id':      county_id_val if county_id_val is not None else pd.NA,
                    'Country_Id':     country_id,
                    'Postal_Code_Num': pc_num,
                    'Time_Zone_Cd':   ci['time_zone_cd'],
                })
        df_postal = pd.DataFrame(postal_rows, columns=_COLS_POSTAL)
        df_postal = df_postal.astype({
            'Postal_Code_Id': 'Int64', 'County_Id': 'Int64', 'Country_Id': 'Int64',
        })
        df_postal = self.stamp_di(df_postal, start_ts=_GEO_DI_START_TS)

        # ── GEOGRAPHICAL_AREA ─────────────────────────────────────────────────
        geo_area_rows: List[Dict] = []
        geo_area_id_by_name: Dict[str, int] = {}
        for ga in seed['geographical_areas']:
            gid = ctx.ids.next('geographical_area')
            geo_area_id_by_name[ga['name']] = gid
            geo_area_rows.append({
                'Geographical_Area_Id':         gid,
                'Geographical_Area_Subtype_Cd': ga['subtype_cd'],
                'Geographical_Area_Short_Name': ga['short_name'],
                'Geographical_Area_Name':       ga['name'],
                'Geographical_Area_Desc':       ga['desc'],
                'Geographical_Area_Start_Dt':   ga['start_dt'],
                'Geographical_Area_End_Dt':     None,
            })
        df_geo_area = pd.DataFrame(geo_area_rows, columns=_COLS_GEO_AREA)
        df_geo_area = df_geo_area.astype({'Geographical_Area_Id': 'Int64'})
        df_geo_area = self.stamp_di(df_geo_area, start_ts=_GEO_DI_START_TS)

        # ── GEOGRAPHICAL_AREA_CURRENCY ────────────────────────────────────────
        geo_curr_rows: List[Dict] = []
        for ga in seed['geographical_areas']:
            geo_curr_rows.append({
                'Geographical_Area_Id':               geo_area_id_by_name[ga['name']],
                'Currency_Cd':                        ga['currency_cd'],
                'Geographical_Area_Currency_Start_Dt': '2000-01-01',
                'Geographical_Area_Currency_Role_Cd': 'preferred',
                'Geographical_Area_Currency_End_Dt':  None,
            })
        df_geo_curr = pd.DataFrame(geo_curr_rows, columns=_COLS_GEO_CURR)
        df_geo_curr = df_geo_curr.astype({'Geographical_Area_Id': 'Int64'})
        df_geo_curr = self.stamp_di(df_geo_curr, start_ts=_GEO_DI_START_TS)

        return {
            'Core_DB.COUNTRY':                               df_country,
            'Core_DB.ISO_3166_COUNTRY_STANDARD':             df_iso_country,
            'Core_DB.REGION':                                df_region,
            'Core_DB.TERRITORY':                             df_territory,
            'Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD': df_iso_subdiv,
            'Core_DB.COUNTY':                                df_county,
            'Core_DB.CITY':                                  df_city,
            'Core_DB.POSTAL_CODE':                           df_postal,
            'Core_DB.GEOGRAPHICAL_AREA':                     df_geo_area,
            'Core_DB.GEOGRAPHICAL_AREA_CURRENCY':            df_geo_curr,
        }

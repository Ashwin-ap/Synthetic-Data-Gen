from typing import Dict
import pandas as pd

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}

# ── ADDRESS_SUBTYPE ── (PHYSICAL required — Step 15 ADDRESS generator)
_cols_address_subtype = [
    'Address_Subtype_Cd', 'Address_Subtype_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_address_subtype_rows = [
    {'Address_Subtype_Cd': 'PHYSICAL', 'Address_Subtype_Desc': 'Physical Address',         **_DI},
    {'Address_Subtype_Cd': 'MAILING',  'Address_Subtype_Desc': 'Mailing Address',           **_DI},
    {'Address_Subtype_Cd': 'BILLING',  'Address_Subtype_Desc': 'Billing Address',           **_DI},
    {'Address_Subtype_Cd': 'WORK',     'Address_Subtype_Desc': 'Work Address',              **_DI},
    {'Address_Subtype_Cd': 'VACATION', 'Address_Subtype_Desc': 'Vacation Address',          **_DI},
    {'Address_Subtype_Cd': 'PO_BOX',   'Address_Subtype_Desc': 'Post Office Box Address',   **_DI},
]

# ── DIRECTION_TYPE ── (all 8 compass points required — Step 15 STREET_ADDRESS)
_cols_direction_type = [
    'Direction_Type_Cd', 'Direction_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_direction_type_rows = [
    {'Direction_Type_Cd': 'N',  'Direction_Type_Desc': 'North',      **_DI},
    {'Direction_Type_Cd': 'S',  'Direction_Type_Desc': 'South',      **_DI},
    {'Direction_Type_Cd': 'E',  'Direction_Type_Desc': 'East',       **_DI},
    {'Direction_Type_Cd': 'W',  'Direction_Type_Desc': 'West',       **_DI},
    {'Direction_Type_Cd': 'NE', 'Direction_Type_Desc': 'Northeast',  **_DI},
    {'Direction_Type_Cd': 'NW', 'Direction_Type_Desc': 'Northwest',  **_DI},
    {'Direction_Type_Cd': 'SE', 'Direction_Type_Desc': 'Southeast',  **_DI},
    {'Direction_Type_Cd': 'SW', 'Direction_Type_Desc': 'Southwest',  **_DI},
]

# ── STREET_SUFFIX_TYPE ── (USPS-standard codes)
_cols_street_suffix_type = [
    'Street_Suffix_Cd', 'Street_Suffix_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_street_suffix_type_rows = [
    {'Street_Suffix_Cd': 'ST',   'Street_Suffix_Desc': 'Street',     **_DI},
    {'Street_Suffix_Cd': 'AVE',  'Street_Suffix_Desc': 'Avenue',     **_DI},
    {'Street_Suffix_Cd': 'BLVD', 'Street_Suffix_Desc': 'Boulevard',  **_DI},
    {'Street_Suffix_Cd': 'DR',   'Street_Suffix_Desc': 'Drive',      **_DI},
    {'Street_Suffix_Cd': 'LN',   'Street_Suffix_Desc': 'Lane',       **_DI},
    {'Street_Suffix_Cd': 'RD',   'Street_Suffix_Desc': 'Road',       **_DI},
    {'Street_Suffix_Cd': 'WAY',  'Street_Suffix_Desc': 'Way',        **_DI},
    {'Street_Suffix_Cd': 'CT',   'Street_Suffix_Desc': 'Court',      **_DI},
    {'Street_Suffix_Cd': 'PL',   'Street_Suffix_Desc': 'Place',      **_DI},
    {'Street_Suffix_Cd': 'PKWY', 'Street_Suffix_Desc': 'Parkway',    **_DI},
    {'Street_Suffix_Cd': 'CIR',  'Street_Suffix_Desc': 'Circle',     **_DI},
    {'Street_Suffix_Cd': 'TER',  'Street_Suffix_Desc': 'Terrace',    **_DI},
    {'Street_Suffix_Cd': 'TRL',  'Street_Suffix_Desc': 'Trail',      **_DI},
    {'Street_Suffix_Cd': 'HWY',  'Street_Suffix_Desc': 'Highway',    **_DI},
    {'Street_Suffix_Cd': 'LOOP', 'Street_Suffix_Desc': 'Loop',       **_DI},
]

# ── TERRITORY_TYPE ── (Step 9 Tier 1 Geography)
_cols_territory_type = [
    'Territory_Type_Cd', 'Territory_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_territory_type_rows = [
    {'Territory_Type_Cd': 'STATE',                'Territory_Type_Desc': 'State',                    **_DI},
    {'Territory_Type_Cd': 'PROVINCE',             'Territory_Type_Desc': 'Province',                 **_DI},
    {'Territory_Type_Cd': 'TERRITORY',            'Territory_Type_Desc': 'Territory',                **_DI},
    {'Territory_Type_Cd': 'DEPENDENCY',           'Territory_Type_Desc': 'Dependency',               **_DI},
    {'Territory_Type_Cd': 'COUNTRY_SUBDIVISION',  'Territory_Type_Desc': 'Country Subdivision',      **_DI},
]

# ── CITY_TYPE ── (Step 9 Tier 1 Geography)
_cols_city_type = [
    'City_Type_Cd', 'City_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_city_type_rows = [
    {'City_Type_Cd': 'CITY',            'City_Type_Desc': 'City',                  **_DI},
    {'City_Type_Cd': 'TOWN',            'City_Type_Desc': 'Town',                  **_DI},
    {'City_Type_Cd': 'VILLAGE',         'City_Type_Desc': 'Village',               **_DI},
    {'City_Type_Cd': 'MUNICIPALITY',    'City_Type_Desc': 'Municipality',          **_DI},
    {'City_Type_Cd': 'UNINCORPORATED',  'City_Type_Desc': 'Unincorporated Area',   **_DI},
]

# ── CALENDAR_TYPE ──
_cols_calendar_type = [
    'Calendar_Type_Cd', 'Calendar_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_calendar_type_rows = [
    {'Calendar_Type_Cd': 'GREGORIAN',     'Calendar_Type_Desc': 'Gregorian Calendar',             **_DI},
    {'Calendar_Type_Cd': 'FISCAL_JAN',    'Calendar_Type_Desc': 'Fiscal Year Starting January',   **_DI},
    {'Calendar_Type_Cd': 'FISCAL_JUL',    'Calendar_Type_Desc': 'Fiscal Year Starting July',      **_DI},
    {'Calendar_Type_Cd': 'FISCAL_OCT',    'Calendar_Type_Desc': 'Fiscal Year Starting October',   **_DI},
    {'Calendar_Type_Cd': 'ISLAMIC_HIJRI', 'Calendar_Type_Desc': 'Islamic Hijri Calendar',         **_DI},
]


def get_address_type_tables() -> Dict[str, pd.DataFrame]:
    return {
        'Core_DB.ADDRESS_SUBTYPE':    pd.DataFrame(_address_subtype_rows,    columns=_cols_address_subtype),
        'Core_DB.DIRECTION_TYPE':     pd.DataFrame(_direction_type_rows,     columns=_cols_direction_type),
        'Core_DB.STREET_SUFFIX_TYPE': pd.DataFrame(_street_suffix_type_rows, columns=_cols_street_suffix_type),
        'Core_DB.TERRITORY_TYPE':     pd.DataFrame(_territory_type_rows,     columns=_cols_territory_type),
        'Core_DB.CITY_TYPE':          pd.DataFrame(_city_type_rows,          columns=_cols_city_type),
        'Core_DB.CALENDAR_TYPE':      pd.DataFrame(_calendar_type_rows,      columns=_cols_calendar_type),
    }

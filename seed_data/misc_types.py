from typing import Dict
import pandas as pd

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}

# ── UNIT_OF_MEASURE_TYPE ── (authored first; UNIT_OF_MEASURE FKs to this)
_cols_unit_of_measure_type = [
    'Unit_Of_Measure_Type_Cd', 'Unit_Of_Measure_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_unit_of_measure_type_rows = [
    {'Unit_Of_Measure_Type_Cd': 'CURRENCY',   'Unit_Of_Measure_Type_Desc': 'Currency',    **_DI},
    {'Unit_Of_Measure_Type_Cd': 'LENGTH',     'Unit_Of_Measure_Type_Desc': 'Length',      **_DI},
    {'Unit_Of_Measure_Type_Cd': 'WEIGHT',     'Unit_Of_Measure_Type_Desc': 'Weight',      **_DI},
    {'Unit_Of_Measure_Type_Cd': 'COUNT',      'Unit_Of_Measure_Type_Desc': 'Count',       **_DI},
    {'Unit_Of_Measure_Type_Cd': 'TIME',       'Unit_Of_Measure_Type_Desc': 'Time',        **_DI},
    {'Unit_Of_Measure_Type_Cd': 'PERCENTAGE', 'Unit_Of_Measure_Type_Desc': 'Percentage',  **_DI},
]

# ── UNIT_OF_MEASURE ── (FK Unit_Of_Measure_Type_Cd → UNIT_OF_MEASURE_TYPE)
_cols_unit_of_measure = [
    'Unit_Of_Measure_Cd', 'Unit_Of_Measure_Name', 'Unit_Of_Measure_Type_Cd',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_unit_of_measure_rows = [
    {'Unit_Of_Measure_Cd': 'USD', 'Unit_Of_Measure_Name': 'US Dollar',   'Unit_Of_Measure_Type_Cd': 'CURRENCY',   **_DI},
    {'Unit_Of_Measure_Cd': 'EUR', 'Unit_Of_Measure_Name': 'Euro',        'Unit_Of_Measure_Type_Cd': 'CURRENCY',   **_DI},
    {'Unit_Of_Measure_Cd': 'PCT', 'Unit_Of_Measure_Name': 'Percent',     'Unit_Of_Measure_Type_Cd': 'PERCENTAGE', **_DI},
    {'Unit_Of_Measure_Cd': 'YR',  'Unit_Of_Measure_Name': 'Year',        'Unit_Of_Measure_Type_Cd': 'TIME',       **_DI},
    {'Unit_Of_Measure_Cd': 'MO',  'Unit_Of_Measure_Name': 'Month',       'Unit_Of_Measure_Type_Cd': 'TIME',       **_DI},
    {'Unit_Of_Measure_Cd': 'DAY', 'Unit_Of_Measure_Name': 'Day',         'Unit_Of_Measure_Type_Cd': 'TIME',       **_DI},
    {'Unit_Of_Measure_Cd': 'CNT', 'Unit_Of_Measure_Name': 'Count',       'Unit_Of_Measure_Type_Cd': 'COUNT',      **_DI},
    {'Unit_Of_Measure_Cd': 'KG',  'Unit_Of_Measure_Name': 'Kilogram',    'Unit_Of_Measure_Type_Cd': 'WEIGHT',     **_DI},
    {'Unit_Of_Measure_Cd': 'M',   'Unit_Of_Measure_Name': 'Meter',       'Unit_Of_Measure_Type_Cd': 'LENGTH',     **_DI},
]

# ── TIME_PERIOD_TYPE ── (PK column is Time_Period_Cd, not Time_Period_Type_Cd)
# Used by INTEREST_RATE_INDEX.Interest_Rate_Index_Time_Period_Cd FK.
_cols_time_period_type = [
    'Time_Period_Cd', 'Time_Period_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_time_period_type_rows = [
    {'Time_Period_Cd': 'DAY',           'Time_Period_Desc': 'Day',            **_DI},
    {'Time_Period_Cd': 'WEEK',          'Time_Period_Desc': 'Week',           **_DI},
    {'Time_Period_Cd': 'MONTH',         'Time_Period_Desc': 'Month',          **_DI},
    {'Time_Period_Cd': 'QUARTER',       'Time_Period_Desc': 'Quarter',        **_DI},
    {'Time_Period_Cd': 'YEAR',          'Time_Period_Desc': 'Year',           **_DI},
    {'Time_Period_Cd': 'DECADE',        'Time_Period_Desc': 'Decade',         **_DI},
    {'Time_Period_Cd': 'FISCAL_QUARTER','Time_Period_Desc': 'Fiscal Quarter', **_DI},
    {'Time_Period_Cd': 'FISCAL_YEAR',   'Time_Period_Desc': 'Fiscal Year',    **_DI},
]


def get_misc_type_tables() -> Dict[str, pd.DataFrame]:
    return {
        'Core_DB.UNIT_OF_MEASURE_TYPE': pd.DataFrame(_unit_of_measure_type_rows, columns=_cols_unit_of_measure_type),
        'Core_DB.UNIT_OF_MEASURE':      pd.DataFrame(_unit_of_measure_rows,      columns=_cols_unit_of_measure),
        'Core_DB.TIME_PERIOD_TYPE':     pd.DataFrame(_time_period_type_rows,     columns=_cols_time_period_type),
    }

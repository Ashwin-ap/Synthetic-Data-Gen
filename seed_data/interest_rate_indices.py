from typing import Dict
import pandas as pd

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}

# ── INTEREST_RATE_INDEX ──
# DDL columns (from 07_mvp-schema-reference.md §1707):
#   Interest_Rate_Index_Cd, Interest_Rate_Index_Desc, Interest_Rate_Index_Short_Name,
#   Currency_Cd, Yield_Curve_Maturity_Segment_Cd, Compound_Frequency_Time_Period_Cd,
#   Interest_Rate_Index_Type_Cd, Interest_Rate_Index_Time_Period_Cd (NOT NULL),
#   Interest_Index_Time_Period_Num
# Exactly {SOFR, PRIME, FEDFUNDS, LIBOR, EURIBOR} required — Step 16 INTEREST_INDEX_RATE.
# Interest_Rate_Index_Time_Period_Cd (NOT NULL): FK to TIME_PERIOD_TYPE.Time_Period_Cd.
#   Overnight/daily indices → 'DAY'; term indices (LIBOR 3M, EURIBOR 3M) → 'MONTH'.
_cols_interest_rate_index = [
    'Interest_Rate_Index_Cd',
    'Interest_Rate_Index_Desc',
    'Interest_Rate_Index_Short_Name',
    'Currency_Cd',
    'Yield_Curve_Maturity_Segment_Cd',
    'Compound_Frequency_Time_Period_Cd',
    'Interest_Rate_Index_Type_Cd',
    'Interest_Rate_Index_Time_Period_Cd',
    'Interest_Index_Time_Period_Num',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_interest_rate_index_rows = [
    {
        'Interest_Rate_Index_Cd':           'SOFR',
        'Interest_Rate_Index_Desc':         'Secured Overnight Financing Rate',
        'Interest_Rate_Index_Short_Name':   'SOFR',
        'Currency_Cd':                      'USD',
        'Yield_Curve_Maturity_Segment_Cd':  None,
        'Compound_Frequency_Time_Period_Cd': None,
        'Interest_Rate_Index_Type_Cd':      None,
        'Interest_Rate_Index_Time_Period_Cd': 'DAY',
        'Interest_Index_Time_Period_Num':   '1',
        **_DI,
    },
    {
        'Interest_Rate_Index_Cd':           'PRIME',
        'Interest_Rate_Index_Desc':         'Wall Street Journal US Prime Rate',
        'Interest_Rate_Index_Short_Name':   'Prime',
        'Currency_Cd':                      'USD',
        'Yield_Curve_Maturity_Segment_Cd':  None,
        'Compound_Frequency_Time_Period_Cd': None,
        'Interest_Rate_Index_Type_Cd':      None,
        'Interest_Rate_Index_Time_Period_Cd': 'DAY',
        'Interest_Index_Time_Period_Num':   '1',
        **_DI,
    },
    {
        'Interest_Rate_Index_Cd':           'FEDFUNDS',
        'Interest_Rate_Index_Desc':         'Federal Funds Rate',
        'Interest_Rate_Index_Short_Name':   'Fed Funds',
        'Currency_Cd':                      'USD',
        'Yield_Curve_Maturity_Segment_Cd':  None,
        'Compound_Frequency_Time_Period_Cd': None,
        'Interest_Rate_Index_Type_Cd':      None,
        'Interest_Rate_Index_Time_Period_Cd': 'DAY',
        'Interest_Index_Time_Period_Num':   '1',
        **_DI,
    },
    {
        'Interest_Rate_Index_Cd':           'LIBOR',
        'Interest_Rate_Index_Desc':         'London Interbank Offered Rate',
        'Interest_Rate_Index_Short_Name':   'LIBOR',
        'Currency_Cd':                      None,
        'Yield_Curve_Maturity_Segment_Cd':  None,
        'Compound_Frequency_Time_Period_Cd': None,
        'Interest_Rate_Index_Type_Cd':      None,
        'Interest_Rate_Index_Time_Period_Cd': 'MONTH',
        'Interest_Index_Time_Period_Num':   '3',
        **_DI,
    },
    {
        'Interest_Rate_Index_Cd':           'EURIBOR',
        'Interest_Rate_Index_Desc':         'Euro Interbank Offered Rate',
        'Interest_Rate_Index_Short_Name':   'EURIBOR',
        'Currency_Cd':                      'EUR',
        'Yield_Curve_Maturity_Segment_Cd':  None,
        'Compound_Frequency_Time_Period_Cd': None,
        'Interest_Rate_Index_Type_Cd':      None,
        'Interest_Rate_Index_Time_Period_Cd': 'MONTH',
        'Interest_Index_Time_Period_Num':   '3',
        **_DI,
    },
]


def get_interest_rate_index_tables() -> Dict[str, pd.DataFrame]:
    return {
        'Core_DB.INTEREST_RATE_INDEX': pd.DataFrame(_interest_rate_index_rows, columns=_cols_interest_rate_index),
    }

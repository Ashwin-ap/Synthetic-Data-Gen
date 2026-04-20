from typing import Dict
import pandas as pd

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}

# ── CURRENCY ──
# DDL columns (from 07_mvp-schema-reference.md §367):
#   Currency_Cd, Currency_Name, Exchange_Rate_Unit_Cnt, Currency_Rounding_Decimal_Cnt,
#   ISO_4217_Currency_Alpha_3_Cd  — no Currency_Symbol or numeric code in DDL.
# USD required: Step 16 AGREEMENT_CURRENCY hard-codes Currency_Use_Cd='preferred' with 'USD'.
# Currency_Rounding_Decimal_Cnt: 2 for most currencies; 0 for JPY (no sub-unit).
_cols_currency = [
    'Currency_Cd', 'Currency_Name', 'Exchange_Rate_Unit_Cnt',
    'Currency_Rounding_Decimal_Cnt', 'ISO_4217_Currency_Alpha_3_Cd',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_currency_rows = [
    {'Currency_Cd': 'USD', 'Currency_Name': 'US Dollar',              'Exchange_Rate_Unit_Cnt': 1, 'Currency_Rounding_Decimal_Cnt': 2, 'ISO_4217_Currency_Alpha_3_Cd': 'USD', **_DI},
    {'Currency_Cd': 'EUR', 'Currency_Name': 'Euro',                   'Exchange_Rate_Unit_Cnt': 1, 'Currency_Rounding_Decimal_Cnt': 2, 'ISO_4217_Currency_Alpha_3_Cd': 'EUR', **_DI},
    {'Currency_Cd': 'GBP', 'Currency_Name': 'British Pound Sterling', 'Exchange_Rate_Unit_Cnt': 1, 'Currency_Rounding_Decimal_Cnt': 2, 'ISO_4217_Currency_Alpha_3_Cd': 'GBP', **_DI},
    {'Currency_Cd': 'CAD', 'Currency_Name': 'Canadian Dollar',        'Exchange_Rate_Unit_Cnt': 1, 'Currency_Rounding_Decimal_Cnt': 2, 'ISO_4217_Currency_Alpha_3_Cd': 'CAD', **_DI},
    {'Currency_Cd': 'AUD', 'Currency_Name': 'Australian Dollar',      'Exchange_Rate_Unit_Cnt': 1, 'Currency_Rounding_Decimal_Cnt': 2, 'ISO_4217_Currency_Alpha_3_Cd': 'AUD', **_DI},
    {'Currency_Cd': 'JPY', 'Currency_Name': 'Japanese Yen',           'Exchange_Rate_Unit_Cnt': 1, 'Currency_Rounding_Decimal_Cnt': 0, 'ISO_4217_Currency_Alpha_3_Cd': 'JPY', **_DI},
]


def get_currency_tables() -> Dict[str, pd.DataFrame]:
    return {
        'Core_DB.CURRENCY': pd.DataFrame(_currency_rows, columns=_cols_currency),
    }

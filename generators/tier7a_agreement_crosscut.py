from __future__ import annotations

from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, Dict, List, Tuple

import pandas as pd

from config.settings import HISTORY_START, SIM_DATE
from config.code_values import (
    AGREEMENT_STATUS_SCHEMES,
    FROZEN_STATUS_ROW,
    CURRENCY_USE_CODES,
    AGREEMENT_FEATURE_ROLE_CODES,
    PROFITABILITY_MODEL_TYPE_CD,
    RATE_FEATURE_SUBTYPE_CD,
    ORIGINAL_LOAN_TERM_CLASSIFICATION_CD,
)
from generators.base import BaseGenerator
from utils.date_utils import month_snapshots

if TYPE_CHECKING:
    from registry.context import GenerationContext
    from registry.profiles import AgreementProfile

_TIER7A_DI_START_TS = '2000-01-01 00:00:00.000000'

_PREFERRED_CURRENCY_USE_CD         = CURRENCY_USE_CODES[0]           # 'preferred'
_USD_CURRENCY_CD                   = 'USD'
_RATE_AGREEMENT_FEATURE_ROLE_CD    = AGREEMENT_FEATURE_ROLE_CODES[2]  # 'rate'
_PRIMARY_AGREEMENT_FEATURE_ROLE_CD = AGREEMENT_FEATURE_ROLE_CODES[0]  # 'primary'
_AGREEMENT_RATE_TYPE_CD            = 'INTEREST'
_BALANCE_CATEGORY_TYPE_CD          = 'PRINCIPAL'
_TIME_PERIOD_YEAR_CD               = 'YEAR'
_AGREEMENT_METRIC_TYPE_CD          = 'CURRENT_BALANCE'
_MONETARY_UOM_CD                   = 'USD'
# Conflict: spec assumed 'PERCENT' but misc_types.py seeds 'PCT' -- use actual seeded value
_RATE_UOM_CD                       = 'PCT'

_REPRESENTATIVE_INDEX_RATES: Dict[str, Decimal] = {
    'SOFR':     Decimal('0.053300000000'),
    'PRIME':    Decimal('0.082500000000'),
    'FEDFUNDS': Decimal('0.053300000000'),
    'LIBOR':    Decimal('0.050000000000'),
    'EURIBOR':  Decimal('0.038500000000'),
}

# Maps Feature_Classification_Cd of Rate Feature rows → Interest_Rate_Index_Cd
_VARIABLE_RATE_SPREAD_CD_BY_CLASSIFICATION: Dict[str, str] = {
    'Original Loan Term': 'SOFR',
    'Current Rate':       'PRIME',
    'Origination Rate':   'FEDFUNDS',
    'Minimum Payment':    'SOFR',
}

_REQUIRED_UPSTREAM_TABLES = (
    'Core_DB.AGREEMENT_STATUS_TYPE',
    'Core_DB.AGREEMENT_STATUS_SCHEME_TYPE',
    'Core_DB.AGREEMENT_FEATURE_ROLE_TYPE',
    'Core_DB.INTEREST_RATE_INDEX',
    'Core_DB.CURRENCY',
    'Core_DB.TIME_PERIOD_TYPE',
)

# DDL column order (business cols only; DI tail appended by stamp_di)
_COLS_AGREEMENT_STATUS = [
    'Agreement_Id', 'Agreement_Status_Scheme_Cd', 'Agreement_Status_Start_Dttm',
    'Agreement_Status_Cd', 'Agreement_Status_Reason_Cd', 'Agreement_Status_End_Dttm',
]
_COLS_AGREEMENT_CURRENCY = [
    'Currency_Use_Cd', 'Agreement_Id', 'Agreement_Currency_Start_Dt',
    'Agreement_Currency_Cd', 'Agreement_Currency_End_Dt',
]
_COLS_AGREEMENT_SCORE = [
    'Agreement_Id', 'Model_Id', 'Model_Run_Id', 'Agreement_Score_Val',
]
_COLS_AGREEMENT_FEATURE = [
    'Agreement_Id', 'Feature_Id', 'Agreement_Feature_Role_Cd',
    'Agreement_Feature_Start_Dttm', 'Agreement_Feature_End_Dttm',
    'Overridden_Feature_Id', 'Agreement_Feature_Concession_Ind',
    'Agreement_Feature_Amt', 'Agreement_Feature_To_Amt',
    'Agreement_Feature_Rate', 'Agreement_Feature_Qty',
    'Agreement_Feature_Num', 'Agreement_Feature_Dt',
    'Agreement_Feature_UOM_Cd', 'Interest_Rate_Index_Cd', 'Currency_Cd',
]
_COLS_AGREEMENT_METRIC = [
    'Agreement_Id', 'Agreement_Metric_Type_Cd', 'Agreement_Metric_Start_Dttm',
    'Agreement_Metric_End_Dttm', 'Agreement_Metric_Time_Period_Cd',
    'Agreement_Metric_Amt', 'Agreement_Metric_Cnt', 'Agreement_Metric_Rate',
    'Agreement_Metric_Qty', 'Agreement_Currency_Metric_Amt', 'Currency_Cd',
    'Unit_Of_Measure_Cd', 'GL_Main_Account_Segment_Id',
]
_COLS_AGREEMENT_RATE = [
    'Agreement_Id', 'Rate_Type_Cd', 'Balance_Category_Type_Cd',
    'Agreement_Rate_Start_Dttm', 'Agreement_Rate_End_Dttm',
    'Agreement_Rate_Time_Period_Cd', 'Agreement_Rate',
]
_COLS_INTEREST_INDEX_RATE = [
    'Interest_Rate_Index_Cd', 'Index_Rate_Effective_Dttm',
    'Interest_Index_Rate', 'Discount_Factor_Pct', 'Zero_Coupon_Rate',
]
_COLS_VARIABLE_INTEREST_RATE_FEATURE = [
    'Feature_Id', 'Spread_Rate', 'Interest_Rate_Index_Cd',
    'Upper_Limit_Rate', 'Lower_Limit_Rate',
]
_COLS_TERM_FEATURE = [
    'Feature_Id', 'From_Time_Period_Cd', 'To_Time_Period_Cd',
    'Until_Age_Cd', 'From_Time_Period_Num', 'To_Time_Period_Num',
    'Until_Age_Num', 'Term_Type_Cd',
]


class Tier7aAgreementCrosscut(BaseGenerator):
    """Generates 9 Core_DB agreement cross-cutting tables (Tier 7a).

    No new IDs are minted. All FKs reuse Agreement_Id (Tier 2), Feature_Id
    (Tier 2), and Interest_Rate_Index_Cd (Tier 0). Entirely deterministic;
    no random sampling performed.
    """

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # --- A. Guards ---
        if not ctx.agreements:
            raise RuntimeError(
                "Tier7a: ctx.agreements is empty — run Tier 2 (AGREEMENT) first"
            )
        missing = [t for t in _REQUIRED_UPSTREAM_TABLES if t not in ctx.tables]
        if missing:
            raise RuntimeError(
                f"Tier7a: missing upstream tables: {missing} — run Tier 0 and Tier 2 first"
            )
        for required in ('Core_DB.AGREEMENT', 'Core_DB.FEATURE', 'Core_DB.ANALYTICAL_MODEL'):
            if required not in ctx.tables:
                raise RuntimeError(
                    f"Tier7a: {required} missing — run Tier 2 first"
                )

        feature_df = ctx.tables['Core_DB.FEATURE']

        # Rate-feature Feature_Id: both subtype AND classification must match (Layer 2 #6/#18)
        rate_feat_rows = feature_df[
            (feature_df['Feature_Subtype_Cd'] == RATE_FEATURE_SUBTYPE_CD) &
            (feature_df['Feature_Classification_Cd'] == ORIGINAL_LOAN_TERM_CLASSIFICATION_CD)
        ]
        if len(rate_feat_rows) == 0:
            raise RuntimeError(
                f"Tier7a: no FEATURE row with Subtype='{RATE_FEATURE_SUBTYPE_CD}' "
                f"AND Classification='{ORIGINAL_LOAN_TERM_CLASSIFICATION_CD}'"
            )
        rate_feature_id = int(rate_feat_rows.iloc[0]['Feature_Id'])

        # Balance-feature Feature_Id for DECLINING balance trajectory rows
        bal_feat_rows = feature_df[feature_df['Feature_Subtype_Cd'] == 'Balance Feature']
        if len(bal_feat_rows) == 0:
            raise RuntimeError(
                "Tier7a: no FEATURE row with Feature_Subtype_Cd='Balance Feature'"
            )
        balance_feature_id = int(bal_feat_rows.iloc[0]['Feature_Id'])

        # Profitability model for AGREEMENT_SCORE (Layer 2 #17)
        model_df = ctx.tables['Core_DB.ANALYTICAL_MODEL']
        prof_mask = model_df['Model_Type_Cd'] == PROFITABILITY_MODEL_TYPE_CD
        if not prof_mask.any():
            raise RuntimeError(
                f"Tier7a: no ANALYTICAL_MODEL with Model_Type_Cd='{PROFITABILITY_MODEL_TYPE_CD}'"
            )
        profitability_model_id = int(model_df[prof_mask].iloc[0]['Model_Id'])

        # Month snapshots for DECLINING balance trajectory (computed once)
        snaps: List[Tuple[date, date]] = month_snapshots(HISTORY_START, SIM_DATE)

        # --- B. AGREEMENT_STATUS ---
        # 6 current rows per agreement + 1 historical past-due row for delinquent agreements
        status_rows = []
        for ag in ctx.agreements:
            for scheme in AGREEMENT_STATUS_SCHEMES:
                code = self._status_code(ag, scheme)
                reason = (
                    'DELINQUENCY'
                    if scheme == 'Past Due Status' and ag.is_delinquent
                    else None
                )
                status_rows.append({
                    'Agreement_Id':               ag.agreement_id,
                    'Agreement_Status_Scheme_Cd': scheme,
                    'Agreement_Status_Start_Dttm': ag.open_dttm,
                    'Agreement_Status_Cd':         code,
                    'Agreement_Status_Reason_Cd':  reason,
                    'Agreement_Status_End_Dttm':   None,
                })
            if ag.is_delinquent:
                status_rows.append({
                    'Agreement_Id':               ag.agreement_id,
                    'Agreement_Status_Scheme_Cd': 'Past Due Status',
                    'Agreement_Status_Start_Dttm': ag.open_dttm,
                    'Agreement_Status_Cd':         'CURRENT',
                    'Agreement_Status_Reason_Cd':  None,
                    'Agreement_Status_End_Dttm':   ag.open_dttm + timedelta(days=365),
                })
        df_status = pd.DataFrame(status_rows, columns=_COLS_AGREEMENT_STATUS)
        df_status['Agreement_Id'] = df_status['Agreement_Id'].astype('Int64')

        # --- C. AGREEMENT_CURRENCY ---
        # One 'preferred' USD row per agreement (Layer 2 #8)
        currency_rows = [
            {
                'Currency_Use_Cd':             _PREFERRED_CURRENCY_USE_CD,
                'Agreement_Id':                ag.agreement_id,
                'Agreement_Currency_Start_Dt': ag.open_dttm.date(),
                'Agreement_Currency_Cd':       _USD_CURRENCY_CD,
                'Agreement_Currency_End_Dt':   None,
            }
            for ag in ctx.agreements
        ]
        df_currency = pd.DataFrame(currency_rows, columns=_COLS_AGREEMENT_CURRENCY)
        df_currency['Agreement_Id'] = df_currency['Agreement_Id'].astype('Int64')

        # --- D. AGREEMENT_SCORE ---
        # Deterministic profitability score via Knuth multiplicative hash (Layer 2 #17)
        score_rows = []
        for ag in ctx.agreements:
            score = ((ag.agreement_id * 2654435761) % 10_000) / 10_000
            score_rows.append({
                'Agreement_Id':       ag.agreement_id,
                'Model_Id':           profitability_model_id,
                'Model_Run_Id':       1,
                'Agreement_Score_Val': f'{float(score):.4f}',
            })
        df_score = pd.DataFrame(score_rows, columns=_COLS_AGREEMENT_SCORE)
        for col in ('Agreement_Id', 'Model_Id', 'Model_Run_Id'):
            df_score[col] = df_score[col].astype('Int64')

        # --- E. AGREEMENT_FEATURE ---
        # Two row types: rate-feature rows (loan-type only) + balance-trajectory rows (DECLINING only)
        feature_rows = []
        for ag in ctx.agreements:
            if ag.is_loan_term or ag.is_mortgage or ag.is_credit_card or ag.is_loan_transaction:
                feature_rows.append({
                    'Agreement_Id':                    ag.agreement_id,
                    'Feature_Id':                      rate_feature_id,
                    'Agreement_Feature_Role_Cd':       _RATE_AGREEMENT_FEATURE_ROLE_CD,
                    'Agreement_Feature_Start_Dttm':    ag.open_dttm,
                    'Agreement_Feature_End_Dttm':      None,
                    'Overridden_Feature_Id':           None,
                    'Agreement_Feature_Concession_Ind': None,
                    'Agreement_Feature_Amt':           None,
                    'Agreement_Feature_To_Amt':        None,
                    'Agreement_Feature_Rate':          ag.interest_rate,
                    'Agreement_Feature_Qty':           None,
                    'Agreement_Feature_Num':           None,
                    'Agreement_Feature_Dt':            None,
                    'Agreement_Feature_UOM_Cd':        _RATE_UOM_CD,
                    'Interest_Rate_Index_Cd':          'SOFR',
                    'Currency_Cd':                     _USD_CURRENCY_CD,
                })
            if len(ag.monthly_balances) == 6:
                for i, (month_start, month_end) in enumerate(snaps):
                    feature_rows.append({
                        'Agreement_Id':                    ag.agreement_id,
                        'Feature_Id':                      balance_feature_id,
                        'Agreement_Feature_Role_Cd':       _PRIMARY_AGREEMENT_FEATURE_ROLE_CD,
                        'Agreement_Feature_Start_Dttm':    datetime(
                            month_start.year, month_start.month, month_start.day
                        ),
                        'Agreement_Feature_End_Dttm':      datetime(
                            month_end.year, month_end.month, month_end.day, 23, 59, 59
                        ),
                        'Overridden_Feature_Id':           None,
                        'Agreement_Feature_Concession_Ind': None,
                        'Agreement_Feature_Amt':           ag.monthly_balances[i],
                        'Agreement_Feature_To_Amt':        None,
                        'Agreement_Feature_Rate':          None,
                        'Agreement_Feature_Qty':           None,
                        'Agreement_Feature_Num':           None,
                        'Agreement_Feature_Dt':            None,
                        'Agreement_Feature_UOM_Cd':        _MONETARY_UOM_CD,
                        'Interest_Rate_Index_Cd':          None,
                        'Currency_Cd':                     _USD_CURRENCY_CD,
                    })
        df_feature = pd.DataFrame(feature_rows, columns=_COLS_AGREEMENT_FEATURE)
        for col in ('Agreement_Id', 'Feature_Id', 'Overridden_Feature_Id'):
            df_feature[col] = df_feature[col].astype('Int64')

        # --- F. AGREEMENT_METRIC ---
        metric_rows = [
            {
                'Agreement_Id':                ag.agreement_id,
                'Agreement_Metric_Type_Cd':    _AGREEMENT_METRIC_TYPE_CD,
                'Agreement_Metric_Start_Dttm': ag.open_dttm,
                'Agreement_Metric_End_Dttm':   None,
                'Agreement_Metric_Time_Period_Cd': None,
                'Agreement_Metric_Amt':        ag.balance_amt,
                'Agreement_Metric_Cnt':        None,
                'Agreement_Metric_Rate':       None,
                'Agreement_Metric_Qty':        None,
                'Agreement_Currency_Metric_Amt': ag.balance_amt,
                'Currency_Cd':                 _USD_CURRENCY_CD,
                'Unit_Of_Measure_Cd':          _MONETARY_UOM_CD,
                'GL_Main_Account_Segment_Id':  None,
            }
            for ag in ctx.agreements
        ]
        df_metric = pd.DataFrame(metric_rows, columns=_COLS_AGREEMENT_METRIC)
        df_metric['Agreement_Id'] = df_metric['Agreement_Id'].astype('Int64')
        df_metric['GL_Main_Account_Segment_Id'] = (
            df_metric['GL_Main_Account_Segment_Id'].astype('Int64')
        )

        # --- G. AGREEMENT_RATE ---
        # ag.interest_rate consumed verbatim — mortgage vintages applied in UniverseBuilder
        rate_rows = [
            {
                'Agreement_Id':                ag.agreement_id,
                'Rate_Type_Cd':                _AGREEMENT_RATE_TYPE_CD,
                'Balance_Category_Type_Cd':    _BALANCE_CATEGORY_TYPE_CD,
                'Agreement_Rate_Start_Dttm':   ag.open_dttm,
                'Agreement_Rate_End_Dttm':     None,
                'Agreement_Rate_Time_Period_Cd': _TIME_PERIOD_YEAR_CD,
                'Agreement_Rate':              ag.interest_rate,
            }
            for ag in ctx.agreements
        ]
        df_rate = pd.DataFrame(rate_rows, columns=_COLS_AGREEMENT_RATE)
        df_rate['Agreement_Id'] = df_rate['Agreement_Id'].astype('Int64')

        # --- H. INTEREST_INDEX_RATE ---
        # One representative rate row per seeded index (no daily/monthly history)
        iir_rows = []
        for _, idx_row in ctx.tables['Core_DB.INTEREST_RATE_INDEX'].iterrows():
            cd = idx_row['Interest_Rate_Index_Cd']
            iir_rows.append({
                'Interest_Rate_Index_Cd':   cd,
                'Index_Rate_Effective_Dttm': HISTORY_START,  # DATE despite "Dttm" suffix per DDL
                'Interest_Index_Rate':      _REPRESENTATIVE_INDEX_RATES[cd],
                'Discount_Factor_Pct':      None,
                'Zero_Coupon_Rate':         None,
            })
        df_iir = pd.DataFrame(iir_rows, columns=_COLS_INTEREST_INDEX_RATE)

        # --- I. VARIABLE_INTEREST_RATE_FEATURE ---
        # One row per Rate Feature row in FEATURE (exactly 4 per tier2 templates)
        all_rate_feat_df = feature_df[
            feature_df['Feature_Subtype_Cd'] == RATE_FEATURE_SUBTYPE_CD
        ]
        assert len(all_rate_feat_df) == 4, (
            f"Expected 4 Rate Feature rows in FEATURE, got {len(all_rate_feat_df)}"
        )
        virf_rows = []
        for _, feat_row in all_rate_feat_df.iterrows():
            classification = feat_row['Feature_Classification_Cd']
            virf_rows.append({
                'Feature_Id':           feat_row['Feature_Id'],
                'Spread_Rate':          Decimal('0.020000000000'),
                'Interest_Rate_Index_Cd': _VARIABLE_RATE_SPREAD_CD_BY_CLASSIFICATION[classification],
                'Upper_Limit_Rate':     Decimal('0.180000000000'),
                'Lower_Limit_Rate':     Decimal('0.010000000000'),
            })
        df_virf = pd.DataFrame(virf_rows, columns=_COLS_VARIABLE_INTEREST_RATE_FEATURE)
        df_virf['Feature_Id'] = df_virf['Feature_Id'].astype('Int64')

        # --- J. TERM_FEATURE ---
        # One row per Term Feature row in FEATURE (exactly 4 per tier2 templates)
        term_feat_df = feature_df[feature_df['Feature_Subtype_Cd'] == 'Term Feature']
        assert len(term_feat_df) == 4, (
            f"Expected 4 Term Feature rows in FEATURE, got {len(term_feat_df)}"
        )
        tf_rows = []
        for _, feat_row in term_feat_df.iterrows():
            tf_rows.append({
                'Feature_Id':          feat_row['Feature_Id'],
                'From_Time_Period_Cd': 'MONTH',
                'To_Time_Period_Cd':   'MONTH',
                'Until_Age_Cd':        None,
                'From_Time_Period_Num': '0',
                'To_Time_Period_Num':  '360',
                'Until_Age_Num':       None,
                'Term_Type_Cd':        'STANDARD',
            })
        df_term = pd.DataFrame(tf_rows, columns=_COLS_TERM_FEATURE)
        df_term['Feature_Id'] = df_term['Feature_Id'].astype('Int64')

        # --- K. DI stamping — all 9 DataFrames; no stamp_valid() (all Core_DB) ---
        df_status   = self.stamp_di(df_status,   start_ts=_TIER7A_DI_START_TS)
        df_currency = self.stamp_di(df_currency, start_ts=_TIER7A_DI_START_TS)
        df_score    = self.stamp_di(df_score,    start_ts=_TIER7A_DI_START_TS)
        df_feature  = self.stamp_di(df_feature,  start_ts=_TIER7A_DI_START_TS)
        df_metric   = self.stamp_di(df_metric,   start_ts=_TIER7A_DI_START_TS)
        df_rate     = self.stamp_di(df_rate,     start_ts=_TIER7A_DI_START_TS)
        df_iir      = self.stamp_di(df_iir,      start_ts=_TIER7A_DI_START_TS)
        df_virf     = self.stamp_di(df_virf,     start_ts=_TIER7A_DI_START_TS)
        df_term     = self.stamp_di(df_term,     start_ts=_TIER7A_DI_START_TS)

        return {
            'Core_DB.AGREEMENT_STATUS':               df_status,
            'Core_DB.AGREEMENT_CURRENCY':             df_currency,
            'Core_DB.AGREEMENT_SCORE':                df_score,
            'Core_DB.AGREEMENT_FEATURE':              df_feature,
            'Core_DB.AGREEMENT_METRIC':               df_metric,
            'Core_DB.AGREEMENT_RATE':                 df_rate,
            'Core_DB.INTEREST_INDEX_RATE':            df_iir,
            'Core_DB.VARIABLE_INTEREST_RATE_FEATURE': df_virf,
            'Core_DB.TERM_FEATURE':                   df_term,
        }

    @staticmethod
    def _status_code(ag: 'AgreementProfile', scheme: str) -> str:
        if scheme == 'Account Status':
            return 'CLOSED' if ag.close_dttm is not None else 'OPEN'
        if scheme == 'Accrual Status':
            return 'NON_ACCRUING' if ag.is_severely_delinquent else 'ACCRUING'
        if scheme == 'Default Status':
            return 'DEFAULT' if ag.is_severely_delinquent else 'CURRENT'
        if scheme == 'Drawn Undrawn Status':
            return 'DRAWN' if ag.balance_amt > 0 else 'UNDRAWN'
        if scheme == 'Frozen Status':
            return FROZEN_STATUS_ROW['Agreement_Status_Cd'] if ag.is_frozen else 'NOT_FROZEN'
        if scheme == 'Past Due Status':
            if ag.is_severely_delinquent:
                return 'DPD_90'
            if ag.is_delinquent:
                return 'DPD_30'
            return 'CURRENT'
        raise ValueError(f"Unknown scheme: {scheme}")

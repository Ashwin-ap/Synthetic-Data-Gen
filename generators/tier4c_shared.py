from __future__ import annotations

from datetime import datetime, time
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import pandas as pd

from config.code_values import CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD, LANGUAGE_USAGE_TYPES
from config.settings import HIGH_DATE, HISTORY_START
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

_TIER4C_DI_START_TS = '2000-01-01 00:00:00.000000'
_LANGUAGE_USAGE_TYPES = LANGUAGE_USAGE_TYPES
_CHURNED_TRANSITION_DT = HISTORY_START
_BANKRUPT_MOD = 90       # ~1.1% of individuals at seed=42 (~33 of 2400)
_SPECIALTY_MOD = 10      # ~10% of all parties
_ID_TYPES_INDIVIDUAL: Tuple[str, ...] = ('SSN', "Driver's License", 'Passport')
_PROFILE_LANG_BY_ETHNICITY: Dict[str, str] = {'HISPANIC': 'ES', 'ASIAN': 'ZH'}
_CONTACT_PREF_CHANNEL_BY_INTERNET: Dict[bool, int] = {True: 3, False: 1}
_CONTACT_PREF_TYPES: Tuple[int, ...] = (1, 2)
_SCORE_TYPE_CD_FICO = 'FICO'
# 9_999_999 reuses same reserved BIGINT as BANK_PARTY_ID/SELF_EMP_ORG_ID — credit bureau placeholder
_CREDIT_BUREAU_REPORTING_PARTY_ID = 9_999_999
# 9_999_999 reused as issuing party placeholder — no separate party row required
_ISSUING_PARTY_ID = 9_999_999
_REQUIRED_TIER0_TABLES: Tuple[str, ...] = (
    'Core_DB.LANGUAGE_TYPE',
    'Core_DB.SPECIALTY_TYPE',
    'Core_DB.DATA_SOURCE_TYPE',
)
_REQUIRED_TIER2_TABLES: Tuple[str, ...] = (
    'Core_DB.ANALYTICAL_MODEL',
    'Core_DB.MARKET_SEGMENT',
)

# Each entry: (value_cd, range_start_val, range_end_val, desc)
_DEMOGRAPHIC_CODES: Dict[str, List[Tuple[str, Optional[str], Optional[str], str]]] = {
    'AGE_BAND': [
        ('UNDER_35', '18', '34',  'Age 18-34'),
        ('35_44',    '35', '44',  'Age 35-44'),
        ('45_54',    '45', '54',  'Age 45-54'),
        ('55_64',    '55', '64',  'Age 55-64'),
        ('65_PLUS',  '65', None,  'Age 65 and over'),
    ],
    'INCOME_QUARTILE': [
        ('Q1', None, None, 'Income Quartile 1 (lowest)'),
        ('Q2', None, None, 'Income Quartile 2'),
        ('Q3', None, None, 'Income Quartile 3'),
        ('Q4', None, None, 'Income Quartile 4 (highest)'),
    ],
    'DEPENDENTS': [
        ('NONE',       '0', '0',  'No dependents'),
        ('ONE_TO_TWO', '1', '2',  '1-2 dependents'),
        ('THREE_PLUS', '3', None, '3 or more dependents'),
    ],
}

_COLS_PARTY_LANGUAGE_USAGE = [
    'Party_Id', 'Language_Type_Cd', 'Language_Usage_Type_Cd',
    'Party_Language_Start_Dttm', 'Party_Language_End_Dttm', 'Party_Language_Priority_Num',
]
_COLS_PARTY_STATUS = ['Party_Id', 'Party_Status_Cd', 'Party_Status_Dt']
_COLS_PARTY_SCORE = ['Party_Id', 'Model_Id', 'Model_Run_Id', 'Party_Score_Val']
_COLS_PARTY_CREDIT_REPORT_SCORE = [
    'Reporting_Party_Id', 'Obligor_Party_Id', 'Credit_Report_Dttm',
    'Score_Type_Cd', 'Credit_Report_Score_Num',
]
_COLS_PARTY_IDENTIFICATION = [
    'Party_Id', 'Issuing_Party_Id', 'Party_Identification_Type_Cd',
    'Party_Identification_Start_Dttm', 'Party_Identification_End_Dttm',
    'Party_Identification_Num', 'Party_Identification_Receipt_Dt',
    'Party_Identification_Primary_Ind', 'Party_Identification_Name',
]
_COLS_PARTY_DEMOGRAPHIC = [
    'Party_Id', 'Demographic_Cd', 'Data_Source_Type_Cd', 'Party_Demographic_Start_Dt',
    'Demographic_Value_Cd', 'Party_Demographic_End_Dt', 'Party_Demographic_Num',
    'Party_Demographic_Val',
]
_COLS_DEMOGRAPHIC_VALUE = [
    'Demographic_Cd', 'Demographic_Value_Cd', 'Demographic_Range_Start_Val',
    'Demographic_Range_End_Val', 'Demographic_Value_Desc', 'Demographic_Val',
]
_COLS_PARTY_SEGMENT = [
    'Party_Id', 'Market_Segment_Id', 'Party_Segment_Start_Dttm', 'Party_Segment_End_Dttm',
]
_COLS_PARTY_SPECIALTY = [
    'Party_Id', 'Specialty_Type_Cd', 'Party_Specialty_Start_Dt', 'Party_Specialty_End_Dt',
]
_COLS_PARTY_CONTACT_PREFERENCE = [
    'Party_Id', 'Channel_Type_Cd', 'Contact_Preference_Type_Cd',
    'Party_Contact_Preference_Start_Dt', 'Party_Contact_Preference_End_Dt',
    'Party_Contact_Preference_Priority_Num', 'Protocol_Type_Cd', 'Days_Cd', 'Hours_Cd',
]


def _age_band(age: int) -> str:
    if age < 35:
        return 'UNDER_35'
    if age < 45:
        return '35_44'
    if age < 55:
        return '45_54'
    if age < 65:
        return '55_64'
    return '65_PLUS'


def _dependents_band(n: int) -> str:
    if n == 0:
        return 'NONE'
    if n <= 2:
        return 'ONE_TO_TWO'
    return 'THREE_PLUS'


class Tier4cShared(BaseGenerator):

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # --- Guards ---
        if not ctx.customers:
            raise RuntimeError(
                'Tier4cShared requires a populated ctx.customers — run UniverseBuilder.build() first'
            )
        for key in _REQUIRED_TIER0_TABLES + _REQUIRED_TIER2_TABLES:
            if key not in ctx.tables:
                raise RuntimeError(f'Tier4cShared requires {key} to be loaded first')

        am_df = ctx.tables['Core_DB.ANALYTICAL_MODEL']
        ms_df = ctx.tables['Core_DB.MARKET_SEGMENT']

        prof_rows = am_df[am_df['Model_Purpose_Cd'] == CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD]
        if prof_rows.empty:
            raise RuntimeError(
                'Tier4cShared requires an ANALYTICAL_MODEL row with '
                'Model_Purpose_Cd=customer profitability — Step 10 did not emit it'
            )
        # iloc[0] is deterministic because Step 10's template order is fixed
        prof_model_id = int(prof_rows.iloc[0]['Model_Id'])
        # ANALYTICAL_MODEL has no Model_Run_Id column; read it from MARKET_SEGMENT
        # (Step 10 seeds Model_Run_Id=1 on all segment rows — that is the only run in the system)
        prof_model_run_id = int(ms_df['Model_Run_Id'].iloc[0])
        # fallback: deterministic modulo index; actual CLV-scheme filter is applied if column exists
        clv_rows = ms_df
        for col in ms_df.columns:
            matches = ms_df[ms_df[col].astype(str).str.upper().str.contains('CLV', na=False)]
            if len(matches) >= 10:
                clv_rows = matches
                break
        clv_to_segment_id: Dict[int, int] = {
            decile: int(clv_rows['Market_Segment_Id'].iloc[(decile - 1) % len(clv_rows)])
            for decile in range(1, 11)
        }
        if len(clv_to_segment_id) != 10:
            raise RuntimeError(
                'Tier4cShared requires MARKET_SEGMENT rows for all 10 CLV deciles '
                '— Step 10 emitted fewer'
            )

        # --- Pre-computations ---
        cps = ctx.customers
        ind_cps = [cp for cp in cps if cp.party_type == 'INDIVIDUAL']
        specialty_pool = sorted(
            ctx.tables['Core_DB.SPECIALTY_TYPE']['Specialty_Type_Cd'].tolist()
        )

        # --- DEMOGRAPHIC_VALUE (12 rows — seeded inline, no seed_data/*.py) ---
        dv_rows = []
        for demo_cd, values in _DEMOGRAPHIC_CODES.items():
            for val_cd, rstart, rend, desc in values:
                dv_rows.append({
                    'Demographic_Cd':            demo_cd,
                    'Demographic_Value_Cd':       val_cd,
                    'Demographic_Range_Start_Val': rstart,
                    'Demographic_Range_End_Val':   rend,
                    'Demographic_Value_Desc':      desc,
                    'Demographic_Val':             None,
                })
        dv_df = pd.DataFrame(dv_rows, columns=_COLS_DEMOGRAPHIC_VALUE)
        dv_df = self.stamp_di(dv_df, start_ts=_TIER4C_DI_START_TS)

        # --- PARTY_LANGUAGE_USAGE (~6,000 rows — all parties × 2) ---
        lang_rows = []
        for cp in cps:
            lang_cd = _PROFILE_LANG_BY_ETHNICITY.get(cp.ethnicity_type_cd or '', 'EN')
            start_dttm = datetime.combine(cp.party_since, time(0, 0))
            for i, usage_type in enumerate(_LANGUAGE_USAGE_TYPES, start=1):
                lang_rows.append({
                    'Party_Id':                    cp.party_id,
                    'Language_Type_Cd':            lang_cd,
                    'Language_Usage_Type_Cd':      usage_type,
                    'Party_Language_Start_Dttm':   start_dttm,
                    'Party_Language_End_Dttm':     None,
                    'Party_Language_Priority_Num': str(i),
                })
        lang_df = pd.DataFrame(lang_rows, columns=_COLS_PARTY_LANGUAGE_USAGE)
        lang_df['Party_Id'] = lang_df['Party_Id'].astype('Int64')
        lang_df = self.stamp_di(lang_df, start_ts=_TIER4C_DI_START_TS)

        # --- PARTY_STATUS (~3,150 rows) ---
        status_rows = []
        for cp in cps:
            if cp.lifecycle_cohort == 'CHURNED':
                status_rows.append({
                    'Party_Id':        cp.party_id,
                    'Party_Status_Cd': 'ACTIVE',
                    'Party_Status_Dt': cp.party_since,
                })
                status_rows.append({
                    'Party_Id':        cp.party_id,
                    'Party_Status_Cd': 'CHURNED',
                    'Party_Status_Dt': _CHURNED_TRANSITION_DT,
                })
            elif (
                cp.party_type == 'INDIVIDUAL'
                and cp.lifecycle_cohort != 'CHURNED'
                and cp.party_id % _BANKRUPT_MOD == 0
            ):
                status_rows.append({
                    'Party_Id':        cp.party_id,
                    'Party_Status_Cd': 'BANKRUPT',
                    'Party_Status_Dt': cp.party_since,
                })
            else:
                status_rows.append({
                    'Party_Id':        cp.party_id,
                    'Party_Status_Cd': 'ACTIVE',
                    'Party_Status_Dt': cp.party_since,
                })
        status_df = pd.DataFrame(status_rows, columns=_COLS_PARTY_STATUS)
        status_df['Party_Id'] = status_df['Party_Id'].astype('Int64')
        status_df = self.stamp_di(status_df, start_ts=_TIER4C_DI_START_TS)

        # --- PARTY_SCORE (~3,000 rows — all parties × 1) ---
        score_rows = [
            {
                'Party_Id':       cp.party_id,
                'Model_Id':       prof_model_id,
                'Model_Run_Id':   prof_model_run_id,
                'Party_Score_Val': f'{(cp.party_id % 10000) / 10000:.4f}',
            }
            for cp in cps
        ]
        score_df = pd.DataFrame(score_rows, columns=_COLS_PARTY_SCORE)
        for col in ('Party_Id', 'Model_Id', 'Model_Run_Id'):
            score_df[col] = score_df[col].astype('Int64')
        score_df = self.stamp_di(score_df, start_ts=_TIER4C_DI_START_TS)

        # --- PARTY_CREDIT_REPORT_SCORE (~2,400 rows — INDIVIDUAL only × 1) ---
        credit_rows = [
            {
                'Reporting_Party_Id':    _CREDIT_BUREAU_REPORTING_PARTY_ID,
                'Obligor_Party_Id':      cp.party_id,
                'Credit_Report_Dttm':    datetime.combine(cp.party_since, time(9, 0, 0)),
                'Score_Type_Cd':         _SCORE_TYPE_CD_FICO,
                'Credit_Report_Score_Num': str(cp.fico_score),
            }
            for cp in ind_cps
        ]
        credit_df = pd.DataFrame(credit_rows, columns=_COLS_PARTY_CREDIT_REPORT_SCORE)
        for col in ('Reporting_Party_Id', 'Obligor_Party_Id'):
            credit_df[col] = credit_df[col].astype('Int64')
        credit_df = self.stamp_di(credit_df, start_ts=_TIER4C_DI_START_TS)

        # --- PARTY_IDENTIFICATION (~7,200 rows — INDIVIDUAL only × 3) ---
        ident_rows = []
        for cp in ind_cps:
            start_dttm = datetime.combine(cp.party_since, time(0, 0))
            for type_cd in _ID_TYPES_INDIVIDUAL:
                ident_rows.append({
                    'Party_Id':                       cp.party_id,
                    'Issuing_Party_Id':               _ISSUING_PARTY_ID,
                    'Party_Identification_Type_Cd':   type_cd,
                    'Party_Identification_Start_Dttm': start_dttm,
                    'Party_Identification_End_Dttm':  None,
                    'Party_Identification_Num':       f'{type_cd[:3].upper()}-{cp.party_id:09d}',
                    'Party_Identification_Receipt_Dt': cp.party_since,
                    'Party_Identification_Primary_Ind': 'Yes' if type_cd == 'SSN' else 'No',
                    'Party_Identification_Name':      type_cd,
                })
        ident_df = pd.DataFrame(ident_rows, columns=_COLS_PARTY_IDENTIFICATION)
        for col in ('Party_Id', 'Issuing_Party_Id'):
            ident_df[col] = ident_df[col].astype('Int64')
        ident_df = self.stamp_di(ident_df, start_ts=_TIER4C_DI_START_TS)

        # --- PARTY_DEMOGRAPHIC (~7,200 rows — INDIVIDUAL only × 3) ---
        demo_rows = []
        for cp in ind_cps:
            value_cd_by_code = {
                'AGE_BAND':        _age_band(cp.age),
                'INCOME_QUARTILE': f'Q{cp.income_quartile}',
                'DEPENDENTS':      _dependents_band(cp.num_dependents),
            }
            for demo_cd in ('AGE_BAND', 'INCOME_QUARTILE', 'DEPENDENTS'):
                demo_rows.append({
                    'Party_Id':                 cp.party_id,
                    'Demographic_Cd':           demo_cd,
                    'Data_Source_Type_Cd':      'CORE_BANKING',
                    'Party_Demographic_Start_Dt': cp.party_since,
                    'Demographic_Value_Cd':     value_cd_by_code[demo_cd],
                    'Party_Demographic_End_Dt': None,
                    'Party_Demographic_Num':    None,
                    'Party_Demographic_Val':    None,
                })
        demo_df = pd.DataFrame(demo_rows, columns=_COLS_PARTY_DEMOGRAPHIC)
        demo_df['Party_Id'] = demo_df['Party_Id'].astype('Int64')
        demo_df = self.stamp_di(demo_df, start_ts=_TIER4C_DI_START_TS)

        # --- PARTY_SEGMENT (~3,000 rows — all parties × 1) ---
        segment_rows = [
            {
                'Party_Id':                cp.party_id,
                'Market_Segment_Id':       clv_to_segment_id[cp.clv_segment],
                'Party_Segment_Start_Dttm': datetime.combine(cp.party_since, time(0, 0)),
                'Party_Segment_End_Dttm':  None,
            }
            for cp in cps
        ]
        segment_df = pd.DataFrame(segment_rows, columns=_COLS_PARTY_SEGMENT)
        for col in ('Party_Id', 'Market_Segment_Id'):
            segment_df[col] = segment_df[col].astype('Int64')
        segment_df = self.stamp_di(segment_df, start_ts=_TIER4C_DI_START_TS)

        # --- PARTY_SPECIALTY (~300 rows — every 10th party, all types) ---
        specialty_rows = []
        for cp in cps:
            if cp.party_id % _SPECIALTY_MOD == 0:
                specialty_rows.append({
                    'Party_Id':               cp.party_id,
                    'Specialty_Type_Cd':      specialty_pool[cp.party_id % len(specialty_pool)],
                    'Party_Specialty_Start_Dt': cp.party_since,
                    'Party_Specialty_End_Dt': None,
                })
        specialty_df = pd.DataFrame(specialty_rows, columns=_COLS_PARTY_SPECIALTY)
        specialty_df['Party_Id'] = specialty_df['Party_Id'].astype('Int64')
        specialty_df = self.stamp_di(specialty_df, start_ts=_TIER4C_DI_START_TS)

        # --- PARTY_CONTACT_PREFERENCE (~6,000 rows — all parties × 2) ---
        contact_rows = []
        for cp in cps:
            channel = _CONTACT_PREF_CHANNEL_BY_INTERNET[cp.has_internet]
            for pref_type in _CONTACT_PREF_TYPES:
                contact_rows.append({
                    'Party_Id':                            cp.party_id,
                    'Channel_Type_Cd':                    channel,
                    'Contact_Preference_Type_Cd':         pref_type,
                    'Party_Contact_Preference_Start_Dt':  cp.party_since,
                    'Party_Contact_Preference_End_Dt':    HIGH_DATE,  # NOT NULL sentinel
                    'Party_Contact_Preference_Priority_Num': 1,
                    'Protocol_Type_Cd':                   1,
                    'Days_Cd':                            1,
                    'Hours_Cd':                           1,
                })
        contact_df = pd.DataFrame(contact_rows, columns=_COLS_PARTY_CONTACT_PREFERENCE)
        contact_df['Party_Id'] = contact_df['Party_Id'].astype('Int64')
        contact_df = self.stamp_di(contact_df, start_ts=_TIER4C_DI_START_TS)

        return {
            'Core_DB.PARTY_LANGUAGE_USAGE':       lang_df,
            'Core_DB.PARTY_STATUS':               status_df,
            'Core_DB.PARTY_SCORE':                score_df,
            'Core_DB.PARTY_CREDIT_REPORT_SCORE':  credit_df,
            'Core_DB.PARTY_IDENTIFICATION':       ident_df,
            'Core_DB.PARTY_DEMOGRAPHIC':          demo_df,
            'Core_DB.DEMOGRAPHIC_VALUE':          dv_df,
            'Core_DB.PARTY_SEGMENT':              segment_df,
            'Core_DB.PARTY_SPECIALTY':            specialty_df,
            'Core_DB.PARTY_CONTACT_PREFERENCE':   contact_df,
        }

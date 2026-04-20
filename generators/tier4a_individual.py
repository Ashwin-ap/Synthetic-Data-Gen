from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING, Dict, List

import pandas as pd
from faker import Faker

from config.settings import BANK_PARTY_ID, HIGH_DATE, SEED, SELF_EMP_ORG_ID
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

_TIER4A_DI_START_TS = '2000-01-01 00:00:00.000000'

_GENDER_PRONOUN_BY_GENDER: Dict[str, str] = {'MALE': 'HE', 'FEMALE': 'SHE'}

_VIP_BY_CLV_SEGMENT: Dict[int, str] = {10: 'PLATINUM', 9: 'GOLD', 8: 'SILVER'}

_JOB_TITLE_BY_OCCUPATION: Dict[str, str] = {
    'EMP': 'Analyst',
    'SELF_EMP': 'Business Owner',
    'RETIRED': 'Retired',
    'NOT_WORKING': 'Not Employed',
}

_ASSOCIATE_SAMPLING_MOD = 50

_SKILL_POOL: List[str] = [
    'ACCOUNTING', 'ENGINEERING', 'SALES', 'NURSING', 'CARPENTRY',
    'TEACHING', 'PROGRAMMING', 'MANAGEMENT', 'DRIVING', 'COOKING',
    'LEGAL', 'MEDICINE', 'ADMIN', 'FINANCE', 'MARKETING',
]

_SPECIAL_NEED_POOL: List[str] = [
    'NONE', 'VISUAL_IMPAIRMENT', 'HEARING_IMPAIRMENT', 'MOBILITY_IMPAIRMENT',
    'COGNITIVE', 'SPEECH', 'OTHER',
]

_REQUIRED_TIER0_TABLES = (
    'Core_DB.GENDER_PRONOUN',
    'Core_DB.MARITAL_STATUS_TYPE',
    'Core_DB.VERY_IMPORTANT_PERSON_TYPE',
    'Core_DB.OCCUPATION_TYPE',
    'Core_DB.MILITARY_STATUS_TYPE',
    'Core_DB.GENERAL_MEDICAL_STATUS_TYPE',
    'Core_DB.DATA_SOURCE_TYPE',
    'Core_DB.SKILL_TYPE',
    'Core_DB.SPECIAL_NEED_TYPE',
    'Core_DB.TIME_PERIOD_TYPE',
)

_REQUIRED_TIER3_TABLES = ('Core_DB.ORGANIZATION',)

# DDL business-column order (source: references/07_mvp-schema-reference.md)
_COLS_INDIVIDUAL_NAME = [
    'Individual_Party_Id', 'Name_Type_Cd', 'Individual_Name_Start_Dt',
    'Given_Name', 'Middle_Name', 'Family_Name', 'Birth_Family_Name',
    'Name_Prefix_Txt', 'Name_Suffix_Txt', 'Individual_Name_End_Dt', 'Individual_Full_Name',
]
_COLS_INDIVIDUAL_GENDER_PRONOUN = [
    'Gender_Pronoun_Start_Dt', 'Gender_Pronoun_End_Dt', 'Self_reported_Ind',
    'Individual_Party_Id', 'Gender_Pronoun_Type_Cd', 'Gender_Pronoun_Cd',
]
_COLS_INDIVIDUAL_MARITAL_STATUS = [
    'Individual_Party_Id', 'Individual_Marital_Status_Start_Dt',
    'Marital_Status_Cd', 'Individual_Marital_Status_End_Dt',
]
_COLS_INDIVIDUAL_VIP_STATUS = [
    'Individual_Party_Id', 'Individual_VIP_Status_Start_Dt',
    'VIP_Type_Cd', 'Individual_VIP_Status_End_Dt',
]
_COLS_INDIVIDUAL_OCCUPATION = [
    'Individual_Party_Id', 'Occupation_Type_Cd', 'Individual_Occupation_Start_Dt',
    'Individual_Occupation_End_Dt', 'Individual_Job_Title_Txt',
]
_COLS_INDIVIDUAL_MILITARY_STATUS = [
    'Individual_Party_Id', 'Individual_Military_Start_Dt',
    'Military_Status_Type_Cd', 'Individual_Military_End_Dt',
]
_COLS_INDIVIDUAL_MEDICAL = [
    'Individual_Party_Id', 'Data_Source_Type_Cd', 'Individual_Medical_Start_Dt',
    'Individual_Medical_End_Dt', 'Physical_Exam_Dt', 'General_Medical_Status_Cd',
    'Last_Menstrual_Period_Dt', 'Last_X_ray_Dt', 'Estimated_Pregnancy_Due_Dt',
]
_COLS_INDIVIDUAL_SKILL = ['Individual_Party_Id', 'Skill_Cd', 'Individual_Skill_Dt']
_COLS_INDIVIDUAL_SPECIAL_NEED = ['Individual_Party_Id', 'Special_Need_Cd']
_COLS_INDIVIDUAL_PAY_TIMING = [
    'Individual_Party_Id', 'Business_Party_Id', 'Pay_Day_Num', 'Time_Period_Cd',
]
_COLS_INDIVIDUAL_BONUS_TIMING = [
    'Individual_Party_Id', 'Bonus_Month_Num', 'Business_Party_Id',
]
_COLS_ASSOCIATE_EMPLOYMENT = [
    'Associate_Party_Id', 'Organization_Party_Id', 'Associate_Employment_Start_Dt',
    'Associate_Employment_End_Dt', 'Associate_Hire_Dt',
    'Associate_Termination_Dttm', 'Associate_HR_Num',
]

_EPOCH = date(1970, 1, 1)


# ---------------------------------------------------------------------------
# Pure deterministic helpers (no RNG — party_id modulo only)
# ---------------------------------------------------------------------------

# Military: party_id % 100: 0–6 → VETERAN (7%), 7–9 → ACTIVE_DUTY (3%), 10–99 → CIVILIAN (90%)
def _military_status_for(party_id: int) -> str:
    r = party_id % 100
    if r <= 6:
        return 'VETERAN'
    if r <= 9:
        return 'ACTIVE_DUTY'
    return 'CIVILIAN'


# Medical: party_id % 10: 0–6 → HEALTHY (70%), 7 → CHRONIC_CONDITION, 8 → ACUTE_CONDITION, 9 → UNKNOWN
def _medical_status_for(party_id: int) -> str:
    r = party_id % 10
    if r <= 6:
        return 'HEALTHY'
    if r == 7:
        return 'CHRONIC_CONDITION'
    if r == 8:
        return 'ACUTE_CONDITION'
    return 'UNKNOWN'


# Special need: party_id % 100: 0–84 → NONE (85%), 85–89 → VISUAL_IMPAIRMENT,
# 90–93 → HEARING_IMPAIRMENT, 94–96 → MOBILITY_IMPAIRMENT,
# 97 → COGNITIVE, 98 → SPEECH, 99 → OTHER
def _special_need_for(party_id: int) -> str:
    r = party_id % 100
    if r <= 84:
        return 'NONE'
    if r <= 89:
        return 'VISUAL_IMPAIRMENT'
    if r <= 93:
        return 'HEARING_IMPAIRMENT'
    if r <= 96:
        return 'MOBILITY_IMPAIRMENT'
    if r == 97:
        return 'COGNITIVE'
    if r == 98:
        return 'SPEECH'
    return 'OTHER'


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class Tier4aIndividual(BaseGenerator):
    """Projects every INDIVIDUAL CustomerProfile onto 12 Core_DB attribute tables."""

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # --- Fail-fast guards ---
        if not ctx.customers:
            raise RuntimeError(
                'Tier4aIndividual requires a populated ctx.customers — run UniverseBuilder.build() first'
            )
        for key in _REQUIRED_TIER0_TABLES + _REQUIRED_TIER3_TABLES:
            if key not in ctx.tables:
                raise RuntimeError(f'Tier4aIndividual requires Tier 0 table {key} to be loaded first')
        org_df = ctx.tables.get('Core_DB.ORGANIZATION')
        if org_df is None or SELF_EMP_ORG_ID not in org_df['Organization_Party_Id'].values:
            raise RuntimeError('SELF_EMP_ORG_ID row missing from Core_DB.ORGANIZATION — Step 11 incomplete')

        # --- Pre-computations ---
        fake = Faker('en_US')
        fake.seed_instance(SEED)

        ind_cps = [cp for cp in ctx.customers if cp.party_type == 'INDIVIDUAL']
        real_org_ids = sorted(set(org_df['Organization_Party_Id']) - {SELF_EMP_ORG_ID})

        def emp_org_for(party_id: int) -> int:
            return real_org_ids[party_id % len(real_org_ids)]

        # --- INDIVIDUAL_NAME ---
        name_rows = []
        for cp in ind_cps:
            given = fake.first_name_male() if cp.gender_type_cd == 'MALE' else fake.first_name_female()
            middle = fake.first_name()
            family = fake.last_name()
            name_rows.append({
                'Individual_Party_Id':      cp.party_id,
                'Name_Type_Cd':             'legal',
                'Individual_Name_Start_Dt': cp.party_since,
                'Given_Name':               given,
                'Middle_Name':              middle,
                'Family_Name':              family,
                'Birth_Family_Name':        None,
                'Name_Prefix_Txt':          None,
                'Name_Suffix_Txt':          None,
                'Individual_Name_End_Dt':   HIGH_DATE,  # Layer 2 #3 exception: must not be NULL
                'Individual_Full_Name':     f'{given} {middle} {family}',
            })
        df_name = pd.DataFrame(name_rows, columns=_COLS_INDIVIDUAL_NAME)
        df_name['Individual_Party_Id'] = df_name['Individual_Party_Id'].astype('Int64')
        df_name = self.stamp_di(df_name, start_ts=_TIER4A_DI_START_TS)

        # --- INDIVIDUAL_GENDER_PRONOUN ---
        gp_rows = []
        for cp in ind_cps:
            gp_rows.append({
                'Gender_Pronoun_Start_Dt':  cp.party_since,
                'Gender_Pronoun_End_Dt':    None,
                'Self_reported_Ind':        'No',  # CHAR(3)
                'Individual_Party_Id':      cp.party_id,
                'Gender_Pronoun_Type_Cd':   'subjective',
                'Gender_Pronoun_Cd':        _GENDER_PRONOUN_BY_GENDER[cp.gender_type_cd],
            })
        df_gp = pd.DataFrame(gp_rows, columns=_COLS_INDIVIDUAL_GENDER_PRONOUN)
        df_gp['Individual_Party_Id'] = df_gp['Individual_Party_Id'].astype('Int64')
        df_gp = self.stamp_di(df_gp, start_ts=_TIER4A_DI_START_TS)

        # --- INDIVIDUAL_MARITAL_STATUS ---
        ms_rows = []
        for cp in ind_cps:
            ms_rows.append({
                'Individual_Party_Id':                  cp.party_id,
                'Individual_Marital_Status_Start_Dt':   cp.party_since,
                'Marital_Status_Cd':                    cp.marital_status_cd,
                'Individual_Marital_Status_End_Dt':     None,
            })
        df_ms = pd.DataFrame(ms_rows, columns=_COLS_INDIVIDUAL_MARITAL_STATUS)
        df_ms['Individual_Party_Id'] = df_ms['Individual_Party_Id'].astype('Int64')
        df_ms = self.stamp_di(df_ms, start_ts=_TIER4A_DI_START_TS)

        # --- INDIVIDUAL_VIP_STATUS ---
        vip_rows = []
        for cp in ind_cps:
            vip_rows.append({
                'Individual_Party_Id':           cp.party_id,
                'Individual_VIP_Status_Start_Dt': cp.party_since,
                'VIP_Type_Cd':                   _VIP_BY_CLV_SEGMENT.get(cp.clv_segment, 'NONE'),
                'Individual_VIP_Status_End_Dt':  None,
            })
        df_vip = pd.DataFrame(vip_rows, columns=_COLS_INDIVIDUAL_VIP_STATUS)
        df_vip['Individual_Party_Id'] = df_vip['Individual_Party_Id'].astype('Int64')
        df_vip = self.stamp_di(df_vip, start_ts=_TIER4A_DI_START_TS)

        # --- INDIVIDUAL_OCCUPATION ---
        occ_rows = []
        for cp in ind_cps:
            occ_start = max(cp.party_since - timedelta(days=3650), _EPOCH)
            occ_rows.append({
                'Individual_Party_Id':          cp.party_id,
                'Occupation_Type_Cd':           cp.occupation_cd,
                'Individual_Occupation_Start_Dt': occ_start,
                'Individual_Occupation_End_Dt': None,
                'Individual_Job_Title_Txt':     _JOB_TITLE_BY_OCCUPATION[cp.occupation_cd],
            })
        df_occ = pd.DataFrame(occ_rows, columns=_COLS_INDIVIDUAL_OCCUPATION)
        df_occ['Individual_Party_Id'] = df_occ['Individual_Party_Id'].astype('Int64')
        df_occ = self.stamp_di(df_occ, start_ts=_TIER4A_DI_START_TS)

        # --- INDIVIDUAL_MILITARY_STATUS ---
        mil_rows = []
        for cp in ind_cps:
            mil_rows.append({
                'Individual_Party_Id':       cp.party_id,
                'Individual_Military_Start_Dt': cp.party_since,
                'Military_Status_Type_Cd':   _military_status_for(cp.party_id),
                'Individual_Military_End_Dt': None,
            })
        df_mil = pd.DataFrame(mil_rows, columns=_COLS_INDIVIDUAL_MILITARY_STATUS)
        df_mil['Individual_Party_Id'] = df_mil['Individual_Party_Id'].astype('Int64')
        df_mil = self.stamp_di(df_mil, start_ts=_TIER4A_DI_START_TS)

        # --- INDIVIDUAL_MEDICAL ---
        med_rows = []
        for cp in ind_cps:
            med_rows.append({
                'Individual_Party_Id':          cp.party_id,
                'Data_Source_Type_Cd':          'CORE_BANKING',
                'Individual_Medical_Start_Dt':  cp.party_since,
                'Individual_Medical_End_Dt':    None,
                'Physical_Exam_Dt':             None,
                'General_Medical_Status_Cd':    _medical_status_for(cp.party_id),
                'Last_Menstrual_Period_Dt':      None,
                'Last_X_ray_Dt':                None,
                'Estimated_Pregnancy_Due_Dt':   None,
            })
        df_med = pd.DataFrame(med_rows, columns=_COLS_INDIVIDUAL_MEDICAL)
        df_med['Individual_Party_Id'] = df_med['Individual_Party_Id'].astype('Int64')
        df_med = self.stamp_di(df_med, start_ts=_TIER4A_DI_START_TS)

        # --- INDIVIDUAL_SKILL ---
        skill_rows = []
        for cp in ind_cps:
            skill_rows.append({
                'Individual_Party_Id': cp.party_id,
                'Skill_Cd':            _SKILL_POOL[cp.party_id % len(_SKILL_POOL)],
                'Individual_Skill_Dt': cp.party_since,
            })
        df_skill = pd.DataFrame(skill_rows, columns=_COLS_INDIVIDUAL_SKILL)
        df_skill['Individual_Party_Id'] = df_skill['Individual_Party_Id'].astype('Int64')
        df_skill = self.stamp_di(df_skill, start_ts=_TIER4A_DI_START_TS)

        # --- INDIVIDUAL_SPECIAL_NEED ---
        sn_rows = []
        for cp in ind_cps:
            sn_rows.append({
                'Individual_Party_Id': cp.party_id,
                'Special_Need_Cd':     _special_need_for(cp.party_id),
            })
        df_sn = pd.DataFrame(sn_rows, columns=_COLS_INDIVIDUAL_SPECIAL_NEED)
        df_sn['Individual_Party_Id'] = df_sn['Individual_Party_Id'].astype('Int64')
        df_sn = self.stamp_di(df_sn, start_ts=_TIER4A_DI_START_TS)

        # --- INDIVIDUAL_PAY_TIMING and INDIVIDUAL_BONUS_TIMING (EMP + SELF_EMP only) ---
        pay_rows = []
        bonus_rows = []
        for cp in ind_cps:
            if cp.occupation_cd not in {'EMP', 'SELF_EMP'}:
                continue
            biz_id = SELF_EMP_ORG_ID if cp.occupation_cd == 'SELF_EMP' else emp_org_for(cp.party_id)
            pay_rows.append({
                'Individual_Party_Id': cp.party_id,
                'Business_Party_Id':   biz_id,
                'Pay_Day_Num':         '15',
                'Time_Period_Cd':      'MONTH',
            })
            bonus_rows.append({
                'Individual_Party_Id': cp.party_id,
                'Bonus_Month_Num':     '12',
                'Business_Party_Id':   biz_id,
            })

        df_pay = pd.DataFrame(pay_rows, columns=_COLS_INDIVIDUAL_PAY_TIMING)
        for col in ('Individual_Party_Id', 'Business_Party_Id'):
            df_pay[col] = df_pay[col].astype('Int64')
        df_pay = self.stamp_di(df_pay, start_ts=_TIER4A_DI_START_TS)

        df_bonus = pd.DataFrame(bonus_rows, columns=_COLS_INDIVIDUAL_BONUS_TIMING)
        for col in ('Individual_Party_Id', 'Business_Party_Id'):
            df_bonus[col] = df_bonus[col].astype('Int64')
        df_bonus = self.stamp_di(df_bonus, start_ts=_TIER4A_DI_START_TS)

        # --- ASSOCIATE_EMPLOYMENT (~2% of EMP, deterministic) ---
        assoc_rows = []
        for cp in ind_cps:
            if cp.occupation_cd != 'EMP':
                continue
            if cp.party_id % _ASSOCIATE_SAMPLING_MOD != 0:
                continue
            emp_start = max(cp.party_since - timedelta(days=365), _EPOCH)
            hire_dt = max(cp.party_since - timedelta(days=730), _EPOCH)
            assoc_rows.append({
                'Associate_Party_Id':              cp.party_id,
                'Organization_Party_Id':           BANK_PARTY_ID,
                'Associate_Employment_Start_Dt':   emp_start,
                'Associate_Employment_End_Dt':     None,
                'Associate_Hire_Dt':               hire_dt,
                'Associate_Termination_Dttm':      None,
                'Associate_HR_Num':                f'HR-{cp.party_id:07d}',
            })
        df_assoc = pd.DataFrame(assoc_rows, columns=_COLS_ASSOCIATE_EMPLOYMENT)
        for col in ('Associate_Party_Id', 'Organization_Party_Id'):
            df_assoc[col] = df_assoc[col].astype('Int64')
        df_assoc = self.stamp_di(df_assoc, start_ts=_TIER4A_DI_START_TS)

        return {
            'Core_DB.INDIVIDUAL_NAME':            df_name,
            'Core_DB.INDIVIDUAL_GENDER_PRONOUN':  df_gp,
            'Core_DB.INDIVIDUAL_MARITAL_STATUS':  df_ms,
            'Core_DB.INDIVIDUAL_VIP_STATUS':      df_vip,
            'Core_DB.INDIVIDUAL_OCCUPATION':      df_occ,
            'Core_DB.INDIVIDUAL_MILITARY_STATUS': df_mil,
            'Core_DB.INDIVIDUAL_MEDICAL':         df_med,
            'Core_DB.INDIVIDUAL_SKILL':           df_skill,
            'Core_DB.INDIVIDUAL_SPECIAL_NEED':    df_sn,
            'Core_DB.INDIVIDUAL_PAY_TIMING':      df_pay,
            'Core_DB.INDIVIDUAL_BONUS_TIMING':    df_bonus,
            'Core_DB.ASSOCIATE_EMPLOYMENT':       df_assoc,
        }

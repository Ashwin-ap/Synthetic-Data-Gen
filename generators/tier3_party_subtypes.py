from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, Dict

import pandas as pd

from config.settings import SELF_EMP_ORG_ID, SIM_DATE
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ── Constants ────────────────────────────────────────────────────────────────

_TIER3_DI_START_TS = '2000-01-01 00:00:00.000000'

# Birth_Dt: deterministic month/day jitter prevents same-age individuals collapsing to
# one date. Month = (party_id % 12) + 1 (1–12). Day = min(28, (party_id//12 % 28) + 1)
# so it is valid in every month including February.

_TAX_BRACKET_BY_QUARTILE: Dict[int, str] = {
    1: 'BRACKET_12',
    2: 'BRACKET_22',
    3: 'BRACKET_24',
    4: 'BRACKET_32',
}

# Single stable bracket for org entities — no income_quartile available for orgs.
_ORG_TAX_BRACKET = 'BRACKET_22'

_REQUIRED_TIER0_TABLES = (
    'Core_DB.GENDER_TYPE',
    'Core_DB.ETHNICITY_TYPE',
    'Core_DB.TAX_BRACKET_TYPE',
    'Core_DB.NATIONALITY_TYPE',
    'Core_DB.LEGAL_CLASSIFICATION',
    'Core_DB.BUSINESS_CATEGORY',
)

# ── Column lists (DDL declaration order per references/07_mvp-schema-reference.md) ──

_COLS_INDIVIDUAL = [
    'Individual_Party_Id', 'Birth_Dt', 'Death_Dt', 'Gender_Type_Cd',
    'Ethnicity_Type_Cd', 'Tax_Bracket_Cd', 'Retirement_Dt', 'Employment_Start_Dt',
    'Nationality_Cd', 'Name_Only_No_Pronoun_Ind',
]

_COLS_ORGANIZATION = [
    'Organization_Party_Id', 'Organization_Type_Cd', 'Organization_Established_Dttm',
    'Parent_Organization_Party_Id', 'Organization_Size_Type_Cd', 'Legal_Classification_Cd',
    'Ownership_Type_Cd', 'Organization_Close_Dt', 'Organization_Operation_Dt',
    'Organization_Fiscal_Month_Num', 'Organization_Fiscal_Day_Num',
    'Basel_Organization_Type_Cd', 'Basel_Market_Participant_Cd',
    'Basel_Eligible_Central_Ind', 'BIC_Business_Alpha_4_Cd',
]

_COLS_BUSINESS = [
    'Business_Party_Id', 'Business_Category_Cd', 'Business_Legal_Start_Dt',
    'Business_Legal_End_Dt', 'Tax_Bracket_Cd', 'Customer_Location_Type_Cd',
    'Stock_Exchange_Listed_Ind',
]

_LEGAL_CLASS_CYCLE = ['LLC', 'CORPORATION', 'PARTNERSHIP']
_BIZ_CATEGORY_CYCLE = ['SMALL_BUSINESS', 'MID_MARKET', 'ENTERPRISE', 'MICRO_BUSINESS']


# ── Generator ─────────────────────────────────────────────────────────────────

class Tier3PartySubtypes(BaseGenerator):
    """Emits Core_DB.INDIVIDUAL, ORGANIZATION, and BUSINESS DataFrames.

    Pure projection of ctx.customers — no statistical decisions, no ID minting,
    no randomness. The reserved SELF_EMP_ORG_ID placeholder row is injected into
    ORGANIZATION so downstream tiers (INDIVIDUAL_PAY_TIMING, INDIVIDUAL_BONUS_TIMING)
    have a valid FK target for self-employed individuals.
    """

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # ── Guards ────────────────────────────────────────────────────────────
        if not ctx.customers:
            raise RuntimeError(
                'Tier3PartySubtypes requires a populated ctx.customers'
                ' — run UniverseBuilder.build() first'
            )
        for key in _REQUIRED_TIER0_TABLES:
            if key not in ctx.tables:
                raise RuntimeError(
                    f'Tier3PartySubtypes requires Tier 0 table {key} to be loaded first'
                )

        # ── Partition customers ───────────────────────────────────────────────
        ind_cps = [cp for cp in ctx.customers if cp.party_type == 'INDIVIDUAL']
        org_cps = [cp for cp in ctx.customers if cp.party_type == 'ORGANIZATION']

        # ── INDIVIDUAL ────────────────────────────────────────────────────────
        ind_rows = []
        for cp in ind_cps:
            birth_month = (cp.party_id % 12) + 1
            birth_day = min(28, (cp.party_id // 12 % 28) + 1)
            ind_rows.append({
                'Individual_Party_Id':      cp.party_id,
                'Birth_Dt':                 date(SIM_DATE.year - cp.age, birth_month, birth_day),
                'Death_Dt':                 None,
                'Gender_Type_Cd':           cp.gender_type_cd,
                'Ethnicity_Type_Cd':        cp.ethnicity_type_cd,
                'Tax_Bracket_Cd':           _TAX_BRACKET_BY_QUARTILE[cp.income_quartile],
                'Retirement_Dt':            None,
                'Employment_Start_Dt':      None,
                'Nationality_Cd':           'USA',
                'Name_Only_No_Pronoun_Ind': 'No',
            })

        df_ind = pd.DataFrame(ind_rows, columns=_COLS_INDIVIDUAL)
        df_ind['Individual_Party_Id'] = df_ind['Individual_Party_Id'].astype('Int64')

        # ── ORGANIZATION (regular rows + reserved placeholder) ────────────────
        org_rows = []
        for cp in org_cps:
            established = datetime.combine(cp.party_since, time(0, 0)) - timedelta(days=3650)
            org_rows.append({
                'Organization_Party_Id':        cp.party_id,
                'Organization_Type_Cd':         'COMMERCIAL',
                'Organization_Established_Dttm': established,
                'Parent_Organization_Party_Id': None,
                'Organization_Size_Type_Cd':    'SMALL',
                'Legal_Classification_Cd':      _LEGAL_CLASS_CYCLE[cp.party_id % 3],
                'Ownership_Type_Cd':            None,
                'Organization_Close_Dt':        None,
                'Organization_Operation_Dt':    cp.party_since,
                'Organization_Fiscal_Month_Num': '12',
                'Organization_Fiscal_Day_Num':  '31',
                'Basel_Organization_Type_Cd':   None,
                'Basel_Market_Participant_Cd':  None,
                'Basel_Eligible_Central_Ind':   'No',
                'BIC_Business_Alpha_4_Cd':      None,
            })

        # Reserved placeholder — FK target for INDIVIDUAL_PAY_TIMING/BONUS_TIMING
        # for self-employed individuals (PRD §7.12). Not in Core_DB.PARTY.
        org_rows.append({
            'Organization_Party_Id':        SELF_EMP_ORG_ID,
            'Organization_Type_Cd':         'PLACEHOLDER',
            'Organization_Established_Dttm': None,
            'Parent_Organization_Party_Id': None,
            'Organization_Size_Type_Cd':    None,
            'Legal_Classification_Cd':      'SOLE_PROPRIETORSHIP',
            'Ownership_Type_Cd':            None,
            'Organization_Close_Dt':        None,
            'Organization_Operation_Dt':    None,
            'Organization_Fiscal_Month_Num': None,
            'Organization_Fiscal_Day_Num':  None,
            'Basel_Organization_Type_Cd':   None,
            'Basel_Market_Participant_Cd':  None,
            'Basel_Eligible_Central_Ind':   None,
            'BIC_Business_Alpha_4_Cd':      None,
        })

        df_org = pd.DataFrame(org_rows, columns=_COLS_ORGANIZATION)
        df_org['Organization_Party_Id']        = df_org['Organization_Party_Id'].astype('Int64')
        df_org['Parent_Organization_Party_Id'] = df_org['Parent_Organization_Party_Id'].astype('Int64')

        # ── BUSINESS (1:1 with real org customers; no placeholder row) ────────
        biz_rows = []
        for cp in org_cps:
            biz_rows.append({
                'Business_Party_Id':        cp.party_id,
                'Business_Category_Cd':     _BIZ_CATEGORY_CYCLE[cp.party_id % 4],
                'Business_Legal_Start_Dt':  cp.party_since - timedelta(days=3650),
                'Business_Legal_End_Dt':    None,
                'Tax_Bracket_Cd':           _ORG_TAX_BRACKET,
                'Customer_Location_Type_Cd': None,
                'Stock_Exchange_Listed_Ind': 'No',
            })

        df_biz = pd.DataFrame(biz_rows, columns=_COLS_BUSINESS)
        df_biz['Business_Party_Id'] = df_biz['Business_Party_Id'].astype('Int64')

        # ── DI stamping (Core_DB only — no stamp_valid) ───────────────────────
        df_ind = self.stamp_di(df_ind, start_ts=_TIER3_DI_START_TS)
        df_org = self.stamp_di(df_org, start_ts=_TIER3_DI_START_TS)
        df_biz = self.stamp_di(df_biz, start_ts=_TIER3_DI_START_TS)

        return {
            'Core_DB.INDIVIDUAL':   df_ind,
            'Core_DB.ORGANIZATION': df_org,
            'Core_DB.BUSINESS':     df_biz,
        }

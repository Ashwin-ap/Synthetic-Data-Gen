from __future__ import annotations

from datetime import date, datetime, time
from typing import TYPE_CHECKING, Dict, List

import pandas as pd

from config.settings import BANK_PARTY_ID, HISTORY_START, SIM_DATE  # noqa: F401
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

_TIER9_DI_START_TS = '2000-01-01 00:00:00.000000'

_CUSTOMER_ROLE_CD = 'customer'
_BORROWER_ROLE_CD = 'borrower'
_CUSTOMER_OF_ENTERPRISE_CD = 'customer of enterprise'
_PARTY_STRUCTURE_TYPE_CD = 'banking_relationship'
_CLAIM_ROLE_CD = 'claimant'
_PARTY_CLAIM_CONTACT_PROHIBITED_NO = 'No'
_PARTY_CLAIM_RATE = 0.02

_CREDIT_PRODUCT_TYPES: frozenset = frozenset({
    'CREDIT_CARD', 'VEHICLE_LOAN', 'STUDENT_LOAN',
    'MORTGAGE', 'HELOC', 'PAYDAY',
})

_REQUIRED_UPSTREAM_TABLES = ('Core_DB.PARTY', 'Core_DB.AGREEMENT')

_COLS_PARTY_AGREEMENT: List[str] = [
    'Party_Id', 'Agreement_Id', 'Party_Agreement_Role_Cd',
    'Party_Agreement_Start_Dt', 'Party_Agreement_End_Dt',
    'Allocation_Pct', 'Party_Agreement_Amt',
    'Party_Agreement_Currency_Amt', 'Party_Agreement_Num',
]
_COLS_PARTY_RELATED: List[str] = [
    'Party_Id', 'Related_Party_Id', 'Party_Related_Role_Cd',
    'Party_Related_Start_Dttm', 'Party_Related_End_Dttm',
    'Party_Structure_Type_Cd', 'Party_Related_Status_Reason_Cd',
    'Party_Related_Status_Type_Cd', 'Party_Related_Subtype_Cd',
]
_COLS_PARTY_CLAIM: List[str] = [
    'Claim_Id', 'Party_Id', 'Party_Claim_Role_Cd',
    'Party_Claim_Start_Dttm', 'Party_Claim_End_Dttm',
    'Party_Claim_Contact_Prohibited_Ind',
]


class Tier9PartyAgreement(BaseGenerator):
    """Tier 9 — Party-Agreement Links.

    Produces PARTY_AGREEMENT, PARTY_RELATED, and PARTY_CLAIM for Core_DB.
    Every agreement gets a 'customer' role row; every credit agreement also
    gets a 'borrower' row.  Every customer gets a 'customer of enterprise'
    row linked to BANK_PARTY_ID.  ~2% of customers receive a standalone claim.
    """

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # Guard: upstream prerequisites
        if not ctx.customers:
            raise RuntimeError('Tier 9 prerequisite missing: ctx.customers is empty')
        if not ctx.agreements:
            raise RuntimeError('Tier 9 prerequisite missing: ctx.agreements is empty')
        for key in _REQUIRED_UPSTREAM_TABLES:
            if key not in ctx.tables:
                raise RuntimeError(f'Tier 9 prerequisite missing: {key}')
        party_ids = set(ctx.tables['Core_DB.PARTY']['Party_Id'].astype(int))
        if BANK_PARTY_ID not in party_ids:
            raise RuntimeError(
                f'Tier 9 prerequisite missing: BANK_PARTY_ID={BANK_PARTY_ID} not in Core_DB.PARTY'
            )

        df_pa = self.stamp_di(self._build_party_agreement(ctx), start_ts=_TIER9_DI_START_TS)
        df_pr = self.stamp_di(self._build_party_related(ctx), start_ts=_TIER9_DI_START_TS)
        df_pc = self.stamp_di(self._build_party_claim(ctx), start_ts=_TIER9_DI_START_TS)

        return {
            'Core_DB.PARTY_AGREEMENT': df_pa,
            'Core_DB.PARTY_RELATED': df_pr,
            'Core_DB.PARTY_CLAIM': df_pc,
        }

    # ------------------------------------------------------------------
    # Private builders
    # ------------------------------------------------------------------

    def _build_party_agreement(self, ctx: 'GenerationContext') -> pd.DataFrame:
        rows: List[dict] = []
        for ag in ctx.agreements:
            start_dt: date = ag.open_dttm.date()
            end_dt = ag.close_dttm.date() if ag.close_dttm is not None else None

            rows.append({
                'Party_Id': ag.owner_party_id,
                'Agreement_Id': ag.agreement_id,
                'Party_Agreement_Role_Cd': _CUSTOMER_ROLE_CD,
                'Party_Agreement_Start_Dt': start_dt,
                'Party_Agreement_End_Dt': end_dt,
                'Allocation_Pct': None,
                'Party_Agreement_Amt': None,
                'Party_Agreement_Currency_Amt': None,
                'Party_Agreement_Num': None,
            })

            if ag.is_credit:
                rows.append({
                    'Party_Id': ag.owner_party_id,
                    'Agreement_Id': ag.agreement_id,
                    'Party_Agreement_Role_Cd': _BORROWER_ROLE_CD,
                    'Party_Agreement_Start_Dt': start_dt,
                    'Party_Agreement_End_Dt': end_dt,
                    'Allocation_Pct': None,
                    'Party_Agreement_Amt': None,
                    'Party_Agreement_Currency_Amt': None,
                    'Party_Agreement_Num': None,
                })

        df = pd.DataFrame(rows, columns=_COLS_PARTY_AGREEMENT)
        df['Party_Id'] = df['Party_Id'].astype('Int64')
        df['Agreement_Id'] = df['Agreement_Id'].astype('Int64')
        return df

    def _build_party_related(self, ctx: 'GenerationContext') -> pd.DataFrame:
        _midnight = time.min
        rows: List[dict] = []
        for cp in ctx.customers:
            rows.append({
                'Party_Id': cp.party_id,
                'Related_Party_Id': BANK_PARTY_ID,
                'Party_Related_Role_Cd': _CUSTOMER_OF_ENTERPRISE_CD,
                'Party_Related_Start_Dttm': datetime.combine(cp.party_since, _midnight),
                'Party_Related_End_Dttm': None,
                'Party_Structure_Type_Cd': _PARTY_STRUCTURE_TYPE_CD,
                'Party_Related_Status_Reason_Cd': None,
                'Party_Related_Status_Type_Cd': None,
                'Party_Related_Subtype_Cd': None,
            })

        df = pd.DataFrame(rows, columns=_COLS_PARTY_RELATED)
        df['Party_Id'] = df['Party_Id'].astype('Int64')
        df['Related_Party_Id'] = df['Related_Party_Id'].astype('Int64')
        return df

    def _build_party_claim(self, ctx: 'GenerationContext') -> pd.DataFrame:
        _claim_start = datetime.combine(HISTORY_START, time.min)
        rows: List[dict] = []
        for cp in ctx.customers:
            if ctx.rng.random() < _PARTY_CLAIM_RATE:
                rows.append({
                    'Claim_Id': ctx.ids.next('claim'),
                    'Party_Id': cp.party_id,
                    'Party_Claim_Role_Cd': _CLAIM_ROLE_CD,
                    'Party_Claim_Start_Dttm': _claim_start,
                    'Party_Claim_End_Dttm': None,
                    'Party_Claim_Contact_Prohibited_Ind': _PARTY_CLAIM_CONTACT_PROHIBITED_NO,
                })

        df = pd.DataFrame(rows, columns=_COLS_PARTY_CLAIM)
        if not df.empty:
            df['Claim_Id'] = df['Claim_Id'].astype('Int64')
            df['Party_Id'] = df['Party_Id'].astype('Int64')
        return df

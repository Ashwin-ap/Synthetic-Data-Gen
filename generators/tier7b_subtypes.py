from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import pandas as pd

from config.settings import SIM_DATE
from generators.base import BaseGenerator
from utils.luhn import generate_card_number, generate_cvv

if TYPE_CHECKING:
    from registry.context import GenerationContext

_TIER7B_DI_START_TS = '2000-01-01 00:00:00.000000'
_BANKING_BOOK_CD = 'BANKING_BOOK'

_FINANCIAL_AGREEMENT_TYPE_BY_PRODUCT: Dict[str, str] = {
    'CHECKING':               'DEPOSIT',
    'SAVINGS':                'DEPOSIT',
    'MMA':                    'DEPOSIT',
    'RETIREMENT':             'DEPOSIT',
    'COMMERCIAL_CHECKING':    'DEPOSIT',
    'CERTIFICATE_OF_DEPOSIT': 'DEPOSIT',
    'CREDIT_CARD':            'CREDIT',
    'HELOC':                  'CREDIT',
    'VEHICLE_LOAN':           'LOAN',
    'STUDENT_LOAN':           'LOAN',
    'MORTGAGE':               'LOAN',
    'PAYDAY':                 'LOAN',
}

_INTEREST_DISBURSEMENT_BY_PRODUCT: Dict[str, str] = {
    'CHECKING':               'COMPOUNDED',
    'SAVINGS':                'COMPOUNDED',
    'MMA':                    'COMPOUNDED',
    'COMMERCIAL_CHECKING':    'COMPOUNDED',
    'RETIREMENT':             'ACCRUED',
    'CERTIFICATE_OF_DEPOSIT': 'SIMPLE',
}

# CD maturity subtype bucketing — deterministic by ag.agreement_id % 6
_CD_MATURITY_SUBTYPES: List[str] = ['3M', '6M', '12M', '24M', '36M', '60M']

_DEPOSIT_MATURITY_DAYS: Dict[str, int] = {
    '3M': 91, '6M': 183, '12M': 365, '24M': 730, '36M': 1095, '60M': 1825,
}

_SECURITY_TYPE_BY_PRODUCT: Dict[str, str] = {
    'VEHICLE_LOAN': 'VEHICLE',
    'MORTGAGE':     'REAL_ESTATE',
    'STUDENT_LOAN': 'UNSECURED',
}

_LOAN_MATURITY_BY_PRODUCT: Dict[str, str] = {
    'VEHICLE_LOAN': 'SHORT_TERM',
    'STUDENT_LOAN': 'MEDIUM_TERM',
    'MORTGAGE':     'LONG_TERM',
}

_LOAN_MATURITY_YEARS: Dict[str, int] = {
    'VEHICLE_LOAN': 5,
    'STUDENT_LOAN': 10,
    'MORTGAGE':     30,
}

_LOAN_TERM_SUBTYPE_BY_PRODUCT: Dict[str, str] = {
    'VEHICLE_LOAN': 'INSTALLMENT',
    'STUDENT_LOAN': 'INSTALLMENT',
    'MORTGAGE':     'AMORTIZING',
}

_AMORTIZATION_METHOD_BY_PRODUCT: Dict[str, str] = {
    'VEHICLE_LOAN': 'LEVEL_PAYMENT',
    'STUDENT_LOAN': 'LEVEL_PAYMENT',
    'MORTGAGE':     'LEVEL_PAYMENT',
}

# ⚠️ Conflict A — literals not in PURCHASE_INTENT_TYPE; different semantic domain; no FK declared
_OBLIGOR_BORROWING_PURPOSE_BY_PRODUCT: Dict[str, str] = {
    'CREDIT_CARD':  'GENERAL',
    'HELOC':        'HOME_IMPROVEMENT',
    'VEHICLE_LOAN': 'VEHICLE',
    'STUDENT_LOAN': 'EDUCATION',
    'MORTGAGE':     'HOME_PURCHASE',
}

# ⚠️ Conflict B — no seed table; no FK declared in DDL
_CREDIT_GRACE_PERIOD_BY_PRODUCT: Dict[str, str] = {
    'CREDIT_CARD':  '25_DAYS',
    'HELOC':        '30_DAYS',
    'VEHICLE_LOAN': 'NONE',
    'STUDENT_LOAN': 'NONE',
    'MORTGAGE':     'NONE',
}

# Mortgage type bucketing — deterministic by ag.agreement_id % 5; HELOC excluded (own product)
_MORTGAGE_TYPES: List[str] = ['FIXED_RATE', 'ARM', 'FHA', 'VA', 'JUMBO']

# Credit-card subtype bucketing — deterministic by ag.agreement_id % 5
_CC_SUBTYPES: List[str] = ['STANDARD', 'REWARDS', 'SECURED', 'BUSINESS', 'STUDENT']

# ⚠️ Conflict C — no seed table; VISA/MASTERCARD/AMEX/DISCOVER used as authoritative literals
_CARD_ASSOCIATION_TYPES: Tuple[str, ...] = ('VISA', 'MASTERCARD', 'AMEX', 'DISCOVER')

_CARD_BIN_BY_ASSOCIATION: Dict[str, str] = {
    'VISA':       '400000',
    'MASTERCARD': '510000',
    'AMEX':       '340000',
    'DISCOVER':   '601100',
}

_CARD_NAME_BY_ASSOCIATION: Dict[str, str] = {
    'VISA':       'Visa Platinum',
    'MASTERCARD': 'Mastercard Gold',
    'AMEX':       'Amex Blue',
    'DISCOVER':   'Discover It',
}

_REQUIRED_UPSTREAM_TABLES: Tuple[str, ...] = (
    'Core_DB.FINANCIAL_AGREEMENT_TYPE',
    'Core_DB.MARKET_RISK_TYPE',
    'Core_DB.DEPOSIT_MATURITY_SUBTYPE',
    'Core_DB.INTEREST_DISBURSEMENT_TYPE',
    'Core_DB.LOAN_MATURITY_SUBTYPE',
    'Core_DB.LOAN_TERM_SUBTYPE',
    'Core_DB.LOAN_TRANSACTION_SUBTYPE',
    'Core_DB.AMORTIZATION_METHOD_TYPE',
    'Core_DB.SECURITY_TYPE',
    'Core_DB.CREDIT_CARD_AGREEMENT_SUBTYPE',
    'Core_DB.MORTGAGE_TYPE',
    'Core_DB.AGREEMENT',
)

# DDL column order (business cols only; DI tail appended by stamp_di)
_COLS_FINANCIAL_AGREEMENT = [
    'Agreement_Id', 'Financial_Agreement_Subtype_Cd', 'Market_Risk_Type_Cd',
    'Original_Maturity_Dt', 'Risk_Exposure_Mitigant_Subtype_Cd', 'Trading_Book_Cd',
    'Pricing_Method_Subtype_Cd', 'Financial_Agreement_Type_Cd', 'Day_Count_Basis_Cd',
    'ISO_8583_Account_Type_Cd',
]
_COLS_DEPOSIT_AGREEMENT = [
    'Agreement_Id', 'Deposit_Maturity_Subtype_Cd', 'Interest_Disbursement_Type_Cd',
    'Deposit_Ownership_Type_Cd', 'Original_Deposit_Amt', 'Original_Deposit_Dt',
    'Agreement_Currency_Original_Deposit_Amt',
]
_COLS_DEPOSIT_TERM_AGREEMENT = [
    'Agreement_Id', 'Next_Term_Maturity_Dt', 'Grace_Period_End_Dt',
]
_COLS_CREDIT_AGREEMENT = [
    'Agreement_Id', 'Seniority_Level_Cd', 'Credit_Agreement_Reaging_Cnt',
    'Credit_Agreement_Past_Due_Amt', 'Credit_Agreement_Charge_Off_Amt',
    'Credit_Agreement_Impairment_Amt', 'Credit_Agreement_Settlement_Dt',
    'Credit_Agreement_Subtype_Cd', 'Obligor_Borrowing_Purpose_Cd',
    'Agreement_Currency_Past_Due_Amt', 'Agreement_Currency_Charge_Off_Amt',
    'Agreement_Currency_Last_Payment_Amt', 'Agreement_Currency_Impairment_Amt',
    'Specialized_Lending_Type_Cd', 'Credit_Agreement_Grace_Period_Cd',
    'Payment_Frequency_Time_Period_Cd', 'Credit_Agreement_Last_Payment_Amt',
    'Credit_Agreement_Last_Payment_Dt',
]
_COLS_LOAN_AGREEMENT = [
    'Agreement_Id', 'Loan_Maturity_Subtype_Cd', 'Security_Type_Cd', 'Due_Day_Num',
    'Realizable_Collateral_Amt', 'Loan_Payoff_Amt',
    'Agreement_Currency_Real_Collateral_Amt', 'Agreement_Currency_Loan_Payoff_Amt',
]
_COLS_LOAN_TERM_AGREEMENT = [
    'Agreement_Id', 'Amortization_Method_Cd', 'Amortization_End_Dt', 'Balloon_Amt',
    'Loan_Term_Subtype_Cd', 'Original_Loan_Amt', 'Preapproved_Loan_Amt',
    'Maximum_Monthly_Payment_Amt', 'Improvement_Allocation_Amt',
    'Debt_Payment_Allocation_Amt', 'Down_Payment_Amt', 'Loan_Maturity_Dt',
    'Loan_Termination_Dt', 'Loan_Renewal_Dt', 'Commit_Start_Dt', 'Commit_End_Dt',
    'Payoff_Dt', 'Loan_Asset_Purchase_Dt', 'Agreement_Currency_Balloon_Amt',
    'Agreement_Currency_Original_Loan_Amt', 'Agreement_Currency_Preapproved_Amt',
    'Agreement_Currency_Maximum_Monthly_Payment_Amt',
    'Agreement_Currency_Improve_Allocation_Amt',
    'Agreement_Currency_Debt_Payment_Allocation_Amt', 'Loan_Refinance_Ind',
    'Agreement_Currency_Down_Payment_Amt', 'Agreement_Currency_Down_Payment_Borrow_Amt',
]
_COLS_LOAN_TRANSACTION_AGREEMENT = [
    'Agreement_Id', 'Loan_Transaction_Subtype_Cd',
]
_COLS_MORTGAGE_AGREEMENT = [
    'Agreement_Id', 'First_Time_Mortgage_Ind', 'Closing_Cost_Amt',
    'Adjustable_Payment_Cap_Amt', 'Prepayment_Penalty_Dt', 'Early_Payoff_Penalty_Amt',
    'Agreement_Currency_Closing_Cost_Amt', 'Agreement_Currency_Adjustable_Cap_Amt',
    'Agreement_Currency_Early_Penalty_Amt', 'Mortgage_Type_Cd',
]
_COLS_CREDIT_CARD_AGREEMENT = [
    'Agreement_Id', 'Credit_Card_Agreement_Subtype_Cd', 'Credit_Card_Activation_Dttm',
]
_COLS_CARD = [
    'Access_Device_Id', 'Card_Subtype_Cd', 'Card_Association_Type_Cd',
    'Technology_Type_Cd', 'Card_Num', 'Card_Sequence_Num', 'Card_Expiration_Dt',
    'Card_Issue_Dt', 'Card_Activation_Dt', 'Card_Deactivation_Dt', 'Card_Name',
    'Card_Encrypted_Num', 'Card_Manufacture_Dt', 'Card_Replacement_Order_Dt',
    'Language_Type_Cd', 'Bank_Identification_Num', 'Card_Security_Code_Num',
]


class Tier7bSubtypes(BaseGenerator):
    """Generates 10 Core_DB agreement sub-type + CARD tables (Tier 7b).

    Fans out each AgreementProfile into the correct exclusive sub-type path
    based on is_* flags set atomically by UniverseBuilder. No sub-typing
    decisions are made here — only deterministic column population.
    CARD rows are Luhn-valid via utils.luhn; all other fields are deterministic.
    """

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # --- A. Guards ---
        if not ctx.agreements:
            raise RuntimeError(
                'Tier 7b prerequisite missing: ctx.agreements is empty'
            )
        missing = [t for t in _REQUIRED_UPSTREAM_TABLES if t not in ctx.tables]
        if missing:
            raise RuntimeError(f'Tier 7b prerequisite missing: {missing}')

        # --- B. Pre-build lookups ---
        owner_age_by_party_id = {cp.party_id: cp.age for cp in ctx.customers}

        # --- C. Row collectors ---
        fin_rows: List[dict] = []
        dep_rows: List[dict] = []
        td_rows:  List[dict] = []
        cr_rows:  List[dict] = []
        la_rows:  List[dict] = []
        lta_rows: List[dict] = []
        lx_rows:  List[dict] = []
        mg_rows:  List[dict] = []
        cc_rows:  List[dict] = []
        card_rows: List[dict] = []

        # --- D. Single pass over all agreements ---
        for ag in ctx.agreements:
            open_dt: date = ag.open_dttm.date()

            # ── FINANCIAL_AGREEMENT (all agreements have is_financial=True) ──
            if ag.is_financial:
                pt = ag.product_type
                if pt == 'MORTGAGE':
                    maturity_dt: Optional[date] = open_dt + timedelta(days=365 * 30)
                elif pt == 'VEHICLE_LOAN':
                    maturity_dt = open_dt + timedelta(days=365 * 5)
                elif pt == 'STUDENT_LOAN':
                    maturity_dt = open_dt + timedelta(days=365 * 10)
                elif pt == 'CERTIFICATE_OF_DEPOSIT':
                    cd_sub = _CD_MATURITY_SUBTYPES[ag.agreement_id % 6]
                    maturity_dt = open_dt + timedelta(days=_DEPOSIT_MATURITY_DAYS[cd_sub])
                else:
                    maturity_dt = None

                fin_rows.append({
                    'Agreement_Id':                      ag.agreement_id,
                    'Financial_Agreement_Subtype_Cd':    ag.agreement_subtype_cd,
                    'Market_Risk_Type_Cd':               _BANKING_BOOK_CD,
                    'Original_Maturity_Dt':              maturity_dt,
                    'Risk_Exposure_Mitigant_Subtype_Cd': None,
                    'Trading_Book_Cd':                   None,
                    'Pricing_Method_Subtype_Cd':         None,
                    'Financial_Agreement_Type_Cd':       _FINANCIAL_AGREEMENT_TYPE_BY_PRODUCT[pt],
                    'Day_Count_Basis_Cd':                None,
                    'ISO_8583_Account_Type_Cd':          None,
                })

            # ── DEPOSIT_AGREEMENT ──
            if ag.is_deposit:
                pt = ag.product_type
                mat_sub: Optional[str] = (
                    _CD_MATURITY_SUBTYPES[ag.agreement_id % 6]
                    if pt == 'CERTIFICATE_OF_DEPOSIT' else None
                )
                dep_rows.append({
                    'Agreement_Id':                          ag.agreement_id,
                    'Deposit_Maturity_Subtype_Cd':           mat_sub,
                    'Interest_Disbursement_Type_Cd':         _INTEREST_DISBURSEMENT_BY_PRODUCT[pt],
                    'Deposit_Ownership_Type_Cd':             None,
                    'Original_Deposit_Amt':                  ag.balance_amt,
                    'Original_Deposit_Dt':                   open_dt,
                    'Agreement_Currency_Original_Deposit_Amt': ag.balance_amt,
                })

            # ── DEPOSIT_TERM_AGREEMENT (CDs only) ──
            if ag.is_term_deposit:
                cd_sub = _CD_MATURITY_SUBTYPES[ag.agreement_id % 6]
                next_mat = open_dt + timedelta(days=_DEPOSIT_MATURITY_DAYS[cd_sub])
                td_rows.append({
                    'Agreement_Id':        ag.agreement_id,
                    'Next_Term_Maturity_Dt': next_mat,
                    'Grace_Period_End_Dt': next_mat + timedelta(days=10),
                })

            # ── CREDIT_AGREEMENT ──
            if ag.is_credit:
                pt = ag.product_type
                months_since_open = (
                    (SIM_DATE.year - ag.open_dttm.year) * 12
                    + (SIM_DATE.month - ag.open_dttm.month)
                )
                months_elapsed = max(months_since_open - 1, 0)
                last_payment_dt = open_dt + timedelta(days=30 * months_elapsed)
                last_payment_amt = ag.balance_amt * Decimal('0.02')

                past_due_amt: Optional[Decimal] = (
                    ag.balance_amt * Decimal('0.03') if ag.is_delinquent else None
                )
                charge_off_amt: Optional[Decimal] = (
                    ag.balance_amt * Decimal('0.10') if ag.is_severely_delinquent else None
                )
                cr_rows.append({
                    'Agreement_Id':                       ag.agreement_id,
                    'Seniority_Level_Cd':                 None,  # ⚠️ Conflict D: no seed table
                    'Credit_Agreement_Reaging_Cnt':       0,
                    'Credit_Agreement_Past_Due_Amt':      past_due_amt,
                    'Credit_Agreement_Charge_Off_Amt':    charge_off_amt,
                    'Credit_Agreement_Impairment_Amt':    None,
                    'Credit_Agreement_Settlement_Dt':     None,
                    'Credit_Agreement_Subtype_Cd':        ag.agreement_subtype_cd,
                    'Obligor_Borrowing_Purpose_Cd':       _OBLIGOR_BORROWING_PURPOSE_BY_PRODUCT[pt],
                    'Agreement_Currency_Past_Due_Amt':    past_due_amt,
                    'Agreement_Currency_Charge_Off_Amt':  None,
                    'Agreement_Currency_Last_Payment_Amt': last_payment_amt,
                    'Agreement_Currency_Impairment_Amt':  None,
                    'Specialized_Lending_Type_Cd':        None,
                    'Credit_Agreement_Grace_Period_Cd':   _CREDIT_GRACE_PERIOD_BY_PRODUCT[pt],
                    'Payment_Frequency_Time_Period_Cd':   'MONTH',
                    'Credit_Agreement_Last_Payment_Amt':  last_payment_amt,
                    'Credit_Agreement_Last_Payment_Dt':   last_payment_dt,
                })

            # ── LOAN_AGREEMENT (vehicle/student/mortgage) ──
            if ag.is_loan_term:
                pt = ag.product_type
                collateral: Optional[Decimal] = (
                    ag.original_loan_amt * Decimal('1.10')
                    if pt in ('VEHICLE_LOAN', 'MORTGAGE') else None
                )
                la_rows.append({
                    'Agreement_Id':                       ag.agreement_id,
                    'Loan_Maturity_Subtype_Cd':           _LOAN_MATURITY_BY_PRODUCT[pt],
                    'Security_Type_Cd':                   _SECURITY_TYPE_BY_PRODUCT[pt],
                    'Due_Day_Num':                        str(ag.open_dttm.day),
                    'Realizable_Collateral_Amt':          collateral,
                    'Loan_Payoff_Amt':                    ag.balance_amt,
                    'Agreement_Currency_Real_Collateral_Amt': collateral,
                    'Agreement_Currency_Loan_Payoff_Amt': ag.balance_amt,
                })

            # ── LOAN_TERM_AGREEMENT (vehicle/student/mortgage) ──
            if ag.is_loan_term:
                pt = ag.product_type
                years = _LOAN_MATURITY_YEARS[pt]
                total_months = years * 12
                mat_dt = open_dt + timedelta(days=365 * years)
                max_monthly = (
                    ag.original_loan_amt / Decimal(str(total_months)) * Decimal('1.3')
                )
                down_pmt: Decimal = (
                    ag.original_loan_amt * Decimal('0.20')
                    if pt == 'MORTGAGE' else Decimal('0')
                )
                lta_rows.append({
                    'Agreement_Id':                               ag.agreement_id,
                    'Amortization_Method_Cd':                    _AMORTIZATION_METHOD_BY_PRODUCT[pt],
                    'Amortization_End_Dt':                       mat_dt,
                    'Balloon_Amt':                               None,
                    'Loan_Term_Subtype_Cd':                      _LOAN_TERM_SUBTYPE_BY_PRODUCT[pt],
                    'Original_Loan_Amt':                         ag.original_loan_amt,
                    'Preapproved_Loan_Amt':                      None,
                    'Maximum_Monthly_Payment_Amt':               max_monthly,
                    'Improvement_Allocation_Amt':                None,
                    'Debt_Payment_Allocation_Amt':               None,
                    'Down_Payment_Amt':                          down_pmt,
                    'Loan_Maturity_Dt':                          mat_dt,
                    'Loan_Termination_Dt':                       None,
                    'Loan_Renewal_Dt':                           None,
                    'Commit_Start_Dt':                           None,
                    'Commit_End_Dt':                             None,
                    'Payoff_Dt':                                 None,
                    'Loan_Asset_Purchase_Dt':                    None,
                    'Agreement_Currency_Balloon_Amt':            None,
                    'Agreement_Currency_Original_Loan_Amt':      ag.original_loan_amt,
                    'Agreement_Currency_Preapproved_Amt':        None,
                    'Agreement_Currency_Maximum_Monthly_Payment_Amt': max_monthly,
                    'Agreement_Currency_Improve_Allocation_Amt': None,
                    'Agreement_Currency_Debt_Payment_Allocation_Amt': None,
                    'Loan_Refinance_Ind':                        'No',
                    'Agreement_Currency_Down_Payment_Amt':       down_pmt,
                    'Agreement_Currency_Down_Payment_Borrow_Amt': None,
                })

            # ── LOAN_TRANSACTION_AGREEMENT (payday only) ──
            if ag.is_loan_transaction:
                lx_rows.append({
                    'Agreement_Id':              ag.agreement_id,
                    'Loan_Transaction_Subtype_Cd': 'PAYDAY',
                })

            # ── MORTGAGE_AGREEMENT ──
            if ag.is_mortgage:
                mortgage_type = _MORTGAGE_TYPES[ag.agreement_id % 5]
                owner_age = owner_age_by_party_id.get(ag.owner_party_id, 99)
                first_time = 'Yes' if owner_age < 35 else 'No'
                adj_cap: Optional[Decimal] = (
                    ag.original_loan_amt * Decimal('1.2')
                    if mortgage_type == 'ARM' else None
                )
                mg_rows.append({
                    'Agreement_Id':                      ag.agreement_id,
                    'First_Time_Mortgage_Ind':           first_time,
                    'Closing_Cost_Amt':                  ag.original_loan_amt * Decimal('0.03'),
                    'Adjustable_Payment_Cap_Amt':        adj_cap,
                    'Prepayment_Penalty_Dt':             open_dt + timedelta(days=365 * 3),
                    'Early_Payoff_Penalty_Amt':          ag.original_loan_amt * Decimal('0.01'),
                    'Agreement_Currency_Closing_Cost_Amt': ag.original_loan_amt * Decimal('0.03'),
                    'Agreement_Currency_Adjustable_Cap_Amt': adj_cap,
                    'Agreement_Currency_Early_Penalty_Amt': ag.original_loan_amt * Decimal('0.01'),
                    'Mortgage_Type_Cd':                  mortgage_type,
                })

            # ── CREDIT_CARD_AGREEMENT + CREDIT CARD row ──
            if ag.is_credit_card:
                cc_rows.append({
                    'Agreement_Id':                     ag.agreement_id,
                    'Credit_Card_Agreement_Subtype_Cd': _CC_SUBTYPES[ag.agreement_id % 5],
                    'Credit_Card_Activation_Dttm':      ag.open_dttm,
                })
                card_rows.append(
                    self._build_card_row(ctx, ag, 'CREDIT')
                )

            # ── DEBIT CARD row (checking deposits) ──
            if ag.product_type in ('CHECKING', 'COMMERCIAL_CHECKING'):
                card_rows.append(
                    self._build_card_row(ctx, ag, 'DEBIT')
                )

        # --- E. Build DataFrames ---
        df_fin  = pd.DataFrame(fin_rows,  columns=_COLS_FINANCIAL_AGREEMENT)
        df_dep  = pd.DataFrame(dep_rows,  columns=_COLS_DEPOSIT_AGREEMENT)
        df_td   = pd.DataFrame(td_rows,   columns=_COLS_DEPOSIT_TERM_AGREEMENT)
        df_cr   = pd.DataFrame(cr_rows,   columns=_COLS_CREDIT_AGREEMENT)
        df_la   = pd.DataFrame(la_rows,   columns=_COLS_LOAN_AGREEMENT)
        df_lta  = pd.DataFrame(lta_rows,  columns=_COLS_LOAN_TERM_AGREEMENT)
        df_lx   = pd.DataFrame(lx_rows,   columns=_COLS_LOAN_TRANSACTION_AGREEMENT)
        df_mg   = pd.DataFrame(mg_rows,   columns=_COLS_MORTGAGE_AGREEMENT)
        df_cc   = pd.DataFrame(cc_rows,   columns=_COLS_CREDIT_CARD_AGREEMENT)
        df_card = pd.DataFrame(card_rows, columns=_COLS_CARD)

        # --- F. Int64 casts (PRD §7.1 — BIGINT for all IDs) ---
        for df in (df_fin, df_dep, df_td, df_cr, df_la, df_lta, df_lx, df_mg, df_cc):
            df['Agreement_Id'] = df['Agreement_Id'].astype('Int64')
        df_card['Access_Device_Id'] = df_card['Access_Device_Id'].astype('Int64')
        if len(df_cr):
            df_cr['Credit_Agreement_Reaging_Cnt'] = (
                df_cr['Credit_Agreement_Reaging_Cnt'].astype('Int64')
            )

        # --- G. DI stamping — all 10 DataFrames; no stamp_valid() (all Core_DB) ---
        df_fin  = self.stamp_di(df_fin,  start_ts=_TIER7B_DI_START_TS)
        df_dep  = self.stamp_di(df_dep,  start_ts=_TIER7B_DI_START_TS)
        df_td   = self.stamp_di(df_td,   start_ts=_TIER7B_DI_START_TS)
        df_cr   = self.stamp_di(df_cr,   start_ts=_TIER7B_DI_START_TS)
        df_la   = self.stamp_di(df_la,   start_ts=_TIER7B_DI_START_TS)
        df_lta  = self.stamp_di(df_lta,  start_ts=_TIER7B_DI_START_TS)
        df_lx   = self.stamp_di(df_lx,   start_ts=_TIER7B_DI_START_TS)
        df_mg   = self.stamp_di(df_mg,   start_ts=_TIER7B_DI_START_TS)
        df_cc   = self.stamp_di(df_cc,   start_ts=_TIER7B_DI_START_TS)
        df_card = self.stamp_di(df_card, start_ts=_TIER7B_DI_START_TS)

        return {
            'Core_DB.FINANCIAL_AGREEMENT':        df_fin,
            'Core_DB.DEPOSIT_AGREEMENT':          df_dep,
            'Core_DB.DEPOSIT_TERM_AGREEMENT':     df_td,
            'Core_DB.CREDIT_AGREEMENT':           df_cr,
            'Core_DB.LOAN_AGREEMENT':             df_la,
            'Core_DB.LOAN_TERM_AGREEMENT':        df_lta,
            'Core_DB.LOAN_TRANSACTION_AGREEMENT': df_lx,
            'Core_DB.MORTGAGE_AGREEMENT':         df_mg,
            'Core_DB.CREDIT_CARD_AGREEMENT':      df_cc,
            'Core_DB.CARD':                       df_card,
        }

    @staticmethod
    def _build_card_row(ctx: 'GenerationContext', ag, subtype: str) -> dict:
        access_device_id = ctx.ids.next('card')
        association = _CARD_ASSOCIATION_TYPES[access_device_id % 4]
        bin_prefix = _CARD_BIN_BY_ASSOCIATION[association]
        card_num = generate_card_number(ctx.rng, bin_prefix=bin_prefix)
        cvv = generate_cvv(ctx.rng)
        open_dt: date = ag.open_dttm.date()
        return {
            'Access_Device_Id':          access_device_id,
            'Card_Subtype_Cd':           subtype,
            'Card_Association_Type_Cd':  association,
            'Technology_Type_Cd':        'CHIP_AND_PIN',
            'Card_Num':                  card_num,
            'Card_Sequence_Num':         '1',
            'Card_Expiration_Dt':        open_dt + timedelta(days=365 * 4),
            'Card_Issue_Dt':             open_dt,
            'Card_Activation_Dt':        open_dt,
            'Card_Deactivation_Dt':      None,
            'Card_Name':                 _CARD_NAME_BY_ASSOCIATION[association],
            'Card_Encrypted_Num':        card_num,
            'Card_Manufacture_Dt':       open_dt - timedelta(days=7),
            'Card_Replacement_Order_Dt': None,
            'Language_Type_Cd':          'EN',
            'Bank_Identification_Num':   card_num[:6],
            'Card_Security_Code_Num':    cvv,
        }

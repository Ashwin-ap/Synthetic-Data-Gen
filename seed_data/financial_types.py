from typing import Dict

import pandas as pd

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}


def get_financial_type_tables() -> Dict[str, pd.DataFrame]:
    financial_agreement_types = [
        {'Financial_Agreement_Type_Cd': 'DEPOSIT',    'Financial_Agreement_Type_Desc': 'Deposit',    **_DI},
        {'Financial_Agreement_Type_Cd': 'LOAN',       'Financial_Agreement_Type_Desc': 'Loan',       **_DI},
        {'Financial_Agreement_Type_Cd': 'CREDIT',     'Financial_Agreement_Type_Desc': 'Credit',     **_DI},
        {'Financial_Agreement_Type_Cd': 'INVESTMENT', 'Financial_Agreement_Type_Desc': 'Investment', **_DI},
        {'Financial_Agreement_Type_Cd': 'INSURANCE',  'Financial_Agreement_Type_Desc': 'Insurance',  **_DI},
    ]

    amortization_methods = [
        {'Amortization_Method_Cd': 'STRAIGHT_LINE',      'Amortization_Method_Desc': 'Straight Line',      **_DI},
        {'Amortization_Method_Cd': 'EFFECTIVE_INTEREST', 'Amortization_Method_Desc': 'Effective Interest', **_DI},
        {'Amortization_Method_Cd': 'LEVEL_PAYMENT',      'Amortization_Method_Desc': 'Level Payment',      **_DI},
        {'Amortization_Method_Cd': 'INTEREST_ONLY',      'Amortization_Method_Desc': 'Interest Only',      **_DI},
        {'Amortization_Method_Cd': 'BULLET',             'Amortization_Method_Desc': 'Bullet',             **_DI},
        {'Amortization_Method_Cd': 'CUSTOM',             'Amortization_Method_Desc': 'Custom',             **_DI},
    ]

    loan_maturity_subtypes = [
        {'Loan_Maturity_Subtype_Cd': 'SHORT_TERM',  'Loan_Maturity_Subtype_Desc': 'Short Term',  **_DI},
        {'Loan_Maturity_Subtype_Cd': 'MEDIUM_TERM', 'Loan_Maturity_Subtype_Desc': 'Medium Term', **_DI},
        {'Loan_Maturity_Subtype_Cd': 'LONG_TERM',   'Loan_Maturity_Subtype_Desc': 'Long Term',   **_DI},
        {'Loan_Maturity_Subtype_Cd': 'PERPETUAL',   'Loan_Maturity_Subtype_Desc': 'Perpetual',   **_DI},
    ]

    loan_transaction_subtypes = [
        {'Loan_Transaction_Subtype_Cd': 'PAYDAY',       'Loan_Transaction_Subtype_Desc': 'Payday Loan',  **_DI},
        {'Loan_Transaction_Subtype_Cd': 'CASH_ADVANCE', 'Loan_Transaction_Subtype_Desc': 'Cash Advance', **_DI},
        {'Loan_Transaction_Subtype_Cd': 'OVERDRAFT',    'Loan_Transaction_Subtype_Desc': 'Overdraft',    **_DI},
    ]

    loan_term_subtypes = [
        {'Loan_Term_Subtype_Cd': 'INSTALLMENT', 'Loan_Term_Subtype_Desc': 'Installment', **_DI},
        {'Loan_Term_Subtype_Cd': 'BALLOON',     'Loan_Term_Subtype_Desc': 'Balloon',     **_DI},
        {'Loan_Term_Subtype_Cd': 'AMORTIZING',  'Loan_Term_Subtype_Desc': 'Amortizing',  **_DI},
    ]

    credit_card_subtypes = [
        {'Credit_Card_Agreement_Subtype_Cd': 'STANDARD',  'Credit_Card_Agreement_Subtype_Desc': 'Standard',  **_DI},
        {'Credit_Card_Agreement_Subtype_Cd': 'REWARDS',   'Credit_Card_Agreement_Subtype_Desc': 'Rewards',   **_DI},
        {'Credit_Card_Agreement_Subtype_Cd': 'SECURED',   'Credit_Card_Agreement_Subtype_Desc': 'Secured',   **_DI},
        {'Credit_Card_Agreement_Subtype_Cd': 'BUSINESS',  'Credit_Card_Agreement_Subtype_Desc': 'Business',  **_DI},
        {'Credit_Card_Agreement_Subtype_Cd': 'STUDENT',   'Credit_Card_Agreement_Subtype_Desc': 'Student',   **_DI},
    ]

    mortgage_types = [
        {'Mortgage_Type_Cd': 'FIXED_RATE', 'Mortgage_Type_Desc': 'Fixed Rate',        **_DI},
        {'Mortgage_Type_Cd': 'ARM',        'Mortgage_Type_Desc': 'Adjustable Rate',   **_DI},
        {'Mortgage_Type_Cd': 'FHA',        'Mortgage_Type_Desc': 'FHA Loan',          **_DI},
        {'Mortgage_Type_Cd': 'VA',         'Mortgage_Type_Desc': 'VA Loan',           **_DI},
        {'Mortgage_Type_Cd': 'JUMBO',      'Mortgage_Type_Desc': 'Jumbo',             **_DI},
        {'Mortgage_Type_Cd': 'HELOC',      'Mortgage_Type_Desc': 'Home Equity Line',  **_DI},
    ]

    deposit_maturity_subtypes = [
        {'Deposit_Maturity_Subtype_Cd': '3M',  'Deposit_Maturity_Subtype_Desc': '3 Month',  **_DI},
        {'Deposit_Maturity_Subtype_Cd': '6M',  'Deposit_Maturity_Subtype_Desc': '6 Month',  **_DI},
        {'Deposit_Maturity_Subtype_Cd': '12M', 'Deposit_Maturity_Subtype_Desc': '12 Month', **_DI},
        {'Deposit_Maturity_Subtype_Cd': '24M', 'Deposit_Maturity_Subtype_Desc': '24 Month', **_DI},
        {'Deposit_Maturity_Subtype_Cd': '36M', 'Deposit_Maturity_Subtype_Desc': '36 Month', **_DI},
        {'Deposit_Maturity_Subtype_Cd': '60M', 'Deposit_Maturity_Subtype_Desc': '60 Month', **_DI},
    ]

    interest_disbursement_types = [
        {'Interest_Disbursement_Type_Cd': 'COMPOUNDED', 'Interest_Disbursement_Type_Desc': 'Compounded', **_DI},
        {'Interest_Disbursement_Type_Cd': 'SIMPLE',     'Interest_Disbursement_Type_Desc': 'Simple',     **_DI},
        {'Interest_Disbursement_Type_Cd': 'ACCRUED',    'Interest_Disbursement_Type_Desc': 'Accrued',    **_DI},
        {'Interest_Disbursement_Type_Cd': 'CAPITALIZED','Interest_Disbursement_Type_Desc': 'Capitalized', **_DI},
    ]

    payment_timing_types = [
        {'Payment_Timing_Type_Cd': 'MONTHLY',   'Payment_Timing_Type_Desc': 'Monthly',    **_DI},
        {'Payment_Timing_Type_Cd': 'BIWEEKLY',  'Payment_Timing_Type_Desc': 'Biweekly',   **_DI},
        {'Payment_Timing_Type_Cd': 'WEEKLY',    'Payment_Timing_Type_Desc': 'Weekly',     **_DI},
        {'Payment_Timing_Type_Cd': 'QUARTERLY', 'Payment_Timing_Type_Desc': 'Quarterly',  **_DI},
        {'Payment_Timing_Type_Cd': 'ANNUAL',    'Payment_Timing_Type_Desc': 'Annual',     **_DI},
    ]

    purchase_intent_types = [
        {'Purchase_Intent_Cd': 'PURCHASE',    'Purchase_Intent_Desc': 'Purchase',        **_DI},
        {'Purchase_Intent_Cd': 'REFINANCE',   'Purchase_Intent_Desc': 'Refinance',       **_DI},
        {'Purchase_Intent_Cd': 'CASH_OUT',    'Purchase_Intent_Desc': 'Cash Out',        **_DI},
        {'Purchase_Intent_Cd': 'HOME_EQUITY', 'Purchase_Intent_Desc': 'Home Equity',     **_DI},
    ]

    security_types = [
        {'Security_Type_Cd': 'REAL_ESTATE', 'Security_Type_Desc': 'Real Estate', **_DI},
        {'Security_Type_Cd': 'VEHICLE',     'Security_Type_Desc': 'Vehicle',     **_DI},
        {'Security_Type_Cd': 'DEPOSIT',     'Security_Type_Desc': 'Deposit',     **_DI},
        {'Security_Type_Cd': 'SECURITIES',  'Security_Type_Desc': 'Securities',  **_DI},
        {'Security_Type_Cd': 'UNSECURED',   'Security_Type_Desc': 'Unsecured',   **_DI},
    ]

    market_risk_types = [
        {'Market_Risk_Type_Cd': 'TRADING_BOOK',       'Market_Risk_Type_Desc': 'Trading Book',       **_DI},
        {'Market_Risk_Type_Cd': 'BANKING_BOOK',       'Market_Risk_Type_Desc': 'Banking Book',       **_DI},
        {'Market_Risk_Type_Cd': 'HELD_FOR_SALE',      'Market_Risk_Type_Desc': 'Held For Sale',      **_DI},
        {'Market_Risk_Type_Cd': 'AVAILABLE_FOR_SALE', 'Market_Risk_Type_Desc': 'Available For Sale', **_DI},
    ]

    trading_book_types = [
        {'Trading_Book_Cd': 'TRADING', 'Trading_Book_Desc': 'Trading', **_DI},
        {'Trading_Book_Cd': 'BANKING', 'Trading_Book_Desc': 'Banking', **_DI},
        {'Trading_Book_Cd': 'HEDGING', 'Trading_Book_Desc': 'Hedging', **_DI},
    ]

    day_count_basis_types = [
        {'Day_Count_Basis_Cd': '30_360',       'Day_Count_Basis_Desc': '30/360',        **_DI},
        {'Day_Count_Basis_Cd': 'ACTUAL_360',   'Day_Count_Basis_Desc': 'Actual/360',    **_DI},
        {'Day_Count_Basis_Cd': 'ACTUAL_365',   'Day_Count_Basis_Desc': 'Actual/365',    **_DI},
        {'Day_Count_Basis_Cd': 'ACTUAL_ACTUAL','Day_Count_Basis_Desc': 'Actual/Actual', **_DI},
    ]

    risk_mitigant_subtypes = [
        {'Risk_Exposure_Mitigant_Subtype_Cd': 'COLLATERAL',       'Risk_Exposure_Mitigant_Subtype_Desc': 'Collateral',       **_DI},
        {'Risk_Exposure_Mitigant_Subtype_Cd': 'GUARANTEE',        'Risk_Exposure_Mitigant_Subtype_Desc': 'Guarantee',        **_DI},
        {'Risk_Exposure_Mitigant_Subtype_Cd': 'NETTING',          'Risk_Exposure_Mitigant_Subtype_Desc': 'Netting',          **_DI},
        {'Risk_Exposure_Mitigant_Subtype_Cd': 'CREDIT_INSURANCE', 'Risk_Exposure_Mitigant_Subtype_Desc': 'Credit Insurance', **_DI},
    ]

    pricing_method_subtypes = [
        {'Pricing_Method_Subtype_Cd': 'FIXED',    'Pricing_Method_Subtype_Desc': 'Fixed',    **_DI},
        {'Pricing_Method_Subtype_Cd': 'FLOATING', 'Pricing_Method_Subtype_Desc': 'Floating', **_DI},
        {'Pricing_Method_Subtype_Cd': 'INDEXED',  'Pricing_Method_Subtype_Desc': 'Indexed',  **_DI},
        {'Pricing_Method_Subtype_Cd': 'TIERED',   'Pricing_Method_Subtype_Desc': 'Tiered',   **_DI},
    ]

    _c2 = lambda a, b: [a, b, 'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']

    return {
        'Core_DB.FINANCIAL_AGREEMENT_TYPE':      pd.DataFrame(financial_agreement_types, columns=_c2('Financial_Agreement_Type_Cd',         'Financial_Agreement_Type_Desc')),
        'Core_DB.AMORTIZATION_METHOD_TYPE':      pd.DataFrame(amortization_methods,      columns=_c2('Amortization_Method_Cd',              'Amortization_Method_Desc')),
        'Core_DB.LOAN_MATURITY_SUBTYPE':         pd.DataFrame(loan_maturity_subtypes,     columns=_c2('Loan_Maturity_Subtype_Cd',            'Loan_Maturity_Subtype_Desc')),
        'Core_DB.LOAN_TRANSACTION_SUBTYPE':      pd.DataFrame(loan_transaction_subtypes,  columns=_c2('Loan_Transaction_Subtype_Cd',         'Loan_Transaction_Subtype_Desc')),
        'Core_DB.LOAN_TERM_SUBTYPE':             pd.DataFrame(loan_term_subtypes,         columns=_c2('Loan_Term_Subtype_Cd',                'Loan_Term_Subtype_Desc')),
        'Core_DB.CREDIT_CARD_AGREEMENT_SUBTYPE': pd.DataFrame(credit_card_subtypes,       columns=_c2('Credit_Card_Agreement_Subtype_Cd',   'Credit_Card_Agreement_Subtype_Desc')),
        'Core_DB.MORTGAGE_TYPE':                 pd.DataFrame(mortgage_types,             columns=_c2('Mortgage_Type_Cd',                    'Mortgage_Type_Desc')),
        'Core_DB.DEPOSIT_MATURITY_SUBTYPE':      pd.DataFrame(deposit_maturity_subtypes,  columns=_c2('Deposit_Maturity_Subtype_Cd',         'Deposit_Maturity_Subtype_Desc')),
        'Core_DB.INTEREST_DISBURSEMENT_TYPE':    pd.DataFrame(interest_disbursement_types,columns=_c2('Interest_Disbursement_Type_Cd',       'Interest_Disbursement_Type_Desc')),
        'Core_DB.PAYMENT_TIMING_TYPE':           pd.DataFrame(payment_timing_types,       columns=_c2('Payment_Timing_Type_Cd',              'Payment_Timing_Type_Desc')),
        'Core_DB.PURCHASE_INTENT_TYPE':          pd.DataFrame(purchase_intent_types,      columns=_c2('Purchase_Intent_Cd',                  'Purchase_Intent_Desc')),
        'Core_DB.SECURITY_TYPE':                 pd.DataFrame(security_types,             columns=_c2('Security_Type_Cd',                    'Security_Type_Desc')),
        'Core_DB.MARKET_RISK_TYPE':              pd.DataFrame(market_risk_types,           columns=_c2('Market_Risk_Type_Cd',                 'Market_Risk_Type_Desc')),
        'Core_DB.TRADING_BOOK_TYPE':             pd.DataFrame(trading_book_types,          columns=_c2('Trading_Book_Cd',                     'Trading_Book_Desc')),
        'Core_DB.DAY_COUNT_BASIS_TYPE':          pd.DataFrame(day_count_basis_types,       columns=_c2('Day_Count_Basis_Cd',                  'Day_Count_Basis_Desc')),
        'Core_DB.RISK_EXPOSURE_MITIGANT_SUBTYPE':pd.DataFrame(risk_mitigant_subtypes,     columns=_c2('Risk_Exposure_Mitigant_Subtype_Cd',   'Risk_Exposure_Mitigant_Subtype_Desc')),
        'Core_DB.PRICING_METHOD_SUBTYPE':        pd.DataFrame(pricing_method_subtypes,    columns=_c2('Pricing_Method_Subtype_Cd',            'Pricing_Method_Subtype_Desc')),
    }

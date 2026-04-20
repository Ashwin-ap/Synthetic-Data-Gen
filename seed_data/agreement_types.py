from typing import Dict

import pandas as pd

from config.code_values import AGREEMENT_FEATURE_ROLE_CODES, AGREEMENT_STATUS_SCHEMES

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}


def get_agreement_type_tables() -> Dict[str, pd.DataFrame]:
    subtypes = [
        {'Agreement_Subtype_Cd': 'CHECKING',            'Agreement_Subtype_Desc': 'Checking',                **_DI},
        {'Agreement_Subtype_Cd': 'SAVINGS',             'Agreement_Subtype_Desc': 'Savings',                 **_DI},
        {'Agreement_Subtype_Cd': 'MMA',                 'Agreement_Subtype_Desc': 'Money Market Account',    **_DI},
        {'Agreement_Subtype_Cd': 'CERTIFICATE_OF_DEPOSIT', 'Agreement_Subtype_Desc': 'Certificate of Deposit', **_DI},
        {'Agreement_Subtype_Cd': 'RETIREMENT',          'Agreement_Subtype_Desc': 'Retirement',              **_DI},
        {'Agreement_Subtype_Cd': 'MORTGAGE',            'Agreement_Subtype_Desc': 'Mortgage',                **_DI},
        {'Agreement_Subtype_Cd': 'CREDIT_CARD',         'Agreement_Subtype_Desc': 'Credit Card',             **_DI},
        {'Agreement_Subtype_Cd': 'VEHICLE_LOAN',        'Agreement_Subtype_Desc': 'Vehicle Loan',            **_DI},
        {'Agreement_Subtype_Cd': 'STUDENT_LOAN',        'Agreement_Subtype_Desc': 'Student Loan',            **_DI},
        {'Agreement_Subtype_Cd': 'HELOC',               'Agreement_Subtype_Desc': 'Home Equity Line of Credit', **_DI},
        {'Agreement_Subtype_Cd': 'PAYDAY',              'Agreement_Subtype_Desc': 'Payday Loan',             **_DI},
        {'Agreement_Subtype_Cd': 'COMMERCIAL_CHECKING', 'Agreement_Subtype_Desc': 'Commercial Checking',     **_DI},
    ]

    types = [
        {'Agreement_Type_Cd': 'DEPOSIT',    'Agreement_Type_Desc': 'Deposit',    **_DI},
        {'Agreement_Type_Cd': 'LOAN',       'Agreement_Type_Desc': 'Loan',       **_DI},
        {'Agreement_Type_Cd': 'CREDIT',     'Agreement_Type_Desc': 'Credit',     **_DI},
        {'Agreement_Type_Cd': 'COMMERCIAL', 'Agreement_Type_Desc': 'Commercial', **_DI},
    ]

    format_types = [
        {'Agreement_Format_Type_Cd': 'PAPER',      'Agreement_Format_Type_Desc': 'Paper',      **_DI},
        {'Agreement_Format_Type_Cd': 'ELECTRONIC', 'Agreement_Format_Type_Desc': 'Electronic', **_DI},
        {'Agreement_Format_Type_Cd': 'HYBRID',     'Agreement_Format_Type_Desc': 'Hybrid',     **_DI},
    ]

    objective_types = [
        {'Agreement_Objective_Type_Cd': 'SAVINGS_GOAL',  'Agreement_Objective_Type_Desc': 'Savings Goal',  **_DI},
        {'Agreement_Objective_Type_Cd': 'HOME_PURCHASE', 'Agreement_Objective_Type_Desc': 'Home Purchase', **_DI},
        {'Agreement_Objective_Type_Cd': 'EDUCATION',     'Agreement_Objective_Type_Desc': 'Education',     **_DI},
        {'Agreement_Objective_Type_Cd': 'VEHICLE',       'Agreement_Objective_Type_Desc': 'Vehicle',       **_DI},
    ]

    obtained_types = [
        {'Agreement_Obtained_Cd': 'BRANCH',   'Agreement_Obtained_Desc': 'Branch',   **_DI},
        {'Agreement_Obtained_Cd': 'ONLINE',   'Agreement_Obtained_Desc': 'Online',   **_DI},
        {'Agreement_Obtained_Cd': 'PHONE',    'Agreement_Obtained_Desc': 'Phone',    **_DI},
        {'Agreement_Obtained_Cd': 'REFERRAL', 'Agreement_Obtained_Desc': 'Referral', **_DI},
    ]

    _scheme_descs = {
        'Account Status':       'Account Status',
        'Accrual Status':       'Accrual Status',
        'Default Status':       'Default Status',
        'Drawn Undrawn Status': 'Drawn Undrawn Status',
        'Frozen Status':        'Frozen Status',
        'Past Due Status':      'Past Due Status',
    }
    scheme_types = [
        {'Agreement_Status_Scheme_Cd': s, 'Agreement_Status_Scheme_Desc': _scheme_descs[s], **_DI}
        for s in AGREEMENT_STATUS_SCHEMES
    ]

    reason_types = [
        {'Agreement_Status_Reason_Cd': 'DELINQUENCY',       'Agreement_Status_Reason_Desc': 'Delinquency',       **_DI},
        {'Agreement_Status_Reason_Cd': 'CUSTOMER_REQUEST',  'Agreement_Status_Reason_Desc': 'Customer Request',  **_DI},
        {'Agreement_Status_Reason_Cd': 'FRAUD',             'Agreement_Status_Reason_Desc': 'Fraud',             **_DI},
        {'Agreement_Status_Reason_Cd': 'DECEASED',          'Agreement_Status_Reason_Desc': 'Deceased',          **_DI},
        {'Agreement_Status_Reason_Cd': 'WRITE_OFF',         'Agreement_Status_Reason_Desc': 'Write Off',         **_DI},
    ]

    feature_role_types = [
        {'Agreement_Feature_Role_Cd': code, 'Agreement_Feature_Role_Desc': code.title(), **_DI}
        for code in AGREEMENT_FEATURE_ROLE_CODES
    ]

    asset_liability_types = [
        {'Asset_Liability_Cd': 'ASSET',             'Asset_Liability_Desc': 'Asset',             **_DI},
        {'Asset_Liability_Cd': 'LIABILITY',         'Asset_Liability_Desc': 'Liability',         **_DI},
        {'Asset_Liability_Cd': 'OFF_BALANCE_SHEET', 'Asset_Liability_Desc': 'Off Balance Sheet', **_DI},
    ]

    balance_sheet_types = [
        {'Balance_Sheet_Cd': 'ON_BALANCE_SHEET',  'Balance_Sheet_Desc': 'On Balance Sheet',  **_DI},
        {'Balance_Sheet_Cd': 'OFF_BALANCE_SHEET', 'Balance_Sheet_Desc': 'Off Balance Sheet', **_DI},
        {'Balance_Sheet_Cd': 'CONTINGENT',        'Balance_Sheet_Desc': 'Contingent',        **_DI},
    ]

    # DDL columns: Document_Production_Cycle_Cd, Time_Period_Cd, Document_Cycle_Desc,
    #              Document_Cycle_Frequency_Num, Document_Cycle_Frequency_Day_Num, di_*
    doc_cycle_types = [
        {'Document_Production_Cycle_Cd': 'MONTHLY',   'Time_Period_Cd': None, 'Document_Cycle_Desc': 'Monthly',    'Document_Cycle_Frequency_Num': None, 'Document_Cycle_Frequency_Day_Num': None, **_DI},
        {'Document_Production_Cycle_Cd': 'QUARTERLY', 'Time_Period_Cd': None, 'Document_Cycle_Desc': 'Quarterly',  'Document_Cycle_Frequency_Num': None, 'Document_Cycle_Frequency_Day_Num': None, **_DI},
        {'Document_Production_Cycle_Cd': 'ANNUAL',    'Time_Period_Cd': None, 'Document_Cycle_Desc': 'Annual',     'Document_Cycle_Frequency_Num': None, 'Document_Cycle_Frequency_Day_Num': None, **_DI},
        {'Document_Production_Cycle_Cd': 'ON_DEMAND', 'Time_Period_Cd': None, 'Document_Cycle_Desc': 'On Demand',  'Document_Cycle_Frequency_Num': None, 'Document_Cycle_Frequency_Day_Num': None, **_DI},
    ]

    statement_mail_types = [
        {'Statement_Mail_Type_Cd': 'PAPER',  'Statement_Mail_Type_Desc': 'Paper',  **_DI},
        {'Statement_Mail_Type_Cd': 'EMAIL',  'Statement_Mail_Type_Desc': 'Email',  **_DI},
        {'Statement_Mail_Type_Cd': 'PORTAL', 'Statement_Mail_Type_Desc': 'Portal', **_DI},
        {'Statement_Mail_Type_Cd': 'NONE',   'Statement_Mail_Type_Desc': 'None',   **_DI},
    ]

    data_source_types = [
        {'Data_Source_Type_Cd': 'CORE_BANKING',      'Data_Source_Type_Desc': 'Core Banking',      **_DI},
        {'Data_Source_Type_Cd': 'CARD_SYSTEM',       'Data_Source_Type_Desc': 'Card System',       **_DI},
        {'Data_Source_Type_Cd': 'LOAN_ORIGINATION',  'Data_Source_Type_Desc': 'Loan Origination',  **_DI},
        {'Data_Source_Type_Cd': 'MDM',               'Data_Source_Type_Desc': 'MDM',               **_DI},
    ]

    _cols_subtype     = ['Agreement_Subtype_Cd',          'Agreement_Subtype_Desc',          'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_type        = ['Agreement_Type_Cd',             'Agreement_Type_Desc',             'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_format      = ['Agreement_Format_Type_Cd',      'Agreement_Format_Type_Desc',      'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_objective   = ['Agreement_Objective_Type_Cd',   'Agreement_Objective_Type_Desc',   'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_obtained    = ['Agreement_Obtained_Cd',         'Agreement_Obtained_Desc',         'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_scheme      = ['Agreement_Status_Scheme_Cd',    'Agreement_Status_Scheme_Desc',    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_reason      = ['Agreement_Status_Reason_Cd',    'Agreement_Status_Reason_Desc',    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_feature_role = ['Agreement_Feature_Role_Cd',   'Agreement_Feature_Role_Desc',     'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_asset_liab  = ['Asset_Liability_Cd',            'Asset_Liability_Desc',            'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_balance     = ['Balance_Sheet_Cd',              'Balance_Sheet_Desc',              'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_doc_cycle   = ['Document_Production_Cycle_Cd', 'Time_Period_Cd', 'Document_Cycle_Desc', 'Document_Cycle_Frequency_Num', 'Document_Cycle_Frequency_Day_Num', 'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_stmt_mail   = ['Statement_Mail_Type_Cd',        'Statement_Mail_Type_Desc',        'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_data_src    = ['Data_Source_Type_Cd',           'Data_Source_Type_Desc',           'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']

    return {
        'Core_DB.AGREEMENT_SUBTYPE':              pd.DataFrame(subtypes,          columns=_cols_subtype),
        'Core_DB.AGREEMENT_TYPE':                 pd.DataFrame(types,             columns=_cols_type),
        'Core_DB.AGREEMENT_FORMAT_TYPE':          pd.DataFrame(format_types,      columns=_cols_format),
        'Core_DB.AGREEMENT_OBJECTIVE_TYPE':       pd.DataFrame(objective_types,   columns=_cols_objective),
        'Core_DB.AGREEMENT_OBTAINED_TYPE':        pd.DataFrame(obtained_types,    columns=_cols_obtained),
        'Core_DB.AGREEMENT_STATUS_SCHEME_TYPE':   pd.DataFrame(scheme_types,      columns=_cols_scheme),
        'Core_DB.AGREEMENT_STATUS_REASON_TYPE':   pd.DataFrame(reason_types,      columns=_cols_reason),
        'Core_DB.AGREEMENT_FEATURE_ROLE_TYPE':    pd.DataFrame(feature_role_types, columns=_cols_feature_role),
        'Core_DB.ASSET_LIABILITY_TYPE':           pd.DataFrame(asset_liability_types, columns=_cols_asset_liab),
        'Core_DB.BALANCE_SHEET_TYPE':             pd.DataFrame(balance_sheet_types, columns=_cols_balance),
        'Core_DB.DOCUMENT_PRODUCTION_CYCLE_TYPE': pd.DataFrame(doc_cycle_types,   columns=_cols_doc_cycle),
        'Core_DB.STATEMENT_MAIL_TYPE':            pd.DataFrame(statement_mail_types, columns=_cols_stmt_mail),
        'Core_DB.DATA_SOURCE_TYPE':               pd.DataFrame(data_source_types, columns=_cols_data_src),
    }

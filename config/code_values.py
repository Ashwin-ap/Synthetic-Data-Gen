PARTY_AGREEMENT_ROLE_CODES = {'customer', 'borrower', 'guarantor', 'co-borrower', 'owner'}

PARTY_RELATED_ROLE_CODES = {
    'customer of enterprise',
    'prospect of enterprise',
    'employee of enterprise',
}

AGREEMENT_STATUS_SCHEMES = (
    'Account Status',
    'Accrual Status',
    'Default Status',
    'Drawn Undrawn Status',
    'Frozen Status',
    'Past Due Status',
)

AGREEMENT_FEATURE_ROLE_CODES = ('primary', 'fee', 'rate', 'term')

CURRENCY_USE_CODES = ('preferred', 'secondary', 'home')

# Layer 2 ACCOUNT_STATUS_DIMENSION matches this row exactly to set Frozen_Ind='1'
FROZEN_STATUS_ROW = {
    'Agreement_Status_Scheme_Cd': 'Frozen Status',
    'Agreement_Status_Cd': 'FROZEN',
    'Agreement_Status_Desc': 'Frozen',
}

LANGUAGE_USAGE_TYPES = ('primary spoken language', 'primary written language')

ORG_NAME_TYPES = ('brand name', 'business name', 'legal name', 'registered name')

PROFITABILITY_MODEL_TYPE_CD             = 'profitability'
CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD = 'customer profitability'
RATE_FEATURE_SUBTYPE_CD                 = 'Rate Feature'
ORIGINAL_LOAN_TERM_CLASSIFICATION_CD    = 'Original Loan Term'
TERRITORY_ISO_STANDARD_CD               = 'ISO 3166-2 Country Subdivision Standard'

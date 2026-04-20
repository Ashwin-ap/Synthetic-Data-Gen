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

# ---------------------------------------------------------------------------
# Tier 13 — SMALLINT code dictionaries for task and activity tables
# ---------------------------------------------------------------------------

TASK_ACTIVITY_TYPE_CD = {
    1: 'COMPLAINT_RESOLUTION',
    2: 'SERVICE_REQUEST',
    3: 'ACCOUNT_UPDATE',
}

TASK_SUBTYPE_CD = {
    1: 'INVESTIGATION',
    2: 'ESCALATION',
    3: 'COMPENSATION',
}

TASK_REASON_CD = {
    1: 'FEE_DISPUTE',
    2: 'SERVICE_QUALITY',
    3: 'PRODUCT_ISSUE',
}

TASK_STATUS_TYPE_CD = {
    1: 'OPEN',
    2: 'IN_PROGRESS',
    3: 'RESOLVED',
    4: 'CLOSED',
}

TASK_STATUS_REASON_CD = {
    1: 'INITIAL_INTAKE',
    2: 'AWAITING_CUSTOMER',
    3: 'RESOLVED_SUCCESS',
    4: 'RESOLVED_FAILURE',
}

ACTIVITY_TYPE_CD = {
    1: 'OUTBOUND_CALL',
    2: 'INBOUND_CALL',
    3: 'EMAIL',
    4: 'INTERNAL_NOTE',
    5: 'FOLLOW_UP',
}

ACTIVITY_STATUS_TYPE_CD = {
    1: 'PENDING',
    2: 'COMPLETED',
    3: 'FAILED',
}

ACTIVITY_STATUS_REASON_CD = {
    1: 'EXECUTED',
    2: 'NO_RESPONSE',
    3: 'CUSTOMER_SATISFIED',
}

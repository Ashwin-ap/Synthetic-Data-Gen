from decimal import Decimal
import pandas as pd
from typing import Dict

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}

# ── GENDER_TYPE ──────────────────────────────────────────────────────────────
_cols_gender_type = [
    'Gender_Type_Cd', 'Gender_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_gender_type_rows = [
    {'Gender_Type_Cd': 'MALE',        'Gender_Type_Desc': 'Male',        **_DI},
    {'Gender_Type_Cd': 'FEMALE',      'Gender_Type_Desc': 'Female',      **_DI},
    {'Gender_Type_Cd': 'NON_BINARY',  'Gender_Type_Desc': 'Non Binary',  **_DI},
    {'Gender_Type_Cd': 'UNSPECIFIED', 'Gender_Type_Desc': 'Unspecified', **_DI},
]

# ── GENDER_PRONOUN ────────────────────────────────────────────────────────────
# Composite PK: (Gender_Pronoun_Cd, Gender_Pronoun_Type_Cd)
_cols_gender_pronoun = [
    'Gender_Pronoun_Cd', 'Gender_Pronoun_Name', 'Gender_Pronoun_Type_Cd',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_gender_pronoun_rows = [
    {'Gender_Pronoun_Cd': 'HE',     'Gender_Pronoun_Name': 'He',     'Gender_Pronoun_Type_Cd': 'subjective', **_DI},
    {'Gender_Pronoun_Cd': 'HIM',    'Gender_Pronoun_Name': 'Him',    'Gender_Pronoun_Type_Cd': 'objective',  **_DI},
    {'Gender_Pronoun_Cd': 'HIS',    'Gender_Pronoun_Name': 'His',    'Gender_Pronoun_Type_Cd': 'possessive', **_DI},
    {'Gender_Pronoun_Cd': 'SHE',    'Gender_Pronoun_Name': 'She',    'Gender_Pronoun_Type_Cd': 'subjective', **_DI},
    {'Gender_Pronoun_Cd': 'HER',    'Gender_Pronoun_Name': 'Her',    'Gender_Pronoun_Type_Cd': 'objective',  **_DI},
    {'Gender_Pronoun_Cd': 'HERS',   'Gender_Pronoun_Name': 'Hers',   'Gender_Pronoun_Type_Cd': 'possessive', **_DI},
    {'Gender_Pronoun_Cd': 'THEY',   'Gender_Pronoun_Name': 'They',   'Gender_Pronoun_Type_Cd': 'subjective', **_DI},
    {'Gender_Pronoun_Cd': 'THEM',   'Gender_Pronoun_Name': 'Them',   'Gender_Pronoun_Type_Cd': 'objective',  **_DI},
    {'Gender_Pronoun_Cd': 'THEIRS', 'Gender_Pronoun_Name': 'Theirs', 'Gender_Pronoun_Type_Cd': 'possessive', **_DI},
]

# ── ETHNICITY_TYPE ────────────────────────────────────────────────────────────
# Must equal exactly {WHITE, BLACK, HISPANIC, ASIAN, OTHER} — UniverseBuilder literal match
_cols_ethnicity_type = [
    'Ethnicity_Type_Cd', 'Ethnicity_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_ethnicity_type_rows = [
    {'Ethnicity_Type_Cd': 'WHITE',    'Ethnicity_Type_Desc': 'White',    **_DI},
    {'Ethnicity_Type_Cd': 'BLACK',    'Ethnicity_Type_Desc': 'Black',    **_DI},
    {'Ethnicity_Type_Cd': 'HISPANIC', 'Ethnicity_Type_Desc': 'Hispanic', **_DI},
    {'Ethnicity_Type_Cd': 'ASIAN',    'Ethnicity_Type_Desc': 'Asian',    **_DI},
    {'Ethnicity_Type_Cd': 'OTHER',    'Ethnicity_Type_Desc': 'Other',    **_DI},
]

# ── MARITAL_STATUS_TYPE ───────────────────────────────────────────────────────
_cols_marital_status_type = [
    'Marital_Status_Cd', 'Marital_Status_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_marital_status_type_rows = [
    {'Marital_Status_Cd': 'MARRIED',   'Marital_Status_Desc': 'Married',   **_DI},
    {'Marital_Status_Cd': 'SINGLE',    'Marital_Status_Desc': 'Single',    **_DI},
    {'Marital_Status_Cd': 'DIVORCED',  'Marital_Status_Desc': 'Divorced',  **_DI},
    {'Marital_Status_Cd': 'WIDOWED',   'Marital_Status_Desc': 'Widowed',   **_DI},
    {'Marital_Status_Cd': 'SEPARATED', 'Marital_Status_Desc': 'Separated', **_DI},
]

# ── NATIONALITY_TYPE ──────────────────────────────────────────────────────────
_cols_nationality_type = [
    'Nationality_Cd', 'Nationality_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_nationality_type_rows = [
    {'Nationality_Cd': 'USA', 'Nationality_Desc': 'United States', **_DI},
    {'Nationality_Cd': 'CAN', 'Nationality_Desc': 'Canadian',      **_DI},
    {'Nationality_Cd': 'GBR', 'Nationality_Desc': 'British',       **_DI},
    {'Nationality_Cd': 'IND', 'Nationality_Desc': 'Indian',        **_DI},
    {'Nationality_Cd': 'CHN', 'Nationality_Desc': 'Chinese',       **_DI},
    {'Nationality_Cd': 'MEX', 'Nationality_Desc': 'Mexican',       **_DI},
    {'Nationality_Cd': 'PHL', 'Nationality_Desc': 'Filipino',      **_DI},
    {'Nationality_Cd': 'VNM', 'Nationality_Desc': 'Vietnamese',    **_DI},
    {'Nationality_Cd': 'KOR', 'Nationality_Desc': 'Korean',        **_DI},
    {'Nationality_Cd': 'ESP', 'Nationality_Desc': 'Spanish',       **_DI},
]

# ── TAX_BRACKET_TYPE ──────────────────────────────────────────────────────────
# US Federal 2024 marginal brackets; Tax_Bracket_Rate is DECIMAL(15,12)
# Step 11 maps income_quartile → Q1=BRACKET_12, Q2=BRACKET_22, Q3=BRACKET_24, Q4=BRACKET_32
_cols_tax_bracket_type = [
    'Tax_Bracket_Cd', 'Tax_Bracket_Desc', 'Tax_Bracket_Rate',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_tax_bracket_type_rows = [
    {'Tax_Bracket_Cd': 'BRACKET_10', 'Tax_Bracket_Desc': '10% Federal Bracket', 'Tax_Bracket_Rate': Decimal('0.100000000000'), **_DI},
    {'Tax_Bracket_Cd': 'BRACKET_12', 'Tax_Bracket_Desc': '12% Federal Bracket', 'Tax_Bracket_Rate': Decimal('0.120000000000'), **_DI},
    {'Tax_Bracket_Cd': 'BRACKET_22', 'Tax_Bracket_Desc': '22% Federal Bracket', 'Tax_Bracket_Rate': Decimal('0.220000000000'), **_DI},
    {'Tax_Bracket_Cd': 'BRACKET_24', 'Tax_Bracket_Desc': '24% Federal Bracket', 'Tax_Bracket_Rate': Decimal('0.240000000000'), **_DI},
    {'Tax_Bracket_Cd': 'BRACKET_32', 'Tax_Bracket_Desc': '32% Federal Bracket', 'Tax_Bracket_Rate': Decimal('0.320000000000'), **_DI},
    {'Tax_Bracket_Cd': 'BRACKET_35', 'Tax_Bracket_Desc': '35% Federal Bracket', 'Tax_Bracket_Rate': Decimal('0.350000000000'), **_DI},
    {'Tax_Bracket_Cd': 'BRACKET_37', 'Tax_Bracket_Desc': '37% Federal Bracket', 'Tax_Bracket_Rate': Decimal('0.370000000000'), **_DI},
]

# ── VERY_IMPORTANT_PERSON_TYPE ────────────────────────────────────────────────
_cols_vip_type = [
    'VIP_Type_Cd', 'VIP_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_vip_type_rows = [
    {'VIP_Type_Cd': 'NONE',     'VIP_Type_Desc': 'None',     **_DI},
    {'VIP_Type_Cd': 'PLATINUM', 'VIP_Type_Desc': 'Platinum', **_DI},
    {'VIP_Type_Cd': 'GOLD',     'VIP_Type_Desc': 'Gold',     **_DI},
    {'VIP_Type_Cd': 'SILVER',   'VIP_Type_Desc': 'Silver',   **_DI},
    {'VIP_Type_Cd': 'BRONZE',   'VIP_Type_Desc': 'Bronze',   **_DI},
]

# ── MILITARY_STATUS_TYPE ──────────────────────────────────────────────────────
_cols_military_status_type = [
    'Military_Status_Type_Cd', 'Military_Status_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_military_status_type_rows = [
    {'Military_Status_Type_Cd': 'ACTIVE_DUTY',      'Military_Status_Desc': 'Active Duty',      **_DI},
    {'Military_Status_Type_Cd': 'VETERAN',          'Military_Status_Desc': 'Veteran',          **_DI},
    {'Military_Status_Type_Cd': 'RESERVE',          'Military_Status_Desc': 'Reserve',          **_DI},
    {'Military_Status_Type_Cd': 'NATIONAL_GUARD',   'Military_Status_Desc': 'National Guard',   **_DI},
    {'Military_Status_Type_Cd': 'CIVILIAN',         'Military_Status_Desc': 'Civilian',         **_DI},
    {'Military_Status_Type_Cd': 'RETIRED_MILITARY', 'Military_Status_Desc': 'Retired Military', **_DI},
]

# ── OCCUPATION_TYPE ───────────────────────────────────────────────────────────
# Must equal exactly {EMP, SELF_EMP, RETIRED, NOT_WORKING} — UniverseBuilder literal match
_cols_occupation_type = [
    'Occupation_Type_Cd', 'Occupation_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_occupation_type_rows = [
    {'Occupation_Type_Cd': 'EMP',         'Occupation_Type_Desc': 'Employed',    **_DI},
    {'Occupation_Type_Cd': 'SELF_EMP',    'Occupation_Type_Desc': 'Self Employed', **_DI},
    {'Occupation_Type_Cd': 'RETIRED',     'Occupation_Type_Desc': 'Retired',     **_DI},
    {'Occupation_Type_Cd': 'NOT_WORKING', 'Occupation_Type_Desc': 'Not Working', **_DI},
]

# ── PARTY_RELATED_STATUS_TYPE ─────────────────────────────────────────────────
_cols_party_related_status_type = [
    'Party_Related_Status_Type_Cd', 'Party_Related_Status_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_party_related_status_type_rows = [
    {'Party_Related_Status_Type_Cd': 'ACTIVE',    'Party_Related_Status_Type_Desc': 'Active',    **_DI},
    {'Party_Related_Status_Type_Cd': 'INACTIVE',  'Party_Related_Status_Type_Desc': 'Inactive',  **_DI},
    {'Party_Related_Status_Type_Cd': 'PENDING',   'Party_Related_Status_Type_Desc': 'Pending',   **_DI},
    {'Party_Related_Status_Type_Cd': 'CANCELLED', 'Party_Related_Status_Type_Desc': 'Cancelled', **_DI},
]

# ── GENERAL_MEDICAL_STATUS_TYPE ───────────────────────────────────────────────
_cols_general_medical_status_type = [
    'General_Medical_Status_Cd', 'General_Medical_Status_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_general_medical_status_type_rows = [
    {'General_Medical_Status_Cd': 'HEALTHY',           'General_Medical_Status_Desc': 'Healthy',           **_DI},
    {'General_Medical_Status_Cd': 'CHRONIC_CONDITION', 'General_Medical_Status_Desc': 'Chronic Condition', **_DI},
    {'General_Medical_Status_Cd': 'ACUTE_CONDITION',   'General_Medical_Status_Desc': 'Acute Condition',   **_DI},
    {'General_Medical_Status_Cd': 'UNKNOWN',           'General_Medical_Status_Desc': 'Unknown',           **_DI},
    {'General_Medical_Status_Cd': 'DISABLED',          'General_Medical_Status_Desc': 'Disabled',          **_DI},
    {'General_Medical_Status_Cd': 'DECEASED',          'General_Medical_Status_Desc': 'Deceased',          **_DI},
]

# ── SKILL_TYPE ────────────────────────────────────────────────────────────────
_cols_skill_type = [
    'Skill_Cd', 'Skill_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_skill_type_rows = [
    {'Skill_Cd': 'ACCOUNTING',   'Skill_Desc': 'Accounting',    **_DI},
    {'Skill_Cd': 'ENGINEERING',  'Skill_Desc': 'Engineering',   **_DI},
    {'Skill_Cd': 'SALES',        'Skill_Desc': 'Sales',         **_DI},
    {'Skill_Cd': 'NURSING',      'Skill_Desc': 'Nursing',       **_DI},
    {'Skill_Cd': 'CARPENTRY',    'Skill_Desc': 'Carpentry',     **_DI},
    {'Skill_Cd': 'TEACHING',     'Skill_Desc': 'Teaching',      **_DI},
    {'Skill_Cd': 'PROGRAMMING',  'Skill_Desc': 'Programming',   **_DI},
    {'Skill_Cd': 'MANAGEMENT',   'Skill_Desc': 'Management',    **_DI},
    {'Skill_Cd': 'DRIVING',      'Skill_Desc': 'Driving',       **_DI},
    {'Skill_Cd': 'COOKING',      'Skill_Desc': 'Cooking',       **_DI},
    {'Skill_Cd': 'LEGAL',        'Skill_Desc': 'Legal',         **_DI},
    {'Skill_Cd': 'MEDICINE',     'Skill_Desc': 'Medicine',      **_DI},
    {'Skill_Cd': 'ADMIN',        'Skill_Desc': 'Administration', **_DI},
    {'Skill_Cd': 'FINANCE',      'Skill_Desc': 'Finance',       **_DI},
    {'Skill_Cd': 'MARKETING',    'Skill_Desc': 'Marketing',     **_DI},
]

# ── SPECIAL_NEED_TYPE ─────────────────────────────────────────────────────────
_cols_special_need_type = [
    'Special_Need_Cd', 'Special_Need_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_special_need_type_rows = [
    {'Special_Need_Cd': 'NONE',                'Special_Need_Desc': 'None',                **_DI},
    {'Special_Need_Cd': 'VISUAL_IMPAIRMENT',   'Special_Need_Desc': 'Visual Impairment',   **_DI},
    {'Special_Need_Cd': 'HEARING_IMPAIRMENT',  'Special_Need_Desc': 'Hearing Impairment',  **_DI},
    {'Special_Need_Cd': 'MOBILITY_IMPAIRMENT', 'Special_Need_Desc': 'Mobility Impairment', **_DI},
    {'Special_Need_Cd': 'COGNITIVE',           'Special_Need_Desc': 'Cognitive Impairment', **_DI},
    {'Special_Need_Cd': 'SPEECH',              'Special_Need_Desc': 'Speech Impairment',   **_DI},
    {'Special_Need_Cd': 'OTHER',               'Special_Need_Desc': 'Other',               **_DI},
]

# ── LANGUAGE_TYPE ─────────────────────────────────────────────────────────────
# ISO_Language_Type_Cd is NOT NULL (ISO-639-1 two-letter lowercase code)
_cols_language_type = [
    'Language_Type_Cd', 'Language_Type_Desc', 'Language_Native_Name', 'ISO_Language_Type_Cd',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_language_type_rows = [
    {'Language_Type_Cd': 'EN', 'Language_Type_Desc': 'English',    'Language_Native_Name': 'English',      'ISO_Language_Type_Cd': 'en', **_DI},
    {'Language_Type_Cd': 'ES', 'Language_Type_Desc': 'Spanish',    'Language_Native_Name': 'Español',      'ISO_Language_Type_Cd': 'es', **_DI},
    {'Language_Type_Cd': 'ZH', 'Language_Type_Desc': 'Chinese',    'Language_Native_Name': '中文',          'ISO_Language_Type_Cd': 'zh', **_DI},
    {'Language_Type_Cd': 'HI', 'Language_Type_Desc': 'Hindi',      'Language_Native_Name': 'हिन्दी',        'ISO_Language_Type_Cd': 'hi', **_DI},
    {'Language_Type_Cd': 'AR', 'Language_Type_Desc': 'Arabic',     'Language_Native_Name': 'العربية',       'ISO_Language_Type_Cd': 'ar', **_DI},
    {'Language_Type_Cd': 'FR', 'Language_Type_Desc': 'French',     'Language_Native_Name': 'Français',     'ISO_Language_Type_Cd': 'fr', **_DI},
    {'Language_Type_Cd': 'DE', 'Language_Type_Desc': 'German',     'Language_Native_Name': 'Deutsch',      'ISO_Language_Type_Cd': 'de', **_DI},
    {'Language_Type_Cd': 'JA', 'Language_Type_Desc': 'Japanese',   'Language_Native_Name': '日本語',        'ISO_Language_Type_Cd': 'ja', **_DI},
    {'Language_Type_Cd': 'KO', 'Language_Type_Desc': 'Korean',     'Language_Native_Name': '한국어',        'ISO_Language_Type_Cd': 'ko', **_DI},
    {'Language_Type_Cd': 'VI', 'Language_Type_Desc': 'Vietnamese', 'Language_Native_Name': 'Tiếng Việt',  'ISO_Language_Type_Cd': 'vi', **_DI},
    {'Language_Type_Cd': 'TL', 'Language_Type_Desc': 'Tagalog',    'Language_Native_Name': 'Tagalog',      'ISO_Language_Type_Cd': 'tl', **_DI},
    {'Language_Type_Cd': 'PT', 'Language_Type_Desc': 'Portuguese', 'Language_Native_Name': 'Português',   'ISO_Language_Type_Cd': 'pt', **_DI},
    {'Language_Type_Cd': 'RU', 'Language_Type_Desc': 'Russian',    'Language_Native_Name': 'Русский',      'ISO_Language_Type_Cd': 'ru', **_DI},
    {'Language_Type_Cd': 'IT', 'Language_Type_Desc': 'Italian',    'Language_Native_Name': 'Italiano',    'ISO_Language_Type_Cd': 'it', **_DI},
    {'Language_Type_Cd': 'PL', 'Language_Type_Desc': 'Polish',     'Language_Native_Name': 'Polski',      'ISO_Language_Type_Cd': 'pl', **_DI},
]

# ── SPECIALTY_TYPE ────────────────────────────────────────────────────────────
_cols_specialty_type = [
    'Specialty_Type_Cd', 'Specialty_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_specialty_type_rows = [
    {'Specialty_Type_Cd': 'GENERAL',             'Specialty_Type_Desc': 'General',             **_DI},
    {'Specialty_Type_Cd': 'MEDICAL',             'Specialty_Type_Desc': 'Medical',             **_DI},
    {'Specialty_Type_Cd': 'LEGAL',               'Specialty_Type_Desc': 'Legal',               **_DI},
    {'Specialty_Type_Cd': 'FINANCIAL_ADVISORY',  'Specialty_Type_Desc': 'Financial Advisory',  **_DI},
    {'Specialty_Type_Cd': 'TECHNICAL',           'Specialty_Type_Desc': 'Technical',           **_DI},
    {'Specialty_Type_Cd': 'REAL_ESTATE',         'Specialty_Type_Desc': 'Real Estate',         **_DI},
    {'Specialty_Type_Cd': 'EDUCATION',           'Specialty_Type_Desc': 'Education',           **_DI},
]

# ── LEGAL_CLASSIFICATION ──────────────────────────────────────────────────────
_cols_legal_classification = [
    'Legal_Classification_Cd', 'Legal_Classification_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_legal_classification_rows = [
    {'Legal_Classification_Cd': 'CORPORATION',          'Legal_Classification_Desc': 'Corporation',           **_DI},
    {'Legal_Classification_Cd': 'LLC',                  'Legal_Classification_Desc': 'Limited Liability Company', **_DI},
    {'Legal_Classification_Cd': 'PARTNERSHIP',          'Legal_Classification_Desc': 'Partnership',           **_DI},
    {'Legal_Classification_Cd': 'SOLE_PROPRIETORSHIP',  'Legal_Classification_Desc': 'Sole Proprietorship',   **_DI},
    {'Legal_Classification_Cd': 'NONPROFIT',            'Legal_Classification_Desc': 'Nonprofit Organization', **_DI},
    {'Legal_Classification_Cd': 'GOVERNMENT',           'Legal_Classification_Desc': 'Government Entity',     **_DI},
    {'Legal_Classification_Cd': 'TRUST',                'Legal_Classification_Desc': 'Trust',                 **_DI},
    {'Legal_Classification_Cd': 'COOPERATIVE',          'Legal_Classification_Desc': 'Cooperative',           **_DI},
]

# ── BUSINESS_CATEGORY ─────────────────────────────────────────────────────────
# Must include SELF_EMPLOYED — reserved org (party ID 9999999) FKs to this code
_cols_business_category = [
    'Business_Category_Cd', 'Business_Category_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_business_category_rows = [
    {'Business_Category_Cd': 'SMALL_BUSINESS', 'Business_Category_Desc': 'Small Business', **_DI},
    {'Business_Category_Cd': 'MID_MARKET',     'Business_Category_Desc': 'Mid Market',     **_DI},
    {'Business_Category_Cd': 'ENTERPRISE',     'Business_Category_Desc': 'Enterprise',     **_DI},
    {'Business_Category_Cd': 'MICRO_BUSINESS', 'Business_Category_Desc': 'Micro Business', **_DI},
    {'Business_Category_Cd': 'STARTUP',        'Business_Category_Desc': 'Startup',        **_DI},
    {'Business_Category_Cd': 'SELF_EMPLOYED',  'Business_Category_Desc': 'Self Employed',  **_DI},
]


def get_party_type_tables() -> Dict[str, pd.DataFrame]:
    return {
        'Core_DB.GENDER_TYPE':               pd.DataFrame(_gender_type_rows,               columns=_cols_gender_type),
        'Core_DB.GENDER_PRONOUN':            pd.DataFrame(_gender_pronoun_rows,            columns=_cols_gender_pronoun),
        'Core_DB.ETHNICITY_TYPE':            pd.DataFrame(_ethnicity_type_rows,            columns=_cols_ethnicity_type),
        'Core_DB.MARITAL_STATUS_TYPE':       pd.DataFrame(_marital_status_type_rows,       columns=_cols_marital_status_type),
        'Core_DB.NATIONALITY_TYPE':          pd.DataFrame(_nationality_type_rows,          columns=_cols_nationality_type),
        'Core_DB.TAX_BRACKET_TYPE':          pd.DataFrame(_tax_bracket_type_rows,          columns=_cols_tax_bracket_type),
        'Core_DB.VERY_IMPORTANT_PERSON_TYPE': pd.DataFrame(_vip_type_rows,                 columns=_cols_vip_type),
        'Core_DB.MILITARY_STATUS_TYPE':      pd.DataFrame(_military_status_type_rows,      columns=_cols_military_status_type),
        'Core_DB.OCCUPATION_TYPE':           pd.DataFrame(_occupation_type_rows,           columns=_cols_occupation_type),
        'Core_DB.PARTY_RELATED_STATUS_TYPE': pd.DataFrame(_party_related_status_type_rows, columns=_cols_party_related_status_type),
        'Core_DB.GENERAL_MEDICAL_STATUS_TYPE': pd.DataFrame(_general_medical_status_type_rows, columns=_cols_general_medical_status_type),
        'Core_DB.SKILL_TYPE':                pd.DataFrame(_skill_type_rows,                columns=_cols_skill_type),
        'Core_DB.SPECIAL_NEED_TYPE':         pd.DataFrame(_special_need_type_rows,         columns=_cols_special_need_type),
        'Core_DB.LANGUAGE_TYPE':             pd.DataFrame(_language_type_rows,             columns=_cols_language_type),
        'Core_DB.SPECIALTY_TYPE':            pd.DataFrame(_specialty_type_rows,            columns=_cols_specialty_type),
        'Core_DB.LEGAL_CLASSIFICATION':      pd.DataFrame(_legal_classification_rows,      columns=_cols_legal_classification),
        'Core_DB.BUSINESS_CATEGORY':         pd.DataFrame(_business_category_rows,         columns=_cols_business_category),
    }

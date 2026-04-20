from datetime import date
from pathlib import Path

SEED = 42
TARGET_CUSTOMERS = 3_000
TARGET_AGREEMENTS = 5_000

INDIVIDUAL_PCT = 0.80
ORGANIZATION_PCT = 0.20

COHORT_ACTIVE_PCT    = 0.55
COHORT_DECLINING_PCT = 0.30
COHORT_CHURNED_PCT   = 0.05
COHORT_NEW_PCT       = 0.10

CHECKING_PENETRATION_PCT = 0.90

HISTORY_START = date(2025, 10, 1)
SIM_DATE      = date(2026, 3, 31)

HIGH_DATE = '9999-12-31'
HIGH_TS   = '9999-12-31 00:00:00.000000'

# Both reserved IDs are 9_999_999 — shared party-ID space (PRD §7.2/§7.12).
# BANK_PARTY_ID  → PARTY_RELATED 'customer of enterprise' rows (Tier 9)
# SELF_EMP_ORG_ID → ORGANIZATION placeholder for self-employed individuals (Tier 3/4)
# Both are above every ID_RANGES start, so no generated party ID ever collides.
BANK_PARTY_ID   = 9_999_999
SELF_EMP_ORG_ID = 9_999_999

# Single source of truth for the double-R typo — Step 22 reads this (PRD §7.10)
PARTY_INTERRACTION_EVENT_TABLE_NAME = 'PARTY_INTERRACTION_EVENT'

# Authoritative skip list — consulted by Step 5 (writer) and Step 15 (location)
SKIPPED_TABLES = {'Core_DB.GEOSPATIAL'}

OUTPUT_DIR  = Path('output')
CORE_DB_DIR = OUTPUT_DIR / 'Core_DB'
CDM_DB_DIR  = OUTPUT_DIR / 'CDM_DB'
PIM_DB_DIR  = OUTPUT_DIR / 'PIM_DB'

# BIGINT starting offsets per entity type (mvp-tool-design.md §8).
# Combined with sequential counters in IdFactory these produce BIGINT values.
ID_RANGES = {
    'party':      10_000_000,
    'agreement':  100_000,
    'event':      50_000_000,
    'address':    1_000_000,
    'locator':    2_000_000,
    'feature':    5_000,
    'product':    1_000,
    'campaign':   100,
    'promotion':  200,
    'model':      1,
    'claim':      9_000_000,
    'household':  8_000_000,
    'task':        3_000_000,
    'task_status': 3_500_000,
    'activity':    4_000_000,
    'contact':    6_000_000,
    'card':       7_000_000,
    'market_seg': 500,
    'channel':    50,
    'pim_id':          90_000_000,
    'group_id':        91_000_000,
    'pim_parameter':   92_000_000,   # Tier 15 — PIM_Parameter_Id sequence (Step 23)
    # Tier 1 — Geography (Step 9)
    'country':             700,
    'region':              800,
    'territory':           900,
    'county':            1_100,
    'city':              1_400,
    'postal_code':       1_600,
    'geographical_area': 1_900,
    # Tier 5 — Location (Step 15)
    'street_address':  2_100_000,   # reserved; STREET_ADDRESS reuses Address_Id (1_000_000-range)
    'parcel_address':  2_200_000,   # actively used — PARCEL_ADDRESS PKs
    'post_office_box': 2_300_000,   # actively used — POST_OFFICE_BOX_ADDRESS PKs
    # Tier 14 — CDM_DB (Step 22)
    'cdm_address':    20_000_000,   # CDM_Address_Id surrogate — unused band below event (50M)
}

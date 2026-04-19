# CIF Synthetic Data Generator — MVP Design Document

**Version:** 1.0  
**Date:** 2026-04-17  
**Scope:** Layer 1 only — `Core_DB` (iDM/FSDM), `CDM_DB` (MDM), `PIM_DB` (MDM PIM)  
**Output:** CSV files per table, one subdirectory per schema  
**Primary references:**  `references/07_mvp-schema-reference.md`, `references/01_schema-reference.md`, `references/02_data-mapping-reference.md`, `references/05_architect-qa.md`, `references/06_supporting-enrichments.md`

---

## 1. Simulation Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| Target customers | ~3,000 unique party IDs | `06_supporting-enrichments.md` Part J |
| Target agreements | ~5,000 | `06_supporting-enrichments.md` Part J |
| Individual / Organization split | 80% / 20% | `06_supporting-enrichments.md` Part J |
| History window start | `2025-10-01` | 6-month window |
| Simulation end date (SIM_DATE) | `2026-03-31` | 6-month window |
| Random seed | `42` (configurable) | Reproducibility |
| High date (DATE fields) | `9999-12-31` | `05_architect-qa.md` |
| High date (TIMESTAMP fields) | `9999-12-31 00:00:00.000000` | `05_architect-qa.md` |
| Attrition cohort split | 55% Active / 30% Declining / 5% Churned / 10% New | `06_supporting-enrichments.md` Part G |
| Checking account penetration | 90% | `06_supporting-enrichments.md` Part B |

---

## 2. Architecture Overview

The generator uses an **Entity-First Registry + Tiered Writers** pattern. The fundamental problem it solves: cross-table correlation consistency. A customer's age, income quartile, and lifecycle cohort must coherently drive their product mix, balances, credit score, agreement status history, and event frequency across **206 tables** (per `references/07_mvp-schema-reference.md`). Generating tables independently breaks this.

### Two-phase execution

**Phase 1 — Universe Build** (in-memory, no I/O):  
`UniverseBuilder` makes all correlated decisions for every customer and agreement upfront, producing `CustomerProfile` and `AgreementProfile` registries.

**Phase 2 — Tiered Writing** (pure transformation):  
15 tier generators each read from the registries + upstream table DataFrames and produce new DataFrames. No statistical decisions in this phase — only data formatting and FK wiring.

```
UniverseBuilder
    │
    ├── CustomerProfile registry  (list of ~3,000)
    └── AgreementProfile registry (list of ~5,000)
              │
              ▼
    Tier 0  → lookup/reference CSVs  (seeded, not generated)
    Tier 1  → geography CSVs
    Tier 2  → core entity CSVs       (PARTY, AGREEMENT, PRODUCT, ...)
    Tier 3  → party subtype CSVs     (INDIVIDUAL, ORGANIZATION)
    Tier 4  → party attribute CSVs   (INDIVIDUAL_NAME, OCCUPATION, ...)
    Tier 5  → location CSVs          (STREET_ADDRESS, POSTAL_CODE, ...)
    Tier 6  → link CSVs              (PARTY_LOCATOR)
    Tier 7  → agreement detail CSVs  (AGREEMENT_STATUS ×6, AGREEMENT_CURRENCY, ...)
    Tier 8  → product hierarchy CSVs (PRODUCT_FEATURE, AGREEMENT_PRODUCT, ...)
    Tier 9  → party-agreement CSVs   (PARTY_AGREEMENT, PARTY_RELATED)
    Tier 10 → event CSVs             (EVENT, FINANCIAL_EVENT, FUNDS_TRANSFER_EVENT, ...)
    Tier 11 → CRM CSVs               (CAMPAIGN_STATUS, PROMOTION, PROMOTION_OFFER)
    Tier 13 → task CSVs              (PARTY_TASK, TASK_ACTIVITY, ...)
    Tier 14 → CDM_DB CSVs
    Tier 15 → PIM_DB CSVs
```

---

## 3. Folder Structure

```
synthetic_data_gen/
│
├── config/
│   ├── settings.py           # Scale params, date window, random seed, paths
│   ├── distributions.py      # All SCF/WP5 statistical samplers
│   └── code_values.py        # All constrained code value sets (exact strings)
│
├── seed_data/                # Tier 0 — static reference data (NOT randomly generated)
│   ├── agreement_types.py    # AGREEMENT_SUBTYPE, AGREEMENT_TYPE, etc.
│   ├── status_types.py       # AGREEMENT_STATUS_TYPE (incl. FROZEN seed row)
│   ├── feature_types.py      # FEATURE_SUBTYPE, FEATURE_CLASSIFICATION_TYPE
│   ├── party_types.py        # GENDER_TYPE, MARITAL_STATUS_TYPE, NATIONALITY_TYPE, etc.
│   ├── channel_types.py      # CHANNEL_TYPE, CHANNEL_INSTANCE_SUBTYPE
│   ├── campaign_types.py     # CAMPAIGN_TYPE, CAMPAIGN_STRATEGY_TYPE
│   ├── financial_types.py    # FINANCIAL_AGREEMENT_TYPE, AMORTIZATION_METHOD_TYPE, etc.
│   ├── geography_ref.py      # ~20 countries, ~50 US states/territories, ~100 cities
│   ├── industry_codes.py     # Real NAICS / SIC / GICS / NACE seed rows
│   ├── interest_rate_indices.py  # SOFR, PRIME, FEDFUNDS, LIBOR, EURIBOR
│   └── currency.py           # ISO 4217 codes: USD, EUR, GBP, CAD, AUD, JPY
│
├── registry/
│   ├── profiles.py           # CustomerProfile, AgreementProfile dataclasses
│   └── universe.py           # UniverseBuilder
│
├── generators/
│   ├── base.py               # BaseGenerator: DI column stamping, shared helpers
│   ├── tier0_lookups.py
│   ├── tier1_geography.py
│   ├── tier2_core.py
│   ├── tier3_party_subtypes.py
│   ├── tier4_party_attributes.py
│   ├── tier5_location.py
│   ├── tier6_links.py
│   ├── tier7_agreement_details.py
│   ├── tier8_product_hierarchy.py
│   ├── tier9_party_agreement.py
│   ├── tier10_events.py
│   ├── tier11_crm.py
│   ├── tier13_tasks.py
│   ├── tier14_cdm.py
│   └── tier15_pim.py
│
├── utils/
│   ├── id_factory.py         # Centralised BIGINT ID sequences per entity type
│   ├── date_utils.py         # SCD2 helpers, simulation window, date arithmetic
│   ├── luhn.py               # Luhn-valid 16-digit card number generation
│   └── di_columns.py         # Stamps DI metadata columns on any DataFrame
│
├── output/
│   ├── writer.py             # DataFrame → CSV with DDL column ordering
│   └── validator.py          # Post-generation FK + Layer 2 constraint checks
│
├── main.py                   # Orchestrator: runs all tiers in order
├── requirements.txt
│
└── output/                   # Generated CSVs (git-ignored)
    ├── Core_DB/
    │   ├── AGREEMENT.csv
    │   ├── AGREEMENT_STATUS.csv
    │   └── ... (all Core_DB tables)
    ├── CDM_DB/
    │   ├── PARTY.csv
    │   └── ...
    └── PIM_DB/
        ├── PRODUCT.csv
        └── ...
```

---

## 4. Registry Design (`registry/profiles.py`)

### CustomerProfile

Every field is decided atomically in `UniverseBuilder` before any CSV is written. Downstream generators read these fields — they never make statistical decisions.

```python
@dataclass
class CustomerProfile:
    # Identity
    party_id: int                        # BIGINT — shared with CDM_Party_Id (Q1 resolution)
    party_type: str                      # 'INDIVIDUAL' | 'ORGANIZATION'
    
    # Demographics (drives all product/amount decisions)
    age: int                             # SCF AGECL distribution
    income_quartile: int                 # 1–4 (SCF INCQRTCAT)
    lifecycle_cohort: str                # 'ACTIVE' | 'DECLINING' | 'CHURNED' | 'NEW'
    clv_segment: int                     # 1–10 decile (top 10% = high-value)
    
    # Individual attributes (None for ORGANIZATION)
    gender_type_cd: Optional[str]        # 'MALE' | 'FEMALE'
    marital_status_cd: Optional[str]     # 'MARRIED' | 'SINGLE'
    ethnicity_type_cd: Optional[str]     # WHITE | BLACK | HISPANIC | ASIAN | OTHER
    occupation_cd: Optional[str]         # EMP | SELF_EMP | RETIRED | NOT_WORKING
    num_dependents: int                  # 0–5 (SCF KIDS distribution)
    fico_score: int                      # 300–850 (SCF-calibrated by ethnicity+income)
    
    # Household
    household_id: Optional[int]          # None for single-member or org
    household_role: str                  # 'HEAD' | 'SPOUSE' | 'DEPENDENT'
    lifecl: int                          # 1–6 (SCF LIFECL household stage)
    
    # Channel / contact
    has_internet: bool                   # 89.7% True → drives PARTY_CONTACT_PREFERENCE
    preferred_channel_cd: int            # SMALLINT: 3=ONLINE | 4=MOBILE | 1=BRANCH
    
    # Products decided (drives all agreement generation)
    product_set: List[str]               # e.g. ['CHECKING', 'SAVINGS', 'MORTGAGE']
    
    # Dates
    party_since: date                    # Customer relationship start
    
    # Address reference
    address_id: int                      # Points to a pre-generated address row
    
    # Org-specific (None for INDIVIDUAL)
    org_name: Optional[str]
    naics_sector_cd: Optional[str]
    sic_cd: Optional[str]
    gics_sector_cd: Optional[str]
```

### AgreementProfile

```python
@dataclass
class AgreementProfile:
    agreement_id: int                    # BIGINT
    owner_party_id: int                  # FK to CustomerProfile.party_id
    product_type: str                    # 'CHECKING' | 'SAVINGS' | 'MORTGAGE' | etc.
    agreement_subtype_cd: str            # Matches AGREEMENT_SUBTYPE seed table
    product_id: int                      # FK to Core_DB.PRODUCT
    
    # Temporal
    open_dttm: datetime
    close_dttm: Optional[datetime]       # None = open; set for CHURNED cohort
    
    # Financial
    balance_amt: Decimal                 # SCF income-quartile stratified
    interest_rate: Decimal               # AGREEMENT_RATE.Agreement_Rate
    original_loan_amt: Optional[Decimal] # Loan/mortgage agreements only
    
    # Status flags (drive AGREEMENT_STATUS scheme rows)
    is_delinquent: bool                  # 11.2% rate (SCF LATE)
    is_severely_delinquent: bool         # 4.6% rate (SCF LATE60)
    is_frozen: bool                      # Small % — drives 'Frozen Status' scheme
    
    # Balance trajectory (for DECLINING cohort — monthly snapshots)
    monthly_balances: List[Decimal]      # 6 values, one per history month
    
    # Agreement sub-type path (exclusive sub-typing)
    is_financial: bool                   # Has FINANCIAL_AGREEMENT row
    is_deposit: bool                     # Has DEPOSIT_AGREEMENT row
    is_term_deposit: bool                # Has DEPOSIT_TERM_AGREEMENT row
    is_credit: bool                      # Has CREDIT_AGREEMENT row
    is_loan_term: bool                   # Has LOAN_TERM_AGREEMENT row
    is_mortgage: bool                    # Has MORTGAGE_AGREEMENT row
    is_credit_card: bool                 # Has CREDIT_CARD_AGREEMENT row
    is_loan_transaction: bool            # Has LOAN_TRANSACTION_AGREEMENT row
```

---

## 5. UniverseBuilder (`registry/universe.py`)

Builds the complete registry in memory. Called once from `main.py` before any tier runs.

### Build sequence

```python
class UniverseBuilder:
    def build(self, config: Config, rng: np.random.Generator) -> GenerationContext:
        customers = self._generate_customer_shells(config, rng)   # party_id, party_type
        self._assign_demographics(customers, rng)                  # age, gender, income_quartile, etc.
        self._assign_households(customers, rng)                    # household_id, lifecl
        self._assign_cohorts(customers, rng)                       # lifecycle_cohort (55/30/5/10)
        self._assign_clv_segments(customers, rng)                  # clv_segment 1–10
        self._assign_products(customers, rng)                      # product_set (Maslow + ownership rates)
        agreements = self._generate_agreements(customers, config, rng)
        self._assign_open_dates(customers, agreements, config, rng)
        self._assign_balances(customers, agreements, rng)          # income_quartile + product_type
        self._assign_balance_trajectories(agreements, rng)         # monthly_balances for DECLINING
        self._assign_status_flags(agreements, rng)                 # delinquent, frozen flags
        addresses = self._generate_address_pool(config, rng)       # shared address pool
        self._assign_addresses(customers, addresses, rng)
        return GenerationContext(customers, agreements, addresses, config, rng)
```

### Product assignment rules (`_assign_products`)

Priority:
1. 10% unbanked customers → empty `product_set`
2. All others get CHECKING (90% penetration)
3. Apply SCF ownership rates independently for each additional product:
   - SAVINGS: 48.4%; MMA: 20.0%; CERTIFICATE_OF_DEPOSIT: 7.8%
   - RETIREMENT: 59.1% (age-conditional: 45.1% under-35, 64.6% peak at 55–64)
   - MORTGAGE: 39.6% (age-conditional: 23.7% under-35, 47–53% at 45–64)
   - CREDIT_CARD: 37.8%
   - VEHICLE_LOAN: 30.3%
   - STUDENT_LOAN: 17.7% (age-conditional: higher under-35)
4. CLV top-decile customers (clv_segment=10): force 4–8 products
5. Organizations: COMMERCIAL_CHECKING only; no mortgage/retirement
6. DECLINING cohort: product set frozen at current state (no new products)
7. NEW cohort: product_set from Maslow hierarchy for their age/lifecl

### Lifecycle cohort rules (`_assign_cohorts` + `_assign_open_dates`)

| Cohort | % | Agreement.open_dttm | Agreement.close_dttm |
|--------|---|---------------------|----------------------|
| ACTIVE | 55% | 2015-01-01 to 2025-09-30 | None |
| DECLINING | 30% | 2015-01-01 to 2025-06-30 | None (still open) |
| CHURNED | 5% | 2015-01-01 to 2025-06-30 | 2025-10-01 to 2026-03-15 |
| NEW | 10% | 2026-01-15 to 2026-03-31 | None |

---

## 6. GenerationContext

Passed through every tier generator. Accumulates output DataFrames.

```python
@dataclass
class GenerationContext:
    customers: List[CustomerProfile]
    agreements: List[AgreementProfile]
    addresses: List[AddressRecord]          # Pre-generated address pool
    config: Config
    rng: np.random.Generator
    ids: IdFactory
    tables: Dict[str, pd.DataFrame]         # key = 'Schema.TABLE_NAME'
```

All tier generators read from `ctx.tables` for upstream data and write back to it. Example: `ctx.tables['Core_DB.AGREEMENT']`, `ctx.tables['CDM_DB.PARTY']`.

---

## 7. BaseGenerator and DI Columns (`generators/base.py`)

```python
HIGH_TS   = '9999-12-31 00:00:00.000000'
HIGH_DATE = '9999-12-31'

class BaseGenerator:
    def stamp_di(self, df: pd.DataFrame,
                 start_ts: str,
                 end_ts: str = HIGH_TS,
                 deleted: str = 'N') -> pd.DataFrame:
        df['di_data_src_cd']      = None
        df['di_start_ts']         = start_ts
        df['di_proc_name']        = None
        df['di_rec_deleted_Ind']  = deleted
        df['di_end_ts']           = end_ts
        return df

    def stamp_valid(self, df: pd.DataFrame,
                    from_dt: str,
                    to_dt: str = HIGH_DATE,
                    del_ind: str = 'N') -> pd.DataFrame:
        df['Valid_From_Dt'] = from_dt
        df['Valid_To_Dt']   = to_dt
        df['Del_Ind']       = del_ind
        return df
```

Rules:
- `stamp_di()` is called on **all** tables (Core_DB, CDM_DB, PIM_DB, customized)
- `stamp_valid()` is called additionally on **CDM_DB and PIM_DB** tables only
- Active records: `di_end_ts = HIGH_TS`, `Valid_To_Dt = HIGH_DATE`
- Historical records: `di_end_ts` = actual end timestamp, `Valid_To_Dt` = actual end date
- `di_data_src_cd` and `di_proc_name` → NULL (per `05_architect-qa.md` Q5c)

---

## 8. ID Factory (`utils/id_factory.py`)

All BIGINT IDs generated from central sequences. **Never reuse IDs across entity types.**

```python
ID_RANGES = {
    'party':      10_000_000,    # BIGINT start
    'agreement':  100_000,
    'event':      50_000_000,
    'address':    1_000_000,
    'locator':    2_000_000,
    'feature':    5_000,
    'product':    1_000,
    'campaign':   100,
    'promotion':  200,
    'model':      1,
    'claim':      1_000_000,
    'household':  8_000_000,
    'task':       3_000_000,
    'activity':   4_000_000,
    'contact':    6_000_000,
    'card':       7_000_000,
    'market_seg': 500,
    'channel':    50,
    'pim_id':     90_000_000,
    'group_id':   91_000_000,
}
```

---

## 9. Tier-by-Tier Generator Reference

### Tier 0 — Lookup / Reference Tables (`tier0_lookups.py`)

**Not generated — loaded from `seed_data/` and written directly.**

These tables must exist with exact code values before any other tier runs. Tier 0 is the only tier where data is hardcoded rather than randomly generated.

Tables produced (complete list):

**Agreement domain:** `AGREEMENT_SUBTYPE`, `AGREEMENT_TYPE`, `AGREEMENT_FORMAT_TYPE`, `AGREEMENT_OBJECTIVE_TYPE`, `AGREEMENT_OBTAINED_TYPE`, `AGREEMENT_STATUS_TYPE` *, `AGREEMENT_STATUS_REASON_TYPE`, `AGREEMENT_STATUS_SCHEME_TYPE`, `AGREEMENT_FEATURE_ROLE_TYPE`, `ASSET_LIABILITY_TYPE`, `BALANCE_SHEET_TYPE`, `DOCUMENT_PRODUCTION_CYCLE_TYPE`, `STATEMENT_MAIL_TYPE`, `DATA_SOURCE_TYPE`

**Financial:** `FINANCIAL_AGREEMENT_TYPE`, `AMORTIZATION_METHOD_TYPE`, `LOAN_MATURITY_SUBTYPE`, `LOAN_TRANSACTION_SUBTYPE`, `LOAN_TERM_SUBTYPE`, `CREDIT_CARD_AGREEMENT_SUBTYPE`, `MORTGAGE_TYPE`, `DEPOSIT_MATURITY_SUBTYPE`, `INTEREST_DISBURSEMENT_TYPE`, `PAYMENT_TIMING_TYPE`, `PURCHASE_INTENT_TYPE`, `SECURITY_TYPE`, `MARKET_RISK_TYPE`, `TRADING_BOOK_TYPE`, `DAY_COUNT_BASIS_TYPE`, `RISK_EXPOSURE_MITIGANT_SUBTYPE`, `PRICING_METHOD_SUBTYPE`

**Party:** `GENDER_TYPE`, `GENDER_PRONOUN`, `ETHNICITY_TYPE`, `MARITAL_STATUS_TYPE`, `NATIONALITY_TYPE`, `TAX_BRACKET_TYPE`, `VERY_IMPORTANT_PERSON_TYPE`, `MILITARY_STATUS_TYPE`, `OCCUPATION_TYPE`, `SPECIAL_NEED_TYPE`, `GENERAL_MEDICAL_STATUS_TYPE`, `PARTY_RELATED_STATUS_TYPE`, `SKILL_TYPE`, `LANGUAGE_TYPE`

**Product/Feature:** `FEATURE_SUBTYPE`, `FEATURE_INSURANCE_SUBTYPE`, `FEATURE_CLASSIFICATION_TYPE`

**Channel/Promotion:** `CHANNEL_INSTANCE_SUBTYPE`, `CONVENIENCE_FACTOR_TYPE`, `CHANNEL_STATUS_TYPE`, `CAMPAIGN_STRATEGY_TYPE`, `CAMPAIGN_TYPE`, `CAMPAIGN_CLASSIFICATION`, `CAMPAIGN_STATUS_TYPE`, `PROMOTION_OFFER_TYPE`, `PROMOTION_METRIC_TYPE`

**Address/Geo:** `ADDRESS_SUBTYPE`, `DIRECTION_TYPE`, `STREET_SUFFIX_TYPE`, `TERRITORY_TYPE`, `CITY_TYPE`, `CALENDAR_TYPE`

**Other:** `BUSINESS_CATEGORY`, `LEGAL_CLASSIFICATION` (initial rows), `SPECIALTY_TYPE`, `UNIT_OF_MEASURE`, `UNIT_OF_MEASURE_TYPE`, `TIME_PERIOD_TYPE`, `CURRENCY`, `NAICS_INDUSTRY`, `NACE_CLASS`, `SIC`, `GICS_SECTOR_TYPE`, `GICS_INDUSTRY_GROUP_TYPE`, `GICS_INDUSTRY_TYPE`, `GICS_SUBINDUSTRY_TYPE`

\* `AGREEMENT_STATUS_TYPE` has composite PK (`Agreement_Status_Scheme_Cd` + `Agreement_Status_Cd`). Must include this critical row:
```python
{'Agreement_Status_Scheme_Cd': 'Frozen Status',
 'Agreement_Status_Cd': 'FROZEN',
 'Agreement_Status_Desc': 'Frozen'}
```
This is the exact row Layer 2 ACCOUNT_STATUS_DIMENSION matches to set `Frozen_Ind = '1'`.

---

### Tier 1 — Geography (`tier1_geography.py`)

Tables: `COUNTRY`, `REGION`, `TERRITORY`, `COUNTY`, `CITY`, `POSTAL_CODE`, `ISO_3166_COUNTRY_STANDARD`, `ISO_3166_COUNTRY_SUBDIVISION_STANDARD`, `GEOGRAPHICAL_AREA`, `GEOGRAPHICAL_AREA_CURRENCY`

Use ~20 real countries, ~50 US states as territories, ~100 real cities. Real ISO codes required because STREET_ADDRESS_BB territory chain (`TERRITORY BB WHERE Territory_Standard_Type = 'ISO 3166-2 Country Subdivision Standard'`) FK-joins to `ISO_3166_COUNTRY_SUBDIVISION_STANDARD`.

Seed `ISO_3166_COUNTRY_SUBDIVISION_STANDARD` with `Territory_Standard_Type_Cd = 'ISO 3166-2 Country Subdivision Standard'` for each US state.

---

### Tier 2 — Core Entities (`tier2_core.py`)

Tables: `PARTY` (Core_DB conceptual — IDs from CDM_DB), `PRODUCT`, `FEATURE`, `AGREEMENT`, `ANALYTICAL_MODEL`, `MARKET_SEGMENT`, `CHANNEL_INSTANCE`, `CAMPAIGN`

**AGREEMENT:** Generate from `AgreementProfile` list. Column `Agreement_Id` is BIGINT (Q1 resolution). `Agreement_Legally_Binding_Ind` is CHAR(3): `'Yes'` / `'No'`.

**FEATURE:** Seed 20–30 features. Must include at least:
- One row with `Feature_Subtype_Cd = 'Rate Feature'` (needed for LOAN_ACCOUNT_BB)
- One row with `Feature_Classification_Cd = 'Original Loan Term'` (needed for LOAN_ACCOUNT_BB)

**ANALYTICAL_MODEL:** Seed 5–20 models. Must include:
- At least one with `Model_Type_Cd = 'profitability'` (for AGREEMENT_SCORE)
- At least one with `Model_Purpose_Cd = 'customer profitability'` (for PARTY_SCORE)

**CHANNEL_INSTANCE:** Generate ~20 rows covering BRANCH, ATM, ONLINE, MOBILE, CALL_CENTER types.

---

### Tier 3 — Party Subtypes (`tier3_party_subtypes.py`)

Tables: `INDIVIDUAL` (Core_DB), `ORGANIZATION` (Core_DB), `BUSINESS`

**INDIVIDUAL:** `Individual_Party_Id` = `CustomerProfile.party_id` for all INDIVIDUAL-type customers. `Tax_Bracket_Cd` NOT NULL — derive from `income_quartile`. `Nationality_Cd` NOT NULL.

**ORGANIZATION:** `Organization_Party_Id` = `CustomerProfile.party_id` for ORGANIZATION-type customers. Populate Basel fields with defaults ('No' for indicators).

---

### Tier 4 — Party Attributes (`tier4_party_attributes.py`)

Tables: `INDIVIDUAL_NAME`, `INDIVIDUAL_GENDER_PRONOUN`, `INDIVIDUAL_MARITAL_STATUS`, `INDIVIDUAL_VIP_STATUS`, `INDIVIDUAL_OCCUPATION`, `INDIVIDUAL_MILITARY_STATUS`, `INDIVIDUAL_MEDICAL`, `INDIVIDUAL_SKILL`, `INDIVIDUAL_SPECIAL_NEED`, `INDIVIDUAL_BONUS_TIMING`, `INDIVIDUAL_PAY_TIMING`, `ASSOCIATE_EMPLOYMENT`, `ORGANIZATION_NAME`, `ORGANIZATION_NAICS`, `ORGANIZATION_NACE`, `ORGANIZATION_SIC`, `ORGANIZATION_GICS`, `PARTY_LANGUAGE_USAGE`, `PARTY_STATUS`, `PARTY_SCORE`, `PARTY_CREDIT_REPORT_SCORE`, `PARTY_IDENTIFICATION`, `PARTY_DEMOGRAPHIC`, `DEMOGRAPHIC_VALUE`, `PARTY_SEGMENT` (Core_DB), `PARTY_SPECIALTY`, `MARKET_SEGMENT`, `PARTY_CONTACT_PREFERENCE` (customized)

**Critical constraints for Layer 2 readiness:**

`INDIVIDUAL_NAME`:
- `Individual_Name_Start_Dt` must be before SIM_DATE; `Individual_Name_End_Dt` = `9999-12-31`
- `Name_Type_Cd` must be populated (use `'legal'`)
- All three of `Given_Name`, `Middle_Name`, `Family_Name` are NOT NULL — use Faker

`PARTY_LANGUAGE_USAGE`: Every party must have **two** records:
```python
{'Language_Usage_Type_Cd': 'primary spoken language', ...}
{'Language_Usage_Type_Cd': 'primary written language', ...}
```
Without these, Language_Cd and Language_Written_Cd columns in INDIVIDUAL_BB are NULL.

`PARTY_STATUS`: Every party must have at least one record. Layer 2 filter: `WHERE Party_Status_Dt = max(Party_Status_Dt)`. Use `Party_Status_Cd = 'ACTIVE'` for non-churned; `'BANKRUPT'` for 1.1% (SCF).

`PARTY_CREDIT_REPORT_SCORE`: `Credit_Report_Score_Num` stored as VARCHAR(50) string ("300"–"850"). Derive from `CustomerProfile.fico_score`.

`PARTY_SCORE`: `Party_Score_Val` as VARCHAR(100) probability string, e.g., `"0.7823"`. One row per party with `Model_Purpose_Cd = 'customer profitability'`.

`ORGANIZATION_NAME`: Must include name records with `Name_Type_Cd` values: `'brand name'`, `'business name'`, `'legal name'`, `'registered name'` (used in ORGANIZATION_BB pivot).

`ORGANIZATION_NAICS` / `ORGANIZATION_SIC` / `ORGANIZATION_GICS`: Exactly one row per org with `Primary_NAICS_Ind = 'Yes'` / `Primary_SIC_Ind = 'Yes'` / `Primary_GICS_Ind = 'Yes'`. Required for ORGANIZATION_BB industry pivot.

`PARTY_CONTACT_PREFERENCE` (customized): SMALLINT codes.
- `Channel_Type_Cd`: 3=ONLINE for `has_internet=True` customers; 1=BRANCH otherwise
- `Contact_Preference_Type_Cd`: 1=Sales, 2=Service (two rows per party)
- `Protocol_Type_Cd`, `Days_Cd`, `Hours_Cd`: use defaults (1=any_time, 1=any_day, 1=any_hours)

`INDIVIDUAL_MEDICAL`: Populate for all individual customers. Every individual party gets at least one row. All tables listed in `07_mvp-schema-reference.md` are populated — no sparse/optional treatment.

`INDIVIDUAL_SKILL`: Populate for all individual customers. One or more rows per individual with `Skill_Cd` FK to seeded `SKILL_TYPE` table.

`INDIVIDUAL_SPECIAL_NEED`: Populate for all individual customers. One or more rows per individual with `Special_Need_Cd` FK to seeded `SPECIAL_NEED_TYPE` table.

`INDIVIDUAL_PAY_TIMING` / `INDIVIDUAL_BONUS_TIMING`: Both tables populated for all employed and self-employed individuals (per `05_architect-qa.md` Q7). `Business_Party_Id` FK to `ORGANIZATION`: employed individuals point to a real org; self-employed individuals point to reserved placeholder ID `9999999` ('Self-Employment Organization' row in ORGANIZATION CSV — see Section 10 rule).

`DEMOGRAPHIC_VALUE`: Seed lookup rows (e.g., age-band, income-band, ethnicity demographic codes) before generating `PARTY_DEMOGRAPHIC` rows. `PARTY_DEMOGRAPHIC.Demographic_Cd` and `PARTY_DEMOGRAPHIC.Demographic_Value_Cd` must FK to `DEMOGRAPHIC_VALUE` rows. No standalone DEMOGRAPHIC table exists in the DDL — the chain is `PARTY_DEMOGRAPHIC → DEMOGRAPHIC_VALUE` directly.

---

### Tier 5 — Location (`tier5_location.py`)

Tables: `ADDRESS` (Core_DB), `STREET_ADDRESS`, `STREET_ADDRESS_DETAIL`, `PARCEL_ADDRESS`, `POST_OFFICE_BOX_ADDRESS`, `POSTAL_CODE` (additional rows), `GEOSPATIAL_POINT`, `LOCATOR_RELATED`

Generate a pool of ~500 addresses shared across customers (realistic — families/householders share). `Address_Subtype_Cd` = TITLE 'Locator Type Cd'; use `'PHYSICAL'` as primary type.

`STREET_ADDRESS`: `City_Id`, `County_Id`, `Territory_Id`, `Postal_Code_Id`, `Country_Id` must all FK to Tier 1 rows. Use US addresses with real city/territory/postal chains.

`GEOSPATIAL_POINT`: Lat/Lon as DECIMAL(18,4) — realistic US coordinate ranges (lat 25–49, lon -125 to -65).

No `GEOSPATIAL` table — it contains `ST_Geometry` column which cannot be represented in CSV; skip.

---

### Tier 6 — Links (`tier6_links.py`)

Tables: `PARTY_LOCATOR`

`PARTY_LOCATOR`: Links each party to their address. `Locator_Id` FK to ADDRESS.Address_Id. `Locator_Usage_Type_Cd = 'physical_primary'` for primary address.

---

### Tier 7 — Agreement Details (`tier7_agreement_details.py`)

Tables: `AGREEMENT_STATUS`, `AGREEMENT_CURRENCY`, `AGREEMENT_SCORE`, `AGREEMENT_FEATURE`, `AGREEMENT_METRIC`, `AGREEMENT_RATE`, `FINANCIAL_AGREEMENT`, `DEPOSIT_AGREEMENT`, `DEPOSIT_TERM_AGREEMENT`, `CREDIT_AGREEMENT`, `LOAN_AGREEMENT`, `LOAN_TERM_AGREEMENT`, `LOAN_TRANSACTION_AGREEMENT`, `MORTGAGE_AGREEMENT`, `CREDIT_CARD_AGREEMENT`, `TERM_FEATURE`, `INTEREST_RATE_INDEX`, `INTEREST_INDEX_RATE`, `VARIABLE_INTEREST_RATE_FEATURE`, `CARD`

**Most critical tier for Layer 2 readiness.**

`AGREEMENT_STATUS` — **all 6 scheme types per agreement, no exceptions:**
```python
REQUIRED_SCHEMES = [
    'Account Status', 'Accrual Status', 'Default Status',
    'Drawn Undrawn Status', 'Frozen Status', 'Past Due Status'
]
for scheme in REQUIRED_SCHEMES:
    # generate one current row (Agreement_Status_End_Dttm = NULL)
```
For delinquent agreements (`ag.is_delinquent`): add additional historical 'Past Due Status' row with non-NULL `Agreement_Status_End_Dttm`.
For frozen agreements (`ag.is_frozen`): 'Frozen Status' scheme row must use `Agreement_Status_Cd = 'FROZEN'` (exact match to seeded AGREEMENT_STATUS_TYPE row).

`AGREEMENT_CURRENCY` — every agreement gets a `Currency_Use_Cd = 'preferred'` row:
```python
{'Agreement_Id': ag.agreement_id, 'Currency_Use_Cd': 'preferred',
 'Agreement_Currency_Cd': 'USD', 'Agreement_Currency_Start_Dt': ag.open_dttm.date(),
 'Agreement_Currency_End_Dt': None}
```

`AGREEMENT_FEATURE` — loan agreements must have a 'Rate Feature' row:
```python
# For LOAN_TERM, MORTGAGE, CREDIT_CARD agreements:
{'Agreement_Id': ag.agreement_id, 'Feature_Id': RATE_FEATURE_ID,
 'Agreement_Feature_Role_Cd': 'rate',
 'Agreement_Feature_Start_Dttm': ag.open_dttm, ...}
```
`RATE_FEATURE_ID` = the Feature_Id from Tier 2 where `Feature_Subtype_Cd = 'Rate Feature'`.

`AGREEMENT_FEATURE` for balance trajectory (DECLINING cohort): generate one row per month in `ag.monthly_balances` with `Agreement_Feature_Start_Dttm` / `Agreement_Feature_End_Dttm` date ranges spanning each month.

`AGREEMENT_SCORE`: One row per agreement with the profitability model (`Model_Type_Cd = 'profitability'`). `Agreement_Score_Val` as VARCHAR probability string `"0.xxxx"`.

`AGREEMENT_RATE`: Use `ag.interest_rate` (Decimal). For mortgages, apply origination-year rate vintages from `06_supporting-enrichments.md` Part I1.

`FINANCIAL_AGREEMENT`, `DEPOSIT_AGREEMENT`, etc.: 1:1 exclusive sub-type rows. Only generate the sub-type row(s) matching `AgreementProfile.is_deposit`, `is_loan_term`, etc. `Market_Risk_Type_Cd` NOT NULL on FINANCIAL_AGREEMENT.

`INTEREST_INDEX_RATE`: Reference/lookup table only — generate **one row per distinct interest rate index type** (SOFR, PRIME, FEDFUNDS, LIBOR, EURIBOR). No daily or monthly history granularity; the PK is `Interest_Rate_Index_Cd` alone. The single row per index captures a representative rate value.

`CARD`: Generate two card types, differentiated by `Card_Subtype_Cd`:
- `'CREDIT'` — one per `CREDIT_CARD_AGREEMENT` agreement; `Agreement_Id` FK to the credit card agreement
- `'DEBIT'` — one per DEPOSIT_AGREEMENT checking account; `Agreement_Id` FK to the checking deposit agreement
`Card_Num` must be Luhn-valid 16-digit string (use `utils/luhn.py`). `Bank_Identification_Num` = first 6 digits. `Card_Security_Code_Num` = 3-digit CVV.

---

### Tier 8 — Product Hierarchy (`tier8_product_hierarchy.py`)

Tables: `PRODUCT_FEATURE`, `PRODUCT_COST`†, `PRODUCT_GROUP` (Core_DB)†, `PRODUCT_TO_GROUP`, `AGREEMENT_PRODUCT`

> `PRODUCT_COST` and `PRODUCT_GROUP` (Core_DB) DDLs have been added to `resources/Core_DB.sql` and `references/07_mvp-schema-reference.md` (2026-04-18). `PRODUCT_TO_GROUP` uses the DDL name from `07_mvp-schema-reference.md` (was written as `PRODUCT_TO_PRODUCT_GROUP` in earlier versions of this doc). Note: PIM_DB also has `PRODUCT_GROUP` and `PRODUCT_TO_GROUP` — those are separate tables generated in Tier 15.

**`AGREEMENT_PRODUCT` — critical constraint:**  
Every agreement must have at least one row with `Agreement_Product_Role_Cd = 'primary'`. This drives `ACCOUNT_DIMENSION.Product_Cd` and `Product_Desc` in Layer 2:
```python
{'Agreement_Id': ag.agreement_id, 'Product_Id': ag.product_id,
 'Agreement_Product_Role_Cd': 'primary', ...}
```

---

### Tier 9 — Party-Agreement Links (`tier9_party_agreement.py`)

Tables: `PARTY_AGREEMENT`, `PARTY_RELATED`, `PARTY_CLAIM`

**`PARTY_RELATED` — critical for Layer 2 indicator derivations:**

Every individual customer party must have a `PARTY_RELATED` row linking them to the bank entity (a seeded `BANK_PARTY_ID` constant):
```python
{'Party_Id': cp.party_id, 'Related_Party_Id': BANK_PARTY_ID,
 'Party_Related_Role_Cd': 'customer of enterprise',   # → Customer_Ind = 'Y'
 'Party_Structure_Type_Cd': 'banking_relationship',
 'Party_Related_Start_Dttm': cp.party_since}
```
Prospect party (small %; pre-acquisition): `Party_Related_Role_Cd = 'prospect of enterprise'`  
Associate/employee party: `Party_Related_Role_Cd = 'employee of enterprise'`

Seed one `BANK_PARTY_ID` constant (e.g., `9999999`) in `config/settings.py` representing the bank itself.

**`PARTY_AGREEMENT`:**
```python
{'Party_Id': cp.party_id, 'Agreement_Id': ag.agreement_id,
 'Party_Agreement_Role_Cd': 'customer',   # → Customer_Account_Ind = '1'
 'Party_Agreement_Start_Dt': ag.open_dttm.date()}
```
For loan agreements: also generate a row with `Party_Agreement_Role_Cd = 'borrower'` (→ Borrower_Ind).

---

### Tier 10 — Events (`tier10_events.py`)

Tables: `EVENT`, `EVENT_PARTY`, `EVENT_CHANNEL_INSTANCE`, `FINANCIAL_EVENT`, `FINANCIAL_EVENT_AMOUNT`, `FUNDS_TRANSFER_EVENT`, `ACCESS_DEVICE_EVENT`, `DIRECT_CONTACT_EVENT`, `COMPLAINT_EVENT` (customized)

`EVENT.Event_Id`: BIGINT (Q2 resolution — override INTEGER in Core_DB DDL).

Generate 1–5 events per customer per month. DECLINING cohort: event frequency decreases each month. CHURNED cohort: events stop after `Agreement_Close_Dttm`.

`FINANCIAL_EVENT`: `In_Out_Direction_Type_Cd` values: `'IN'` (interest earned on deposits) or `'OUT'` (interest paid on loans, fees charged). Both directions must be present in the dataset for Layer 2 `FINANCIAL_EVENT_AMOUNT` to produce Interest_Earned and Interest_Paid.

Fee records: generate monthly statement fee events with `Financial_Event_Type_Cd = 'STATEMENT_FEE'`. Generate overdraft fee events for accounts with negative balance months.

`COMPLAINT_EVENT`: Generate for ~5% of customers. `Event_Sentiment_Cd` SMALLINT: 1=positive, 2=neutral, 3=negative. `Event_Channel_Type_Cd` SMALLINT: 1–5. `Event_Multimedia_Object_Ind` CHAR(1).

---

### Tier 11 — CRM (`tier11_crm.py`)

Tables: `CAMPAIGN_STATUS`, `PROMOTION`, `PROMOTION_OFFER`

`CAMPAIGN_STATUS`: At least one record per campaign. Layer 2 selects `max(Campaign_Status_Dttm)` — ensure at least one status row exists per campaign with a `Campaign_Status_Cd` from the seeded `CAMPAIGN_STATUS_TYPE` table.

`PROMOTION_OFFER`: Up to 5 offers per promotion. PROMOTION_BB Layer 2 rule creates columns for 1st–5th Promotion_Offer_Id; fewer than 5 is acceptable (higher-order columns will be NULL).

---

### Tier 13 — Tasks (`tier13_tasks.py`)

Tables: `PARTY_TASK`, `PARTY_TASK_STATUS`, `TASK_ACTIVITY`, `TASK_ACTIVITY_STATUS`

Generate tasks only for customers with COMPLAINT_EVENT records (FK: `Source_Event_Id`). All codes are SMALLINT — use `code_values.py` enumerations.

---

### Tier 14 — CDM_DB (`tier14_cdm.py`)

Tables: `CDM_DB.PARTY`, `CDM_DB.INDIVIDUAL`, `CDM_DB.ORGANIZATION`, `CDM_DB.HOUSEHOLD`, `INDIVIDUAL_TO_INDIVIDUAL`, `INDIVIDUAL_TO_HOUSEHOLD`, `INDIVIDUAL_TO_ORGANIZATION`, `ORGANIZATION_TO_ORGANIZATION`, `PARTY_TO_AGREEMENT_ROLE`, `PARTY_TO_EVENT_ROLE`, `PARTY_SEGMENT`, `ADDRESS` (CDM), `ADDRESS_TO_AGREEMENT`, `PARTY_CONTACT`, `CONTACT_TO_AGREEMENT`, `PARTY_INTERRACTION_EVENT`

All CDM_DB tables are MULTISET. Stamp both `di_*` and `Valid_From_Dt / Valid_To_Dt / Del_Ind`.

`CDM_DB.PARTY.CDM_Party_Id` = `CustomerProfile.party_id` (same ID space — Q1 resolution).

`CDM_DB.PARTY` SMALLINT codes:
- `Source_Cd`: 1 (CIF source system)
- `Party_Type_Cd`: 1=Individual, 2=Organization
- `Party_Lifecycle_Phase_Cd`: 1=External, 2=Prospect, 3=Active Customer (3 for most)
- `Survival_Record_Ind`: `'Y'` (all generated records are survival records)

`CDM_DB.ADDRESS`: **Add `CDM_Address_Id` column** (BIGINT surrogate, per `05_architect-qa.md` Q6). The DDL is missing this — it must be included in the generated CSV.

`PARTY_INTERRACTION_EVENT`: Table name must preserve double-R typo `INTERRACTION` exactly (matches DDL). All codes SMALLINT.

`PARTY_CONTACT`: `Contact_Type_Cd` 1=email, 2=phone, 3=mobile. `Contact_Value` must contain a realistic value for the type (Faker email/phone). Table name per `07_mvp-schema-reference.md` line 194.

`PARTY_TO_AGREEMENT_ROLE`: `Agreement_Id` is BIGINT; `Role_Type_Cd` SMALLINT (1=primary).

---

### Tier 15 — PIM_DB (`tier15_pim.py`)

Tables: `PIM_DB.PRODUCT`, `PRODUCT_PARAMETERS`, `PRODUCT_PARAMETER_TYPE`, `PRODUCT_TO_GROUP`, `PRODUCT_GROUP`, `PRODUCT_GROUP_TYPE`

`PIM_DB.PRODUCT.Product_Id` must match `Core_DB.PRODUCT.Product_Id` (cross-schema FK).

`PRODUCT_GROUP`: Recursive self-reference — `Parent_Group_Id` points to the same table's `Product_Group_Id`. Top-level groups point to **themselves** (per `05_architect-qa.md` Q3).

Product hierarchy (CLV 8-type grouping):
```
Root (self-referential)
  └── CLV Product Types (Product_Group_Type_Cd = CLV_TYPE)
        ├── Checking
        ├── Savings
        ├── Retirement
        ├── Credit Card
        ├── Vehicle Loan
        ├── Mortgage
        ├── Investments
        └── Insurance
```

All `PRODUCT_GROUP_TYPE.Product_Group_Type_Cd` and `PRODUCT_PARAMETER_TYPE.PIM_Parameter_Type_Cd` are SMALLINT — self-defined by the generator lookup tables.

---

## 10. Statistical Distributions (`config/distributions.py`)

All distributions use a seeded `numpy.random.Generator` for reproducibility.

### Which distribution source to use

| Layer | Distribution Source | Usage |
|-------|---------------------|-------|
| Feature Store features (CLV, deposit balance, CC balance, investments, tenure, income) | **WP5 (file 02)** — ground truth | These are aggregate Feature Store metrics |
| Per-account `AGREEMENT_FEATURE.Agreement_Feature_Amt` | **SCF income-quartile stratified (file 06 Part C)** | Per-account point-in-time balance |
| Demographics (age, gender, marital, occupation, ethnicity) | **SCF (file 06 Part A)** | Not specified in file 02 |
| Account ownership rates (which products to generate) | **SCF (file 06 Part B)** | Not specified in file 02 |

The two tension points resolved:
- **Average Deposit Balance**: WP5 (Mean $2K) applies to Feature Store metric; SCF stratified ranges apply to per-account generation
- **Total Investments AUM**: WP5 applies only to investment-holding customers (~59%); remaining ~41% have AUM = 0 / no investment AGREEMENT

### Key sampler signatures

```python
# Age: SCF AGECL weights
def sample_age(n) -> np.ndarray
    # weights: [0.133, 0.166, 0.178, 0.223, 0.188, 0.110]
    # ranges:  [20-34, 35-44, 45-54, 55-64, 65-74, 75-82]
    # Hard cap: 1940-01-01 to 2005-12-31 (file 01)

# Balance: SCF income-quartile stratified, log-normal
def sample_deposit_balance(income_quartile) -> Decimal
    # Q1: median $350, Q2: $1,600, Q3: $4,000, Q4: $23,000

# FICO: SCF credit denial rates by ethnicity + income
def sample_fico(ethnicity, income_quartile) -> int  # 300–850

# Mortgage rate: vintage-year based
def sample_mortgage_rate(origination_year) -> Decimal
    # Pre-2020: 3.5–4.5%, 2020: ~3.0%, 2021: ~3.1%, 2022: 5.0–7.0%

# Income: occupation-based annual ranges
def sample_annual_income(occupation_cd, income_quartile) -> Decimal
    # EMP: $24K–$450K, SELF_EMP: $30K–$5M, RETIRED: $12K–$500K
```

### Mandatory correlation rules (enforced in UniverseBuilder)

1. Under-35 → lower mortgage rate (23.7%); higher student loan rate; smaller retirement balances
2. Income Q4 → retirement ownership 90%; Q1 → 13%
3. Income Q4 → CC balance carrier rate 24% (lower); Q2 → 50% (higher)
4. Self-employed (`SELF_EMP`) → business equity records required (`ORGANIZATION + BUSINESS`)
5. LIFECL=3 (families with kids) → mortgage + vehicle loan more likely
6. `has_internet = False` → `preferred_channel_cd = 1` (BRANCH); no ONLINE/MOBILE contact preferences
7. **INDIVIDUAL_PAY_TIMING / INDIVIDUAL_BONUS_TIMING — reserved placeholder ORGANIZATION** (per `05_architect-qa.md` Q7): At universe build time, ensure one reserved ORGANIZATION row with `Organization_Party_Id = 9999999` and name 'Self-Employment Organization' is injected into the ORGANIZATION CSV. All customers with `occupation_cd = 'SELF_EMP'` have their `INDIVIDUAL_PAY_TIMING.Business_Party_Id` and `INDIVIDUAL_BONUS_TIMING.Business_Party_Id` set to `9999999`. Employed individuals (`occupation_cd = 'EMP'`) point to a real generated ORGANIZATION row. RETIRED and NOT_WORKING individuals are excluded from these two tables.

---

## 11. Output Format (`output/writer.py`)

```python
SIM_DATE     = date(2026, 3, 31)
HISTORY_START = date(2025, 10, 1)
HIGH_TS      = '9999-12-31 00:00:00.000000'
HIGH_DATE    = '9999-12-31'
```

| Data type | CSV format |
|-----------|------------|
| NULL | empty field (not `"NULL"`) |
| TIMESTAMP(6) | `2025-10-15 09:23:44.000000` |
| DATE | `2025-10-15` |
| CHAR(1) flag | `Y` or `N` |
| CHAR(3) flag | `Yes` or `No` |
| BIGINT | plain integer, no quotes |
| DECIMAL | `1234.5600` (4dp for amounts, 12dp for rates) |
| VARCHAR | unquoted unless contains comma/quote |

- Column order in CSV **must match DDL declaration order** (required for Teradata BTEQ/FastLoad)
- Quoting: `csv.QUOTE_MINIMAL`
- Encoding: UTF-8
- File naming: exact DDL table name, e.g., `PARTY_INTERRACTION_EVENT.csv` (preserve typo)

---

## 12. Layer 2 Transformation-Readiness Checklist

These 22 constraints (from `02_data-mapping-reference.md` Step 3) are enforced by generators and verified by `output/validator.py` before finalising output. Validator halts generation and reports violations.

| # | Constraint | Enforced in |
|---|------------|-------------|
| 1 | AGREEMENT_STATUS has all 6 scheme types per agreement | Tier 7 loop |
| 2 | All lookup DESC columns exist (code→desc joins) | Tier 0 seeding |
| 3 | INDIVIDUAL_NAME: SIM_DATE between Start_Dt and End_Dt | Tier 4: End_Dt = 9999-12-31 |
| 4 | PARTY_LANGUAGE_USAGE: 'primary spoken' + 'primary written' | Tier 4: two rows per party |
| 5 | PARTY_STATUS: ≥1 record per party | Tier 4: always generated |
| 6 | AGREEMENT_FEATURE Rate Feature for loans | Tier 7: explicit rate feature row |
| 7 | AGREEMENT_PRODUCT: ≥1 'primary' role per agreement | Tier 8: 'primary' row first |
| 8 | AGREEMENT_CURRENCY: 'preferred' row per agreement | Tier 7: 'preferred' row always |
| 9 | PARTY_AGREEMENT: 'customer' role per agreement | Tier 9: 'customer' role always |
| 10 | PARTY_RELATED: 'customer of enterprise' per individual party | Tier 9: bank relationship row |
| 11 | PARTY_AGREEMENT: 'borrower' role for loan agreements | Tier 9: conditional on product_type |
| 12 | PARTY_AGREEMENT: 'customer' for retail banking agreements | Tier 9: all retail → 'customer' |
| 13 | AGREEMENT_STATUS 'Frozen Status' scheme code = 'FROZEN' | Tier 0 seed + Tier 7 code |
| 14 | ORGANIZATION NAICS/SIC/GICS: exactly one Primary_*_Ind='Yes' | Tier 4: enforced per org |
| 15 | CAMPAIGN_STATUS: ≥1 record per campaign | Tier 11: always generated |
| 16 | PROMOTION_OFFER: up to 5 offers per promotion (OK if fewer) | Tier 11: 1–5 generated |
| 17 | AGREEMENT_SCORE: profitability model row per agreement | Tier 7: Model_Type_Cd='profitability' |
| 18 | PARTY_SCORE: customer profitability model row per party | Tier 4: Model_Purpose_Cd='customer profitability' |
| 19 | Territory chain: ISO_3166_COUNTRY_SUBDIVISION_STANDARD populated | Tier 0/1 seeding |
| 20 | PRODUCT_GROUP: CLV type grouping in PIM | Tier 15: 8 CLV groups |
| 21 | AGREEMENT_STATUS Frozen_Ind: code desc matches 'Frozen' | Tier 0 seed row |
| 22 | PARTY_IDENTIFICATION: SSN/Passport/DL type rows per individual | Tier 4: 1–3 types per party |

---

## 13. Libraries

```
numpy>=1.26          # All RNG — use numpy.random.Generator(numpy.random.PCG64(seed))
pandas>=2.0          # DataFrames and CSV I/O
faker>=24.0          # Names, addresses, emails, phone numbers
python-dateutil      # Date arithmetic
scipy>=1.12          # Log-normal and truncated normal distributions
```

No ORMs, no databases, no simulation frameworks. Pure in-memory → CSV.

---

## 14. Key Design Decisions and Rationale

### Decision 1: Entity-first registry, not table-first generation
**Why:** Cross-table correlations (age → product mix → balance → credit score → CLV segment) span 10+ tables. If each table generates independently, the Layer 2 CUSTOMER DIMENSION will join a 55-year-old with student loans and $200 checking balance — implausible data breaks demo credibility. The CustomerProfile is the single source of truth; all tables are derived from it.

### Decision 2: Seed data baked in (not randomly generated) for Tier 0
**Why:** Lookup tables must contain exact code values that Layer 2 rules match literally. `AGREEMENT_STATUS_TYPE` must have `Agreement_Status_Cd = 'FROZEN'` to make `Frozen_Ind = '1'` fire. `FEATURE` must have a row with `Feature_Subtype_Cd = 'Rate Feature'` or the LOAN_ACCOUNT_BB rate derivation returns NULL. Randomising these codes guarantees Layer 2 failures.

### Decision 3: BIGINT everywhere (overrides all INTEGER declarations)
**Why:** `05_architect-qa.md` Q1 explicitly resolves this: "Wherever this problem arises choosing between INTEGER and BIGINT — always choose BIGINT." CDM_DB consumers of `Agreement_Id` and `Event_Id` declare BIGINT; `Core_DB.AGREEMENT.Agreement_Id` declares INTEGER. The BIGINT rule wins everywhere.

### Decision 4: Same party_id in Core_DB and CDM_DB
**Why:** `02_data-mapping-reference.md` WP3 FSAS Customizations explicitly states "Replace Party Id with MDM Party ID (CDM)". All Core_DB tables referencing `Party_Id` draw from the `CDM_DB.PARTY.CDM_Party_Id` universe. Generate once, use everywhere.

### Decision 5: SCF distributions for demographics; WP5 for Feature Store metrics
**Why:** These operate at different abstraction levels. WP5 `Average Deposit Balance` (Mean $2K) is a Feature Store aggregate computed across ALL customers (including 10% unbanked at $0). SCF stratified ranges are point-in-time per-account balances. Using WP5 ranges for `AGREEMENT_FEATURE.Agreement_Feature_Amt` would produce unrealistically low per-account values; using SCF for the Feature Store metric would over-estimate. The resolution in `06_supporting-enrichments.md` Part C1 is authoritative.

### Decision 6: Validator as a hard gate before CSV write
**Why:** Silent FK violations or missing Layer 2 constraint rows produce output that looks plausible but silently breaks Layer 2 transforms. A validator that runs all 22 checks and halts on first failure is cheaper than debugging a broken ACCOUNT_STATUS_DIMENSION two sprints later.

### Decision 7: PARTY_INTERRACTION_EVENT typo preserved
**Why:** The DDL table name has a double-R typo. The output CSV filename and all FK references must use the typo verbatim. Any "correction" creates a mismatch with the target DDL.

### Decision 8: No `GEOSPATIAL` table in output
**Why:** `GEOSPATIAL.Geospatial_Coordinates_Geosptl` is declared as `ST_Geometry` — a Teradata spatial type that has no valid CSV representation. The table is skipped entirely. `GEOSPATIAL_POINT` (lat/lon DECIMAL) is generated normally.

---

## 15. `main.py` Orchestration

```python
def main():
    config = load_config()
    rng = np.random.default_rng(config.seed)
    
    # Phase 1: Build universe
    universe = UniverseBuilder().build(config, rng)
    ctx = universe.to_context(config, rng)
    
    # Phase 2: Run tiers in order
    tiers = [
        Tier0Lookups(), Tier1Geography(), Tier2Core(),
        Tier3PartySubtypes(), Tier4PartyAttributes(), Tier5Location(),
        Tier6Links(), Tier7AgreementDetails(), Tier8ProductHierarchy(),
        Tier9PartyAgreement(), Tier10Events(), Tier11CRM(),
        Tier13Tasks(), Tier14CDM(), Tier15PIM(),
    ]
    
    for tier in tiers:
        new_tables = tier.generate(ctx)
        ctx.tables.update(new_tables)
        print(f"  {tier.__class__.__name__}: {sum(len(df) for df in new_tables.values()):,} rows across {len(new_tables)} tables")
    
    # Phase 3: Validate
    errors = Validator().check_all(ctx)
    if errors:
        for e in errors:
            print(f"VALIDATION ERROR: {e}")
        sys.exit(1)
    
    # Phase 4: Write CSVs
    Writer(config.output_dir).write_all(ctx.tables)
    print(f"Done. Output in {config.output_dir}")
```

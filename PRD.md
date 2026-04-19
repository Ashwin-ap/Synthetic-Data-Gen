# Product Requirements Document
## CIF Synthetic Data Generator — Layer 1 MVP

**Version:** 1.0  
**Date:** 2026-04-17  
**Status:** Approved for implementation  
**Design reference:** `mvp-tool-design.md`

---

## 1. Executive Summary

The CIF Synthetic Data Generator produces a statistically coherent set of synthetic banking CSV files that populate the Layer 1 tables of Teradata's Financial Services Data Model (FSDM). The output is immediately usable as the source layer for WP3 Layer 2 transformation rules, enabling end-to-end demonstration of the Customer Intelligence Framework (CIF) data pipeline without requiring access to real customer data.

The generator produces ~3,000 customers, ~5,000 accounts, and supporting reference/event data across **206 tables** (as defined in `references/07_mvp-schema-reference.md`; 197 original + 9 DDL-gap tables resolved 2026-04-18), spanning the `Core_DB` (FSDM iDM), `CDM_DB` (MDM Customer), and `PIM_DB` (MDM Product) schemas.

---

## 2. Problem Statement

Demonstrating the CIF pipeline — from raw source data through FSDM Layer 1, through WP3 Building Block transforms, to FSAS dimensions and end data products — requires a populated Layer 1 that satisfies all the structural constraints the Layer 2 transformation rules assume. Real customer data cannot be used. Manually crafted test data does not scale to the 80+ tables required, and random generation without cross-table correlation produces output that breaks Layer 2 joins (NULL dimensions, missing indicators, implausible customer profiles).

The generator must produce data that is:
- **Structurally correct**: all FK references valid, all NOT NULL constraints satisfied
- **Transformation-ready**: every one of the 22 Layer 2 prerequisite constraints explicitly guaranteed
- **Statistically coherent**: customer demographics, product holdings, balances, and behaviours are correlated as they would be in real banking data

---

## 3. Target Users

| User | Use |
|------|-----|
| **Solution CoE engineers** | Develop and test Layer 2 APBB/DIM transformation logic against a consistent, reproducible source dataset |
| **CIF architects** | Demonstrate the full FSDM → FSAS → End Data Product pipeline to banking clients |
| **Data product developers** | Validate CUSTOMER DIMENSION, ACCOUNT DIMENSION, and other FSAS outputs against known inputs |
| **QA / testing** | Baseline regression dataset for pipeline changes |

---

## 4. MVP Scope

### 4.1 In-scope layers

| Layer | Schema | Description |
|-------|--------|-------------|
| Layer 1 — FSDM iDM | `Core_DB` | Full FSDM entity model: agreements, parties, products, campaigns, channels, addresses, events, rates, features, and all lookup/reference tables (174 tables per schema reference; GEOSPATIAL excluded → 173 generated) |
| Layer 1 — MDM Customer | `CDM_DB` | Survivored party, household, relationship, segment, address, contact, interaction event tables (16 tables) |
| Layer 1 — MDM Product | `PIM_DB` | Product catalogue with parameters, group hierarchy, and CLV product taxonomy (6 tables) |
| Layer 1 — FSDM Extensions | `Core_DB` (customized) | Contact preferences, complaint events, tasks, activities (6 tables: PARTY_CONTACT_PREFERENCE, COMPLAINT_EVENT, PARTY_TASK, PARTY_TASK_STATUS, TASK_ACTIVITY, TASK_ACTIVITY_STATUS — the last 3 are included in the Core_DB count of 174; PARTY_CONTACT_PREFERENCE, PARTY_TASK_STATUS, TASK_ACTIVITY_STATUS have no DDL in schema reference yet) |

### 4.2 In-scope table domains

**Agreement & Financial Products:** AGREEMENT and all sub-types (FINANCIAL_AGREEMENT, DEPOSIT_AGREEMENT, DEPOSIT_TERM_AGREEMENT, CREDIT_AGREEMENT, LOAN_AGREEMENT, LOAN_TERM_AGREEMENT, MORTGAGE_AGREEMENT, CREDIT_CARD_AGREEMENT, LOAN_TRANSACTION_AGREEMENT), AGREEMENT_STATUS, AGREEMENT_CURRENCY, AGREEMENT_FEATURE, AGREEMENT_METRIC, AGREEMENT_RATE, AGREEMENT_SCORE, AGREEMENT_PRODUCT, CARD, TERM_FEATURE, INTEREST_RATE_INDEX, INTEREST_INDEX_RATE, VARIABLE_INTEREST_RATE_FEATURE

**Party & Individual:** INDIVIDUAL (Core_DB), INDIVIDUAL_NAME, INDIVIDUAL_GENDER_PRONOUN, INDIVIDUAL_MARITAL_STATUS, INDIVIDUAL_VIP_STATUS, INDIVIDUAL_OCCUPATION, INDIVIDUAL_MILITARY_STATUS, INDIVIDUAL_MEDICAL, INDIVIDUAL_SKILL, INDIVIDUAL_SPECIAL_NEED, INDIVIDUAL_BONUS_TIMING, INDIVIDUAL_PAY_TIMING, ASSOCIATE_EMPLOYMENT

**Organization:** ORGANIZATION (Core_DB), ORGANIZATION_NAME, ORGANIZATION_NAICS, ORGANIZATION_NACE, ORGANIZATION_SIC, ORGANIZATION_GICS, BUSINESS

**Party shared:** PARTY_AGREEMENT, PARTY_RELATED, PARTY_CLAIM, PARTY_LANGUAGE_USAGE, PARTY_STATUS†, PARTY_SCORE, PARTY_CREDIT_REPORT_SCORE, PARTY_IDENTIFICATION, PARTY_DEMOGRAPHIC, DEMOGRAPHIC_VALUE, PARTY_SEGMENT† (Core_DB only — CDM_DB version has DDL), PARTY_SPECIALTY

**Address & Location:** ADDRESS, STREET_ADDRESS, STREET_ADDRESS_DETAIL, PARCEL_ADDRESS, POST_OFFICE_BOX_ADDRESS, POSTAL_CODE, CITY, COUNTY, TERRITORY, REGION, COUNTRY, GEOGRAPHICAL_AREA, GEOGRAPHICAL_AREA_CURRENCY, ISO_3166_COUNTRY_STANDARD, ISO_3166_COUNTRY_SUBDIVISION_STANDARD, GEOSPATIAL_POINT, LOCATOR_RELATED, PARTY_LOCATOR

**Products & Features:** PRODUCT (Core_DB), FEATURE, TERM_FEATURE, PRODUCT_FEATURE, PRODUCT_COST†, PRODUCT_GROUP (Core_DB)†, PRODUCT_TO_GROUP, ANALYTICAL_MODEL

**Campaign & Promotion:** CAMPAIGN, CAMPAIGN_STATUS, PROMOTION, PROMOTION_OFFER, MARKET_SEGMENT

**Channel & Events:** CHANNEL_INSTANCE, CHANNEL_INSTANCE_STATUS, CHANNEL_TYPE, EVENT, EVENT_PARTY, EVENT_CHANNEL_INSTANCE†, FINANCIAL_EVENT, FINANCIAL_EVENT_AMOUNT†, FUNDS_TRANSFER_EVENT†, ACCESS_DEVICE_EVENT†, DIRECT_CONTACT_EVENT†

**Customized extensions:** PARTY_CONTACT_PREFERENCE, COMPLAINT_EVENT, PARTY_TASK, PARTY_TASK_STATUS, TASK_ACTIVITY, TASK_ACTIVITY_STATUS

**MDM CDM_DB:** PARTY, INDIVIDUAL, ORGANIZATION, HOUSEHOLD, INDIVIDUAL_TO_INDIVIDUAL, INDIVIDUAL_TO_HOUSEHOLD, INDIVIDUAL_TO_ORGANIZATION, ORGANIZATION_TO_ORGANIZATION, PARTY_TO_AGREEMENT_ROLE, PARTY_TO_EVENT_ROLE, PARTY_SEGMENT (CDM), ADDRESS (CDM), ADDRESS_TO_AGREEMENT, PARTY_CONTACT, CONTACT_TO_AGREEMENT, PARTY_INTERRACTION_EVENT

**MDM PIM_DB:** PRODUCT, PRODUCT_PARAMETERS, PRODUCT_PARAMETER_TYPE, PRODUCT_TO_GROUP, PRODUCT_GROUP, PRODUCT_GROUP_TYPE

**All lookup/type tables:** ~35 `*_TYPE` / `*_SUBTYPE` / `*_CLASSIFICATION` tables (AGREEMENT_SUBTYPE, GENDER_TYPE, MARITAL_STATUS_TYPE, NATIONALITY_TYPE, LANGUAGE_TYPE, NAICS_INDUSTRY, GICS_SECTOR_TYPE, SIC, NACE_CLASS, CURRENCY, etc.)

> **DDL gaps resolved (2026-04-18)** — All 9 previously-missing DDL tables have been added to `resources/Core_DB.sql` and `references/07_mvp-schema-reference.md`. Column definitions were derived from WP2/WP3 mapping rules in `references/02_data-mapping-reference.md`.
>
> | Table | Required by | Resolution |
> |-------|-------------|------------|
> | `PARTY_STATUS` | 02 Tier 4; Layer 2 constraint #5 | DDL added to Core_DB.sql + 07 |
> | `PARTY_SEGMENT` (Core_DB) | 02 Tier 4 | DDL added to Core_DB.sql + 07; CDM_DB version unchanged |
> | `PRODUCT_COST` | 02 Tier 8; WP2 mapping | DDL added to Core_DB.sql + 07 |
> | `PRODUCT_GROUP` (Core_DB) | 02 Tier 8 | DDL added to Core_DB.sql + 07; PIM_DB.PRODUCT_GROUP unchanged |
> | `EVENT_CHANNEL_INSTANCE` | 02 Tier 10; Layer 2 event chain | DDL added to Core_DB.sql + 07 |
> | `FINANCIAL_EVENT_AMOUNT` | 02 Tier 10; Layer 2 interest earned/paid | DDL added to Core_DB.sql + 07 |
> | `FUNDS_TRANSFER_EVENT` | 02 Tier 10; WP2 payment mapping | DDL added to Core_DB.sql + 07 |
> | `ACCESS_DEVICE_EVENT` | 02 Tier 10; WP2 device event mapping | DDL added to Core_DB.sql + 07 |
> | `DIRECT_CONTACT_EVENT` | 02 Tier 10; WP2 complaint/interaction | DDL added to Core_DB.sql + 07 |
>
> Additionally, `PARTY_CONTACT_PREFERENCE`, `PARTY_TASK_STATUS`, and `TASK_ACTIVITY_STATUS` (Customized extensions) have DDL in `resources/Core_DB_customized.sql` but are not listed in `07_mvp-schema-reference.md`'s summary table. They are in scope per 02 Tiers 4 and 13.

### 4.3 Output format

- One CSV file per table, named exactly as the DDL table name
- Subdirectory per schema: `output/Core_DB/`, `output/CDM_DB/`, `output/PIM_DB/`
- Column order matches DDL declaration order
- NULL = empty field; TIMESTAMP(6) = `YYYY-MM-DD HH:MM:SS.ffffff`; DATE = `YYYY-MM-DD`
- High date sentinel: `9999-12-31` (DATE) / `9999-12-31 00:00:00.000000` (TIMESTAMP)
- CHAR(1) flags: `Y` / `N`; CHAR(3) flags: `Yes` / `No`

### 4.4 Generation scale

| Parameter | Value |
|-----------|-------|
| Unique customers | ~3,000 |
| Agreements | ~5,000 |
| Individual / Organization | 80% / 20% |
| History window | 2025-10-01 to 2026-03-31 (6 months) |
| Lifecycle cohorts | 55% Active / 30% Declining / 5% Churned / 10% New |
| Random seed | 42 (configurable) |

---

## 5. Core Design Principles

**1. Correctness over completeness.**  
Every FK reference must be valid by construction; every NOT NULL constraint satisfied. A smaller but structurally sound dataset is preferred over a larger one with integrity violations.

**2. Layer 2 transformation-readiness is explicit, not accidental.**  
All 22 structural prerequisites identified in `references/02_data-mapping-reference.md` Step 3 are enforced at generation time and verified by a post-generation validator before any CSV is written.

**3. Cross-table correlation is preserved.**  
A customer's age, income quartile, and lifecycle cohort drive their product mix, balance amounts, credit score, status history, and event frequency. These decisions are made atomically in the `UniverseBuilder` before any table is written. No table generates data independently.

**4. Seed data is canonical, not random.**  
Lookup/reference tables (`*_TYPE`, `*_SUBTYPE`) are hardcoded from the authoritative code values in `references/02_data-mapping-reference.md`, `references/01_schema-reference.md`, and `references/07_mvp-schema-reference.md` (the filtered, finalised DDL-derived set that defines MVP table scope). Randomising code values would break Layer 2 literal-match rules (e.g. `Frozen_Ind` derivation requires `Agreement_Status_Desc = 'Frozen'` exactly).

**5. Statistical realism without over-engineering.**  
Demographic distributions follow SCF 2022 data (age, gender, marital status, occupation, account ownership rates). Financial amounts use WP5 Feature Store distributions for aggregate metrics and SCF income-quartile stratified ranges for per-account amounts. Correlations (age × product mix, income × balance, cohort × balance trajectory) are enforced; exotic multi-variate models are not.

**6. Reproducibility.**  
A single integer seed in `config/settings.py` drives all random number generation. Same seed → identical output.

---

## 6. Architecture Overview

The generator is a Python application using an **Entity-First Registry + Tiered Writers** pattern.

```
Phase 1 — Universe Build (in-memory, no I/O)
  UniverseBuilder
    → CustomerProfile registry (~3,000)     all demographic + product decisions
    → AgreementProfile registry (~5,000)    all account + balance decisions

Phase 2 — Tiered Writing (pure transformation, no statistical decisions)
  Tier 0  → Lookup/reference CSVs  (seeded, not randomly generated)
  Tier 1  → Geography CSVs
  Tier 2  → Core entity CSVs
  Tier 3  → Party subtype CSVs
  Tier 4  → Party attribute CSVs
  Tier 5  → Location CSVs
  Tier 6  → Link CSVs
  Tier 7  → Agreement detail CSVs   ← most critical for Layer 2 readiness
  Tier 8  → Product hierarchy CSVs
  Tier 9  → Party-agreement CSVs    ← PARTY_RELATED enterprise roles
  Tier 10 → Event CSVs
  Tier 11 → CRM CSVs
  Tier 13 → Task CSVs
  Tier 14 → CDM_DB CSVs
  Tier 15 → PIM_DB CSVs

Phase 3 — Validation (22-point Layer 2 constraint check; halts on failure)

Phase 4 — CSV Write
```

See `mvp-tool-design.md` for complete component breakdown, profile dataclass field lists, UniverseBuilder build sequence, per-tier table lists, and validator constraint mapping.

**Libraries:** `numpy`, `pandas`, `faker`, `scipy`, `python-dateutil`. No databases, no ORMs.

---

## 7. Key Technical Decisions

### 7.1 BIGINT everywhere
All ID columns (`Party_Id`, `Agreement_Id`, `Event_Id`, and all FKs) are generated as BIGINT regardless of the INTEGER declaration in `Core_DB` DDL. Rationale: `CDM_DB` consumers (`PARTY_TO_AGREEMENT_ROLE.Agreement_Id`, `ADDRESS_TO_AGREEMENT.Agreement_Id`, `COMPLAINT_EVENT.Event_Id`) are all declared BIGINT. The universal BIGINT rule from `05_architect-qa.md` Q1/Q2 resolves all cross-schema mismatches.

### 7.2 Shared Party ID space (Core_DB + CDM_DB)
`CDM_DB.PARTY.CDM_Party_Id` and `Core_DB` Party references share the same ID universe. `CustomerProfile.party_id` is used as both `CDM_Party_Id` (CDM_DB) and the `Party_Id` FK referenced in Core_DB tables. This reflects the WP3 FSAS Customization: "Replace Party Id with MDM Party ID (CDM)."

### 7.3 Two DI column sets for CDM_DB / PIM_DB
- `di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind`: stamped on ALL tables
- `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind`: stamped additionally on CDM_DB and PIM_DB tables only
- `di_data_src_cd` and `di_proc_name`: NULL (no source system code or process name needed)
- Active records: `di_end_ts = 9999-12-31 00:00:00.000000`; `Valid_To_Dt = 9999-12-31`

### 7.4 SCD2 history approach
- A record is **current** when its `*_End_Dt` / `*_End_Dttm` is NULL (Core_DB) or `9999-12-31` (CDM_DB/PIM_DB)
- Historical records are generated for: AGREEMENT_STATUS (delinquency transitions), INDIVIDUAL_NAME (maiden/married name change for married cohort), PARTY_STATUS (churned customers)
- DECLINING cohort balance trajectory: `AGREEMENT_FEATURE` generates 6 monthly rows with explicit `Agreement_Feature_Start_Dttm` / `Agreement_Feature_End_Dttm` date ranges across the history window

### 7.5 Exclusive sub-typing for AGREEMENT
Each agreement follows exactly one sub-type path through the inheritance hierarchy (AGREEMENT → FINANCIAL_AGREEMENT → DEPOSIT_AGREEMENT OR CREDIT_AGREEMENT → ...). An agreement cannot be both a DEPOSIT_AGREEMENT and a LOAN_AGREEMENT. This is enforced via the `AgreementProfile.is_*` flags set atomically in `UniverseBuilder`.

### 7.6 FK generation order (15 tiers)
The tier sequence satisfies all FK dependencies from the ground up: reference/lookup tables (no deps) → geography → core entities → party subtypes → party attributes → location → links → agreement details → product hierarchy → party-agreement bridges → events → CRM → tasks → CDM → PIM. No tier reads from a table it has not yet generated.

### 7.7 SCF distributions for demographics; WP5 for Feature Store metrics
These operate at different abstraction levels and are not in conflict:
- **WP5 distributions** (Mean $2K deposit, Mean $2.5K CC balance, etc.) are Feature Store aggregate metrics — used for `PARTY_SCORE.Party_Score_Val` and similar feature-level derivations
- **SCF income-quartile stratified ranges** are per-account point-in-time balances — used for `AGREEMENT_FEATURE.Agreement_Feature_Amt`

### 7.8 CDM_DB ADDRESS primary key
`CDM_DB.ADDRESS` DDL is missing `CDM_Address_Id`. Per `05_architect-qa.md` Q6, a BIGINT surrogate key `CDM_Address_Id` is added to this table's generated CSV. The DDL should be updated correspondingly before loading.

### 7.9 GEOSPATIAL table skipped
`Core_DB.GEOSPATIAL` contains a `Geospatial_Coordinates_Geosptl ST_Geometry` column with no valid CSV representation. This table is excluded from output. `GEOSPATIAL_POINT` (lat/lon as DECIMAL) is generated normally.

### 7.10 PARTY_INTERRACTION_EVENT typo preserved
The DDL table name contains a double-R typo: `PARTY_INTERRACTION_EVENT`. The output CSV filename and all FK references preserve this spelling verbatim to match the target DDL.

### 7.12 Self-employed placeholder for INDIVIDUAL_PAY_TIMING and INDIVIDUAL_BONUS_TIMING
Both tables are in scope (per `05_architect-qa.md` Q7). Both carry `Business_Party_Id NOT NULL` as an FK to `ORGANIZATION`. Self-employed individuals (~21.7%) have no real employer, so a dedicated placeholder row — 'Self-Employment Organization', reserved ID `9999999` — is inserted into the ORGANIZATION CSV. All self-employed individuals in these two tables reference that reserved ID. No schema changes, no new columns, no new tables are required.

### 7.11 Tier 0 lookup tables are seeded, not generated
All `*_TYPE` / `*_SUBTYPE` / `*_CLASSIFICATION` tables are populated from hardcoded seed dictionaries in `seed_data/`, not randomly generated.

**Authoring process.** Each `seed_data/*.py` module is handwritten by Claude Code in a dedicated Tier 0 session (see `implementation-steps.md` Steps 6–8). The session reads only the distilled references — `references/07_mvp-schema-reference.md` for DDL (columns, types, composite PKs), `references/02_data-mapping-reference.md` Step 3 for constrained code values and literal-match rows, and `references/05_architect-qa.md` for domain-specific Q's. The underlying Excels (`resources/CIF_FSDM_Mapping_MASTER.xlsx`, `resources/iDM_MDM_tables_DDLs.xlsx`) are NOT re-read per session — the references already distil them with architect Q&A resolutions applied. If the distilled refs have a gap (a code appears in `02` without a complete enumeration, or `07` has a column whose legal values are unclear), the session escalates via Handoff Protocol §2 in `implementation-steps.md` rather than silently improvising.

Critical seed rows that Layer 2 rules match literally:
- `AGREEMENT_STATUS_TYPE`: must include `{Scheme='Frozen Status', Code='FROZEN', Desc='Frozen'}` — triggers `Frozen_Ind = '1'`
- `AGREEMENT_FEATURE_ROLE_TYPE`: must include `'primary'`, `'fee'`, `'rate'`, `'term'`
- `FEATURE`: must include a row with `Feature_Subtype_Cd = 'Rate Feature'` and one with `Feature_Classification_Cd = 'Original Loan Term'`
- `ANALYTICAL_MODEL`: must include `Model_Type_Cd = 'profitability'` and `Model_Purpose_Cd = 'customer profitability'`

---

## 8. Out of Scope

| Item | Reason |
|------|--------|
| **Layer 2 — APBB Building Block tables** | WP3 transformation rules generate these from Layer 1; not a source layer |
| **Layer 2 — DIM / FACT tables** | Same — output of WP3, not input |
| **CIF End Data Products (WP7–9)** | CUSTOMER_CLV, CUSTOMER_PROFILE, etc. are Layer 3+ outputs |
| **Feature Store (EFS)** | Derived from FSAS; out of scope per `05_architect-qa.md` |
| **Vector Store (WP6)** | Empty in workbook; not defined |
| **AML / Watch list tables** | WATCH_LIST, WATCH_LIST_SOURCE, WATCH_LIST_MEMBER, PARTY_RISK_GRADE, PARTY_GROUP_RISK_GRADE — no DDL exists in any source file |
| **GEOSPATIAL table** | ST_Geometry column has no CSV representation |
| **OPPORTUNITY / PROPOSAL / APPLICATION tables** | Not in DDL set provided; referenced in WP2 but no schema defined |
| **MULTIMEDIA_OBJECT / MULTIMEDIA_OBJECT_LOCATOR / EVENT_MULTIMEDIA_OBJECT / EVENT_LOCATOR** | Parent MULTIMEDIA_OBJECT DDL not defined; all four tables skipped |
| **PARTY_SOLICITATION_PREFERENCE** | Superseded by custom PARTY_CONTACT_PREFERENCE; generate the custom table only |
| **Real-time / streaming output** | Batch CSV only |
| **Teradata load scripts** | Out of scope; CSVs are the deliverable |
| **Data masking / privacy controls** | Synthetic data only; no real PII |

---

## 9. Open Questions

| # | Question | Impact | Status |
|---|----------|--------|--------|
| 1 | **INDIVIDUAL_MEDICAL population density** — Should medical records be sparse or fully populated? | Affects INDIVIDUAL_MEDICAL row count | **Resolved:** Populate all three tables (INDIVIDUAL_MEDICAL, INDIVIDUAL_SKILL, INDIVIDUAL_SPECIAL_NEED) for all applicable individuals. All tables present in `07_mvp-schema-reference.md` must be populated. |
| 2 | **INDIVIDUAL_SKILL / INDIVIDUAL_SPECIAL_NEED** — Should they be populated at all in MVP? | CSV presence only | **Resolved:** Populate per Q1 resolution above. No sparse/optional treatment. |
| 3 | **PARTY_CLAIM standalone vs. event-linked** — Should claims be linked to COMPLAINT_EVENT records via Source_Event_Id pattern, or fully standalone? | FK design for complaint-to-claim traceability | No FK between PARTY_CLAIM and EVENT in the DDL; treat as standalone unless architect specifies otherwise |
| 4 | **MULTIMEDIA_OBJECT_LOCATOR parent FK** — Should MULTIMEDIA_OBJECT_LOCATOR be generated with orphaned FKs, or skipped? | Missing parent table | **Resolved:** Skip. Table, EVENT_MULTIMEDIA_OBJECT, and EVENT_LOCATOR all moved to Section 8 Out of Scope. Parent MULTIMEDIA_OBJECT DDL not defined. |

---

## 10. Ground Truth Priority

When any specification conflict arises during implementation:

1. `references/02_data-mapping-reference.md` (+ `resources/CIF_FSDM_Mapping_MASTER.xlsx` for clarification) — **do not change values from this**
2. `references/01_schema-reference.md` and `references/07_mvp-schema-reference.md` and `references/05_architect-qa.md` — primary supporting references. `07_mvp-schema-reference.md` takes precedence over `01_schema-reference.md` for MVP scope questions (which tables are in scope, column definitions for in-scope tables) as it is the filtered and finalised DDL-derived set.
3. `references/06_supporting-enrichments.md` — incorporate only where it does not contradict priority 1
4. `mvp-tool-design.md` — implementation decisions derived from the above; update if a conflict is found at the source level

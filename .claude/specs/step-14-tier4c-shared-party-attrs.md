# Spec: Step 14 — Tier 4c Shared Party Attributes

## Overview

This step builds **Tier 4c — Shared Party Attributes**, the 10 attribute tables that hang off **every** `CustomerProfile` (both INDIVIDUAL and ORGANIZATION where applicable) and deliver four of the 22 Layer 2 transformation-readiness constraints at once: **#4** (`PARTY_LANGUAGE_USAGE` must contain both `'primary spoken language'` and `'primary written language'` rows per party — drives `INDIVIDUAL_BB.Language_Cd` / `Language_Written_Cd`), **#5** (`PARTY_STATUS` must have ≥1 record per party — Layer 2 selects `max(Party_Status_Dt)`), **#18** (`PARTY_SCORE` must carry a `Model_Purpose_Cd='customer profitability'` row per party — drives `INDIVIDUAL_BB.Customer_Profitability_Score_Val`), and **#22** (`PARTY_IDENTIFICATION` must carry SSN + Driver's License + Passport type rows per individual — drives the INDIVIDUAL_IDENTIFICATION_PIVOT_BB). The tables are: `PARTY_LANGUAGE_USAGE`, `PARTY_STATUS`, `PARTY_SCORE`, `PARTY_CREDIT_REPORT_SCORE`, `PARTY_IDENTIFICATION`, `PARTY_DEMOGRAPHIC`, `DEMOGRAPHIC_VALUE`, `PARTY_SEGMENT` (Core_DB variant), `PARTY_SPECIALTY`, `PARTY_CONTACT_PREFERENCE` (customized extension). `MARKET_SEGMENT` is **not** produced here — Step 10 Tier 2 already emits it and this step's `PARTY_SEGMENT` rows FK into those Market_Segment_Ids. `DEMOGRAPHIC_VALUE` is a lookup-type table whose rows this step seeds inline (3 demographic codes × 3–5 values each = ~12 rows total); every `PARTY_DEMOGRAPHIC` row then FKs to one of these via the composite key (`Demographic_Cd`, `Demographic_Value_Cd`). All values are either pure projections of `CustomerProfile` fields or deterministic modulo picks on `cp.party_id` — no Faker, no `ctx.rng`. Churn handling: the CHURNED cohort (~5% of customers) gets a historical `ACTIVE` row plus a current `CHURNED` row in `PARTY_STATUS`; BANKRUPT (1.1% per `references/06_supporting-enrichments.md` Part C9) is a deterministic slice of non-churned individuals. Organizations are covered for the cross-cutting tables (`PARTY_LANGUAGE_USAGE`, `PARTY_STATUS`, `PARTY_SCORE`, `PARTY_SEGMENT`, `PARTY_CONTACT_PREFERENCE`) and excluded from individual-only tables (`PARTY_CREDIT_REPORT_SCORE`, `PARTY_IDENTIFICATION`, `PARTY_DEMOGRAPHIC`); `PARTY_SPECIALTY` is emitted as a small deterministic subset (not required by any Layer 2 rule — one row per ~10th party). Step 14 is the third of three parallel children of Step 11 (12/13/14 — Tier 4a / 4b / 4c); it writes 10 Core_DB tables disjoint from the 12 Tier 4a tables (Step 12) and 5 Tier 4b tables (Step 13), so the three run in any order. See `mvp-tool-design.md` §9 Tier 4 ("Party Attributes" critical constraints list) and `references/02_data-mapping-reference.md` Step 3 items #4, #5, #17, #18, #22 for the authoritative constraints.

## Depends on

- **Step 1** — consumes from `config/settings.py`: `SIM_DATE` (upper bound for all `*_Start_Dt` fields and anchor for Layer 2 `max(Party_Status_Dt)` recency filter), `HIGH_DATE` / `HIGH_TS` (stamped via `BaseGenerator.stamp_di()`; also used explicitly as `Valid_From_Dt`/end-date literals in CHURNED cohort handling), `HISTORY_START` (`2025-10-01` — used as the CHURNED-cohort status transition date). Consumes from `config/code_values.py`: `LANGUAGE_USAGE_TYPES = ('primary spoken language', 'primary written language')`, `CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD = 'customer profitability'`. No `SEED` needed — this step is deterministic (no Faker, no `ctx.rng`).
- **Step 2** — consumes `generators/base.BaseGenerator` (`stamp_di()` only — Tier 4c is all Core_DB, so `stamp_valid()` is **never called**). No new utility modules.
- **Step 3** — consumes `registry/profiles.CustomerProfile` fields: `party_id`, `party_type`, `age`, `income_quartile`, `lifecycle_cohort` (`ACTIVE`/`DECLINING`/`CHURNED`/`NEW`), `clv_segment` (1–10), `fico_score` (0 for orgs), `has_internet`, `preferred_channel_cd` (1=BRANCH, 3=ONLINE, 4=MOBILE), `num_dependents`, `ethnicity_type_cd`, `party_since`. `registry/context.GenerationContext` is consumed positionally; this step returns a `Dict[str, pd.DataFrame]` rather than mutating `ctx.tables`.
- **Step 4** — consumes the built universe. Critical invariants this step relies on and must re-verify in guards:
  - Every `CustomerProfile.lifecycle_cohort ∈ {'ACTIVE','DECLINING','CHURNED','NEW'}`, `cp.party_since ≤ SIM_DATE`, `cp.clv_segment ∈ [1..10]`, `cp.income_quartile ∈ [1..4]`, `cp.preferred_channel_cd ∈ {1, 3, 4}` (SMALLINT per profile docstring).
  - For INDIVIDUALs: `cp.fico_score ∈ [300, 850]`, `cp.ethnicity_type_cd` non-None. For ORGANIZATIONs: `cp.fico_score == 0`, `cp.ethnicity_type_cd is None` — this step filters individuals out of org-only and org out of individual-only tables by `cp.party_type`.
  - CHURNED cohort must have `cp.party_since ≤ HISTORY_START` (Step 4 places CHURNED opens up to 2025-06-30); this step uses `HISTORY_START` as the `ACTIVE → CHURNED` transition date.
- **Step 8** — consumes already-stamped Tier 0 lookup tables (FK resolution). Required FK targets (all must exist in `ctx.tables` before this step runs — verify in fail-fast guard):
  - `Core_DB.LANGUAGE_TYPE` — `PARTY_LANGUAGE_USAGE.Language_Type_Cd` FKs here. Seeded ISO codes include `'EN', 'ES', 'FR', 'ZH', 'VI', 'KO', 'HI', 'DE'` etc. (per `seed_data/party_types.py` LANGUAGE_TYPE section).
  - `Core_DB.SPECIALTY_TYPE` — `PARTY_SPECIALTY.Specialty_Type_Cd` FKs here. Seeded in `seed_data/party_types.py`.
  - `Core_DB.DATA_SOURCE_TYPE` — `PARTY_DEMOGRAPHIC.Data_Source_Type_Cd` (NOT NULL) FKs here. Seeded codes include `'CORE_BANKING'`, `'CARD_SYSTEM'`, `'MDM'` etc. (reused from Tier 4a).
- **Step 10** — consumes `ctx.tables['Core_DB.ANALYTICAL_MODEL']` (for `PARTY_SCORE.Model_Id` FK — must include at least one row with `Model_Purpose_Cd = 'customer profitability'`) and `ctx.tables['Core_DB.MARKET_SEGMENT']` (for `PARTY_SEGMENT.Market_Segment_Id` FK — Step 10 emits one row per CLV-decile segment). Reading these at the top of `generate()` via `ctx.tables['Core_DB.ANALYTICAL_MODEL']` / `ctx.tables['Core_DB.MARKET_SEGMENT']`:
  - From `ANALYTICAL_MODEL`: select the row where `Model_Purpose_Cd == 'customer profitability'`; take its `Model_Id` and `Model_Run_Id`. Used for **all** `PARTY_SCORE` rows (one per party). Fail-fast if no such row exists.
  - From `MARKET_SEGMENT`: build `clv_to_segment_id: Dict[int, int]` — mapping `cp.clv_segment` (1–10 decile) to a Market_Segment_Id. Step 10's MARKET_SEGMENT carries one row per CLV decile per Market_Segment_Scheme_Id; pick the CLV scheme's segment per decile.
- **Step 11** — consumes `ctx.tables['Core_DB.ORGANIZATION']` only for the placeholder-row invariant check (does not project org attrs — that is Step 13). Actual org customers iterate from `ctx.customers` filtered by `party_type == 'ORGANIZATION'`. Does not read `INDIVIDUAL` or `BUSINESS` DataFrames — Tier 4c is a projection of `ctx.customers`, not of Step 11's DataFrames.

No other dependencies. Does **not** read `ctx.tables` from Steps 12/13 — Tier 4a/4b/4c are parallel siblings on disjoint tables. Does **not** FK to any Tier 4a or Tier 4b output.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 14):
- `PRD.md` §4.2 ("Party shared" sub-list enumerates all Tier 4c tables — verify scope matches; note `PARTY_SEGMENT†` annotation meaning Core_DB-only here while CDM_DB.PARTY_SEGMENT is Step 22), §4.3 (CHAR(1) = Y/N, CHAR(3) = Yes/No — applies to `PARTY_IDENTIFICATION.Party_Identification_Primary_Ind` CHAR(3)), §7.1 (BIGINT rule — every `*_Id` column in every Tier 4c table), §7.2 (shared party ID space), §7.3 (DI column rules — Core_DB gets `di_*` only), §7.4 (active-record convention — `*_End_Dt = NULL` for Core_DB active rows; CHURNED `PARTY_STATUS` requires one historical row with actual `End_Dt`), §7.6 (reproducibility — modulo indexing on `party_id` gives byte-identical reruns), §7.11 (Tier 0 seeding — `DEMOGRAPHIC_VALUE` is **not** a Tier 0 table despite being a lookup in shape; it is seeded inline in this step because it's a shallow 12-row table with no other consumers until Layer 2).
- `mvp-tool-design.md` §9 Tier 4 — authoritative per-table constraints:
  - `PARTY_LANGUAGE_USAGE`: every party gets **2** rows with `Language_Usage_Type_Cd ∈ {'primary spoken language', 'primary written language'}`.
  - `PARTY_STATUS`: ≥1 per party; Layer 2 filter `WHERE Party_Status_Dt = max(Party_Status_Dt)`. Default `'ACTIVE'` for non-churned, `'BANKRUPT'` for 1.1% (SCF — `references/06_supporting-enrichments.md` C9).
  - `PARTY_CREDIT_REPORT_SCORE`: `Credit_Report_Score_Num` is a VARCHAR(50) stringified FICO `"300"..."850"`.
  - `PARTY_SCORE`: one row per party with `Model_Purpose_Cd = 'customer profitability'`; `Party_Score_Val` as VARCHAR(100) probability string `"0.xxxx"`.
  - `PARTY_CONTACT_PREFERENCE` (customized): SMALLINT codes. `Channel_Type_Cd` = 3 (ONLINE) for `has_internet=True`, 1 (BRANCH) otherwise. `Contact_Preference_Type_Cd` 1=Sales, 2=Service — **two rows per party**. `Protocol_Type_Cd`, `Days_Cd`, `Hours_Cd` defaults all = 1.
  - `DEMOGRAPHIC_VALUE`: seed lookup rows first, then `PARTY_DEMOGRAPHIC` references them. No standalone `DEMOGRAPHIC` parent table.
  - §10 rule 6 ("`has_internet = False` → `preferred_channel_cd = 1` (BRANCH); no ONLINE/MOBILE contact preferences") — confirms the Step 4 invariant this step projects.
  - §12 Layer 2 constraints **#4** (`PARTY_LANGUAGE_USAGE` two-row rule), **#5** (`PARTY_STATUS` ≥1 per party), **#17** (`PARTY_SCORE` profitability — §12 item #17 is actually AGREEMENT_SCORE; the PARTY_SCORE variant is **#18** in the list), **#18** (`PARTY_SCORE` customer-profitability), **#22** (`PARTY_IDENTIFICATION` type rows per individual — SSN, Passport, Driver's License minimum).
- `implementation-steps.md` Step 14 entry (Produces, Reads from, Exit criteria, Scope=M); Handoff Protocol (post-session notes rules); Seed Data Authoring Convention (partially applies — `DEMOGRAPHIC_VALUE` is a shallow lookup seeded inline, not via `seed_data/*.py`; document the deviation).

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/02_data-mapping-reference.md` — read **Step 3 items #4, #5, #17, #18, #22** **only**. (Note: implementation-steps.md Step 14 "Reads from" lists items #4, #5, #17, #22 — item #17 is AGREEMENT_SCORE which is Tier 7, not Tier 4c; Layer 2 rule #18 is the PARTY_SCORE rule that this step actually delivers. Treat #17 as a hint to also look at #18 which is the true relevant rule.) Also skim the "Which columns must not be null?" table (around line 850) for `PARTY_LANGUAGE_USAGE`, `PARTY_STATUS`, and the "Which code/lookup values must exist in Layer 1?" table (line 874) for `Contact Preference Type Cd` SMALLINT 1=Sales/2=Service mapping (line 887). All other Step-3 items are consumed by other steps.
- `references/06_supporting-enrichments.md` — read **Part C9** "Debt-to-Income and Delinquency Rates" **only** (around line 269). Authoritative source for the **1.1% BANKRUPT rate** applied to `PARTY_STATUS.Party_Status_Cd = 'BANKRUPT'` and the 11.2% / 4.6% delinquency rates (the delinquency rates are consumed by Step 4 universe build into `AgreementProfile.is_delinquent` / `is_severely_delinquent`; this step does not re-sample them — those flags drive Tier 7, not Tier 4c). Do NOT re-read Parts A–B or D–K — distributions were finalised in Step 4 and are already baked into `cp` fields.
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the 10 Tier 4c tables. Open only these DDL blocks (line numbers approximate):
  - `#### PARTY_LANGUAGE_USAGE` (near line 7167). 6 business columns + 3-col DI tail in DDL; `stamp_di()` appends the canonical 5-col tail. `Party_Id`, `Language_Type_Cd`, `Language_Usage_Type_Cd`, `Party_Language_Start_Dttm` NOT NULL. `Party_Language_End_Dttm`, `Party_Language_Priority_Num` nullable.
  - `#### PARTY_STATUS` (near line 3743). 3 business columns + 3-col DI tail. All 3 business columns NOT NULL (`Party_Id`, `Party_Status_Cd`, `Party_Status_Dt`).
  - `#### PARTY_SCORE` (near line 5428). 4 business columns + 3-col DI tail. `Party_Id`, `Model_Id`, `Model_Run_Id` NOT NULL. `Party_Score_Val` VARCHAR(100) nullable.
  - `#### PARTY_CREDIT_REPORT_SCORE` (near line 5494). 5 business columns + 3-col DI tail. `Reporting_Party_Id`, `Obligor_Party_Id`, `Credit_Report_Dttm`, `Score_Type_Cd` NOT NULL. `Credit_Report_Score_Num` VARCHAR(50) nullable (always populated in this step).
  - `#### PARTY_IDENTIFICATION` (near line 7130). 9 business columns + 3-col DI tail. `Party_Id`, `Issuing_Party_Id`, `Party_Identification_Type_Cd`, `Party_Identification_Start_Dttm` NOT NULL. `Party_Identification_Primary_Ind` is **CHAR(3)** — use `'Yes'`/`'No'`.
  - `#### PARTY_DEMOGRAPHICS` (renders as `#### PARTY_DEMOGRAPHIC` — near line 8090). 8 business columns + 3-col DI tail. `Party_Id`, `Demographic_Cd`, `Data_Source_Type_Cd`, `Party_Demographic_Start_Dt`, `Demographic_Value_Cd` NOT NULL.
  - `#### DEMOGRAPHICS_VALUE` (renders as `#### DEMOGRAPHIC_VALUE` — near line 8183). 6 business columns + 3-col DI tail. `Demographic_Cd`, `Demographic_Value_Cd` NOT NULL (composite PK). `Demographic_Range_Start_Val`, `Demographic_Range_End_Val`, `Demographic_Value_Desc`, `Demographic_Val` nullable.
  - `#### PARTY_SEGMENT (Core_DB)` (near line 3767). 4 business columns + 3-col DI tail. `Party_Id`, `Market_Segment_Id` NOT NULL. `Party_Segment_Start_Dttm`, `Party_Segment_End_Dttm` nullable.
  - `#### PARTY_SPECIALTY` (near line 6866). 4 business columns + 3-col DI tail. `Party_Id`, `Specialty_Type_Cd`, `Party_Specialty_Start_Dt` NOT NULL. `Party_Specialty_End_Dt` nullable.
  - `PARTY_CONTACT_PREFERENCE` is **not in `07_mvp-schema-reference.md`** — the DDL lives in `resources/Core_DB_customized.sql` (lines 1–21). 9 business columns + 5-col DI tail. `Party_Id`, `Channel_Type_Cd`, `Contact_Preference_Type_Cd`, `Party_Contact_Preference_Start_Dt`, `Party_Contact_Preference_End_Dt`, `Protocol_Type_Cd`, `Days_Cd`, `Hours_Cd` NOT NULL. `Party_Contact_Preference_Priority_Num` INTEGER nullable. Note: DDL has `Party_Contact_Preference_End_Dt DATE NOT NULL` — use `HIGH_DATE = '9999-12-31'` for active rows (sentinel, not NULL).

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is the MVP-filtered authoritative DDL set per PRD §10. Exception: if `07` has an ambiguity around `PARTY_CONTACT_PREFERENCE` SMALLINT code enumerations, consult `01_schema-reference.md` "SMALLINT Code Enumerations" section (referenced by `02` line 887). This is a narrow lookup, not a full read.
- `references/02_data-mapping-reference.md` beyond Step 3 #4/#5/#17/#18/#22 and the NULL / code-lookup tables — the rest of Step 3 is covered by other tiers.
- `references/05_architect-qa.md` — no Q directly touches any Tier 4c table. (Q1/Q2 are INTEGER/BIGINT ID rules — already baked into this spec; Q3 is PRODUCT_GROUP; Q4/Q5 are customized; Q6 is CDM ADDRESS; Q7 is INDIVIDUAL_PAY_TIMING (Tier 4a); Q8 is industry codes (Tier 4b).)
- `references/06_supporting-enrichments.md` beyond Part C9 — Parts A/B/D/F/G apply to Step 4; Parts C1–C8, E, H–K apply to Tier 7/10/11.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `resources/iDM_MDM_tables_DDLs.xlsx` — distilled into `07`. Exception: `resources/Core_DB_customized.sql` must be opened to read the `PARTY_CONTACT_PREFERENCE` DDL block (lines 1–21 only). Do not read the rest of that file.
- CDM_DB and PIM_DB DDL blocks — Step 22 / Step 23, not touched here.
- Other generators' code — `generators/tier3_party_subtypes.py` (Step 11) is worth a glance for the module-level-constant / `_COLS_*` / guard pattern. `generators/tier4a_individual.py` (Step 12) and `generators/tier4b_organization.py` (Step 13) are parallel siblings — their internals are not required, but a quick scan of their module structure / constant layout / DataFrame-construction pattern is useful for stylistic consistency.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier4c_shared.py` — `class Tier4cShared(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]` method returning 10 Core_DB DataFrames. Implementation contract:
  1. **Imports** — `from __future__ import annotations`; stdlib `datetime` (`date`, `datetime`, `time`, `timedelta`); third-party `pandas as pd`; project imports `from config.settings import HIGH_DATE, HIGH_TS, HISTORY_START, SIM_DATE`; `from config.code_values import LANGUAGE_USAGE_TYPES, CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD`; `from generators.base import BaseGenerator`; `from typing import TYPE_CHECKING, Dict, List, Tuple`; `if TYPE_CHECKING: from registry.context import GenerationContext`.
  2. **Module-level constants** — use ALL-CAPS names prefixed `_` for module-private:
     - `_TIER4C_DI_START_TS = '2000-01-01 00:00:00.000000'` — fixed timestamp mirrors Tier 0/1/2/3/4a/4b convention for byte-identical reruns.
     - `_LANGUAGE_USAGE_TYPES = LANGUAGE_USAGE_TYPES` — imported for clarity; `('primary spoken language', 'primary written language')`.
     - `_CHURNED_TRANSITION_DT = HISTORY_START` — date(2025, 10, 1), the `ACTIVE → CHURNED` transition date per Step 4's CHURNED cohort rule.
     - `_BANKRUPT_MOD = 90` — `cp.party_id % 90 == 0 AND lifecycle_cohort != 'CHURNED'` picks BANKRUPT subset (~1.1% of 3000 = ~33 parties; modulo 90 yields ~33 hits at seed=42, within the target band).
     - `_SPECIALTY_MOD = 10` — `cp.party_id % 10 == 0` picks PARTY_SPECIALTY subset (~300 rows out of 3000 customers; MVP-minimal volume; no Layer 2 constraint on PARTY_SPECIALTY).
     - `_ID_TYPES_INDIVIDUAL: Tuple[str, ...] = ('SSN', "Driver's License", 'Passport')` — the 3 types per individual, per `mvp-tool-design.md` §12 #22. Emit in this order for every individual; apostrophe in `Driver's License` is literal.
     - `_PROFILE_LANG_BY_ETHNICITY: Dict[str, str]` — `{'HISPANIC': 'ES', 'ASIAN': 'ZH'}`; fallback `'EN'` for `WHITE`/`BLACK`/`OTHER`/None. Used for BOTH `'primary spoken language'` AND `'primary written language'` rows — MVP simplification.
     - `_CONTACT_PREF_CHANNEL_BY_INTERNET: Dict[bool, int]` — `{True: 3, False: 1}` (SMALLINT: 3=ONLINE, 1=BRANCH). Per `mvp-tool-design.md` §10 rule 6.
     - `_CONTACT_PREF_TYPES: Tuple[int, ...] = (1, 2)` — SMALLINT (1=Sales, 2=Service); emit both rows per party. (`references/02_data-mapping-reference.md` line 887 / 1030.)
     - `_DEMOGRAPHIC_CODES` — 3 codes with their value-cd enumerations, seeded into DEMOGRAPHIC_VALUE:
       - `'AGE_BAND'`: values `'UNDER_35'` (range 18–34), `'35_44'`, `'45_54'`, `'55_64'`, `'65_PLUS'`
       - `'INCOME_QUARTILE'`: values `'Q1'`, `'Q2'`, `'Q3'`, `'Q4'`
       - `'DEPENDENTS'`: values `'NONE'` (0), `'ONE_TO_TWO'` (1–2), `'THREE_PLUS'` (3+)
     Total ~12 DEMOGRAPHIC_VALUE rows.
     - `_SCORE_TYPE_CD_FICO = 'FICO'` — NOT NULL value for `PARTY_CREDIT_REPORT_SCORE.Score_Type_Cd`.
     - `_CREDIT_BUREAU_REPORTING_PARTY_ID = 9_999_999` — reuse the same reserved BIGINT used as `BANK_PARTY_ID` / `SELF_EMP_ORG_ID`. It stands in as the credit bureau reporting entity (no separate row required — `PARTY_CREDIT_REPORT_SCORE.Reporting_Party_Id` is NOT NULL but is a soft FK that Layer 2 does not join-filter). Document this reuse in a 1-line module comment above the constant.
     - `_ISSUING_PARTY_ID = 9_999_999` — reused for `PARTY_IDENTIFICATION.Issuing_Party_Id` for the same reason. Document the reuse.
     - `_REQUIRED_TIER0_TABLES: Tuple[str, ...] = ('Core_DB.LANGUAGE_TYPE', 'Core_DB.SPECIALTY_TYPE', 'Core_DB.DATA_SOURCE_TYPE')`.
     - `_REQUIRED_TIER2_TABLES: Tuple[str, ...] = ('Core_DB.ANALYTICAL_MODEL', 'Core_DB.MARKET_SEGMENT')`.
     - 10 column-order lists `_COLS_PARTY_LANGUAGE_USAGE`, `_COLS_PARTY_STATUS`, `_COLS_PARTY_SCORE`, `_COLS_PARTY_CREDIT_REPORT_SCORE`, `_COLS_PARTY_IDENTIFICATION`, `_COLS_PARTY_DEMOGRAPHIC`, `_COLS_DEMOGRAPHIC_VALUE`, `_COLS_PARTY_SEGMENT`, `_COLS_PARTY_SPECIALTY`, `_COLS_PARTY_CONTACT_PREFERENCE` — each matching the DDL business-column order verbatim. Exact canonical orders:
       - `_COLS_PARTY_LANGUAGE_USAGE = ['Party_Id','Language_Type_Cd','Language_Usage_Type_Cd','Party_Language_Start_Dttm','Party_Language_End_Dttm','Party_Language_Priority_Num']`
       - `_COLS_PARTY_STATUS = ['Party_Id','Party_Status_Cd','Party_Status_Dt']`
       - `_COLS_PARTY_SCORE = ['Party_Id','Model_Id','Model_Run_Id','Party_Score_Val']`
       - `_COLS_PARTY_CREDIT_REPORT_SCORE = ['Reporting_Party_Id','Obligor_Party_Id','Credit_Report_Dttm','Score_Type_Cd','Credit_Report_Score_Num']`
       - `_COLS_PARTY_IDENTIFICATION = ['Party_Id','Issuing_Party_Id','Party_Identification_Type_Cd','Party_Identification_Start_Dttm','Party_Identification_End_Dttm','Party_Identification_Num','Party_Identification_Receipt_Dt','Party_Identification_Primary_Ind','Party_Identification_Name']`
       - `_COLS_PARTY_DEMOGRAPHIC = ['Party_Id','Demographic_Cd','Data_Source_Type_Cd','Party_Demographic_Start_Dt','Demographic_Value_Cd','Party_Demographic_End_Dt','Party_Demographic_Num','Party_Demographic_Val']`
       - `_COLS_DEMOGRAPHIC_VALUE = ['Demographic_Cd','Demographic_Value_Cd','Demographic_Range_Start_Val','Demographic_Range_End_Val','Demographic_Value_Desc','Demographic_Val']`
       - `_COLS_PARTY_SEGMENT = ['Party_Id','Market_Segment_Id','Party_Segment_Start_Dttm','Party_Segment_End_Dttm']`
       - `_COLS_PARTY_SPECIALTY = ['Party_Id','Specialty_Type_Cd','Party_Specialty_Start_Dt','Party_Specialty_End_Dt']`
       - `_COLS_PARTY_CONTACT_PREFERENCE = ['Party_Id','Channel_Type_Cd','Contact_Preference_Type_Cd','Party_Contact_Preference_Start_Dt','Party_Contact_Preference_End_Dt','Party_Contact_Preference_Priority_Num','Protocol_Type_Cd','Days_Cd','Hours_Cd']`
  3. **Guards (first ~20 lines of `generate()`)**:
     - Raise `RuntimeError('Tier4cShared requires a populated ctx.customers — run UniverseBuilder.build() first')` if `not ctx.customers`.
     - Iterate `_REQUIRED_TIER0_TABLES + _REQUIRED_TIER2_TABLES`; for any key missing from `ctx.tables`, raise `RuntimeError(f'Tier4cShared requires {key} to be loaded first')`.
     - Resolve the customer-profitability model row: `am_df = ctx.tables['Core_DB.ANALYTICAL_MODEL']; prof_rows = am_df[am_df['Model_Purpose_Cd'] == CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD]`. Raise `RuntimeError('Tier4cShared requires an ANALYTICAL_MODEL row with Model_Purpose_Cd=customer profitability — Step 10 did not emit it')` if `prof_rows.empty`. Pick `prof_rows.iloc[0]` for Model_Id / Model_Run_Id. Document in a 1-line comment that picking `iloc[0]` is deterministic because Step 10's template order is fixed.
     - Resolve the CLV Market_Segment_Id mapping: read `ctx.tables['Core_DB.MARKET_SEGMENT']`, filter to the CLV scheme, build `clv_to_segment_id: Dict[int, int]` mapping decile 1–10 to `Market_Segment_Id`. Raise `RuntimeError('Tier4cShared requires MARKET_SEGMENT rows for all 10 CLV deciles — Step 10 emitted fewer')` if the mapping is incomplete. If Step 10's MARKET_SEGMENT uses a different segment-granularity (e.g., fewer rows or a different scheme key), use a deterministic fallback: `clv_to_segment_id[decile] = market_segment_df['Market_Segment_Id'].iloc[(decile - 1) % len(market_segment_df)]`. Document the fallback in a 1-line comment.
  4. **Pre-computations**:
     - `cps = ctx.customers` — full list (both types).
     - `ind_cps = [cp for cp in cps if cp.party_type == 'INDIVIDUAL']` — for individual-only tables (PARTY_CREDIT_REPORT_SCORE, PARTY_IDENTIFICATION, PARTY_DEMOGRAPHIC).
     - Helper `def _age_band(age: int) -> str` — returns `'UNDER_35'`/`'35_44'`/`'45_54'`/`'55_64'`/`'65_PLUS'`.
     - Helper `def _dependents_band(n: int) -> str` — returns `'NONE'`/`'ONE_TO_TWO'`/`'THREE_PLUS'`.
  5. **Build 10 DataFrames** — order is free (no intra-tier FK dependency except PARTY_DEMOGRAPHIC → DEMOGRAPHIC_VALUE, which this step populates both sides). For each table:
     - Iterate the appropriate filter of `cps`.
     - Construct dicts with keys in DDL business-column order; append DI via `self.stamp_di(df, start_ts=_TIER4C_DI_START_TS)`.
     - Explicitly cast `*_Id` columns to `Int64` (nullable BIGINT) after construction.
     - Per-table rules (see below).
  6. **Return** a `Dict[str, pd.DataFrame]` keyed `Core_DB.<TABLE>` with all 10 tables. Do not mutate `ctx.tables`.

  **Per-table population rules:**

  | Table | Row source | Key field rules |
  |-------|-----------|-----------------|
  | `PARTY_LANGUAGE_USAGE` | All parties × 2 rows | For each `cp` emit 2 rows: `(Language_Usage_Type_Cd='primary spoken language', Party_Language_Priority_Num='1')` and `(Language_Usage_Type_Cd='primary written language', Party_Language_Priority_Num='2')`. `Language_Type_Cd = _PROFILE_LANG_BY_ETHNICITY.get(cp.ethnicity_type_cd, 'EN')` for individuals, `'EN'` for orgs. `Party_Language_Start_Dttm = datetime.combine(cp.party_since, time(0, 0))`; `Party_Language_End_Dttm = None`. |
  | `PARTY_STATUS` | All parties; CHURNED gets 2 rows, BANKRUPT gets 1 row w/ `'BANKRUPT'`, others get 1 row w/ `'ACTIVE'` | For `cp.lifecycle_cohort == 'CHURNED'`: emit `(Party_Status_Cd='ACTIVE', Party_Status_Dt=cp.party_since)` AND `(Party_Status_Cd='CHURNED', Party_Status_Dt=_CHURNED_TRANSITION_DT)`. For `cp.lifecycle_cohort != 'CHURNED' AND cp.party_id % _BANKRUPT_MOD == 0 AND cp.party_type == 'INDIVIDUAL'`: emit `(Party_Status_Cd='BANKRUPT', Party_Status_Dt=cp.party_since)`. Everyone else: emit `(Party_Status_Cd='ACTIVE', Party_Status_Dt=cp.party_since)`. Each row: `Party_Id=cp.party_id`. |
  | `PARTY_SCORE` | All parties (1 row each) | `Party_Id=cp.party_id`; `Model_Id=prof_model_id`; `Model_Run_Id=prof_model_run_id` (from ANALYTICAL_MODEL lookup); `Party_Score_Val=f'{(cp.party_id % 10000) / 10000:.4f}'` (produces `"0.xxxx"` probability string, deterministic). |
  | `PARTY_CREDIT_REPORT_SCORE` | INDIVIDUAL-type parties only (~2,400 rows) | `Reporting_Party_Id=_CREDIT_BUREAU_REPORTING_PARTY_ID` (9_999_999); `Obligor_Party_Id=cp.party_id`; `Credit_Report_Dttm=datetime.combine(cp.party_since, time(9, 0, 0))`; `Score_Type_Cd=_SCORE_TYPE_CD_FICO`; `Credit_Report_Score_Num=str(cp.fico_score)` (VARCHAR(50) — quote the integer). Organizations excluded (`cp.fico_score == 0` sentinel). |
  | `PARTY_IDENTIFICATION` | INDIVIDUAL-type parties × 3 rows each (~7,200 rows) | For each individual, emit 3 rows in `_ID_TYPES_INDIVIDUAL` order. Each row: `Party_Id=cp.party_id`; `Issuing_Party_Id=_ISSUING_PARTY_ID`; `Party_Identification_Type_Cd ∈ {'SSN',"Driver's License",'Passport'}`; `Party_Identification_Start_Dttm=datetime.combine(cp.party_since, time(0, 0))`; `Party_Identification_End_Dttm=None`; `Party_Identification_Num=f'{type_cd[:3].upper()}-{cp.party_id:09d}'` (opaque VARCHAR(50) token — never a real SSN/passport value); `Party_Identification_Receipt_Dt=cp.party_since`; `Party_Identification_Primary_Ind='Yes'` iff `type_cd=='SSN'` else `'No'` (CHAR(3)); `Party_Identification_Name=type_cd` (human-readable). |
  | `PARTY_DEMOGRAPHIC` | INDIVIDUAL-type parties × 3 rows each (~7,200 rows) — one row per (AGE_BAND, INCOME_QUARTILE, DEPENDENTS) | For each individual, emit 3 rows. Each row: `Party_Id=cp.party_id`; `Demographic_Cd ∈ {'AGE_BAND','INCOME_QUARTILE','DEPENDENTS'}`; `Data_Source_Type_Cd='CORE_BANKING'` (reuse Tier 4a pattern); `Party_Demographic_Start_Dt=cp.party_since`; `Demographic_Value_Cd` = `_age_band(cp.age)` / `f'Q{cp.income_quartile}'` / `_dependents_band(cp.num_dependents)` per row; `Party_Demographic_End_Dt=None`; `Party_Demographic_Num=None`; `Party_Demographic_Val=None` (MVP — values live in DEMOGRAPHIC_VALUE.Demographic_Val on the lookup row; per-party numeric values out of scope). |
  | `DEMOGRAPHIC_VALUE` | Seeded lookup (12 rows total across 3 codes) | Emit all `(Demographic_Cd, Demographic_Value_Cd)` combos per `_DEMOGRAPHIC_CODES`. For ranged values (AGE_BAND, DEPENDENTS): populate `Demographic_Range_Start_Val`/`_End_Val` as VARCHAR stringified ints; for enumerated values (INCOME_QUARTILE): leave range columns NULL. `Demographic_Value_Desc` populated with a human-readable descriptor (e.g., `'Age 35-44'`). `Demographic_Val` = NULL (per-party values live on PARTY_DEMOGRAPHIC). |
  | `PARTY_SEGMENT` (Core_DB) | All parties (1 row each) | `Party_Id=cp.party_id`; `Market_Segment_Id=clv_to_segment_id[cp.clv_segment]`; `Party_Segment_Start_Dttm=datetime.combine(cp.party_since, time(0, 0))`; `Party_Segment_End_Dttm=None`. |
  | `PARTY_SPECIALTY` | Subset (`cp.party_id % _SPECIALTY_MOD == 0`, ~300 rows) | `Party_Id=cp.party_id`; `Specialty_Type_Cd` = deterministic pick from seeded `SPECIALTY_TYPE` pool (use `sorted(ctx.tables['Core_DB.SPECIALTY_TYPE']['Specialty_Type_Cd'])[cp.party_id % len(pool)]`); `Party_Specialty_Start_Dt=cp.party_since`; `Party_Specialty_End_Dt=None`. |
  | `PARTY_CONTACT_PREFERENCE` | All parties × 2 rows (~6,000 rows) | For each `cp`, emit 2 rows (one per `_CONTACT_PREF_TYPES` entry). Each row: `Party_Id=cp.party_id`; `Channel_Type_Cd=_CONTACT_PREF_CHANNEL_BY_INTERNET[cp.has_internet]`; `Contact_Preference_Type_Cd ∈ {1, 2}`; `Party_Contact_Preference_Start_Dt=cp.party_since`; `Party_Contact_Preference_End_Dt=HIGH_DATE` (sentinel — DDL declares NOT NULL); `Party_Contact_Preference_Priority_Num=1` (INTEGER); `Protocol_Type_Cd=1`; `Days_Cd=1`; `Hours_Cd=1` (all SMALLINT defaults). Treat SMALLINT columns as `Int16` / plain int in pandas — no BIGINT cast (they are not `*_Id` columns). |

**Do NOT produce** in this step:
- CSVs — writer is not invoked. `output/` must remain empty.
- New `seed_data/*.py` modules — `DEMOGRAPHIC_VALUE` is seeded inline in the generator (shallow 12-row lookup with no cross-module consumers). All other Tier 0 codes this step FKs to are already seeded.
- New columns in any existing table — `CustomerProfile`, `AgreementProfile`, `AddressRecord`, `GenerationContext`, `IdFactory` are **not modified**.
- `MARKET_SEGMENT` rows — Step 10 Tier 2 already emits this; Tier 4c consumes via FK only.
- `ANALYTICAL_MODEL` rows — Step 10 Tier 2 emits including the `Model_Purpose_Cd='customer profitability'` row this step FKs to.
- Rows in any Tier 4a (Step 12) or Tier 4b (Step 13) tables.
- CDM_DB (`CDM_DB.PARTY_SEGMENT`) / PIM_DB rows — Steps 22 and 23.
- Any modification to `config/*`, `utils/*`, `registry/*`, `output/*`, `main.py`, `generators/base.py`, or any existing `generators/tier*.py`.
- Any modification to documents (`PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/*`, `CLAUDE.md`, `resources/*`).
- Any modification to existing `seed_data/*.py` modules.
- Any top-level module-level side effect (DataFrame construction, pool building, I/O, date computation).

## Tables generated (if applicable)

After `Tier4cShared.generate(ctx)` runs, the returned dict has 10 `Core_DB.*` keys.

Row-count expectations assume the Step 4 universe at seed=42: ~3,000 customers total (~2,400 INDIVIDUAL + ~600 ORGANIZATION), of which ~5% CHURNED (~150), ~1.1% of non-churned individuals BANKRUPT (~25–35 via modulo 90).

| Table | Approx rows | Key FK dependencies | Required literal-match / constraint rows |
|-------|-------------|---------------------|-----------------------------------------|
| `Core_DB.PARTY_LANGUAGE_USAGE` | ~6,000 (2 × 3,000) | `Core_DB.LANGUAGE_TYPE.Language_Type_Cd` | Layer 2 #4: per party, both `Language_Usage_Type_Cd='primary spoken language'` AND `'primary written language'` |
| `Core_DB.PARTY_STATUS` | ~3,150 (3,000 parties, +~150 extra ACTIVE history rows for CHURNED cohort) | — | Layer 2 #5: ≥1 row per party. CHURNED cohort has 2 rows (ACTIVE history + CHURNED current). BANKRUPT subset (~30 rows) has single `'BANKRUPT'` row. |
| `Core_DB.PARTY_SCORE` | ~3,000 | `Core_DB.ANALYTICAL_MODEL.Model_Id` (where `Model_Purpose_Cd='customer profitability'`) | Layer 2 #18: one row per party with the customer-profitability Model_Id |
| `Core_DB.PARTY_CREDIT_REPORT_SCORE` | ~2,400 (individuals only) | — (soft FK to `PARTY`; Reporting_Party_Id = 9_999_999 reserved) | `Score_Type_Cd='FICO'`; `Credit_Report_Score_Num` VARCHAR stringified FICO 300–850 |
| `Core_DB.PARTY_IDENTIFICATION` | ~7,200 (3 × individuals) | — (soft FK; Issuing_Party_Id = 9_999_999 reserved) | Layer 2 #22: per individual, rows for `'SSN'`, `"Driver's License"`, `'Passport'`. `Primary_Ind='Yes'` only on SSN row. |
| `Core_DB.PARTY_DEMOGRAPHIC` | ~7,200 (3 × individuals) | `Core_DB.DATA_SOURCE_TYPE.Data_Source_Type_Cd`; `Core_DB.DEMOGRAPHIC_VALUE` (composite `Demographic_Cd`, `Demographic_Value_Cd`) | 3 rows per individual (AGE_BAND, INCOME_QUARTILE, DEPENDENTS) |
| `Core_DB.DEMOGRAPHIC_VALUE` | ~12 (3 codes × 3–5 values each) | — | Composite PK (`Demographic_Cd`, `Demographic_Value_Cd`); lookup populated BEFORE PARTY_DEMOGRAPHIC FK references resolve |
| `Core_DB.PARTY_SEGMENT` | ~3,000 | `Core_DB.MARKET_SEGMENT.Market_Segment_Id` | One row per party mapping `clv_segment` decile to Market_Segment_Id |
| `Core_DB.PARTY_SPECIALTY` | ~300 (every 10th party) | `Core_DB.SPECIALTY_TYPE.Specialty_Type_Cd` | Optional / non-critical (no Layer 2 constraint) |
| `Core_DB.PARTY_CONTACT_PREFERENCE` | ~6,000 (2 × 3,000) | `Core_DB.CHANNEL_TYPE` (soft — SMALLINT 1=BRANCH/3=ONLINE/4=MOBILE per `resources/Core_DB_customized.sql`) | 2 rows per party (Sales=1, Service=2). Channel depends on `has_internet`. |

All 10 DataFrames have the full 5-column DI tail in `DI_COLUMN_ORDER` as the last 5 columns after `stamp_di()`, with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`.

Layer 2 literal-match seed rows this step introduces: **none that are FK-referenced by other tiers**. The `'primary spoken language'` / `'primary written language'` / `'customer of enterprise'` / `'customer profitability'` literals are row *values*, not seeded lookup rows. `DEMOGRAPHIC_VALUE` is a lookup-shape table seeded inline with 3 demographic codes and ~12 value rows; every PARTY_DEMOGRAPHIC row FKs to it via the composite `(Demographic_Cd, Demographic_Value_Cd)` key.

## Files to modify

No files modified. All `config/*`, `utils/*`, `registry/*`, `output/*`, `main.py`, `CLAUDE.md`, all documents under `references/` and the project root, all `seed_data/*.py`, all existing `generators/*.py` (base, tier0_lookups, tier1_geography, tier2_core, tier3_party_subtypes, tier4a_individual, tier4b_organization) are NOT touched.

If the implementation session finds that `references/07_mvp-schema-reference.md` or `resources/Core_DB_customized.sql` disagrees with this spec on a column name, type, or nullability for any Tier 4c table, escalate per Handoff Protocol §2 — update the upstream reference or add a `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new entries in `requirements.txt`. All imports are stdlib or already-required (pandas).

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — `Party_Id`, `Reporting_Party_Id`, `Obligor_Party_Id`, `Issuing_Party_Id`, `Model_Id`, `Model_Run_Id`, `Market_Segment_Id` are declared `INTEGER` or `BIGINT` in the DDL. This step emits `pd.Int64Dtype()` ("Int64" — nullable BIGINT) for ALL of them. Cast explicitly via `df[col] = df[col].astype('Int64')` after construction to avoid numpy `int64` / `float64` drift. **Exception:** SMALLINT columns (`Channel_Type_Cd`, `Contact_Preference_Type_Cd`, `Protocol_Type_Cd`, `Days_Cd`, `Hours_Cd` on PARTY_CONTACT_PREFERENCE) are NOT `*_Id` columns and do not fall under the BIGINT rule — keep them as native Python `int` or cast to `Int16`.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — every `Party_Id` / `Obligor_Party_Id` in this step equals a `CustomerProfile.party_id` from Step 4. No ID minting — never call `ctx.ids.next(...)`. `Reporting_Party_Id` and `Issuing_Party_Id` reuse the reserved `9_999_999` constant (same pattern as `BANK_PARTY_ID` / `SELF_EMP_ORG_ID`).
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on all 10 DataFrames. Construct each via `pd.DataFrame(rows, columns=_COLS_*)` with business columns only, then `self.stamp_di(df, start_ts=_TIER4C_DI_START_TS)` appends the 5 DI columns. Fixed `_TIER4C_DI_START_TS = '2000-01-01 00:00:00.000000'` guarantees byte-identical reruns.
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts` stamped via `stamp_di()` default. `Valid_To_Dt` n/a: Tier 4c is all Core_DB.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — n/a: Tier 4c is all Core_DB. Do NOT call `stamp_valid()`.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** (and `resources/Core_DB_customized.sql` for `PARTY_CONTACT_PREFERENCE`) — enforced at construction time via 10 module-level `_COLS_*` lists. After `stamp_di()` appends the 5 DI columns, the full column order matches the Tier 0/1/2/3/4a/4b convention.
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — n/a: that table is Step 22.
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — n/a: no GEOSPATIAL row authored here.
- **No ORMs, no database connections — pure pandas → CSV** — generator returns DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — `ctx.rng` is **not used** in this step. All values are deterministic projections of `cp` attributes or modulo picks on sorted pools. No Faker (no names generated — `PARTY_IDENTIFICATION.Party_Identification_Num` is an opaque token `f'{type[:3]}-{party_id:09d}'`, not a realistic SSN/passport).

Step-specific rules (Tier 4c Shared Party Attributes):

- **No randomness at all.** This step does not construct a Faker instance, does not call `ctx.rng`, does not use `random` / `numpy.random`, and does not call `hash()`. All non-constant values are either (a) direct projections of `cp` fields or (b) `pool[cp.party_id % len(pool)]` where `pool` is a sorted list built from a seeded Tier 0 table, or (c) fixed literals. Reproducibility is byte-exact by construction.
- **DEMOGRAPHIC_VALUE is seeded inline, not via `seed_data/*.py`.** This is a deliberate deviation from the Seed Data Authoring Convention for a shallow (~12 row) lookup with no cross-module consumers. Every `PARTY_DEMOGRAPHIC` row's composite `(Demographic_Cd, Demographic_Value_Cd)` must resolve to a row in this step's `DEMOGRAPHIC_VALUE` output — **enforced by construction** (both tables are built from the same `_DEMOGRAPHIC_CODES` constant and the same `_age_band` / `_dependents_band` helper functions).
- **`PARTY_LANGUAGE_USAGE` emits exactly 2 rows per party in the order `(primary spoken language, primary written language)`.** This order is fixed in `_LANGUAGE_USAGE_TYPES` (imported from `config.code_values.LANGUAGE_USAGE_TYPES`) and iterated per party. Any deviation (single row, reversed order, extra rows) violates Layer 2 constraint #4 (`mvp-tool-design.md` §12 #4).
- **`PARTY_STATUS` emits `'CHURNED'` only for `cp.lifecycle_cohort == 'CHURNED'`.** The CHURNED cohort (~5%) gets TWO rows: historical `'ACTIVE'` with `Party_Status_Dt = cp.party_since` AND current `'CHURNED'` with `Party_Status_Dt = HISTORY_START` (`2025-10-01`). Layer 2's `WHERE Party_Status_Dt = max(...)` selects the CHURNED row. Other cohorts get ONE row each (`'ACTIVE'` or `'BANKRUPT'`).
- **`BANKRUPT` subset is deterministic and individual-only.** Filter: `cp.lifecycle_cohort != 'CHURNED' AND cp.party_type == 'INDIVIDUAL' AND cp.party_id % _BANKRUPT_MOD == 0`. Target row count ~1.1% of individuals (~26 at 2400 × 0.011 = ~26). If this deviates from the 1.1% target by more than a factor of 2 at seed=42, adjust `_BANKRUPT_MOD` (smaller modulo → more hits) — document the chosen value in a 1-line comment.
- **`PARTY_SCORE.Party_Score_Val` is a VARCHAR(100) probability string `"0.xxxx"` derived deterministically from `party_id`.** Formula: `f'{(cp.party_id % 10000) / 10000:.4f}'`. This is a synthetic score (MVP placeholder); real Layer 2 customer-profitability computation is out of scope.
- **`PARTY_CREDIT_REPORT_SCORE` is individual-only.** `Credit_Report_Score_Num = str(cp.fico_score)` emits a VARCHAR like `"720"`. Organizations have `cp.fico_score == 0` and are excluded. `Score_Type_Cd = 'FICO'` fixed for all rows.
- **`PARTY_IDENTIFICATION` emits exactly 3 rows per individual in the order `('SSN', "Driver's License", 'Passport')`.** `Primary_Ind='Yes'` only on the SSN row; `'No'` on DL/Passport (CHAR(3) per PRD §4.3). `Party_Identification_Num` is an opaque token `f'{type_cd[:3].upper()}-{cp.party_id:09d}'` — NEVER generate a realistic SSN/passport/DL number (privacy by construction; the MVP dataset must never resemble real PII even accidentally).
- **`PARTY_DEMOGRAPHIC` emits exactly 3 rows per individual (AGE_BAND, INCOME_QUARTILE, DEPENDENTS).** Every row's `(Demographic_Cd, Demographic_Value_Cd)` pair must exist in this step's `DEMOGRAPHIC_VALUE` output (composite FK). `Data_Source_Type_Cd = 'CORE_BANKING'` for all rows (reuses Tier 4a Individual Medical's choice). Organizations excluded.
- **CHAR(3) flags use `'Yes'` / `'No'`, not `'Y'` / `'N'`** (PRD §4.3). Applies to `PARTY_IDENTIFICATION.Party_Identification_Primary_Ind` only.
- **SMALLINT columns on `PARTY_CONTACT_PREFERENCE` are plain integers.** `Channel_Type_Cd` ∈ {1, 3}; `Contact_Preference_Type_Cd` ∈ {1, 2}; `Protocol_Type_Cd=Days_Cd=Hours_Cd=1`; `Party_Contact_Preference_Priority_Num=1` (INTEGER, not SMALLINT — nullable per DDL but populated with `1` here). Do NOT cast SMALLINT columns to Int64 — they are not BIGINT ID columns. Cast to `Int16` if explicit type pinning is needed.
- **`PARTY_CONTACT_PREFERENCE.Party_Contact_Preference_End_Dt` is declared NOT NULL in the DDL.** Use `HIGH_DATE = '9999-12-31'` as the active-row sentinel (not `None`) — this is the only Tier 4c column where the active-row convention deviates from PRD §7.4's `NULL` default, analogous to `INDIVIDUAL_NAME.Individual_Name_End_Dt` in Tier 4a.
- **`PARTY_STATUS` has only 3 business columns — no start/end date range.** The table is an append-only status-ledger; Layer 2 filters by `max(Party_Status_Dt)` to get the current status. Do NOT add a `*_End_Dt` column that isn't in the DDL.
- **Org-only vs individual-only table filters (enforced by explicit `if cp.party_type == 'INDIVIDUAL'` guards, not by silent `fico_score > 0` checks):**
  - Individual-only: `PARTY_CREDIT_REPORT_SCORE`, `PARTY_IDENTIFICATION`, `PARTY_DEMOGRAPHIC`.
  - All-party: `PARTY_LANGUAGE_USAGE`, `PARTY_STATUS`, `PARTY_SCORE`, `PARTY_SEGMENT`, `PARTY_CONTACT_PREFERENCE`.
  - `PARTY_SPECIALTY`: all-party subset (mod 10), no type filter.
- **`DEMOGRAPHIC_VALUE` rows must be emitted BEFORE PARTY_DEMOGRAPHIC FKs resolve** — not a dataflow problem since both are built inside `generate()` and returned in the same dict; but the `assert` in the Definition of done must check that every `(Demographic_Cd, Demographic_Value_Cd)` pair used in PARTY_DEMOGRAPHIC exists as a row in DEMOGRAPHIC_VALUE.
- **No new ID minting.** `ctx.ids` is not called. No `*_Id` columns are generated by this step beyond the projections above.
- **Deterministic derivations only.** `pool[cp.party_id % len(pool)]` is the only indexing primitive for SPECIALTY_TYPE. Pools are sorted at construction. No `hash()`, no `random.choice()`, no `ctx.rng.choice()`.
- **No side effects on import.** `import generators.tier4c_shared` must not construct any DataFrames, build any pools, or perform any I/O. All heavy work happens inside `generate()`.
- **Fail-fast guards at top of `generate()`** (order: populated-universe → tier-0 lookups → tier-2 tables → analytical-model-row-exists → market-segment-mapping-complete). Each guard raises `RuntimeError` with a distinct, greppable message.
- **Escalation over improvisation.** If `07` (or `Core_DB_customized.sql` for PARTY_CONTACT_PREFERENCE) has a column-level ambiguity, stop and leave a `⚠️ Conflict` block in this spec. Do NOT invent columns or silently swap FKs.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current working directory and `python` resolves to the project's environment. All non-trivial checks run in a single `python` process after constructing the full pre-Tier-4c context — this is cheap (<20s end-to-end). The **helper context builder** below (reused by most checks) loads Steps 1–11 output including Tier 2 (which provides ANALYTICAL_MODEL and MARKET_SEGMENT).

### Module-import and API contract

- [ ] `python -c "import generators.tier4c_shared"` exits 0 and triggers no DataFrame construction or I/O side effects.
- [ ] `generators.tier4c_shared.Tier4cShared` inherits from `BaseGenerator` and defines `generate(ctx)`:
  ```bash
  python -c "
  from generators.tier4c_shared import Tier4cShared
  from generators.base import BaseGenerator
  import inspect
  assert issubclass(Tier4cShared, BaseGenerator)
  sig = inspect.signature(Tier4cShared.generate)
  assert 'ctx' in sig.parameters
  print('Tier4cShared contract OK')
  "
  ```

### Helper: full pre-Tier-4c context builder (reused by subsequent checks)

Save as `_verify_tier4c.py` at the project root (delete after the session if desired):

```python
# _verify_tier4c.py — helper loader reused across Definition-of-done checks.
import numpy as np, pandas as pd
import config.settings as cfg
from registry.universe import UniverseBuilder
from registry.context import GenerationContext
from generators.tier0_lookups    import Tier0Lookups
from generators.tier1_geography  import Tier1Geography
from generators.tier2_core       import Tier2Core
from generators.tier3_party_subtypes import Tier3PartySubtypes
from generators.tier4c_shared    import Tier4cShared

def build_pre_tier4c():
    rng = np.random.default_rng(cfg.SEED)
    universe = UniverseBuilder().build(config=cfg, rng=rng)
    ctx = universe.to_context(cfg, rng) if hasattr(universe, 'to_context') else universe
    # Sequential Tier 0/1/2/3
    for tier in (Tier0Lookups(), Tier1Geography(), Tier2Core(), Tier3PartySubtypes()):
        ctx.tables.update(tier.generate(ctx))
    return ctx

def build_with_tier4c():
    ctx = build_pre_tier4c()
    ctx.tables.update(Tier4cShared().generate(ctx))
    return ctx

if __name__ == '__main__':
    ctx = build_with_tier4c()
    print(f'customers={len(ctx.customers)}, tables={len(ctx.tables)}')
```

- [ ] `python _verify_tier4c.py` exits 0 and prints non-zero customer + table counts.

### Row-count and shape checks

- [ ] `PARTY_LANGUAGE_USAGE` has exactly 2 rows per party and both language-usage-type literals appear per party:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  df = ctx.tables['Core_DB.PARTY_LANGUAGE_USAGE']
  counts = df.groupby('Party_Id').size()
  assert (counts == 2).all(), f'parties without 2 rows: {(counts != 2).sum()}'
  pivot = df.groupby('Party_Id')['Language_Usage_Type_Cd'].apply(set)
  required = {'primary spoken language', 'primary written language'}
  assert (pivot == required).all(), f'parties missing a usage type: {(pivot != required).sum()}'
  print('OK — PARTY_LANGUAGE_USAGE')
  "
  ```
- [ ] `PARTY_STATUS` has ≥1 row per party; CHURNED cohort has a `'CHURNED'` row; BANKRUPT rate is in the 0.5%–2% range:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  df = ctx.tables['Core_DB.PARTY_STATUS']
  party_counts = df.groupby('Party_Id').size()
  assert (party_counts >= 1).all(), 'party missing PARTY_STATUS row'
  churned_cps = [cp for cp in ctx.customers if cp.lifecycle_cohort == 'CHURNED']
  churned_ids = {cp.party_id for cp in churned_cps}
  churned_rows = df[(df['Party_Id'].isin(churned_ids)) & (df['Party_Status_Cd'] == 'CHURNED')]
  assert len(churned_rows) == len(churned_ids), f'CHURNED parties missing status row: {len(churned_ids) - len(churned_rows)}'
  bk = df[df['Party_Status_Cd'] == 'BANKRUPT']
  ind_total = sum(1 for cp in ctx.customers if cp.party_type == 'INDIVIDUAL')
  pct = len(bk) / ind_total
  assert 0.005 <= pct <= 0.02, f'BANKRUPT rate {pct:.4f} outside 0.5%–2% band'
  print(f'OK — PARTY_STATUS  (BANKRUPT={len(bk)}, {pct:.2%})')
  "
  ```
- [ ] **SCD2 history for CHURNED cohort:** each CHURNED party has exactly 2 `PARTY_STATUS` rows — one `'ACTIVE'` with `Party_Status_Dt == cp.party_since`, one `'CHURNED'` with `Party_Status_Dt == HISTORY_START` (`2025-10-01`), and the ACTIVE date precedes the CHURNED date (PRD §7.4 SCD2 history requirement):
  ```bash
  python -c "
  from datetime import date
  from _verify_tier4c import build_with_tier4c
  from config.settings import HISTORY_START
  ctx = build_with_tier4c()
  df = ctx.tables['Core_DB.PARTY_STATUS']
  cp_by_id = {cp.party_id: cp for cp in ctx.customers if cp.lifecycle_cohort == 'CHURNED'}
  churned_df = df[df['Party_Id'].isin(cp_by_id.keys())]
  counts = churned_df.groupby('Party_Id').size()
  assert (counts == 2).all(), f'CHURNED parties without exactly 2 rows: {(counts != 2).sum()} (sample: {counts[counts != 2].head().to_dict()})'
  for pid, grp in churned_df.groupby('Party_Id'):
      codes = set(grp['Party_Status_Cd'])
      assert codes == {'ACTIVE', 'CHURNED'}, f'party {pid} status codes {codes}, want {{ACTIVE, CHURNED}}'
      active_dt = grp.loc[grp['Party_Status_Cd'] == 'ACTIVE', 'Party_Status_Dt'].iloc[0]
      churned_dt = grp.loc[grp['Party_Status_Cd'] == 'CHURNED', 'Party_Status_Dt'].iloc[0]
      # Normalise to date() — generator may emit date or pd.Timestamp
      ad = active_dt.date() if hasattr(active_dt, 'date') else active_dt
      cd = churned_dt.date() if hasattr(churned_dt, 'date') else churned_dt
      assert ad == cp_by_id[pid].party_since, f'party {pid} ACTIVE Dt {ad} != party_since {cp_by_id[pid].party_since}'
      assert cd == HISTORY_START, f'party {pid} CHURNED Dt {cd} != HISTORY_START {HISTORY_START}'
      assert ad < cd, f'party {pid} ACTIVE Dt {ad} not before CHURNED Dt {cd}'
  print(f'OK — CHURNED SCD2 history ({len(cp_by_id)} parties × 2 rows)')
  "
  ```
- [ ] `PARTY_SCORE` has exactly 1 row per party and every row carries the customer-profitability Model_Id:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  df = ctx.tables['Core_DB.PARTY_SCORE']
  assert (df.groupby('Party_Id').size() == 1).all(), 'party with != 1 PARTY_SCORE row'
  am = ctx.tables['Core_DB.ANALYTICAL_MODEL']
  prof_ids = set(am[am['Model_Purpose_Cd'] == 'customer profitability']['Model_Id'].tolist())
  assert set(df['Model_Id'].unique()).issubset(prof_ids), 'PARTY_SCORE.Model_Id references non-profitability model'
  print('OK — PARTY_SCORE')
  "
  ```
- [ ] `PARTY_CREDIT_REPORT_SCORE` has exactly 1 row per INDIVIDUAL party; score values parse as integers in [300, 850]:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  df = ctx.tables['Core_DB.PARTY_CREDIT_REPORT_SCORE']
  ind_ids = {cp.party_id for cp in ctx.customers if cp.party_type == 'INDIVIDUAL'}
  assert set(df['Obligor_Party_Id'].tolist()) == ind_ids, 'Obligor_Party_Id set != individual party set'
  scores = df['Credit_Report_Score_Num'].astype(int)
  assert scores.between(300, 850).all(), f'FICO out of range: min={scores.min()}, max={scores.max()}'
  assert (df['Score_Type_Cd'] == 'FICO').all()
  print('OK — PARTY_CREDIT_REPORT_SCORE')
  "
  ```
- [ ] `PARTY_IDENTIFICATION` has exactly 3 rows per individual; each individual has all 3 required types; Primary_Ind='Yes' only on SSN:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  df = ctx.tables['Core_DB.PARTY_IDENTIFICATION']
  ind_ids = {cp.party_id for cp in ctx.customers if cp.party_type == 'INDIVIDUAL'}
  assert set(df['Party_Id'].tolist()) - ind_ids == set(), 'non-individual in PARTY_IDENTIFICATION'
  counts = df.groupby('Party_Id').size()
  assert (counts == 3).all(), f'individuals without 3 id rows: {(counts != 3).sum()}'
  types_per = df.groupby('Party_Id')['Party_Identification_Type_Cd'].apply(set)
  required = {'SSN', \"Driver's License\", 'Passport'}
  assert (types_per == required).all(), 'missing required id type per individual'
  ssn = df[df['Party_Identification_Type_Cd'] == 'SSN']
  assert (ssn['Party_Identification_Primary_Ind'] == 'Yes').all()
  nonssn = df[df['Party_Identification_Type_Cd'] != 'SSN']
  assert (nonssn['Party_Identification_Primary_Ind'] == 'No').all()
  print('OK — PARTY_IDENTIFICATION')
  "
  ```
- [ ] `PARTY_DEMOGRAPHIC` FKs resolve to `DEMOGRAPHIC_VALUE` for every row:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  pd_df = ctx.tables['Core_DB.PARTY_DEMOGRAPHIC']
  dv_df = ctx.tables['Core_DB.DEMOGRAPHIC_VALUE']
  dv_keys = set(zip(dv_df['Demographic_Cd'], dv_df['Demographic_Value_Cd']))
  pd_keys = set(zip(pd_df['Demographic_Cd'], pd_df['Demographic_Value_Cd']))
  missing = pd_keys - dv_keys
  assert not missing, f'PARTY_DEMOGRAPHIC has {len(missing)} orphan FKs: {list(missing)[:5]}'
  ind_ids = {cp.party_id for cp in ctx.customers if cp.party_type == 'INDIVIDUAL'}
  assert set(pd_df['Party_Id'].tolist()).issubset(ind_ids), 'non-individual in PARTY_DEMOGRAPHIC'
  assert (pd_df.groupby('Party_Id').size() == 3).all(), 'individual with != 3 demographic rows'
  print(f'OK — PARTY_DEMOGRAPHIC (DV rows={len(dv_df)})')
  "
  ```
- [ ] `PARTY_SEGMENT` FKs resolve to `MARKET_SEGMENT.Market_Segment_Id` and there is exactly 1 row per party:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  ps = ctx.tables['Core_DB.PARTY_SEGMENT']
  ms = ctx.tables['Core_DB.MARKET_SEGMENT']
  valid = set(ms['Market_Segment_Id'].tolist())
  assert set(ps['Market_Segment_Id'].unique()).issubset(valid), 'PARTY_SEGMENT has orphan FK'
  assert (ps.groupby('Party_Id').size() == 1).all()
  print('OK — PARTY_SEGMENT')
  "
  ```
- [ ] `PARTY_SPECIALTY` FKs resolve to `SPECIALTY_TYPE.Specialty_Type_Cd` and row count is between 50 and 500:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  ps = ctx.tables['Core_DB.PARTY_SPECIALTY']
  st = ctx.tables['Core_DB.SPECIALTY_TYPE']
  valid = set(st['Specialty_Type_Cd'].tolist())
  assert set(ps['Specialty_Type_Cd'].unique()).issubset(valid)
  assert 50 <= len(ps) <= 500, f'PARTY_SPECIALTY count {len(ps)} outside [50, 500]'
  print(f'OK — PARTY_SPECIALTY  (rows={len(ps)})')
  "
  ```
- [ ] `PARTY_CONTACT_PREFERENCE` has exactly 2 rows per party; Channel_Type_Cd follows `has_internet`; Sales+Service both present:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  df = ctx.tables['Core_DB.PARTY_CONTACT_PREFERENCE']
  assert (df.groupby('Party_Id').size() == 2).all()
  by_party = df.groupby('Party_Id')['Contact_Preference_Type_Cd'].apply(set)
  assert (by_party == {1, 2}).all(), 'parties missing Sales or Service row'
  cp_by_id = {cp.party_id: cp for cp in ctx.customers}
  for _, r in df.iterrows():
      expected = 3 if cp_by_id[r['Party_Id']].has_internet else 1
      assert r['Channel_Type_Cd'] == expected, f'party {r[\"Party_Id\"]}: has_internet={cp_by_id[r[\"Party_Id\"]].has_internet}, Channel_Type_Cd={r[\"Channel_Type_Cd\"]}'
  assert (df['Party_Contact_Preference_End_Dt'].astype(str) == '9999-12-31').all()
  print('OK — PARTY_CONTACT_PREFERENCE')
  "
  ```

### DDL column-order check (detects corrupted `_COLS_*` constants)

- [ ] The business-column prefix of every returned DataFrame matches the DDL verbatim — transcribed **independently** from `references/07_mvp-schema-reference.md` (and `resources/Core_DB_customized.sql` for PARTY_CONTACT_PREFERENCE) into an `EXPECTED_ORDER` dict that is **not** imported from `generators/tier4c_shared`. If someone corrupts a `_COLS_*` constant (typo, swapped columns, missing column) the check catches it because the source of truth is the DDL, not the module constant.
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  EXPECTED_ORDER = {
      'PARTY_LANGUAGE_USAGE': ['Party_Id','Language_Type_Cd','Language_Usage_Type_Cd','Party_Language_Start_Dttm','Party_Language_End_Dttm','Party_Language_Priority_Num'],
      'PARTY_STATUS':         ['Party_Id','Party_Status_Cd','Party_Status_Dt'],
      'PARTY_SCORE':          ['Party_Id','Model_Id','Model_Run_Id','Party_Score_Val'],
      'PARTY_CREDIT_REPORT_SCORE': ['Reporting_Party_Id','Obligor_Party_Id','Credit_Report_Dttm','Score_Type_Cd','Credit_Report_Score_Num'],
      'PARTY_IDENTIFICATION': ['Party_Id','Issuing_Party_Id','Party_Identification_Type_Cd','Party_Identification_Start_Dttm','Party_Identification_End_Dttm','Party_Identification_Num','Party_Identification_Receipt_Dt','Party_Identification_Primary_Ind','Party_Identification_Name'],
      'PARTY_DEMOGRAPHIC':    ['Party_Id','Demographic_Cd','Data_Source_Type_Cd','Party_Demographic_Start_Dt','Demographic_Value_Cd','Party_Demographic_End_Dt','Party_Demographic_Num','Party_Demographic_Val'],
      'DEMOGRAPHIC_VALUE':    ['Demographic_Cd','Demographic_Value_Cd','Demographic_Range_Start_Val','Demographic_Range_End_Val','Demographic_Value_Desc','Demographic_Val'],
      'PARTY_SEGMENT':        ['Party_Id','Market_Segment_Id','Party_Segment_Start_Dttm','Party_Segment_End_Dttm'],
      'PARTY_SPECIALTY':      ['Party_Id','Specialty_Type_Cd','Party_Specialty_Start_Dt','Party_Specialty_End_Dt'],
      'PARTY_CONTACT_PREFERENCE': ['Party_Id','Channel_Type_Cd','Contact_Preference_Type_Cd','Party_Contact_Preference_Start_Dt','Party_Contact_Preference_End_Dt','Party_Contact_Preference_Priority_Num','Protocol_Type_Cd','Days_Cd','Hours_Cd'],
  }
  ctx = build_with_tier4c()
  for table, expected in EXPECTED_ORDER.items():
      df = ctx.tables[f'Core_DB.{table}']
      actual_prefix = list(df.columns[:len(expected)])
      assert actual_prefix == expected, f'{table} column-order mismatch:\n  expected: {expected}\n  actual:   {actual_prefix}'
  print(f'OK — DDL column order verified on {len(EXPECTED_ORDER)} tables')
  "
  ```

### DI columns and schema invariants

- [ ] Every returned DataFrame has the canonical 5-col DI tail in the correct order:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  from utils.di_columns import DI_COLUMN_ORDER
  ctx = build_with_tier4c()
  expected = list(DI_COLUMN_ORDER)
  tables = ['PARTY_LANGUAGE_USAGE','PARTY_STATUS','PARTY_SCORE','PARTY_CREDIT_REPORT_SCORE',
            'PARTY_IDENTIFICATION','PARTY_DEMOGRAPHIC','DEMOGRAPHIC_VALUE','PARTY_SEGMENT',
            'PARTY_SPECIALTY','PARTY_CONTACT_PREFERENCE']
  for t in tables:
      cols = list(ctx.tables[f'Core_DB.{t}'].columns)
      assert cols[-5:] == expected, f'{t} DI tail wrong: {cols[-5:]}'
      df = ctx.tables[f'Core_DB.{t}']
      assert (df['di_end_ts'] == '9999-12-31 00:00:00.000000').all()
      assert (df['di_rec_deleted_Ind'] == 'N').all()
  print('OK — DI columns stamped on all 10 tables')
  "
  ```
- [ ] No `stamp_valid()` was called — no Valid_From_Dt / Valid_To_Dt / Del_Ind columns on any Tier 4c table:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  banned = {'Valid_From_Dt', 'Valid_To_Dt', 'Del_Ind'}
  for t in ['PARTY_LANGUAGE_USAGE','PARTY_STATUS','PARTY_SCORE','PARTY_CREDIT_REPORT_SCORE',
            'PARTY_IDENTIFICATION','PARTY_DEMOGRAPHIC','DEMOGRAPHIC_VALUE','PARTY_SEGMENT',
            'PARTY_SPECIALTY','PARTY_CONTACT_PREFERENCE']:
      cols = set(ctx.tables[f'Core_DB.{t}'].columns)
      assert not (cols & banned), f'{t} has Valid_* columns: {cols & banned}'
  print('OK — no stamp_valid called')
  "
  ```
- [ ] Every `*_Id` column is `Int64` (nullable BIGINT) on every returned DataFrame:
  ```bash
  python -c "
  from _verify_tier4c import build_with_tier4c
  ctx = build_with_tier4c()
  for t in ['PARTY_LANGUAGE_USAGE','PARTY_STATUS','PARTY_SCORE','PARTY_CREDIT_REPORT_SCORE',
            'PARTY_IDENTIFICATION','PARTY_DEMOGRAPHIC','DEMOGRAPHIC_VALUE','PARTY_SEGMENT',
            'PARTY_SPECIALTY','PARTY_CONTACT_PREFERENCE']:
      df = ctx.tables[f'Core_DB.{t}']
      id_cols = [c for c in df.columns if c.endswith('_Id')]
      for c in id_cols:
          assert str(df[c].dtype) == 'Int64', f'{t}.{c} dtype is {df[c].dtype}, want Int64'
  print('OK — BIGINT Int64 on all *_Id columns')
  "
  ```

### Layer 2 constraint delivery (mapped to `mvp-tool-design.md` §12)

- [ ] **Layer 2 #4** (`PARTY_LANGUAGE_USAGE` 2-row rule) — covered by the PARTY_LANGUAGE_USAGE row-count check above.
- [ ] **Layer 2 #5** (`PARTY_STATUS` ≥1 per party) — covered by the PARTY_STATUS check above.
- [ ] **Layer 2 #18** (`PARTY_SCORE` with customer-profitability model) — covered by the PARTY_SCORE Model_Id check above.
- [ ] **Layer 2 #22** (`PARTY_IDENTIFICATION` SSN + DL + Passport types per individual) — covered by the PARTY_IDENTIFICATION types check above.

### Reproducibility

- [ ] Two successive builds with seed=42 produce byte-identical Tier 4c DataFrames:
  ```bash
  python -c "
  import hashlib
  from _verify_tier4c import build_with_tier4c
  def fp(ctx):
      h = hashlib.sha256()
      for k in sorted(ctx.tables):
          if not k.startswith('Core_DB.') or k.split('.')[1] not in {
              'PARTY_LANGUAGE_USAGE','PARTY_STATUS','PARTY_SCORE','PARTY_CREDIT_REPORT_SCORE',
              'PARTY_IDENTIFICATION','PARTY_DEMOGRAPHIC','DEMOGRAPHIC_VALUE','PARTY_SEGMENT',
              'PARTY_SPECIALTY','PARTY_CONTACT_PREFERENCE'}:
              continue
          h.update(k.encode())
          h.update(ctx.tables[k].to_csv(index=False).encode())
      return h.hexdigest()
  a, b = fp(build_with_tier4c()), fp(build_with_tier4c())
  assert a == b, f'reruns differ: {a[:12]} vs {b[:12]}'
  print(f'OK — reproducibility  (fp={a[:12]})')
  "
  ```

### Side-effect guards

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else. The only new tracked file should be `generators/tier4c_shared.py`; the `_verify_tier4c.py` helper is a session-local scratch file and should be deleted (or git-ignored) before the session ends.
- [ ] No CSV files in `output/` were created: `ls output/Core_DB/ 2>/dev/null | wc -l` = 0 (or the same count as before the session started, if Steps 1–11 output already exists there for inspection).
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — n/a (Tier 4c does not write CSVs; GEOSPATIAL is a Tier 5 concern).
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — covered by the BIGINT/Int64 check above.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — n/a (that table is Step 22, not Tier 4c).

### Module-hygiene & minimal-review checks

- [ ] `generators/tier4c_shared.py` has no top-level I/O, no top-level DataFrame construction, and no top-level `Faker()` or `np.random` calls. The only top-level work is imports, `TYPE_CHECKING` guards, and module-level constants.
- [ ] `generators/tier4c_shared.py` does not mutate `ctx.tables` (returns a dict; does not write to `ctx.tables[...] = ...`).
- [ ] `python -c "from generators.tier4c_shared import Tier4cShared; t = Tier4cShared(); print(type(t).__name__)"` prints `Tier4cShared` without raising.

## Handoff notes

### What shipped
`generators/tier4c_shared.py` — `Tier4cShared(BaseGenerator)` with a single `generate()` method returning all 10 Core_DB DataFrames. All Definition-of-Done checks passed at seed=42:
- PARTY_LANGUAGE_USAGE: 6,000 rows (2 × 3,000 parties, both usage types per party) ✓
- PARTY_STATUS: 3,150 rows (150 CHURNED × 2 rows, 19 BANKRUPT × 1, rest ACTIVE × 1) — BANKRUPT rate 0.79% ✓
- PARTY_SCORE: 3,000 rows (1 per party, customer-profitability Model_Id) ✓
- PARTY_CREDIT_REPORT_SCORE: 2,400 rows (individuals only, FICO 300–850) ✓
- PARTY_IDENTIFICATION: 7,200 rows (3 × 2,400 individuals, SSN/DL/Passport, Primary_Ind CHAR(3)) ✓
- PARTY_DEMOGRAPHIC + DEMOGRAPHIC_VALUE: 7,200 + 12 rows; all FKs resolve ✓
- PARTY_SEGMENT: 3,000 rows (1 per party, CLV→Market_Segment_Id mapping) ✓
- PARTY_SPECIALTY: 300 rows (every 10th party) ✓
- PARTY_CONTACT_PREFERENCE: 6,000 rows (2 × 3,000; channel follows has_internet; End_Dt = HIGH_DATE sentinel) ✓
- Reproducibility SHA-256: `112dfbd4ba2a...` ✓

### Conflict found and resolved
**`ANALYTICAL_MODEL` has no `Model_Run_Id` column.** The spec said to look up `Model_Run_Id` from the ANALYTICAL_MODEL row. The actual DDL (confirmed in `07_mvp-schema-reference.md`) has no such column. Resolution: `prof_model_run_id` is read from `MARKET_SEGMENT.Model_Run_Id` instead — Step 10 seeds `Model_Run_Id = 1` on all 10 MARKET_SEGMENT rows, making this the only model run in the system. `ms_df` is loaded before `prof_model_run_id` is computed. PARTY_SCORE.Model_Run_Id = 1 for all rows.

### Deviation from spec
`stamp_di()` in `utils/di_columns.py` operates on a **copy** and returns the modified DataFrame (not in-place). The spec and design doc describe it as modifying in-place. All 10 `stamp_di()` calls capture the return value (`xxx_df = self.stamp_di(xxx_df, ...)`).

### Next session hint
Step 15 (Tier 5 + Tier 6 — Location & Links) is next in the sequential chain. Steps 12/13/14 are all complete; Step 15 can start now.

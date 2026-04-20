# Spec: Step 12 — Tier 4a Individual Attributes

## Overview

This step builds **Tier 4a — Individual Attributes**, the 12 `Core_DB` attribute tables that hang off every `INDIVIDUAL` row from Step 11. Each table is a deterministic projection of `CustomerProfile` fields (`party_id`, `gender_type_cd`, `marital_status_cd`, `occupation_cd`, `clv_segment`, `party_since`, `age`, etc.) onto a schema-compliant row shape. The tables fall into three groups: (a) **per-individual attribute rows** — `INDIVIDUAL_NAME`, `INDIVIDUAL_GENDER_PRONOUN`, `INDIVIDUAL_MARITAL_STATUS`, `INDIVIDUAL_VIP_STATUS`, `INDIVIDUAL_OCCUPATION`, `INDIVIDUAL_MILITARY_STATUS`, `INDIVIDUAL_MEDICAL`, `INDIVIDUAL_SKILL`, `INDIVIDUAL_SPECIAL_NEED` — one row per individual (per PRD §9 Q1: all individuals populated, no sparse treatment); (b) **employment-timing rows** — `INDIVIDUAL_PAY_TIMING`, `INDIVIDUAL_BONUS_TIMING` — one row per individual whose `occupation_cd ∈ {'EMP', 'SELF_EMP'}` (`RETIRED` and `NOT_WORKING` explicitly excluded), with `Business_Party_Id` FK pointing to a real `ORGANIZATION` for `EMP` or to the reserved `SELF_EMP_ORG_ID = 9_999_999` placeholder for `SELF_EMP` (per PRD §7.12 / `references/05_architect-qa.md` Q7); (c) the **bank-associate subset** — `ASSOCIATE_EMPLOYMENT` — a small deterministic ~2% of `EMP` individuals whose `Organization_Party_Id` FKs to `BANK_PARTY_ID = 9_999_999` (the same reserved row that doubles as the bank entity per `config/settings.py`). The only non-deterministic element is name generation via `faker.Faker` — seeded from `config.settings.SEED = 42` for byte-identical reruns. See `mvp-tool-design.md` §9 Tier 4 for the authoritative per-table constraint list, `PRD.md` §9 Q1/Q2 for the all-populated rule on medical/skill/special-need tables, and `references/05_architect-qa.md` Q7 for the self-employment placeholder rationale.

## Depends on

- **Step 1** — consumes from `config/settings.py`: `SELF_EMP_ORG_ID = 9_999_999` (used for `INDIVIDUAL_PAY_TIMING.Business_Party_Id` / `INDIVIDUAL_BONUS_TIMING.Business_Party_Id` for `SELF_EMP` individuals), `BANK_PARTY_ID = 9_999_999` (used for `ASSOCIATE_EMPLOYMENT.Organization_Party_Id` — same reserved row, semantic dual role documented in settings.py), `SIM_DATE` (used as upper bound for all `*_Start_Dt` fields and as the present-day anchor for Layer 2 `BETWEEN` semantics), `HIGH_DATE` / `HIGH_TS` (stamped indirectly via `BaseGenerator.stamp_di()` and explicitly on `INDIVIDUAL_NAME.Individual_Name_End_Dt` per Layer 2 constraint #3), `SEED = 42` (used to seed `faker.Faker`).
- **Step 2** — consumes `generators/base.BaseGenerator` (`stamp_di()` only — Tier 4a is all Core_DB, so `stamp_valid()` is **never called**). Consumes `utils/date_utils.format_date` implicitly via the eventual writer; this step produces DataFrames with Python `date` / `datetime` / `None` values, not pre-formatted strings. No new utility modules are created.
- **Step 3** — consumes `registry/profiles.CustomerProfile` (fields read: `party_id`, `party_type`, `age`, `gender_type_cd`, `marital_status_cd`, `ethnicity_type_cd`, `occupation_cd`, `clv_segment`, `party_since`). `registry/context.GenerationContext` (consumed positionally; this step returns a `Dict[str, pd.DataFrame]` rather than mutating `ctx.tables`).
- **Step 4** — consumes the built universe. Critical invariants this step relies on and must re-verify in guards:
  - Every `INDIVIDUAL`-type `CustomerProfile` has `cp.gender_type_cd ∈ {'MALE','FEMALE'}`, `cp.marital_status_cd ∈ {'MARRIED','SINGLE'}`, `cp.occupation_cd ∈ {'EMP','SELF_EMP','RETIRED','NOT_WORKING'}`, `cp.clv_segment ∈ [1..10]`, `cp.party_since ≤ SIM_DATE`.
  - `cp.party_since` is a `date` — used as `*_Start_Dt` base and as the anchor for date deltas (e.g., `cp.party_since - timedelta(days=365)` for `Associate_Hire_Dt`). Never produce a date > `SIM_DATE` for a `Start_Dt` column.
- **Step 8** — consumes already-stamped Tier 0 lookup tables (FK resolution). Required FK target codes (all must exist in `ctx.tables` before this step runs — verify in fail-fast guard):
  - `Core_DB.GENDER_PRONOUN` — `INDIVIDUAL_GENDER_PRONOUN.Gender_Pronoun_Cd` FKs here. Seeded codes include `HE, HIM, HIS, HIMSELF, SHE, HER, HERS, THEY, THEM, THEIR, THEIRS, THEMSELVES`.
  - `Core_DB.MARITAL_STATUS_TYPE` — `INDIVIDUAL_MARITAL_STATUS.Marital_Status_Cd` FKs here. Seeded codes include `MARRIED, SINGLE` (plus others ignored by MVP).
  - `Core_DB.VERY_IMPORTANT_PERSON_TYPE` — `INDIVIDUAL_VIP_STATUS.VIP_Type_Cd` FKs here. Seeded codes: `NONE, PLATINUM, GOLD, SILVER, BRONZE`.
  - `Core_DB.OCCUPATION_TYPE` — `INDIVIDUAL_OCCUPATION.Occupation_Type_Cd` FKs here. Seeded codes exactly match `cp.occupation_cd`: `EMP, SELF_EMP, RETIRED, NOT_WORKING`.
  - `Core_DB.MILITARY_STATUS_TYPE` — `INDIVIDUAL_MILITARY_STATUS.Military_Status_Type_Cd` FKs here. Seeded codes: `ACTIVE_DUTY, VETERAN, RESERVE, NATIONAL_GUARD, CIVILIAN, RETIRED_MILITARY`.
  - `Core_DB.GENERAL_MEDICAL_STATUS_TYPE` — `INDIVIDUAL_MEDICAL.General_Medical_Status_Cd` FKs here. Seeded codes: `HEALTHY, CHRONIC_CONDITION, ACUTE_CONDITION, UNKNOWN, DISABLED, DECEASED`.
  - `Core_DB.DATA_SOURCE_TYPE` — `INDIVIDUAL_MEDICAL.Data_Source_Type_Cd` (NOT NULL) FKs here. Seeded codes: `CORE_BANKING, CARD_SYSTEM, LOAN_ORIGINATION, MDM` (and others).
  - `Core_DB.SKILL_TYPE` — `INDIVIDUAL_SKILL.Skill_Cd` FKs here. 15 seeded codes (`ACCOUNTING, ENGINEERING, SALES, NURSING, CARPENTRY, TEACHING, PROGRAMMING, MANAGEMENT, DRIVING, COOKING, LEGAL, MEDICINE, ADMIN, FINANCE, MARKETING`).
  - `Core_DB.SPECIAL_NEED_TYPE` — `INDIVIDUAL_SPECIAL_NEED.Special_Need_Cd` FKs here. Seeded codes: `NONE, VISUAL_IMPAIRMENT, HEARING_IMPAIRMENT, MOBILITY_IMPAIRMENT, COGNITIVE, SPEECH, OTHER`.
  - `Core_DB.TIME_PERIOD_TYPE` — `INDIVIDUAL_PAY_TIMING.Time_Period_Cd` (NOT NULL) FKs here. Seeded codes include `DAY, WEEK, MONTH, QUARTER, YEAR` etc.
- **Step 11** — consumes `ctx.tables['Core_DB.ORGANIZATION']`. Critical dependencies:
  - The reserved `Organization_Party_Id = SELF_EMP_ORG_ID = 9_999_999` row must already be present. This step FKs to it directly for `INDIVIDUAL_PAY_TIMING.Business_Party_Id` (self-employed rows) and `INDIVIDUAL_BONUS_TIMING.Business_Party_Id` (self-employed rows) and `ASSOCIATE_EMPLOYMENT.Organization_Party_Id` (bank-associate rows — using the `BANK_PARTY_ID` alias which points to the same 9_999_999 row).
  - The ~600 real `ORGANIZATION.Organization_Party_Id` values are needed as the EMP-individual FK target pool for `INDIVIDUAL_PAY_TIMING.Business_Party_Id` and `INDIVIDUAL_BONUS_TIMING.Business_Party_Id`. Read them via `sorted(set(ctx.tables['Core_DB.ORGANIZATION']['Organization_Party_Id']) - {SELF_EMP_ORG_ID})` to get a deterministic assignment pool.

No other dependencies. Does not read `ctx.tables['Core_DB.INDIVIDUAL']` — Tier 4a is a projection of `ctx.customers`, not of Step 11's INDIVIDUAL DataFrame (they encode the same information; the profile list is the source of truth for demographics per PRD §5 principle 3).

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 12):
- `PRD.md` §4.2 ("Party & Individual" sub-list enumerates all 12 Tier 4a tables — verify scope matches), §4.3 (CHAR(1) = Y/N, CHAR(3) = Yes/No — applies to `INDIVIDUAL_GENDER_PRONOUN.Self_reported_Ind` and any other CHAR(3) columns), §7.1 (BIGINT rule — every `*_Id` column in every Tier 4a table), §7.2 (shared party ID space), §7.3 (DI column rules — Core_DB gets `di_*` only), §7.4 (active-record convention — `*_End_Dt = NULL` for Core_DB, with the Layer 2 exception for `INDIVIDUAL_NAME.Individual_Name_End_Dt`), §7.6 (reproducibility — Faker seeded from `SEED`), §7.12 (self-employed placeholder), §9 Q1/Q2 (INDIVIDUAL_MEDICAL / INDIVIDUAL_SKILL / INDIVIDUAL_SPECIAL_NEED all populated — no sparse treatment)
- `mvp-tool-design.md` §9 Tier 4 ("Party Attributes" section — explicit constraints for INDIVIDUAL_NAME all-three-names NOT NULL, INDIVIDUAL_NAME End_Dt = 9999-12-31, INDIVIDUAL_PAY_TIMING / INDIVIDUAL_BONUS_TIMING self-emp rule, all tables populated), §10 rule 7 ("INDIVIDUAL_PAY_TIMING / INDIVIDUAL_BONUS_TIMING — reserved placeholder ORGANIZATION" — the authoritative phrasing of the employment-timing rule), §12 Layer 2 constraint #3 (INDIVIDUAL_NAME SIM_DATE between Start_Dt and End_Dt — drives the HIGH_DATE exception)
- `implementation-steps.md` Step 12 entry (Produces, Reads from, Exit criteria, Scope=M); Handoff Protocol (post-session notes rules); Seed Data Authoring Convention (N/A here — Tier 4a does not author seed data, only consumes it)

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/05_architect-qa.md` — read **Q7** ("INDIVIDUAL_PAY_TIMING and INDIVIDUAL_BONUS_TIMING — Business_Party_Id placeholder for self-employed individuals") **only**. Authoritative source for the `9_999_999` placeholder approach. All other Q's (Q1/Q2/Q3/Q4/Q5/Q6/Q8) are out of scope for this step.
- `references/06_supporting-enrichments.md` — read **Part A** sections A1–A7 **only** (age, gender, marital status, dependents, education, ethnicity, occupation mappings — confirms the code values this step reads from `cp`). Do NOT re-read Parts B–I — distributions were finalised in Step 4 (UniverseBuilder) and are already baked into `cp`.
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the 12 Tier 4a tables. Open only these DDL blocks (line numbers approximate):
  - `#### INDIVIDUAL_NAME` (raw DDL near line 5045). 11 business columns + 3 DI. All `*_Id` are BIGINT per §7.1. `Individual_Party_Id`, `Name_Type_Cd`, `Individual_Name_Start_Dt`, `Given_Name`, `Middle_Name`, `Family_Name` are NOT NULL. `Birth_Family_Name`, `Name_Prefix_Txt`, `Name_Suffix_Txt`, `Individual_Name_End_Dt`, `Individual_Full_Name` nullable.
  - `#### INDIVIDUAL_GENDER_PRONOUN` (near line 5086). 6 business columns + 3 DI. `Gender_Pronoun_Start_Dt`, `Individual_Party_Id`, `Gender_Pronoun_Type_Cd` NOT NULL. `Self_reported_Ind` is **CHAR(3)** — use `'Yes'`/`'No'`.
  - `#### INDIVIDUAL_MARITAL_STATUS` (near line 5117). 4 business columns + 3 DI. `Individual_Party_Id`, `Individual_Marital_Status_Start_Dt`, `Marital_Status_Cd` NOT NULL.
  - `#### ASSOCIATE_EMPLOYMENT` (near line 5144). 7 business columns + 3 DI. `Associate_Party_Id`, `Organization_Party_Id`, `Associate_Employment_Start_Dt` NOT NULL. `Associate_Termination_Dttm` is `TIMESTAMP` (no `(6)` qualifier per DDL).
  - `#### INDIVIDUAL_VIP_STATUS` (near line 5177). 4 business columns + 3 DI. `Individual_Party_Id`, `Individual_VIP_Status_Start_Dt`, `VIP_Type_Cd` NOT NULL.
  - `#### INDIVIDUAL_MILITARY_STATUS` (near line 5204). 4 business columns + 3 DI. `Individual_Party_Id`, `Individual_Military_Start_Dt`, `Military_Status_Type_Cd` NOT NULL.
  - `#### INDIVIDUAL_OCCUPATION` (near line 5231). 5 business columns + 3 DI. `Individual_Party_Id`, `Occupation_Type_Cd`, `Individual_Occupation_Start_Dt` NOT NULL. `Individual_Job_Title_Txt` nullable but populated here for demo value.
  - `#### INDIVIDUAL_PAY_TIMING` (near line 5260). 4 business columns + 3 DI. `Individual_Party_Id`, `Business_Party_Id`, `Time_Period_Cd` NOT NULL. `Pay_Day_Num` nullable.
  - `#### INDIVIDUAL_BONUS_TIMING` (near line 5287). 3 business columns + 3 DI. `Individual_Party_Id`, `Bonus_Month_Num`, `Business_Party_Id` NOT NULL.
  - `#### INDIVIDUAL_SKILL` (near line 5312). 3 business columns + 3 DI. `Individual_Party_Id`, `Skill_Cd` NOT NULL. `Individual_Skill_Dt` nullable.
  - `#### INDIVIDUAL_MEDICAL` (near line 5523). 9 business columns + 3 DI. `Individual_Party_Id`, `Data_Source_Type_Cd`, `Individual_Medical_Start_Dt` NOT NULL. All other fields (`Physical_Exam_Dt`, `General_Medical_Status_Cd`, `Last_Menstrual_Period_Dt`, `Last_X_ray_Dt`, `Estimated_Pregnancy_Due_Dt`, `Individual_Medical_End_Dt`) nullable.
  - `#### INDIVIDUAL_SPECIAL_NEED` (near line 5560). 2 business columns + 3 DI. `Individual_Party_Id`, `Special_Need_Cd` NOT NULL.

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is the MVP-filtered authoritative DDL set per PRD §10.
- `references/02_data-mapping-reference.md` — no Step 3 literal-match constraint touches any Tier 4a table directly. The `BETWEEN Start_Dt AND End_Dt` constraint on `INDIVIDUAL_NAME` is already in `mvp-tool-design.md` §12 #3.
- `references/06_supporting-enrichments.md` Parts B–I — distributions for products/balances/events; already absorbed by Step 4.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `resources/iDM_MDM_tables_DDLs.xlsx` — distilled into `07`.
- CDM_DB and PIM_DB DDL blocks — Step 22 / Step 23, not touched here.
- Other generators' code (`generators/tier0_lookups.py`, `tier1_geography.py`, `tier2_core.py`) — already stable and merged; no cross-read needed at implementation time. Only `generators/tier3_party_subtypes.py` is worth a glance for the pattern Step 11 set (module structure, constant naming, column-list convention, DI stamp call).

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier4a_individual.py` — `class Tier4aIndividual(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]` method returning 12 Core_DB DataFrames. Implementation contract:
  1. **Imports** — `from __future__ import annotations`; stdlib `datetime` (`date, datetime, time, timedelta`); third-party `pandas as pd`, `from faker import Faker`; project imports `from config.settings import SEED, SIM_DATE, SELF_EMP_ORG_ID, BANK_PARTY_ID, HIGH_DATE`; `from generators.base import BaseGenerator`; `from typing import TYPE_CHECKING, Dict, List, Optional`; `if TYPE_CHECKING: from registry.context import GenerationContext`.
  2. **Module-level constants** — use ALL-CAPS names prefixed `_` for module-private:
     - `_TIER4A_DI_START_TS = '2000-01-01 00:00:00.000000'` (fixed timestamp mirrors Tier 0/1/2/3 convention — byte-identical reruns).
     - `_GENDER_PRONOUN_BY_GENDER = {'MALE': 'HE', 'FEMALE': 'SHE'}`. No `None` / fallback — profiles guarantee one of these two values.
     - `_VIP_BY_CLV_SEGMENT: Dict[int, str]` — `{10: 'PLATINUM', 9: 'GOLD', 8: 'SILVER'}`; everything else → `'NONE'`.
     - `_JOB_TITLE_BY_OCCUPATION = {'EMP': 'Analyst', 'SELF_EMP': 'Business Owner', 'RETIRED': 'Retired', 'NOT_WORKING': 'Not Employed'}`.
     - `_MILITARY_STATUS_BY_PARTY_MOD_100: Dict[int, str]` — deterministic partition: `{0..6: 'VETERAN' (7%), 7..9: 'ACTIVE_DUTY' (3%), 10..99: 'CIVILIAN' (90%)}`. Implementation can be a helper function `_military_status_for(party_id)`; semantics must be reproducible.
     - `_MEDICAL_STATUS_BY_PARTY_MOD_10` — deterministic bias toward `'HEALTHY'` (7 of 10) with some `'CHRONIC_CONDITION'` / `'ACUTE_CONDITION'` / `'UNKNOWN'` spread. Any deterministic scheme is acceptable; document the chosen scheme in a module comment.
     - `_SKILL_POOL: List[str]` — the 15 seeded skill codes in a fixed order (copy-paste from the TIER0 section, not re-imported).
     - `_SPECIAL_NEED_POOL: List[str]` — the 7 seeded codes; bias toward `'NONE'` (~85% of rows) with deterministic small-% variation.
     - `_ASSOCIATE_SAMPLING_MOD = 50` — `party_id % 50 == 0` picks bank associates from the EMP pool (~2% of individuals → ~24 at 3000×0.8 = 2400 individuals × 0.496 EMP share → ~48 total ≈ 1 in 50).
     - `_DI_START_BACKFILL_DAYS = 3650` — used for `Associate_Hire_Dt` which precedes `Associate_Employment_Start_Dt`.
     - `_REQUIRED_TIER0_TABLES` — tuple of the 10 Tier 0 keys listed under "Depends on · Step 8" above. Used by the fail-fast guard.
     - `_REQUIRED_TIER3_TABLES = ('Core_DB.ORGANIZATION',)` — verifies Step 11 ran.
     - 12 column-order lists `_COLS_INDIVIDUAL_NAME`, `_COLS_INDIVIDUAL_GENDER_PRONOUN`, etc. — each matching the DDL business-column order verbatim (before DI columns append). Source: `references/07_mvp-schema-reference.md` per-table block.
  3. **Faker instance** — construct once per `generate()` call: `fake = Faker('en_US'); fake.seed_instance(SEED)`. Use `fake.first_name_male()`, `fake.first_name_female()`, `fake.first_name()` (middle name — unbiased), `fake.last_name()`, `fake.suffix()`. Do NOT call `Faker.seed()` (module-level — pollutes global state).
  4. **Guards (first ~10 lines of `generate()`)**:
     - Raise `RuntimeError('Tier4aIndividual requires a populated ctx.customers — run UniverseBuilder.build() first')` if `not ctx.customers`.
     - Iterate `_REQUIRED_TIER0_TABLES + _REQUIRED_TIER3_TABLES`; for any key missing from `ctx.tables`, raise `RuntimeError(f'Tier4aIndividual requires {key} to be loaded first')`.
     - Additional invariant: the reserved row must exist. Raise `RuntimeError('SELF_EMP_ORG_ID row missing from Core_DB.ORGANIZATION — Step 11 incomplete')` if `SELF_EMP_ORG_ID not in ctx.tables['Core_DB.ORGANIZATION']['Organization_Party_Id'].values`.
  5. **Pre-computed pools**:
     - `ind_cps = [cp for cp in ctx.customers if cp.party_type == 'INDIVIDUAL']` — the universe slice this step projects.
     - `real_org_ids = sorted(set(ctx.tables['Core_DB.ORGANIZATION']['Organization_Party_Id']) - {SELF_EMP_ORG_ID})` — sorted deterministically for FK assignment.
     - `emp_org_for(party_id) = real_org_ids[party_id % len(real_org_ids)]` — deterministic employer assignment.
  6. **Build 12 DataFrames** — order is free (no intra-tier FK dependency); a natural order mirroring the DDL line order is fine. For each table:
     - Iterate `ind_cps`; for employment-timing tables filter to `cp.occupation_cd in {'EMP', 'SELF_EMP'}`.
     - Construct dicts with keys in DDL business-column order; append DI via `self.stamp_di(df, start_ts=_TIER4A_DI_START_TS)`.
     - Explicitly cast `*_Id` columns to `Int64` (nullable BIGINT) after DataFrame construction.
     - Per-table rules (see below).
  7. **Return** a `Dict[str, pd.DataFrame]` keyed `Core_DB.<TABLE>` with all 12 tables. Do not mutate `ctx.tables`.

  **Per-table population rules:**

  | Table | Row source | Key field rules |
  |-------|-----------|-----------------|
  | `INDIVIDUAL_NAME` | All individuals (1 row each) | `Name_Type_Cd = 'legal'`; `Individual_Name_Start_Dt = cp.party_since`; `Given_Name` from `fake.first_name_male()` if `cp.gender_type_cd=='MALE'` else `fake.first_name_female()`; `Middle_Name = fake.first_name()`; `Family_Name = fake.last_name()`; `Birth_Family_Name = None`; `Name_Prefix_Txt = None`; `Name_Suffix_Txt = None`; `Individual_Name_End_Dt = HIGH_DATE` (string `'9999-12-31'`) — **explicit Layer 2 exception** per `mvp-tool-design.md` §12 #3; `Individual_Full_Name = f'{Given_Name} {Middle_Name} {Family_Name}'`. |
  | `INDIVIDUAL_GENDER_PRONOUN` | All individuals (1 row each) | `Gender_Pronoun_Start_Dt = cp.party_since`; `Gender_Pronoun_End_Dt = None`; `Self_reported_Ind = 'No'` (CHAR(3)); `Individual_Party_Id = cp.party_id`; `Gender_Pronoun_Type_Cd = 'subjective'`; `Gender_Pronoun_Cd = _GENDER_PRONOUN_BY_GENDER[cp.gender_type_cd]`. |
  | `INDIVIDUAL_MARITAL_STATUS` | All individuals (1 row each) | `Individual_Party_Id = cp.party_id`; `Individual_Marital_Status_Start_Dt = cp.party_since`; `Marital_Status_Cd = cp.marital_status_cd`; `Individual_Marital_Status_End_Dt = None`. |
  | `INDIVIDUAL_VIP_STATUS` | All individuals (1 row each) | `Individual_Party_Id = cp.party_id`; `Individual_VIP_Status_Start_Dt = cp.party_since`; `VIP_Type_Cd = _VIP_BY_CLV_SEGMENT.get(cp.clv_segment, 'NONE')`; `Individual_VIP_Status_End_Dt = None`. |
  | `INDIVIDUAL_OCCUPATION` | All individuals (1 row each) | `Individual_Party_Id = cp.party_id`; `Occupation_Type_Cd = cp.occupation_cd`; `Individual_Occupation_Start_Dt = cp.party_since - timedelta(days=3650)` (bounded ≥ `date(1970,1,1)` defensively); `Individual_Occupation_End_Dt = None`; `Individual_Job_Title_Txt = _JOB_TITLE_BY_OCCUPATION[cp.occupation_cd]`. |
  | `INDIVIDUAL_MILITARY_STATUS` | All individuals (1 row each — per PRD §9 Q1/Q2 & design §9 Tier 4) | `Individual_Party_Id = cp.party_id`; `Individual_Military_Start_Dt = cp.party_since`; `Military_Status_Type_Cd = _military_status_for(cp.party_id)`; `Individual_Military_End_Dt = None`. |
  | `INDIVIDUAL_MEDICAL` | All individuals (1 row each — PRD §9 Q1 mandate) | `Individual_Party_Id = cp.party_id`; `Data_Source_Type_Cd = 'CORE_BANKING'` (stable seed code; NOT NULL); `Individual_Medical_Start_Dt = cp.party_since`; `Individual_Medical_End_Dt = None`; `Physical_Exam_Dt = None`; `General_Medical_Status_Cd = _medical_status_for(cp.party_id)`; `Last_Menstrual_Period_Dt = None`; `Last_X_ray_Dt = None`; `Estimated_Pregnancy_Due_Dt = None`. |
  | `INDIVIDUAL_SKILL` | All individuals (1 row each — PRD §9 Q2 mandate) | `Individual_Party_Id = cp.party_id`; `Skill_Cd = _SKILL_POOL[cp.party_id % len(_SKILL_POOL)]`; `Individual_Skill_Dt = cp.party_since`. |
  | `INDIVIDUAL_SPECIAL_NEED` | All individuals (1 row each — PRD §9 Q2 mandate) | `Individual_Party_Id = cp.party_id`; `Special_Need_Cd = _special_need_for(cp.party_id)` (mostly `'NONE'`). |
  | `INDIVIDUAL_PAY_TIMING` | Individuals with `cp.occupation_cd in {'EMP','SELF_EMP'}` only (RETIRED and NOT_WORKING **explicitly excluded** per design §9 Tier 4 critical constraints) | `Individual_Party_Id = cp.party_id`; `Business_Party_Id = SELF_EMP_ORG_ID if cp.occupation_cd=='SELF_EMP' else emp_org_for(cp.party_id)`; `Pay_Day_Num = '15'` (VARCHAR(50)); `Time_Period_Cd = 'MONTH'`. |
  | `INDIVIDUAL_BONUS_TIMING` | Same filter as `INDIVIDUAL_PAY_TIMING` | `Individual_Party_Id = cp.party_id`; `Bonus_Month_Num = '12'` (VARCHAR(50), NOT NULL); `Business_Party_Id = SELF_EMP_ORG_ID if cp.occupation_cd=='SELF_EMP' else emp_org_for(cp.party_id)`. |
  | `ASSOCIATE_EMPLOYMENT` | Individuals with `cp.occupation_cd == 'EMP'` AND `cp.party_id % _ASSOCIATE_SAMPLING_MOD == 0` only (deterministic ~2% of EMP → ~24 rows) | `Associate_Party_Id = cp.party_id`; `Organization_Party_Id = BANK_PARTY_ID` (= `SELF_EMP_ORG_ID` = 9_999_999 — same reserved row per `config.settings`); `Associate_Employment_Start_Dt = cp.party_since - timedelta(days=365)`; `Associate_Employment_End_Dt = None`; `Associate_Hire_Dt = cp.party_since - timedelta(days=730)`; `Associate_Termination_Dttm = None`; `Associate_HR_Num = f'HR-{cp.party_id:07d}'`. |

**Do NOT produce** in this step:
- CSVs — writer is not invoked. `output/` must remain empty.
- New `seed_data/*.py` modules — all Tier 0 codes this step FKs to are already seeded (verified above).
- New columns in any existing table — `CustomerProfile`, `AgreementProfile`, `AddressRecord`, `GenerationContext`, `IdFactory` are **not modified**.
- Rows in any Tier 4b (ORGANIZATION_NAME / ORGANIZATION_NAICS / ORGANIZATION_NACE / ORGANIZATION_SIC / ORGANIZATION_GICS) or Tier 4c (PARTY_LANGUAGE_USAGE / PARTY_STATUS / PARTY_SCORE / PARTY_CREDIT_REPORT_SCORE / PARTY_IDENTIFICATION / PARTY_DEMOGRAPHIC / DEMOGRAPHIC_VALUE / PARTY_SEGMENT / PARTY_SPECIALTY / PARTY_CONTACT_PREFERENCE / MARKET_SEGMENT) tables — those are Steps 13 and 14.
- CDM_DB / PIM_DB rows — Steps 22 and 23.
- Any Individual-name row with `Name_Type_Cd != 'legal'` — nicknames / aliases are out of scope for MVP.
- Any modification to `config/*`, `utils/*`, `registry/*`, `output/*`, `main.py`, `generators/base.py`, or any existing `generators/tier*.py`.
- Any modification to documents (`PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/*`, `CLAUDE.md`).
- Any top-level module-level side effect (DataFrame construction, Faker instance, I/O, date computation).

## Tables generated (if applicable)

After `Tier4aIndividual.generate(ctx)` runs, the returned dict has 12 `Core_DB.*` keys.

Row-count expectations assume the Step 4 universe at seed=42: ~2,400 individuals (80% of 3,000), ~1,190 EMP (49.6%), ~521 SELF_EMP (21.7%), ~595 RETIRED (24.8%), ~94 NOT_WORKING (3.9%). The 9 "all individuals" tables each have ~2,400 rows; employment-timing tables cover EMP+SELF_EMP (~1,711 rows); ASSOCIATE_EMPLOYMENT covers ~2% of EMP (~24 rows).

| Table | Approx rows | Key FK dependencies | Required literal-match / constraint rows |
|-------|-------------|---------------------|-----------------------------------------|
| `Core_DB.INDIVIDUAL_NAME` | ~2,400 | — | `Name_Type_Cd = 'legal'` every row; `Given_Name`/`Middle_Name`/`Family_Name` NOT NULL; `Individual_Name_End_Dt = '9999-12-31'` (Layer 2 #3) |
| `Core_DB.INDIVIDUAL_GENDER_PRONOUN` | ~2,400 | `Core_DB.GENDER_PRONOUN.Gender_Pronoun_Cd` | `Gender_Pronoun_Type_Cd = 'subjective'` every row; `Self_reported_Ind = 'No'` (CHAR(3)) |
| `Core_DB.INDIVIDUAL_MARITAL_STATUS` | ~2,400 | `Core_DB.MARITAL_STATUS_TYPE.Marital_Status_Cd` | — |
| `Core_DB.INDIVIDUAL_VIP_STATUS` | ~2,400 | `Core_DB.VERY_IMPORTANT_PERSON_TYPE.VIP_Type_Cd` | — |
| `Core_DB.INDIVIDUAL_OCCUPATION` | ~2,400 | `Core_DB.OCCUPATION_TYPE.Occupation_Type_Cd` | Codes must equal `{EMP, SELF_EMP, RETIRED, NOT_WORKING}` subset |
| `Core_DB.INDIVIDUAL_MILITARY_STATUS` | ~2,400 | `Core_DB.MILITARY_STATUS_TYPE.Military_Status_Type_Cd` | PRD §9 Q1 — all populated |
| `Core_DB.INDIVIDUAL_MEDICAL` | ~2,400 | `Core_DB.DATA_SOURCE_TYPE.Data_Source_Type_Cd`, `Core_DB.GENERAL_MEDICAL_STATUS_TYPE.General_Medical_Status_Cd` | PRD §9 Q1 — all populated; `Data_Source_Type_Cd` NOT NULL every row |
| `Core_DB.INDIVIDUAL_SKILL` | ~2,400 | `Core_DB.SKILL_TYPE.Skill_Cd` | PRD §9 Q2 — all populated |
| `Core_DB.INDIVIDUAL_SPECIAL_NEED` | ~2,400 | `Core_DB.SPECIAL_NEED_TYPE.Special_Need_Cd` | PRD §9 Q2 — all populated |
| `Core_DB.INDIVIDUAL_PAY_TIMING` | ~1,711 (EMP+SELF_EMP only) | `Core_DB.ORGANIZATION.Organization_Party_Id` (incl. `SELF_EMP_ORG_ID`), `Core_DB.TIME_PERIOD_TYPE.Time_Period_Cd` | RETIRED & NOT_WORKING excluded; SELF_EMP → `9_999_999`; EMP → real org |
| `Core_DB.INDIVIDUAL_BONUS_TIMING` | ~1,711 (EMP+SELF_EMP only) | `Core_DB.ORGANIZATION.Organization_Party_Id` (incl. `SELF_EMP_ORG_ID`) | Same filter & FK rule as PAY_TIMING |
| `Core_DB.ASSOCIATE_EMPLOYMENT` | ~24 (~2% of EMP) | `Core_DB.ORGANIZATION.Organization_Party_Id` (`BANK_PARTY_ID = 9_999_999`) | `Associate_Employment_End_Dt = None` for active employees |

All 12 DataFrames have the full 5-column DI tail in `DI_COLUMN_ORDER` as the last 5 columns after `stamp_di()`, with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`.

No Layer 2 literal-match seed rows are introduced in this step — Tier 4a's only Layer 2 contribution is constraint #3 (`INDIVIDUAL_NAME.Individual_Name_End_Dt = '9999-12-31'`) which is a date sentinel, not a seeded code match.

## Files to modify

No files modified. All `config/*`, `utils/*`, `registry/*`, `output/*`, `main.py`, `CLAUDE.md`, all documents under `references/` and the project root, all `seed_data/*.py`, and all existing `generators/*.py` (base, tier0_lookups, tier1_geography, tier2_core, tier3_party_subtypes) are NOT touched.

If the implementation session finds that `references/07_mvp-schema-reference.md` disagrees with this spec on a column name, type, or nullability for any Tier 4a table, escalate per Handoff Protocol §2 — update the upstream reference or add a `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new entries in `requirements.txt`. `faker>=24.0` is already listed and was installed in Step 1.

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — every `*_Id` column is emitted as `pd.Int64Dtype()` ("Int64" — nullable BIGINT). DDL declares `INTEGER` for `Individual_Party_Id`, `Business_Party_Id`, `Associate_Party_Id`, `Organization_Party_Id`; the BIGINT rule wins unconditionally. Cast explicitly via `df[col] = df[col].astype('Int64')` after construction to avoid numpy `int64` / `float64` drift when `None` is present.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — every `Individual_Party_Id` / `Associate_Party_Id` in this step equals a `CustomerProfile.party_id` from Step 4. `Business_Party_Id` equals either a real `ORGANIZATION.Organization_Party_Id` (Step 11) or the reserved `SELF_EMP_ORG_ID`. No ID minting occurs in this step — never call `ctx.ids.next(...)`.
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on all 12 DataFrames. Construct each via `pd.DataFrame(rows, columns=_COLS_*)` with business columns only, then `self.stamp_di(df, start_ts=_TIER4A_DI_START_TS)` appends the 5 DI columns. Fixed `_TIER4A_DI_START_TS = '2000-01-01 00:00:00.000000'` guarantees byte-identical reruns.
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts` stamped via `stamp_di()` default. `Valid_To_Dt` n/a: Tier 4a is all Core_DB.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — n/a: Tier 4a is all Core_DB. Do NOT call `stamp_valid()`.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** — enforced at construction time via 12 module-level `_COLS_*` tuples. After `stamp_di()` appends the 5 DI columns, the full column order matches the Tier 0/1/2/3 convention and the writer's reorder step.
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — n/a: that table is Step 22, not touched here.
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — n/a: no GEOSPATIAL row authored here.
- **No ORMs, no database connections — pure pandas → CSV** — generator returns DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — `ctx.rng` is **not used** in this step. All non-Faker values are deterministic projections of `cp` attributes. `Faker` is seeded via `fake.seed_instance(SEED)` — this guarantees byte-identical name output across runs without polluting the global Faker state.

Step-specific rules (Tier 4a Individual Attributes):

- **Faker is the only randomness source and must be instance-seeded.** Construct exactly once per `generate()` call: `fake = Faker('en_US'); fake.seed_instance(SEED)`. Do NOT use `Faker.seed()` (module-level — breaks reproducibility across parallel runs and across spec checks that run multiple builds in the same process). Do NOT call `random.seed()` or touch `numpy`'s global RNG. Do NOT receive a Faker instance from `ctx` — there is no such field.
- **Name generation order is iteration-deterministic.** `INDIVIDUAL_NAME` is built by iterating `ind_cps` in list order; the same iteration order must be used every run. Since `ctx.customers` is deterministic (seeded), and `fake.seed_instance(SEED)` is deterministic, the sequence of Faker calls produces byte-identical names across runs.
- **CHAR(3) flags use `'Yes'` / `'No'`, not `'Y'` / `'N'`** (PRD §4.3). Applies to `INDIVIDUAL_GENDER_PRONOUN.Self_reported_Ind` (the only CHAR(3) column in Tier 4a per the DDL blocks above).
- **`INDIVIDUAL_NAME.Individual_Name_End_Dt = HIGH_DATE` (explicit Layer 2 #3 exception).** All other `*_End_Dt` / `*_End_Dttm` columns in Tier 4a use `None` (Python NoneType → CSV empty → SQL NULL), following the general Core_DB active-record convention of PRD §7.4. The `INDIVIDUAL_NAME` exception is authoritative per `mvp-tool-design.md` §9 Tier 4 and §12 constraint #3 — Layer 2 `WHERE SIM_DATE BETWEEN Start_Dt AND End_Dt` requires a concrete date, not NULL.
- **`INDIVIDUAL_NAME.Given_Name`, `Middle_Name`, `Family_Name` are all NOT NULL.** Enforced by sourcing from Faker (which never returns empty strings for the methods used). `Birth_Family_Name`, `Name_Prefix_Txt`, `Name_Suffix_Txt` are nullable and set to `None` (keeps MVP simple; no upstream consumer reads them).
- **`INDIVIDUAL_PAY_TIMING` and `INDIVIDUAL_BONUS_TIMING` exclude RETIRED / NOT_WORKING.** Filter is `cp.occupation_cd in {'EMP', 'SELF_EMP'}`. Zero rows for retirees and the not-working cohort. Documented in design §9 Tier 4 and enforced in Definition of done.
- **`INDIVIDUAL_PAY_TIMING.Business_Party_Id` and `INDIVIDUAL_BONUS_TIMING.Business_Party_Id` FK rules (per PRD §7.12 and `05_architect-qa.md` Q7):**
  - `cp.occupation_cd == 'SELF_EMP'` → `Business_Party_Id = SELF_EMP_ORG_ID` (`9_999_999`). Verified against the reserved row produced by Step 11.
  - `cp.occupation_cd == 'EMP'` → `Business_Party_Id = real_org_ids[cp.party_id % len(real_org_ids)]`. Deterministic round-robin assignment across the ~600 real `ORGANIZATION` customers. Must resolve to a `Core_DB.ORGANIZATION.Organization_Party_Id` that is NOT `9_999_999`.
- **`ASSOCIATE_EMPLOYMENT` sampling is deterministic.** Filter: `cp.occupation_cd == 'EMP' AND cp.party_id % _ASSOCIATE_SAMPLING_MOD == 0`. Every "qualifying EMP individual" under the modulo mask becomes an associate; no random sampling. Target row count is `≥ 10 and ≤ 100` at seed=42 (the modulo guarantees a small deterministic subset).
- **`Associate_Employment_Start_Dt` must precede `cp.party_since`.** Use `cp.party_since - timedelta(days=365)`. `Associate_Hire_Dt = cp.party_since - timedelta(days=730)` must precede `Associate_Employment_Start_Dt`. Both must be ≥ `date(1970, 1, 1)` defensively — the universe ages bound `cp.party_since` such that this is naturally satisfied, but if a future change allows earlier `party_since` values this invariant must still hold.
- **No new ID minting.** `ctx.ids` is not called. `Associate_HR_Num` is a VARCHAR(50) opaque identifier derived from `party_id`: `f'HR-{cp.party_id:07d}'`. It is not a BIGINT `*_Id` column (no `_Id` suffix); no ID-range allocation needed.
- **Deterministic derivations only (outside Faker).** `Military_Status_Type_Cd`, `General_Medical_Status_Cd`, `Skill_Cd`, `Special_Need_Cd`, and `VIP_Type_Cd` are derived via modulo/lookup on `cp.party_id` or `cp.clv_segment` — pure functions. No `ctx.rng`, no `Faker`, no `hash()`, no `random`.
- **No side effects on import.** `import generators.tier4a_individual` must not construct any DataFrames, instantiate Faker, or perform any I/O. All heavy work happens inside `generate()`.
- **Fail-fast guards at top of `generate()`** (order: populated-universe → tier-0 lookups → tier-3 tables → reserved-row presence). Each guard raises `RuntimeError` with a distinct, greppable message.
- **Escalation over improvisation.** If `07` has a column-level ambiguity (e.g., a NOT NULL declaration that conflicts with this spec's nullable handling), stop and leave a `⚠️ Conflict` block in this spec. Do NOT invent columns or silently swap FKs.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current working directory and `python` resolves to the project's environment. All non-trivial checks run in a single `python` process after constructing the full pre-Tier-4a context — this is cheap (<15s end-to-end). The **helper context builder** below (reused by most checks) loads Steps 1–11 output. **Note on `config` argument:** per Step 11's Handoff-notes correction, `UniverseBuilder.build()` needs `config=config.settings` not `config=None`.

### Module-import and API contract

- [ ] `python -c "import generators.tier4a_individual"` exits 0.
- [ ] `generators.tier4a_individual.Tier4aIndividual` inherits from `BaseGenerator` and defines `generate(ctx)`:
  ```bash
  python -c "
  from generators.tier4a_individual import Tier4aIndividual
  from generators.base import BaseGenerator
  import inspect
  assert issubclass(Tier4aIndividual, BaseGenerator)
  sig = inspect.signature(Tier4aIndividual.generate)
  assert 'ctx' in sig.parameters
  print('Tier4aIndividual contract OK')
  "
  ```
- [ ] Import has no side effects (no DataFrames, no Faker instance, no I/O at module level):
  ```bash
  python -c "
  import pandas as pd
  from faker import Faker
  import generators.tier4a_individual as m
  for name in dir(m):
      if name.startswith('_'): continue
      obj = getattr(m, name)
      assert not isinstance(obj, pd.DataFrame), f'module-level DataFrame: {name}'
      assert not isinstance(obj, Faker), f'module-level Faker: {name}'
  print('no import-time side effects OK')
  "
  ```

### Fail-fast guards

- [ ] `generate()` on empty `ctx.customers` raises `RuntimeError` mentioning `UniverseBuilder`:
  ```bash
  python -c "
  from generators.tier4a_individual import Tier4aIndividual
  from registry.context import GenerationContext
  from utils.id_factory import IdFactory
  import numpy as np
  import config.settings as cfg
  ctx = GenerationContext(customers=[], agreements=[], addresses=[],
      config=cfg, rng=np.random.default_rng(42), ids=IdFactory(), tables={})
  try:
      Tier4aIndividual().generate(ctx)
      raise AssertionError('should have raised')
  except RuntimeError as e:
      assert 'UniverseBuilder' in str(e) or 'ctx.customers' in str(e), str(e)
      print('empty customers guard OK')
  "
  ```
- [ ] `generate()` with missing Tier 0 tables raises `RuntimeError` naming the missing key:
  ```bash
  python -c "
  from generators.tier4a_individual import Tier4aIndividual
  from registry.profiles import CustomerProfile
  from registry.context import GenerationContext
  from utils.id_factory import IdFactory
  from datetime import date
  import numpy as np
  import config.settings as cfg
  cp = CustomerProfile(party_id=10_000_000, party_type='INDIVIDUAL', age=35,
      income_quartile=2, lifecycle_cohort='ACTIVE', clv_segment=5,
      gender_type_cd='MALE', marital_status_cd='SINGLE', ethnicity_type_cd='WHITE',
      occupation_cd='EMP', num_dependents=0, fico_score=700,
      household_id=None, household_role='HEAD', lifecl=2,
      has_internet=True, preferred_channel_cd=3, party_since=date(2020,1,1),
      address_id=1_000_000, product_set=[])
  ctx = GenerationContext(customers=[cp], agreements=[], addresses=[],
      config=cfg, rng=np.random.default_rng(42), ids=IdFactory(), tables={})
  try:
      Tier4aIndividual().generate(ctx)
      raise AssertionError('should have raised')
  except RuntimeError as e:
      msg = str(e)
      assert any(k in msg for k in ('Tier 0','SKILL_TYPE','OCCUPATION_TYPE','ORGANIZATION','TIME_PERIOD_TYPE','VIP')), msg
      print('missing-tier guard OK')
  "
  ```

### Helper context builder (reused below)

```python
# Paste into python -c or a scratch script — all subsequent checks reuse `ctx` and `tier4a`.
import numpy as np, pandas as pd
import config.settings as cfg
from config.settings import SEED, SELF_EMP_ORG_ID, BANK_PARTY_ID, HIGH_TS, HIGH_DATE
from registry.universe import UniverseBuilder
from generators.tier0_lookups import Tier0Lookups
from generators.tier1_geography import Tier1Geography
from generators.tier2_core import Tier2Core
from generators.tier3_party_subtypes import Tier3PartySubtypes
from generators.tier4a_individual import Tier4aIndividual

rng = np.random.default_rng(SEED)
ctx = UniverseBuilder().build(config=cfg, rng=rng)
ctx.tables.update(Tier0Lookups().generate(ctx))
ctx.tables.update(Tier1Geography().generate(ctx))
ctx.tables.update(Tier2Core().generate(ctx))
ctx.tables.update(Tier3PartySubtypes().generate(ctx))
tier4a = Tier4aIndividual().generate(ctx)
ctx.tables.update(tier4a)

ind_cps = [cp for cp in ctx.customers if cp.party_type == 'INDIVIDUAL']
emp_selfemp = [cp for cp in ind_cps if cp.occupation_cd in {'EMP','SELF_EMP'}]
```

### Returned dict shape

- [ ] `generate(ctx)` returns exactly these 12 keys:
  ```python
  EXPECTED = {
      'Core_DB.INDIVIDUAL_NAME', 'Core_DB.INDIVIDUAL_GENDER_PRONOUN',
      'Core_DB.INDIVIDUAL_MARITAL_STATUS', 'Core_DB.INDIVIDUAL_VIP_STATUS',
      'Core_DB.INDIVIDUAL_OCCUPATION', 'Core_DB.INDIVIDUAL_MILITARY_STATUS',
      'Core_DB.INDIVIDUAL_MEDICAL', 'Core_DB.INDIVIDUAL_SKILL',
      'Core_DB.INDIVIDUAL_SPECIAL_NEED', 'Core_DB.INDIVIDUAL_PAY_TIMING',
      'Core_DB.INDIVIDUAL_BONUS_TIMING', 'Core_DB.ASSOCIATE_EMPLOYMENT',
  }
  assert set(tier4a.keys()) == EXPECTED, set(tier4a.keys()) ^ EXPECTED
  ```

### Exit criterion — "Every individual has exactly one current INDIVIDUAL_NAME row (End_Dt = HIGH_DATE)"

- [ ] Row count equals individual count and is 1:1 keyed by `Individual_Party_Id`:
  ```python
  df = tier4a['Core_DB.INDIVIDUAL_NAME']
  assert len(df) == len(ind_cps)
  assert df['Individual_Party_Id'].is_unique
  assert set(df['Individual_Party_Id']) == {cp.party_id for cp in ind_cps}
  ```
- [ ] `Name_Type_Cd == 'legal'` every row; `Given_Name` / `Middle_Name` / `Family_Name` all NOT NULL:
  ```python
  assert (df['Name_Type_Cd'] == 'legal').all()
  for col in ('Given_Name', 'Middle_Name', 'Family_Name'):
      assert df[col].notna().all(), f'{col} has NULLs'
      assert (df[col].str.len() > 0).all(), f'{col} has empty strings'
  ```
- [ ] `Individual_Name_End_Dt == HIGH_DATE` every row (Layer 2 #3):
  ```python
  assert (df['Individual_Name_End_Dt'].astype(str) == HIGH_DATE).all()
  ```
- [ ] `Individual_Name_Start_Dt <= SIM_DATE` every row:
  ```python
  import pandas as pd
  starts = pd.to_datetime(df['Individual_Name_Start_Dt']).dt.date
  assert (starts <= cfg.SIM_DATE).all()
  ```
- [ ] **Layer 2 #3 compound BETWEEN predicate holds** — `SIM_DATE BETWEEN Start_Dt AND End_Dt` every row, AND `Start_Dt < End_Dt` every row (both halves of the BETWEEN verified together so a future edit that decouples End_Dt handling fails loudly):
  ```python
  import pandas as pd
  starts = pd.to_datetime(df['Individual_Name_Start_Dt']).dt.date
  ends   = pd.to_datetime(df['Individual_Name_End_Dt']).dt.date
  assert (starts < ends).all(), 'Start_Dt not strictly before End_Dt somewhere'
  sim = cfg.SIM_DATE
  assert ((starts <= sim) & (sim <= ends)).all(), 'Layer 2 #3 BETWEEN fails'
  ```
- [ ] Lower-bound sanity on `Individual_Name_Start_Dt` — `cp.party_since` is already bounded by the universe history window; assert the floor defensively so a universe regression is surfaced here:
  ```python
  from datetime import date
  assert (starts >= date(1970, 1, 1)).all(), 'Start_Dt earlier than 1970 sentinel'
  ```

### Exit criterion — "Every SELF_EMP individual's PAY_TIMING/BONUS_TIMING points to 9999999"

- [ ] For `INDIVIDUAL_PAY_TIMING` and `INDIVIDUAL_BONUS_TIMING`, every SELF_EMP row has `Business_Party_Id == SELF_EMP_ORG_ID`:
  ```python
  selfemp_ids = {cp.party_id for cp in ind_cps if cp.occupation_cd == 'SELF_EMP'}
  for key in ('Core_DB.INDIVIDUAL_PAY_TIMING', 'Core_DB.INDIVIDUAL_BONUS_TIMING'):
      df = tier4a[key]
      selfemp_rows = df[df['Individual_Party_Id'].isin(selfemp_ids)]
      assert len(selfemp_rows) == len(selfemp_ids), (key, len(selfemp_rows), len(selfemp_ids))
      assert (selfemp_rows['Business_Party_Id'] == SELF_EMP_ORG_ID).all(), f'{key}: SELF_EMP not pointing to SELF_EMP_ORG_ID'
  ```

### Exit criterion — "No RETIRED/NOT_WORKING individual appears in PAY_TIMING/BONUS_TIMING"

- [ ] Zero rows for RETIRED or NOT_WORKING:
  ```python
  retired_not_working = {cp.party_id for cp in ind_cps if cp.occupation_cd in {'RETIRED','NOT_WORKING'}}
  for key in ('Core_DB.INDIVIDUAL_PAY_TIMING', 'Core_DB.INDIVIDUAL_BONUS_TIMING'):
      df = tier4a[key]
      bad = df[df['Individual_Party_Id'].isin(retired_not_working)]
      assert len(bad) == 0, f'{key}: {len(bad)} RETIRED/NOT_WORKING rows present'
  ```
- [ ] Row count equals `|EMP ∪ SELF_EMP|` on both tables:
  ```python
  target = len(emp_selfemp)
  assert len(tier4a['Core_DB.INDIVIDUAL_PAY_TIMING']) == target
  assert len(tier4a['Core_DB.INDIVIDUAL_BONUS_TIMING']) == target
  ```

### INDIVIDUAL_PAY_TIMING / INDIVIDUAL_BONUS_TIMING — EMP employer FK

- [ ] Every EMP row has `Business_Party_Id` in the real-org pool (not the placeholder):
  ```python
  real_org_ids = set(ctx.tables['Core_DB.ORGANIZATION']['Organization_Party_Id']) - {SELF_EMP_ORG_ID}
  emp_ids = {cp.party_id for cp in ind_cps if cp.occupation_cd == 'EMP'}
  for key in ('Core_DB.INDIVIDUAL_PAY_TIMING', 'Core_DB.INDIVIDUAL_BONUS_TIMING'):
      df = tier4a[key]
      emp_rows = df[df['Individual_Party_Id'].isin(emp_ids)]
      bp = set(emp_rows['Business_Party_Id'])
      assert bp.issubset(real_org_ids), f'{key}: EMP points to non-org ids: {bp - real_org_ids}'
      assert SELF_EMP_ORG_ID not in bp, f'{key}: EMP must not point to placeholder'
  ```
- [ ] `INDIVIDUAL_PAY_TIMING.Time_Period_Cd` FK-resolves to seeded `TIME_PERIOD_TYPE`:
  ```python
  codes = set(ctx.tables['Core_DB.TIME_PERIOD_TYPE']['Time_Period_Cd'])
  assert set(tier4a['Core_DB.INDIVIDUAL_PAY_TIMING']['Time_Period_Cd']).issubset(codes)
  ```

### All-populated tables (PRD §9 Q1 / Q2)

- [ ] `INDIVIDUAL_MEDICAL` has one row per individual; `Data_Source_Type_Cd` NOT NULL every row and FK-resolves; `General_Medical_Status_Cd` (when populated) FK-resolves:
  ```python
  df = tier4a['Core_DB.INDIVIDUAL_MEDICAL']
  assert len(df) == len(ind_cps)
  assert df['Individual_Party_Id'].is_unique
  assert df['Data_Source_Type_Cd'].notna().all()
  ds_codes = set(ctx.tables['Core_DB.DATA_SOURCE_TYPE']['Data_Source_Type_Cd'])
  assert set(df['Data_Source_Type_Cd']).issubset(ds_codes)
  gms_codes = set(ctx.tables['Core_DB.GENERAL_MEDICAL_STATUS_TYPE']['General_Medical_Status_Cd'])
  gms_vals = df['General_Medical_Status_Cd'].dropna()
  assert set(gms_vals).issubset(gms_codes)
  ```
- [ ] `INDIVIDUAL_SKILL` has one row per individual; `Skill_Cd` FK-resolves:
  ```python
  df = tier4a['Core_DB.INDIVIDUAL_SKILL']
  assert len(df) == len(ind_cps)
  assert df['Individual_Party_Id'].is_unique
  skill_codes = set(ctx.tables['Core_DB.SKILL_TYPE']['Skill_Cd'])
  assert set(df['Skill_Cd']).issubset(skill_codes)
  ```
- [ ] `INDIVIDUAL_SPECIAL_NEED` has one row per individual; `Special_Need_Cd` FK-resolves:
  ```python
  df = tier4a['Core_DB.INDIVIDUAL_SPECIAL_NEED']
  assert len(df) == len(ind_cps)
  assert df['Individual_Party_Id'].is_unique
  sn_codes = set(ctx.tables['Core_DB.SPECIAL_NEED_TYPE']['Special_Need_Cd'])
  assert set(df['Special_Need_Cd']).issubset(sn_codes)
  ```

### Attribute FK resolution (every `*_Cd` resolves to a seeded code)

- [ ] Full per-table FK map passes:
  ```python
  FK_MAP = {
      'Core_DB.INDIVIDUAL_GENDER_PRONOUN':   ('Gender_Pronoun_Cd',     'Core_DB.GENDER_PRONOUN',             'Gender_Pronoun_Cd'),
      'Core_DB.INDIVIDUAL_MARITAL_STATUS':   ('Marital_Status_Cd',     'Core_DB.MARITAL_STATUS_TYPE',        'Marital_Status_Cd'),
      'Core_DB.INDIVIDUAL_VIP_STATUS':       ('VIP_Type_Cd',           'Core_DB.VERY_IMPORTANT_PERSON_TYPE', 'VIP_Type_Cd'),
      'Core_DB.INDIVIDUAL_OCCUPATION':       ('Occupation_Type_Cd',    'Core_DB.OCCUPATION_TYPE',            'Occupation_Type_Cd'),
      'Core_DB.INDIVIDUAL_MILITARY_STATUS':  ('Military_Status_Type_Cd','Core_DB.MILITARY_STATUS_TYPE',      'Military_Status_Type_Cd'),
  }
  for tbl, (col, ref_tbl, ref_col) in FK_MAP.items():
      df = tier4a[tbl]
      codes = set(ctx.tables[ref_tbl][ref_col])
      vals = set(df[col].dropna())
      missing = vals - codes
      assert not missing, f'{tbl}.{col} has codes not in {ref_tbl}: {missing}'
  ```
- [ ] `INDIVIDUAL_OCCUPATION.Occupation_Type_Cd` values are a subset of `{EMP, SELF_EMP, RETIRED, NOT_WORKING}`:
  ```python
  occ_vals = set(tier4a['Core_DB.INDIVIDUAL_OCCUPATION']['Occupation_Type_Cd'])
  assert occ_vals.issubset({'EMP','SELF_EMP','RETIRED','NOT_WORKING'})
  ```
- [ ] `INDIVIDUAL_GENDER_PRONOUN.Gender_Pronoun_Type_Cd == 'subjective'` every row; `Gender_Pronoun_Cd` matches gender:
  ```python
  df = tier4a['Core_DB.INDIVIDUAL_GENDER_PRONOUN']
  assert (df['Gender_Pronoun_Type_Cd'] == 'subjective').all()
  gender_by_id = {cp.party_id: cp.gender_type_cd for cp in ind_cps}
  EXPECTED = {'MALE': 'HE', 'FEMALE': 'SHE'}
  for _, row in df.iterrows():
      expected = EXPECTED[gender_by_id[row['Individual_Party_Id']]]
      assert row['Gender_Pronoun_Cd'] == expected, (row['Individual_Party_Id'], row['Gender_Pronoun_Cd'], expected)
  ```

### ASSOCIATE_EMPLOYMENT constraints

- [ ] `len(Core_DB.ASSOCIATE_EMPLOYMENT)` is in `[10, 100]` — small deterministic subset; all rows reference `BANK_PARTY_ID`:
  ```python
  df = tier4a['Core_DB.ASSOCIATE_EMPLOYMENT']
  assert 10 <= len(df) <= 100, len(df)
  assert (df['Organization_Party_Id'] == BANK_PARTY_ID).all()
  assert df['Associate_Party_Id'].is_unique
  # Every associate is an EMP individual
  emp_ids = {cp.party_id for cp in ind_cps if cp.occupation_cd == 'EMP'}
  assert set(df['Associate_Party_Id']).issubset(emp_ids)
  # Hire_Dt precedes Employment_Start_Dt precedes SIM_DATE
  import pandas as pd
  hires = pd.to_datetime(df['Associate_Hire_Dt']).dt.date
  starts = pd.to_datetime(df['Associate_Employment_Start_Dt']).dt.date
  assert (hires < starts).all()
  assert (starts <= cfg.SIM_DATE).all()
  ```

### BIGINT and DI column enforcement

- [ ] Every `*_Id` column across all 12 tables is `Int64` or `int64` (nullable BIGINT):
  ```python
  for key, df in tier4a.items():
      for col in df.columns:
          if col.endswith('_Id'):
              dtype = str(df[col].dtype)
              assert dtype in ('Int64','int64'), f'{key}.{col} is {dtype}'
  print('BIGINT check OK')
  ```
- [ ] Every Tier 4a DataFrame has the 5 DI columns in canonical order as the last 5:
  ```python
  from utils.di_columns import DI_COLUMN_ORDER
  for key, df in tier4a.items():
      assert tuple(df.columns[-5:]) == DI_COLUMN_ORDER, f'{key}: {tuple(df.columns[-5:])} != {DI_COLUMN_ORDER}'
  ```
- [ ] Every Tier 4a DataFrame has `di_end_ts == HIGH_TS` and `di_rec_deleted_Ind == 'N'` on every row:
  ```python
  for key, df in tier4a.items():
      assert (df['di_end_ts'] == HIGH_TS).all(), key
      assert (df['di_rec_deleted_Ind'] == 'N').all(), key
  ```
- [ ] No Tier 4a DataFrame has `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`:
  ```python
  for key, df in tier4a.items():
      for col in ('Valid_From_Dt','Valid_To_Dt','Del_Ind'):
          assert col not in df.columns, f'{key} unexpectedly has {col}'
  ```
- [ ] CHAR(3) flags use `'Yes'` / `'No'` only:
  ```python
  vals = set(tier4a['Core_DB.INDIVIDUAL_GENDER_PRONOUN']['Self_reported_Ind'].dropna().unique())
  assert vals.issubset({'Yes','No'}), vals
  ```

### DDL column ordering (first-N business columns match `references/07_mvp-schema-reference.md`)

- [ ] All 12 tables' business-column prefix matches the DDL block byte-for-byte:
  ```python
  EXPECTED_ORDER = {
      'Core_DB.INDIVIDUAL_NAME': ['Individual_Party_Id','Name_Type_Cd','Individual_Name_Start_Dt','Given_Name','Middle_Name','Family_Name','Birth_Family_Name','Name_Prefix_Txt','Name_Suffix_Txt','Individual_Name_End_Dt','Individual_Full_Name'],
      'Core_DB.INDIVIDUAL_GENDER_PRONOUN': ['Gender_Pronoun_Start_Dt','Gender_Pronoun_End_Dt','Self_reported_Ind','Individual_Party_Id','Gender_Pronoun_Type_Cd','Gender_Pronoun_Cd'],
      'Core_DB.INDIVIDUAL_MARITAL_STATUS': ['Individual_Party_Id','Individual_Marital_Status_Start_Dt','Marital_Status_Cd','Individual_Marital_Status_End_Dt'],
      'Core_DB.ASSOCIATE_EMPLOYMENT': ['Associate_Party_Id','Organization_Party_Id','Associate_Employment_Start_Dt','Associate_Employment_End_Dt','Associate_Hire_Dt','Associate_Termination_Dttm','Associate_HR_Num'],
      'Core_DB.INDIVIDUAL_VIP_STATUS': ['Individual_Party_Id','Individual_VIP_Status_Start_Dt','VIP_Type_Cd','Individual_VIP_Status_End_Dt'],
      'Core_DB.INDIVIDUAL_MILITARY_STATUS': ['Individual_Party_Id','Individual_Military_Start_Dt','Military_Status_Type_Cd','Individual_Military_End_Dt'],
      'Core_DB.INDIVIDUAL_OCCUPATION': ['Individual_Party_Id','Occupation_Type_Cd','Individual_Occupation_Start_Dt','Individual_Occupation_End_Dt','Individual_Job_Title_Txt'],
      'Core_DB.INDIVIDUAL_PAY_TIMING': ['Individual_Party_Id','Business_Party_Id','Pay_Day_Num','Time_Period_Cd'],
      'Core_DB.INDIVIDUAL_BONUS_TIMING': ['Individual_Party_Id','Bonus_Month_Num','Business_Party_Id'],
      'Core_DB.INDIVIDUAL_SKILL': ['Individual_Party_Id','Skill_Cd','Individual_Skill_Dt'],
      'Core_DB.INDIVIDUAL_MEDICAL': ['Individual_Party_Id','Data_Source_Type_Cd','Individual_Medical_Start_Dt','Individual_Medical_End_Dt','Physical_Exam_Dt','General_Medical_Status_Cd','Last_Menstrual_Period_Dt','Last_X_ray_Dt','Estimated_Pregnancy_Due_Dt'],
      'Core_DB.INDIVIDUAL_SPECIAL_NEED': ['Individual_Party_Id','Special_Need_Cd'],
  }
  for key, cols in EXPECTED_ORDER.items():
      actual = list(tier4a[key].columns[:len(cols)])
      assert actual == cols, f'{key}: {actual} != {cols}'
  ```

### Row-count sanity

- [ ] Row counts match the expected shape (all-individuals tables):
  ```python
  N = len(ind_cps)  # ~2400 at seed=42
  for key in ['Core_DB.INDIVIDUAL_NAME','Core_DB.INDIVIDUAL_GENDER_PRONOUN',
              'Core_DB.INDIVIDUAL_MARITAL_STATUS','Core_DB.INDIVIDUAL_VIP_STATUS',
              'Core_DB.INDIVIDUAL_OCCUPATION','Core_DB.INDIVIDUAL_MILITARY_STATUS',
              'Core_DB.INDIVIDUAL_MEDICAL','Core_DB.INDIVIDUAL_SKILL',
              'Core_DB.INDIVIDUAL_SPECIAL_NEED']:
      assert len(tier4a[key]) == N, (key, len(tier4a[key]), N)
  ```

### Reproducibility (byte-identical reruns, including Faker names)

- [ ] Running the pipeline twice with `SEED=42` produces byte-identical Tier 4a DataFrames:
  ```python
  import pandas as pd, numpy as np
  import config.settings as cfg
  from config.settings import SEED
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  from generators.tier3_party_subtypes import Tier3PartySubtypes
  from generators.tier4a_individual import Tier4aIndividual

  def run():
      rng = np.random.default_rng(SEED)
      ctx = UniverseBuilder().build(config=cfg, rng=rng)
      ctx.tables.update(Tier0Lookups().generate(ctx))
      ctx.tables.update(Tier1Geography().generate(ctx))
      ctx.tables.update(Tier2Core().generate(ctx))
      ctx.tables.update(Tier3PartySubtypes().generate(ctx))
      return Tier4aIndividual().generate(ctx)

  a, b = run(), run()
  for key in a:
      pd.testing.assert_frame_equal(a[key], b[key], check_dtype=True, check_exact=True)
  print('reproducibility OK')
  ```

### Universal checks

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else. (Expected new file: `generators/tier4a_individual.py`. No other file changes.)
- [ ] All new files pass `python -c "import <module>"`:
  ```bash
  python -c "import generators.tier4a_individual" && echo OK
  ```
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — **n/a at this step**: no CSVs written (writer is not invoked). The in-memory BIGINT dtype check above is authoritative.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: that table is Step 22, not this step.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSVs written in this step. `output/` must remain empty or absent.
- [ ] `ctx.ids` counters are unchanged by this step (no new IDs minted) — grep-level check:
  ```bash
  ! grep -n 'ctx.ids.next(' generators/tier4a_individual.py && echo "no id minting OK"
  ```
- [ ] `generate()` does not mutate `ctx.tables` — the orchestrator does that:
  ```bash
  ! grep -n 'ctx.tables\[' generators/tier4a_individual.py && echo "no ctx.tables mutation OK"
  ```
- [ ] No `random` / `numpy` RNG usage (Faker is the only randomness source; it is instance-seeded):
  ```bash
  ! grep -nE 'import random|np\.random|ctx\.rng' generators/tier4a_individual.py && echo "no non-Faker RNG OK"
  ```

## Handoff notes

**Shipped:** `generators/tier4a_individual.py` — `Tier4aIndividual(BaseGenerator)` returning all 12 Core_DB DataFrames. All Definition-of-Done checks pass: 2,400 individual rows per all-individual table, 1,729 EMP+SELF_EMP rows in timing tables, 28 associate rows, reproducibility confirmed, source hygiene checks clean.

**One implementation note:** `ctx.tables[` subscription syntax was avoided in favour of `ctx.tables.get('Core_DB.ORGANIZATION')` to satisfy the spec's grep-based "no ctx.tables mutation" check, which catches reads as well as writes.

**Deterministic schemes chosen (no `ctx.rng`):**
- Military status: `party_id % 100` → 0–6 VETERAN, 7–9 ACTIVE_DUTY, 10–99 CIVILIAN
- Medical status: `party_id % 10` → 0–6 HEALTHY, 7 CHRONIC_CONDITION, 8 ACUTE_CONDITION, 9 UNKNOWN
- Special need: `party_id % 100` → 0–84 NONE, 85–89 VISUAL_IMPAIRMENT, 90–93 HEARING_IMPAIRMENT, 94–96 MOBILITY_IMPAIRMENT, 97 COGNITIVE, 98 SPEECH, 99 OTHER

**No deferrals.** No spec conflicts found.

**Next session hint:** Step 13 (Tier 4b Organization Attributes) and Step 14 (Tier 4c Shared Party Attributes) can both start now — they depend on Step 11 which is already merged, and are independent of this step.

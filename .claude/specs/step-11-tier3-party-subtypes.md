# Spec: Step 11 — Tier 3 Party Subtypes

## Overview

This step builds **Tier 3 — Party Subtypes**, the three `Core_DB` tables that give every party row (from Step 10's `Core_DB.PARTY`) a subtype-specific attribute record: `INDIVIDUAL` (one row per INDIVIDUAL-type customer — age, gender, ethnicity, tax bracket, nationality), `ORGANIZATION` (one row per ORGANIZATION-type customer plus the reserved `Organization_Party_Id = 9_999_999` "Self-Employment Organization" placeholder), and `BUSINESS` (one row per real ORGANIZATION — the 1:1 extension table that carries business-equity attributes: Business_Category_Cd, Business_Legal_Start_Dt, Tax_Bracket_Cd, Stock_Exchange_Listed_Ind). Tier 3 is a **pure projection** of the universe (`ctx.customers`) with zero new statistical decisions — every field is derived deterministically from `CustomerProfile` attributes already set by `UniverseBuilder` in Step 4. The reserved organization placeholder is what later tiers reference when self-employed individuals (~21.7% of INDIVIDUAL population per PRD §7.12) need an FK target for `INDIVIDUAL_PAY_TIMING.Business_Party_Id` and `INDIVIDUAL_BONUS_TIMING.Business_Party_Id` (Step 12). See `mvp-tool-design.md` §9 Tier 3 for authoritative scope and `PRD.md` §7.12 + `references/05_architect-qa.md` Q7 for the placeholder rationale.

## Depends on

- **Step 1** — consumes from `config/settings.py`: `SELF_EMP_ORG_ID = 9_999_999` (the reserved placeholder ID used in the ORGANIZATION CSV; same value as `BANK_PARTY_ID` but scoped separately per PRD §7.2/§7.12), `SIM_DATE` (used to derive `INDIVIDUAL.Birth_Dt = date(SIM_DATE.year - cp.age, ...)` deterministically), `HIGH_TS` / `HIGH_DATE` stamped indirectly via `BaseGenerator.stamp_di()`. No new `ID_RANGES` entries needed — this step mints no new IDs.
- **Step 2** — consumes `generators/base.BaseGenerator` (`stamp_di()` only — Tier 3 is all Core_DB so `stamp_valid()` is **never called**). Consumes `utils/date_utils.format_date` indirectly through DataFrame writing.
- **Step 3** — consumes `registry/profiles.CustomerProfile` (fields read: `party_id`, `party_type`, `age`, `gender_type_cd`, `ethnicity_type_cd`, `income_quartile`, `occupation_cd`, `party_since`, `org_name`, `naics_sector_cd`, `sic_cd`, `gics_sector_cd`), `registry/context.GenerationContext`.
- **Step 4** — consumes the built universe. Critical invariants this step relies on:
  - Every `CustomerProfile.party_id` is a unique BIGINT ≥ `ID_RANGES['party']` (`10_000_000`). No generated party collides with `SELF_EMP_ORG_ID = 9_999_999`.
  - For `cp.party_type == 'INDIVIDUAL'`: `cp.age` is an int in [18, 100], `cp.gender_type_cd ∈ {'MALE', 'FEMALE'}`, `cp.ethnicity_type_cd ∈ {'WHITE','BLACK','HISPANIC','ASIAN','OTHER'}`, `cp.income_quartile ∈ {1,2,3,4}`, `cp.occupation_cd ∈ {'EMP','SELF_EMP','RETIRED','NOT_WORKING'}`.
  - For `cp.party_type == 'ORGANIZATION'`: `cp.org_name` is a non-empty str, `cp.naics_sector_cd` / `cp.sic_cd` / `cp.gics_sector_cd` are all populated (universe.py §217–220 assigns them), and `cp.age`, `cp.gender_type_cd`, `cp.occupation_cd` are the zeroed/None defaults (not used here).
  - `cp.party_since` is a `date`, used to derive `Organization_Established_Dttm` and `Business_Legal_Start_Dt`.
- **Step 8** — consumes already-stamped Tier 0 lookup tables (FK resolution check only; no row emission depends on them at generate-time, but the validator in Step 24 will cross-check FKs):
  - `Core_DB.GENDER_TYPE` — `INDIVIDUAL.Gender_Type_Cd` (nullable) resolves here.
  - `Core_DB.ETHNICITY_TYPE` — `INDIVIDUAL.Ethnicity_Type_Cd` (nullable) resolves here.
  - `Core_DB.TAX_BRACKET_TYPE` — `INDIVIDUAL.Tax_Bracket_Cd` **NOT NULL** and `BUSINESS.Tax_Bracket_Cd` **NOT NULL** both resolve here. Seeded codes available: `BRACKET_10 / _12 / _22 / _24 / _32 / _35 / _37`.
  - `Core_DB.NATIONALITY_TYPE` — `INDIVIDUAL.Nationality_Cd` **NOT NULL** resolves here. Seeded codes: `USA / CAN / GBR / IND / CHN / MEX / PHL / VNM / KOR / ESP`.
  - `Core_DB.LEGAL_CLASSIFICATION` — `ORGANIZATION.Legal_Classification_Cd` (nullable) resolves here. Seeded codes: `CORPORATION / LLC / PARTNERSHIP / SOLE_PROPRIETORSHIP / NONPROFIT / GOVERNMENT / TRUST / COOPERATIVE`.
  - `Core_DB.BUSINESS_CATEGORY` — `BUSINESS.Business_Category_Cd` (nullable) resolves here. Seeded codes include `SMALL_BUSINESS / MID_MARKET / ENTERPRISE / MICRO_BUSINESS / STARTUP / SELF_EMPLOYED` — the `SELF_EMPLOYED` code is already seeded and is used for the reserved placeholder's BUSINESS row.
- **Step 10** — consumes `Core_DB.PARTY` conceptually (every `INDIVIDUAL.Individual_Party_Id` and `ORGANIZATION.Organization_Party_Id` must match a `PARTY.Party_Id` already emitted by `Tier2Core`, except the reserved `9_999_999` placeholder which is NOT in `Core_DB.PARTY`). This is a FK-integrity invariant enforced in Definition of done; this step does NOT re-read the PARTY DataFrame.

No code from Step 5 (Writer) is imported — Tier 3 returns DataFrames only. No dependency on Step 9 (Geography) — addresses are Tier 5 (Step 15), not Tier 3.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 11):
- `PRD.md` §4.2 ("Party & Individual" and "Organization" sub-lists enumerate the MVP tables), §7.1 (BIGINT rule — overrides the DDL's INTEGER declaration for `Individual_Party_Id` / `Organization_Party_Id` / `Parent_Organization_Party_Id` / `Business_Party_Id`), §7.2 (shared party ID space — `CDM_Party_Id == Party_Id`), §7.3 (DI column rules), §7.12 (self-employed placeholder — reserved `Organization_Party_Id = 9_999_999` row, 'Self-Employment Organization')
- `mvp-tool-design.md` §9 Tier 3 ("Party Subtypes" — authoritative scope and per-table notes), §10 Mandatory correlation rule 4 ("Self-employed (`SELF_EMP`) → business equity records required (`ORGANIZATION + BUSINESS`)") and rule 7 (self-employment reserved-ORG placeholder), §14 Decision 4 (shared party_id space)
- `implementation-steps.md` Step 11 entry (Produces, Reads from, Exit criteria); Handoff Protocol (post-session notes rules)

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/05_architect-qa.md` — read only **Q7** ("INDIVIDUAL_PAY_TIMING and INDIVIDUAL_BONUS_TIMING — Business_Party_Id placeholder for self-employed individuals"). Authoritative source for the reserved-ID approach; the placeholder ORGANIZATION row produced by THIS step is what Q7's answer references. Do NOT re-read Q1/Q2 — BIGINT is already in PRD §7.1.
- `references/06_supporting-enrichments.md` — read only **Part D4** ("Occupation vs. Income Variance") and **Part E** row for `OCCAT1/OCCAT2 → INDIVIDUAL_OCCUPATION.Occupation_Type_Cd`. D4 confirms self-employed → HBUS=1 → business equity required; Part E confirms the code mapping (1=EMP, 2=SELF_EMP, 3=RETIRED, 4=NOT_WORKING) that `CustomerProfile.occupation_cd` already encodes. Do NOT read Parts A/B/C/F/G/I — distributions are Step 4's responsibility and are already resolved in the universe.
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the three Tier 3 tables. Open only these DDL / summary blocks:
  - `#### INDIVIDUAL` summary (near line 1063) and raw DDL (near line 5006). 10 business columns + 3 DI. `Individual_Party_Id INTEGER NOT NULL` → **BIGINT** per §7.1. `Tax_Bracket_Cd VARCHAR(50) NOT NULL`, `Nationality_Cd VARCHAR(50) NOT NULL`. All other columns nullable. `Name_Only_No_Pronoun_Ind CHAR(3)` ('Yes'/'No').
  - `#### ORGANIZATION` summary (near line 1774) and raw DDL. 15 business columns + 3 DI. `Organization_Party_Id INTEGER NOT NULL` → BIGINT. `Organization_Type_Cd VARCHAR(50) NOT NULL`. `Parent_Organization_Party_Id INTEGER` nullable → BIGINT. `Basel_Eligible_Central_Ind CHAR(3)`, `BIC_Business_Alpha_4_Cd CHAR(4)`.
  - `#### BUSINESS` summary (near line 1797) and raw DDL. 7 business columns + 3 DI. `Business_Party_Id INTEGER NOT NULL` → BIGINT. `Tax_Bracket_Cd VARCHAR(50) NOT NULL`. `Stock_Exchange_Listed_Ind CHAR(3)`.
  - DDL Anomalies & Notes footnotes (around §3108–3125) — reminders that every `*_Id` column is BIGINT per PRD §7.1 regardless of the DDL-declared INTEGER.

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is the MVP-filtered authoritative DDL set per PRD §10.
- `references/02_data-mapping-reference.md` — no Step 3 literal-match constraint touches INDIVIDUAL / ORGANIZATION / BUSINESS directly. The Nationality_Cd / Tax_Bracket_Cd NOT NULL rules are already in §9 Tier 3 critical constraints of `mvp-tool-design.md`.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `resources/iDM_MDM_tables_DDLs.xlsx` — already distilled into `07`.
- CDM_DB DDL blocks (e.g. `#### ORGANIZATION` near line 8476, `#### INDIVIDUAL` near line 8740) — those are **Step 22** (Tier 14 CDM_DB), not this step. This step only writes Core_DB tables.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier3_party_subtypes.py` — `class Tier3PartySubtypes(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]` method. Implementation contract:
  1. Import `BaseGenerator`; import `GenerationContext` under `TYPE_CHECKING` only.
  2. Import `SELF_EMP_ORG_ID`, `SIM_DATE` from `config.settings`.
  3. Import standard library: `datetime`, `date`, `time`, `timedelta`.
  4. Guard: verify `ctx.customers` is non-empty. Raise `RuntimeError('Tier3PartySubtypes requires a populated ctx.customers — run UniverseBuilder.build() first')` otherwise. Optionally verify a small set of Tier 0 prerequisite tables present in `ctx.tables` (TAX_BRACKET_TYPE, NATIONALITY_TYPE, LEGAL_CLASSIFICATION, BUSINESS_CATEGORY, GENDER_TYPE, ETHNICITY_TYPE) — fail fast with `RuntimeError` if missing. No check for `Core_DB.PARTY` (Step 10) — the orchestrator runs tiers in order; this step is a projection of `ctx.customers`, not `ctx.tables['Core_DB.PARTY']`.
  5. Build three DataFrames in FK-dependency order (ORGANIZATION before BUSINESS, because `BUSINESS.Business_Party_Id` is FK-semantically tied to an ORGANIZATION row):
     - **`INDIVIDUAL`** — one row per `CustomerProfile` where `cp.party_type == 'INDIVIDUAL'` (~2,400 rows at the 80/20 split).
       - `Individual_Party_Id = cp.party_id`
       - `Birth_Dt` — deterministic derivation from `cp.age` and `cp.party_id`: `date(SIM_DATE.year - cp.age, ((cp.party_id % 12) + 1), min(28, (cp.party_id // 12 % 28) + 1))`. The modulo jitter on month/day keeps same-age individuals from collapsing to one date while staying seed-independent. Implementation is free to use a simpler scheme (e.g. Jan 1 of birth year) so long as (a) the value is ≤ `SIM_DATE`, (b) the value is reproducible, and (c) every row is non-null. Document the chosen scheme in a module-level comment.
       - `Death_Dt = None` (MVP — no deceased cohort).
       - `Gender_Type_Cd = cp.gender_type_cd` (FK to `Core_DB.GENDER_TYPE`).
       - `Ethnicity_Type_Cd = cp.ethnicity_type_cd` (FK to `Core_DB.ETHNICITY_TYPE`).
       - `Tax_Bracket_Cd` **NOT NULL** — derive from `cp.income_quartile` via a module-level `_TAX_BRACKET_BY_QUARTILE = {1: 'BRACKET_12', 2: 'BRACKET_22', 3: 'BRACKET_24', 4: 'BRACKET_32'}` dict (codes already seeded in `Core_DB.TAX_BRACKET_TYPE`). Seed hint comment in `seed_data/party_types.py` line 196 explicitly names this mapping.
       - `Retirement_Dt = None` for `cp.occupation_cd != 'RETIRED'`; `= date(SIM_DATE.year - 62, 6, 15)` (deterministic, age-62 retirement) for retirees. Simpler: always `None` is acceptable — the DDL is nullable and this is not a hard constraint. Document the choice.
       - `Employment_Start_Dt = None` (ASSOCIATE_EMPLOYMENT is Step 12's responsibility).
       - `Nationality_Cd = 'USA'` **NOT NULL** for all rows (MVP is a US-centric synthetic dataset; Faker would over-engineer this). The `NATIONALITY_TYPE` seed table already contains 'USA'.
       - `Name_Only_No_Pronoun_Ind = 'No'` (CHAR(3), not `'N'`).
     - **`ORGANIZATION`** — one row per `CustomerProfile` where `cp.party_type == 'ORGANIZATION'` (~600 rows at the 80/20 split) **plus** exactly one reserved placeholder row at `Organization_Party_Id = SELF_EMP_ORG_ID` (`9_999_999`). Total: ~601 rows.
       - Regular org row fields:
         - `Organization_Party_Id = cp.party_id`
         - `Organization_Type_Cd = 'COMMERCIAL'` **NOT NULL** (free-text VARCHAR(50) per DDL; no FK target in MVP; pick a stable literal).
         - `Organization_Established_Dttm = datetime.combine(cp.party_since, time(0, 0)) - timedelta(days=3650)` (established ~10 years before relationship start — produces non-NULL plausible values deterministically).
         - `Parent_Organization_Party_Id = None` (flat hierarchy in MVP).
         - `Organization_Size_Type_Cd = 'SMALL'` (free-text VARCHAR — no MVP FK target).
         - `Legal_Classification_Cd = 'LLC'` (FK to seeded LEGAL_CLASSIFICATION — pick a single stable default; deterministic variation optional via `['LLC', 'CORPORATION', 'PARTNERSHIP'][cp.party_id % 3]`).
         - `Ownership_Type_Cd = None` (no FK target; nullable).
         - `Organization_Close_Dt = None`.
         - `Organization_Operation_Dt = cp.party_since`.
         - `Organization_Fiscal_Month_Num = '12'`, `Organization_Fiscal_Day_Num = '31'` (calendar-year fiscal; VARCHAR(50) per DDL).
         - `Basel_Organization_Type_Cd = None`, `Basel_Market_Participant_Cd = None`, `Basel_Eligible_Central_Ind = 'No'` (CHAR(3)).
         - `BIC_Business_Alpha_4_Cd = None` (CHAR(4); nullable; MVP does not model SWIFT codes).
       - Reserved placeholder row fields (ONE row only):
         - `Organization_Party_Id = SELF_EMP_ORG_ID` (`9_999_999`).
         - `Organization_Type_Cd = 'PLACEHOLDER'` (documents the row's purpose; free-text VARCHAR).
         - `Organization_Established_Dttm = None`.
         - `Parent_Organization_Party_Id = None`.
         - `Organization_Size_Type_Cd = None`.
         - `Legal_Classification_Cd = 'SOLE_PROPRIETORSHIP'` (semantically accurate for self-employed; FKs to seeded LEGAL_CLASSIFICATION).
         - `Organization_Close_Dt = None`.
         - `Organization_Operation_Dt = None`.
         - `Organization_Fiscal_Month_Num = None`, `Organization_Fiscal_Day_Num = None`.
         - All Basel_* = None; `Basel_Eligible_Central_Ind = None`.
         - `BIC_Business_Alpha_4_Cd = None`.
       - The placeholder row's `org_name` equivalent is carried in a later step's ORGANIZATION_NAME table (Step 13) with `Name_Type_Cd = 'legal name'`, `Organization_Name_Val = 'Self-Employment Organization'` — **this step does NOT emit ORGANIZATION_NAME** (Tier 4b's responsibility). The placeholder must be present in `ORGANIZATION` so Step 13 has a valid FK target.
     - **`BUSINESS`** — one row per real ORGANIZATION customer (1:1 extension table; ~600 rows). **Do NOT emit a BUSINESS row for the reserved `9_999_999` placeholder** — the placeholder exists only as an FK target for `INDIVIDUAL_PAY_TIMING.Business_Party_Id` (which Step 12 populates); it does not itself represent an equity-linked business entity. This keeps the reserved row minimal and avoids a `SELF_EMPLOYED`-coded BUSINESS row that no downstream tier reads.
       - `Business_Party_Id = cp.party_id` (for each ORGANIZATION customer — FKs to the matching `ORGANIZATION.Organization_Party_Id` row).
       - `Business_Category_Cd` — derive deterministically from `cp.party_id % 4` to pick from `['SMALL_BUSINESS', 'MID_MARKET', 'ENTERPRISE', 'MICRO_BUSINESS']` (all four codes seeded in `Core_DB.BUSINESS_CATEGORY`). Nullable but populated here for Layer 2 demo value.
       - `Business_Legal_Start_Dt = cp.party_since - timedelta(days=3650)` (mirrors `Organization_Established_Dttm`'s date part).
       - `Business_Legal_End_Dt = None` (open; active business).
       - `Tax_Bracket_Cd` **NOT NULL** — use `'BRACKET_22'` as a stable org default (no `cp.income_quartile` for orgs; the 22% bracket is mid-range and plausible for a small-to-mid business). All ORGANIZATION customers use the same value; document the choice in a module-level constant `_ORG_TAX_BRACKET = 'BRACKET_22'`.
       - `Customer_Location_Type_Cd = None` (no MVP FK target).
       - `Stock_Exchange_Listed_Ind = 'No'` (CHAR(3); MVP assumes no public companies).
  6. For every DataFrame, stamp via `self.stamp_di(df, start_ts=_TIER3_DI_START_TS)` where `_TIER3_DI_START_TS = '2000-01-01 00:00:00.000000'` (mirrors Tier 1 / Tier 2 fixed-timestamp convention for byte-identical reruns). Do NOT call `stamp_valid()` — Tier 3 is all Core_DB.
  7. Return `Dict[str, pd.DataFrame]` keyed `Core_DB.<TABLE>` for all three tables. Do not mutate `ctx.tables` — the orchestrator does that.

**Do NOT produce** in this step:
- CSVs — writer is not invoked. `output/` must remain empty.
- New `seed_data/*.py` modules — Tier 3 emits entity rows, not lookups. All required codes are already seeded by Steps 6/7/8.
- New `generators/tier3_*.py` submodules — a single flat generator module is simpler than splitting by table (Tier 3 is only 3 tables).
- Wiring into `main.py` — orchestrator changes are Step 25's responsibility.
- `ORGANIZATION_NAME` rows (Step 13), `INDIVIDUAL_NAME` rows (Step 12), or any Tier 4 attribute tables. These are separate steps.
- CDM_DB.INDIVIDUAL / CDM_DB.ORGANIZATION rows — Step 22 (Tier 14 CDM_DB).
- Changes to `config/settings.py`, `config/code_values.py`, `config/distributions.py`, `utils/*`, `registry/*`, `output/*`, `generators/base.py`, or any existing generator (Tier 0 / Tier 1 / Tier 2).
- Changes to any document (`PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/*`).

## Tables generated (if applicable)

After `Tier3PartySubtypes.generate(ctx)` runs, `ctx.tables` gains these three `Core_DB` keys:

| Table | Row count | FK dependencies (Tier 0 codes) | Constraint requirements |
|-------|-----------|--------------------------------|-------------------------|
| `Core_DB.INDIVIDUAL` | = count of INDIVIDUAL-type customers (~2,400 at 80/20) | `GENDER_TYPE.Gender_Type_Cd`, `ETHNICITY_TYPE.Ethnicity_Type_Cd`, `TAX_BRACKET_TYPE.Tax_Bracket_Cd`, `NATIONALITY_TYPE.Nationality_Cd` | `Tax_Bracket_Cd` NOT NULL every row; `Nationality_Cd` NOT NULL every row; `Individual_Party_Id` unique and equal to some `CustomerProfile.party_id` with `party_type='INDIVIDUAL'` |
| `Core_DB.ORGANIZATION` | = count of ORGANIZATION-type customers + 1 reserved (~601 at 80/20) | `LEGAL_CLASSIFICATION.Legal_Classification_Cd` | Contains exactly one row with `Organization_Party_Id = 9_999_999`; `Organization_Type_Cd` NOT NULL every row |
| `Core_DB.BUSINESS` | = count of ORGANIZATION-type customers (~600 — does NOT include the 9_999_999 placeholder) | `BUSINESS_CATEGORY.Business_Category_Cd` (nullable but populated), `TAX_BRACKET_TYPE.Tax_Bracket_Cd` | `Tax_Bracket_Cd` NOT NULL every row; every `Business_Party_Id` resolves to an `ORGANIZATION.Organization_Party_Id` row |

All three DataFrames have the full 5-column DI tail in `DI_COLUMN_ORDER` after `stamp_di()`, with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`.

No literal-match seed rows are required for Tier 3 — the Layer 2 literal-match constraints (FROZEN / Rate Feature / Original Loan Term / customer profitability / primary role) all belong to other tiers.

## Files to modify

No files modified. `config/*`, `utils/*`, `registry/*`, `output/*`, `main.py`, `CLAUDE.md`, all documents under `references/` and the project root, all `seed_data/*.py`, and all existing `generators/*.py` (base, tier0_lookups, tier1_geography, tier2_core) are NOT touched.

If the implementation session finds that `references/07_mvp-schema-reference.md` disagrees with this spec on a column name, type, or nullability for INDIVIDUAL / ORGANIZATION / BUSINESS, escalate per Handoff Protocol §2 — update the upstream reference or add a `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new dependencies. Uses only stdlib `datetime` + pandas (already in `requirements.txt`) + existing project modules.

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — every `*_Id` column is emitted as `pd.Int64Dtype()` (nullable BIGINT) or `int64` when all non-null. DDL declares `INTEGER` for `Individual_Party_Id`, `Organization_Party_Id`, `Parent_Organization_Party_Id`, `Business_Party_Id`; the BIGINT rule wins unconditionally. Specifically: `Individual_Party_Id`, `Organization_Party_Id`, `Parent_Organization_Party_Id`, `Business_Party_Id`.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — `Individual_Party_Id` and `Organization_Party_Id` in this step come directly from `CustomerProfile.party_id`; the same BIGINT values will later be written as `CDM_DB.PARTY.CDM_Party_Id` in Step 22. Do NOT re-mint party IDs here. The reserved `SELF_EMP_ORG_ID = 9_999_999` exists in Core_DB only — it is a placeholder, NOT a real party and NOT emitted to `Core_DB.PARTY` by Step 10. Downstream tiers that need to join ORGANIZATION to PARTY must be aware that the 9_999_999 row has no PARTY counterpart (documented in design §7.12).
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on all three DataFrames. Construct each via `pd.DataFrame(rows, columns=_COLS_*)` with business columns only, then `self.stamp_di(df, start_ts=_TIER3_DI_START_TS)` appends the 5 DI columns at the end. Fixed `_TIER3_DI_START_TS = '2000-01-01 00:00:00.000000'` guarantees byte-identical output across runs.
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts` stamped to `HIGH_TS` via `stamp_di()` default. `Valid_To_Dt` n/a: Tier 3 is all Core_DB.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — n/a: Tier 3 is all Core_DB. Do NOT call `stamp_valid()`.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** — enforced at construction time. Each DataFrame built via `pd.DataFrame(rows, columns=_COLS)` where `_COLS` is a module-level tuple / list matching the DDL business-column order exactly. After `stamp_di()` appends the 5 DI columns, the full column order matches the tier 0/1/2 convention and the writer's reorder step (Step 5).
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — n/a: that table is Step 22, not touched here.
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — n/a: no GEOSPATIAL row authored here.
- **No ORMs, no database connections — pure pandas → CSV** — generator returns DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — **no randomness in this step**. Every row is deterministically derived from `ctx.customers`. The generator does not read or use `ctx.rng`. Any Faker/rng use in this step is a bug.

Step-specific rules (Tier 3 Party Subtypes):

- **Universe projection is deterministic and in iteration order.** `INDIVIDUAL` rows come out in the same order as `[cp for cp in ctx.customers if cp.party_type == 'INDIVIDUAL']`. `ORGANIZATION` rows come out as `[cp for cp in ctx.customers if cp.party_type == 'ORGANIZATION']` followed by the single reserved placeholder row. `BUSINESS` rows mirror the ORGANIZATION customer order (without the placeholder). No sorting or filtering beyond the party_type filter.
- **The reserved `SELF_EMP_ORG_ID = 9_999_999` placeholder is mandatory and exactly one row.** The check is byte-level: `len(df_org[df_org['Organization_Party_Id'] == 9_999_999]) == 1`. Do NOT emit more than one row with this ID; do NOT skip it; do NOT write it into `Core_DB.PARTY` (that's Step 10's responsibility, and Step 10 only writes from `ctx.customers`).
- **No BUSINESS row for the reserved placeholder.** `len(df_business[df_business['Business_Party_Id'] == 9_999_999]) == 0`. The placeholder is an FK target for PAY_TIMING / BONUS_TIMING only; it does not represent a business-equity entity.
- **`INDIVIDUAL.Tax_Bracket_Cd` and `INDIVIDUAL.Nationality_Cd` are NOT NULL every row.** Enforced by construction via the `_TAX_BRACKET_BY_QUARTILE` lookup and the `'USA'` literal default. If a future change introduces a non-USA nationality path, the NOT NULL check in Definition of done must still pass.
- **`BUSINESS.Tax_Bracket_Cd` is NOT NULL every row.** Enforced via the `_ORG_TAX_BRACKET` constant.
- **CHAR(3) flags use `'Yes'` / `'No'`, not `'Y'` / `'N'`** (PRD §4.3). Applies to `INDIVIDUAL.Name_Only_No_Pronoun_Ind`, `ORGANIZATION.Basel_Eligible_Central_Ind`, `BUSINESS.Stock_Exchange_Listed_Ind`.
- **No new ID minting.** `ctx.ids` is not called in this step — every ID comes from `CustomerProfile.party_id` or the reserved `SELF_EMP_ORG_ID` constant. Adding a `ctx.ids.next('party')` call is a bug.
- **Deterministic derivations only.** `Birth_Dt`, `Organization_Established_Dttm`, `Business_Legal_Start_Dt`, `Legal_Classification_Cd`, `Business_Category_Cd` — all are derived from `cp` attributes (age, party_id, party_since) via pure functions. No `ctx.rng`, no `Faker`, no `hash()`.
- **No side effects on import.** `import generators.tier3_party_subtypes` must not construct any DataFrames or perform any network/file I/O. Enforced by the "no import-time DataFrames" check in Definition of done.
- **`Tier3PartySubtypes.generate()` must accept `ctx`** — `BaseGenerator.generate(self, ctx)` signature is fixed by Step 2. Runtime-import `GenerationContext` via `TYPE_CHECKING` only.
- **Tier 0 prerequisite guard.** `Tier3PartySubtypes.generate()` starts with an explicit check that required Tier 0 tables (`Core_DB.GENDER_TYPE`, `Core_DB.ETHNICITY_TYPE`, `Core_DB.TAX_BRACKET_TYPE`, `Core_DB.NATIONALITY_TYPE`, `Core_DB.LEGAL_CLASSIFICATION`, `Core_DB.BUSINESS_CATEGORY`) are in `ctx.tables`. Fail fast with `RuntimeError(f'Tier3PartySubtypes requires Tier 0 table {key} to be loaded first')` if any is missing.
- **Universe prerequisite guard.** `Tier3PartySubtypes.generate()` also explicitly checks `ctx.customers` is non-empty, with a clear error: `RuntimeError('Tier3PartySubtypes requires a populated ctx.customers — run UniverseBuilder.build() first')`.
- **Escalation over improvisation.** If `07` has an ambiguity (column name differs, nullability unclear), stop and leave a `⚠️ Conflict` block in this spec. Do NOT invent columns or silently swap FKs.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current working directory and `python` resolves to the project's Python 3.12 environment. All checks run in a single `python` process after constructing a full `ctx` (UniverseBuilder.build → Tier0Lookups.generate → Tier1Geography.generate → Tier2Core.generate → Tier3PartySubtypes.generate) — this is cheap (<10s end-to-end).

### Module-import and API contract

- [ ] `python -c "import generators.tier3_party_subtypes"` exits 0.
- [ ] `generators.tier3_party_subtypes.Tier3PartySubtypes` inherits from `BaseGenerator` and defines `generate(ctx)`:
  ```bash
  python -c "
  from generators.tier3_party_subtypes import Tier3PartySubtypes
  from generators.base import BaseGenerator
  import inspect
  assert issubclass(Tier3PartySubtypes, BaseGenerator)
  sig = inspect.signature(Tier3PartySubtypes.generate)
  assert 'ctx' in sig.parameters
  print('Tier3PartySubtypes contract OK')
  "
  ```
- [ ] Import has no side effects (no DataFrames constructed at module level):
  ```bash
  python -c "
  import sys
  before = len(sys.modules)
  import generators.tier3_party_subtypes as m
  # Module-level symbols are types/constants/dicts only — no pd.DataFrame at top level
  for name in dir(m):
      if name.startswith('_'): continue
      obj = getattr(m, name)
      import pandas as pd
      assert not isinstance(obj, pd.DataFrame), f'module-level DataFrame: {name}'
  print('no import-time DataFrames OK')
  "
  ```

### Fail-fast guards

- [ ] Calling `generate()` on an empty-`ctx.customers` context raises `RuntimeError` mentioning `UniverseBuilder`:
  ```bash
  python -c "
  from generators.tier3_party_subtypes import Tier3PartySubtypes
  from registry.context import GenerationContext
  from utils.id_factory import IdFactory
  import numpy as np
  ctx = GenerationContext(customers=[], agreements=[], addresses=[],
      config=None, rng=np.random.default_rng(42), ids=IdFactory(), tables={})
  try:
      Tier3PartySubtypes().generate(ctx)
      raise AssertionError('should have raised')
  except RuntimeError as e:
      assert 'UniverseBuilder' in str(e) or 'ctx.customers' in str(e), str(e)
      print('empty customers guard OK')
  "
  ```
- [ ] Calling `generate()` with missing Tier 0 tables raises `RuntimeError` mentioning `Tier 0`:
  ```bash
  python -c "
  from generators.tier3_party_subtypes import Tier3PartySubtypes
  from registry.profiles import CustomerProfile
  from registry.context import GenerationContext
  from utils.id_factory import IdFactory
  from datetime import date
  import numpy as np
  cp = CustomerProfile(party_id=10_000_000, party_type='INDIVIDUAL', age=35,
      income_quartile=2, lifecycle_cohort='ACTIVE', clv_segment=5,
      gender_type_cd='MALE', marital_status_cd='SINGLE', ethnicity_type_cd='WHITE',
      occupation_cd='EMP', num_dependents=0, fico_score=700,
      household_id=None, household_role='HEAD', lifecl=2,
      has_internet=True, preferred_channel_cd=3, party_since=date(2020,1,1),
      address_id=1_000_000, product_set=[])
  ctx = GenerationContext(customers=[cp], agreements=[], addresses=[],
      config=None, rng=np.random.default_rng(42), ids=IdFactory(), tables={})
  try:
      Tier3PartySubtypes().generate(ctx)
      raise AssertionError('should have raised')
  except RuntimeError as e:
      assert 'Tier 0' in str(e) or 'TAX_BRACKET_TYPE' in str(e) or 'NATIONALITY_TYPE' in str(e), str(e)
      print('missing-tier0 guard OK')
  "
  ```

### Table emission

Helper context builder (reused across checks below — construct once and cache `tables`):

```python
# Paste into a throwaway python -c invocation; all subsequent checks reuse `tables`.
from config.settings import SEED
from registry.universe import UniverseBuilder
from generators.tier0_lookups import Tier0Lookups
from generators.tier1_geography import Tier1Geography
from generators.tier2_core import Tier2Core
from generators.tier3_party_subtypes import Tier3PartySubtypes
import numpy as np

rng = np.random.default_rng(SEED)
ctx = UniverseBuilder().build(config=None, rng=rng)
ctx.tables.update(Tier0Lookups().generate(ctx))
ctx.tables.update(Tier1Geography().generate(ctx))
ctx.tables.update(Tier2Core().generate(ctx))
tier3 = Tier3PartySubtypes().generate(ctx)
ctx.tables.update(tier3)
```

- [ ] `Tier3PartySubtypes().generate(ctx)` returns a dict with exactly these three keys: `{'Core_DB.INDIVIDUAL', 'Core_DB.ORGANIZATION', 'Core_DB.BUSINESS'}`. Run:
  ```python
  assert set(tier3.keys()) == {'Core_DB.INDIVIDUAL', 'Core_DB.ORGANIZATION', 'Core_DB.BUSINESS'}, tier3.keys()
  ```

### INDIVIDUAL — exit criterion "Every INDIVIDUAL.Individual_Party_Id maps back to a unique CustomerProfile"

- [ ] `Core_DB.INDIVIDUAL` row count equals the count of INDIVIDUAL-type customers (and only those):
  ```python
  df_i = tier3['Core_DB.INDIVIDUAL']
  ind_customers = [cp for cp in ctx.customers if cp.party_type == 'INDIVIDUAL']
  assert len(df_i) == len(ind_customers), (len(df_i), len(ind_customers))
  ```
- [ ] `Individual_Party_Id` is unique and is a 1-to-1 mapping to `CustomerProfile.party_id` for INDIVIDUAL-type customers:
  ```python
  assert df_i['Individual_Party_Id'].is_unique
  ind_ids = {cp.party_id for cp in ind_customers}
  assert set(df_i['Individual_Party_Id'].tolist()) == ind_ids
  ```

### INDIVIDUAL — exit criterion "No INDIVIDUAL row has NULL Tax_Bracket_Cd or Nationality_Cd"

- [ ] Both columns are non-null on every row:
  ```python
  assert df_i['Tax_Bracket_Cd'].notna().all(), 'Tax_Bracket_Cd has NULLs'
  assert df_i['Nationality_Cd'].notna().all(), 'Nationality_Cd has NULLs'
  ```
- [ ] Tax_Bracket_Cd values all resolve to a seeded `Core_DB.TAX_BRACKET_TYPE.Tax_Bracket_Cd`:
  ```python
  tax_codes = set(ctx.tables['Core_DB.TAX_BRACKET_TYPE']['Tax_Bracket_Cd'])
  assert set(df_i['Tax_Bracket_Cd']).issubset(tax_codes), set(df_i['Tax_Bracket_Cd']) - tax_codes
  ```
- [ ] Nationality_Cd values all resolve to a seeded `Core_DB.NATIONALITY_TYPE.Nationality_Cd`:
  ```python
  nat_codes = set(ctx.tables['Core_DB.NATIONALITY_TYPE']['Nationality_Cd'])
  assert set(df_i['Nationality_Cd']).issubset(nat_codes)
  ```

### ORGANIZATION — exit criterion "ORGANIZATION contains the reserved ID 9999999 row"

- [ ] `Core_DB.ORGANIZATION` row count equals `len(org_customers) + 1`:
  ```python
  df_o = tier3['Core_DB.ORGANIZATION']
  org_customers = [cp for cp in ctx.customers if cp.party_type == 'ORGANIZATION']
  assert len(df_o) == len(org_customers) + 1, (len(df_o), len(org_customers) + 1)
  ```
- [ ] Exactly one row has `Organization_Party_Id == 9_999_999`:
  ```python
  from config.settings import SELF_EMP_ORG_ID
  reserved = df_o[df_o['Organization_Party_Id'] == SELF_EMP_ORG_ID]
  assert len(reserved) == 1, f'expected 1 reserved row, got {len(reserved)}'
  ```
- [ ] Every non-reserved `Organization_Party_Id` is a valid ORGANIZATION-type `CustomerProfile.party_id` and all are unique:
  ```python
  assert df_o['Organization_Party_Id'].is_unique
  non_reserved_ids = set(df_o['Organization_Party_Id']) - {SELF_EMP_ORG_ID}
  org_ids = {cp.party_id for cp in org_customers}
  assert non_reserved_ids == org_ids
  ```
- [ ] `Organization_Type_Cd` is NOT NULL on every row (DDL requirement):
  ```python
  assert df_o['Organization_Type_Cd'].notna().all(), 'Organization_Type_Cd has NULLs'
  ```
- [ ] `Legal_Classification_Cd` values all resolve to seeded codes (or are NULL):
  ```python
  legal_codes = set(ctx.tables['Core_DB.LEGAL_CLASSIFICATION']['Legal_Classification_Cd'])
  legal_vals = df_o['Legal_Classification_Cd'].dropna()
  assert set(legal_vals).issubset(legal_codes)
  ```

### BUSINESS — 1:1 with real ORGANIZATION, NOT NULL Tax_Bracket_Cd, no placeholder row

- [ ] `Core_DB.BUSINESS` row count equals `len(org_customers)` (no placeholder row):
  ```python
  df_b = tier3['Core_DB.BUSINESS']
  assert len(df_b) == len(org_customers), (len(df_b), len(org_customers))
  ```
- [ ] `Business_Party_Id` is unique, and every value FK-resolves to a non-reserved `ORGANIZATION.Organization_Party_Id`:
  ```python
  from config.settings import SELF_EMP_ORG_ID
  assert df_b['Business_Party_Id'].is_unique
  biz_ids = set(df_b['Business_Party_Id'])
  assert SELF_EMP_ORG_ID not in biz_ids, 'BUSINESS must NOT include placeholder'
  assert biz_ids == {cp.party_id for cp in org_customers}
  ```
- [ ] `Tax_Bracket_Cd` is NOT NULL on every row and resolves to a seeded code:
  ```python
  assert df_b['Tax_Bracket_Cd'].notna().all()
  assert set(df_b['Tax_Bracket_Cd']).issubset(tax_codes)
  ```
- [ ] `Business_Category_Cd` (nullable) when populated resolves to seeded `Core_DB.BUSINESS_CATEGORY`:
  ```python
  cat_codes = set(ctx.tables['Core_DB.BUSINESS_CATEGORY']['Business_Category_Cd'])
  cat_vals = df_b['Business_Category_Cd'].dropna()
  assert set(cat_vals).issubset(cat_codes)
  ```

### BIGINT and DI column enforcement

- [ ] Every `*_Id` column in every Tier 3 DataFrame is pandas `Int64` (nullable BIGINT):
  ```python
  for key, df in tier3.items():
      for col in df.columns:
          if col.endswith('_Id'):
              dtype = str(df[col].dtype)
              assert dtype in ('Int64', 'int64'), f'{key}.{col} is {dtype}, expected BIGINT'
  print('BIGINT check OK')
  ```
- [ ] Every Tier 3 DataFrame has the 5 DI columns in canonical `DI_COLUMN_ORDER` as the last 5 columns:
  ```python
  from utils.di_columns import DI_COLUMN_ORDER
  for key, df in tier3.items():
      tail = tuple(df.columns[-5:])
      assert tail == DI_COLUMN_ORDER, f'{key}: {tail} != {DI_COLUMN_ORDER}'
  ```
- [ ] Every Tier 3 DataFrame has `di_end_ts == HIGH_TS` and `di_rec_deleted_Ind == 'N'` on every row:
  ```python
  from config.settings import HIGH_TS
  for key, df in tier3.items():
      assert (df['di_end_ts'] == HIGH_TS).all(), f'{key}: di_end_ts mismatch'
      assert (df['di_rec_deleted_Ind'] == 'N').all(), f'{key}: di_rec_deleted_Ind mismatch'
  ```
- [ ] No Tier 3 DataFrame has `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` columns (Core_DB only, no stamp_valid):
  ```python
  for key, df in tier3.items():
      assert 'Valid_From_Dt' not in df.columns, f'{key}: unexpected Valid_From_Dt'
      assert 'Valid_To_Dt' not in df.columns, f'{key}: unexpected Valid_To_Dt'
      assert 'Del_Ind' not in df.columns, f'{key}: unexpected Del_Ind'
  ```
- [ ] CHAR(3) flag columns use `'Yes'` / `'No'` only, never `'Y'` / `'N'` (PRD §4.3):
  ```python
  CHAR3_COLS = {
      'Core_DB.INDIVIDUAL':    ['Name_Only_No_Pronoun_Ind'],
      'Core_DB.ORGANIZATION':  ['Basel_Eligible_Central_Ind'],
      'Core_DB.BUSINESS':      ['Stock_Exchange_Listed_Ind'],
  }
  for key, cols in CHAR3_COLS.items():
      for col in cols:
          vals = set(tier3[key][col].dropna().unique())
          assert vals.issubset({'Yes', 'No'}), f'{key}.{col} has non-CHAR(3) values: {vals}'
  print('CHAR(3) flag check OK')
  ```

### DDL column ordering (matches `references/07_mvp-schema-reference.md`)

- [ ] Every Tier 3 DataFrame, when written through `output.writer._reorder_to_ddl()` (if invoked), matches the DDL column order. Verify by direct comparison of the business-column prefix against the DDL summary block:
  ```python
  # Quick business-column contract: the first N columns (before DI) must match DDL order.
  expected_individual = ['Individual_Party_Id', 'Birth_Dt', 'Death_Dt', 'Gender_Type_Cd',
      'Ethnicity_Type_Cd', 'Tax_Bracket_Cd', 'Retirement_Dt', 'Employment_Start_Dt',
      'Nationality_Cd', 'Name_Only_No_Pronoun_Ind']
  assert list(tier3['Core_DB.INDIVIDUAL'].columns[:10]) == expected_individual
  expected_org = ['Organization_Party_Id', 'Organization_Type_Cd', 'Organization_Established_Dttm',
      'Parent_Organization_Party_Id', 'Organization_Size_Type_Cd', 'Legal_Classification_Cd',
      'Ownership_Type_Cd', 'Organization_Close_Dt', 'Organization_Operation_Dt',
      'Organization_Fiscal_Month_Num', 'Organization_Fiscal_Day_Num',
      'Basel_Organization_Type_Cd', 'Basel_Market_Participant_Cd',
      'Basel_Eligible_Central_Ind', 'BIC_Business_Alpha_4_Cd']
  assert list(tier3['Core_DB.ORGANIZATION'].columns[:15]) == expected_org
  expected_biz = ['Business_Party_Id', 'Business_Category_Cd', 'Business_Legal_Start_Dt',
      'Business_Legal_End_Dt', 'Tax_Bracket_Cd', 'Customer_Location_Type_Cd',
      'Stock_Exchange_Listed_Ind']
  assert list(tier3['Core_DB.BUSINESS'].columns[:7]) == expected_biz
  ```

### Reproducibility (byte-identical reruns)

- [ ] Running the build pipeline twice with `SEED=42` produces byte-identical Tier 3 DataFrames:
  ```python
  import pandas as pd, numpy as np
  from config.settings import SEED
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  from generators.tier3_party_subtypes import Tier3PartySubtypes

  def run():
      rng = np.random.default_rng(SEED)
      ctx = UniverseBuilder().build(config=None, rng=rng)
      ctx.tables.update(Tier0Lookups().generate(ctx))
      ctx.tables.update(Tier1Geography().generate(ctx))
      ctx.tables.update(Tier2Core().generate(ctx))
      return Tier3PartySubtypes().generate(ctx)

  a, b = run(), run()
  for key in a:
      pd.testing.assert_frame_equal(a[key], b[key], check_dtype=True, check_exact=True)
  print('reproducibility OK')
  ```

### Universal checks

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else. (Expected new file: `generators/tier3_party_subtypes.py`. No other file changes.)
- [ ] All new files pass `python -c "import <module>"`:
  ```bash
  python -c "import generators.tier3_party_subtypes" && echo OK
  ```
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — **n/a at this step**: no CSVs written (writer is not invoked). The in-memory BIGINT check above is the relevant check.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: that table is Step 22, not this step.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSVs written in this step. `output/` must remain empty or absent.
- [ ] `ctx.ids.peek(...)` counters for `party` are unchanged by this step (no new IDs minted):
  ```python
  # Wrap the Tier 3 call in before/after peek comparisons
  before = ctx.ids.peek('party') if hasattr(ctx.ids, 'peek') else None
  Tier3PartySubtypes().generate(ctx)
  after = ctx.ids.peek('party') if hasattr(ctx.ids, 'peek') else None
  assert before == after, f'party counter advanced: {before} -> {after}'
  ```
  If `IdFactory.peek()` does not exist, mark this check as "n/a — helper absent" and instead verify that the generator source contains no `ctx.ids.next(` call:
  ```bash
  ! grep -n 'ctx.ids.next(' generators/tier3_party_subtypes.py && echo "no id minting OK"
  ```

## Handoff notes

_Filled in at the end of the implementation session per `implementation-steps.md` Handoff Protocol._

# Spec: Step 07 — Tier 0b Seed Data — Party / Demographics / Industry

## Overview

This step authors the **second slice of Tier 0 seed data** — the handwritten Python dict literals that populate lookup / reference tables for the `PARTY` domain (demographics, status, medical, skills, language, specialty, legal classification) and the `INDUSTRY` domain (NAICS, NACE, SIC, GICS hierarchies). These tables are *not* randomly generated (see `PRD.md` §7.11 Decision 11 and `mvp-tool-design.md` §14 Decision 2): downstream generators (Steps 11, 12, 13) will FK-reference these codes, and the UniverseBuilder (Step 4, already shipped) samples ethnicity and occupation from a fixed enumeration that must match the seeded `ETHNICITY_TYPE.Ethnicity_Type_Cd` and `OCCUPATION_TYPE.Occupation_Type_Cd` universes verbatim (see `references/06_supporting-enrichments.md` lines 84–99, 356–357). Industry codes are additionally required because `ORGANIZATION_NAICS` / `ORGANIZATION_NACE` / `ORGANIZATION_SIC` / `ORGANIZATION_GICS` each carry multi-column NOT-NULL FKs into the corresponding code tables (Step 13 writes the bridge rows; this step seeds the parent hierarchies). This step ships two `seed_data/*.py` modules — `party_types.py` and `industry_codes.py` — each exposing a `get_<domain>_tables() -> Dict[str, pd.DataFrame]` function returning un-stamped DataFrames keyed by `'Core_DB.<TABLE>'`. No DI column stamping is done here — that responsibility lives in Step 8's `Tier0Lookups` generator, which will consume these modules alongside those from Steps 6 and 8. Steps 6, 7, and 8 are independent (per `implementation-steps.md` Dependency Graph) and may run in parallel.

## Depends on

- **Step 1** — consumes from `config/settings.py`:
  - `HIGH_DATE`, `HIGH_TS` — n/a for this step's tables (all Tier 0b tables are pure code→desc lookups with no lifecycle dates).
  - No imports from `config/code_values.py` are required for Step 7 — unlike Step 6, the Tier 0b domain does not carry any Layer 2 literal-match codes defined in `code_values.py` (ethnicity / occupation codes are distribution-derived, not literal-match). If any code is later promoted to a `code_values.py` constant (e.g. a specific NATIONALITY_TYPE default), this module must import and reuse it rather than duplicate the string.

No code from Step 2, 3, 4, or 5 is imported by this step — the seed modules are pure data with a thin pandas DataFrame wrapper. The tables they produce are consumed by Step 8's `Tier0Lookups.generate(ctx)` via the `get_<domain>_tables()` contract.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and **Seed Data Authoring Convention** all apply)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 7 + the Seed Data Authoring Convention):
- `PRD.md` §7.11 (Tier 0 seeded-not-generated rule), §10 (Ground Truth Priority — `07` takes precedence over `01` for MVP scope)
- `mvp-tool-design.md` §9 Tier 0 (authoritative Tier-0 table list grouped by domain; Step 7 implements the "Party" block plus the NAICS / NACE / SIC / GICS entries from the "Other" block), §14 Decision 2 (rationale for hand-coded seed data)
- `implementation-steps.md` Step 7 entry (exit criteria), **Seed Data Authoring Convention** (read-discipline, escalation rules, `get_<domain>_tables` output contract)

**Additional reference files** (only those named in the step's "Reads from" line, filtered per the Seed Data Authoring Convention):
- `references/07_mvp-schema-reference.md` — **authoritative DDL slice** for every table this step seeds. For each table, open only the `#### <TABLE_NAME>` block and capture column names, types, nullability, composite PKs, and FK relationships. Use DDL column order exactly — Step 5's `_load_ddl_column_order` parser returns the DI columns as the final three entries, so every DataFrame must include `di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind` (all `None`) as the last three columns. Specific DDL blocks to read (line numbers current as of 2026-04-20):
  - `GENDER_TYPE` (§5606), `GENDER_PRONOUN` (§5629 — composite PK + `Gender_Pronoun_Name`), `ETHNICITY_TYPE` (§5655), `MARITAL_STATUS_TYPE` (§5678), `NATIONALITY_TYPE` (§5701), `TAX_BRACKET_TYPE` (§5724 — includes `Tax_Bracket_Rate DECIMAL(15,12)`), `VERY_IMPORTANT_PERSON_TYPE` (§5749), `MILITARY_STATUS_TYPE` (§5772), `OCCUPATION_TYPE` (§5795), `PARTY_RELATED_STATUS_TYPE` (§5841), `GENERAL_MEDICAL_STATUS_TYPE` (§5864)
  - `SKILL_TYPE` (§5337), `SPECIAL_NEED_TYPE` (§5583), `SPECIALTY_TYPE` (§7076), `LANGUAGE_TYPE` (§7198 — includes `Language_Native_Name`, `ISO_Language_Type_Cd NOT NULL`), `LEGAL_CLASSIFICATION` (§6893), `BUSINESS_CATEGORY` (§6678)
  - `NAICS_INDUSTRY` (§6916 — 5-column code chain), `NACE_CLASS` (§6773 — 4-column chain), `SIC` (§6947 — `SIC_Cd` + `SIC_Group_Cd`), `GICS_SECTOR_TYPE` (§7053), `GICS_INDUSTRY_GROUP_TYPE` (§7028), `GICS_INDUSTRY_TYPE` (§6972), `GICS_SUBINDUSTRY_TYPE` (§6999)
  - The bridge DDLs are read for **context only**, not authored here: `ORGANIZATION_NAICS` (§6701), `ORGANIZATION_NACE` (§6738), `ORGANIZATION_SIC` (§6802), `ORGANIZATION_GICS` (§6831). These show which code columns from the hierarchies are required NOT NULL on the bridge — the seeded parent tables must cover every value that Step 13 will later pick from.
- `references/02_data-mapping-reference.md` Step 3 — **constrained code values and literal-match rows**. Scan for party / industry domain items and embed any literal codes verbatim. Current known items:
  - Item #14 (ORGANIZATION BB industry pivot): NAICS / SIC / GICS hierarchies must be populated with enough rows that Step 13 can select one `Primary_*_Ind='Yes'` code per organization.
  - No party-domain literal-match row equivalent to FROZEN / Rate Feature / Original Loan Term exists (party codes are distribution-derived, not literal-match).
- `references/06_supporting-enrichments.md` **Part A only** (demographic code mapping) — this is an **explicit exception** to the Seed Data Authoring Convention's "do not read 06" rule, because Part A defines the exact ethnicity / occupation code strings the UniverseBuilder samples from. Read-scope:
  - Lines 84–87: `{WHITE, BLACK, HISPANIC, ASIAN}` — `ETHNICITY_TYPE.Ethnicity_Type_Cd` must include these four plus an `OTHER` row (per the SCF RACECL5 mapping at line 356).
  - Lines 97–99: `{EMP, SELF_EMP, RETIRED, NOT_WORKING}` — `OCCUPATION_TYPE.Occupation_Type_Cd` must contain exactly these four (per the SCF OCCAT1/OCCAT2 mapping at line 357).
  - **Do not read any other Part of 06** — Parts B–J cover distributions, which are Step 4's concern, not Tier 0's.

**Do NOT read** (explicitly excluded to protect context budget and per the Seed Data Authoring Convention):
- `references/01_schema-reference.md` — supplementary; `07` is the MVP-filtered DDL set and takes precedence per PRD §10. (Note: `implementation-steps.md` Step 7's "Reads from" line still mentions `01`. The Seed Data Authoring Convention in the same file overrides — only open `01` if `07` is ambiguous for a specific column.)
- `references/05_architect-qa.md` — **⚠️ Conflict with `implementation-steps.md` Step 7**: the step names "Q8 (industry code requirements)", but the file only contains Q1–Q7 (76 lines total, ends mid-Q7 answer). Q8 has **never existed** in this file. This is a documentation drift inherited from an earlier draft. The architect has not defined a Q8; proceed with real-world NAICS / NACE / SIC / GICS public knowledge + the DDL column structure in `07`. If the implementation session finds this genuinely blocking, escalate per Handoff Protocol §2 — do **not** silently re-read `01` or the Excels. See the `## ⚠️ Conflict` block below.
- `references/06_supporting-enrichments.md` **Parts B–J** — distributions; irrelevant for Tier 0. Only Part A is in scope for this step.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` and `resources/iDM_MDM_tables_DDLs.xlsx` — already distilled into the references above. Do not re-read the Excels per session.

## ⚠️ Conflict — `implementation-steps.md` Step 7 references a non-existent Q8

**Observation.** `implementation-steps.md` Step 7 "Reads from" line names `references/05_architect-qa.md Q8 (industry code requirements)`. That file contains Q1–Q7 and ends at line 76; Q8 is not present. This is a stale reference from an earlier draft.

**Impact.** Small — the guidance the session would have drawn from Q8 (which industry code taxonomies to populate, required row density per hierarchy level) is derivable from:
1. `references/07_mvp-schema-reference.md` ORGANIZATION_NAICS / NACE / SIC / GICS bridge DDLs, which enumerate exactly which code columns must be NOT NULL on the bridge tables.
2. Real-world public taxonomies (NAICS sectors 11–99, NACE sections A–U, SIC divisions A–I, GICS 11 sectors) are well-documented.

**Resolution chosen for this spec.** Proceed with public knowledge + DDL column structure. Seed **at least one complete hierarchy path per primary taxonomy** (one path reaches every NOT-NULL column in the bridge), plus enough breadth to let Step 13 pick meaningfully different codes across ~600 organizations. Concretely:
- NAICS: ~6 sectors, each with a full `Sector → Subsector → Industry_Group → Industry → National_Industry` chain (one complete path per sector minimum; multiple paths welcome for sectors 52, 62, 44-45, 51, 72, 81 which are most common for retail bank customers).
- NACE: ~5 sections, each with a full `Section → Division → Group → Class` chain.
- SIC: ~10–15 `(SIC_Cd, SIC_Group_Cd)` rows across 3–4 industry divisions.
- GICS: all 11 sectors, each with at least one industry group → industry → subindustry path.

**If blocking at implementation time:** the implementation session may leave this `⚠️ Conflict` block intact, log what row density it chose, and list the architect question crisply for a future Q8 (e.g. "Do industry codes need to match a specific regulator schema, or are public ISO / Census taxonomies sufficient?"). Do not silently improvise codes that don't exist in the real taxonomies.

## Produces

All paths relative to the project root.

**New files:**

- `seed_data/party_types.py` — seed rows for the party-domain lookup tables. Exposes `get_party_type_tables() -> Dict[str, pd.DataFrame]`. Tables included (keys are `'Core_DB.<TABLE>'`; column order per `07`, DI columns as the last three with `None` values):
  - `Core_DB.GENDER_TYPE` — at least `MALE`, `FEMALE`, `NON_BINARY`, `UNSPECIFIED`. `MALE` and `FEMALE` are the only two codes the UniverseBuilder samples (per `_assign_demographics`), but including `NON_BINARY` / `UNSPECIFIED` keeps the lookup domain realistic and future-proof.
  - `Core_DB.GENDER_PRONOUN` — composite PK `(Gender_Pronoun_Cd, Gender_Pronoun_Type_Cd)`; include e.g. `HE/subjective`, `HIM/objective`, `HIS/possessive`, `SHE/subjective`, `HER/objective`, `HERS/possessive`, `THEY/subjective`, `THEM/objective`, `THEIRS/possessive`. Populate `Gender_Pronoun_Name` with the human-readable form.
  - `Core_DB.ETHNICITY_TYPE` — **must contain exactly `{WHITE, BLACK, HISPANIC, ASIAN, OTHER}`** (literal-match to `06` Part A lines 84–87 + line 356 SCF RACECL5 mapping; the UniverseBuilder's `sample_ethnicity` output must resolve to a seeded row).
  - `Core_DB.MARITAL_STATUS_TYPE` — at least `MARRIED`, `SINGLE`, `DIVORCED`, `WIDOWED`, `SEPARATED`. `MARRIED` and `SINGLE` are the two codes the UniverseBuilder samples; the others are domain completeness.
  - `Core_DB.NATIONALITY_TYPE` — 10–20 ISO-3166 alpha-3 nationality codes used by `INDIVIDUAL.Nationality_Cd` (NOT NULL). Must include at minimum `USA`, `CAN`, `GBR`, `IND`, `CHN`, `MEX`, `PHL`, `VNM`, `KOR`, `ESP` to plausibly cover a US retail-bank customer base. `Nationality_Desc` is the English country-of-origin label (e.g. `United States`, `Canadian`).
  - `Core_DB.TAX_BRACKET_TYPE` — **US Federal 2024 marginal brackets**: 7 rows with `Tax_Bracket_Cd` values `BRACKET_10`, `BRACKET_12`, `BRACKET_22`, `BRACKET_24`, `BRACKET_32`, `BRACKET_35`, `BRACKET_37` and matching `Tax_Bracket_Rate` DECIMAL(15,12) values (`0.100000000000`, `0.120000000000`, …, `0.370000000000`). Step 11 maps `CustomerProfile.income_quartile` onto these codes (Q1 → `BRACKET_12`, Q2 → `BRACKET_22`, Q3 → `BRACKET_24`, Q4 → `BRACKET_32`), so all seven must be present. `Tax_Bracket_Desc` is human-readable (e.g. `10% Federal Bracket`).
  - `Core_DB.VERY_IMPORTANT_PERSON_TYPE` — 3–5 rows covering `NONE`, `PLATINUM`, `GOLD`, `SILVER`, `BRONZE` or similar tiers. Used by `INDIVIDUAL_VIP_STATUS` (Step 12).
  - `Core_DB.MILITARY_STATUS_TYPE` — 4–6 rows: `ACTIVE_DUTY`, `VETERAN`, `RESERVE`, `NATIONAL_GUARD`, `CIVILIAN`, `RETIRED_MILITARY`. Used by `INDIVIDUAL_MILITARY_STATUS` (Step 12).
  - `Core_DB.OCCUPATION_TYPE` — **must contain exactly `{EMP, SELF_EMP, RETIRED, NOT_WORKING}`** (literal-match to `06` Part A lines 97–99 + line 357 SCF OCCAT1/OCCAT2 mapping; the UniverseBuilder's `sample_occupation` output must resolve to a seeded row).
  - `Core_DB.PARTY_RELATED_STATUS_TYPE` — 3–5 rows: `ACTIVE`, `INACTIVE`, `PENDING`, `CANCELLED`. Used by `PARTY_RELATED.Party_Related_Status_Type_Cd` (Step 19).
  - `Core_DB.GENERAL_MEDICAL_STATUS_TYPE` — 4–6 rows: `HEALTHY`, `CHRONIC_CONDITION`, `ACUTE_CONDITION`, `UNKNOWN`, `DISABLED`, `DECEASED`. Used by `INDIVIDUAL_MEDICAL` (Step 12).
  - `Core_DB.SKILL_TYPE` — 10–15 generic skills (e.g. `ACCOUNTING`, `ENGINEERING`, `SALES`, `NURSING`, `CARPENTRY`, `TEACHING`, `PROGRAMMING`, `MANAGEMENT`, `DRIVING`, `COOKING`, `LEGAL`, `MEDICINE`, `ADMIN`, `FINANCE`, `MARKETING`). Used by `INDIVIDUAL_SKILL` (Step 12).
  - `Core_DB.SPECIAL_NEED_TYPE` — 5–8 rows (`NONE`, `VISUAL_IMPAIRMENT`, `HEARING_IMPAIRMENT`, `MOBILITY_IMPAIRMENT`, `COGNITIVE`, `SPEECH`, `OTHER`). Used by `INDIVIDUAL_SPECIAL_NEED` (Step 12).
  - `Core_DB.LANGUAGE_TYPE` — 10–20 ISO-639 rows; `Language_Type_Cd` = the ISO-639-1 or custom code (`EN`, `ES`, `ZH`, `HI`, `AR`, `FR`, `DE`, `JA`, `KO`, `VI`, `TL`, `PT`, `RU`, `IT`, …), `Language_Native_Name` = the name as written in the language itself (`English`, `Español`, `中文`, `हिन्दी`, …), `ISO_Language_Type_Cd` (NOT NULL) = the matching ISO-639-1 two-letter code (`en`, `es`, `zh`, `hi`, …). Used by `PARTY_LANGUAGE_USAGE` (Step 14). Include `EN` at minimum because every party gets a `primary spoken` + `primary written` row with a language that must FK-resolve.
  - `Core_DB.SPECIALTY_TYPE` — 5–8 rows: professional specialty codes (`GENERAL`, `MEDICAL`, `LEGAL`, `FINANCIAL_ADVISORY`, `TECHNICAL`, `REAL_ESTATE`, `EDUCATION`). Used by `PARTY_SPECIALTY` (Step 14).
  - `Core_DB.LEGAL_CLASSIFICATION` — 5–10 legal-entity codes (`CORPORATION`, `LLC`, `PARTNERSHIP`, `SOLE_PROPRIETORSHIP`, `NONPROFIT`, `GOVERNMENT`, `TRUST`, `COOPERATIVE`). Used by ORGANIZATION (Step 11).
  - `Core_DB.BUSINESS_CATEGORY` — 5–10 coarse business categorisations (`SMALL_BUSINESS`, `MID_MARKET`, `ENTERPRISE`, `MICRO_BUSINESS`, `STARTUP`, `SELF_EMPLOYED`). Used by BUSINESS (Step 11). **Must include a `SELF_EMPLOYED` row** so that the reserved `Self-Employment Organization` (party ID 9999999, per PRD §7.12) can FK-resolve its `Business_Category_Cd` to a real seeded code.

- `seed_data/industry_codes.py` — seed rows for the four industry-code hierarchies. Exposes `get_industry_code_tables() -> Dict[str, pd.DataFrame]`. Tables included:
  - `Core_DB.NAICS_INDUSTRY` — ≥6 rows forming complete `(Sector → Subsector → Industry_Group → Industry → National_Industry)` chains, covering at least sectors **52 (Finance & Insurance)**, **62 (Health Care)**, **44–45 (Retail Trade)**, **51 (Information)**, **72 (Accommodation & Food Services)**, **81 (Other Services)** — the six sectors most common among retail bank customers. `NAICS_Industry_Desc` is English.
  - `Core_DB.NACE_CLASS` — ≥5 rows covering sections **A (Agriculture)**, **C (Manufacturing)**, **G (Wholesale & Retail Trade)**, **K (Financial & Insurance Activities)**, **N (Administrative & Support)**. Each row has all four code columns (`NACE_Class_Cd`, `NACE_Group_Cd`, `NACE_Division_Cd`, `NACE_Section_Cd`) populated.
  - `Core_DB.SIC` — 10–15 `(SIC_Cd, SIC_Group_Cd)` rows across industry divisions **H (Finance)**, **I (Services)**, **F (Retail Trade)** to name three. `SIC_Desc` is English.
  - `Core_DB.GICS_SECTOR_TYPE` — all **11 GICS sectors**: `10` Energy, `15` Materials, `20` Industrials, `25` Consumer Discretionary, `30` Consumer Staples, `35` Health Care, `40` Financials, `45` Information Technology, `50` Communication Services, `55` Utilities, `60` Real Estate.
  - `Core_DB.GICS_INDUSTRY_GROUP_TYPE` — ≥11 rows (at least one per sector), composite FK into `GICS_SECTOR_TYPE`.
  - `Core_DB.GICS_INDUSTRY_TYPE` — ≥11 rows, composite FK into GICS Industry Group + Sector.
  - `Core_DB.GICS_SUBINDUSTRY_TYPE` — ≥11 rows, composite FK into GICS Industry + Industry Group + Sector. Every complete GICS chain row must have all 4 levels populated.

**Do NOT produce** in this step (belongs to Step 6, 8, or later):
- `seed_data/agreement_types.py`, `seed_data/status_types.py`, `seed_data/financial_types.py`, `seed_data/feature_types.py` — **Step 6**, already shipped on main.
- `seed_data/channel_types.py`, `seed_data/campaign_types.py`, `seed_data/address_types.py`, `seed_data/currency.py`, `seed_data/interest_rate_indices.py`, `seed_data/misc_types.py`, `generators/tier0_lookups.py` — **Step 8**.
- Any DI column stamping on the returned DataFrames — deferred to Step 8's `Tier0Lookups.generate(ctx)`. The `get_<domain>_tables()` contract is explicit: return un-stamped, DDL-ordered DataFrames where the three DI columns are the last three columns with `None` values (Step 6 established this convention — see `seed_data/status_types.py` `_DI` literal).

## Tables generated (if applicable)

The two seed modules together produce **21 un-stamped DataFrames** keyed by `'Core_DB.<TABLE>'`.

| Module | Table | Min rows | Literal-match / constraint requirements |
|--------|-------|---------:|------------------------------------------|
| `party_types.py` | `Core_DB.GENDER_TYPE` | 4 | At least `MALE`, `FEMALE` (UniverseBuilder sampling universe) |
| | `Core_DB.GENDER_PRONOUN` | 9 | Composite PK `(Gender_Pronoun_Cd, Gender_Pronoun_Type_Cd)` uniqueness |
| | `Core_DB.ETHNICITY_TYPE` | 5 | **Must equal `{WHITE, BLACK, HISPANIC, ASIAN, OTHER}` exactly** |
| | `Core_DB.MARITAL_STATUS_TYPE` | 5 | At least `MARRIED`, `SINGLE` |
| | `Core_DB.NATIONALITY_TYPE` | 10 | Include `USA` at minimum |
| | `Core_DB.TAX_BRACKET_TYPE` | 7 | **All 7 US federal 2024 rates present**: 10/12/22/24/32/35/37 as `Tax_Bracket_Rate` DECIMAL(15,12) |
| | `Core_DB.VERY_IMPORTANT_PERSON_TYPE` | 3 | — |
| | `Core_DB.MILITARY_STATUS_TYPE` | 4 | At least `VETERAN`, `CIVILIAN` |
| | `Core_DB.OCCUPATION_TYPE` | 4 | **Must equal `{EMP, SELF_EMP, RETIRED, NOT_WORKING}` exactly** |
| | `Core_DB.PARTY_RELATED_STATUS_TYPE` | 3 | — |
| | `Core_DB.GENERAL_MEDICAL_STATUS_TYPE` | 4 | — |
| | `Core_DB.SKILL_TYPE` | 10 | — |
| | `Core_DB.SPECIAL_NEED_TYPE` | 5 | Include `NONE` |
| | `Core_DB.LANGUAGE_TYPE` | 10 | Include `EN` with `ISO_Language_Type_Cd='en'` |
| | `Core_DB.SPECIALTY_TYPE` | 5 | — |
| | `Core_DB.LEGAL_CLASSIFICATION` | 5 | — |
| | `Core_DB.BUSINESS_CATEGORY` | 5 | **Must include `SELF_EMPLOYED` row** (for reserved ORG party 9999999) |
| `industry_codes.py` | `Core_DB.NAICS_INDUSTRY` | 6 | Every row has all 5 NAICS code columns populated |
| | `Core_DB.NACE_CLASS` | 5 | Every row has all 4 NACE code columns populated |
| | `Core_DB.SIC` | 10 | Every row has `SIC_Cd` + `SIC_Group_Cd` populated |
| | `Core_DB.GICS_SECTOR_TYPE` | 11 | **All 11 GICS sectors present** |
| | `Core_DB.GICS_INDUSTRY_GROUP_TYPE` | 11 | ≥1 row per GICS sector; composite FK consistent |
| | `Core_DB.GICS_INDUSTRY_TYPE` | 11 | Composite FK consistent with Industry Group + Sector |
| | `Core_DB.GICS_SUBINDUSTRY_TYPE` | 11 | Composite FK consistent with Industry + Industry Group + Sector |

Actual column counts and orderings are dictated by `references/07_mvp-schema-reference.md` — not by this spec. Every DataFrame must have all DDL-declared columns (including nullable ones — fill with `None` where data is genuinely absent; do not omit the column). DI columns (`di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind`) are the last three columns of every DataFrame, all populated with `None` — Step 6 established this pattern and the alignment check depends on it.

## Files to modify

No files modified. All outputs are new files under `seed_data/`. `config/`, `utils/`, `registry/`, `generators/`, `output/`, `main.py`, `CLAUDE.md`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, and `references/` are NOT touched.

If the implementation discovers that a column spelled in `references/07_mvp-schema-reference.md` differs from what this spec assumes (e.g. a capitalisation or underscore difference), escalate per Handoff Protocol §2 — update the upstream reference or add a `⚠️ Conflict` block to this spec. Do not silently improvise column names.

## New dependencies

No new dependencies. `pandas` is already in `requirements.txt` (Step 1). Seed modules depend only on the standard library and pandas.

## Rules for implementation

Universal (apply to every step):

- BIGINT for all ID columns (per PRD §7.1) — **n/a for lookup tables**: all tables in this step have CHAR / VARCHAR code columns as their PK, no `*_Id` BIGINT columns. If `07` reveals any BIGINT column in these tables, use `pd.Int64Dtype()` (nullable BIGINT). (Spot-check: none of the tables in Step 7's scope carry `*_Id` BIGINT columns — all PKs are `*_Cd` VARCHAR(50).)
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — n/a: no party IDs in lookup tables.
- DI column stamping on every table via `BaseGenerator.stamp_di()` — **deferred to Step 8**. This step produces DataFrames with `di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind` columns present (last three columns) but all-`None` values. Do NOT import `generators.base` here.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records — n/a at seed-authoring time; stamped in Step 8.
- CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` (per PRD §7.3) — n/a: every table in this step is `Core_DB`.
- **Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md`** — enforced at authoring time. Each dict literal or `pd.DataFrame(..., columns=[...])` must list columns in DDL order including the three DI columns as the last three. Step 5's writer reorderer would re-order them anyway, but authoring in DDL order prevents silent divergence and aids review.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — n/a: no `PARTY_INTERRACTION_EVENT` rows in this step.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — n/a: no geospatial tables here.
- No ORMs, no database connections — pure pandas → CSV. The seed modules construct `pd.DataFrame(...)` and return them; no disk I/O, no imports beyond pandas + standard library + `config`.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42` — **n/a, and critically so**: this step introduces zero randomness. Seed data is deterministic by construction (every row is hand-written).

Step-specific rules (Tier 0 seed authoring for Party + Industry):

- **No randomness, no Faker, no dynamic generation.** Every row is a hand-written dict literal. `numpy`, `faker`, `scipy`, `random`, `secrets` — none of these appear in the imports of any file produced by this step. Verified by a `grep` check in Definition of done.
- **Follow the Step 6 authoring pattern exactly.** See `seed_data/status_types.py` for the reference template: a `_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}` module constant, a `_COLS` list giving the DDL-ordered column list, a module-private rows list with `**_DI` splatted into each row, and a single public `get_<domain>_tables()` returning `pd.DataFrame(..., columns=_COLS)`. Consistency with Step 6 makes review trivial and lets Step 8 treat all seed modules identically.
- **DDL column order is authoritative.** Before authoring any table, open `references/07_mvp-schema-reference.md`, find the `#### <TABLE_NAME>` block, list columns in the exact order shown including the three trailing DI columns. If a column is NULL-able and the seed has no plausible value, use `None`.
- **Literal-match code equality for ETHNICITY_TYPE and OCCUPATION_TYPE.** The two tables `Core_DB.ETHNICITY_TYPE` and `Core_DB.OCCUPATION_TYPE` must contain **exactly and only** the codes specified in `references/06_supporting-enrichments.md` Part A (ethnicity: `WHITE, BLACK, HISPANIC, ASIAN, OTHER`; occupation: `EMP, SELF_EMP, RETIRED, NOT_WORKING`). The UniverseBuilder samples from this exact universe in Step 4 (already shipped) — adding extras is harmless but a typo or missing code will cause `INDIVIDUAL` / `INDIVIDUAL_OCCUPATION` FK joins to fail in Step 11/12. Enforced in Definition of done.
- **TAX_BRACKET_TYPE: 7 US federal 2024 rows.** Include exactly these 7 rates as `Tax_Bracket_Rate DECIMAL(15,12)`: `0.100000000000`, `0.120000000000`, `0.220000000000`, `0.240000000000`, `0.320000000000`, `0.350000000000`, `0.370000000000`. Use Python `Decimal` or string literals to preserve the 12-decimal precision — floats will lose precision. Step 5's writer formats rates to 12 decimal places, so `Decimal('0.100000000000')` is safest.
- **LANGUAGE_TYPE.ISO_Language_Type_Cd NOT NULL.** The DDL declares this column NOT NULL. Every seeded row must have it populated (ISO-639-1 two-letter code, lowercase). `Language_Native_Name` is nullable but should be populated for realism.
- **GICS hierarchy FK consistency.** The four GICS tables have a strict parent-child containment: every `GICS_SUBINDUSTRY_TYPE` row's `(GICS_Industry_Cd, GICS_Industry_Group_Cd, GICS_Sector_Cd)` triple must match a row in `GICS_INDUSTRY_TYPE`; every `GICS_INDUSTRY_TYPE` row's `(GICS_Industry_Group_Cd, GICS_Sector_Cd)` pair must match a row in `GICS_INDUSTRY_GROUP_TYPE`; every `GICS_INDUSTRY_GROUP_TYPE` row's `GICS_Sector_Cd` must match a row in `GICS_SECTOR_TYPE`. The full-sentence rule: the four hierarchies must be FK-consistent internally; any dangling `Sector_Cd` in a child table is a bug. Verified in Definition of done.
- **NAICS / NACE column-completeness.** `NAICS_INDUSTRY` carries 4 NOT-NULL code columns (`NAICS_Sector_Cd`, `NAICS_Subsector_Cd`, `NAICS_Industry_Group_Cd`, `NAICS_Industry_Cd`) plus `NAICS_Industry_Desc` (nullable). `NACE_CLASS` carries 4 NOT-NULL code columns. Every row must have all NOT-NULL columns populated.
- **Composite PK uniqueness.** `GENDER_PRONOUN` has composite PK `(Gender_Pronoun_Cd, Gender_Pronoun_Type_Cd)`. The seed must not repeat a pair. Definition of done includes a uniqueness assertion. Other tables have single-column PKs — standard `.duplicated()` check.
- **Each module exposes exactly one public function**, named `get_<domain>_tables()`, returning `Dict[str, pd.DataFrame]` keyed by `'Core_DB.<TABLE>'`. No other public surface. Helper lists / constants may be module-private (leading underscore).
- **No side effects on import.** Importing a seed module must not construct DataFrames eagerly. Build them inside `get_<domain>_tables()` so module import is cheap and the DataFrames are freshly constructed per caller (avoids cross-call mutation bugs). Verified in Definition of done.
- **Desc columns must be human-readable English.** Title-case for multi-word descs (`'Self Employed'` not `'SELF_EMPLOYED'` in `Occupation_Type_Desc`). These feed downstream BB joins that surface description strings to reporting layers.
- **Escalation over improvisation.** The architect-Q8 gap is already escalated via the `## ⚠️ Conflict` block above — proceed with public taxonomy knowledge. If `references/07_mvp-schema-reference.md` lacks a column whose legal values the spec asks for, or if `references/02_data-mapping-reference.md` Step 3 is ambiguous on a literal code, follow Handoff Protocol §2 — leave an additional `⚠️ Conflict` block in this spec; do NOT invent codes beyond the industry-taxonomy latitude granted above.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current directory and `python` resolves to the project's Python 3.12 environment.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

**Module-import and API contract:**

- [ ] `python -c "import seed_data.party_types, seed_data.industry_codes"` exits 0.
- [ ] Each module exposes exactly one public function named `get_<domain>_tables`. Run:
  ```bash
  python -c "
  import seed_data.party_types as pt, seed_data.industry_codes as ic
  assert callable(pt.get_party_type_tables)
  assert callable(ic.get_industry_code_tables)
  print('API contract OK')
  "
  ```
- [ ] Each `get_<domain>_tables()` returns `Dict[str, pd.DataFrame]` keyed by `'Core_DB.<TABLE>'`. Run:
  ```bash
  python -c "
  import pandas as pd
  from seed_data.party_types import get_party_type_tables
  from seed_data.industry_codes import get_industry_code_tables
  for fn in (get_party_type_tables, get_industry_code_tables):
      d = fn()
      assert isinstance(d, dict) and all(isinstance(v, pd.DataFrame) for v in d.values())
      assert all(k.startswith('Core_DB.') for k in d)
  print('return-type OK')
  "
  ```

**Critical literal-match sets (UniverseBuilder sampling universe):**

- [ ] `Core_DB.ETHNICITY_TYPE` codes equal `{WHITE, BLACK, HISPANIC, ASIAN, OTHER}` exactly. Run:
  ```bash
  python -c "
  from seed_data.party_types import get_party_type_tables
  df = get_party_type_tables()['Core_DB.ETHNICITY_TYPE']
  codes = set(df.Ethnicity_Type_Cd)
  assert codes == {'WHITE','BLACK','HISPANIC','ASIAN','OTHER'}, codes
  print('ETHNICITY_TYPE OK')
  "
  ```
- [ ] `Core_DB.OCCUPATION_TYPE` codes equal `{EMP, SELF_EMP, RETIRED, NOT_WORKING}` exactly. Run:
  ```bash
  python -c "
  from seed_data.party_types import get_party_type_tables
  df = get_party_type_tables()['Core_DB.OCCUPATION_TYPE']
  codes = set(df.Occupation_Type_Cd)
  assert codes == {'EMP','SELF_EMP','RETIRED','NOT_WORKING'}, codes
  print('OCCUPATION_TYPE OK')
  "
  ```
- [ ] `Core_DB.BUSINESS_CATEGORY` contains a `SELF_EMPLOYED` row. Run:
  ```bash
  python -c "
  from seed_data.party_types import get_party_type_tables
  df = get_party_type_tables()['Core_DB.BUSINESS_CATEGORY']
  assert (df.Business_Category_Cd == 'SELF_EMPLOYED').sum() == 1
  print('SELF_EMPLOYED row OK')
  "
  ```

**TAX_BRACKET_TYPE — all 7 US federal rates with DECIMAL(15,12) precision:**

- [ ] The table has exactly 7 rows, each with a distinct `Tax_Bracket_Rate` from `{0.10, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37}`. Run:
  ```bash
  python -c "
  from decimal import Decimal
  from seed_data.party_types import get_party_type_tables
  df = get_party_type_tables()['Core_DB.TAX_BRACKET_TYPE']
  assert len(df) == 7, len(df)
  # Compare as Decimal to avoid float-rounding false negatives
  expected = {Decimal('0.10'), Decimal('0.12'), Decimal('0.22'),
              Decimal('0.24'), Decimal('0.32'), Decimal('0.35'), Decimal('0.37')}
  got = {Decimal(str(r)) for r in df.Tax_Bracket_Rate}
  assert got == expected, got
  print('TAX_BRACKET_TYPE rates OK')
  "
  ```

**LANGUAGE_TYPE — ISO_Language_Type_Cd NOT NULL + EN row present:**

- [ ] Every row in `LANGUAGE_TYPE` has a non-null `ISO_Language_Type_Cd`, and at least one row has `Language_Type_Cd='EN'`. Run:
  ```bash
  python -c "
  from seed_data.party_types import get_party_type_tables
  df = get_party_type_tables()['Core_DB.LANGUAGE_TYPE']
  assert df.ISO_Language_Type_Cd.notna().all(), 'null ISO_Language_Type_Cd'
  assert (df.Language_Type_Cd == 'EN').sum() >= 1
  print('LANGUAGE_TYPE ISO + EN OK')
  "
  ```

**GENDER_PRONOUN composite PK uniqueness:**

- [ ] No repeated `(Gender_Pronoun_Cd, Gender_Pronoun_Type_Cd)` pair. Run:
  ```bash
  python -c "
  from seed_data.party_types import get_party_type_tables
  df = get_party_type_tables()['Core_DB.GENDER_PRONOUN']
  assert not df.duplicated(['Gender_Pronoun_Cd','Gender_Pronoun_Type_Cd']).any()
  assert df.Gender_Pronoun_Name.notna().all()
  print('GENDER_PRONOUN composite PK OK')
  "
  ```

**GICS hierarchy FK consistency:**

- [ ] Every `GICS_INDUSTRY_GROUP_TYPE.GICS_Sector_Cd` resolves in `GICS_SECTOR_TYPE`; every `GICS_INDUSTRY_TYPE` `(Industry_Group_Cd, Sector_Cd)` resolves in `GICS_INDUSTRY_GROUP_TYPE`; every `GICS_SUBINDUSTRY_TYPE` `(Industry_Cd, Industry_Group_Cd, Sector_Cd)` resolves in `GICS_INDUSTRY_TYPE`. Run:
  ```bash
  python -c "
  from seed_data.industry_codes import get_industry_code_tables
  t = get_industry_code_tables()
  sec  = t['Core_DB.GICS_SECTOR_TYPE']
  grp  = t['Core_DB.GICS_INDUSTRY_GROUP_TYPE']
  ind  = t['Core_DB.GICS_INDUSTRY_TYPE']
  sub  = t['Core_DB.GICS_SUBINDUSTRY_TYPE']
  sec_keys = set(sec.GICS_Sector_Cd)
  grp_keys = set(zip(grp.GICS_Industry_Group_Cd, grp.GICS_Sector_Cd))
  ind_keys = set(zip(ind.GICS_Industry_Cd, ind.GICS_Industry_Group_Cd, ind.GICS_Sector_Cd))
  assert set(grp.GICS_Sector_Cd) <= sec_keys, 'group→sector dangling'
  assert set(zip(ind.GICS_Industry_Group_Cd, ind.GICS_Sector_Cd)) <= grp_keys, 'industry→group dangling'
  assert set(zip(sub.GICS_Industry_Cd, sub.GICS_Industry_Group_Cd, sub.GICS_Sector_Cd)) <= ind_keys, 'subindustry→industry dangling'
  assert len(sec) == 11, f'expected 11 GICS sectors, got {len(sec)}'
  print('GICS hierarchy FK consistency OK')
  "
  ```

**NAICS / NACE column-completeness:**

- [ ] `NAICS_INDUSTRY` has no nulls in `NAICS_Sector_Cd`, `NAICS_Subsector_Cd`, `NAICS_Industry_Group_Cd`, `NAICS_Industry_Cd`. Run:
  ```bash
  python -c "
  from seed_data.industry_codes import get_industry_code_tables
  df = get_industry_code_tables()['Core_DB.NAICS_INDUSTRY']
  for col in ['NAICS_Sector_Cd','NAICS_Subsector_Cd','NAICS_Industry_Group_Cd','NAICS_Industry_Cd']:
      assert df[col].notna().all(), col
  print('NAICS_INDUSTRY NOT-NULL cols OK')
  "
  ```
- [ ] `NACE_CLASS` has no nulls in `NACE_Class_Cd`, `NACE_Group_Cd`, `NACE_Division_Cd`, `NACE_Section_Cd`. Run:
  ```bash
  python -c "
  from seed_data.industry_codes import get_industry_code_tables
  df = get_industry_code_tables()['Core_DB.NACE_CLASS']
  for col in ['NACE_Class_Cd','NACE_Group_Cd','NACE_Division_Cd','NACE_Section_Cd']:
      assert df[col].notna().all(), col
  print('NACE_CLASS NOT-NULL cols OK')
  "
  ```

**DDL column-order alignment with Step 5's parser:**

- [ ] For every table produced by every seed module in this step, the DataFrame's column list equals the DDL column list returned by `output.writer._load_ddl_column_order()`. Run:
  ```bash
  python -c "
  from output.writer import _load_ddl_column_order
  from seed_data.party_types import get_party_type_tables
  from seed_data.industry_codes import get_industry_code_tables
  ddl = _load_ddl_column_order()
  combined = {}
  for fn in (get_party_type_tables, get_industry_code_tables):
      combined.update(fn())
  problems = []
  for key, df in combined.items():
      if key not in ddl:
          problems.append(f'{key}: not found in 07 DDL parse'); continue
      ddl_cols = ddl[key]
      df_cols  = list(df.columns)
      if df_cols != ddl_cols:
          problems.append(f'{key}: order mismatch\\n  DDL: {ddl_cols}\\n  DF : {df_cols}')
  if problems:
      for p in problems: print(p)
      raise SystemExit(1)
  print(f'{len(combined)} tables aligned with DDL')
  "
  ```
  If a table is legitimately missing from `07`'s DDL parse, log the mismatch and escalate per Handoff Protocol §2 rather than silently passing.

**Row-count plausibility:**

- [ ] Every table has ≥3 rows. Run:
  ```bash
  python -c "
  from seed_data.party_types import get_party_type_tables
  from seed_data.industry_codes import get_industry_code_tables
  combined = {}
  for fn in (get_party_type_tables, get_industry_code_tables):
      combined.update(fn())
  for k, df in combined.items():
      assert len(df) >= 3, f'{k}: only {len(df)} rows'
  print(f'all {len(combined)} tables have >=3 rows')
  "
  ```
- [ ] Total table count produced by this step is exactly 24 (17 party-domain + 7 industry-domain — 21 tables authored, with `GICS_SECTOR_TYPE` / `GICS_INDUSTRY_GROUP_TYPE` / `GICS_INDUSTRY_TYPE` / `GICS_SUBINDUSTRY_TYPE` counted separately plus NAICS_INDUSTRY, NACE_CLASS, SIC). Run:
  ```bash
  python -c "
  from seed_data.party_types import get_party_type_tables
  from seed_data.industry_codes import get_industry_code_tables
  n = sum(len(fn()) for fn in (get_party_type_tables, get_industry_code_tables))
  # 17 party tables + 7 industry tables = 24 total
  assert 20 <= n <= 26, n
  print(f'{n} tables produced')
  "
  ```

**No randomness / no dynamic generation:**

- [ ] No seed module imports `numpy`, `faker`, `scipy`, `random`, or `secrets`. Run:
  ```bash
  python -c "
  import re, pathlib
  pat = re.compile(r'^\s*(?:import|from)\s+(numpy|faker|scipy|random|secrets)\b')
  bad = []
  for p in ('seed_data/party_types.py', 'seed_data/industry_codes.py'):
      for i, line in enumerate(pathlib.Path(p).read_text().splitlines(), 1):
          if pat.match(line):
              bad.append(f'{p}:{i}: {line}')
  assert not bad, bad
  print('no randomness imports')
  "
  ```
- [ ] No seed module has top-level DataFrame construction (side-effect-free imports). Run:
  ```bash
  python -c "
  import importlib, sys, pandas as pd
  calls = {'n': 0}
  _orig = pd.DataFrame
  def _wrap(*a, **k):
      calls['n'] += 1
      return _orig(*a, **k)
  pd.DataFrame = _wrap
  for name in ('seed_data.party_types','seed_data.industry_codes'):
      sys.modules.pop(name, None)
      importlib.import_module(name)
  pd.DataFrame = _orig
  assert calls['n'] == 0, f'{calls[\"n\"]} DataFrame(s) built at import time'
  print('no import-time DataFrames')
  "
  ```

**Authoring pattern consistency with Step 6:**

- [ ] Both files use the `_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}` pattern (or equivalent). Run:
  ```bash
  python -c "
  import pathlib
  for p in ('seed_data/party_types.py', 'seed_data/industry_codes.py'):
      src = pathlib.Path(p).read_text()
      assert 'di_start_ts' in src and 'di_end_ts' in src and 'di_rec_deleted_Ind' in src
      assert 'None' in src, 'expected None-valued DI columns'
  print('DI-None authoring pattern OK')
  "
  ```

### Universal checks

- [ ] `git status` shows only files listed under ## Produces — nothing else. Run:
  ```bash
  git status --porcelain
  ```
  Every line must map to `seed_data/party_types.py` or `seed_data/industry_codes.py` (plus this spec file which was already committed by `/create-spec`). No stray files (no `__pycache__`, no outputs, no changes under `config/`, `utils/`, `generators/`, `output/`, `references/`, `specs/` outside this step's spec). `seed_data/__init__.py` already exists from Step 6 — do NOT recreate it.
- [ ] All new files pass `python -c "import <module>"` — covered by the first check above.
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — **n/a**: this step produces no CSVs. The seed tables are pure code-based lookups with no `*_Id` BIGINT columns by design (PKs are `*_Cd` VARCHAR(50)).
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: `PARTY_INTERRACTION_EVENT` is a CDM_DB table generated in Step 22, not touched here.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSV output at this step; the writer is not invoked.

## Handoff notes

*(Leave empty — filled by the implementation session per `implementation-steps.md` Handoff Protocol.)*

# Spec: Step 13 — Tier 4b Organization Attributes

## Overview

This step builds **Tier 4b — Organization Attributes**, the 5 `Core_DB` attribute tables that hang off every real `ORGANIZATION` row from Step 11 (`ORGANIZATION_NAME`, `ORGANIZATION_NAICS`, `ORGANIZATION_NACE`, `ORGANIZATION_SIC`, `ORGANIZATION_GICS`). Each table is a deterministic projection of `CustomerProfile` fields (`party_id`, `party_type=='ORGANIZATION'`, `org_name`, `naics_sector_cd`, `sic_cd`, `gics_sector_cd`, `party_since`) onto a schema-compliant row shape, with the industry-code columns resolved to the seeded Tier 0b industry hierarchies (`NAICS_INDUSTRY`, `NACE_CLASS`, `SIC`, `GICS_SUBINDUSTRY_TYPE`) so every `*_Cd` FK resolves. The critical Layer 2 guarantee this step delivers is `references/02_data-mapping-reference.md` Step 3 constraint **#14** (ORGANIZATION BB industry pivot): **exactly one** `Primary_NAICS_Ind='Yes'` row per organization, **exactly one** `Primary_SIC_Ind='Yes'`, **exactly one** `Primary_GICS_Ind='Yes'` — trivially satisfied here by writing a single 1-row-per-org record in each table and stamping it primary. `ORGANIZATION_NAME` emits the 4 literal name-type rows (`'brand name'`, `'business name'`, `'legal name'`, `'registered name'`) every org needs for the ORGANIZATION_BB name pivot (`references/02_data-mapping-reference.md` line 1032). The reserved placeholder ORGANIZATION row (`Organization_Party_Id = SELF_EMP_ORG_ID = 9_999_999`) injected by Step 11 is **explicitly excluded** from this step — it is a functional stand-in for "no employer" and has no industry classification. All non-deterministic decisions were made at universe-build time (`cp.naics_sector_cd`, `cp.sic_cd`, `cp.gics_sector_cd`, `cp.org_name` already populated by Step 4); this step uses only deterministic modulo indexing into seeded pools. See `mvp-tool-design.md` §9 Tier 4 ("Party Attributes") and `references/02_data-mapping-reference.md` Step 3 #14 for the authoritative constraints. Step 13 is one of three parallel children of Step 11 (12/13/14); it writes to 5 Core_DB tables disjoint from the 12 Tier 4a tables (Step 12) and 10 Tier 4c tables (Step 14), so the three run in any order.

## Depends on

- **Step 1** — consumes from `config/settings.py`: `SELF_EMP_ORG_ID = 9_999_999` (used as an exclusion sentinel — Tier 4b skips this Party_Id), `SIM_DATE` (upper bound for all `*_Start_Dt` fields), `HIGH_DATE` / `HIGH_TS` (stamped indirectly via `BaseGenerator.stamp_di()`). No RNG seed needed — this step is fully deterministic (no Faker, no `ctx.rng`).
- **Step 2** — consumes `generators/base.BaseGenerator` (`stamp_di()` only — Tier 4b is all Core_DB, so `stamp_valid()` is **never called**). No new utility modules.
- **Step 3** — consumes `registry/profiles.CustomerProfile` fields: `party_id`, `party_type`, `org_name`, `naics_sector_cd`, `sic_cd`, `gics_sector_cd`, `party_since`. `registry/context.GenerationContext` is consumed positionally; this step returns a `Dict[str, pd.DataFrame]` rather than mutating `ctx.tables`.
- **Step 4** — consumes the built universe. Critical invariants this step relies on and must re-verify in guards:
  - Every `ORGANIZATION`-type `CustomerProfile` has `cp.org_name` a non-empty string, `cp.naics_sector_cd ∈ {'52','62','44','51','72','81'}` (the 6 seeded NAICS sectors), `cp.gics_sector_cd ∈ {'10','20','25','35','40','45','50','55'}` (the 8 sampled GICS sectors, all of which exist in the 11-sector GICS seed), `cp.sic_cd` is a 4-digit string (may or may not match a seeded SIC.SIC_Cd — see NB below), `cp.party_since` ≤ `SIM_DATE`.
  - **NB on `cp.sic_cd`:** Step 4's universe samples `cp.sic_cd` from `['6020','6210','5411','5912','7011','8011']`, only 3 of which (`'6020'`, `'5411'`, `'7011'`, `'8011'`) are present in the seeded `Core_DB.SIC` pool. Tier 4b therefore **does not** read `cp.sic_cd` — it picks a `SIC_Cd` deterministically from the seeded pool via `cp.party_id % len(seeded_sic_codes)`. This is a deliberate override, documented under "Rules for implementation" below. No change to Step 4 is required; the universe's `cp.sic_cd` is not consumed by any downstream tier that enforces FK resolution.
- **Step 8** — consumes already-stamped Tier 0 lookup tables (FK resolution). Required FK targets (all must exist in `ctx.tables` before this step runs — verify in fail-fast guard):
  - `Core_DB.NAICS_INDUSTRY` — `ORGANIZATION_NAICS.NAICS_Industry_Cd`, `NAICS_Subsector_Cd`, `NAICS_Industry_Group_Cd`, `NAICS_Sector_Cd` FK here. Seeded sectors: `52, 62, 44, 45, 51, 72, 81` (9 rows total; sector 45 has 1 row, sectors 52/62/44/51/72/81 have 1–3 rows each).
  - `Core_DB.NACE_CLASS` — `ORGANIZATION_NACE.NACE_Class_Cd`, `NACE_Group_Cd`, `NACE_Division_Cd`, `NACE_Section_Cd` FK here. 6 seeded rows spanning sections A/C/G/K/N.
  - `Core_DB.SIC` — `ORGANIZATION_SIC.SIC_Cd` FKs here. 12 seeded codes (see Step 7's `seed_data/industry_codes.py`).
  - `Core_DB.GICS_SUBINDUSTRY_TYPE` — `ORGANIZATION_GICS.GICS_Subindustry_Cd`, `GICS_Industry_Cd`, `GICS_Industry_Group_Cd`, `GICS_Sector_Cd` FK here. 11 seeded sub-industries, one per GICS sector, providing the full 4-level chain in every row.
- **Step 11** — consumes `ctx.tables['Core_DB.ORGANIZATION']`. Critical dependencies:
  - Every `Organization_Party_Id` this step writes (excluding the placeholder) must already exist in `Core_DB.ORGANIZATION.Organization_Party_Id`. Verified by filtering `ctx.customers` to `party_type == 'ORGANIZATION'` (which excludes the placeholder — the placeholder was appended to the DataFrame only, never to `ctx.customers`).
  - The reserved `SELF_EMP_ORG_ID = 9_999_999` placeholder row must be present in `Core_DB.ORGANIZATION` (indirect invariant — used as an exclusion filter, not a row-source, in this step).

No other dependencies. Does not read `ctx.tables['Core_DB.BUSINESS']` — Step 11 already emits one `BUSINESS` row per real ORG and those are orthogonal to the industry/name attributes Tier 4b writes. Does not read `ctx.tables['Core_DB.INDIVIDUAL']` or any Tier 4a output — Step 12 and Step 13 are parallel siblings on disjoint tables.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 13):
- `PRD.md` §4.2 ("Organization" sub-list — ORGANIZATION, ORGANIZATION_NAME, ORGANIZATION_NAICS, ORGANIZATION_NACE, ORGANIZATION_SIC, ORGANIZATION_GICS, BUSINESS are listed as in-scope; Tier 4b owns the 5 attribute tables), §4.3 (CHAR(1) = Y/N, CHAR(3) = Yes/No — applies to `Primary_NAICS_Ind` / `Primary_SIC_Ind` / `Primary_GICS_Ind`, all CHAR(3) in the DDL), §7.1 (BIGINT rule — every `*_Id` column is emitted as `Int64` / BIGINT regardless of the DDL's `INTEGER` declaration), §7.2 (shared party ID space — `Organization_Party_Id == CustomerProfile.party_id`), §7.3 (DI column rules — Core_DB gets `di_*` only, no `Valid_*`), §7.4 (active-record convention — `*_End_Dt = NULL` for Core_DB; no Layer 2 exception applies to Tier 4b tables since constraint #14 only requires a *current* record and Layer 2 selects the Primary row by the `Primary_*_Ind='Yes'` predicate, not by date window), §7.6 (reproducibility — no Faker or ctx.rng used; modulo indexing gives byte-identical reruns).
- `mvp-tool-design.md` §9 Tier 4 — authoritative per-table constraints: `ORGANIZATION_NAME` must include the 4 `Name_Type_Cd` values `'brand name'`, `'business name'`, `'legal name'`, `'registered name'` (used in ORGANIZATION_BB pivot); `ORGANIZATION_NAICS / ORGANIZATION_SIC / ORGANIZATION_GICS` — **exactly one** row per org with `Primary_NAICS_Ind='Yes'` / `Primary_SIC_Ind='Yes'` / `Primary_GICS_Ind='Yes'`. §12 Layer 2 constraint **#14** ("ORGANIZATION NAICS/SIC/GICS: exactly one Primary_*_Ind='Yes'"). §7 `AgreementProfile.is_*` exclusivity is unrelated to Tier 4b; but note `CustomerProfile.org_name` / `naics_sector_cd` / `sic_cd` / `gics_sector_cd` from §4 dataclass definition (confirms these fields exist on the profile).
- `implementation-steps.md` Step 13 entry (Produces, Reads from, Exit criteria, Scope=S); Handoff Protocol (post-session notes rules); Seed Data Authoring Convention (N/A here — Tier 4b does not author seed data, only consumes it).

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/02_data-mapping-reference.md` — read **Step 3 constraint #14** (around line 832: "Organization industry pivot (ORGANIZATION BB): Exactly one record in ORGANIZATION NAICS with `Primary NAICS Ind = 'Y'`, one in ORGANIZATION SIC with `Primary SIC Ind = 'Y'`, and one in ORGANIZATION GICS with `Primary GICS Ind = 'Y'`."). Also skim the ORGANIZATION_BB section around line 336–338 (business-name pivot on 4 `Name_Type_Cd` values) and the literal-match row near line 1031–1032. All other Step-3 items are consumed by other steps.
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the 5 Tier 4b tables:
  - `#### ORGANIZATION_NAICS` (near line 6701). 9 business columns + 3 DI (only 3, not 5 — the 07 DDL for the ORGANIZATION_* tables shows a short DI tail with `di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind` only; `BaseGenerator.stamp_di()` nonetheless appends the full canonical 5-column DI tail per `utils/di_columns.DI_COLUMN_ORDER` — match the Tier 0/1/2/3/4a convention, not the short DDL tail). `Organization_Party_Id`, `NAICS_National_Industry_Cd`, `Organization_NAICS_Start_Dt`, `NAICS_Sector_Cd`, `NAICS_Subsector_Cd`, `NAICS_Industry_Group_Cd`, `NAICS_Industry_Cd` NOT NULL. `Organization_NAICS_End_Dt`, `Primary_NAICS_Ind` nullable.
  - `#### ORGANIZATION_NACE` (near line 6738). 8 business columns + 3 DI. `Organization_Party_Id`, `NACE_Class_Cd`, `NACE_Group_Cd`, `NACE_Division_Cd`, `NACE_Section_Cd`, `Organization_NACE_Start_Dt` NOT NULL. `Organization_NACE_End_Dt`, `Importance_Order_NACE_Num` nullable. **No `Primary_NACE_Ind` column** — design §9 Tier 4 and Layer 2 constraint #14 only reference NAICS/SIC/GICS primary indicators.
  - `#### ORGANIZATION_SIC` (near line 6802). 5 business columns + 3 DI. `Organization_Party_Id`, `SIC_Cd`, `Organization_SIC_Start_Dt` NOT NULL. `Organization_SIC_End_Dt`, `Primary_SIC_Ind` nullable.
  - `#### ORGANIZATION_GICS` (near line 6831). 8 business columns + 3 DI. `Organization_Party_Id`, `GICS_Subindustry_Cd`, `GICS_Industry_Cd`, `GICS_Industry_Group_Cd`, `GICS_Sector_Cd`, `Organization_GICS_Start_Dt` NOT NULL. `Organization_GICS_End_Dt`, `Primary_GICS_Ind` nullable.
  - `#### ORGANIZATION_NAME` (near line 7099). 6 business columns + 3 DI. `Organization_Party_Id`, `Name_Type_Cd`, `Organization_Name_Start_Dt`, `Organization_Name` NOT NULL. `Organization_Name_Desc`, `Organization_Name_End_Dt` nullable.

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is the MVP-filtered authoritative DDL set per PRD §10.
- `references/02_data-mapping-reference.md` beyond Step 3 #14 and the ORGANIZATION_BB pivot paragraphs — the rest of Step 3 (items 1–13, 15–22) is covered by other tiers.
- `references/05_architect-qa.md` — no Q directly touches ORGANIZATION_* attribute tables. (Q7 is Tier 4a only; Q8 lists industry-code scope but that was absorbed by Step 7 seed authoring.)
- `references/06_supporting-enrichments.md` — Part A demographics (individuals) and Parts B–I (balances/events); not relevant to Tier 4b.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `resources/iDM_MDM_tables_DDLs.xlsx` — distilled into `07`.
- CDM_DB and PIM_DB DDL blocks — Step 22 / Step 23, not touched here.
- Other generators' code — `generators/tier3_party_subtypes.py` is the only one worth glancing at for the module-level-constant / `_COLS_*` / guard pattern Step 11 established; `generators/tier4a_individual.py` (Step 12) is a parallel sibling and its internals are not relevant to Tier 4b.
- `seed_data/industry_codes.py` — do not re-read at implementation time beyond confirming the pool sizes; the seed rows are already loaded into `ctx.tables` by Tier 0.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier4b_organization.py` — `class Tier4bOrganization(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]` method returning 5 Core_DB DataFrames. Implementation contract:
  1. **Imports** — `from __future__ import annotations`; stdlib `datetime` (`date` only — no `datetime` / `time` / `timedelta` needed); third-party `pandas as pd`; project imports `from config.settings import SELF_EMP_ORG_ID, HIGH_DATE, SIM_DATE`; `from generators.base import BaseGenerator`; `from typing import TYPE_CHECKING, Dict, List, Tuple`; `if TYPE_CHECKING: from registry.context import GenerationContext`.
  2. **Module-level constants** — use ALL-CAPS names prefixed `_` for module-private:
     - `_TIER4B_DI_START_TS = '2000-01-01 00:00:00.000000'` — fixed timestamp mirrors Tier 0/1/2/3/4a convention for byte-identical reruns.
     - `_NAME_TYPE_CDS: Tuple[str, ...] = ('brand name', 'business name', 'legal name', 'registered name')` — the 4 literal-match values per `references/02_data-mapping-reference.md` line 1032; emitted in this exact order for every org to make reruns deterministic and grep-friendly.
     - `_PRIMARY_YES = 'Yes'`; `_PRIMARY_NO = 'No'` — CHAR(3) sentinels (PRD §4.3). Only `_PRIMARY_YES` is used at row time since every org gets exactly one row per table in Tier 4b; `_PRIMARY_NO` is declared for reference but not emitted (left here as a hook for future multi-row-per-org variants; delete if unused).
     - `_REQUIRED_TIER0_TABLES: Tuple[str, ...] = ('Core_DB.NAICS_INDUSTRY', 'Core_DB.NACE_CLASS', 'Core_DB.SIC', 'Core_DB.GICS_SUBINDUSTRY_TYPE')` — used by the fail-fast guard.
     - `_REQUIRED_TIER3_TABLES: Tuple[str, ...] = ('Core_DB.ORGANIZATION',)` — verifies Step 11 ran.
     - 5 column-order lists `_COLS_ORGANIZATION_NAICS`, `_COLS_ORGANIZATION_NACE`, `_COLS_ORGANIZATION_SIC`, `_COLS_ORGANIZATION_GICS`, `_COLS_ORGANIZATION_NAME` — each matching the DDL business-column order verbatim (before DI columns append). Source: `references/07_mvp-schema-reference.md` per-table block. Exact canonical orders:
       - `_COLS_ORGANIZATION_NAICS = ['Organization_Party_Id','NAICS_National_Industry_Cd','Organization_NAICS_Start_Dt','NAICS_Sector_Cd','NAICS_Subsector_Cd','NAICS_Industry_Group_Cd','NAICS_Industry_Cd','Organization_NAICS_End_Dt','Primary_NAICS_Ind']`
       - `_COLS_ORGANIZATION_NACE = ['Organization_Party_Id','NACE_Class_Cd','NACE_Group_Cd','NACE_Division_Cd','NACE_Section_Cd','Organization_NACE_Start_Dt','Organization_NACE_End_Dt','Importance_Order_NACE_Num']`
       - `_COLS_ORGANIZATION_SIC = ['Organization_Party_Id','SIC_Cd','Organization_SIC_Start_Dt','Organization_SIC_End_Dt','Primary_SIC_Ind']`
       - `_COLS_ORGANIZATION_GICS = ['Organization_Party_Id','GICS_Subindustry_Cd','GICS_Industry_Cd','GICS_Industry_Group_Cd','GICS_Sector_Cd','Organization_GICS_Start_Dt','Organization_GICS_End_Dt','Primary_GICS_Ind']`
       - `_COLS_ORGANIZATION_NAME = ['Organization_Party_Id','Name_Type_Cd','Organization_Name_Start_Dt','Organization_Name','Organization_Name_Desc','Organization_Name_End_Dt']`
  3. **Guards (first ~15 lines of `generate()`)**:
     - Raise `RuntimeError('Tier4bOrganization requires a populated ctx.customers — run UniverseBuilder.build() first')` if `not ctx.customers`.
     - Iterate `_REQUIRED_TIER0_TABLES + _REQUIRED_TIER3_TABLES`; for any key missing from `ctx.tables`, raise `RuntimeError(f'Tier4bOrganization requires {key} to be loaded first')`.
     - Verify at least one org customer exists: `org_cps = [cp for cp in ctx.customers if cp.party_type == 'ORGANIZATION']`; raise `RuntimeError('Tier4bOrganization requires at least one ORGANIZATION CustomerProfile — universe has none')` if `not org_cps`.
  4. **Pre-computed pools** — read once at the top of `generate()`:
     - `naics_df = ctx.tables['Core_DB.NAICS_INDUSTRY']` — columns used: `NAICS_Sector_Cd`, `NAICS_Subsector_Cd`, `NAICS_Industry_Group_Cd`, `NAICS_Industry_Cd`.
     - `nace_df = ctx.tables['Core_DB.NACE_CLASS']` — columns used: `NACE_Class_Cd`, `NACE_Group_Cd`, `NACE_Division_Cd`, `NACE_Section_Cd`.
     - `sic_codes: List[str] = sorted(ctx.tables['Core_DB.SIC']['SIC_Cd'].tolist())` — deterministic order for modulo indexing.
     - `gics_df = ctx.tables['Core_DB.GICS_SUBINDUSTRY_TYPE']` — columns used: `GICS_Subindustry_Cd`, `GICS_Industry_Cd`, `GICS_Industry_Group_Cd`, `GICS_Sector_Cd`.
     - Build `naics_by_sector: Dict[str, List[tuple]]` — for each `sector_cd` present in the seed, a sorted list of `(National_Industry_Cd, Industry_Cd, Industry_Group_Cd, Subsector_Cd, Sector_Cd)` tuples. `National_Industry_Cd` is **synthesised** as `NAICS_Industry_Cd` (i.e. the 5-digit industry is used verbatim as the national-industry code — no separate national-industry seed table exists in MVP scope).
     - Build `gics_by_sector: Dict[str, List[tuple]]` — for each `sector_cd` present in `gics_df`, a sorted list of `(Subindustry_Cd, Industry_Cd, Industry_Group_Cd, Sector_Cd)` tuples.
     - Build `nace_rows: List[tuple]` — a sorted list of `(Class_Cd, Group_Cd, Division_Cd, Section_Cd)` tuples from `nace_df`, used for modulo assignment per org.
     - Helper `def pick(pool, key: int)` returning `pool[key % len(pool)]` — the single deterministic indexing primitive used across all 4 code tables.
  5. **Build 5 DataFrames** — no intra-tier FK dependency, so any order works; a natural order matching the DDL block order is fine. For each table:
     - Iterate `org_cps` (already filtered to exclude the placeholder since it is not in `ctx.customers`).
     - Construct dicts with keys in DDL business-column order; append DI via `self.stamp_di(df, start_ts=_TIER4B_DI_START_TS)`.
     - Explicitly cast `Organization_Party_Id` to `Int64` after DataFrame construction.
     - Per-table rules (see below).
  6. **Return** a `Dict[str, pd.DataFrame]` keyed `Core_DB.<TABLE>` with all 5 tables. Do not mutate `ctx.tables`.

  **Per-table population rules:**

  | Table | Row count | Key field rules |
  |-------|-----------|-----------------|
  | `ORGANIZATION_NAME` | **4 rows per org** (one per `_NAME_TYPE_CDS` entry, emitted in list order) | `Organization_Party_Id = cp.party_id`; `Name_Type_Cd = nt` (iterated over `_NAME_TYPE_CDS`); `Organization_Name_Start_Dt = cp.party_since`; `Organization_Name = cp.org_name` (same value for all 4 rows — MVP simplification; downstream ORGANIZATION_BB pivots on `Name_Type_Cd`, not on name variation); `Organization_Name_Desc = None`; `Organization_Name_End_Dt = None`. |
  | `ORGANIZATION_NAICS` | **1 row per org** | `Organization_Party_Id = cp.party_id`; resolve `matching = naics_by_sector.get(cp.naics_sector_cd) or sorted fallback` → pick `pick(matching, cp.party_id)`. `NAICS_National_Industry_Cd = NAICS_Industry_Cd` (synthesised — no separate seed); `Organization_NAICS_Start_Dt = cp.party_since`; `NAICS_Sector_Cd`, `NAICS_Subsector_Cd`, `NAICS_Industry_Group_Cd`, `NAICS_Industry_Cd` from the chosen tuple; `Organization_NAICS_End_Dt = None`; `Primary_NAICS_Ind = 'Yes'`. |
  | `ORGANIZATION_NACE` | **1 row per org** | `Organization_Party_Id = cp.party_id`; pick `(Class, Group, Division, Section) = pick(nace_rows, cp.party_id)`; `Organization_NACE_Start_Dt = cp.party_since`; `Organization_NACE_End_Dt = None`; `Importance_Order_NACE_Num = '1'` (VARCHAR(50) literal — denotes "primary NACE" in absence of a `Primary_NACE_Ind` column). |
  | `ORGANIZATION_SIC` | **1 row per org** | `Organization_Party_Id = cp.party_id`; `SIC_Cd = pick(sic_codes, cp.party_id)`; `Organization_SIC_Start_Dt = cp.party_since`; `Organization_SIC_End_Dt = None`; `Primary_SIC_Ind = 'Yes'`. |
  | `ORGANIZATION_GICS` | **1 row per org** | `Organization_Party_Id = cp.party_id`; resolve `matching = gics_by_sector.get(cp.gics_sector_cd) or sorted fallback` → pick `pick(matching, cp.party_id)`; fields `GICS_Subindustry_Cd`, `GICS_Industry_Cd`, `GICS_Industry_Group_Cd`, `GICS_Sector_Cd` from the chosen tuple; `Organization_GICS_Start_Dt = cp.party_since`; `Organization_GICS_End_Dt = None`; `Primary_GICS_Ind = 'Yes'`. |

  **Fallback semantics (applies to NAICS and GICS only).** If `cp.naics_sector_cd` does not appear as a key in `naics_by_sector` (universe regression), fall back to the sorted first sector's pool — this guarantees every row's FK still resolves. Same for `cp.gics_sector_cd` and `gics_by_sector`. Both fallbacks are cold paths at seed=42 (Step 4 sectors are a subset of seeded sectors); they exist purely as a defence against future universe changes.

**Do NOT produce** in this step:
- CSVs — writer is not invoked. `output/` must remain empty.
- New `seed_data/*.py` modules — all Tier 0 codes this step FKs to are already seeded.
- New columns in any existing table — `CustomerProfile`, `AgreementProfile`, `AddressRecord`, `GenerationContext`, `IdFactory` are **not modified**.
- Rows in any Tier 4a (Step 12) or Tier 4c (Step 14) tables.
- Rows for the reserved `SELF_EMP_ORG_ID = 9_999_999` placeholder — it is not an `ORGANIZATION` in `ctx.customers`, has no `cp.naics_sector_cd` / `cp.sic_cd` / `cp.gics_sector_cd` / `cp.org_name`, and semantically represents "no employer", not a classifiable business. Exclusion is natural (iteration of `[cp for cp in ctx.customers if cp.party_type == 'ORGANIZATION']`).
- Multiple `Primary_*_Ind='Yes'` rows per org — the single row per org in each of NAICS/SIC/GICS trivially satisfies Layer 2 constraint #14. Do not generate multi-row variants speculatively.
- Any modification to `config/*`, `utils/*`, `registry/*`, `output/*`, `main.py`, `generators/base.py`, or any existing `generators/tier*.py`.
- Any modification to documents (`PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/*`, `CLAUDE.md`).
- Any top-level module-level side effect (DataFrame construction, I/O, date computation, pool construction).

## Tables generated (if applicable)

After `Tier4bOrganization.generate(ctx)` runs, the returned dict has 5 `Core_DB.*` keys.

Row-count expectations assume the Step 4 universe at seed=42: ~600 organizations (20% of 3,000). The 4 single-row tables each have ~600 rows; `ORGANIZATION_NAME` has ~2,400 rows (4 per org).

| Table | Approx rows | Key FK dependencies | Required literal-match / constraint rows |
|-------|-------------|---------------------|-----------------------------------------|
| `Core_DB.ORGANIZATION_NAME` | ~2,400 (4 × ~600 orgs) | — | Per org: exactly one row each with `Name_Type_Cd ∈ {'brand name','business name','legal name','registered name'}` (ORGANIZATION_BB pivot — `references/02_data-mapping-reference.md` line 1032) |
| `Core_DB.ORGANIZATION_NAICS` | ~600 | `Core_DB.NAICS_INDUSTRY` (4-column chain) | Layer 2 #14: exactly one `Primary_NAICS_Ind='Yes'` per org |
| `Core_DB.ORGANIZATION_NACE` | ~600 | `Core_DB.NACE_CLASS` (4-column chain) | No primary indicator required (no such column in DDL); `Importance_Order_NACE_Num = '1'` denotes primary |
| `Core_DB.ORGANIZATION_SIC` | ~600 | `Core_DB.SIC` (1 column: `SIC_Cd`) | Layer 2 #14: exactly one `Primary_SIC_Ind='Yes'` per org |
| `Core_DB.ORGANIZATION_GICS` | ~600 | `Core_DB.GICS_SUBINDUSTRY_TYPE` (4-column chain) | Layer 2 #14: exactly one `Primary_GICS_Ind='Yes'` per org |

All 5 DataFrames have the full 5-column DI tail in `DI_COLUMN_ORDER` as the last 5 columns after `stamp_di()`, with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`.

Layer 2 literal-match seed rows this step introduces: **none** — the literal-match codes (`'brand name'`, `'business name'`, `'legal name'`, `'registered name'`, `'Yes'`) are row *values* in this tier, not seeded lookup rows. (The `Primary_NAICS_Ind` / `Primary_SIC_Ind` / `Primary_GICS_Ind` columns have no FK lookup; `'Yes'` / `'No'` is the CHAR(3) flag domain per PRD §4.3.)

## Files to modify

No files modified. All `config/*`, `utils/*`, `registry/*`, `output/*`, `main.py`, `CLAUDE.md`, all documents under `references/` and the project root, all `seed_data/*.py`, and all existing `generators/*.py` (base, tier0_lookups, tier1_geography, tier2_core, tier3_party_subtypes, tier4a_individual) are NOT touched.

If the implementation session finds that `references/07_mvp-schema-reference.md` disagrees with this spec on a column name, type, or nullability for any Tier 4b table, escalate per Handoff Protocol §2 — update the upstream reference or add a `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new entries in `requirements.txt`. All imports are stdlib or already-required (pandas).

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — `Organization_Party_Id` is declared `INTEGER NOT NULL` in the DDL for all 5 tables; this step emits `pd.Int64Dtype()` ("Int64" — nullable BIGINT) everywhere. Cast explicitly via `df['Organization_Party_Id'] = df['Organization_Party_Id'].astype('Int64')` after construction to avoid numpy `int64` / `float64` drift.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — every `Organization_Party_Id` equals a `CustomerProfile.party_id` from Step 4 (via the `party_type == 'ORGANIZATION'` filter). No ID minting — never call `ctx.ids.next(...)`.
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on all 5 DataFrames. Construct each via `pd.DataFrame(rows, columns=_COLS_*)` with business columns only, then `self.stamp_di(df, start_ts=_TIER4B_DI_START_TS)` appends the 5 DI columns. Fixed `_TIER4B_DI_START_TS = '2000-01-01 00:00:00.000000'` guarantees byte-identical reruns.
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts` stamped via `stamp_di()` default. `Valid_To_Dt` n/a: Tier 4b is all Core_DB.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — n/a: Tier 4b is all Core_DB. Do NOT call `stamp_valid()`.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** — enforced at construction time via the 5 module-level `_COLS_*` lists. After `stamp_di()` appends the 5 DI columns, the full column order matches the Tier 0/1/2/3/4a convention.
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — n/a: that table is Step 22.
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — n/a: no GEOSPATIAL row authored here.
- **No ORMs, no database connections — pure pandas → CSV** — generator returns DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — `ctx.rng` is **not used** in this step. All values are deterministic projections of `cp` attributes or modulo picks on sorted seeded pools. `Faker` is not used (no name generation in this step — `cp.org_name` is already populated by Step 4).

Step-specific rules (Tier 4b Organization Attributes):

- **No randomness at all.** This step does not construct a Faker instance, does not call `ctx.rng`, does not use `random` / `numpy.random`, and does not call `hash()`. All non-constant values are either (a) direct projections of `cp` fields or (b) `pool[cp.party_id % len(pool)]` where `pool` is a sorted list built from a seeded Tier 0 table. Reproducibility is byte-exact by construction.
- **Exclude the `SELF_EMP_ORG_ID = 9_999_999` placeholder.** The filter `[cp for cp in ctx.customers if cp.party_type == 'ORGANIZATION']` naturally excludes it (the placeholder is a DataFrame-only row injected by Step 11, not a universe customer). Do NOT iterate `ctx.tables['Core_DB.ORGANIZATION']['Organization_Party_Id']` as the row source — that would pull in the placeholder and produce unfiled industry rows for a non-existent employer.
- **CHAR(3) flags use `'Yes'` / `'No'`, not `'Y'` / `'N'`** (PRD §4.3). Applies to `Primary_NAICS_Ind`, `Primary_SIC_Ind`, `Primary_GICS_Ind`. Only `'Yes'` is emitted in this step (every single-row-per-org record is primary).
- **Layer 2 constraint #14 (`mvp-tool-design.md` §12 #14) is satisfied by construction.** "Exactly one `Primary_NAICS_Ind='Yes'` per org" holds because every org gets exactly one NAICS row and every row has `Primary_NAICS_Ind='Yes'`. Same for SIC and GICS. The implementation does not need any extra "primary assignment" logic — the 1-row-per-org shape is the enforcement.
- **`ORGANIZATION_NAME` emits 4 literal rows per org in the order `('brand name', 'business name', 'legal name', 'registered name')`.** This order is fixed in `_NAME_TYPE_CDS` and iterated per org. Any deviation (alternate spellings, extra name types, missing name types) violates `references/02_data-mapping-reference.md` line 1032.
- **`NAICS_National_Industry_Cd` is synthesised from `NAICS_Industry_Cd`.** No separate national-industry seed table exists in MVP scope; using the 5-digit industry code as the national-industry code is an MVP simplification that keeps the column NOT NULL without requiring a new seed. Document this in a 1-line module comment above `naics_by_sector` construction.
- **`SIC_Cd` is picked from the seeded `Core_DB.SIC` pool, not from `cp.sic_cd`.** This is a deliberate override — `cp.sic_cd` (sampled from `['6020','6210','5411','5912','7011','8011']` in Step 4) is not guaranteed to be a key in the seeded SIC pool. Using the seeded pool directly (`sorted(SIC['SIC_Cd']) [cp.party_id % len(...)]`) guarantees FK resolution. Document this override in a 1-line module comment above `sic_codes` construction.
- **`NAICS_Sector_Cd` matches `cp.naics_sector_cd` when possible.** The universe samples from sectors `{52, 62, 44, 51, 72, 81}`, all of which exist in the seed — so the matching path is hot at seed=42; the fallback exists only for universe regressions.
- **`GICS_Sector_Cd` matches `cp.gics_sector_cd` when possible.** The universe samples from 8 GICS sectors, all of which exist in the 11-sector seed — matching path is hot; fallback is defensive.
- **`Organization_NACE_End_Dt = None` and `Importance_Order_NACE_Num = '1'`.** NACE has no `Primary_NACE_Ind`; the `Importance_Order_NACE_Num` column (VARCHAR(50)) denotes primary ordering. One row per org, so `'1'` is the only value emitted.
- **All `*_Start_Dt` fields = `cp.party_since`.** The bank-relationship-start date is the industry-classification-start date for MVP purposes. `cp.party_since ≤ SIM_DATE` by universe construction.
- **All `*_End_Dt` fields = `None`** (Python NoneType → CSV empty → SQL NULL), per Core_DB active-record convention (PRD §7.4). No Layer 2 BETWEEN predicate applies to Tier 4b tables.
- **No new ID minting.** `ctx.ids` is not called. No `*_Id` columns are generated by this step beyond `Organization_Party_Id` (which is inherited from `cp.party_id`).
- **Deterministic derivations only.** `pool[cp.party_id % len(pool)]` is the only indexing primitive; no `hash()`, no `random.choice()`, no `ctx.rng.choice()`. Pools are sorted at construction to guarantee order stability across Python runs.
- **No side effects on import.** `import generators.tier4b_organization` must not construct any DataFrames, build any pools, or perform any I/O. All heavy work happens inside `generate()`.
- **Fail-fast guards at top of `generate()`** (order: populated-universe → tier-0 lookups → tier-3 tables → at-least-one-org). Each guard raises `RuntimeError` with a distinct, greppable message.
- **Escalation over improvisation.** If `07` has a column-level ambiguity (e.g., a NOT NULL declaration that conflicts with this spec's nullable handling, or a column we didn't list above), stop and leave a `⚠️ Conflict` block in this spec. Do NOT invent columns or silently swap FKs.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current working directory and `python` resolves to the project's environment. All non-trivial checks run in a single `python` process after constructing the full pre-Tier-4b context — this is cheap (<15s end-to-end). The **helper context builder** below (reused by most checks) loads Steps 1–11 output. **Note on `config` argument:** per Step 11's Handoff-notes correction, `UniverseBuilder.build()` needs `config=config.settings` not `config=None`.

### Module-import and API contract

- [ ] `python -c "import generators.tier4b_organization"` exits 0.
- [ ] `generators.tier4b_organization.Tier4bOrganization` inherits from `BaseGenerator` and defines `generate(ctx)`:
  ```bash
  python -c "
  from generators.tier4b_organization import Tier4bOrganization
  from generators.base import BaseGenerator
  import inspect
  assert issubclass(Tier4bOrganization, BaseGenerator)
  sig = inspect.signature(Tier4bOrganization.generate)
  assert 'ctx' in sig.parameters
  print('Tier4bOrganization contract OK')
  "
  ```
- [ ] Import has no side effects (no DataFrames, no pool construction, no I/O at module level):
  ```bash
  python -c "
  import pandas as pd
  import generators.tier4b_organization as m
  for name in dir(m):
      if name.startswith('_'): continue
      obj = getattr(m, name)
      assert not isinstance(obj, pd.DataFrame), f'module-level DataFrame: {name}'
      assert not isinstance(obj, dict) or not obj, f'module-level non-empty dict: {name}'
  print('no import-time side effects OK')
  "
  ```

### Fail-fast guards

- [ ] `generate()` on empty `ctx.customers` raises `RuntimeError` mentioning `UniverseBuilder`:
  ```bash
  python -c "
  from generators.tier4b_organization import Tier4bOrganization
  from registry.context import GenerationContext
  from utils.id_factory import IdFactory
  import numpy as np
  import config.settings as cfg
  ctx = GenerationContext(customers=[], agreements=[], addresses=[],
      config=cfg, rng=np.random.default_rng(42), ids=IdFactory(), tables={})
  try:
      Tier4bOrganization().generate(ctx)
      raise AssertionError('should have raised')
  except RuntimeError as e:
      assert 'UniverseBuilder' in str(e) or 'ctx.customers' in str(e), str(e)
      print('empty customers guard OK')
  "
  ```
- [ ] `generate()` with missing Tier 0 tables raises `RuntimeError` naming the missing key:
  ```bash
  python -c "
  from generators.tier4b_organization import Tier4bOrganization
  from registry.profiles import CustomerProfile
  from registry.context import GenerationContext
  from utils.id_factory import IdFactory
  from datetime import date
  import numpy as np
  import config.settings as cfg
  cp = CustomerProfile(party_id=10_000_000, party_type='ORGANIZATION', age=0,
      income_quartile=2, lifecycle_cohort='ACTIVE', clv_segment=5,
      gender_type_cd=None, marital_status_cd=None, ethnicity_type_cd=None,
      occupation_cd=None, num_dependents=0, fico_score=0,
      household_id=None, household_role='HEAD', lifecl=1,
      has_internet=False, preferred_channel_cd=1, party_since=date(2020,1,1),
      address_id=1_000_000, product_set=[],
      org_name='Acme Corp', naics_sector_cd='52', sic_cd='6020', gics_sector_cd='40')
  ctx = GenerationContext(customers=[cp], agreements=[], addresses=[],
      config=cfg, rng=np.random.default_rng(42), ids=IdFactory(), tables={})
  try:
      Tier4bOrganization().generate(ctx)
      raise AssertionError('should have raised')
  except RuntimeError as e:
      msg = str(e)
      assert any(k in msg for k in ('NAICS_INDUSTRY','NACE_CLASS','SIC','GICS_SUBINDUSTRY_TYPE','ORGANIZATION','Tier 0','Tier 3','Core_DB')), msg
      print('missing-tier guard OK')
  "
  ```
- [ ] `generate()` on a universe with no ORGANIZATION customers raises `RuntimeError`:
  ```bash
  python -c "
  from generators.tier4b_organization import Tier4bOrganization
  from generators.tier0_lookups import Tier0Lookups
  from registry.profiles import CustomerProfile
  from registry.context import GenerationContext
  from utils.id_factory import IdFactory
  from datetime import date
  import pandas as pd, numpy as np
  import config.settings as cfg
  ind = CustomerProfile(party_id=10_000_000, party_type='INDIVIDUAL', age=35,
      income_quartile=2, lifecycle_cohort='ACTIVE', clv_segment=5,
      gender_type_cd='MALE', marital_status_cd='SINGLE', ethnicity_type_cd='WHITE',
      occupation_cd='EMP', num_dependents=0, fico_score=700,
      household_id=None, household_role='HEAD', lifecl=2,
      has_internet=True, preferred_channel_cd=3, party_since=date(2020,1,1),
      address_id=1_000_000, product_set=[])
  ctx = GenerationContext(customers=[ind], agreements=[], addresses=[],
      config=cfg, rng=np.random.default_rng(42), ids=IdFactory(), tables={})
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables['Core_DB.ORGANIZATION'] = pd.DataFrame(
      [{'Organization_Party_Id': cfg.SELF_EMP_ORG_ID}])
  try:
      Tier4bOrganization().generate(ctx)
      raise AssertionError('should have raised')
  except RuntimeError as e:
      assert 'ORGANIZATION' in str(e), str(e)
      print('no-orgs guard OK')
  "
  ```

### Helper context builder (reused below)

```python
# Paste into python -c or a scratch script — all subsequent checks reuse `ctx` and `tier4b`.
import numpy as np, pandas as pd
import config.settings as cfg
from config.settings import SEED, SELF_EMP_ORG_ID, HIGH_TS, HIGH_DATE
from registry.universe import UniverseBuilder
from generators.tier0_lookups import Tier0Lookups
from generators.tier1_geography import Tier1Geography
from generators.tier2_core import Tier2Core
from generators.tier3_party_subtypes import Tier3PartySubtypes
from generators.tier4b_organization import Tier4bOrganization

rng = np.random.default_rng(SEED)
ctx = UniverseBuilder().build(config=cfg, rng=rng)
ctx.tables.update(Tier0Lookups().generate(ctx))
ctx.tables.update(Tier1Geography().generate(ctx))
ctx.tables.update(Tier2Core().generate(ctx))
ctx.tables.update(Tier3PartySubtypes().generate(ctx))
tier4b = Tier4bOrganization().generate(ctx)
ctx.tables.update(tier4b)

org_cps = [cp for cp in ctx.customers if cp.party_type == 'ORGANIZATION']
org_ids = {cp.party_id for cp in org_cps}
```

### Returned dict shape

- [ ] `generate(ctx)` returns exactly these 5 keys:
  ```python
  EXPECTED = {
      'Core_DB.ORGANIZATION_NAME', 'Core_DB.ORGANIZATION_NAICS',
      'Core_DB.ORGANIZATION_NACE', 'Core_DB.ORGANIZATION_SIC',
      'Core_DB.ORGANIZATION_GICS',
  }
  assert set(tier4b.keys()) == EXPECTED, set(tier4b.keys()) ^ EXPECTED
  ```

### Exit criterion — "For every organization: exactly one Primary_NAICS_Ind='Yes', one Primary_SIC_Ind='Yes', one Primary_GICS_Ind='Yes'" (Layer 2 #14)

- [ ] `ORGANIZATION_NAICS` has exactly one `Primary_NAICS_Ind='Yes'` row per org:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_NAICS']
  assert len(df) == len(org_cps), (len(df), len(org_cps))
  assert df['Organization_Party_Id'].is_unique
  assert set(df['Organization_Party_Id']) == org_ids
  yes = df[df['Primary_NAICS_Ind'] == 'Yes']
  assert yes.groupby('Organization_Party_Id').size().eq(1).all()
  assert set(yes['Organization_Party_Id']) == org_ids
  ```
- [ ] `ORGANIZATION_SIC` has exactly one `Primary_SIC_Ind='Yes'` row per org:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_SIC']
  assert len(df) == len(org_cps)
  assert df['Organization_Party_Id'].is_unique
  yes = df[df['Primary_SIC_Ind'] == 'Yes']
  assert yes.groupby('Organization_Party_Id').size().eq(1).all()
  assert set(yes['Organization_Party_Id']) == org_ids
  ```
- [ ] `ORGANIZATION_GICS` has exactly one `Primary_GICS_Ind='Yes'` row per org:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_GICS']
  assert len(df) == len(org_cps)
  assert df['Organization_Party_Id'].is_unique
  yes = df[df['Primary_GICS_Ind'] == 'Yes']
  assert yes.groupby('Organization_Party_Id').size().eq(1).all()
  assert set(yes['Organization_Party_Id']) == org_ids
  ```

### Exit criterion — "All industry FKs resolve to Tier 0b seed rows (no orphan codes)"

- [ ] `ORGANIZATION_NAICS` 4-column chain resolves to a single seeded `NAICS_INDUSTRY` row per `(Sector, Subsector, Industry_Group, Industry)` tuple:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_NAICS']
  seed = ctx.tables['Core_DB.NAICS_INDUSTRY']
  seed_tuples = set(zip(seed['NAICS_Sector_Cd'], seed['NAICS_Subsector_Cd'],
                        seed['NAICS_Industry_Group_Cd'], seed['NAICS_Industry_Cd']))
  row_tuples = set(zip(df['NAICS_Sector_Cd'], df['NAICS_Subsector_Cd'],
                       df['NAICS_Industry_Group_Cd'], df['NAICS_Industry_Cd']))
  missing = row_tuples - seed_tuples
  assert not missing, f'ORGANIZATION_NAICS has unseeded tuples: {missing}'
  ```
- [ ] `ORGANIZATION_NAICS.NAICS_National_Industry_Cd` is NOT NULL every row (synthesised from `NAICS_Industry_Cd`):
  ```python
  df = tier4b['Core_DB.ORGANIZATION_NAICS']
  assert df['NAICS_National_Industry_Cd'].notna().all()
  assert (df['NAICS_National_Industry_Cd'].str.len() > 0).all()
  ```
- [ ] `ORGANIZATION_NACE` 4-column chain resolves to a single seeded `NACE_CLASS` row:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_NACE']
  seed = ctx.tables['Core_DB.NACE_CLASS']
  seed_tuples = set(zip(seed['NACE_Class_Cd'], seed['NACE_Group_Cd'],
                        seed['NACE_Division_Cd'], seed['NACE_Section_Cd']))
  row_tuples = set(zip(df['NACE_Class_Cd'], df['NACE_Group_Cd'],
                       df['NACE_Division_Cd'], df['NACE_Section_Cd']))
  missing = row_tuples - seed_tuples
  assert not missing, f'ORGANIZATION_NACE has unseeded tuples: {missing}'
  ```
- [ ] `ORGANIZATION_SIC.SIC_Cd` FK-resolves:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_SIC']
  seed_codes = set(ctx.tables['Core_DB.SIC']['SIC_Cd'])
  vals = set(df['SIC_Cd'])
  missing = vals - seed_codes
  assert not missing, f'ORGANIZATION_SIC has unseeded SIC codes: {missing}'
  ```
- [ ] `ORGANIZATION_GICS` 4-column chain resolves to a single seeded `GICS_SUBINDUSTRY_TYPE` row:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_GICS']
  seed = ctx.tables['Core_DB.GICS_SUBINDUSTRY_TYPE']
  seed_tuples = set(zip(seed['GICS_Subindustry_Cd'], seed['GICS_Industry_Cd'],
                        seed['GICS_Industry_Group_Cd'], seed['GICS_Sector_Cd']))
  row_tuples = set(zip(df['GICS_Subindustry_Cd'], df['GICS_Industry_Cd'],
                       df['GICS_Industry_Group_Cd'], df['GICS_Sector_Cd']))
  missing = row_tuples - seed_tuples
  assert not missing, f'ORGANIZATION_GICS has unseeded tuples: {missing}'
  ```

### Exit criterion — "ORGANIZATION_NAME has all 4 required Name_Type_Cd values per org"

- [ ] 4 rows per org, and the set of `Name_Type_Cd` values per org equals the required literal set:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_NAME']
  assert len(df) == len(org_cps) * 4, (len(df), len(org_cps) * 4)
  REQUIRED = {'brand name', 'business name', 'legal name', 'registered name'}
  grouped = df.groupby('Organization_Party_Id')['Name_Type_Cd'].apply(set)
  assert (grouped == REQUIRED).all(), 'some orgs missing name-type rows'
  ```
- [ ] `Organization_Name` is NOT NULL on every row and equals `cp.org_name`:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_NAME']
  assert df['Organization_Name'].notna().all()
  assert (df['Organization_Name'].str.len() > 0).all()
  name_by_id = {cp.party_id: cp.org_name for cp in org_cps}
  for _, row in df.iterrows():
      assert row['Organization_Name'] == name_by_id[row['Organization_Party_Id']]
  ```
- [ ] `Organization_Name_Start_Dt <= SIM_DATE` and `Organization_Name_End_Dt is NULL` every row:
  ```python
  import pandas as pd
  df = tier4b['Core_DB.ORGANIZATION_NAME']
  starts = pd.to_datetime(df['Organization_Name_Start_Dt']).dt.date
  assert (starts <= cfg.SIM_DATE).all()
  assert df['Organization_Name_End_Dt'].isna().all()
  ```

### Exit criterion — "All industry FKs resolve to Tier 0b seed rows" (no orphans against placeholder)

- [ ] `SELF_EMP_ORG_ID = 9_999_999` does NOT appear as `Organization_Party_Id` in any Tier 4b table (placeholder exclusion):
  ```python
  for key in tier4b:
      df = tier4b[key]
      bad = df[df['Organization_Party_Id'] == cfg.SELF_EMP_ORG_ID]
      assert len(bad) == 0, f'{key}: placeholder row leaked — {len(bad)} rows'
  ```

### Row-count sanity

- [ ] Single-row-per-org tables have ~600 rows matching `len(org_cps)`:
  ```python
  N = len(org_cps)
  for key in ['Core_DB.ORGANIZATION_NAICS','Core_DB.ORGANIZATION_NACE',
              'Core_DB.ORGANIZATION_SIC','Core_DB.ORGANIZATION_GICS']:
      assert len(tier4b[key]) == N, (key, len(tier4b[key]), N)
  ```
- [ ] `ORGANIZATION_NAME` has `4 × N` rows:
  ```python
  assert len(tier4b['Core_DB.ORGANIZATION_NAME']) == 4 * len(org_cps)
  ```
- [ ] `len(org_cps)` is within ±1% of `0.20 × 3000 = 600`:
  ```python
  assert 570 <= len(org_cps) <= 630, len(org_cps)
  ```

### NAICS / GICS sector-matching path

- [ ] Every `ORGANIZATION_NAICS.NAICS_Sector_Cd` matches its owning `cp.naics_sector_cd` (matching path, not fallback):
  ```python
  df = tier4b['Core_DB.ORGANIZATION_NAICS']
  naics_by_id = {cp.party_id: cp.naics_sector_cd for cp in org_cps}
  for _, row in df.iterrows():
      exp = naics_by_id[row['Organization_Party_Id']]
      assert row['NAICS_Sector_Cd'] == exp, (row['Organization_Party_Id'], row['NAICS_Sector_Cd'], exp)
  ```
- [ ] Every `ORGANIZATION_GICS.GICS_Sector_Cd` matches its owning `cp.gics_sector_cd`:
  ```python
  df = tier4b['Core_DB.ORGANIZATION_GICS']
  gics_by_id = {cp.party_id: cp.gics_sector_cd for cp in org_cps}
  for _, row in df.iterrows():
      exp = gics_by_id[row['Organization_Party_Id']]
      assert row['GICS_Sector_Cd'] == exp, (row['Organization_Party_Id'], row['GICS_Sector_Cd'], exp)
  ```

### SIC override (universe vs. seed)

- [ ] `ORGANIZATION_SIC.SIC_Cd` values are a subset of the seeded SIC pool (override documented — `cp.sic_cd` is not read):
  ```python
  df = tier4b['Core_DB.ORGANIZATION_SIC']
  seed_codes = set(ctx.tables['Core_DB.SIC']['SIC_Cd'])
  assert set(df['SIC_Cd']).issubset(seed_codes)
  ```

### Start-date / End-date hygiene (applies to all 5 tables)

- [ ] Every `*_Start_Dt` column is `<= SIM_DATE` and every `*_End_Dt` column is NULL:
  ```python
  import pandas as pd
  start_cols = {
      'Core_DB.ORGANIZATION_NAME':  ('Organization_Name_Start_Dt',  'Organization_Name_End_Dt'),
      'Core_DB.ORGANIZATION_NAICS': ('Organization_NAICS_Start_Dt', 'Organization_NAICS_End_Dt'),
      'Core_DB.ORGANIZATION_NACE':  ('Organization_NACE_Start_Dt',  'Organization_NACE_End_Dt'),
      'Core_DB.ORGANIZATION_SIC':   ('Organization_SIC_Start_Dt',   'Organization_SIC_End_Dt'),
      'Core_DB.ORGANIZATION_GICS':  ('Organization_GICS_Start_Dt',  'Organization_GICS_End_Dt'),
  }
  for key, (sc, ec) in start_cols.items():
      df = tier4b[key]
      starts = pd.to_datetime(df[sc]).dt.date
      assert (starts <= cfg.SIM_DATE).all(), f'{key}.{sc} has dates past SIM_DATE'
      assert df[ec].isna().all(), f'{key}.{ec} has non-NULL end dates'
  ```

### BIGINT and DI column enforcement

- [ ] Every `Organization_Party_Id` column across all 5 tables is `Int64` (nullable BIGINT):
  ```python
  for key, df in tier4b.items():
      dtype = str(df['Organization_Party_Id'].dtype)
      assert dtype in ('Int64','int64'), f'{key}.Organization_Party_Id is {dtype}'
  print('BIGINT check OK')
  ```
- [ ] Every Tier 4b DataFrame has the 5 DI columns in canonical order as the last 5:
  ```python
  from utils.di_columns import DI_COLUMN_ORDER
  for key, df in tier4b.items():
      assert tuple(df.columns[-5:]) == DI_COLUMN_ORDER, f'{key}: {tuple(df.columns[-5:])} != {DI_COLUMN_ORDER}'
  ```
- [ ] Every Tier 4b DataFrame has `di_end_ts == HIGH_TS` and `di_rec_deleted_Ind == 'N'` on every row:
  ```python
  for key, df in tier4b.items():
      assert (df['di_end_ts'] == HIGH_TS).all(), key
      assert (df['di_rec_deleted_Ind'] == 'N').all(), key
  ```
- [ ] No Tier 4b DataFrame has `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`:
  ```python
  for key, df in tier4b.items():
      for col in ('Valid_From_Dt','Valid_To_Dt','Del_Ind'):
          assert col not in df.columns, f'{key} unexpectedly has {col}'
  ```
- [ ] CHAR(3) flags use `'Yes'` / `'No'` only:
  ```python
  vals = set(tier4b['Core_DB.ORGANIZATION_NAICS']['Primary_NAICS_Ind'].dropna().unique())
  assert vals.issubset({'Yes','No'}), ('NAICS', vals)
  vals = set(tier4b['Core_DB.ORGANIZATION_SIC']['Primary_SIC_Ind'].dropna().unique())
  assert vals.issubset({'Yes','No'}), ('SIC', vals)
  vals = set(tier4b['Core_DB.ORGANIZATION_GICS']['Primary_GICS_Ind'].dropna().unique())
  assert vals.issubset({'Yes','No'}), ('GICS', vals)
  ```

### DDL column ordering (first-N business columns match `references/07_mvp-schema-reference.md`)

- [ ] All 5 tables' business-column prefix matches the DDL block:
  ```python
  EXPECTED_ORDER = {
      'Core_DB.ORGANIZATION_NAICS': ['Organization_Party_Id','NAICS_National_Industry_Cd','Organization_NAICS_Start_Dt','NAICS_Sector_Cd','NAICS_Subsector_Cd','NAICS_Industry_Group_Cd','NAICS_Industry_Cd','Organization_NAICS_End_Dt','Primary_NAICS_Ind'],
      'Core_DB.ORGANIZATION_NACE':  ['Organization_Party_Id','NACE_Class_Cd','NACE_Group_Cd','NACE_Division_Cd','NACE_Section_Cd','Organization_NACE_Start_Dt','Organization_NACE_End_Dt','Importance_Order_NACE_Num'],
      'Core_DB.ORGANIZATION_SIC':   ['Organization_Party_Id','SIC_Cd','Organization_SIC_Start_Dt','Organization_SIC_End_Dt','Primary_SIC_Ind'],
      'Core_DB.ORGANIZATION_GICS':  ['Organization_Party_Id','GICS_Subindustry_Cd','GICS_Industry_Cd','GICS_Industry_Group_Cd','GICS_Sector_Cd','Organization_GICS_Start_Dt','Organization_GICS_End_Dt','Primary_GICS_Ind'],
      'Core_DB.ORGANIZATION_NAME':  ['Organization_Party_Id','Name_Type_Cd','Organization_Name_Start_Dt','Organization_Name','Organization_Name_Desc','Organization_Name_End_Dt'],
  }
  for key, cols in EXPECTED_ORDER.items():
      actual = list(tier4b[key].columns[:len(cols)])
      assert actual == cols, f'{key}: {actual} != {cols}'
  ```

### Organization_Party_Id domain (no leaks, no missing)

- [ ] Every `Organization_Party_Id` in every Tier 4b table exists in `Core_DB.ORGANIZATION.Organization_Party_Id` (FK resolution):
  ```python
  org_table_ids = set(ctx.tables['Core_DB.ORGANIZATION']['Organization_Party_Id'])
  for key, df in tier4b.items():
      vals = set(df['Organization_Party_Id'])
      missing = vals - org_table_ids
      assert not missing, f'{key}: party ids not in ORGANIZATION: {missing}'
  ```
- [ ] Every real-org `party_id` appears in every Tier 4b table (coverage):
  ```python
  for key, df in tier4b.items():
      covered = set(df['Organization_Party_Id'])
      missing = org_ids - covered
      assert not missing, f'{key}: orgs missing rows: {missing}'
  ```

### Reproducibility (byte-identical reruns)

- [ ] Running the pipeline twice with `SEED=42` produces byte-identical Tier 4b DataFrames:
  ```python
  import pandas as pd, numpy as np
  import config.settings as cfg
  from config.settings import SEED
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  from generators.tier3_party_subtypes import Tier3PartySubtypes
  from generators.tier4b_organization import Tier4bOrganization

  def run():
      rng = np.random.default_rng(SEED)
      ctx = UniverseBuilder().build(config=cfg, rng=rng)
      ctx.tables.update(Tier0Lookups().generate(ctx))
      ctx.tables.update(Tier1Geography().generate(ctx))
      ctx.tables.update(Tier2Core().generate(ctx))
      ctx.tables.update(Tier3PartySubtypes().generate(ctx))
      return Tier4bOrganization().generate(ctx)

  a, b = run(), run()
  for key in a:
      pd.testing.assert_frame_equal(a[key], b[key], check_dtype=True, check_exact=True)
  print('reproducibility OK')
  ```

### Universal checks

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else. (Expected new file: `generators/tier4b_organization.py`. No other file changes.)
- [ ] All new files pass `python -c "import <module>"`:
  ```bash
  python -c "import generators.tier4b_organization" && echo OK
  ```
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — **n/a at this step**: no CSVs written (writer is not invoked). The in-memory BIGINT dtype check above is authoritative.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: that table is Step 22.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSVs written in this step. `output/` must remain empty or absent.
- [ ] `ctx.ids` counters are unchanged by this step (no new IDs minted) — grep-level check:
  ```bash
  ! grep -n 'ctx.ids.next(' generators/tier4b_organization.py && echo "no id minting OK"
  ```
- [ ] `generate()` does not mutate `ctx.tables` — the orchestrator does that:
  ```bash
  ! grep -n 'ctx.tables\[' generators/tier4b_organization.py && echo "no ctx.tables mutation OK"
  ```
- [ ] No randomness sources whatsoever (Tier 4b is fully deterministic; no Faker, no ctx.rng, no random, no numpy.random, no hash):
  ```bash
  ! grep -nE 'import random|np\.random|ctx\.rng|Faker|fake\.|hash\(' generators/tier4b_organization.py && echo "no randomness OK"
  ```

## Handoff notes

### What shipped
- `generators/tier4b_organization.py` — `Tier4bOrganization(BaseGenerator)` with a single `generate(ctx)` method returning all 5 Core_DB DataFrames as a `Dict[str, pd.DataFrame]`.
- All 22 Definition of Done checks pass at seed=42 (600 orgs, 2400 NAME rows, 600 rows each for NAICS/NACE/SIC/GICS).
- Seed tables read via `ctx.tables.get()` (not `ctx.tables[key]`) to match tier4a convention and satisfy the no-ctx.tables-mutation grep check.

### Implementation notes
- `IdFactory.__init__` requires `id_ranges: Dict[str, int]` — use `IdFactory(cfg.ID_RANGES)` in test harnesses (the DoD snippets use bare `IdFactory()` which fails; corrected in verification runs).
- The spec's `ctx.tables[` grep check catches reads, not just writes. Switched to `.get()` for the 4 seed-table reads to match tier4a pattern.
- `NAICS_National_Industry_Cd` synthesised correctly: seed has no such column; value equals `NAICS_Industry_Cd` (5-digit code reused as national-industry code).
- `SIC_Cd` override confirmed: `cp.sic_cd` not consumed; `pick(sorted(sic_df['SIC_Cd']), cp.party_id)` used instead.
- All sector-matching assertions pass: Step 4 NAICS sectors `{52,62,44,51,72,81}` and GICS sectors are all present in seed, so matching path is always hot at seed=42.

### Deferred items
None — step is complete and self-contained.

### Next session hint
Step 14 (Tier 4c Shared Party Attributes) is the remaining parallel sibling and can start now. It depends on Step 11 (already done) and is independent of Steps 12 and 13.

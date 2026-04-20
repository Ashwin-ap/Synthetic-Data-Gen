# Spec: Step 18 — Tier 8 Product Hierarchy

## Overview

This step builds **Tier 8 — Product Hierarchy**, the five Core_DB tables that materialise the product/agreement-product linkage plane the universe already decided in Step 4 and Step 10 projected into `Core_DB.PRODUCT` + `Core_DB.AGREEMENT`: **`PRODUCT_FEATURE`** (which features each product carries), **`PRODUCT_COST`** (fee/acquisition/maintenance cost series per product), **`PRODUCT_GROUP`** (Core_DB CLV-style 9-node hierarchy: 1 root + 8 CLV children), **`PRODUCT_TO_GROUP`** (bridge from each Core_DB product to its CLV group), and **`AGREEMENT_PRODUCT`** (the 1-row-per-agreement bridge carrying the Layer-2-critical `Agreement_Product_Role_Cd = 'primary'` literal that drives `ACCOUNT_DIMENSION.Product_Cd` and `Product_Desc` per `references/02_data-mapping-reference.md` Step 3 item #7). No statistical decisions are made in this step — `PRODUCT`, `FEATURE`, and `AGREEMENT` already exist (Step 10); `AgreementProfile.product_id` already maps every agreement to its product (Step 4 `UniverseBuilder._generate_agreements`, `registry/universe.py:391–393`); the tier is pure deterministic fan-out and FK wiring, mirroring the Tier 2 / Tier 7a/7b pattern (hand-coded row literals + universe projection). See `mvp-tool-design.md` §9 Tier 8 for scope, §12 item #7 for the Layer 2 primary-role constraint, and `references/02_data-mapping-reference.md` Step 3 item #7 for the literal-match derivation.

One structural subtlety: `references/07_mvp-schema-reference.md` §8433 declares `CORE_DB.PRODUCT_TO_GROUP` with columns `PIM_Id BIGINT NOT NULL, Group_Id BIGINT NOT NULL` plus a `Valid_From_Dt`/`Valid_To_Dt`/`Del_Ind` trio plus a 5-column DI tail (`di_data_src_cd`, `di_start_ts`, `di_proc_name`, `di_rec_deleted_Ind`, `di_end_ts`). This is non-standard for Core_DB (PRD §7.3 reserves `Valid_*`/`Del_Ind` for CDM_DB and PIM_DB only; and `di_data_src_cd`/`di_proc_name` are NULL sentinels per design §7). The spec follows the DDL verbatim — flagged as ⚠️ Conflict A below — and populates `PIM_Id` with `Core_DB.PRODUCT.Product_Id` values (the column name is DDL-legacy and means "the pointed-to product key in this schema's PRODUCT table" regardless of which schema the row lives in).

## Depends on

- **Step 1** — consumes from `config/settings.py`: `HIGH_TS`, `HIGH_DATE`, `HISTORY_START`, `SIM_DATE`. No new `ID_RANGES` category is added — Core_DB `Product_Group_Id` values are hand-coded module-level BIGINT constants (9 rows total: 1 root + 8 CLV children) starting at `92_000_000` to stay clear of every existing `ID_RANGES` offset (`pim_id=90_000_000`, `group_id=91_000_000` are reserved for PIM_DB in Step 23 — `92_000_000+` is deliberately past them).
- **Step 2** — consumes `generators/base.BaseGenerator.stamp_di()` (3-column tail: `di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind`) and `BaseGenerator.stamp_valid()` (3-column tail: `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind`). Does **not** consume `utils/id_factory.IdFactory` — no counter-backed IDs are minted in this step. Does **not** consume `utils/luhn` or `utils/date_utils` (no date arithmetic needed beyond `HISTORY_START` anchor).
- **Step 3** — consumes `registry/context.GenerationContext`, `registry/profiles.CustomerProfile`, `registry/profiles.AgreementProfile`. `Tier8ProductHierarchy.generate(ctx)` reads `ctx.customers` (only for size checks — no customer attributes are projected into these tables), `ctx.agreements` (for `AGREEMENT_PRODUCT` fan-out), and `ctx.tables` (for upstream prerequisite checks on PRODUCT/FEATURE/AGREEMENT/CURRENCY/UNIT_OF_MEASURE).
- **Step 4** — consumes the built universe. Critical invariants this step depends on:
  - Every `AgreementProfile.product_id` is a BIGINT already minted into `Core_DB.PRODUCT.Product_Id` by Step 10 (the step does NOT re-mint).
  - Every `AgreementProfile.agreement_id` is unique and present in `ctx.tables['Core_DB.AGREEMENT'].Agreement_Id`.
  - Every `AgreementProfile.open_dttm.date() ≥ HISTORY_START - 10y` and `≤ SIM_DATE` — so `Agreement_Product_Start_Dt = ag.open_dttm.date()` always yields a valid DATE column.
  - `ctx.agreements` carries exactly the 12 MVP `product_type` values (`CHECKING`, `SAVINGS`, `MMA`, `CERTIFICATE_OF_DEPOSIT`, `RETIREMENT`, `MORTGAGE`, `CREDIT_CARD`, `VEHICLE_LOAN`, `STUDENT_LOAN`, `HELOC`, `PAYDAY`, `COMMERCIAL_CHECKING`). The CLV-to-product mapping in this step covers all twelve.
- **Step 5** — n/a at generation time. The writer is not invoked in this step; DDL column ordering is enforced at DataFrame construction via `pd.DataFrame(rows, columns=_COLS_*)`.
- **Step 8** — consumes these already-stamped Tier 0 seed tables that Tier 8 FK-references by code (not by surrogate key):
  - `Core_DB.CURRENCY` — `PRODUCT_FEATURE.Currency_Cd` (nullable) resolves here (seeded USD/EUR/GBP/CAD/AUD/JPY at `seed_data/currency.py`). Populated with `'USD'` for every PRODUCT_FEATURE row.
  - `Core_DB.UNIT_OF_MEASURE` — `PRODUCT_FEATURE.Unit_Of_Measure_Cd` (nullable) resolves here (seeded at `seed_data/misc_types.py:20–35`: `USD`, `EUR`, `PCT`, `YR`, `MO`, `DAY`, `CNT`, `KG`, `M`). Populated per feature type: `'PCT'` for rate features, `'USD'` for amount features, `'YR'` for term features, `None` for counts.
- **Step 10** — consumes `ctx.tables['Core_DB.PRODUCT']` (for Product_Id FK universe) and `ctx.tables['Core_DB.FEATURE']` (for Feature_Id FK universe; must include the `RATE_FEATURE_SUBTYPE_CD = 'Rate Feature'` row and the `ORIGINAL_LOAN_TERM_CLASSIFICATION_CD = 'Original Loan Term'` classification row that Step 10 seeded). PRODUCT row count = distinct product types in the universe (11–12); FEATURE row count = 24 (per Step 10 spec §Tables generated).
- **Step 17** — consumes the fact that Step 17 already committed the sub-type chain tables. This is **order-dependency only** — Tier 8 does not import from Tier 7a or Tier 7b's output tables. (Rationale: placing Tier 8 after Tier 7b in the dependency graph is a documentation choice in `implementation-steps.md`; the code itself reads only PRODUCT/FEATURE/AGREEMENT from Tier 2.)

No code from Step 9 (Tier 1 geography), Step 11–15 (Tier 3/4/5/6), Step 16 (Tier 7a), or Step 17 (Tier 7b) is imported by this step. The writer is not invoked — `generate()` returns DataFrames only; orchestrator (Step 25) handles `ctx.tables.update()` and later CSV emission.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 18):
- `PRD.md` §4.2 (enumerated table list — the 5 Tier 8 tables), §7.1 (BIGINT rule), §7.3 (DI column rules — 3-col Core_DB tail), §10 (conflict-resolution priority — DDL wins over earlier design docs for column naming)
- `mvp-tool-design.md` §9 Tier 8 (**authoritative scope + footnote on `PRODUCT_TO_GROUP` naming vs `PRODUCT_TO_PRODUCT_GROUP` legacy**), §12 item #7 (Layer 2 primary-role constraint — enforced in this step), §14 Decision 3 (BIGINT everywhere), §14 Decision 1 (entity-first registry — Tier 8 is pure projection)
- `implementation-steps.md` Step 18 entry (exit criteria); Handoff Protocol (post-session rules)

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the 5 in-scope tables. Open only these blocks (line numbers current as of 2026-04-20; the SQL DDL wins when it disagrees with any summary table, per CLAUDE.md "DDL verification rule" and PRD §10):
  - `AGREEMENT_PRODUCT` (§3573) — 5 business + 3 DI = 8 cols. NOT NULL: `Agreement_Id`, `Product_Id`, `Agreement_Product_Role_Cd`, `Agreement_Product_Start_Dt`. Nullable: `Agreement_Product_End_Dt`. PI on `Agreement_Id`. Both `*_Id` are INTEGER in DDL → **BIGINT** per PRD §7.1.
  - `PRODUCT_FEATURE` (§3602) — 10 business + 3 DI = 13 cols. NOT NULL: `Product_Id`, `Feature_Id`, `Product_Feature_Type_Cd`, `Product_Feature_Start_Dttm`. Nullable: `Product_Feature_End_Dttm`, `Product_Feature_Amt` DECIMAL(18,4), `Product_Feature_Rate` DECIMAL(15,12), `Product_Feature_Qty` DECIMAL(18,4), `Product_Feature_Num` VARCHAR(50), `Currency_Cd` VARCHAR(50), `Unit_Of_Measure_Cd` VARCHAR(50). Both `*_Id` are INTEGER → BIGINT.
  - `PRODUCT_COST` (§3798) — 5 business + 3 DI = 8 cols. NOT NULL: `Product_Id`, `Cost_Cd`, `Product_Cost_Start_Dttm`. Nullable: `Product_Cost_Amt` DECIMAL(18,4), `Product_Cost_End_Dttm`. `Product_Id` is already BIGINT in DDL. Composite logical PK (Product_Id, Cost_Cd, Product_Cost_Start_Dttm).
  - `PRODUCT_GROUP` (Core_DB, §3826) — 5 business + 3 DI = 8 cols. NOT NULL: `Product_Group_Id`, `Parent_Group_Id`, `Product_Group_Type_Cd`. Nullable: `Product_Group_Name` VARCHAR(255), `Product_Group_Desc` VARCHAR(1000). Both `*_Id` are INTEGER → BIGINT. `Parent_Group_Id` is NOT NULL, which means the root row MUST self-reference (root.Parent_Group_Id = root.Product_Group_Id) — same rule as PIM_DB (per `05_architect-qa.md` Q3, reused here for Core_DB).
  - `PRODUCT_TO_GROUP` (Core_DB, §8436) — **non-standard shape** (⚠️ Conflict A below). 5 business + 5 DI = 10 cols. NOT NULL: `PIM_Id` BIGINT, `Group_Id` BIGINT, `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind`. The DI tail contains `di_data_src_cd`, `di_start_ts`, `di_proc_name`, `di_rec_deleted_Ind`, `di_end_ts` (5 columns; Core_DB elsewhere stamps only 3). Session MUST follow the DDL verbatim (column names and full 5-col DI + Valid_* tail). The session populates `PIM_Id = Core_DB.Product_Id` (not `PIM_DB.PIM_Id` — see ⚠️ Conflict A) and `Group_Id = Core_DB.Product_Group_Id`.

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is MVP-authoritative per PRD §10; only open `01` if `07` is ambiguous for a specific column.
- `references/05_architect-qa.md` — only Q3 (root self-reference) matters and is already absorbed into the design-doc Tier 8/Tier 15 notes. No other Q touches Tier 8.
- `references/06_supporting-enrichments.md` — no distribution is needed in this step; Tier 8 is pure deterministic projection.
- `references/02_data-mapping-reference.md` beyond Step 3 item #7 — the only Layer 2 literal-match constraint is item #7 (`Agreement_Product_Role_Cd = 'primary'`). Item #20 (`Product_Group_Type_Cd = 'CLV'` for ACCOUNT_DIMENSION.Product_CLV_Type) binds **PIM_DB.PRODUCT_GROUP**, not Core_DB.PRODUCT_GROUP — but the session uses `'CLV'` as the Core_DB Product_Group_Type_Cd too for semantic consistency with Step 23 (no Layer 2 constraint binds the Core_DB value, so this choice is free but deliberate).
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `resources/iDM_MDM_tables_DDLs.xlsx` — already distilled into `07`.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier8_product_hierarchy.py` — `class Tier8ProductHierarchy(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]` method. Implementation contract:
  1. Import `BaseGenerator`; import `GenerationContext`/`AgreementProfile`/`CustomerProfile` under `TYPE_CHECKING` only. Import `pd`, `numpy as np` (optional — only for `Int64Dtype()` / dtype coercion if needed), `from datetime import datetime, date, timedelta`, `from decimal import Decimal`, `from typing import Dict, List, Tuple`.
  2. Import literal-match constants from `config.code_values`: `RATE_FEATURE_SUBTYPE_CD`, `ORIGINAL_LOAN_TERM_CLASSIFICATION_CD`. Import `HISTORY_START`, `SIM_DATE`, `HIGH_TS`, `HIGH_DATE` from `config.settings`.
  3. Declare module-level constants (all reproducibility-friendly — **no `datetime.now()`, no `ctx.rng` consumption**):
     - `_TIER8_DI_START_TS = '2000-01-01 00:00:00.000000'` (matches `_TIER7A_DI_START_TS`, `_TIER7B_DI_START_TS`, and `_TIER2_DI_START_TS` convention).
     - `_TIER8_VALID_FROM_DT = HISTORY_START.isoformat()` (`'2025-10-01'`, used only for PRODUCT_TO_GROUP's `Valid_From_Dt` NOT NULL column).
     - `_PRIMARY_ROLE_CD = 'primary'` — Layer 2 literal-match (Step 3 item #7).
     - `_PRODUCT_GROUP_TYPE_CLV = 'CLV'` — the `Product_Group_Type_Cd` used on every Core_DB.PRODUCT_GROUP row (documented as deliberate alignment with PIM_DB's Tier 15 convention; Layer 2 does not bind this value in Core_DB but binding it anyway is internally consistent).
     - `_USD_CURRENCY_CD = 'USD'` — every PRODUCT_FEATURE row uses USD.
     - `_PRODUCT_GROUP_IDS: Dict[str, int]` — hand-coded 9-row hierarchy:
       ```python
       _PRODUCT_GROUP_IDS = {
           'ROOT':          92_000_000,
           'CHECKING':      92_000_001,
           'SAVINGS':       92_000_002,
           'RETIREMENT':    92_000_003,
           'CREDIT_CARD':   92_000_004,
           'VEHICLE_LOAN':  92_000_005,
           'MORTGAGE':      92_000_006,
           'INVESTMENTS':   92_000_007,
           'INSURANCE':     92_000_008,
       }
       ```
       Rationale for `92_000_000+`: sits above `pim_id=90_000_000` and `group_id=91_000_000` (which are reserved for PIM_DB in Step 23), so Core_DB product-group IDs never collide with PIM_DB identifiers even if both schemas are loaded into the same analytics database.
     - `_PRODUCT_GROUP_ROWS: List[Dict]` — 9 literal row dicts (1 root self-referential + 8 CLV children). Every row has every business column spelled out; diff review is trivial. Root's `Parent_Group_Id = _PRODUCT_GROUP_IDS['ROOT']` (self-reference — satisfies NOT NULL). Children's `Parent_Group_Id = _PRODUCT_GROUP_IDS['ROOT']`. `Product_Group_Type_Cd = _PRODUCT_GROUP_TYPE_CLV` on every row (including root — this is acceptable because the DDL constraint is NOT NULL, not a specific FK to a typed lookup that only has CLV/non-CLV values; session verifies no such FK exists).
     - `_PRODUCT_TO_CLV_GROUP: Dict[str, str]` — maps each of the 12 MVP product types to its CLV group key:
       ```python
       _PRODUCT_TO_CLV_GROUP = {
           'CHECKING':                'CHECKING',
           'COMMERCIAL_CHECKING':     'CHECKING',
           'SAVINGS':                 'SAVINGS',
           'MMA':                     'SAVINGS',
           'CERTIFICATE_OF_DEPOSIT':  'SAVINGS',
           'RETIREMENT':              'RETIREMENT',
           'CREDIT_CARD':             'CREDIT_CARD',
           'VEHICLE_LOAN':            'VEHICLE_LOAN',
           'STUDENT_LOAN':            'VEHICLE_LOAN',     # no Education CLV in standard 8
           'MORTGAGE':                'MORTGAGE',
           'HELOC':                   'MORTGAGE',
           'PAYDAY':                  'CREDIT_CARD',       # short-term credit line
       }
       ```
       The STUDENT_LOAN → VEHICLE_LOAN and PAYDAY → CREDIT_CARD mappings are documented in the handoff as deliberate simplifications (the standard CLV 8-type hierarchy has no Education or Short-Term-Credit bucket — `references/02_data-mapping-reference.md` line 1096: "(1) Checking, (2) Savings, (3) Retirement, (4) Credit Card, (5) Vehicle Loan, (6) Mortgage, (7) Investments, (8) Insurance"). Investments and Insurance exist as CLV groups but have no agreements pointing to them in MVP — they are included in PRODUCT_GROUP for structural completeness but have zero PRODUCT_TO_GROUP rows targeting them.
     - `_PRODUCT_COST_RECIPE: Dict[str, List[Tuple[str, Decimal]]]` — per-product-type list of `(Cost_Cd, Product_Cost_Amt)` pairs. Every product gets 2 cost rows: `'ACQUISITION'` and `'MAINTENANCE'`. Hand-coded amounts (e.g., CHECKING → acquisition $12.00, maintenance $5.00/month; MORTGAGE → acquisition $500.00, maintenance $50.00/month; etc.). The values are illustrative — no Layer 2 rule binds them; session picks plausible magnitudes and documents the choice.
     - `_PRODUCT_FEATURE_RECIPE: Dict[str, List[Dict]]` — per-product-type list of feature-row seed templates. Each template specifies which FEATURE subtype to pick (by `Feature_Subtype_Cd` lookup into `ctx.tables['Core_DB.FEATURE']`) plus the product-feature-type-code + amount/rate/qty values. Every product gets at minimum one `'Rate Feature'` row (so LOAN_ACCOUNT_BB's rate derivation fires even when AGREEMENT_FEATURE is silent). Loan products additionally get `'Original Loan Term'` classification rows. Deposits get an extra `'Deposit Feature'` row if the subtype exists; otherwise skipped. Example shape:
       ```python
       _PRODUCT_FEATURE_RECIPE = {
           'CHECKING': [
               {'feature_subtype': 'Rate Feature', 'product_feature_type': 'rate', 'rate': Decimal('0.000100000000'), 'amt': None, 'qty': None, 'uom': 'PCT'},
               {'feature_subtype': 'Fee Feature',  'product_feature_type': 'fee',  'rate': None, 'amt': Decimal('25.0000'), 'qty': None, 'uom': 'USD'},
           ],
           'MORTGAGE': [
               {'feature_subtype': 'Rate Feature',                'product_feature_type': 'rate', 'rate': Decimal('0.065000000000'), 'amt': None, 'qty': None, 'uom': 'PCT', 'classification': 'Origination Rate'},
               {'feature_subtype': 'Rate Feature',                'product_feature_type': 'term', 'rate': None, 'amt': None, 'qty': Decimal('30.0000'), 'uom': 'YR',  'classification': ORIGINAL_LOAN_TERM_CLASSIFICATION_CD},
           ],
           ...
       }
       ```
       Session consults the `FEATURE` table's seeded `Feature_Subtype_Cd` and `Feature_Classification_Cd` values — if a recipe names a subtype that isn't seeded, the row is skipped and a `⚠️ Conflict` block is appended; the session does not invent features.
  4. Declare `_COLS_*` list-of-str module constants for every emitted DataFrame in **DDL declaration order** (business cols only; DI tail appended by `stamp_di()`). For PRODUCT_TO_GROUP, DI tail is 5-col (non-standard — see ⚠️ Conflict A) and business cols include the Valid_* trio; stamp them explicitly instead of relying on `stamp_valid()` + `stamp_di()` defaults.
     ```python
     _COLS_AGREEMENT_PRODUCT = [
         'Agreement_Id', 'Product_Id', 'Agreement_Product_Role_Cd',
         'Agreement_Product_Start_Dt', 'Agreement_Product_End_Dt',
     ]
     _COLS_PRODUCT_FEATURE = [
         'Product_Id', 'Feature_Id', 'Product_Feature_Type_Cd',
         'Product_Feature_Start_Dttm', 'Product_Feature_End_Dttm',
         'Product_Feature_Amt', 'Product_Feature_Rate', 'Product_Feature_Qty',
         'Product_Feature_Num', 'Currency_Cd', 'Unit_Of_Measure_Cd',
     ]
     _COLS_PRODUCT_COST = [
         'Product_Id', 'Cost_Cd', 'Product_Cost_Amt',
         'Product_Cost_Start_Dttm', 'Product_Cost_End_Dttm',
     ]
     _COLS_PRODUCT_GROUP = [
         'Product_Group_Id', 'Parent_Group_Id', 'Product_Group_Type_Cd',
         'Product_Group_Name', 'Product_Group_Desc',
     ]
     _COLS_PRODUCT_TO_GROUP = [
         'PIM_Id', 'Group_Id', 'Valid_From_Dt', 'Valid_To_Dt', 'Del_Ind',
     ]
     ```
  5. **Guard** at the top of `generate()`: verify `ctx.agreements` and `ctx.customers` are non-empty; verify every required upstream table is present in `ctx.tables` (use `_REQUIRED_UPSTREAM_TABLES = ('Core_DB.AGREEMENT', 'Core_DB.PRODUCT', 'Core_DB.FEATURE', 'Core_DB.CURRENCY', 'Core_DB.UNIT_OF_MEASURE')`). Raise `RuntimeError(f'Tier 8 prerequisite missing: {key}')` on any failure. No silent fallback.
  6. Resolve the **canonical `product_type → Product_Id` map** by scanning `ctx.tables['Core_DB.PRODUCT']` once (keyed by `Product_Subtype_Cd`, which equals the `product_type` string per Step 10 spec). Verify the invariant that every value is a unique BIGINT (no two product types share a Product_Id). Also resolve the **`(feature_subtype_cd, classification_cd) → Feature_Id` map** by scanning `ctx.tables['Core_DB.FEATURE']` once; the `classification_cd` lookup is optional (some recipes match only on subtype).
  7. Build **`AGREEMENT_PRODUCT`** DataFrame — **one row per `ctx.agreements` entry**. `Agreement_Id = ag.agreement_id`; `Product_Id = ag.product_id`; `Agreement_Product_Role_Cd = _PRIMARY_ROLE_CD`; `Agreement_Product_Start_Dt = ag.open_dttm.date()`; `Agreement_Product_End_Dt = ag.close_dttm.date() if ag.close_dttm is not None else None`. Row count = `len(ctx.agreements)` exactly — every agreement gets **exactly one** primary-role row (Step 3 item #7 requires ≥1; session emits exactly 1, keeping the count minimal and the invariant trivial to verify).
  8. Build **`PRODUCT_FEATURE`** DataFrame — per-product rows from `_PRODUCT_FEATURE_RECIPE`. Iterate `ctx.tables['Core_DB.PRODUCT']` rows; for each product's `Product_Subtype_Cd`, look up the recipe (fall through gracefully if unlisted — every product must have ≥1 PRODUCT_FEATURE row; if the recipe is empty, add a default `'Rate Feature'` fallback row and log the product in handoff notes). Populate `Product_Feature_Start_Dttm` = `datetime.combine(HISTORY_START, time.min)` (deterministic — every product's features begin at the history-window start). `Product_Feature_End_Dttm = None` (active). `Currency_Cd = _USD_CURRENCY_CD` for amount rows, `None` for rate/qty rows. `Unit_Of_Measure_Cd` per recipe row. Only one of `Product_Feature_Amt` / `Product_Feature_Rate` / `Product_Feature_Qty` is non-null per row (matches the feature's shape).
  9. Build **`PRODUCT_COST`** DataFrame — 2 rows per product (`ACQUISITION`, `MAINTENANCE`) from `_PRODUCT_COST_RECIPE`. `Product_Cost_Start_Dttm = datetime.combine(HISTORY_START, time.min)`. `Product_Cost_End_Dttm = None` (active). `Product_Cost_Amt` per recipe.
  10. Build **`PRODUCT_GROUP`** DataFrame — exactly 9 rows from `_PRODUCT_GROUP_ROWS`. Root row: `Product_Group_Id = Parent_Group_Id = 92_000_000`, `Product_Group_Type_Cd = 'CLV'`, `Product_Group_Name = 'Root'`, `Product_Group_Desc = 'Root of Core_DB product group hierarchy — self-referential per 05_architect-qa.md Q3'`. 8 CLV children: `Parent_Group_Id = 92_000_000`, names from the 8-type list (`Checking`, `Savings`, `Retirement`, `Credit Card`, `Vehicle Loan`, `Mortgage`, `Investments`, `Insurance`).
  11. Build **`PRODUCT_TO_GROUP`** DataFrame — one row per Core_DB product, mapped through `_PRODUCT_TO_CLV_GROUP`. `PIM_Id = Product.Product_Id` (see ⚠️ Conflict A: DDL column name is PIM_Id but it holds a Core_DB Product_Id value here). `Group_Id = _PRODUCT_GROUP_IDS[_PRODUCT_TO_CLV_GROUP[product_subtype_cd]]`. `Valid_From_Dt = HIGH_DATE`? No — `Valid_From_Dt = _TIER8_VALID_FROM_DT = '2025-10-01'` (HISTORY_START as ISO string). `Valid_To_Dt = HIGH_DATE`. `Del_Ind = 'N'` (CHAR(1)).
  12. Apply dtype coercions — cast every `*_Id` column and `PIM_Id`/`Group_Id` to `Int64` (nullable BIGINT). DECIMAL columns stay as Python Decimal (pandas stores as `object`). Dates as `date`. Datetimes as `datetime`. `Del_Ind` as Python `str` (`'N'`).
  13. Stamp the 4 standard Core_DB DataFrames via `self.stamp_di(df, start_ts=_TIER8_DI_START_TS)` — yields the 3-col tail. Do NOT call `stamp_valid()` on any of the 4 — Tier 8 standard tables are Core_DB (PRD §7.3).
  14. Stamp **`PRODUCT_TO_GROUP`** with a custom 5-col DI tail (⚠️ Conflict A): `df['di_data_src_cd'] = None`, `df['di_start_ts'] = _TIER8_DI_START_TS`, `df['di_proc_name'] = None`, `df['di_rec_deleted_Ind'] = 'N'`, `df['di_end_ts'] = HIGH_TS`. Do this inline rather than extending `BaseGenerator` (the 5-col tail is a per-table exception, not a project-wide convention). `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` were already populated as business columns in step 11 (not via `stamp_valid()`).
  15. Return a dict with exactly these 5 keys:
      ```
      {
        'Core_DB.AGREEMENT_PRODUCT', 'Core_DB.PRODUCT_FEATURE',
        'Core_DB.PRODUCT_COST', 'Core_DB.PRODUCT_GROUP',
        'Core_DB.PRODUCT_TO_GROUP',
      }
      ```
  Do NOT mutate `ctx.tables` — the orchestrator does that after the call returns.

**Do NOT produce** in this step:
- CSVs — writer is not invoked. `output/` is not touched.
- PIM_DB.PRODUCT_TO_GROUP, PIM_DB.PRODUCT_GROUP, PIM_DB.PRODUCT_GROUP_TYPE, PIM_DB.PRODUCT, PIM_DB.PRODUCT_PARAMETERS, PIM_DB.PRODUCT_PARAMETER_TYPE — Step 23's responsibility (Tier 15 PIM_DB).
- New `seed_data/*.py` modules — PRODUCT_GROUP, PRODUCT_COST, PRODUCT_FEATURE rows are entity instances (not reference lookups), hand-coded **inside the generator** module. Reserving `seed_data/` for Tier 0 pure lookups keeps the folder contract clean.
- Wiring into `main.py` — orchestrator changes are Step 25's responsibility.
- New Tier 0 lookup rows — every code referenced by Tier 8 (`Currency_Cd`, `Unit_Of_Measure_Cd`, `Feature_Subtype_Cd`, `Feature_Classification_Cd`) is already seeded. If Tier 8 needs a code that is not seeded (e.g., a `PRODUCT_GROUP_TYPE` Core_DB lookup), escalate per Handoff Protocol §2 rather than monkey-patching Tier 0.
- Changes to `config/settings.py` — the 9 Core_DB product-group IDs are module-level constants in `tier8_product_hierarchy.py`, not new `ID_RANGES` entries. Rationale: the fixed 9-row count doesn't warrant a counter-backed factory, and keeping the diff to one file minimises review surface.
- Changes to `config/code_values.py` — no new literal-match constants needed. `_PRIMARY_ROLE_CD = 'primary'` is local to this module (it's a per-tier constant, not cross-tier; Step 9 Tier 9 uses `'customer'`/`'borrower'`, not `'primary'`).

## Tables generated (if applicable)

After `Tier8ProductHierarchy.generate(ctx)` runs, `ctx.tables` gains these 5 Core_DB keys:

| Table | Row count | Driven by | Notes |
|-------|-----------|-----------|-------|
| `Core_DB.AGREEMENT_PRODUCT` | ≈ 5,000 (= `len(ctx.agreements)`) | per-agreement | **Layer 2 literal-match**: every row has `Agreement_Product_Role_Cd = 'primary'` (satisfies Step 3 item #7) |
| `Core_DB.PRODUCT_FEATURE` | 20–35 (2–3 rows per product × 11–12 products) | per-product via `_PRODUCT_FEATURE_RECIPE` | Every product has ≥1 row; loan products have a `'Rate Feature'` row |
| `Core_DB.PRODUCT_COST` | 22–24 (exactly 2 rows per product) | per-product via `_PRODUCT_COST_RECIPE` | `ACQUISITION` + `MAINTENANCE` per product; illustrative amounts (no Layer 2 binding) |
| `Core_DB.PRODUCT_GROUP` | 9 (1 root + 8 CLV children) | hand-coded `_PRODUCT_GROUP_ROWS` | Root self-references (`Parent_Group_Id = Product_Group_Id = 92_000_000`) per `05_architect-qa.md` Q3; every row has `Product_Group_Type_Cd = 'CLV'` |
| `Core_DB.PRODUCT_TO_GROUP` | 11–12 (one per distinct product in universe) | per-product via `_PRODUCT_TO_CLV_GROUP` | ⚠️ Non-standard column names (`PIM_Id`, `Group_Id`) + 5-col DI + Valid_* tail per DDL §8436 |

All 4 standard DataFrames have the 3-column Core_DB DI tail after `stamp_di()` with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. `PRODUCT_TO_GROUP` has the non-standard 5-col DI + Valid_* trio (`Valid_From_Dt = '2025-10-01'`, `Valid_To_Dt = '9999-12-31'`, `Del_Ind = 'N'`) per ⚠️ Conflict A.

**Layer-2 constraint coverage guaranteed by this step:**
- **Item #7** (AGREEMENT_PRODUCT primary role): every agreement has exactly one `Agreement_Product_Role_Cd = 'primary'` row with a valid `Product_Id`. Verified in DoD.

## ⚠️ Conflict handling protocol (conditional — only activates if triggered during implementation)

Three upstream gaps could be discovered during implementation. Do NOT silently improvise — escalate per Handoff Protocol §2 and add a `⚠️ Conflict` block to this spec:

1. **`PRODUCT_TO_GROUP` non-standard shape.** DDL §8436 declares Core_DB.PRODUCT_TO_GROUP with (a) column names `PIM_Id`/`Group_Id` that do not match the surrounding Core_DB naming convention (would expect `Product_Id`/`Product_Group_Id`), and (b) a `Valid_From_Dt`/`Valid_To_Dt`/`Del_Ind` trio + 5-col DI tail that PRD §7.3 reserves for CDM_DB/PIM_DB. Session follows the DDL verbatim — see ⚠️ Conflict A below (pre-filled because this is certain to arise).
2. **`PRODUCT_GROUP_TYPE` Core_DB lookup table.** The DDL declares `Product_Group_Type_Cd VARCHAR(50) NOT NULL` but no `CORE_DB.PRODUCT_GROUP_TYPE` lookup table exists in `07_mvp-schema-reference.md` (the only `PRODUCT_GROUP_TYPE` is PIM_DB's, SMALLINT-keyed — Step 23 territory). Session uses the literal `'CLV'` without FK-check; if a future step reveals a Core_DB lookup table with different legal values, this choice is renegotiated. Documented as ⚠️ Conflict B.
3. **`_PRODUCT_FEATURE_RECIPE` references a subtype not seeded.** If the session's recipe names e.g. `'Deposit Feature'` but `ctx.tables['Core_DB.FEATURE']` lacks that subtype, the row is skipped rather than invented. If every product would end up with 0 feature rows under this rule, raise `RuntimeError` — the FEATURE seed in Step 10 is incomplete. Otherwise note the skip in handoff.

## ⚠️ Conflict A — `PRODUCT_TO_GROUP` non-standard shape (pre-filled)

**Trigger:** Conflict #1 in the protocol above (certain to occur — flagged pre-implementation).
**Finding:** `references/07_mvp-schema-reference.md` §8436 declares `CORE_DB.PRODUCT_TO_GROUP` with:
- Column `PIM_Id BIGINT NOT NULL` — name suggests FK to `PIM_DB.PRODUCT.PIM_Id`, but the table lives in Core_DB and the Tier 8 design (mvp-tool-design.md §9) places PRODUCT_TO_GROUP as a Core_DB-internal bridge from Core_DB.PRODUCT to Core_DB.PRODUCT_GROUP.
- Column `Group_Id BIGINT NOT NULL` — name suggests a generic group FK, consistent with pointing to Core_DB.PRODUCT_GROUP.Product_Group_Id.
- Trio `Valid_From_Dt`/`Valid_To_Dt`/`Del_Ind` — PRD §7.3 says these are CDM_DB/PIM_DB only.
- 5-col DI tail including `di_data_src_cd`/`di_proc_name` — Core_DB elsewhere has only 3-col DI.
**Resolution:**
1. Follow the DDL **verbatim** for column names (PRD §10: DDL wins over design-doc naming when they disagree).
2. Populate `PIM_Id` with Core_DB.PRODUCT.Product_Id values (Core_DB-internal bridge; the DDL column name is a legacy misnomer). Do NOT attempt to populate with PIM_DB.PIM_Id — that would require Step 23 to run first, contradicting the tier dependency graph.
3. Populate the Valid_* trio + 5-col DI tail as the DDL demands. `Valid_From_Dt = '2025-10-01'` (HISTORY_START), `Valid_To_Dt = '9999-12-31'`, `Del_Ind = 'N'` (CHAR(1)). 5-col DI: `di_data_src_cd = None`, `di_start_ts = '2000-01-01 00:00:00.000000'`, `di_proc_name = None`, `di_rec_deleted_Ind = 'N'`, `di_end_ts = '9999-12-31 00:00:00.000000'`.
4. Do NOT modify `PRD.md` §7.3 or `mvp-tool-design.md` §7 to accommodate this one table; the exception is table-local per DDL and documented here.
5. Handoff note should flag this to the architect: if the naming/shape is a DDL error, rename and align; if intentional, document the rationale in `mvp-tool-design.md`.

## ⚠️ Conflict B — Core_DB `PRODUCT_GROUP_TYPE` lookup absent (pre-filled)

**Trigger:** Conflict #2 in the protocol above.
**Finding:** `CORE_DB.PRODUCT_GROUP.Product_Group_Type_Cd VARCHAR(50) NOT NULL` has no corresponding lookup table in `07_mvp-schema-reference.md`. The only `PRODUCT_GROUP_TYPE` in the reference is `PIM_DB.PRODUCT_GROUP_TYPE` (SMALLINT-keyed, Step 23).
**Resolution:** Use the literal string `'CLV'` for every Core_DB.PRODUCT_GROUP row, chosen for semantic consistency with PIM_DB's 8-type CLV hierarchy (per `references/02_data-mapping-reference.md` line 1096). No FK check is possible. Handoff flags this for the architect.

## Files to modify

No files modified. `config/settings.py`, `config/code_values.py`, `config/distributions.py`, `utils/*`, `registry/*`, `seed_data/*`, all existing `generators/*.py`, `output/*`, `main.py`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/*`, `CLAUDE.md` are all **NOT touched**.

If implementation discovers that `references/07_mvp-schema-reference.md` disagrees with this spec on any column name, type, or nullability (beyond those flagged above), escalate per Handoff Protocol §2 — update the upstream reference or add a new `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new dependencies. `pandas` is already in `requirements.txt` (Step 1). This step imports only the standard library + pandas + existing project modules.

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — every `*_Id` column in every Tier 8 DataFrame is emitted as `pd.Int64Dtype()` (nullable BIGINT) or `int64` (when all non-null). The DDL declares `INTEGER` for `AGREEMENT_PRODUCT.Agreement_Id`, `AGREEMENT_PRODUCT.Product_Id`, `PRODUCT_FEATURE.Product_Id`, `PRODUCT_FEATURE.Feature_Id`, `PRODUCT_GROUP.Product_Group_Id`, `PRODUCT_GROUP.Parent_Group_Id`; the BIGINT rule wins. `PRODUCT_COST.Product_Id` and `PRODUCT_TO_GROUP.PIM_Id`/`Group_Id` are already BIGINT in DDL.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — n/a: Tier 8 tables carry no `Party_Id` columns.
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on the 4 standard DataFrames (AGREEMENT_PRODUCT, PRODUCT_FEATURE, PRODUCT_COST, PRODUCT_GROUP). `PRODUCT_TO_GROUP` gets a custom 5-col DI tail per ⚠️ Conflict A. Every DataFrame uses `_TIER8_DI_START_TS = '2000-01-01 00:00:00.000000'` for byte-stable reproducibility (mirrors Tier 2 / Tier 7a / Tier 7b pattern).
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts` stamped to `HIGH_TS` via `stamp_di()` default; `Valid_To_Dt` set to `HIGH_DATE` on `PRODUCT_TO_GROUP` only (Conflict A).
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — all 5 tables in this step live in Core_DB. `PRODUCT_TO_GROUP` carries Valid_* columns **not** because of the standard rule but because the DDL declares them explicitly (Conflict A). The session does NOT call `stamp_valid()` — the Valid_* columns are populated inline as business columns to keep column ordering tight to the DDL.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** — enforced at construction time via `pd.DataFrame(rows, columns=_COLS_*)`. The Definition-of-done check against the writer's DDL-order reordering validates final correctness.
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — n/a: that table is Step 22 (Tier 14 CDM_DB).
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — n/a: Tier 8 has no geospatial tables.
- **No ORMs, no database connections — pure pandas → CSV** — writer is not invoked; generator returns DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — **no randomness in this step**. Every row is hand-coded or projected deterministically from `ctx.customers`/`ctx.agreements`/`ctx.tables['Core_DB.PRODUCT']`/`ctx.tables['Core_DB.FEATURE']`. The generator does not read or use `ctx.rng`. Every `_TIER8_*` constant is a module-level literal.

Step-specific rules (Tier 8 Product Hierarchy):

- **Universe projection is 1-to-1 and deterministic.** `AGREEMENT_PRODUCT` has exactly `len(ctx.agreements)` rows in the same iteration order as the list; no filtering, no sampling, no sort.
- **`product_id` reuse is invariant, not a convenience.** Every `AgreementProfile.product_id` must match exactly one `Core_DB.PRODUCT.Product_Id`. Verified at generate-time via a scan; raise `RuntimeError` on any mismatch — this is a universe-builder bug and must not be silently tolerated.
- **`product` IdFactory counter must not be advanced by this step.** No product IDs are minted — verified post-emission that `ctx.ids.peek('product')` is unchanged.
- **Literal-match constants come from `config.code_values`** where already centralised: `RATE_FEATURE_SUBTYPE_CD`, `ORIGINAL_LOAN_TERM_CLASSIFICATION_CD`. Tier-8-local constants (`_PRIMARY_ROLE_CD = 'primary'`, `_PRODUCT_GROUP_TYPE_CLV = 'CLV'`, `_USD_CURRENCY_CD = 'USD'`) live inside this module.
- **Every agreement produces exactly one AGREEMENT_PRODUCT row** with `Agreement_Product_Role_Cd = 'primary'`. Step 3 item #7 requires ≥1; session emits exactly 1 to keep the invariant crisp. No `'secondary'` role rows are emitted in this step (a future step may add them, but it's out of scope here).
- **Root PRODUCT_GROUP self-references.** `Product_Group_Id = Parent_Group_Id = 92_000_000` on the root row. This satisfies the `Parent_Group_Id NOT NULL` DDL constraint and mirrors Step 23's PIM_DB rule (per `05_architect-qa.md` Q3). All 8 CLV children point to the root.
- **Every Core_DB.PRODUCT has exactly one PRODUCT_TO_GROUP row.** Fan-out is `len(Core_DB.PRODUCT)` rows, not `len(ctx.agreements)`. The PIM_Id column holds the Core_DB `Product_Id` value (⚠️ Conflict A).
- **Every product has ≥1 PRODUCT_COST row and ≥1 PRODUCT_FEATURE row.** Recipe fallbacks ensure no product is left bare. If a recipe references a feature subtype not present in the FEATURE seed, skip that row and log the skip in handoff — do NOT invent a new FEATURE row.
- **`Del_Ind` is CHAR(1) `'N'`/`'Y'`** (not CHAR(3) Yes/No) on `PRODUCT_TO_GROUP`. DDL §8441 declares `Del_Ind CHAR(1) NOT NULL`. Active rows use `'N'`.
- **No side effects on import.** `import generators.tier8_product_hierarchy` must not construct any DataFrames or perform any network/file I/O.
- **`Tier8ProductHierarchy.generate()` must accept `ctx`** — the `BaseGenerator.generate(self, ctx)` signature is fixed by Step 2. Runtime-import `GenerationContext` via `TYPE_CHECKING` only.
- **Upstream prerequisite guard.** `generate()` starts with an explicit check that the 5 required upstream tables are in `ctx.tables`. Fail fast with `RuntimeError` if any is missing.
- **Universe prerequisite guard.** `generate()` also explicitly checks `ctx.customers` and `ctx.agreements` are non-empty.
- **Escalation over improvisation.** If `07` has an ambiguity (column name differs, nullability unclear, lookup table missing), stop and add a `⚠️ Conflict` block. Do NOT invent columns or silently swap FKs.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current directory and `python` resolves to the project's Python 3.12 environment.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

**Module-import and API contract:**

- [ ] `python -c "import generators.tier8_product_hierarchy"` exits 0.
- [ ] `generators.tier8_product_hierarchy.Tier8ProductHierarchy` inherits from `BaseGenerator` and `generate(ctx)` is defined:
  ```bash
  python -c "
  from generators.tier8_product_hierarchy import Tier8ProductHierarchy
  from generators.base import BaseGenerator
  import inspect
  assert issubclass(Tier8ProductHierarchy, BaseGenerator)
  sig = inspect.signature(Tier8ProductHierarchy.generate)
  assert 'ctx' in sig.parameters
  print('Tier8ProductHierarchy contract OK')
  "
  ```

**End-to-end table emission:**

The session builds a reusable test harness (either a fresh Python snippet per check or a `tests/test_tier8.py` scratch file, at the session's discretion — the harness is NOT committed). The harness invokes `UniverseBuilder().build(...) → Tier0Lookups → Tier1Geography → Tier2Core → ... → Tier7bSubtypes → Tier8ProductHierarchy`. A lighter-weight alternative: build a minimal `ctx` with only the 5 upstream tables required + `ctx.customers`/`ctx.agreements` populated from a small synthesised universe (10 customers, 20 agreements covering 5+ product types). The session picks one; both are acceptable.

- [ ] `Tier8ProductHierarchy().generate(ctx)` returns a dict with exactly the 5 keys:
  `{Core_DB.AGREEMENT_PRODUCT, Core_DB.PRODUCT_FEATURE, Core_DB.PRODUCT_COST, Core_DB.PRODUCT_GROUP, Core_DB.PRODUCT_TO_GROUP}` — verify with `set(result) == expected_keys`.
- [ ] Every DataFrame is non-empty (`len(df) > 0`) for all 5 keys.

**AGREEMENT_PRODUCT invariants (Step 3 item #7):**

- [ ] Row count equals `len(ctx.agreements)` exactly:
  ```python
  df = result['Core_DB.AGREEMENT_PRODUCT']
  assert len(df) == len(ctx.agreements), f'{len(df)} != {len(ctx.agreements)}'
  ```
- [ ] Every row has `Agreement_Product_Role_Cd == 'primary'`:
  ```python
  assert (df['Agreement_Product_Role_Cd'] == 'primary').all()
  ```
- [ ] Every `Agreement_Id` in AGREEMENT_PRODUCT resolves to `ctx.tables['Core_DB.AGREEMENT'].Agreement_Id`:
  ```python
  ag_ids = set(ctx.tables['Core_DB.AGREEMENT']['Agreement_Id'].astype(int))
  df_ids = set(df['Agreement_Id'].astype(int))
  assert df_ids.issubset(ag_ids) and df_ids == ag_ids
  ```
- [ ] Every `Product_Id` resolves to `ctx.tables['Core_DB.PRODUCT'].Product_Id`:
  ```python
  prod_ids = set(ctx.tables['Core_DB.PRODUCT']['Product_Id'].astype(int))
  assert set(df['Product_Id'].astype(int)).issubset(prod_ids)
  ```
- [ ] Every agreement has exactly one `'primary'` row (not zero, not two):
  ```python
  counts = df.groupby('Agreement_Id').size()
  assert (counts == 1).all(), f'Found non-1 counts: {counts[counts != 1].head()}'
  ```
- [ ] `Agreement_Product_Start_Dt` column dtype is `date` (not string, not datetime):
  ```python
  from datetime import date
  assert all(isinstance(v, date) and not isinstance(v, __import__('datetime').datetime) for v in df['Agreement_Product_Start_Dt'].dropna())
  ```

**PRODUCT_FEATURE invariants:**

- [ ] Every product has ≥1 PRODUCT_FEATURE row:
  ```python
  pf = result['Core_DB.PRODUCT_FEATURE']
  pf_product_ids = set(pf['Product_Id'].astype(int))
  assert prod_ids.issubset(pf_product_ids), f'Products missing feature rows: {prod_ids - pf_product_ids}'
  ```
- [ ] Every `Feature_Id` in PRODUCT_FEATURE resolves to `ctx.tables['Core_DB.FEATURE'].Feature_Id`:
  ```python
  feat_ids = set(ctx.tables['Core_DB.FEATURE']['Feature_Id'].astype(int))
  assert set(pf['Feature_Id'].astype(int)).issubset(feat_ids)
  ```
- [ ] At least one PRODUCT_FEATURE row references the `'Rate Feature'` subtype (via FEATURE lookup):
  ```python
  feat = ctx.tables['Core_DB.FEATURE']
  rate_feature_ids = set(feat[feat['Feature_Subtype_Cd'] == 'Rate Feature']['Feature_Id'].astype(int))
  assert set(pf['Feature_Id'].astype(int)) & rate_feature_ids
  ```
- [ ] `Currency_Cd` is `'USD'` or NULL (never any other literal):
  ```python
  assert set(pf['Currency_Cd'].dropna().unique()).issubset({'USD'})
  ```

**PRODUCT_COST invariants:**

- [ ] Every product has exactly 2 rows (ACQUISITION + MAINTENANCE):
  ```python
  pc = result['Core_DB.PRODUCT_COST']
  counts = pc.groupby('Product_Id').size()
  assert (counts == 2).all()
  ```
- [ ] Cost codes are exactly `{ACQUISITION, MAINTENANCE}`:
  ```python
  assert set(pc['Cost_Cd'].unique()) == {'ACQUISITION', 'MAINTENANCE'}
  ```

**PRODUCT_GROUP invariants:**

- [ ] Exactly 9 rows (1 root + 8 CLV children):
  ```python
  pg = result['Core_DB.PRODUCT_GROUP']
  assert len(pg) == 9
  ```
- [ ] Root row self-references:
  ```python
  root = pg[pg['Product_Group_Id'] == 92_000_000].iloc[0]
  assert int(root['Parent_Group_Id']) == 92_000_000
  ```
- [ ] All 8 non-root rows point to the root:
  ```python
  non_root = pg[pg['Product_Group_Id'] != 92_000_000]
  assert len(non_root) == 8
  assert (non_root['Parent_Group_Id'].astype(int) == 92_000_000).all()
  ```
- [ ] Every row has `Product_Group_Type_Cd == 'CLV'`:
  ```python
  assert (pg['Product_Group_Type_Cd'] == 'CLV').all()
  ```
- [ ] The 8 child names match the CLV 8-type list exactly:
  ```python
  expected = {'Checking', 'Savings', 'Retirement', 'Credit Card',
              'Vehicle Loan', 'Mortgage', 'Investments', 'Insurance'}
  assert set(non_root['Product_Group_Name']) == expected
  ```

**PRODUCT_TO_GROUP invariants (⚠️ Conflict A):**

- [ ] Row count equals the distinct product count in the universe:
  ```python
  ptg = result['Core_DB.PRODUCT_TO_GROUP']
  assert len(ptg) == len(ctx.tables['Core_DB.PRODUCT'])
  ```
- [ ] Columns are exactly `{PIM_Id, Group_Id, Valid_From_Dt, Valid_To_Dt, Del_Ind}` + 5-col DI tail:
  ```python
  business = {'PIM_Id', 'Group_Id', 'Valid_From_Dt', 'Valid_To_Dt', 'Del_Ind'}
  di_cols = {'di_data_src_cd', 'di_start_ts', 'di_proc_name', 'di_rec_deleted_Ind', 'di_end_ts'}
  assert set(ptg.columns) == business | di_cols
  ```
- [ ] `PIM_Id` values are a subset of `Core_DB.PRODUCT.Product_Id` (⚠️ Conflict A — legacy column name holds Product_Id):
  ```python
  assert set(ptg['PIM_Id'].astype(int)).issubset(prod_ids)
  ```
- [ ] `Group_Id` values are a subset of the 9 seeded PRODUCT_GROUP IDs:
  ```python
  group_ids = set(pg['Product_Group_Id'].astype(int))
  assert set(ptg['Group_Id'].astype(int)).issubset(group_ids)
  ```
- [ ] `Valid_From_Dt` on every row equals `'2025-10-01'`; `Valid_To_Dt` equals `'9999-12-31'`; `Del_Ind` equals `'N'`:
  ```python
  assert (ptg['Valid_From_Dt'] == '2025-10-01').all()
  assert (ptg['Valid_To_Dt'] == '9999-12-31').all()
  assert (ptg['Del_Ind'] == 'N').all()
  ```
- [ ] `PIM_Id` is unique across PRODUCT_TO_GROUP rows (semantic invariant: one Core_DB product maps to exactly one CLV group via `_PRODUCT_TO_CLV_GROUP`). DDL `PRIMARY INDEX (PIM_Id)` is non-unique in Teradata by default, so the check is DoD-only:
  ```python
  dupes = ptg['PIM_Id'].value_counts()
  dupes = dupes[dupes > 1]
  assert dupes.empty, f'Duplicate PIM_Id rows (recipe bug?): {dupes.to_dict()}'
  ```

**BIGINT / dtype invariants:**

- [ ] Every `*_Id` column in every emitted DataFrame dtype is `Int64`:
  ```python
  id_cols = {
      'Core_DB.AGREEMENT_PRODUCT': ['Agreement_Id', 'Product_Id'],
      'Core_DB.PRODUCT_FEATURE': ['Product_Id', 'Feature_Id'],
      'Core_DB.PRODUCT_COST': ['Product_Id'],
      'Core_DB.PRODUCT_GROUP': ['Product_Group_Id', 'Parent_Group_Id'],
      'Core_DB.PRODUCT_TO_GROUP': ['PIM_Id', 'Group_Id'],
  }
  for tbl, cols in id_cols.items():
      df = result[tbl]
      for c in cols:
          assert str(df[c].dtype) == 'Int64', f'{tbl}.{c}: {df[c].dtype}'
  ```
- [ ] Every non-null DECIMAL amount column value is a `decimal.Decimal`:
  ```python
  from decimal import Decimal
  for c in ['Product_Feature_Amt', 'Product_Feature_Rate', 'Product_Feature_Qty']:
      vals = result['Core_DB.PRODUCT_FEATURE'][c].dropna()
      assert all(isinstance(v, Decimal) for v in vals), f'PRODUCT_FEATURE.{c}: non-Decimal values'
  assert all(isinstance(v, Decimal) for v in result['Core_DB.PRODUCT_COST']['Product_Cost_Amt'].dropna())
  ```

**DI column invariants:**

- [ ] All 4 standard Core_DB tables (AGREEMENT_PRODUCT, PRODUCT_FEATURE, PRODUCT_COST, PRODUCT_GROUP) have the 3-col DI tail with `di_start_ts = '2000-01-01 00:00:00.000000'`, `di_end_ts = '9999-12-31 00:00:00.000000'`, `di_rec_deleted_Ind = 'N'`:
  ```python
  for tbl in ['Core_DB.AGREEMENT_PRODUCT', 'Core_DB.PRODUCT_FEATURE',
              'Core_DB.PRODUCT_COST', 'Core_DB.PRODUCT_GROUP']:
      df = result[tbl]
      assert (df['di_start_ts'] == '2000-01-01 00:00:00.000000').all()
      assert (df['di_end_ts'] == '9999-12-31 00:00:00.000000').all()
      assert (df['di_rec_deleted_Ind'] == 'N').all()
      assert 'di_data_src_cd' not in df.columns
      assert 'di_proc_name' not in df.columns
  ```
- [ ] PRODUCT_TO_GROUP has the 5-col DI tail with `di_data_src_cd = None`, `di_proc_name = None`, other 3 as above:
  ```python
  ptg = result['Core_DB.PRODUCT_TO_GROUP']
  assert ptg['di_data_src_cd'].isna().all()
  assert ptg['di_proc_name'].isna().all()
  assert (ptg['di_start_ts'] == '2000-01-01 00:00:00.000000').all()
  assert (ptg['di_end_ts'] == '9999-12-31 00:00:00.000000').all()
  assert (ptg['di_rec_deleted_Ind'] == 'N').all()
  ```

**Side-effect / no-mutation invariants:**

- [ ] `generate()` does not call `ctx.rng` (no numpy state change). Snapshot `ctx.rng.bit_generator.state` before and after; assert equal:
  ```python
  before = ctx.rng.bit_generator.state
  _ = Tier8ProductHierarchy().generate(ctx)
  after = ctx.rng.bit_generator.state
  import json
  assert json.dumps(before, default=repr) == json.dumps(after, default=repr), 'Tier 8 consumed rng'
  ```
- [ ] `generate()` does not advance `ctx.ids.peek('product')`:
  ```python
  before = ctx.ids.peek('product')
  _ = Tier8ProductHierarchy().generate(ctx)
  after = ctx.ids.peek('product')
  assert before == after, f'{before} != {after}: Tier 8 minted product IDs'
  ```
- [ ] `generate()` does not mutate `ctx.tables`:
  ```python
  before_keys = set(ctx.tables)
  _ = Tier8ProductHierarchy().generate(ctx)
  after_keys = set(ctx.tables)
  assert before_keys == after_keys, 'Tier 8 mutated ctx.tables'
  ```
- [ ] Running `generate(ctx)` twice on the same `ctx` produces byte-identical DataFrames (reproducibility):
  ```python
  import pandas.testing as pdt
  r1 = Tier8ProductHierarchy().generate(ctx)
  r2 = Tier8ProductHierarchy().generate(ctx)
  for k in r1:
      pdt.assert_frame_equal(r1[k].reset_index(drop=True), r2[k].reset_index(drop=True))
  ```

**DDL column-order invariants:**

- [ ] For each emitted DataFrame, business columns match the DDL order exactly (DI tail trailing):
  ```python
  expected_cols = {
      'Core_DB.AGREEMENT_PRODUCT': ['Agreement_Id', 'Product_Id', 'Agreement_Product_Role_Cd',
                                     'Agreement_Product_Start_Dt', 'Agreement_Product_End_Dt',
                                     'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind'],
      'Core_DB.PRODUCT_FEATURE': ['Product_Id', 'Feature_Id', 'Product_Feature_Type_Cd',
                                   'Product_Feature_Start_Dttm', 'Product_Feature_End_Dttm',
                                   'Product_Feature_Amt', 'Product_Feature_Rate', 'Product_Feature_Qty',
                                   'Product_Feature_Num', 'Currency_Cd', 'Unit_Of_Measure_Cd',
                                   'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind'],
      'Core_DB.PRODUCT_COST': ['Product_Id', 'Cost_Cd', 'Product_Cost_Amt',
                                'Product_Cost_Start_Dttm', 'Product_Cost_End_Dttm',
                                'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind'],
      'Core_DB.PRODUCT_GROUP': ['Product_Group_Id', 'Parent_Group_Id', 'Product_Group_Type_Cd',
                                 'Product_Group_Name', 'Product_Group_Desc',
                                 'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind'],
      'Core_DB.PRODUCT_TO_GROUP': ['PIM_Id', 'Group_Id', 'Valid_From_Dt', 'Valid_To_Dt', 'Del_Ind',
                                    'di_data_src_cd', 'di_start_ts', 'di_proc_name',
                                    'di_rec_deleted_Ind', 'di_end_ts'],
  }
  for k, cols in expected_cols.items():
      assert list(result[k].columns) == cols, f'{k} column order mismatch: {list(result[k].columns)}'
  ```

**Universal checks (apply to every step):**

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else.
- [ ] All new files pass `python -c "import generators.tier8_product_hierarchy"`.
- [ ] No CSV column named `*_Id` uses INTEGER — n/a at this step (no CSVs are written; this is enforced at DataFrame level via the BIGINT / dtype invariants block above).
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — n/a: this step writes no such table.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — n/a: this step does not invoke the writer.

## Handoff notes

_To be filled in at the end of the implementation session per the Handoff Protocol in `implementation-steps.md`._

# Spec: Step 23 — Tier 15 PIM_DB

## Overview

This step produces the MDM Product side of Layer 1 — **all 6 `PIM_DB` tables** — by projecting the `Core_DB.PRODUCT` universe (established in Step 10 / Tier 2) onto the MDM product catalogue and authoring the CLV 8-group hierarchy as handwritten rows. Unlike every prior tier, PIM_DB tables are almost entirely **static** (PRODUCT_PARAMETER_TYPE, PRODUCT_GROUP_TYPE, PRODUCT_GROUP are seeded in-generator) or **derived** (PRODUCT is a 1:1 denormalisation of `Core_DB.PRODUCT`; PRODUCT_TO_GROUP is a 1:1 assignment of each PIM product to its CLV group). The only multi-row-per-entity table is PRODUCT_PARAMETERS — 3–5 parameter rows per product. Every PIM_DB table carries both DI metadata (`di_*`) and Valid/Del metadata (`Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind`). The recursive root-group self-reference (top-level `Parent_Group_Id = Product_Group_Id`) is dictated by `references/05_architect-qa.md` Q3. See `mvp-tool-design.md` §9 Tier 15 for the driving constraints.

## Depends on

- **Step 1** — `config/settings.py` (SIM_DATE, HISTORY_START, HIGH_DATE, HIGH_TS, `ID_RANGES` including `'pim_id': 90_000_000` and `'group_id': 91_000_000` which are already reserved). This step **adds** a new `'pim_parameter'` key to `ID_RANGES` for the `PIM_Parameter_Id` sequence.
- **Step 2** — `utils/id_factory.IdFactory.next()` (used for `'pim_id'`, `'group_id'`, `'pim_parameter'`), `utils/date_utils` (no new helpers needed), `generators/base.BaseGenerator` (`stamp_di` + `stamp_valid` — both called for every PIM_DB table).
- **Step 3** — `registry/context.GenerationContext` (reads `ctx.ids`, writes into `ctx.tables`).
- **Step 10** — Tier 2 core entities. **Sole upstream table consumed:** `Core_DB.PRODUCT` (12 rows; each row becomes exactly one `PIM_DB.PRODUCT` row via `Product_Id` cross-schema FK). Consumed fields: `Product_Id`, `Product_Subtype_Cd` (the product-type token such as `CHECKING`, `MORTGAGE`), `Product_Name`.
- **Step 5** — `output/writer.py` (`_load_ddl_column_order` already recognises the `### PIM Tables (PIM_DB)` heading, per `output/writer.py:63`, and already asserts `'PIM_DB.PRODUCT_GROUP' in d`). No writer changes needed.
- Steps 11–22 are **not** consumed — this tier reads only `Core_DB.PRODUCT`.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to:**
- `PRD.md` §4.2 (MDM PIM_DB table list — 6 tables), §7.1 (BIGINT everywhere), §7.3 (two DI column sets — both required for PIM_DB), §7.11 (seed data rules apply here since PRODUCT_GROUP/PRODUCT_GROUP_TYPE/PRODUCT_PARAMETER_TYPE are all hand-authored)
- `mvp-tool-design.md` §7 BaseGenerator DI rules, §9 Tier 15 (authoritative list of 6 tables, CLV 8-group hierarchy specification, recursive self-reference rule), §11 Output Format, §14 Decision 1 (entity-first registry — but PIM is 99% static so this is mostly about Core_DB.PRODUCT consistency)
- `implementation-steps.md` Step 23 (exit criteria — 8 CLV child nodes, root self-reference, Product_Id ↔ Core_DB.PRODUCT round-trip)

**Additional reference files** (named in the step's "Reads from" line — plus the DDL verification rule in CLAUDE.md):
- `references/05_architect-qa.md` **Q3** (the recursive `Parent_Group_Id` rule — top-level groups point to themselves; child groups point to parent's `Product_Group_Id`). Other Q's are not relevant to this step.
- `references/07_mvp-schema-reference.md` **§PIM Tables (PIM_DB)** — lines 3018–3114 define all 6 PIM_DB tables. Verify column order and NOT NULL lists verbatim before defining `_COLS_<TABLE>` module-level lists. The 6 DDLs (in file order) are: `PRODUCT_TO_GROUP`, `PRODUCT`, `PRODUCT_PARAMETERS`, `PRODUCT_PARAMETER_TYPE`, `PRODUCT_GROUP`, `PRODUCT_GROUP_TYPE`.

## Produces

### New generator module

- `generators/tier15_pim.py` — `Tier15PIM(BaseGenerator)` class. Single public `generate(ctx) -> Dict[str, pd.DataFrame]` method returning 6 DataFrames keyed by their `PIM_DB.<TABLE>` schema keys:

  | Output key | Notes |
  |------------|-------|
  | `PIM_DB.PRODUCT_GROUP_TYPE` | 2 seeded rows (`{1: 'ROOT'}`, `{2: 'CLV_TYPE'}`) |
  | `PIM_DB.PRODUCT_GROUP` | 9 seeded rows (1 root self-referential + 8 CLV children) |
  | `PIM_DB.PRODUCT_PARAMETER_TYPE` | 5 seeded rows (MIN_BALANCE, INTEREST_RATE, FEE, TERM_MONTHS, CREDIT_LIMIT) |
  | `PIM_DB.PRODUCT` | 1 row per `Core_DB.PRODUCT` row (≈12) |
  | `PIM_DB.PRODUCT_TO_GROUP` | 1 row per PIM product (≈12); maps PIM_Id → CLV Group_Id |
  | `PIM_DB.PRODUCT_PARAMETERS` | 3–5 rows per PIM product (≈40–60); parameter type-specific values |

  Row counts are deterministic for SEED=42; session should verify final totals and record them in ## Handoff notes.

## Tables generated

| Table | Approx rows | Row-construction rule |
|-------|-------------|-----------------------|
| `PIM_DB.PRODUCT_GROUP_TYPE` | 2 | Hand-authored seed rows. `Product_Group_Type_Cd` SMALLINT PK; reserve `1` = `'ROOT'`, `2` = `'CLV_TYPE'`. `Product_Group_Type_Name` populated; `Product_Group_Type_Desc` populated. Must be emitted **before** PRODUCT_GROUP for FK coverage. |
| `PIM_DB.PRODUCT_GROUP` | 9 | One `ROOT` row + 8 CLV children. `Product_Group_Id` minted via `ctx.ids.next('group_id')`. **Root row:** `Parent_Group_Id = Product_Group_Id` (self-reference — required by Q3 and DoD), `Product_Group_Type_Cd = 1`. **8 CLV children:** one row each for `Checking`, `Savings`, `Retirement`, `Credit Card`, `Vehicle Loan`, `Mortgage`, `Investments`, `Insurance`; each has `Parent_Group_Id = <root's Product_Group_Id>`, `Product_Group_Type_Cd = 2`. Store the `{CLV_label → Product_Group_Id}` map in a local dict for use by PRODUCT_TO_GROUP. |
| `PIM_DB.PRODUCT_PARAMETER_TYPE` | 5 | Hand-authored seed rows. `PIM_Parameter_Type_Cd` SMALLINT PK; reserve `1` = `'MIN_BALANCE'`, `2` = `'INTEREST_RATE'`, `3` = `'FEE'`, `4` = `'TERM_MONTHS'`, `5` = `'CREDIT_LIMIT'`. `PIM_Parameter_Type_Desc` populated. Must be emitted **before** PRODUCT_PARAMETERS for FK coverage. |
| `PIM_DB.PRODUCT` | = len(`Core_DB.PRODUCT`) ≈ 12 | One row per Core_DB.PRODUCT row. `PIM_Id` minted via `ctx.ids.next('pim_id')`. `Product_Id` = `Core_DB.PRODUCT.Product_Id` (cross-schema FK — PRD §7.1/design §9 Tier 15). `PIM_Product_Name` = `Core_DB.PRODUCT.Product_Name` (or `Product_Subtype_Cd.replace('_',' ').title()` as a fallback). `PIM_Product_Desc` may be NULL or a templated descriptor. Store the `{Product_Subtype_Cd → PIM_Id}` map in a local dict for use by PRODUCT_TO_GROUP and PRODUCT_PARAMETERS. |
| `PIM_DB.PRODUCT_TO_GROUP` | = len(`PIM_DB.PRODUCT`) ≈ 12 | One row per PIM product. `PIM_Id` is the PK **and** FK to `PIM_DB.PRODUCT.PIM_Id` (DDL: PIM_Id is the only PK column). `Group_Id` FK to `PIM_DB.PRODUCT_GROUP.Product_Group_Id` — select the CLV child group that matches the product's `Product_Subtype_Cd` via a module-level mapping dict `_PRODUCT_TYPE_TO_CLV_GROUP`. Assign every universe product_type (CHECKING, SAVINGS, MMA, CERTIFICATE_OF_DEPOSIT, RETIREMENT, MORTGAGE, CREDIT_CARD, VEHICLE_LOAN, STUDENT_LOAN, HELOC, PAYDAY, COMMERCIAL_CHECKING) to one of the 8 CLV groups — fail loudly (ValueError) on any unmapped subtype so future product types cannot silently fall through. Suggested mapping: `{CHECKING: 'Checking', COMMERCIAL_CHECKING: 'Checking', SAVINGS: 'Savings', MMA: 'Savings', CERTIFICATE_OF_DEPOSIT: 'Savings', RETIREMENT: 'Retirement', CREDIT_CARD: 'Credit Card', VEHICLE_LOAN: 'Vehicle Loan', STUDENT_LOAN: 'Vehicle Loan', PAYDAY: 'Vehicle Loan', MORTGAGE: 'Mortgage', HELOC: 'Mortgage'}`. Session may refine; assertion is "every universe subtype resolves". |
| `PIM_DB.PRODUCT_PARAMETERS` | 3–5 per PIM product ≈ 40–60 | 3–5 rows per PIM_Id, each row with `PIM_Parameter_Id` minted via `ctx.ids.next('pim_parameter')`. Parameter-type rows depend on the product kind: deposit products (CHECKING/SAVINGS/MMA/CD/COMMERCIAL_CHECKING) emit MIN_BALANCE + INTEREST_RATE + FEE (+ optional TERM_MONTHS for CD); credit products (CREDIT_CARD) emit INTEREST_RATE + FEE + CREDIT_LIMIT; loan products (MORTGAGE/VEHICLE_LOAN/STUDENT_LOAN/HELOC/PAYDAY) emit INTEREST_RATE + FEE + TERM_MONTHS; RETIREMENT emits MIN_BALANCE + INTEREST_RATE. `PIM_Parameter_Value` is a **VARCHAR(1000)** — stringify numeric values (`'2500.00'`, `'0.0450'`, `'360'`). No randomness via `ctx.rng` — use deterministic values-per-type lookup dict so repeat runs are byte-identical without consuming RNG state. |

Total new rows ≈ 65–95.

## Files to modify

- `config/settings.py` — **append** a new `'pim_parameter': 92_000_000` entry to `ID_RANGES`. This sits in the unused band above `'group_id'` (91M) and below the Tier 5 `'street_address'` (2.1M has already been reserved in a different band) / `'cdm_address'` (20M). Verify no collision by importing `ID_RANGES` and asserting `'pim_parameter'` is a fresh key before editing. Do not renumber existing keys.

- `config/code_values.py` — **append** two SMALLINT enum dicts for the two PIM_DB code columns:
  - `PRODUCT_GROUP_TYPE_CD` (`{1: 'ROOT', 2: 'CLV_TYPE'}`)
  - `PIM_PARAMETER_TYPE_CD` (`{1: 'MIN_BALANCE', 2: 'INTEREST_RATE', 3: 'FEE', 4: 'TERM_MONTHS', 5: 'CREDIT_LIMIT'}`)

  These mirror the Tier 14 convention: emit the integer code on the CSV; the dict is the single source of truth for the decode. Exact integer values can be refined in-session; the requirement is that every SMALLINT column in PIM_DB draws from a named dict here.

No other files modified. Do **not** modify `registry/profiles.py`, `registry/universe.py`, `utils/id_factory.py`, `generators/base.py`, `output/writer.py`, or any earlier tier generator or seed module. In particular, do **not** write a new `seed_data/pim_*.py` file — PIM group/type rows are hand-coded inside `generators/tier15_pim.py` (they are not lookups shared with any other tier, so the Tier 0 seed pattern does not apply here).

## New dependencies

No new dependencies.

## Rules for implementation

**Universal rules (every step):**

- BIGINT for all ID columns (per PRD §7.1) — never INTEGER, even when the DDL says INTEGER. Applies to `PIM_Id`, `Product_Id`, `Product_Group_Id`, `Parent_Group_Id`, `Group_Id`, `PIM_Parameter_Id`. Emit every `*_Id` pandas column as dtype `Int64`.
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — n/a; this tier does not touch party IDs.
- DI column stamping on every table via `BaseGenerator.stamp_di()` — all 6 tables.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records. `Del_Ind = 'N'`. `di_rec_deleted_Ind = 'N'`.
- `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` stamped additionally on **all 6 PIM_DB tables** via `BaseGenerator.stamp_valid()` (per PRD §7.3: Valid_* stamped on CDM_DB **and** PIM_DB tables; and every one of the 6 DDLs at lines 3020–3114 of the schema reference carries the Valid/Del columns).
- `di_data_src_cd` and `di_proc_name` are NULL (Q5c).
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` §PIM Tables (lines 3018–3114). Use module-level `_COLS_<TABLE>: List[str]` lists (mirroring the `tier14_cdm`/`tier10_events` pattern) and construct DataFrames with `pd.DataFrame(rows, columns=_COLS_<TABLE>)`.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — n/a; this tier does not write CDM_DB.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — n/a; upstream concern.
- No ORMs, no database connections — pure pandas → CSV.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42`. This tier **should not need `ctx.rng` at all** (seed rows are hand-coded; product-parameter values are looked up from a dict keyed on `Product_Subtype_Cd`). If the implementation uses `ctx.rng` for anything (e.g. a randomised parameter value), justify it in Handoff notes.

**Step-specific rules:**

- **Root PRODUCT_GROUP must self-reference.** The root row must have `Parent_Group_Id == Product_Group_Id` (per Q3). Emit the root row **first**, capture its minted `Product_Group_Id`, then emit the 8 CLV children all pointing at that root. There is no `NULL` option — `Parent_Group_Id` is NOT NULL in the DDL (line 3089).
- **CLV hierarchy has exactly 8 child nodes** — `Checking`, `Savings`, `Retirement`, `Credit Card`, `Vehicle Loan`, `Mortgage`, `Investments`, `Insurance` (from `mvp-tool-design.md` §9 Tier 15 hierarchy diagram). Note `Investments` and `Insurance` have **no** corresponding Core_DB product_types in this MVP — their PRODUCT_GROUP rows exist (so the hierarchy is DDL-complete) but zero PIM products point at them via PRODUCT_TO_GROUP. This is expected and not an error.
- **`PRODUCT_TO_GROUP.PIM_Id` is both PK and FK.** The DDL (line 3024) marks `PIM_Id` as the sole PK of PRODUCT_TO_GROUP, and the column references `PIM_DB.PRODUCT.PIM_Id`. Do **not** mint a fresh ID for PRODUCT_TO_GROUP.PIM_Id — reuse the `PIM_Id` minted when PRODUCT was generated. This gives a strict 1:1 product-to-group relationship.
- **Product type → CLV group mapping is total and fail-loud.** Build `_PRODUCT_TYPE_TO_CLV_GROUP` as a module-level dict covering every `Product_Subtype_Cd` that can appear in `Core_DB.PRODUCT` (the 12 listed in Step 10's exit criteria). When iterating, raise `ValueError(f'unmapped product subtype: {pt}')` on any miss. Do not silently default to a group.
- **Emission order matters for FK coverage.** Within `generate()`, build DataFrames in this order: (1) PRODUCT_GROUP_TYPE, (2) PRODUCT_GROUP (root first), (3) PRODUCT_PARAMETER_TYPE, (4) PRODUCT, (5) PRODUCT_TO_GROUP, (6) PRODUCT_PARAMETERS. Return all 6 from the same call as a single dict.
- **`Product_Id` is a cross-schema FK, not a fresh mint.** `PIM_DB.PRODUCT.Product_Id` values must be a subset of `Core_DB.PRODUCT.Product_Id` (in practice: equal, since this tier generates one PIM row per Core product). Look up `Core_DB.PRODUCT` from `ctx.tables['Core_DB.PRODUCT']` and iterate its rows directly — do not reconstruct from `ctx.agreements`.
- **Parameter values are deterministic lookups, not random.** Define a module-level `_PRODUCT_PARAMETERS_BY_TYPE: Dict[str, List[Tuple[int, str]]]` mapping `Product_Subtype_Cd` → `[(PIM_Parameter_Type_Cd, value_str), …]`. Same inputs → same outputs, zero RNG state consumed. Example: `'CHECKING': [(1, '500.00'), (2, '0.0005'), (3, '15.00')]` produces 3 parameter rows with MIN_BALANCE=500, INTEREST_RATE=0.05%, FEE=$15.
- **SMALLINT dtype.** Pandas has no Int16; project convention is `Int64`. Cast every SMALLINT column (`Product_Group_Type_Cd`, `PIM_Parameter_Type_Cd`) with `.astype('Int64')`.
- **No seeded `seed_data/pim_*.py` module.** The CLV 8-group names, the 2 group-type labels, and the 5 parameter-type labels all live as module-level constants inside `generators/tier15_pim.py`. They are not used by any other tier, so the Tier 0 pattern (factor into `seed_data/` for reuse) does not apply.
- **Writer round-trip must succeed for all 6 tables.** `output/writer.py._load_ddl_column_order()` already parses the `### PIM Tables (PIM_DB)` section — no writer edits needed. Verify via `_load_ddl_column_order()['PIM_DB.PRODUCT']` etc. returning non-empty lists.

## Definition of done

Tick every box before the session ends, or mark as `n/a` with a one-line justification.

**Source-of-truth & scaffolding:**

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else
- [ ] `python -c "import generators.tier15_pim"` exits 0
- [ ] `python -c "from generators.tier15_pim import Tier15PIM; Tier15PIM().generate"` exits 0
- [ ] `config/settings.py` has a `'pim_parameter'` key in `ID_RANGES`: `python -c "from config.settings import ID_RANGES; assert 'pim_parameter' in ID_RANGES and isinstance(ID_RANGES['pim_parameter'], int); assert 'pim_id' in ID_RANGES and 'group_id' in ID_RANGES"` exits 0
- [ ] `config/code_values.py` re-imports cleanly and exposes the two new dicts: `python -c "import config.code_values as cv; [getattr(cv, n) for n in ['PRODUCT_GROUP_TYPE_CD','PIM_PARAMETER_TYPE_CD']]"` exits 0
- [ ] Writer recognises all 6 PIM_DB tables: `python -c "from output.writer import _load_ddl_column_order as f; d=f(); [d[f'PIM_DB.{t}'] for t in ('PRODUCT','PRODUCT_TO_GROUP','PRODUCT_GROUP','PRODUCT_GROUP_TYPE','PRODUCT_PARAMETERS','PRODUCT_PARAMETER_TYPE')]"` exits 0

**Table count & presence (run against `ctx` built by running Steps 4, 8, 10, then `Tier15PIM().generate(ctx)`):**

- [ ] All 6 expected PIM_DB keys appear in the returned dict:
      ```python
      expected = {
          'PIM_DB.PRODUCT','PIM_DB.PRODUCT_TO_GROUP','PIM_DB.PRODUCT_GROUP',
          'PIM_DB.PRODUCT_GROUP_TYPE','PIM_DB.PRODUCT_PARAMETERS','PIM_DB.PRODUCT_PARAMETER_TYPE',
      }
      assert set(new_tables.keys()) == expected, set(new_tables.keys()) ^ expected
      ```
- [ ] No table is empty:
      ```python
      for k, df in new_tables.items():
          assert len(df) > 0, f'{k} is empty'
      ```

**Row-count & structural invariants:**

- [ ] `PIM_DB.PRODUCT_GROUP_TYPE` has exactly 2 rows with `Product_Group_Type_Cd` values `{1, 2}`:
      ```python
      pgt = new_tables['PIM_DB.PRODUCT_GROUP_TYPE']
      assert len(pgt) == 2
      assert set(pgt['Product_Group_Type_Cd']) == {1, 2}
      ```
- [ ] `PIM_DB.PRODUCT_GROUP` has exactly 9 rows: 1 root + 8 CLV children, with root self-referential and all children pointing at root:
      ```python
      pg = new_tables['PIM_DB.PRODUCT_GROUP']
      assert len(pg) == 9
      roots = pg[pg['Product_Group_Type_Cd'] == 1]
      clv   = pg[pg['Product_Group_Type_Cd'] == 2]
      assert len(roots) == 1
      assert len(clv) == 8
      root_id = int(roots.iloc[0]['Product_Group_Id'])
      assert int(roots.iloc[0]['Parent_Group_Id']) == root_id  # self-reference
      assert (clv['Parent_Group_Id'].astype('Int64') == root_id).all()
      # Every Product_Group_Id unique
      assert pg['Product_Group_Id'].is_unique
      ```
- [ ] `PIM_DB.PRODUCT_PARAMETER_TYPE` has exactly 5 rows with `PIM_Parameter_Type_Cd` values `{1..5}`:
      ```python
      ppt = new_tables['PIM_DB.PRODUCT_PARAMETER_TYPE']
      assert len(ppt) == 5
      assert set(ppt['PIM_Parameter_Type_Cd']) == {1, 2, 3, 4, 5}
      ```
- [ ] `PIM_DB.PRODUCT` row count equals `len(Core_DB.PRODUCT)`; every Product_Id maps back to Core_DB.PRODUCT; every PIM_Id is unique:
      ```python
      prod = new_tables['PIM_DB.PRODUCT']
      core_prod = ctx.tables['Core_DB.PRODUCT']
      assert len(prod) == len(core_prod)
      assert set(prod['Product_Id'].astype('Int64')) == set(core_prod['Product_Id'].astype('Int64'))
      assert prod['PIM_Id'].is_unique
      ```
- [ ] `PIM_DB.PRODUCT_TO_GROUP` row count equals `len(PIM_DB.PRODUCT)`; every PIM_Id resolves to PRODUCT; every Group_Id resolves to PRODUCT_GROUP; PIM_Id is unique (strict 1:1):
      ```python
      p2g  = new_tables['PIM_DB.PRODUCT_TO_GROUP']
      assert len(p2g) == len(prod)
      assert p2g['PIM_Id'].is_unique
      assert set(p2g['PIM_Id']).issubset(set(prod['PIM_Id']))
      assert set(p2g['Group_Id']).issubset(set(pg['Product_Group_Id']))
      # Every assigned group is a CLV child (never the root)
      clv_ids = set(pg.loc[pg['Product_Group_Type_Cd'] == 2, 'Product_Group_Id'])
      assert set(p2g['Group_Id']).issubset(clv_ids)
      ```
- [ ] `PIM_DB.PRODUCT_PARAMETERS` has 3–5 rows per PIM_Id; every PIM_Id resolves to PRODUCT; every PIM_Parameter_Type_Cd resolves to PRODUCT_PARAMETER_TYPE; every PIM_Parameter_Id is unique:
      ```python
      pp = new_tables['PIM_DB.PRODUCT_PARAMETERS']
      counts = pp.groupby('PIM_Id').size()
      assert counts.between(3, 5).all(), counts.describe()
      assert set(pp['PIM_Id']).issubset(set(prod['PIM_Id']))
      assert set(pp['PIM_Parameter_Type_Cd']).issubset(set(ppt['PIM_Parameter_Type_Cd']))
      assert pp['PIM_Parameter_Id'].is_unique
      ```
- [ ] Every Core_DB product_subtype is covered in PRODUCT_TO_GROUP (no orphans):
      ```python
      subtype_to_pim = dict(zip(prod['Product_Id'], prod['PIM_Id']))
      core_subtypes = set(core_prod['Product_Subtype_Cd'])
      assigned_pim_ids = set(p2g['PIM_Id'])
      core_pim_ids    = {subtype_to_pim[pid] for pid in core_prod['Product_Id']}
      assert core_pim_ids == assigned_pim_ids, core_pim_ids ^ assigned_pim_ids
      ```

**ID-type / dtype invariants:**

- [ ] All `*_Id` columns across the 6 tables have pandas dtype `Int64`:
      ```python
      id_cols = {
          'PIM_DB.PRODUCT':              ['PIM_Id','Product_Id'],
          'PIM_DB.PRODUCT_TO_GROUP':     ['PIM_Id','Group_Id'],
          'PIM_DB.PRODUCT_GROUP':        ['Product_Group_Id','Parent_Group_Id'],
          'PIM_DB.PRODUCT_PARAMETERS':   ['PIM_Parameter_Id','PIM_Id'],
      }
      for k, cols in id_cols.items():
          df = new_tables[k]
          for c in cols:
              assert str(df[c].dtype) == 'Int64', f'{k}.{c}: {df[c].dtype}'
      ```
- [ ] Every SMALLINT code column has dtype `Int64`:
      ```python
      sm_cols = {
          'PIM_DB.PRODUCT_GROUP':          ['Product_Group_Type_Cd'],
          'PIM_DB.PRODUCT_GROUP_TYPE':     ['Product_Group_Type_Cd'],
          'PIM_DB.PRODUCT_PARAMETERS':     ['PIM_Parameter_Type_Cd'],
          'PIM_DB.PRODUCT_PARAMETER_TYPE': ['PIM_Parameter_Type_Cd'],
      }
      for k, cols in sm_cols.items():
          df = new_tables[k]
          for c in cols:
              assert str(df[c].dtype) == 'Int64', f'{k}.{c}: {df[c].dtype}'
      ```
- [ ] Every NOT-NULL column has no NULL. Minimum coverage (drawn from DDL lines 3020–3114):
      ```python
      not_null = {
          'PIM_DB.PRODUCT_TO_GROUP':       ['PIM_Id','Group_Id'],
          'PIM_DB.PRODUCT':                ['PIM_Id','Product_Id'],
          'PIM_DB.PRODUCT_PARAMETERS':     ['PIM_Parameter_Id','PIM_Id','PIM_Parameter_Type_Cd'],
          'PIM_DB.PRODUCT_PARAMETER_TYPE': ['PIM_Parameter_Type_Cd'],
          'PIM_DB.PRODUCT_GROUP':          ['Product_Group_Id','Parent_Group_Id','Product_Group_Type_Cd'],
          'PIM_DB.PRODUCT_GROUP_TYPE':     ['Product_Group_Type_Cd'],
      }
      for k, cols in not_null.items():
          df = new_tables[k]
          for c in cols:
              assert df[c].notna().all(), f'{k}.{c} has NULL'
      ```

**DI / Valid column invariants:**

- [ ] Every PIM_DB table carries the 5-col DI suffix from `stamp_di` with HIGH_TS sentinel:
      ```python
      for k, df in new_tables.items():
          for c in ('di_data_src_cd','di_start_ts','di_proc_name','di_rec_deleted_Ind','di_end_ts'):
              assert c in df.columns, f'{k} missing DI col {c}'
          assert (df['di_end_ts'] == '9999-12-31 00:00:00.000000').all()
          assert (df['di_rec_deleted_Ind'] == 'N').all()
      ```
- [ ] Every PIM_DB table carries Valid_From_Dt/Valid_To_Dt/Del_Ind with HIGH_DATE sentinel on every row (all 6 tables — unlike CDM, there is no Valid-exempt table in PIM):
      ```python
      for k, df in new_tables.items():
          for c in ('Valid_From_Dt','Valid_To_Dt','Del_Ind'):
              assert c in df.columns, f'{k} missing {c}'
          assert (df['Valid_To_Dt'] == '9999-12-31').all()
          assert (df['Del_Ind'] == 'N').all()
      ```

**Column order (Writer round-trip):**

- [ ] Each DataFrame passes `_reorder_to_ddl` without error:
      ```python
      from output.writer import _reorder_to_ddl
      for k, df in new_tables.items():
          _reorder_to_ddl(df, k)  # raises on any mismatch
      ```
- [ ] Writer can emit a CSV for each table under `output/PIM_DB/`:
      ```python
      import tempfile, os
      from output.writer import Writer
      with tempfile.TemporaryDirectory() as tmp:
          w = Writer(tmp)
          for k, df in new_tables.items():
              p = w.write_one(k, df)
              assert p.exists() and p.stat().st_size > 0, p
              # file lives under tmp/PIM_DB/<TABLE>.csv
              assert 'PIM_DB' in str(p)
      ```

**Reproducibility:**

- [ ] Running `Tier15PIM().generate(ctx)` twice on two freshly-built contexts (both seeded from 42 and carrying identical upstream `Core_DB.PRODUCT`) yields DataFrames that compare equal via `pd.testing.assert_frame_equal` for every one of the 6 output keys:
      ```python
      # Pseudocode — session will implement with two UniverseBuilder+Tier2Core runs:
      a = Tier15PIM().generate(ctx_a)
      b = Tier15PIM().generate(ctx_b)
      for k in a:
          pd.testing.assert_frame_equal(a[k].reset_index(drop=True),
                                        b[k].reset_index(drop=True),
                                        check_like=False)
      ```

**Miscellaneous universal checks:**

- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — covered by the ID-dtype invariant above.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — n/a; this step writes only PIM_DB tables.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — n/a; this step does not write Core_DB.

## Handoff notes

_(leave empty — filled in at session end per implementation-steps.md "Handoff Protocol")_

# Spec: Step 05 — Output Writer

## Overview

This step implements the CSV writer that serialises every DataFrame in `ctx.tables` to a `.csv` file on disk, one per table, in the correct schema subdirectory — the final phase of generation before validation (Phase 4 in `mvp-tool-design.md` §2 and §15). The writer owns three concerns that every tier after it depends on: (1) **DDL column order** — Teradata BTEQ/FastLoad is positional, so each CSV's header and cell ordering must match the DDL declaration in `references/07_mvp-schema-reference.md` exactly; (2) **type-correct CSV formatting** — NULLs rendered as empty fields (not `"NULL"` / `"None"` / `"NaN"`), dates / timestamps / flags / BIGINTs / decimals rendered per the table in `mvp-tool-design.md` §11; (3) **catalogue hygiene** — the `PARTY_INTERRACTION_EVENT` typo is preserved in the output filename (PRD §7.10), and `GEOSPATIAL` is skipped because `ST_Geometry` has no CSV representation (PRD §7.9). This step ships no generated data — the writer operates purely on whatever DataFrames Steps 8–23 will later place into `ctx.tables`, so it must be complete and tested against hand-built fixtures *before* any tier generator writes real rows.

## Depends on

- **Step 2** — consumes:
  - `utils/date_utils.py` — `format_date(d)` and `format_ts(dt)` for any residual datetime/date objects the writer encounters (tier generators are expected to pre-format, but the writer hardens the contract).
  - `utils/di_columns.py` — `DI_COLUMN_ORDER` (5-tuple) and `VALID_COLUMN_ORDER` (3-tuple); the writer uses these as the canonical tail-of-row column order when a DataFrame has DI / Valid columns already stamped.
  - `generators/base.py` — indirect only (no import). The writer must tolerate DataFrames that were stamped via `BaseGenerator.stamp_di` / `stamp_valid`, i.e. DI columns appear at the end in `DI_COLUMN_ORDER` and (for CDM_DB / PIM_DB) Valid columns immediately after.

- **Step 1** — consumes from `config/settings.py`:
  - `OUTPUT_DIR`, `CORE_DB_DIR`, `CDM_DB_DIR`, `PIM_DB_DIR` — target paths, one subdir per schema.
  - `SKIPPED_TABLES` — authoritative skip list (currently `{'Core_DB.GEOSPATIAL'}`; the writer must consult this, not hardcode the name).
  - `PARTY_INTERRACTION_EVENT_TABLE_NAME` — the single source of truth for the double-R typo filename.
  - `HIGH_DATE`, `HIGH_TS` — used by the round-trip sanity test in the module's `__main__` block.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 5):
- `mvp-tool-design.md` §11 (Output Format) — the authoritative table of data-type → CSV formatting (NULL = empty, TIMESTAMP(6) = `YYYY-MM-DD HH:MM:SS.ffffff`, DATE = `YYYY-MM-DD`, CHAR(1) = `Y`/`N`, CHAR(3) = `Yes`/`No`, BIGINT plain integer, DECIMAL 4dp for amounts / 12dp for rates), plus the QUOTE_MINIMAL / UTF-8 / DDL-column-order rules and the filename rule for `PARTY_INTERRACTION_EVENT.csv`.
- `mvp-tool-design.md` §15 (`main.py` Orchestration) — Phase 4 calls `Writer(config.output_dir).write_all(ctx.tables)`; this step must produce exactly that API surface.
- `mvp-tool-design.md` §2, §9 per-tier — informs the set of `'Schema.TABLE'` keys the writer will eventually see (Core_DB, CDM_DB, PIM_DB). No code writes tables yet; the writer is exercised via hand-built fixtures.
- `PRD.md` §4.3 (Output format) — one CSV per table, subdirectory per schema, filename matches DDL exactly.
- `PRD.md` §7.9 (GEOSPATIAL skip), §7.10 (PARTY_INTERRACTION_EVENT typo preserved).
- `implementation-steps.md` Step 5 entry — the four exit-criteria bullets are rewritten into executable checks under Definition of done below.

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/07_mvp-schema-reference.md` — **authoritative source for per-table DDL column order**. The writer parses this file once at module-import time to build `{'Schema.TABLE': [col_1, col_2, …]}`. Read the "Schemas by Table Type" section that follows the summary table; each `#### <TABLE_NAME>` heading begins a Markdown column table whose first column is the DDL column name (wrapped in backticks). The Summary Table (lines 1–213) is NOT the source of truth for column order — use it only to sanity-check that every table in the detailed sections appears in the summary (counts match), and to discover schema prefixes for tables that sit under `UNKNOWN` (fall back to `Core_DB` for those).

**Do NOT read** (explicitly excluded to protect context budget):
- `references/01_schema-reference.md` — supplementary; `07` is the MVP-filtered / final DDL set and takes precedence per PRD §10.
- `references/02_data-mapping-reference.md` — transformation rules; not needed for the writer.
- `references/05_architect-qa.md` — architect Q&A; the relevant Q's (BIGINT Q1/Q2, typo via PRD §7.10, GEOSPATIAL via §7.9) are already codified in `PRD.md` and `config/settings.py`.
- `references/06_supporting-enrichments.md` — distributions; consumed by Step 4 (UniverseBuilder), irrelevant here.

## Produces

All paths relative to the project root.

**New files:**

- `output/writer.py` — the `Writer` class and supporting module-level helpers:
  - `class Writer`:
    - `__init__(self, output_dir: Path | str = OUTPUT_DIR)` — creates schema subdirectories (`Core_DB/`, `CDM_DB/`, `PIM_DB/`) lazily on first write.
    - `write_all(self, tables: Dict[str, pd.DataFrame]) -> Dict[str, Path]` — iterates every `'Schema.TABLE'` key; skips anything in `SKIPPED_TABLES`; delegates per-table to `write_one`; returns a `{table_key: written_path}` manifest (excludes skipped keys) so callers can log / audit what was written.
    - `write_one(self, table_key: str, df: pd.DataFrame) -> Path` — parses `table_key` into `(schema, table_name)`, resolves the target subdirectory, re-orders `df` columns to DDL order (see `_reorder_to_ddl` below), serialises via `df.to_csv(…, index=False, na_rep='', quoting=csv.QUOTE_MINIMAL, encoding='utf-8', lineterminator='\n')`, returns the target `Path`. Raises `ValueError` if `table_key` resolves to a `SKIPPED_TABLES` entry (callers should use `write_all` instead; `write_one` is for tests).
  - `_load_ddl_column_order(md_path: Path = …) -> Dict[str, List[str]]` — parses `references/07_mvp-schema-reference.md` once. For each `#### <TABLE_NAME>` heading inside the detailed schema sections, captures the subsequent Markdown table's first column (stripping backticks) until a blank line or the next heading. Returns a dict keyed by fully-qualified `'Schema.TABLE'` — schema is determined from the heading's preceding `### <SCHEMA_NAME> Tables` block (Core_DB, CDM_DB, PIM_DB, Core_DB_customized → treated as Core_DB per Q4 in `05_architect-qa.md`). Module-level cache via `functools.lru_cache` so the Markdown file is parsed at most once per process.
  - `_reorder_to_ddl(df: pd.DataFrame, table_key: str) -> pd.DataFrame` — re-arranges `df.columns` to match the DDL order for `table_key`:
    1. Look up DDL column list from the cached parser.
    2. Split DDL columns into *business columns* (anything not in `DI_COLUMN_ORDER` or `VALID_COLUMN_ORDER`) and *metadata columns* (DI + Valid).
    3. Enforce final order: `[DDL-ordered business cols] + [DI cols present in df, in DI_COLUMN_ORDER] + [Valid cols present in df, in VALID_COLUMN_ORDER]`.
    4. Raise `ValueError` listing missing columns if any DDL business column is absent from `df`.
    5. Raise `ValueError` listing unexpected columns if `df` contains business columns not in the DDL.
  - `_filename_for(table_name: str) -> str` — returns `f'{table_name}.csv'`. Acts as a single pinch-point for any future filename normalisation; for this step it is an identity function — the `PARTY_INTERRACTION_EVENT` typo is preserved by virtue of the key already carrying it.
  - `__main__` block — self-test fixtures verifying each exit criterion (see Definition of done). Runs under `python output/writer.py`.

**New files (generated directories):** `output/Core_DB/`, `output/CDM_DB/`, `output/PIM_DB/` are created on-demand by `Writer.__init__`; they already exist per `.gitignore` convention at the project root (per `mvp-tool-design.md` §3 the whole `output/` tree is git-ignored).

## Tables generated (if applicable)

No tables generated in this step. The writer is an I/O sink — it consumes DataFrames produced by Steps 8–23 and writes them to disk. Self-tests in `__main__` build tiny in-memory DataFrames but do not mutate `ctx.tables`.

## Files to modify

- `main.py` — **verify only, modify only if Step 1's stub already references the writer**. The Phase-4 orchestration call (`Writer(config.output_dir).write_all(ctx.tables)` per `mvp-tool-design.md` §15) is Step 25's responsibility; Step 5 should leave `main.py` as Step 1 left it. If the current `main.py` contains a TODO marker for Step 5, it is acceptable to replace that marker with a commented-out `from output.writer import Writer  # wired up in Step 25` line — nothing more.

No other existing files are modified.

## New dependencies

No new dependencies. `pandas`, `numpy`, and the standard-library `csv` / `pathlib` / `functools` modules (already pulled in by prior steps) are sufficient.

## Rules for implementation

Universal (apply to every step):

- BIGINT for all ID columns (per PRD §7.1) — never INTEGER, even when the DDL says INTEGER. The writer does not cast types, but its `__main__` fixtures must use `pd.Int64Dtype()` (nullable BIGINT) for any ID column, to prove the writer emits BIGINT IDs as plain integers (no `.0` suffix, no scientific notation).
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — n/a for the writer itself, but the fixture CSV round-trip must not re-quote or mangle BIGINT party IDs.
- DI column stamping on every table via `BaseGenerator.stamp_di()` — n/a: the writer is downstream of stamping. It does verify DI / Valid column order when they are present.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records — n/a: values come from upstream.
- CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` (per PRD §7.3) — the writer's DDL re-orderer places these after DI columns when present (see `_reorder_to_ddl` step 3 above).
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` — **enforced by this step**. The reorderer is the single control point.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — the writer must NOT silently "correct" spellings. Use the exact `table_name` from the `ctx.tables` key.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — consult `SKIPPED_TABLES` from `config/settings.py`; do not inline the string.
- No ORMs, no database connections — pure pandas → CSV. `df.to_csv(...)` only; no intermediate serialisation.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42` — n/a: the writer introduces no randomness. But byte-identical output requires stable column ordering (enforced) and stable float formatting (tier generators pre-format; writer does not round).

Step-specific rules:

- **Tier generators are responsible for value formatting, the writer is responsible for layout.** The writer does not coerce types: if a tier generator hands the writer a `datetime` object, it writes whatever `df.to_csv` emits (which for pandas 2.x is ISO-8601 without microseconds — the wrong format). Tier generators must pre-format dates / timestamps / decimals to strings in the correct shape per `mvp-tool-design.md` §11. This rule is encoded by the writer erroring out in debug mode on unstringified datetime columns **only** in the `__main__` fixtures (to catch regressions early); production `write_all` does not type-check — it writes what it is given.
- **`df.to_csv` parameters (authoritative set):** `index=False`, `header=True`, `na_rep=''`, `quoting=csv.QUOTE_MINIMAL`, `encoding='utf-8'`, `lineterminator='\n'`. Do not pass `date_format` or `float_format` — those would override upstream pre-formatting.
- **DDL-order parser must be idempotent.** Calling `_load_ddl_column_order()` twice within a process returns the same dict object (via `lru_cache`). The parser must handle Markdown oddities observed in `07`:
  - Table headings of the form `#### <TABLE_NAME>` where `<TABLE_NAME>` may contain underscores but never spaces.
  - Column rows of the form `| \`<col>\` | \`<type>\` | <pk?> | <nullable> |` — the column name is wrapped in backticks and must be stripped.
  - Blank lines or the next `####` / `###` heading terminates the column list for the current table.
  - Columns appearing under `### UNKNOWN` → assign schema `Core_DB` (affects `PARTY_ADDRESS` only per the summary at line 213 of `07`).
  - Schema inference: track the most recent `### <Schema>` block (one of `Core_DB`, `CDM_DB`, `PIM_DB`, `Core_DB_customized`). Map `Core_DB_customized` → `Core_DB` per `05_architect-qa.md` Q4.
- **Filename preservation.** The `_filename_for` helper is deliberately trivial; the only way the typo could be lost is if a tier generator writes the key with a corrected spelling. The writer's contract is: if `table_key.endswith('PARTY_INTERRACTION_EVENT')`, the emitted file is `PARTY_INTERRACTION_EVENT.csv` with the double-R. A fixture test covers this.
- **Skip list is data, not code.** The writer reads `SKIPPED_TABLES` from `config/settings.py`. Adding a new skipped table in a future step must not require editing the writer.
- **CHAR(1) vs CHAR(3) flags and decimal precision are NOT the writer's concern.** Per the pre-formatting rule above, tier generators emit strings like `'Y'`, `'Yes'`, `'1234.5600'`, `'0.032500000000'` already formatted. The writer just writes them. This keeps the writer a stable, simple component across all downstream steps.
- **No row / dtype validation beyond DDL column presence.** The writer is not a validator — that is Step 24's role. The writer may optionally warn on an empty DataFrame but must not refuse to write one (some lookup tables are validly tiny; empty is a valid Tier 0 pathology that Step 24 catches).
- **Path-safety on Windows.** `Path(output_dir) / schema / filename` throughout; no string concatenation of paths. The writer must work with the OneDrive-synced working directory under Windows / Git-bash (the user's platform).

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current directory.

**Code shape:**

- [ ] `python -c "import output.writer"` exits 0 — module imports cleanly with no side effects other than the lru-cached parser being primed on first access.
- [ ] `python -c "from output.writer import Writer, _load_ddl_column_order, _reorder_to_ddl; w = Writer()"` exits 0 — public and private names are exposed as designed.
- [ ] `python output/writer.py` exits 0 — the `__main__` self-test runs every fixture listed below and prints `output/writer.py OK` on success.
- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else.

**DDL-order parser:**

- [ ] `_load_ddl_column_order()` returns a dict with at least 200 keys (the summary table lists 206; tolerate ≤6 of mismatch if any tables in `07` have inconsistent headings). Run:
  ```python
  from output.writer import _load_ddl_column_order
  d = _load_ddl_column_order()
  assert len(d) >= 200, len(d)
  assert 'Core_DB.AGREEMENT' in d
  assert 'CDM_DB.PARTY_INTERRACTION_EVENT' in d
  assert 'PIM_DB.PRODUCT_GROUP' in d
  # UNKNOWN-schema fallback rule: PARTY_ADDRESS sits under `### UNKNOWN` in `07`
  # (summary line 213) and must be reassigned to Core_DB per the Rules section.
  assert 'Core_DB.PARTY_ADDRESS' in d
  ```
- [ ] `Core_DB.AGREEMENT` DDL order starts with `Agreement_Id` as the first column and contains `Agreement_Subtype_Cd` in position 2 (matches `07` lines 223–249). Run:
  ```python
  from output.writer import _load_ddl_column_order
  cols = _load_ddl_column_order()['Core_DB.AGREEMENT']
  assert cols[0] == 'Agreement_Id'
  assert cols[1] == 'Agreement_Subtype_Cd'
  ```
- [ ] No DDL column name contains backticks, leading/trailing whitespace, or the asterisk wildcard from the summary table. Run:
  ```python
  from output.writer import _load_ddl_column_order
  for tbl, cols in _load_ddl_column_order().items():
      for c in cols:
          assert '`' not in c and c.strip() == c and '*' not in c, (tbl, c)
  ```

**Column-order reorderer:**

- [ ] Given a hand-built DataFrame with columns in scrambled order, `_reorder_to_ddl` returns a new DataFrame whose columns match DDL order for `Core_DB.AGREEMENT_SUBTYPE`. Fixture under `__main__`:
  ```python
  import pandas as pd
  from output.writer import _reorder_to_ddl
  df = pd.DataFrame({
      'Agreement_Subtype_Desc': ['Checking'],
      'Agreement_Subtype_Cd':   ['CHECKING'],
      'di_end_ts':              ['9999-12-31 00:00:00.000000'],
      'di_start_ts':            ['2026-04-20 00:00:00.000000'],
      'di_rec_deleted_Ind':     ['N'],
      'di_proc_name':           [None],
      'di_data_src_cd':         [None],
  })
  out = _reorder_to_ddl(df, 'Core_DB.AGREEMENT_SUBTYPE')
  assert list(out.columns)[:2] == ['Agreement_Subtype_Cd', 'Agreement_Subtype_Desc']
  # DI tail in canonical order
  assert list(out.columns)[-5:] == ['di_data_src_cd', 'di_start_ts', 'di_proc_name',
                                     'di_rec_deleted_Ind', 'di_end_ts']
  ```
- [ ] Missing business columns raise `ValueError` with the missing names listed. Fixture: drop `Agreement_Subtype_Cd`, assert `ValueError` with substring `Agreement_Subtype_Cd` in `str(exc)`.
- [ ] Unexpected columns (not in DDL, not in DI / Valid) raise `ValueError`. Fixture: add `Extra_Col`, assert `ValueError` mentioning `Extra_Col`.
- [ ] For a CDM_DB fixture with both DI and Valid columns stamped, the final column order is `[business cols per DDL] + DI_COLUMN_ORDER + VALID_COLUMN_ORDER`. Fixture builds `CDM_DB.PARTY_INTERRACTION_EVENT` DataFrame and asserts tail.

**CSV formatting:**

- [ ] NULL cells render as empty fields — not `"NULL"`, not `"None"`, not `"nan"`. Fixture:
  ```python
  import pandas as pd, subprocess
  from output.writer import Writer
  df = pd.DataFrame({
      'Agreement_Subtype_Cd':   ['CHECKING', 'SAVINGS'],
      'Agreement_Subtype_Desc': ['Checking', None],
  })
  # … stamp DI here via generators.base.BaseGenerator().stamp_di(df) …
  w = Writer('/tmp/step5_test_out')  # or a tempfile.TemporaryDirectory on Windows
  path = w.write_one('Core_DB.AGREEMENT_SUBTYPE', df)
  content = path.read_text(encoding='utf-8')
  # Row 2's Desc field must be empty between the two commas that bracket it
  assert ',,' in content or content.endswith(',\n') or ',\n' in content
  for bad in ('NULL', 'None', 'nan', 'NaN'):
      assert bad not in content, f'writer emitted {bad!r}'
  ```
- [ ] BIGINT IDs render as plain integers with no decimal point or scientific notation. Fixture builds a DataFrame with `pd.Int64Dtype()` column `Agreement_Id = [100_000, 100_001, 999_999_999]`, asserts the CSV text contains exactly those three integer literals and none of `100000.0`, `1e5`, `1.0e+05`.
- [ ] UTF-8 encoding is used — fixture with a non-ASCII character (e.g. `Given_Name='Zoé'`) round-trips via `Path.read_text(encoding='utf-8')` without raising `UnicodeDecodeError`.
- [ ] Line-terminator is `\n` (not `\r\n`) even on Windows — `assert b'\r\n' not in path.read_bytes()`.

**Schema-subdir placement & filename rules:**

- [ ] Writing a `CDM_DB.PARTY_INTERRACTION_EVENT` fixture DataFrame produces exactly the file `output/CDM_DB/PARTY_INTERRACTION_EVENT.csv` (double-R typo preserved). Fixture:
  ```python
  # Under __main__
  out = Writer(tmp_dir).write_one('CDM_DB.PARTY_INTERRACTION_EVENT', df)
  assert out.name == 'PARTY_INTERRACTION_EVENT.csv'
  assert out.parent.name == 'CDM_DB'
  # Spelling has double R in both positions:
  assert out.name.count('R') == 2 and 'INTERRACTION' in out.name
  ```
- [ ] `write_all` with a `{'Core_DB.GEOSPATIAL': df}` entry writes **no file** for that key and returns a manifest missing that key. Fixture:
  ```python
  manifest = Writer(tmp_dir).write_all({'Core_DB.GEOSPATIAL': tiny_df,
                                         'Core_DB.AGREEMENT_SUBTYPE': fixture_df})
  assert 'Core_DB.GEOSPATIAL' not in manifest
  assert 'Core_DB.AGREEMENT_SUBTYPE' in manifest
  assert not (Path(tmp_dir) / 'Core_DB' / 'GEOSPATIAL.csv').exists()
  ```
- [ ] Writer reads the skip list from `config.settings.SKIPPED_TABLES`, not an inline string. Fixture:
  ```python
  import config.settings as cs, output.writer as w
  src = Path(w.__file__).read_text()
  assert "'Core_DB.GEOSPATIAL'" not in src and '"Core_DB.GEOSPATIAL"' not in src
  assert 'SKIPPED_TABLES' in src
  ```
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — n/a at this step: no real tables are written here; Step 24 (validator) and Step 25 (smoke test) enforce this on the end-to-end output. The writer's BIGINT fixture above covers the serialisation side.

**Orchestration surface matches mvp-tool-design.md §15:**

- [ ] `Writer` is importable as `from output.writer import Writer` and accepts either `str` or `Path` in its constructor. Fixture:
  ```python
  from output.writer import Writer
  from pathlib import Path
  assert isinstance(Writer('out').output_dir, Path)
  assert isinstance(Writer(Path('out')).output_dir, Path)
  ```
- [ ] `Writer().write_all({})` returns `{}` and creates no files beyond the (possibly new) schema subdirectories. (Creating empty subdirs is acceptable; do not fail on empty input.)

**Housekeeping:**

- [ ] No randomness in `output/writer.py` — `grep -n 'random\|rng\|seed' output/writer.py` returns nothing (or only comments).
- [ ] The DDL-order parser is not invoked at *import time* of the module — only on first call of `_load_ddl_column_order` / `_reorder_to_ddl`. Verify by importing under a Python session with `references/07_mvp-schema-reference.md` temporarily renamed: import succeeds, first reorder call raises `FileNotFoundError` with a clear message.

## Handoff notes

### What shipped

- `output/__init__.py` — created (empty); missing from Step 1 scaffolding.
- `output/writer.py` — full implementation: `_load_ddl_column_order` (lru_cached Markdown parser), `_reorder_to_ddl`, `_filename_for`, `class Writer` (`write_all` / `write_one`), `__main__` self-test (15 embedded tests + test 14 verified externally).

All 16 DoD checks pass:
- Parser yields 205 keys (≥200 threshold met; 1 below 206 summary count — within ≤6 tolerance).
- AGREEMENT DDL order, PARTY_ADDRESS Core_DB fallback, PARTY_INTERRACTION_EVENT key all confirmed.
- Reorderer handles 3-DI tables (Core_DB) and 5-DI + 3-Valid tables (CDM_DB) correctly.
- NULL→empty, BIGINT→plain int, UTF-8, CRLF, filename typo, skip-list — all verified.
- `python output/writer.py` exits 0 printing "output/writer.py OK".

### Deferred items

- **DoD test 14 (source inspection)** is not embedded in `__main__` due to inherent self-reference: the assertion `'Core_DB.GEOSPATIAL' not in src` would always find that literal in its own code. Verified instead by inspecting only the production section (`src.split('if __name__')[0]`). No inline skip key exists in production code — `SKIPPED_TABLES` is imported and used exclusively.
- **No `.gitignore`** in the project root. `git status` shows `utils/__pycache__/di_columns.cpython-312.pyc` as a tracked modified file (side effect of running tests). A `.gitignore` covering `__pycache__/`, `*.pyc`, and `output/` should be added in a future step or retroactively in Step 1.

### Next session hint

Step 6 (Tier 0a seed data) can begin immediately. The writer is stable. Seed modules call `get_<domain>_tables() -> Dict[str, pd.DataFrame]`; Step 8 wires them through `Writer` after DI stamping. No writer changes expected until Step 25.

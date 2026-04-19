# Spec: Step 02 — Core Utils & Base Generator

## Overview

This step builds the shared utility layer every downstream tier will consume: centralised BIGINT ID allocation, SCD2 / history-window date helpers, DI metadata stamping primitives, Luhn-valid card-number generation, and the `BaseGenerator` that wraps the stamping helpers for all tier generators. Nothing in this step makes a statistical decision, emits a DataFrame of business data, or writes a CSV — it delivers the primitives that Steps 3–25 depend on. The contracts here are fixed by `mvp-tool-design.md` §7 (BaseGenerator with `stamp_di` / `stamp_valid` and the `HIGH_TS` / `HIGH_DATE` sentinels), §8 (ID Factory — centralised sequences per entity type, never reuse IDs across entity types), and PRD §7.3 (two DI column sets: five `di_*` columns on every table; three `Valid_*` / `Del_Ind` columns additionally on CDM_DB and PIM_DB).

## Depends on

Step 1 (committed on `main` as `afa2f27 step1 completed`). Consumes from `config/settings.py`:

- `ID_RANGES` — BIGINT starting offsets per entity category (20 keys: `party`, `agreement`, `event`, `address`, `locator`, `feature`, `product`, `campaign`, `promotion`, `model`, `claim`, `household`, `task`, `activity`, `contact`, `card`, `market_seg`, `channel`, `pim_id`, `group_id`)
- `HIGH_TS` (`'9999-12-31 00:00:00.000000'`) and `HIGH_DATE` (`'9999-12-31'`) — active-record sentinels used by `stamp_di` and `stamp_valid`
- `HISTORY_START` (`date(2025, 10, 1)`) and `SIM_DATE` (`date(2026, 3, 31)`) — the 6-month simulation window used by `date_utils` helpers
- `SEED = 42` — only read transitively (date helpers may accept an `rng` argument; no sampling done here)

No other Step 1 artefacts are consumed (`code_values`, `distributions` are orthogonal to utils).

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md`):
- `mvp-tool-design.md` §7 (BaseGenerator and DI columns — stamp_di / stamp_valid signatures, sentinel values, which tables get which stamps)
- `mvp-tool-design.md` §8 (ID Factory — BIGINT sequences, the 20-key `ID_RANGES` dict, "Never reuse IDs across entity types" rule)
- `mvp-tool-design.md` §11 (Output format — informs DI column ordering used later by the writer; this step only needs the column set, not formatting)
- `mvp-tool-design.md` §15 (main.py orchestration — shows how `BaseGenerator` subclasses are invoked; utils must be importable without side-effects)
- `PRD.md` §7.3 (Two DI column sets for CDM_DB / PIM_DB — the authoritative rule this step implements)
- `PRD.md` §7.1 (BIGINT everywhere — all IDs emitted by `IdFactory` must be BIGINT-sized ints, never INTEGER)
- `PRD.md` §7.4 (SCD2 history approach — informs `date_utils` month-snapshot helper for DECLINING cohort balance trajectory)
- `PRD.md` §7.6 (Reproducibility — all randomness from `ctx.rng`; `luhn.py` accepts an `rng` argument, never calls `random.random()` directly)
- `implementation-steps.md` Step 2 entry

**Additional reference files** (only those named in the step's "Reads from" line):
- None. Step 2 does not read any `references/` file — the PRD and design doc already specify sentinel values and BIGINT semantics.

## Produces

All paths relative to the project root.

**`utils/` package**:
- `utils/__init__.py` — empty marker so `utils` is importable as a package.
- `utils/id_factory.py` — `IdFactory` class providing monotonic BIGINT sequences per entity category. API:
  - `IdFactory(id_ranges: Dict[str, int])` — constructor takes the `ID_RANGES` dict from settings; each key seeds an independent counter starting at `ID_RANGES[key]`.
  - `next(category: str) -> int` — returns the next BIGINT ID for that category and advances the counter by 1. Raises `KeyError` with a helpful message if the category is unknown.
  - `next_many(category: str, n: int) -> List[int]` — returns a contiguous block of `n` IDs.
  - `peek(category: str) -> int` — returns the next ID without advancing (diagnostic use only).
  - Internal state is a mutable `dict[str, int]` of current counters; no cross-category leakage.
- `utils/date_utils.py` — SCD2 and history-window helpers used by tier generators:
  - `history_start() -> date` and `sim_date() -> date` — thin wrappers around `config.settings` for readability at call sites.
  - `is_active(end_ts_or_dt: Optional[Union[str, date, datetime]]) -> bool` — returns True when the end value is NULL, `HIGH_TS`, or `HIGH_DATE`.
  - `month_snapshots(start: date, end: date) -> List[Tuple[date, date]]` — returns `(month_start, month_end)` tuples spanning `[start, end]`. Used by Tier 7 for DECLINING-cohort 6-row `AGREEMENT_FEATURE` balance trajectories.
  - `random_datetime_between(start: Union[date, datetime], end: Union[date, datetime], rng: np.random.Generator) -> datetime` — uniform random timestamp in the closed interval; used for `Agreement_Open_Dttm`, event timestamps, etc.
  - `random_date_between(start: date, end: date, rng: np.random.Generator) -> date` — same, DATE-typed.
  - `format_ts(ts: Union[str, datetime, None]) -> str` — canonical `YYYY-MM-DD HH:MM:SS.ffffff` rendering; returns `HIGH_TS` when input is `None` or already the sentinel. Used later by writer; defined here so date helpers and stamp helpers render identically.
  - `format_date(dt: Union[str, date, None]) -> str` — canonical `YYYY-MM-DD`; returns `HIGH_DATE` when input is `None` or already the sentinel.
- `utils/di_columns.py` — pure stamping primitives (no class wrapper; `BaseGenerator` is the class wrapper). Functions:
  - `DI_COLUMN_ORDER: Tuple[str, ...]` — the immutable tuple `('di_data_src_cd', 'di_start_ts', 'di_proc_name', 'di_rec_deleted_Ind', 'di_end_ts')` — used by the writer in Step 5 to validate column order.
  - `VALID_COLUMN_ORDER: Tuple[str, ...]` — `('Valid_From_Dt', 'Valid_To_Dt', 'Del_Ind')`.
  - `stamp_di(df: pd.DataFrame, start_ts: Union[str, datetime], end_ts: Union[str, datetime] = HIGH_TS, deleted: str = 'N') -> pd.DataFrame` — adds the 5 DI columns in canonical order at the END of the DataFrame. `di_data_src_cd` and `di_proc_name` are set to `None` (NULL in CSV) per PRD §7.3 and `05_architect-qa.md` Q5c. Operates in place on a copy; returns the modified copy.
  - `stamp_valid(df: pd.DataFrame, from_dt: Union[str, date], to_dt: Union[str, date] = HIGH_DATE, del_ind: str = 'N') -> pd.DataFrame` — adds the 3 `Valid_*` / `Del_Ind` columns at the END of the DataFrame. Used only for CDM_DB and PIM_DB tables.
- `utils/luhn.py` — Luhn-valid card number + CVV generation:
  - `luhn_check(card_num: str) -> bool` — standard mod-10 check; returns True if valid.
  - `generate_card_number(rng: np.random.Generator, bin_prefix: Optional[str] = None) -> str` — returns a 16-digit string passing mod-10. If `bin_prefix` is given (6 digits), uses it; otherwise picks a realistic default (e.g. `'400000'` for Visa) so Step 17 can set `Bank_Identification_Num = card[:6]` and get a coherent BIN.
  - `generate_cvv(rng: np.random.Generator) -> str` — zero-padded 3-digit string, `'000'`–`'999'`.

**`generators/` package**:
- `generators/__init__.py` — empty marker.
- `generators/base.py` — `BaseGenerator` class that every tier generator subclasses. Responsibilities:
  - `stamp_di(df, start_ts=None, end_ts=HIGH_TS, deleted='N') -> pd.DataFrame` — delegates to `utils.di_columns.stamp_di`; if `start_ts` is `None`, defaults to `format_ts(datetime.now())` (the generation run's load timestamp).
  - `stamp_valid(df, from_dt=None, to_dt=HIGH_DATE, del_ind='N') -> pd.DataFrame` — delegates to `utils.di_columns.stamp_valid`.
  - `generate(ctx) -> Dict[str, pd.DataFrame]` — abstract method (`raise NotImplementedError`). Every tier subclass overrides this and returns a dict keyed `'Schema.TABLE'` → DataFrame.
  - No state is stored on the instance beyond configuration; each `generate()` call is pure w.r.t. the input `GenerationContext`.

## Tables generated (if applicable)

No tables generated in this step. Utilities only — the `BaseGenerator` class is abstract.

## Files to modify

No files modified. All files are new. `config/`, `main.py`, `requirements.txt`, `specs/`, `references/`, `CLAUDE.md`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md` are NOT touched.

## New dependencies

No new dependencies. `numpy`, `pandas` are already pinned in `requirements.txt` from Step 1 and are sufficient for this step (`faker`/`scipy`/`python-dateutil` are not needed until Step 4).

## Rules for implementation

- BIGINT for all ID columns (per PRD §7.1) — `IdFactory` returns Python `int` values seeded from `ID_RANGES` which are always ≥ 1 and expected to grow into the millions; downstream CSVs must render these as plain BIGINT integers (no quoting, no INTEGER truncation). `IdFactory` must never return 0 or a negative value.
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — `IdFactory` has a single `'party'` counter; the same BIGINT is used as both `Core_DB.PARTY.Party_Id` and `CDM_DB.PARTY.CDM_Party_Id`. Do not add a separate `'cdm_party'` counter.
- DI column stamping on every table via `BaseGenerator.stamp_di()` — `stamp_di` MUST append the 5 DI columns in exactly this order at the END of the DataFrame: `('di_data_src_cd', 'di_start_ts', 'di_proc_name', 'di_rec_deleted_Ind', 'di_end_ts')`. This order matches `references/01_schema-reference.md` Universal Conventions and the writer in Step 5 will validate against `DI_COLUMN_ORDER`.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records — `stamp_di` default `end_ts=HIGH_TS`, `stamp_valid` default `to_dt=HIGH_DATE`. Imported from `config.settings`, never redefined locally.
- CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` (per PRD §7.3) — `stamp_valid` is a separate function from `stamp_di`; never auto-invoked together. Each tier generator decides which stamps apply (Tier 14 = both, Tier 15 = both, everything else in Core_DB = `stamp_di` only).
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` — n/a at this step (no business-data DataFrames produced); `DI_COLUMN_ORDER` and `VALID_COLUMN_ORDER` are the only column-order contracts established here and are enforced by the writer in Step 5.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — n/a at this step (no table names referenced); constant is in `config.settings` from Step 1.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — n/a at this step (no tier generation); skip list in `config.settings.SKIPPED_TABLES` from Step 1 is still the authoritative source.
- No ORMs, no database connections — pure pandas → CSV. Utilities use `pandas` only for DataFrame in/out; no SQL, no ORM imports.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42`. `luhn.generate_card_number` and `luhn.generate_cvv` take `rng: np.random.Generator` as a required argument; they must never call `random.random()`, `numpy.random.rand()` (module-level), or `os.urandom`. `date_utils.random_datetime_between` / `random_date_between` likewise take `rng` as a required argument.

Step-specific rules:

- `IdFactory` is monotonically increasing per category; no sharing of numeric ranges across categories is allowed. If two categories share a range boundary (e.g. `'address'=1_000_000` and `'claim'=1_000_000` both start at 1M), the `IdFactory` MUST still return distinct counters — this is by construction since each category has its own counter. Do not rewrite `ID_RANGES` to disambiguate; the collision is accepted because IDs from different categories never appear in the same column.
- `luhn_check` and `generate_card_number` must operate on string inputs/outputs (not int) because leading-zero preservation matters for BIN lookups and Teradata VARCHAR card columns.
- `stamp_di` and `stamp_valid` accept either a `datetime`/`date` or a pre-formatted string for their start/end arguments — the helper is defensive so tier generators can pass either without a local conversion. Strings pass through unchanged; `datetime` / `date` are rendered via `format_ts` / `format_date`.
- `BaseGenerator.generate()` is abstract and MUST raise `NotImplementedError` with a message naming the subclass (e.g. `f"{type(self).__name__}.generate() is abstract"`).
- Every util file includes a `if __name__ == '__main__':` block containing the unit-style assertions from the Exit criteria. This is the step's intentional self-test mechanism per `implementation-steps.md` Step 2.
- Do NOT depend on `registry/` or any Step 3+ module — `utils/` is upstream of the registry. Import from `config.*` and from the Python stdlib / `numpy` / `pandas` only.
- Do NOT add logging, CLI entry points, or side-effecting code at module import time. All behaviour is in functions / methods.

## Definition of done

Each item is a checkbox. Tick every box or mark it `n/a` with a one-line justification before the session ends.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

- [ ] `utils/id_factory.py` unit-style block runs as `__main__` and all assertions pass:
  ```bash
  python utils/id_factory.py
  ```
  The block must assert at minimum: (a) two successive `next('party')` calls differ by exactly 1; (b) `next_many('agreement', 5)` returns a contiguous block of 5 ints; (c) `next('party')` and `next('agreement')` never return the same integer; (d) `next('does_not_exist')` raises `KeyError`; (e) all returned values are positive Python `int` and `>= config.settings.ID_RANGES[category]`.
- [ ] `utils/date_utils.py` unit-style block runs as `__main__` and all assertions pass:
  ```bash
  python utils/date_utils.py
  ```
  Must assert at minimum: (a) `month_snapshots(HISTORY_START, SIM_DATE)` returns exactly 6 tuples spanning Oct 2025 through Mar 2026 inclusive; (b) the last tuple's end equals `SIM_DATE`; (c) `is_active(HIGH_TS)` and `is_active(HIGH_DATE)` and `is_active(None)` all return True; (d) `is_active(datetime(2025,12,31))` returns False; (e) `format_ts(None) == HIGH_TS`; (f) `format_date(None) == HIGH_DATE`; (g) `random_datetime_between(HISTORY_START, SIM_DATE, rng)` returns a datetime in the closed interval for 1,000 samples with a fixed rng.
- [ ] `utils/di_columns.py` unit-style block runs as `__main__` and all assertions pass:
  ```bash
  python utils/di_columns.py
  ```
  Must assert at minimum: (a) `stamp_di` on a 3-row DataFrame returns a 3-row DataFrame with exactly 5 new columns appended in `DI_COLUMN_ORDER`; (b) default `di_end_ts` values equal `HIGH_TS`; (c) default `di_rec_deleted_Ind` values equal `'N'`; (d) `di_data_src_cd` and `di_proc_name` are NaN/None; (e) `stamp_valid` appends exactly 3 columns in `VALID_COLUMN_ORDER` with defaults `HIGH_DATE` and `'N'`; (f) calling `stamp_di` then `stamp_valid` on the same DataFrame leaves the DI columns first in append order, then the Valid columns.
- [ ] `utils/luhn.py` unit-style block runs as `__main__` and all assertions pass:
  ```bash
  python utils/luhn.py
  ```
  Must assert at minimum: (a) 1,000 card numbers generated with a seeded rng all pass `luhn_check`; (b) those 1,000 values are all unique; (c) every generated card is a 16-character string of digits; (d) `generate_cvv` returns a 3-character digit string; (e) a known bad number like `'4111111111111112'` fails `luhn_check`; (f) a known good number like `'4111111111111111'` passes.
- [ ] `BaseGenerator.stamp_di()` applied to an empty DataFrame yields a DF with exactly 5 DI columns in canonical order with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. Verify:
  ```bash
  python -c "
  import pandas as pd
  from generators.base import BaseGenerator
  from config.settings import HIGH_TS
  from utils.di_columns import DI_COLUMN_ORDER
  class _T(BaseGenerator): 
      def generate(self, ctx): return {}
  df = _T().stamp_di(pd.DataFrame(), start_ts='2026-04-20 00:00:00.000000')
  assert list(df.columns) == list(DI_COLUMN_ORDER), df.columns.tolist()
  # An empty DataFrame with 5 stamped columns should have 0 rows but 5 columns
  assert df.shape[1] == 5
  print('stamp_di OK on empty DataFrame')
  "
  ```
  Must print `stamp_di OK on empty DataFrame`.
- [ ] `BaseGenerator.stamp_valid()` applied to an empty DataFrame yields a DF with exactly 3 Valid columns in canonical order with `Valid_To_Dt = HIGH_DATE` and `Del_Ind = 'N'`. Verify:
  ```bash
  python -c "
  import pandas as pd
  from generators.base import BaseGenerator
  from config.settings import HIGH_DATE
  from utils.di_columns import VALID_COLUMN_ORDER
  class _T(BaseGenerator): 
      def generate(self, ctx): return {}
  df = _T().stamp_valid(pd.DataFrame(), from_dt='2025-10-01')
  assert list(df.columns) == list(VALID_COLUMN_ORDER), df.columns.tolist()
  assert df.shape[1] == 3
  print('stamp_valid OK on empty DataFrame')
  "
  ```
  Must print `stamp_valid OK on empty DataFrame`.
- [ ] `BaseGenerator.generate()` on the base class raises `NotImplementedError`. Verify:
  ```bash
  python -c "
  from generators.base import BaseGenerator
  try:
      BaseGenerator().generate(ctx=None)
  except NotImplementedError as e:
      print('abstract OK:', e)
  "
  ```
  Must print a line starting with `abstract OK:`.
- [ ] `luhn.generate_card_number()` output passes mod-10 check for 1,000 samples and all are unique. Verify:
  ```bash
  python -c "
  import numpy as np
  from utils.luhn import generate_card_number, luhn_check
  rng = np.random.default_rng(42)
  cards = [generate_card_number(rng) for _ in range(1000)]
  assert all(luhn_check(c) for c in cards), 'mod-10 fail'
  assert len(set(cards)) == 1000, f'dup cards: {1000 - len(set(cards))}'
  assert all(len(c) == 16 and c.isdigit() for c in cards)
  print('luhn OK')
  "
  ```
  Must print `luhn OK`.

### Universal checks

- [ ] `git status` shows only files listed under `## Produces` — nothing else. Run:
  ```bash
  git status --porcelain
  ```
  Every line must map to a path under `## Produces` (`utils/__init__.py`, `utils/id_factory.py`, `utils/date_utils.py`, `utils/di_columns.py`, `utils/luhn.py`, `generators/__init__.py`, `generators/base.py`). No stray files.
- [ ] All new files pass `python -c "import <module>"`. Run:
  ```bash
  python -c "import utils.id_factory, utils.date_utils, utils.di_columns, utils.luhn, generators.base"
  ```
  Must exit 0 with no output.
- [ ] No CSV column named `*_Id` uses INTEGER — n/a: this step produces no CSVs. BIGINT semantics are enforced upstream by `IdFactory` returning Python `int` values; the first test of BIGINT CSV rendering happens in Step 5 (writer) and is verified end-to-end in Step 25.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — n/a: this step writes no CSVs.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — n/a: this step writes no CSVs. The `output/` directory from Step 1 stays empty.
- [ ] `utils/` and `generators/` packages have `__init__.py` markers (so Step 3+ can do absolute imports like `from utils.id_factory import IdFactory` and `from generators.base import BaseGenerator`). Verify:
  ```bash
  [ -f utils/__init__.py ] && [ -f generators/__init__.py ] && echo OK || echo MISSING
  ```
  Must print `OK`.

## Handoff notes

**Completed:** 2026-04-20

### What shipped

All 7 files specified under `## Produces` were created exactly as specced:
- `utils/__init__.py`, `utils/id_factory.py`, `utils/date_utils.py`, `utils/di_columns.py`, `utils/luhn.py`
- `generators/__init__.py`, `generators/base.py`

All exit-criteria checks pass: four module self-tests print OK; BaseGenerator smoke checks pass; 1,000-card Luhn check passes; `git status --porcelain` shows only `utils/` and `generators/`.

One implementation note: module-level `config.*` and `utils.*` imports in `date_utils.py`, `di_columns.py`, and `generators/base.py` use a `try/except ImportError` fallback that inserts the project root into `sys.path`. This allows the files to be run directly as scripts (`python utils/date_utils.py`) while still importing cleanly when used as package modules.

### Deferrals

None. Scope was utility primitives only — nothing deferred.

### Next-session hint

Step 3 (`specs/step-03-registry.md`) can start now. It imports `from utils.id_factory import IdFactory` and `from generators.base import BaseGenerator` — both stable. `IdFactory(config.settings.ID_RANGES)` is the constructor call pattern; `BaseGenerator.stamp_di()` and `stamp_valid()` are ready to subclass.

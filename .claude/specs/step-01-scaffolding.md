# Spec: Step 01 — Project Scaffolding & Config

## Overview

This step lays the foundational directory tree and configuration layer for the generator, before any registry, generator, or writer code is written. It creates the skeleton described in `mvp-tool-design.md` §3 and hardcodes the simulation parameters from §1 (scale, date window, seed, high-date sentinels) and the cross-cutting constants from §7 (BIGINT ID ranges, shared party-ID space, reserved placeholder IDs) into `config/` modules. The goal is a tree whose imports resolve cleanly so that every downstream step can assume the same parameter universe without re-deriving constants. No tables are generated, no statistical logic runs, no CSVs are written.

## Depends on

None (foundational step).

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md`):
- `PRD.md` §4 (MVP scope — scale, output format, generation scale), §6 (Architecture Overview — libraries), §7 (Key Technical Decisions — BIGINT, shared party-id, DI columns, sentinels, self-employed placeholder, PARTY_INTERRACTION_EVENT typo, GEOSPATIAL skip)
- `mvp-tool-design.md` §1 (Simulation Parameters table), §3 (Folder Structure — authoritative tree), §7 (BaseGenerator sentinels — HIGH_TS / HIGH_DATE), §8 (ID Factory ranges), §15 (main.py orchestration skeleton)
- `implementation-steps.md` Step 1 entry

**Additional reference files** (only those named in the step's "Reads from" line):
- None. Step 1 does not depend on any `references/` file — the design doc already distills the scale and sentinel values that belong in config.

## Produces

Directory skeleton and config modules. All paths relative to the project root.

**Directory tree** (empty directories are permissible at this stage; downstream steps populate them):
- `config/` — configuration modules (see files below)
- `seed_data/` — empty; populated in Steps 6–8
- `registry/` — empty; populated in Steps 3–4
- `generators/` — empty; populated in Steps 8–23
- `utils/` — empty; populated in Step 2
- `output/` — empty; populated in Step 5 (writer) and at runtime (CSV output subdirs `Core_DB/`, `CDM_DB/`, `PIM_DB/`)
- `specs/` — already exists in repo; no change
- `references/` — already exists in repo; no change

**Files** (each an absolute path under the project root):

- `config/__init__.py` — empty marker file so `config` is importable as a package.
- `config/settings.py` — scale, cohort split, date window, seed, high-date sentinels, reserved IDs, output paths. All constants mirror `mvp-tool-design.md` §1 and PRD §7. Must include at minimum:
  - `SEED = 42`
  - `TARGET_CUSTOMERS = 3_000`
  - `TARGET_AGREEMENTS = 5_000`
  - `INDIVIDUAL_PCT = 0.80`, `ORGANIZATION_PCT = 0.20`
  - Cohort split: `COHORT_ACTIVE_PCT = 0.55`, `COHORT_DECLINING_PCT = 0.30`, `COHORT_CHURNED_PCT = 0.05`, `COHORT_NEW_PCT = 0.10`
  - `CHECKING_PENETRATION_PCT = 0.90`
  - `HISTORY_START = date(2025, 10, 1)`, `SIM_DATE = date(2026, 3, 31)`
  - `HIGH_DATE = '9999-12-31'`, `HIGH_TS = '9999-12-31 00:00:00.000000'`
  - `BANK_PARTY_ID = 9_999_999` (used in PARTY_RELATED 'customer of enterprise' rows)
  - `SELF_EMP_ORG_ID = 9_999_999` (reserved ORGANIZATION row for self-employed individuals)
  - `OUTPUT_DIR = Path('output')` with subdir constants for `Core_DB`, `CDM_DB`, `PIM_DB`
  - `ID_RANGES = {...}` — the BIGINT starting offsets per entity type exactly as `mvp-tool-design.md` §8
  - `SKIPPED_TABLES = {'Core_DB.GEOSPATIAL'}` — one authoritative place for the skip list

- `config/code_values.py` — constrained code strings that multiple tiers reference verbatim. At minimum:
  - `PARTY_AGREEMENT_ROLE_CODES = {'customer', 'borrower', 'guarantor', 'co-borrower', 'owner'}`
  - `PARTY_RELATED_ROLE_CODES = {'customer of enterprise', 'prospect of enterprise', 'employee of enterprise'}`
  - `AGREEMENT_STATUS_SCHEMES = ('Account Status', 'Accrual Status', 'Default Status', 'Drawn Undrawn Status', 'Frozen Status', 'Past Due Status')`
  - `AGREEMENT_FEATURE_ROLE_CODES = ('primary', 'fee', 'rate', 'term')`
  - `CURRENCY_USE_CODES = ('preferred', 'secondary', 'home')`
  - `FROZEN_STATUS_ROW = {'Agreement_Status_Scheme_Cd': 'Frozen Status', 'Agreement_Status_Cd': 'FROZEN', 'Agreement_Status_Desc': 'Frozen'}` — the literal-match row Layer 2 needs
  - `LANGUAGE_USAGE_TYPES = ('primary spoken language', 'primary written language')`
  - `ORG_NAME_TYPES = ('brand name', 'business name', 'legal name', 'registered name')`
  - `PROFITABILITY_MODEL_TYPE_CD = 'profitability'`
  - `CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD = 'customer profitability'`
  - `RATE_FEATURE_SUBTYPE_CD = 'Rate Feature'`
  - `ORIGINAL_LOAN_TERM_CLASSIFICATION_CD = 'Original Loan Term'`
  - `TERRITORY_ISO_STANDARD_CD = 'ISO 3166-2 Country Subdivision Standard'`

- `config/distributions.py` — sampler *stubs* only (function signatures, docstrings, `raise NotImplementedError`). Real sampling implementations are delivered in Step 4. Stubs declared for signatures named in `implementation-steps.md` Step 4 "Statistical samplers fleshed out" list: `sample_age`, `sample_income_quartile`, `sample_fico`, `sample_deposit_balance`, `sample_cc_balance`, `sample_mortgage_rate`, `sample_annual_income`, `sample_ethnicity`, `sample_gender`, `sample_marital`, `sample_occupation`, `sample_kids`, `sample_lifecl`. Each takes `rng: np.random.Generator` and relevant conditioning args and returns the type indicated in `mvp-tool-design.md` §10.

- `requirements.txt` — pinned to the library list in `mvp-tool-design.md` §13:
  ```
  numpy>=1.26
  pandas>=2.0
  faker>=24.0
  scipy>=1.12
  python-dateutil
  ```

- `main.py` — orchestrator stub exactly matching the shape in `mvp-tool-design.md` §15, with TODO markers for each phase. The stub should import from `config.settings`, print the seed/scale on startup, and `pass` through the four phases (Universe Build, Tiered Writing, Validation, CSV Write) without doing any real work. Each phase is a clearly labeled TODO block referencing the step number that will implement it.

## Tables generated (if applicable)

No tables generated in this step. Scaffolding only.

## Files to modify

No files modified. All files are new. `references/`, `specs/`, `resources/`, `CLAUDE.md`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md` are NOT touched.

## New dependencies

All listed in the new `requirements.txt` (no prior `requirements.txt` exists):

- `numpy>=1.26`
- `pandas>=2.0`
- `faker>=24.0`
- `scipy>=1.12`
- `python-dateutil`

No `setup.py` / `pyproject.toml` is created at this step — `requirements.txt` is sufficient for the MVP.

## Rules for implementation

- BIGINT for all ID columns (per PRD §7.1) — never INTEGER, even when the DDL says INTEGER. This step does not generate IDs, but `ID_RANGES` in `settings.py` must use integer offsets ≥ 1 that will produce BIGINT values when combined with sequential counters.
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — `BANK_PARTY_ID` and `SELF_EMP_ORG_ID` must both be `9_999_999` (single reserved ID usable in both schemas — see PRD §7.12 and §7.11 resolution, `mvp-tool-design.md` §10 rule 7).
- DI column stamping on every table via `BaseGenerator.stamp_di()` — no table objects here, but `HIGH_TS` and `HIGH_DATE` constants must be defined in `settings.py` for Step 2 to consume.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records — define `HIGH_TS` and `HIGH_DATE` exactly as these string literals.
- CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` (per PRD §7.3) — scaffold documents this rule; actual stamping logic lives in Step 2.
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` — n/a at this step (no DataFrames produced); enforced in Steps 5/8 onward.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — add a constant `PARTY_INTERRACTION_EVENT_TABLE_NAME = 'PARTY_INTERRACTION_EVENT'` in `settings.py` so Step 22 has a single source of truth and cannot silently "correct" the spelling.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — `SKIPPED_TABLES = {'Core_DB.GEOSPATIAL'}` is authoritative; Step 5 and Step 15 will consult it.
- No ORMs, no database connections — pure pandas → CSV. Scaffold does not add SQLAlchemy, psycopg, teradatasql, etc. to `requirements.txt`.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42`. `settings.SEED = 42` must be an `int` literal, not an env-var read, to guarantee byte-identical runs for the Step 25 reproducibility check.

Step-specific rules:

- No runtime logic beyond constant definitions and docstrings. `main.py` is a stub; it does not import pandas, numpy, or faker (imports are lazy or absent until Step 2+).
- `config/distributions.py` functions raise `NotImplementedError` with a message pointing to Step 4. Do not write partial sampling logic here even if tempting.
- `settings.py` constants are immutable for the life of the project except where the design doc explicitly marks them configurable (SEED, scale params). Do not put environment-variable overrides in Step 1 — that complicates the reproducibility guarantee.
- `BANK_PARTY_ID` and `SELF_EMP_ORG_ID` must be outside every `ID_RANGES` bucket (9,999,999 is well above all starting offsets) so no real party can ever collide with the reserved IDs.
- Use absolute imports in `config/` (`from config.settings import ...`), not relative, so the package is usable from the project root without path tricks.

## Definition of done

Each item is a checkbox. Tick every box or mark it `n/a` with a one-line justification before the session ends.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

- [ ] `python -c "import config.settings, config.code_values, config.distributions"` exits 0 (run from the project root).
- [ ] Folder tree matches `mvp-tool-design.md` §3 exactly. Verify with:
  ```bash
  for d in config seed_data registry generators utils output; do
    [ -d "$d" ] && echo "OK: $d" || echo "MISSING: $d"
  done
  ```
  Every line must print `OK:`.
- [ ] All constants from `mvp-tool-design.md` §1 are present in `config/settings.py`. Verify with:
  ```bash
  python -c "
  import config.settings as s
  assert s.SEED == 42
  assert s.TARGET_CUSTOMERS == 3000
  assert s.TARGET_AGREEMENTS == 5000
  assert abs(s.INDIVIDUAL_PCT - 0.80) < 1e-9
  assert abs(s.ORGANIZATION_PCT - 0.20) < 1e-9
  assert abs(s.COHORT_ACTIVE_PCT - 0.55) < 1e-9
  assert abs(s.COHORT_DECLINING_PCT - 0.30) < 1e-9
  assert abs(s.COHORT_CHURNED_PCT - 0.05) < 1e-9
  assert abs(s.COHORT_NEW_PCT - 0.10) < 1e-9
  assert abs(s.CHECKING_PENETRATION_PCT - 0.90) < 1e-9
  assert str(s.HISTORY_START) == '2025-10-01'
  assert str(s.SIM_DATE) == '2026-03-31'
  assert s.HIGH_DATE == '9999-12-31'
  assert s.HIGH_TS == '9999-12-31 00:00:00.000000'
  print('settings OK')
  "
  ```
  Must print `settings OK`.
- [ ] All constants from `mvp-tool-design.md` §7 / §8 are present. Verify with:
  ```bash
  python -c "
  import config.settings as s
  assert s.BANK_PARTY_ID == 9999999
  assert s.SELF_EMP_ORG_ID == 9999999
  assert 'Core_DB.GEOSPATIAL' in s.SKIPPED_TABLES
  for key in ('party','agreement','event','address','locator','feature','product','campaign','promotion','model','claim','household','task','activity','contact','card','market_seg','channel','pim_id','group_id'):
      assert key in s.ID_RANGES, key
  assert s.PARTY_INTERRACTION_EVENT_TABLE_NAME == 'PARTY_INTERRACTION_EVENT'
  print('constants OK')
  "
  ```
  Must print `constants OK`.
- [ ] `config/code_values.py` defines every constrained code set and literal referenced in `mvp-tool-design.md` §9 (tier constraints) and `references/02_data-mapping-reference.md` Step 3. Verify with:
  ```bash
  python -c "
  import config.code_values as c
  assert 'customer' in c.PARTY_AGREEMENT_ROLE_CODES
  assert 'borrower' in c.PARTY_AGREEMENT_ROLE_CODES
  assert 'customer of enterprise' in c.PARTY_RELATED_ROLE_CODES
  assert 'prospect of enterprise' in c.PARTY_RELATED_ROLE_CODES
  assert 'employee of enterprise' in c.PARTY_RELATED_ROLE_CODES
  assert len(c.AGREEMENT_STATUS_SCHEMES) == 6
  assert set(c.AGREEMENT_FEATURE_ROLE_CODES) == {'primary','fee','rate','term'}
  assert 'preferred' in c.CURRENCY_USE_CODES
  assert c.FROZEN_STATUS_ROW['Agreement_Status_Cd'] == 'FROZEN'
  assert c.FROZEN_STATUS_ROW['Agreement_Status_Desc'] == 'Frozen'
  assert set(c.LANGUAGE_USAGE_TYPES) == {'primary spoken language','primary written language'}
  assert set(c.ORG_NAME_TYPES) == {'brand name','business name','legal name','registered name'}
  assert c.PROFITABILITY_MODEL_TYPE_CD == 'profitability'
  assert c.CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD == 'customer profitability'
  assert c.RATE_FEATURE_SUBTYPE_CD == 'Rate Feature'
  assert c.ORIGINAL_LOAN_TERM_CLASSIFICATION_CD == 'Original Loan Term'
  assert c.TERRITORY_ISO_STANDARD_CD == 'ISO 3166-2 Country Subdivision Standard'
  print('code_values OK')
  "
  ```
  Must print `code_values OK`.
- [ ] `config/distributions.py` declares every sampler stub named in `implementation-steps.md` Step 4 and each raises `NotImplementedError`. Verify with:
  ```bash
  python -c "
  import inspect
  import numpy as np
  import config.distributions as d
  rng = np.random.default_rng(0)
  for name in ('sample_age','sample_income_quartile','sample_fico','sample_deposit_balance','sample_cc_balance','sample_mortgage_rate','sample_annual_income','sample_ethnicity','sample_gender','sample_marital','sample_occupation','sample_kids','sample_lifecl'):
      fn = getattr(d, name)
      assert callable(fn), name
      sig = inspect.signature(fn)
      assert 'rng' in sig.parameters, name
  # spot-check NotImplementedError
  try:
      d.sample_age(rng=rng, n=1)
  except NotImplementedError:
      pass
  else:
      raise AssertionError('sample_age did not raise NotImplementedError')
  print('distributions OK')
  "
  ```
  Must print `distributions OK`.
- [ ] `requirements.txt` contains exactly the five library lines from `mvp-tool-design.md` §13 (order flexible, comments allowed). Verify with:
  ```bash
  python -c "
  import re
  lines = [l.strip() for l in open('requirements.txt') if l.strip() and not l.strip().startswith('#')]
  pkgs = {re.split(r'[<>=!~]', l)[0].strip().lower() for l in lines}
  assert pkgs >= {'numpy','pandas','faker','scipy','python-dateutil'}, pkgs
  print('requirements OK')
  "
  ```
  Must print `requirements OK`.
- [ ] `python main.py` exits 0 and prints the seed and scale summary without attempting to import pandas/numpy/faker (verifies stub-only nature).

### Universal checks

- [ ] `git status` shows only files listed under ## Produces — nothing else. Run:
  ```bash
  git status --porcelain
  ```
  Every line must map to a path under `## Produces` (new `config/` files, empty placeholder dirs, `requirements.txt`, `main.py`). No stray files in other directories.
- [ ] All new files pass `python -c "import <module>"` where applicable (`config.settings`, `config.code_values`, `config.distributions`). Covered by the first check above.
- [ ] No CSV column named `*_Id` uses INTEGER — n/a: this step produces no CSVs.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — n/a: no CSV output at this step. Constant `PARTY_INTERRACTION_EVENT_TABLE_NAME` is defined and verified above for Step 22 consumption.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — n/a: `output/` is an empty scaffold at this step; no CSV files written. `SKIPPED_TABLES` constant verified above.
- [ ] Empty-package markers exist where Python import will need them. Verify:
  ```bash
  [ -f config/__init__.py ] && echo OK || echo MISSING
  ```
  Only `config/` strictly needs an `__init__.py` at this step (it's the only package imported by Step 1 checks). Other directories (`seed_data`, `registry`, etc.) may receive `__init__.py` in their respective steps — fine to add them here if you prefer, but not required.

## Handoff notes

**Completed:** 2026-04-20

### What shipped
All files and directories specified under `## Produces` were created exactly as specced:
- `config/__init__.py`, `config/settings.py`, `config/code_values.py`, `config/distributions.py`
- `requirements.txt`, `main.py`
- Empty placeholder dirs: `seed_data/`, `registry/`, `generators/`, `utils/`, `output/`

All 9 exit-criteria checks pass (import, directory tree, settings, constants, code_values, distributions, requirements, main.py smoke, git status clean).

### Deferrals
None. Scope was scaffolding only — nothing deferred.

### Next-session hint
Step 2 (`specs/step-02-utils.md`) can start now. It reads `config.settings` (stable) and produces `utils/id_factory.py`, `utils/date_utils.py`, `utils/di_columns.py`, `utils/luhn.py`, and `generators/base.py`. The `ID_RANGES` dict in `settings.py` and the `HIGH_TS`/`HIGH_DATE` constants are the primary inputs Step 2 consumes.

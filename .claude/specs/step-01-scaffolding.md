# Spec: Step 01 — Project Scaffolding & Config

## Overview

This is the foundational step that lays down the directory skeleton and the
configuration surface for the entire generator. It creates every top-level
package (`config/`, `seed_data/`, `registry/`, `generators/`, `utils/`,
`output/`) exactly as listed in `mvp-tool-design.md` §3, wires in the three
config modules (`settings.py`, `code_values.py`, `distributions.py`) that
every later tier will import, declares the pinned library set in
`requirements.txt`, and stands up a stub `main.py` orchestrator with
TODO markers for the four pipeline phases (Universe Build → Tiered Writing →
Validation → CSV Write) defined in `mvp-tool-design.md` §2 and §15. No
generator logic is written here — subsequent steps (3 onwards) fill in the
modules. The goal is a clean, importable skeleton that reflects every scale
parameter, date sentinel, reserved ID, and constrained code value called
out in PRD §4/§7 and design §1/§10.

## Depends on

None (foundational step).

## Reads from (source documents)
**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff
  Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to:**
- `PRD.md` §4 (MVP Scope — in-scope layers, output format, generation scale)
- `PRD.md` §6 (Architecture Overview — 4 phases, tier list)
- `PRD.md` §7 (Key Technical Decisions — 7.1 BIGINT, 7.2 shared party id,
  7.3 DI columns, 7.5 exclusive sub-typing, 7.6 tier order, 7.9 GEOSPATIAL
  skip, 7.10 INTERRACTION typo, 7.11 seed data, 7.12 self-emp placeholder)
- `mvp-tool-design.md` §1 (Simulation Parameters table — scale, cohorts,
  dates, seed)
- `mvp-tool-design.md` §3 (Folder Structure — authoritative directory tree)
- `mvp-tool-design.md` §7 (BaseGenerator and DI Columns — sentinel values)
- `mvp-tool-design.md` §13 (Libraries — pinned versions)
- `mvp-tool-design.md` §15 (main.py Orchestration — stub shape)
- `implementation-steps.md` Step 1 (Exit criteria; foundational step
  reading discipline)

## Produces

All paths are relative to the project root
(`.../Synthetic_Data_Gen/`).

**Project root:**
- `requirements.txt` — pinned dependencies: `numpy>=1.26`, `pandas>=2.0`,
  `faker>=24.0`, `scipy>=1.12`, `python-dateutil`
- `main.py` — stub orchestrator with phase-marker TODOs (imports resolve,
  `python main.py` prints a placeholder and exits 0; no real work done)

**`config/`:**
- `config/__init__.py` — empty package marker
- `config/settings.py` — scale params, cohort splits, date window,
  high-date sentinels, `SEED = 42`, `BANK_PARTY_ID = 9999999`,
  `SELF_EMP_ORG_ID = 9999999`, and computed output directory paths
  (`OUTPUT_DIR`, `CORE_DB_DIR`, `CDM_DB_DIR`, `PIM_DB_DIR`)
- `config/code_values.py` — constrained code-value constants used across
  tiers (role codes, scheme names, currency use, feature subtypes, language
  usage types, model type/purpose, org name types, frozen status literals,
  agreement-status scheme list, territory standard, locator usage)
- `config/distributions.py` — sampler function signatures only
  (`sample_age`, `sample_income_quartile`, `sample_fico`,
  `sample_deposit_balance`, `sample_cc_balance`, `sample_mortgage_rate`,
  `sample_annual_income`, `sample_ethnicity`, `sample_gender`,
  `sample_marital`, `sample_occupation`, `sample_kids`, `sample_lifecl`) —
  each raises `NotImplementedError` to be filled in Step 4

**`seed_data/`:**
- `seed_data/__init__.py` — empty package marker (per-domain modules added
  in Steps 6–9)

**`registry/`:**
- `registry/__init__.py` — empty package marker (profiles + context come in
  Step 3)

**`generators/`:**
- `generators/__init__.py` — empty package marker (base.py + tiers come in
  Step 2 onwards)

**`utils/`:**
- `utils/__init__.py` — empty package marker (id_factory, date_utils,
  di_columns, luhn come in Step 2)

**`output/`:**
- `output/__init__.py` — empty package marker (writer.py + validator.py
  come in Steps 5 and 24)
- `output/Core_DB/.gitkeep` — empty file so the output tree exists
- `output/CDM_DB/.gitkeep` — empty file so the output tree exists
- `output/PIM_DB/.gitkeep` — empty file so the output tree exists

**Project root:**
- `.gitignore` — ignore generated CSVs under `output/Core_DB/*.csv`,
  `output/CDM_DB/*.csv`, `output/PIM_DB/*.csv`, plus `__pycache__/`,
  `*.pyc`, `.venv/`

## Tables generated (if applicable)

No tables generated in this step — scaffolding only.

## Files to modify

No files modified. This step only creates new files.

> Note: The pre-existing planning documents (`PRD.md`, `mvp-tool-design.md`,
> `implementation-steps.md`, `CLAUDE.md`, the `references/` folder, and the
> `resources/` folder) are **not** touched by this step.

## New dependencies

All dependencies are first introduced in this step via `requirements.txt`:

```
numpy>=1.26
pandas>=2.0
faker>=24.0
scipy>=1.12
python-dateutil
```

No other runtime or dev dependencies are added at this step.

## Rules for implementation

Project-wide non-negotiables (mostly dormant at this step but must be
honoured by constants/sentinels defined here):

- BIGINT for all ID columns (per PRD §7.1) — never INTEGER, even when the
  DDL says INTEGER. At this step, this is expressed by constants typed as
  plain Python `int` (Python ints are arbitrary precision, so no coercion
  is needed; later steps must persist them as BIGINT in DataFrames/CSVs).
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2). At this
  step: `BANK_PARTY_ID` and `SELF_EMP_ORG_ID` live in `config/settings.py`
  and are both `9999999` — a single integer universe shared across schemas.
- DI column stamping on every table via `BaseGenerator.stamp_di()` — the
  stamping helper itself comes in Step 2; this step only defines the
  sentinels (`HIGH_TS`, `HIGH_DATE`) in `config/settings.py`.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'`
  for active records — defined as `HIGH_TS` and `HIGH_DATE` string
  constants in `config/settings.py`.
- CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`,
  `Del_Ind` (per PRD §7.3) — `Del_Ind` active sentinel is `'N'` (defined in
  `config/code_values.py` or `config/settings.py` as `DEL_IND_ACTIVE = 'N'`).
- Column order in every DataFrame matches the DDL declaration order in
  `references/07_mvp-schema-reference.md` — enforced downstream; no action
  at this step.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10).
  No CSVs are written at this step, but the code-values module must NOT
  silently "correct" any related constant.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9). No action at this
  step — enforced by the Tier 5 generator later.
- No ORMs, no database connections — pure pandas → CSV. Enforced by
  `requirements.txt` (only numpy/pandas/faker/scipy/python-dateutil).
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded
  from `config.settings.SEED = 42`. At this step: `SEED = 42` is declared
  in `config/settings.py`.

Step-specific rules:

- **No runtime logic beyond constants and stubs.** `config/distributions.py`
  functions raise `NotImplementedError("filled in Step 4")` with the
  correct signatures per design §10.
- **No placeholder secrets or credentials.** This tool has none; don't
  invent any.
- **`main.py` is a stub** — it prints a single-line placeholder
  (e.g. `"CIF Synthetic Data Generator — scaffolding only (Step 1)"`) and
  exits 0. It does NOT instantiate `UniverseBuilder`, tiers, writer, or
  validator. It DOES contain TODO comments for each of Phase 1–4 per
  design §15.
- **Constants must match the design doc exactly.**
  - `SEED = 42`
  - `TARGET_CUSTOMERS = 3000`
  - `TARGET_AGREEMENTS = 5000`
  - `INDIVIDUAL_PCT = 0.80`, `ORGANIZATION_PCT = 0.20`
  - `HISTORY_START = date(2025, 10, 1)`
  - `SIM_DATE = date(2026, 3, 31)`
  - `HIGH_TS = '9999-12-31 00:00:00.000000'`
  - `HIGH_DATE = '9999-12-31'`
  - Cohort splits: `ACTIVE=0.55`, `DECLINING=0.30`, `CHURNED=0.05`,
    `NEW=0.10` (expressed as a `COHORT_SPLIT` dict)
  - `CHECKING_PENETRATION = 0.90`
  - `BANK_PARTY_ID = 9999999`, `SELF_EMP_ORG_ID = 9999999`
- **Literal-match code values in `config/code_values.py` must be exact
  strings** — Layer 2 rules match these literally:
  - `PARTY_RELATED_ROLE_CUSTOMER = 'customer of enterprise'`
  - `PARTY_RELATED_ROLE_PROSPECT = 'prospect of enterprise'`
  - `PARTY_RELATED_ROLE_EMPLOYEE = 'employee of enterprise'`
  - `PARTY_AGREEMENT_ROLE_CUSTOMER = 'customer'`
  - `PARTY_AGREEMENT_ROLE_BORROWER = 'borrower'`
  - `AGREEMENT_PRODUCT_ROLE_PRIMARY = 'primary'`
  - `CURRENCY_USE_PREFERRED = 'preferred'`
  - `AGREEMENT_STATUS_SCHEMES = ('Account Status', 'Accrual Status',
    'Default Status', 'Drawn Undrawn Status', 'Frozen Status',
    'Past Due Status')`
  - `FROZEN_STATUS_CD = 'FROZEN'`, `FROZEN_STATUS_DESC = 'Frozen'`,
    `FROZEN_SCHEME = 'Frozen Status'`
  - `AGREEMENT_FEATURE_ROLES = ('primary', 'fee', 'rate', 'term')`
  - `RATE_FEATURE_SUBTYPE = 'Rate Feature'`
  - `ORIGINAL_LOAN_TERM_CLASSIFICATION = 'Original Loan Term'`
  - `ORG_NAME_TYPES = ('brand name', 'business name', 'legal name',
    'registered name')`
  - `LANGUAGE_USAGE_SPOKEN = 'primary spoken language'`
  - `LANGUAGE_USAGE_WRITTEN = 'primary written language'`
  - `MODEL_TYPE_PROFITABILITY = 'profitability'`
  - `MODEL_PURPOSE_CUSTOMER_PROFITABILITY = 'customer profitability'`
  - `LOCATOR_USAGE_PRIMARY = 'physical_primary'`
  - `TERRITORY_STANDARD_ISO_SUBDIV =
    'ISO 3166-2 Country Subdivision Standard'`
- **Output directories must exist** after this step runs (with `.gitkeep`
  markers) so later steps can write into them without a `mkdir` race.
- **Encoding + line endings**: all source files UTF-8, LF line endings
  (even on Windows). Do not rely on the shell to create empty files — use
  the `Write` tool.

## Definition of done

Tick every box before committing. Every item below must be either ✅
verified with the given command (when supplied) or explicitly marked
`n/a` with a one-line reason.

### Verbatim exit criteria from `implementation-steps.md` Step 1

- [ ] `python -c "import config.settings, config.code_values,
      config.distributions"` exits 0
- [ ] Folder tree matches `mvp-tool-design.md` §3 exactly for the
      directories introduced at this step (`config/`, `seed_data/`,
      `registry/`, `generators/`, `utils/`, `output/`, plus `output/Core_DB/`,
      `output/CDM_DB/`, `output/PIM_DB/`)
- [ ] All constants from `mvp-tool-design.md` §1 and PRD §7 are
      represented with the correct values (verify with:
      `python -c "from config.settings import *;
      assert SEED == 42;
      assert TARGET_CUSTOMERS == 3000;
      assert TARGET_AGREEMENTS == 5000;
      assert INDIVIDUAL_PCT == 0.80 and ORGANIZATION_PCT == 0.20;
      assert str(HISTORY_START) == '2025-10-01';
      assert str(SIM_DATE) == '2026-03-31';
      assert HIGH_TS == '9999-12-31 00:00:00.000000';
      assert HIGH_DATE == '9999-12-31';
      assert BANK_PARTY_ID == 9999999 and SELF_EMP_ORG_ID == 9999999;
      assert CHECKING_PENETRATION == 0.90;
      assert abs(sum(COHORT_SPLIT.values()) - 1.0) < 1e-9;
      assert COHORT_SPLIT['ACTIVE'] == 0.55;
      assert COHORT_SPLIT['DECLINING'] == 0.30;
      assert COHORT_SPLIT['CHURNED'] == 0.05;
      assert COHORT_SPLIT['NEW'] == 0.10;
      print('settings OK')"`)

### Step-specific checks

- [ ] `config/code_values.py` contains every literal-match constant listed
      in the Rules section above (verify with:
      `python -c "from config.code_values import
      PARTY_RELATED_ROLE_CUSTOMER, PARTY_AGREEMENT_ROLE_CUSTOMER,
      AGREEMENT_PRODUCT_ROLE_PRIMARY, CURRENCY_USE_PREFERRED,
      AGREEMENT_STATUS_SCHEMES, FROZEN_STATUS_CD, FROZEN_STATUS_DESC,
      AGREEMENT_FEATURE_ROLES, RATE_FEATURE_SUBTYPE,
      ORIGINAL_LOAN_TERM_CLASSIFICATION, ORG_NAME_TYPES,
      LANGUAGE_USAGE_SPOKEN, LANGUAGE_USAGE_WRITTEN,
      MODEL_TYPE_PROFITABILITY, MODEL_PURPOSE_CUSTOMER_PROFITABILITY,
      TERRITORY_STANDARD_ISO_SUBDIV;
      assert PARTY_RELATED_ROLE_CUSTOMER == 'customer of enterprise';
      assert AGREEMENT_PRODUCT_ROLE_PRIMARY == 'primary';
      assert CURRENCY_USE_PREFERRED == 'preferred';
      assert set(AGREEMENT_STATUS_SCHEMES) == {'Account Status',
        'Accrual Status', 'Default Status', 'Drawn Undrawn Status',
        'Frozen Status', 'Past Due Status'};
      assert FROZEN_STATUS_CD == 'FROZEN' and FROZEN_STATUS_DESC == 'Frozen';
      assert set(AGREEMENT_FEATURE_ROLES) ==
        {'primary', 'fee', 'rate', 'term'};
      assert RATE_FEATURE_SUBTYPE == 'Rate Feature';
      assert ORIGINAL_LOAN_TERM_CLASSIFICATION == 'Original Loan Term';
      assert set(ORG_NAME_TYPES) == {'brand name', 'business name',
        'legal name', 'registered name'};
      assert MODEL_TYPE_PROFITABILITY == 'profitability';
      assert MODEL_PURPOSE_CUSTOMER_PROFITABILITY == 'customer profitability';
      assert LANGUAGE_USAGE_SPOKEN == 'primary spoken language';
      assert LANGUAGE_USAGE_WRITTEN == 'primary written language';
      assert TERRITORY_STANDARD_ISO_SUBDIV ==
        'ISO 3166-2 Country Subdivision Standard';
      print('code_values OK')"`)
- [ ] `config/distributions.py` exposes every sampler signature listed in
      the Rules section and each raises `NotImplementedError` when called
      (verify with:
      `python -c "import config.distributions as d, inspect;
      names = ['sample_age','sample_income_quartile','sample_fico',
        'sample_deposit_balance','sample_cc_balance','sample_mortgage_rate',
        'sample_annual_income','sample_ethnicity','sample_gender',
        'sample_marital','sample_occupation','sample_kids','sample_lifecl'];
      missing = [n for n in names if not callable(getattr(d, n, None))];
      assert not missing, f'missing samplers: {missing}';
      try: d.sample_age(1, None)
      except NotImplementedError: print('distributions OK')
      else: raise SystemExit('sample_age did not raise NotImplementedError')"`)
- [ ] `python main.py` exits 0 and prints a single-line placeholder
      (verify with: `python main.py && echo RC=$?`)
- [ ] `requirements.txt` pins exactly the five libraries listed in
      `mvp-tool-design.md` §13 (verify with:
      `python -c "lines = [l.strip() for l in
      open('requirements.txt').readlines() if l.strip() and not
      l.strip().startswith('#')];
      pkgs = sorted(l.split('>=')[0].split('==')[0].split('~=')[0]
        for l in lines);
      assert pkgs == sorted(['faker','numpy','pandas','python-dateutil',
        'scipy']), f'unexpected deps: {pkgs}';
      print('requirements OK')"`)
- [ ] Every package directory has an `__init__.py` file (verify with:
      `python -c "import os; dirs = ['config','seed_data','registry',
      'generators','utils','output']; missing = [d for d in dirs if not
      os.path.isfile(os.path.join(d, '__init__.py'))];
      assert not missing, f'missing __init__.py in: {missing}';
      print('packages OK')"`)
- [ ] Output subdirectories exist and contain a `.gitkeep` (verify with:
      `python -c "import os;
      subs = ['output/Core_DB','output/CDM_DB','output/PIM_DB'];
      missing = [s for s in subs if not
      os.path.isfile(os.path.join(s, '.gitkeep'))];
      assert not missing, f'missing gitkeep in: {missing}';
      print('output tree OK')"`)
- [ ] `.gitignore` ignores generated CSVs and Python cache files (verify
      with: `grep -q "output/Core_DB/\*.csv" .gitignore &&
      grep -q "__pycache__" .gitignore && echo gitignore OK`)

### Universal checks

- [ ] `git status` shows only files listed under ## Produces — nothing
      else (note: `.gitkeep` files in `output/Core_DB/`, `output/CDM_DB/`,
      `output/PIM_DB/` are tracked; *.csv paths in those dirs are ignored)
- [ ] All new Python modules import cleanly:
      `python -c "import config.settings, config.code_values,
      config.distributions; import main"` exits 0
- [ ] No CSV column named `*_Id` uses INTEGER — **n/a**: this step
      produces no CSVs (scaffolding only).
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the
      double-R typo — **n/a**: this step produces no CSVs.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` —
      verify with: `! [ -f output/Core_DB/GEOSPATIAL.csv ] &&
      echo 'no GEOSPATIAL.csv OK'` (directory exists with only `.gitkeep`
      at this step; check is still runnable and passes trivially)

## Handoff notes

_(to be filled in by the implementation session per `implementation-steps.md`
Handoff Protocol)_

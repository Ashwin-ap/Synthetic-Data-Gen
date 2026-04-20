# Spec: Step 06 — Tier 0a Seed Data — Agreement / Financial / Feature Domains

## Overview

This step authors the **first slice of Tier 0 seed data** — the handwritten Python dict literals that populate lookup / reference tables for the `AGREEMENT`, `FINANCIAL`, `STATUS`, and `FEATURE` domains. These tables are *not* randomly generated (see `PRD.md` §7.11 Decision 11 and `mvp-tool-design.md` §14 Decision 2): Layer 2 transformation rules literally match against specific code values (e.g. `Agreement_Status_Cd = 'FROZEN'` drives `Frozen_Ind = '1'`, `Feature_Subtype_Cd = 'Rate Feature'` drives `LOAN_ACCOUNT_BB` rate pivots), so randomising them guarantees Layer 2 failures. This step ships four `seed_data/*.py` modules, each exposing a `get_<domain>_tables() -> Dict[str, pd.DataFrame]` function returning un-stamped DataFrames keyed by `'Core_DB.<TABLE>'`. No DI column stamping is done here — that responsibility lives in Step 8's `Tier0Lookups` generator, which will consume these modules alongside those from Steps 7 and 8. Steps 6, 7, and 8 are independent (per `implementation-steps.md` Dependency Graph) and may run in parallel.

## Depends on

- **Step 1** — consumes from `config/settings.py`:
  - `HIGH_DATE`, `HIGH_TS` — only if any seed row has a `_Start_Dt` / `_Start_Dttm` column the DDL requires (most `*_TYPE` tables are pure code→desc lookups with no lifecycle dates). Not expected to be used in this step, but available if a DDL row demands it.
  - Consumes from `config/code_values.py`:
    - `FROZEN_STATUS_ROW` — the `{'Agreement_Status_Scheme_Cd': 'Frozen Status', 'Agreement_Status_Cd': 'FROZEN', 'Agreement_Status_Desc': 'Frozen'}` literal; `status_types.py` must embed exactly this row verbatim.
    - `AGREEMENT_STATUS_SCHEMES` — 6-tuple of scheme names; `status_types.py` must seed `AGREEMENT_STATUS_SCHEME_TYPE` and `AGREEMENT_STATUS_TYPE` with rows covering every scheme.
    - `AGREEMENT_FEATURE_ROLE_CODES` — 4-tuple (`'primary'`, `'fee'`, `'rate'`, `'term'`); `agreement_types.py` must seed `AGREEMENT_FEATURE_ROLE_TYPE` with all four.
    - `RATE_FEATURE_SUBTYPE_CD` — `'Rate Feature'`; `feature_types.py` must include this as a `FEATURE_SUBTYPE.Feature_Subtype_Cd` value (the underlying `FEATURE` row is created in Step 10).
    - `ORIGINAL_LOAN_TERM_CLASSIFICATION_CD` — `'Original Loan Term'`; `feature_types.py` must include this as a `FEATURE_CLASSIFICATION_TYPE.Feature_Classification_Cd` value.

No code from Step 2, 3, 4, or 5 is imported by this step — the seed modules are pure data with a thin pandas DataFrame wrapper. The tables they produce are consumed by Step 8's `Tier0Lookups.generate(ctx)` via the `get_<domain>_tables()` contract.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and **Seed Data Authoring Convention** apply to every seed step — Step 6 is the first instance)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 6 + the Seed Data Authoring Convention):
- `PRD.md` §7.11 (Tier 0 seeded-not-generated rule; literal-match row examples), §10 (Ground Truth Priority — `07` takes precedence over `01` for MVP scope)
- `mvp-tool-design.md` §9 Tier 0 (the authoritative list of Tier-0 tables grouped by domain; Step 6 implements the "Agreement domain", "Financial", and "Product/Feature" blocks), §14 Decision 2 (rationale for hand-coded seed data)
- `implementation-steps.md` Step 6 entry (exit criteria), **Seed Data Authoring Convention** (read-discipline, escalation rules, `get_<domain>_tables` output contract)

**Additional reference files** (only those named in the step's "Reads from" line, filtered per the Seed Data Authoring Convention):
- `references/07_mvp-schema-reference.md` — **authoritative DDL slice** for every table this step seeds. For each table, open only the `#### <TABLE_NAME>` block and capture column names, types, nullability, and composite PKs. Use the DDL column order exactly (this matches what Step 5's `_load_ddl_column_order` parser returns, and is what Step 8's writer will enforce).
- `references/02_data-mapping-reference.md` Step 3 — **constrained code values and literal-match rows**. Scan for the items listed below and embed them verbatim:
  - Item #1 / #13 / #21 — `Frozen Status` / `FROZEN` / `Frozen` (AGREEMENT_STATUS_TYPE)
  - Item #6 — `'Rate Feature'` subtype + `'Original Loan Term'` classification (FEATURE_SUBTYPE, FEATURE_CLASSIFICATION_TYPE)
  - Any other literal codes tied to Agreement / Financial / Feature domains
- `references/05_architect-qa.md` — open **only** Q's touching the agreement / financial / feature domains (e.g. any note on market-risk-type / day-count-basis / amortization-method). Do not read the whole file; use the document's table of contents.

**Do NOT read** (explicitly excluded to protect context budget and per the Seed Data Authoring Convention):
- `references/01_schema-reference.md` — supplementary; `07` is the MVP-filtered DDL set and takes precedence per PRD §10. (Note: `implementation-steps.md` Step 6's "Reads from" line predates the Seed Data Authoring Convention and still mentions `01`. The Convention in the same file overrides — only open `01` if `07` is ambiguous for a specific column.)
- `references/06_supporting-enrichments.md` — distributions; irrelevant for Tier 0.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` and `resources/iDM_MDM_tables_DDLs.xlsx` — already distilled into the references above. Do not re-read the Excels per session.

## Produces

All paths relative to the project root.

**New files:**

- `seed_data/__init__.py` — empty marker so `seed_data` is importable as a package. (Step 1 scaffolded `seed_data/` as an empty directory without a marker; verify and add if missing.)

- `seed_data/agreement_types.py` — seed rows for the general agreement-domain lookup tables. Exposes `get_agreement_type_tables() -> Dict[str, pd.DataFrame]`. Tables included (keys are `'Core_DB.<TABLE>'`; column order per `07`):
  - `Core_DB.AGREEMENT_SUBTYPE` — at minimum: `CHECKING`, `SAVINGS`, `MMA`, `CERTIFICATE_OF_DEPOSIT`, `RETIREMENT`, `MORTGAGE`, `CREDIT_CARD`, `VEHICLE_LOAN`, `STUDENT_LOAN`, `HELOC`, `PAYDAY`, `COMMERCIAL_CHECKING` (matches Step 10's PRODUCT row count — see `implementation-steps.md` Step 10 exit criteria).
  - `Core_DB.AGREEMENT_TYPE` — coarse-grained parent groupings (e.g. `DEPOSIT`, `LOAN`, `CREDIT`, `COMMERCIAL`).
  - `Core_DB.AGREEMENT_FORMAT_TYPE` — format enumeration (e.g. `PAPER`, `ELECTRONIC`, `HYBRID`).
  - `Core_DB.AGREEMENT_OBJECTIVE_TYPE` — purpose codes (e.g. `SAVINGS_GOAL`, `HOME_PURCHASE`, `EDUCATION`, `VEHICLE`).
  - `Core_DB.AGREEMENT_OBTAINED_TYPE` — channel-of-obtention codes (e.g. `BRANCH`, `ONLINE`, `PHONE`, `REFERRAL`).
  - `Core_DB.AGREEMENT_STATUS_SCHEME_TYPE` — the 6-tuple `config.code_values.AGREEMENT_STATUS_SCHEMES`: `Account Status`, `Accrual Status`, `Default Status`, `Drawn Undrawn Status`, `Frozen Status`, `Past Due Status`.
  - `Core_DB.AGREEMENT_STATUS_REASON_TYPE` — reason codes used by `AGREEMENT_STATUS.Agreement_Status_Reason_Cd` (e.g. `DELINQUENCY`, `CUSTOMER_REQUEST`, `FRAUD`, `DECEASED`, `WRITE_OFF`).
  - `Core_DB.AGREEMENT_FEATURE_ROLE_TYPE` — **must contain the 4 required roles** from `config.code_values.AGREEMENT_FEATURE_ROLE_CODES`: `primary`, `fee`, `rate`, `term`.
  - `Core_DB.ASSET_LIABILITY_TYPE` — balance-sheet side codes (e.g. `ASSET`, `LIABILITY`, `OFF_BALANCE_SHEET`).
  - `Core_DB.BALANCE_SHEET_TYPE` — sub-categorisation (e.g. `ON_BALANCE_SHEET`, `OFF_BALANCE_SHEET`, `CONTINGENT`).
  - `Core_DB.DOCUMENT_PRODUCTION_CYCLE_TYPE` — statement cycle codes (`MONTHLY`, `QUARTERLY`, `ANNUAL`, `ON_DEMAND`).
  - `Core_DB.STATEMENT_MAIL_TYPE` — delivery preference codes (`PAPER`, `EMAIL`, `PORTAL`, `NONE`).
  - `Core_DB.DATA_SOURCE_TYPE` — source-system codes (e.g. `CORE_BANKING`, `CARD_SYSTEM`, `LOAN_ORIGINATION`, `MDM`).

- `seed_data/status_types.py` — seed rows for `AGREEMENT_STATUS_TYPE` and any status-related sub-lookups. Exposes `get_status_type_tables() -> Dict[str, pd.DataFrame]`. Tables included:
  - `Core_DB.AGREEMENT_STATUS_TYPE` — composite PK (`Agreement_Status_Scheme_Cd` + `Agreement_Status_Cd`). **Must include the critical Frozen row verbatim** from `config.code_values.FROZEN_STATUS_ROW`: `{'Agreement_Status_Scheme_Cd': 'Frozen Status', 'Agreement_Status_Cd': 'FROZEN', 'Agreement_Status_Desc': 'Frozen'}`. Must include at least one code per scheme in `AGREEMENT_STATUS_SCHEMES` (6 schemes × ≥2 codes each → ≥12 rows minimum):
    - `Account Status` → `OPEN`, `CLOSED`, `DORMANT`, `WRITE_OFF`
    - `Accrual Status` → `ACCRUING`, `NON_ACCRUING`
    - `Default Status` → `CURRENT`, `DEFAULT`, `CURED`
    - `Drawn Undrawn Status` → `DRAWN`, `UNDRAWN`, `PARTIAL`
    - `Frozen Status` → `FROZEN`, `NOT_FROZEN` (the `FROZEN` row uses exact-desc `'Frozen'` — Layer 2 literal match)
    - `Past Due Status` → `CURRENT`, `DPD_30`, `DPD_60`, `DPD_90`, `DPD_120`

- `seed_data/financial_types.py` — seed rows for financial-instrument lookup tables. Exposes `get_financial_type_tables() -> Dict[str, pd.DataFrame]`. Tables included:
  - `Core_DB.FINANCIAL_AGREEMENT_TYPE` — top-level financial categorisation (e.g. `DEPOSIT`, `LOAN`, `CREDIT`, `INVESTMENT`, `INSURANCE`).
  - `Core_DB.AMORTIZATION_METHOD_TYPE` — standard methods (`STRAIGHT_LINE`, `EFFECTIVE_INTEREST`, `LEVEL_PAYMENT`, `INTEREST_ONLY`, `BULLET`, `CUSTOM`).
  - `Core_DB.LOAN_MATURITY_SUBTYPE` — maturity buckets (`SHORT_TERM`, `MEDIUM_TERM`, `LONG_TERM`, `PERPETUAL`).
  - `Core_DB.LOAN_TRANSACTION_SUBTYPE` — transaction-loan subtypes (`PAYDAY`, `CASH_ADVANCE`, `OVERDRAFT`).
  - `Core_DB.LOAN_TERM_SUBTYPE` — term-loan subtypes (`INSTALLMENT`, `BALLOON`, `AMORTIZING`).
  - `Core_DB.CREDIT_CARD_AGREEMENT_SUBTYPE` — card subtypes (`STANDARD`, `REWARDS`, `SECURED`, `BUSINESS`, `STUDENT`).
  - `Core_DB.MORTGAGE_TYPE` — mortgage structure (`FIXED_RATE`, `ARM`, `FHA`, `VA`, `JUMBO`, `HELOC`).
  - `Core_DB.DEPOSIT_MATURITY_SUBTYPE` — CD maturity buckets (`3M`, `6M`, `12M`, `24M`, `36M`, `60M`).
  - `Core_DB.INTEREST_DISBURSEMENT_TYPE` — how interest is paid (`COMPOUNDED`, `SIMPLE`, `ACCRUED`, `CAPITALIZED`).
  - `Core_DB.PAYMENT_TIMING_TYPE` — payment timing (`MONTHLY`, `BIWEEKLY`, `WEEKLY`, `QUARTERLY`, `ANNUAL`).
  - `Core_DB.PURCHASE_INTENT_TYPE` — mortgage purpose (`PURCHASE`, `REFINANCE`, `CASH_OUT`, `HOME_EQUITY`).
  - `Core_DB.SECURITY_TYPE` — collateral types (`REAL_ESTATE`, `VEHICLE`, `DEPOSIT`, `SECURITIES`, `UNSECURED`).
  - `Core_DB.MARKET_RISK_TYPE` — Basel market-risk classifications (`TRADING_BOOK`, `BANKING_BOOK`, `HELD_FOR_SALE`, `AVAILABLE_FOR_SALE`). **Required NOT NULL on FINANCIAL_AGREEMENT** per `mvp-tool-design.md` §9 Tier 7.
  - `Core_DB.TRADING_BOOK_TYPE` — book classification (`TRADING`, `BANKING`, `HEDGING`).
  - `Core_DB.DAY_COUNT_BASIS_TYPE` — standard conventions (`30_360`, `ACTUAL_360`, `ACTUAL_365`, `ACTUAL_ACTUAL`).
  - `Core_DB.RISK_EXPOSURE_MITIGANT_SUBTYPE` — mitigants (`COLLATERAL`, `GUARANTEE`, `NETTING`, `CREDIT_INSURANCE`).
  - `Core_DB.PRICING_METHOD_SUBTYPE` — rate-setting methods (`FIXED`, `FLOATING`, `INDEXED`, `TIERED`).

- `seed_data/feature_types.py` — seed rows for feature-taxonomy lookup tables. Exposes `get_feature_type_tables() -> Dict[str, pd.DataFrame]`. Tables included:
  - `Core_DB.FEATURE_SUBTYPE` — **must include the row with `Feature_Subtype_Cd = 'Rate Feature'`** (exact string, case-sensitive; matches `config.code_values.RATE_FEATURE_SUBTYPE_CD`) plus at least: `Fee Feature`, `Term Feature`, `Balance Feature`, `Reward Feature`, `Insurance Feature`, `Payment Feature`.
  - `Core_DB.FEATURE_INSURANCE_SUBTYPE` — insurance-feature sub-categorisation (e.g. `LIFE`, `DISABILITY`, `UNEMPLOYMENT`, `PROPERTY`, `CREDIT`).
  - `Core_DB.FEATURE_CLASSIFICATION_TYPE` — **must include the row with `Feature_Classification_Cd = 'Original Loan Term'`** (exact string; matches `config.code_values.ORIGINAL_LOAN_TERM_CLASSIFICATION_CD`) plus at least: `Current Rate`, `Origination Rate`, `Minimum Balance`, `Maximum Balance`, `Minimum Payment`, `Maturity Date`.

**Do NOT produce** in this step (belongs to Step 7, 8, or later):
- `seed_data/party_types.py`, `seed_data/industry_codes.py` — **Step 7**.
- `seed_data/channel_types.py`, `seed_data/campaign_types.py`, `seed_data/address_types.py`, `seed_data/currency.py`, `seed_data/interest_rate_indices.py`, `seed_data/misc_types.py`, `generators/tier0_lookups.py` — **Step 8**.
- Any DI column stamping on the returned DataFrames. Stamping happens in Step 8's `Tier0Lookups.generate(ctx)`. The `get_<domain>_tables()` contract is explicit: return un-stamped, DDL-ordered DataFrames only.

## Tables generated (if applicable)

The four seed modules together produce **~34 un-stamped DataFrames** keyed by `'Core_DB.<TABLE>'`. Row counts are plausible 4–30 per table (lookup tables are small by nature).

| Module | Table | Min rows | Literal-match requirements |
|--------|-------|---------:|----------------------------|
| `agreement_types.py` | `Core_DB.AGREEMENT_SUBTYPE` | 12 | Covers every product type in the universe (per Step 10 PRODUCT row set) |
| | `Core_DB.AGREEMENT_TYPE` | 4 | — |
| | `Core_DB.AGREEMENT_FORMAT_TYPE` | 3 | — |
| | `Core_DB.AGREEMENT_OBJECTIVE_TYPE` | 4 | — |
| | `Core_DB.AGREEMENT_OBTAINED_TYPE` | 4 | — |
| | `Core_DB.AGREEMENT_STATUS_SCHEME_TYPE` | 6 | Exactly the 6 strings in `config.code_values.AGREEMENT_STATUS_SCHEMES` |
| | `Core_DB.AGREEMENT_STATUS_REASON_TYPE` | 5 | — |
| | `Core_DB.AGREEMENT_FEATURE_ROLE_TYPE` | 4 | Exactly `{'primary','fee','rate','term'}` |
| | `Core_DB.ASSET_LIABILITY_TYPE` | 3 | — |
| | `Core_DB.BALANCE_SHEET_TYPE` | 3 | — |
| | `Core_DB.DOCUMENT_PRODUCTION_CYCLE_TYPE` | 4 | — |
| | `Core_DB.STATEMENT_MAIL_TYPE` | 4 | — |
| | `Core_DB.DATA_SOURCE_TYPE` | 4 | — |
| `status_types.py` | `Core_DB.AGREEMENT_STATUS_TYPE` | 12 | **Critical** — row `{'Frozen Status','FROZEN','Frozen'}` present verbatim; composite PK uniqueness holds |
| `financial_types.py` | `Core_DB.FINANCIAL_AGREEMENT_TYPE` | 5 | — |
| | `Core_DB.AMORTIZATION_METHOD_TYPE` | 6 | — |
| | `Core_DB.LOAN_MATURITY_SUBTYPE` | 4 | — |
| | `Core_DB.LOAN_TRANSACTION_SUBTYPE` | 3 | — |
| | `Core_DB.LOAN_TERM_SUBTYPE` | 3 | — |
| | `Core_DB.CREDIT_CARD_AGREEMENT_SUBTYPE` | 5 | — |
| | `Core_DB.MORTGAGE_TYPE` | 6 | — |
| | `Core_DB.DEPOSIT_MATURITY_SUBTYPE` | 6 | — |
| | `Core_DB.INTEREST_DISBURSEMENT_TYPE` | 4 | — |
| | `Core_DB.PAYMENT_TIMING_TYPE` | 5 | — |
| | `Core_DB.PURCHASE_INTENT_TYPE` | 4 | — |
| | `Core_DB.SECURITY_TYPE` | 5 | — |
| | `Core_DB.MARKET_RISK_TYPE` | 4 | Must include at least one code usable as a `FINANCIAL_AGREEMENT.Market_Risk_Type_Cd` default |
| | `Core_DB.TRADING_BOOK_TYPE` | 3 | — |
| | `Core_DB.DAY_COUNT_BASIS_TYPE` | 4 | — |
| | `Core_DB.RISK_EXPOSURE_MITIGANT_SUBTYPE` | 4 | — |
| | `Core_DB.PRICING_METHOD_SUBTYPE` | 4 | — |
| `feature_types.py` | `Core_DB.FEATURE_SUBTYPE` | 7 | **Critical** — `Feature_Subtype_Cd='Rate Feature'` row present |
| | `Core_DB.FEATURE_INSURANCE_SUBTYPE` | 5 | — |
| | `Core_DB.FEATURE_CLASSIFICATION_TYPE` | 7 | **Critical** — `Feature_Classification_Cd='Original Loan Term'` row present |

Actual column counts and orderings are dictated by `references/07_mvp-schema-reference.md` — not by this spec. Every DataFrame must have all DDL-declared columns (including nullable ones — fill with `None` where data is genuinely absent; do not omit the column).

## Files to modify

No files modified. All outputs are new files under `seed_data/`. `config/`, `utils/`, `registry/`, `generators/`, `output/`, `main.py`, `CLAUDE.md`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, and `references/` are NOT touched.

If the implementation discovers that an `AGREEMENT_STATUS_TYPE` row the spec assumes is actually spelled differently in `references/07_mvp-schema-reference.md` (or if `07` omits a column this spec assumes), escalate per Handoff Protocol §2 — update the upstream reference or add a `⚠️ Conflict` block to this spec. Do not silently improvise codes.

## New dependencies

No new dependencies. `pandas` is already in `requirements.txt` (Step 1). Seed modules depend only on the standard library and pandas.

## Rules for implementation

Universal (apply to every step):

- BIGINT for all ID columns (per PRD §7.1) — **n/a for lookup tables**: all tables in this step have CHAR / VARCHAR code columns as their PK, no `*_Id` BIGINT columns. If `07` reveals any BIGINT column in these tables, use `pd.Int64Dtype()` (nullable BIGINT).
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — n/a: no party IDs in lookup tables.
- DI column stamping on every table via `BaseGenerator.stamp_di()` — **deferred to Step 8**. This step produces un-stamped DataFrames. Do NOT import `generators.base` here.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records — n/a at seed-authoring time; stamped in Step 8.
- CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` (per PRD §7.3) — n/a: every table in this step is `Core_DB`.
- **Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md`** — enforced at authoring time. Each dict literal or `pd.DataFrame(..., columns=[...])` must list columns in DDL order. Step 5's writer reorderer would re-order them anyway, but authoring in DDL order prevents silent divergence and aids review.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — n/a: no `PARTY_INTERRACTION_EVENT` rows in this step.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — n/a: no geospatial tables here.
- No ORMs, no database connections — pure pandas → CSV. The seed modules construct `pd.DataFrame(...)` and return them; no disk I/O, no imports beyond pandas + standard library + `config`.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42` — **n/a, and critically so**: this step introduces zero randomness. Seed data is deterministic by construction (every row is hand-written).

Step-specific rules (Tier 0 seed authoring):

- **No randomness, no Faker, no dynamic generation.** Every row is a hand-written dict literal. `numpy`, `faker`, `scipy`, `random` — none of these appear in the imports of any file produced by this step. Verified by a `grep` check in Definition of done.
- **Reuse `config.code_values` literals.** Where a code / scheme / role is already defined as a constant there (`FROZEN_STATUS_ROW`, `AGREEMENT_STATUS_SCHEMES`, `AGREEMENT_FEATURE_ROLE_CODES`, `RATE_FEATURE_SUBTYPE_CD`, `ORIGINAL_LOAN_TERM_CLASSIFICATION_CD`), import and use it verbatim — never duplicate the string. This guarantees a single source of truth for Layer 2 literal-match codes.
- **DDL column order is authoritative.** Before authoring any table, open `references/07_mvp-schema-reference.md`, find the `#### <TABLE_NAME>` block, and list columns in the exact order shown. If a column is NULL-able and the seed has no plausible value, use `None` (Python) — the column must still be present in the DataFrame. Type-appropriate NULL handling (`pd.NA` vs `None`) is left to Step 8's stamping layer; at author time, `None` is acceptable.
- **Composite PK uniqueness is the author's responsibility.** `AGREEMENT_STATUS_TYPE` has composite PK `(Agreement_Status_Scheme_Cd, Agreement_Status_Cd)`. The seed must not repeat a `(scheme, code)` pair. Definition of done includes a uniqueness assertion.
- **Desc columns must be human-readable English.** Title-case for multi-word, preserving any Layer-2-literal exceptions (`'Frozen'`, `'Rate Feature'`, `'Original Loan Term'`). E.g. `STUDENT_LOAN` → `'Student Loan'`, `MMA` → `'Money Market Account'`. These feed `ACCOUNT_DIMENSION.Product_Desc` / `ACCOUNT_STATUS_DIMENSION.Status_Desc` in Layer 2.
- **Each module exposes exactly one public function**, named `get_<domain>_tables()`, returning `Dict[str, pd.DataFrame]` keyed by `'Core_DB.<TABLE>'`. No other public surface. Helper lists / constants may be module-private (leading underscore). This is the contract Step 8 relies on.
- **No side effects on import.** Importing a seed module must not construct DataFrames eagerly. Build them inside `get_<domain>_tables()` so module import is cheap and the DataFrames are freshly constructed per caller (avoids cross-call mutation bugs). Verified in Definition of done.
- **Escalation over improvisation.** If `references/07_mvp-schema-reference.md` lacks a column whose legal values the spec asks for, or if `references/02_data-mapping-reference.md` Step 3 is ambiguous on a literal code, follow Handoff Protocol §2 — leave a `⚠️ Conflict` block in this spec, do NOT invent codes.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current directory and `python` resolves to the project's Python 3.12 environment.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

**Module-import and API contract:**

- [ ] `python -c "import seed_data.agreement_types, seed_data.status_types, seed_data.financial_types, seed_data.feature_types"` exits 0.
- [ ] Each module exposes exactly one public function named `get_<domain>_tables`. Run:
  ```bash
  python -c "
  import seed_data.agreement_types as at, seed_data.status_types as st, \
         seed_data.financial_types as ft, seed_data.feature_types as ffe
  assert callable(at.get_agreement_type_tables)
  assert callable(st.get_status_type_tables)
  assert callable(ft.get_financial_type_tables)
  assert callable(ffe.get_feature_type_tables)
  print('API contract OK')
  "
  ```
- [ ] Each `get_<domain>_tables()` returns `Dict[str, pd.DataFrame]` keyed by `'Core_DB.<TABLE>'`. Run:
  ```bash
  python -c "
  import pandas as pd
  from seed_data.agreement_types import get_agreement_type_tables
  from seed_data.status_types import get_status_type_tables
  from seed_data.financial_types import get_financial_type_tables
  from seed_data.feature_types import get_feature_type_tables
  for fn in (get_agreement_type_tables, get_status_type_tables,
             get_financial_type_tables, get_feature_type_tables):
      d = fn()
      assert isinstance(d, dict) and all(isinstance(v, pd.DataFrame) for v in d.values())
      assert all(k.startswith('Core_DB.') for k in d)
  print('return-type OK')
  "
  ```

**Critical literal-match rows (Layer 2 dependencies):**

- [ ] The `Frozen Status` / `FROZEN` / `Frozen` row is present in `Core_DB.AGREEMENT_STATUS_TYPE` exactly. Run:
  ```bash
  python -c "
  from seed_data.status_types import get_status_type_tables
  df = get_status_type_tables()['Core_DB.AGREEMENT_STATUS_TYPE']
  mask = ((df.Agreement_Status_Scheme_Cd == 'Frozen Status') &
          (df.Agreement_Status_Cd == 'FROZEN') &
          (df.Agreement_Status_Desc == 'Frozen'))
  assert mask.sum() == 1, f'expected exactly 1 FROZEN row, got {mask.sum()}'
  print('FROZEN row OK')
  "
  ```
- [ ] `AGREEMENT_FEATURE_ROLE_TYPE` contains **exactly** `{'primary','fee','rate','term'}`. Run:
  ```bash
  python -c "
  from seed_data.agreement_types import get_agreement_type_tables
  df = get_agreement_type_tables()['Core_DB.AGREEMENT_FEATURE_ROLE_TYPE']
  # PK column name inferred from DDL; fall back to .iloc[:,0] if unsure
  roles = set(df.iloc[:,0].astype(str).str.lower())
  assert roles >= {'primary','fee','rate','term'}, roles
  print('AGREEMENT_FEATURE_ROLE_TYPE OK')
  "
  ```
- [ ] `FEATURE_SUBTYPE` contains `Feature_Subtype_Cd = 'Rate Feature'` exactly. Run:
  ```bash
  python -c "
  from seed_data.feature_types import get_feature_type_tables
  df = get_feature_type_tables()['Core_DB.FEATURE_SUBTYPE']
  assert (df.Feature_Subtype_Cd == 'Rate Feature').sum() == 1
  print('Rate Feature row OK')
  "
  ```
- [ ] `FEATURE_CLASSIFICATION_TYPE` contains `Feature_Classification_Cd = 'Original Loan Term'` exactly. Run:
  ```bash
  python -c "
  from seed_data.feature_types import get_feature_type_tables
  df = get_feature_type_tables()['Core_DB.FEATURE_CLASSIFICATION_TYPE']
  assert (df.Feature_Classification_Cd == 'Original Loan Term').sum() == 1
  print('Original Loan Term row OK')
  "
  ```
- [ ] `AGREEMENT_STATUS_SCHEME_TYPE` has exactly the 6 scheme names from `config.code_values.AGREEMENT_STATUS_SCHEMES`. Run:
  ```bash
  python -c "
  from seed_data.agreement_types import get_agreement_type_tables
  from config.code_values import AGREEMENT_STATUS_SCHEMES
  df = get_agreement_type_tables()['Core_DB.AGREEMENT_STATUS_SCHEME_TYPE']
  schemes = set(df.iloc[:,0].astype(str))
  assert schemes == set(AGREEMENT_STATUS_SCHEMES), (schemes, set(AGREEMENT_STATUS_SCHEMES))
  print('AGREEMENT_STATUS_SCHEME_TYPE OK')
  "
  ```
- [ ] `AGREEMENT_STATUS_TYPE` covers every scheme (each scheme has ≥1 status row). Run:
  ```bash
  python -c "
  from seed_data.status_types import get_status_type_tables
  from config.code_values import AGREEMENT_STATUS_SCHEMES
  df = get_status_type_tables()['Core_DB.AGREEMENT_STATUS_TYPE']
  by_scheme = df.groupby('Agreement_Status_Scheme_Cd').size()
  for sch in AGREEMENT_STATUS_SCHEMES:
      assert sch in by_scheme.index and by_scheme[sch] >= 1, f'scheme {sch} missing'
  # composite PK uniqueness
  assert not df.duplicated(['Agreement_Status_Scheme_Cd','Agreement_Status_Cd']).any()
  print('AGREEMENT_STATUS_TYPE scheme coverage + PK uniqueness OK')
  "
  ```

**DDL column-order alignment with Step 5's parser:**

- [ ] For every table produced by every seed module, the DataFrame's column list equals the DDL column list returned by `output.writer._load_ddl_column_order()`. Run:
  ```bash
  python -c "
  from output.writer import _load_ddl_column_order
  from seed_data.agreement_types import get_agreement_type_tables
  from seed_data.status_types import get_status_type_tables
  from seed_data.financial_types import get_financial_type_tables
  from seed_data.feature_types import get_feature_type_tables
  ddl = _load_ddl_column_order()
  combined = {}
  for fn in (get_agreement_type_tables, get_status_type_tables,
             get_financial_type_tables, get_feature_type_tables):
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
  If a table is legitimately missing from `07`'s DDL parse (`_load_ddl_column_order` yields `<200` keys known), log the mismatch and escalate per Handoff Protocol §2 rather than silently passing.

**Row-count plausibility:**

- [ ] Every table has ≥3 rows. Run:
  ```bash
  python -c "
  from seed_data.agreement_types import get_agreement_type_tables
  from seed_data.status_types import get_status_type_tables
  from seed_data.financial_types import get_financial_type_tables
  from seed_data.feature_types import get_feature_type_tables
  combined = {}
  for fn in (get_agreement_type_tables, get_status_type_tables,
             get_financial_type_tables, get_feature_type_tables):
      combined.update(fn())
  for k, df in combined.items():
      assert len(df) >= 3, f'{k}: only {len(df)} rows'
  print(f'all {len(combined)} tables have >=3 rows')
  "
  ```
- [ ] Total table count produced by this step is between 30 and 40 (the spec itemises ~34). Run:
  ```bash
  python -c "
  from seed_data.agreement_types import get_agreement_type_tables
  from seed_data.status_types import get_status_type_tables
  from seed_data.financial_types import get_financial_type_tables
  from seed_data.feature_types import get_feature_type_tables
  n = sum(len(fn()) for fn in (
      get_agreement_type_tables, get_status_type_tables,
      get_financial_type_tables, get_feature_type_tables))
  assert 30 <= n <= 40, n
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
  for p in pathlib.Path('seed_data').glob('*.py'):
      if p.name == '__init__.py': continue
      for i, line in enumerate(p.read_text().splitlines(), 1):
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
  # Track pd.DataFrame calls during module import
  calls = {'n': 0}
  _orig = pd.DataFrame
  def _wrap(*a, **k):
      calls['n'] += 1
      return _orig(*a, **k)
  pd.DataFrame = _wrap
  for name in ('seed_data.agreement_types','seed_data.status_types',
               'seed_data.financial_types','seed_data.feature_types'):
      sys.modules.pop(name, None)
      importlib.import_module(name)
  pd.DataFrame = _orig
  assert calls['n'] == 0, f'{calls[\"n\"]} DataFrame(s) built at import time'
  print('no import-time DataFrames')
  "
  ```

**Reuse of `config.code_values`:**

- [ ] `seed_data/status_types.py` references `FROZEN_STATUS_ROW` by import (or constructs an equivalent via literals from `config.code_values`). Run:
  ```bash
  python -c "
  import pathlib
  src = pathlib.Path('seed_data/status_types.py').read_text()
  # Either import FROZEN_STATUS_ROW, or have 'Frozen Status' + 'FROZEN' + 'Frozen' literals
  ok = ('FROZEN_STATUS_ROW' in src) or (\"'Frozen Status'\" in src and \"'FROZEN'\" in src and \"'Frozen'\" in src)
  assert ok, 'status_types.py does not reference the Frozen literal-match row'
  print('FROZEN literal-match wiring OK')
  "
  ```
- [ ] `seed_data/agreement_types.py` imports or mirrors `AGREEMENT_STATUS_SCHEMES` from `config.code_values`. Run:
  ```bash
  python -c "
  import pathlib
  src = pathlib.Path('seed_data/agreement_types.py').read_text()
  assert 'AGREEMENT_STATUS_SCHEMES' in src or ('Account Status' in src and 'Frozen Status' in src)
  print('scheme literal wiring OK')
  "
  ```

### Universal checks

- [ ] `git status` shows only files listed under ## Produces — nothing else. Run:
  ```bash
  git status --porcelain
  ```
  Every line must map to `seed_data/__init__.py` or `seed_data/{agreement_types,status_types,financial_types,feature_types}.py`. No stray files (no pycache, no outputs, no changes under `config/`, `utils/`, `generators/`, `output/`, `references/`, `specs/` outside this step's spec).
- [ ] All new files pass `python -c "import <module>"` — covered by the first check above.
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — **n/a**: this step produces no CSVs. The seed tables are pure code-based lookups with no `*_Id` BIGINT columns by design (PKs are CHAR / VARCHAR scheme / code pairs). If `07` reveals any `*_Id` column in the scoped tables, use `pd.Int64Dtype()`.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: `PARTY_INTERRACTION_EVENT` is a CDM_DB table generated in Step 22, not touched here.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSV output at this step; the writer is not invoked.

## Handoff notes

**Shipped (2026-04-20):**
- `seed_data/__init__.py` — empty package marker
- `seed_data/agreement_types.py` — 13 tables, exposes `get_agreement_type_tables()`
- `seed_data/status_types.py` — 1 table (AGREEMENT_STATUS_TYPE, 19 rows across 6 schemes), exposes `get_status_type_tables()`
- `seed_data/financial_types.py` — 17 tables, exposes `get_financial_type_tables()`
- `seed_data/feature_types.py` — 3 tables, exposes `get_feature_type_tables()`
- All 12 DoD checks passed: imports, API contract, 4 literal-match rows, scheme coverage, composite PK uniqueness, DDL column-order alignment (34/34 tables), row counts, no randomness, no import-time DataFrames, config literal wiring

**Key implementation note — DI columns included as None:**
All DataFrames include `di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind` as the final three columns (all `None`). This is required because `output.writer._load_ddl_column_order()` returns column lists that include DI columns, and the DoD alignment check enforces strict equality. Step 8's `Tier0Lookups.generate(ctx)` will overwrite these None values with stamped DI values.

**Deferred / follow-up:** None — all issues resolved in session.
- `.gitignore` created (covers `__pycache__/`, `*.pyc`, generated output dirs, venvs, editor/OS artifacts). All 17 previously-tracked `.pyc` files removed from git index via `git rm --cached`. Clean `git status` — only `seed_data/` and `.gitignore` appear as new untracked files.

**Next session hint:** Step 7 (party/industry seed data) and Step 8 (channel/campaign/misc seed + Tier0Lookups generator wiring) are both unblocked. Steps 6, 7, and 8 are independent per the Dependency Graph.

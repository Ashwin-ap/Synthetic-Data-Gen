# Spec: Step 16 — Tier 7a Agreement Cross-Cutting Details

## Overview

This step builds **Tier 7a**, the most critical tier for Layer 2 transformation-readiness. Every agreement produced by Step 10 (Tier 2 Core) is given its full cross-cutting detail footprint — the six-way `AGREEMENT_STATUS` pivot scheme rows, a `'preferred'`-marked `AGREEMENT_CURRENCY` row, a profitability `AGREEMENT_SCORE` row, at least one `AGREEMENT_FEATURE` row per loan-type agreement plus monthly balance-trajectory rows for the DECLINING cohort, one `AGREEMENT_METRIC` and one `AGREEMENT_RATE` row, plus the three feature sub-type tables (`VARIABLE_INTEREST_RATE_FEATURE`, `TERM_FEATURE`) and the reference rate history table (`INTEREST_INDEX_RATE`). See `mvp-tool-design.md` §9 Tier 7 for the authoritative scope; `references/02_data-mapping-reference.md` Step 3 items #1 (6-scheme pivot), #6 (Rate Feature for loans), #8 (preferred currency), #13/#21 (Frozen_Ind literal), and #17 (profitability AGREEMENT_SCORE) are the Layer-2 literal constraints this step enforces. Nine Core_DB tables are produced, all inheriting `Agreement_Id` / `Feature_Id` / `Interest_Rate_Index_Cd` FKs from upstream tiers (no new IDs are minted here except for the AGREEMENT_METRIC composite PK time dimension). Tier 7b (Step 17) follows and writes the exclusive sub-type chain; Tier 7a intentionally does not touch the sub-type tables or CARD.

## Depends on

- **Step 1** — consumes `config/settings.py` constants: `HIGH_TS`, `HIGH_DATE`, `HISTORY_START`, `SIM_DATE`, `SEED`.
- **Step 2** — consumes `generators/base.BaseGenerator.stamp_di()` (5-column DI tail) and `utils/date_utils.month_snapshots()` (6 calendar-month tuples spanning HISTORY_START → SIM_DATE). Does NOT consume `IdFactory` — this step mints no new entity IDs (FKs reuse `Agreement_Id` from Tier 2, `Feature_Id` from Tier 2, `Interest_Rate_Index_Cd` from Tier 0, `Model_Id` from Tier 2).
- **Step 3** — consumes `registry/context.GenerationContext` and `registry/profiles.AgreementProfile` fields: `agreement_id`, `owner_party_id`, `product_type`, `open_dttm`, `close_dttm`, `balance_amt`, `interest_rate`, `original_loan_amt`, `is_delinquent`, `is_severely_delinquent`, `is_frozen`, `monthly_balances`, `is_financial`, `is_loan_term`, `is_mortgage`, `is_credit_card`, `is_loan_transaction`.
- **Step 4** — consumes `ctx.agreements` (≈5,000 AgreementProfile instances with all flags, dates, amounts, and `monthly_balances` populated; DECLINING cohort has `len(monthly_balances)==6`; ACTIVE/NEW/CHURNED have `len(monthly_balances)==0`).
- **Step 6** — consumes these Tier 0a seed tables (must be present in `ctx.tables` at entry):
  - `Core_DB.AGREEMENT_STATUS_TYPE` — literal-match source. Must contain the row `(Agreement_Status_Scheme_Cd='Frozen Status', Agreement_Status_Cd='FROZEN', Agreement_Status_Desc='Frozen')`. Also `(Frozen Status, NOT_FROZEN, Not Frozen)`, and scheme-specific codes for Account/Accrual/Default/Drawn Undrawn/Past Due. The seed module at `seed_data/status_types.py` authors these.
  - `Core_DB.AGREEMENT_STATUS_SCHEME_TYPE` — the 6 scheme codes (`AGREEMENT_STATUS_SCHEMES` constant from `config/code_values.py`).
  - `Core_DB.AGREEMENT_FEATURE_ROLE_TYPE` — `'primary' | 'fee' | 'rate' | 'term'` codes (`AGREEMENT_FEATURE_ROLE_CODES` from `config/code_values.py`).
- **Step 8** — consumes these Tier 0c seed tables:
  - `Core_DB.INTEREST_RATE_INDEX` — 5 rows keyed by `Interest_Rate_Index_Cd ∈ {SOFR, PRIME, FEDFUNDS, LIBOR, EURIBOR}`. `INTEREST_INDEX_RATE` (Tier 7a) FKs into this.
  - `Core_DB.CURRENCY` — `Currency_Cd='USD'` row present for `AGREEMENT_CURRENCY.Agreement_Currency_Cd`.
  - `Core_DB.TIME_PERIOD_TYPE` — codes `'DAY' | 'MONTH' | 'YEAR'` present (`AGREEMENT_RATE.Agreement_Rate_Time_Period_Cd = 'YEAR'` is the intended literal; the session verifies the code exists in the seed before using it).
  - `Core_DB.UNIT_OF_MEASURE` — Tier 7a reads the `Unit_Of_Measure_Cd` column to pick two values: one for monetary amount (e.g. `'USD'`) and one for rate/percentage (e.g. `'PERCENT'`). If neither exists, the session escalates per Handoff Protocol §2 — do NOT silently improvise.
- **Step 10** — consumes these Tier 2 tables (must be present in `ctx.tables`):
  - `Core_DB.AGREEMENT` — `Agreement_Id` universe. Tier 7a emits one or more rows per `Agreement_Id`; none are invented.
  - `Core_DB.FEATURE` — must contain at least one row with `Feature_Subtype_Cd='Rate Feature'` AND `Feature_Classification_Cd='Original Loan Term'` (the combined Layer 2 literal match, per 02 Step 3 items #6/#18). The current Step 10 seed has row 0 satisfying both constraints. Tier 7a picks that row's `Feature_Id` as the "rate feature ID" for loan AGREEMENT_FEATURE rows.
  - `Core_DB.ANALYTICAL_MODEL` — must contain at least one row with `Model_Type_Cd='profitability'` (per 02 Step 3 item #17). Tier 7a picks the first such `Model_Id` for every AGREEMENT_SCORE row.

No code from Step 5 (writer), Step 9 (Tier 1), Step 11/12/13/14 (Tier 3/4), or Step 15 (Tier 5/6) is imported by this step. The writer is not invoked — `generate()` returns DataFrames only; orchestrator (Step 25) handles `ctx.tables.update()` and later CSV emission.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 16):
- `PRD.md` §5 "Core Design Principles" (esp. §5.2 Layer 2 transformation-readiness), §7.1 (BIGINT), §7.3 (DI columns), §7.4 (SCD2 history — delinquency transitions, DECLINING monthly rows)
- `mvp-tool-design.md` §7 (`BaseGenerator` + DI rules), §9 Tier 7 (**most critical for this step — reads as written**), §12 constraints #1/#6/#7/#8/#13/#17/#21 (this step enforces #1/#6/#8/#13/#17/#21; #7 is Tier 8)
- `implementation-steps.md` Step 16 entry (exit criteria); Handoff Protocol

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the nine in-scope tables. Open only these blocks (use SQL DDL where summary tables disagree, per CLAUDE.md "DDL verification rule" and PRD §10):
  - `AGREEMENT_STATUS` (DDL §4130): 6 business + 3 DI = 9 cols. PK `Agreement_Id` + `Agreement_Status_Scheme_Cd`. NOT NULL: `Agreement_Id`, `Agreement_Status_Scheme_Cd`, `Agreement_Status_Start_Dttm`, `Agreement_Status_Cd`. Nullable: `Agreement_Status_Reason_Cd`, `Agreement_Status_End_Dttm`.
  - `AGREEMENT_CURRENCY` (DDL §3450): 5 business + 3 DI = 8 cols. NOT NULL: `Currency_Use_Cd`, `Agreement_Id`, `Agreement_Currency_Start_Dt`, `Agreement_Currency_Cd`. Nullable: `Agreement_Currency_End_Dt`.
  - `AGREEMENT_SCORE` (DDL §3508): 4 business + 3 DI = 7 cols. NOT NULL: `Agreement_Id`, `Model_Id`, `Model_Run_Id`, `Agreement_Score_Val` VARCHAR(100).
  - `AGREEMENT_FEATURE` (DDL §6491): 16 business + 3 DI = 19 cols. NOT NULL: `Agreement_Id`, `Feature_Id`, `Agreement_Feature_Role_Cd`, `Agreement_Feature_Start_Dttm`, `Agreement_Feature_UOM_Cd`. Nullable: `Agreement_Feature_End_Dttm`, `Overridden_Feature_Id`, `Agreement_Feature_Concession_Ind` (CHAR(3)), `Agreement_Feature_Amt` DECIMAL(18,4), `Agreement_Feature_To_Amt`, `Agreement_Feature_Rate` DECIMAL(15,12), `Agreement_Feature_Qty`, `Agreement_Feature_Num`, `Agreement_Feature_Dt`, `Interest_Rate_Index_Cd`, `Currency_Cd`.
  - `AGREEMENT_METRIC` (DDL §4040): 13 business + 3 DI = 16 cols. NOT NULL: `Agreement_Id`, `Agreement_Metric_Type_Cd`, `Agreement_Metric_Start_Dttm`. Nullable: `Agreement_Metric_End_Dttm`, `Agreement_Metric_Time_Period_Cd`, `Agreement_Metric_Amt`, `Agreement_Metric_Cnt`, `Agreement_Metric_Rate`, `Agreement_Metric_Qty`, `Agreement_Currency_Metric_Amt`, `Currency_Cd`, `Unit_Of_Measure_Cd`, `GL_Main_Account_Segment_Id`.
  - `AGREEMENT_RATE` (DDL §4661): 7 business + 3 DI = 10 cols. NOT NULL: `Agreement_Id`, `Rate_Type_Cd`, `Balance_Category_Type_Cd`, `Agreement_Rate_Start_Dttm`, `Agreement_Rate_Time_Period_Cd`. Nullable: `Agreement_Rate_End_Dttm`, `Agreement_Rate` DECIMAL(15,12).
  - `TERM_FEATURE` (DDL §6417): 8 business + 3 DI = 11 cols. NOT NULL only `Feature_Id`. All other fields nullable VARCHAR(50).
  - `AGREEMENT_FEATURE` (same as above — listed for the critical `Agreement_Feature_UOM_Cd NOT NULL` constraint not present in §2148 summary but present in §6521 DDL). DDL wins.
  - `INTEREST_INDEX_RATE` (DDL §6542): 5 business + 3 DI = 8 cols. NOT NULL: `Interest_Rate_Index_Cd`, `Index_Rate_Effective_Dttm` (DDL declares DATE despite the "Dttm" suffix — use DATE). Nullable: `Interest_Index_Rate`, `Discount_Factor_Pct`, `Zero_Coupon_Rate`.
  - `VARIABLE_INTEREST_RATE_FEATURE` (DDL §6571): 5 business + 3 DI = 8 cols. NOT NULL: `Feature_Id`, `Interest_Rate_Index_Cd`. Nullable: `Spread_Rate` DECIMAL(15,12), `Upper_Limit_Rate`, `Lower_Limit_Rate`.
  - `INTEREST_RATE_INDEX` (DDL §6452) — **DO NOT regenerate.** Already seeded in Step 8 (`seed_data/interest_rate_indices.py`). Tier 7a only reads the seeded 5 rows to wire FKs.
  - Footnote §3102 — `AGREEMENT_FEATURE` duplicate typo `AGREEMEN_FEATURE` is a historical mapping artifact; only the correct spelling is in scope.
  - Footnotes §3103 (`AGREEMENT_SCORE.Model_Id`/`Model_Run_Id` INTEGER FK candidates), §3118 (`AGREEMENT_FEATURE.Feature_Id` INTEGER FK candidate) — **reiterate the BIGINT rule**. Every `*_Id` emitted in this step is `Int64`.
- `references/02_data-mapping-reference.md` Step 3 items — open only these Layer 2 literal-match requirements (**do not change any value sourced from here**, per PRD §10 priority 1):
  - **Item #1** — `AGREEMENT_STATUS` must have records for all 6 scheme types: `'Account Status'`, `'Accrual Status'`, `'Default Status'`, `'Drawn Undrawn Status'`, `'Frozen Status'`, `'Past Due Status'`. Without all 6, ACCOUNT_STATUS_PIVOT_BB produces NULL pivoted columns.
  - **Item #6** — Loan agreements must have an `AGREEMENT_FEATURE` row with `Feature_Id` where `FEATURE.Feature_Subtype_Cd = 'Rate Feature'` (drives `LOAN_ACCOUNT_BB.Interest Rate Index Cd`).
  - **Item #8** — `AGREEMENT_CURRENCY` must have `Currency_Use_Cd = 'preferred'` for each Agreement (drives `ACCOUNT_BB.Preferred Currency Cd`).
  - **Item #13** — ACCOUNT_STATUS_DIMENSION.Frozen_Ind = '1' when frozen status code description matches 'frozen' (case-insensitive). Seed row in AGREEMENT_STATUS_TYPE is `(Frozen Status, FROZEN, Frozen)` — case-insensitive match satisfies the rule.
  - **Item #17** — `AGREEMENT_SCORE` requires an ANALYTICAL_MODEL with `Model_Type_Cd = 'profitability'` and one AGREEMENT_SCORE row per agreement pointing at that model.
  - **Item #21** — Frozen_Ind derivation needs `AGREEMENT_STATUS.Agreement_Status_Scheme_Cd = 'Frozen Status'` AND the corresponding `Agreement_Status_Cd` whose desc = 'Frozen' (covered by the same seed row as item #13).
- `references/06_supporting-enrichments.md` — open **only** Part I1 (§§530–542): "Mortgage Interest Rate Vintages". Provides the origination-year → rate-range table used by `AGREEMENT_RATE.Agreement_Rate` on mortgage agreements. `AgreementProfile.interest_rate` already applies this lookup at universe-build time — Tier 7a consumes `ag.interest_rate` verbatim and does not re-sample.

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is MVP-authoritative per PRD §10; only open `01` if `07` is ambiguous for a specific column.
- `references/05_architect-qa.md` — no Q touches Tier 7a directly (Q7 self-employment is Step 12; Q6 CDM_Address_Id is Step 22).
- `references/06_supporting-enrichments.md` Parts A, B, C, D–H, I2–I5, J — not needed; distributions were consumed by Step 4.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `iDM_MDM_tables_DDLs.xlsx` — already distilled into `07` and `02`.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier7a_agreement_crosscut.py` — `class Tier7aAgreementCrosscut(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]`. Implementation contract:
  1. Import `BaseGenerator`; import `GenerationContext` under `TYPE_CHECKING` only. Import `pd`, `numpy as np`; `from datetime import datetime, date, timedelta`; `from decimal import Decimal`; `from config.settings import HISTORY_START, SIM_DATE`; `from config.code_values import AGREEMENT_STATUS_SCHEMES, FROZEN_STATUS_ROW, CURRENCY_USE_CODES, PROFITABILITY_MODEL_TYPE_CD, RATE_FEATURE_SUBTYPE_CD, ORIGINAL_LOAN_TERM_CLASSIFICATION_CD`; `from utils.date_utils import month_snapshots`; `from registry.profiles import AgreementProfile`.
  2. Declare module-level constants (all reproducibility-friendly — no `datetime.now()`):
     - `_TIER7A_DI_START_TS = '2000-01-01 00:00:00.000000'` (matches `_TIER2_DI_START_TS` convention from `generators/tier2_core.py:23`).
     - `_PREFERRED_CURRENCY_USE_CD = 'preferred'` (Layer 2 filter literal).
     - `_USD_CURRENCY_CD = 'USD'` (all agreements use USD per PRD §4.4 scale).
     - `_RATE_AGREEMENT_FEATURE_ROLE_CD = 'rate'` (matches `AGREEMENT_FEATURE_ROLE_CODES[2]`).
     - `_PRIMARY_AGREEMENT_FEATURE_ROLE_CD = 'primary'` (for balance-trajectory rows).
     - `_AGREEMENT_RATE_TYPE_CD = 'INTEREST'` — primary interest rate. `_BALANCE_CATEGORY_TYPE_CD = 'PRINCIPAL'`. `_TIME_PERIOD_YEAR_CD = 'YEAR'`.
     - `_AGREEMENT_METRIC_TYPE_CD = 'CURRENT_BALANCE'`. `_MONETARY_UOM_CD = 'USD'` (session verifies present in `Core_DB.UNIT_OF_MEASURE`; if not, falls back to the first row of that table and appends a `⚠️ Conflict` block to this spec).
     - `_REPRESENTATIVE_INDEX_RATES: Dict[str, Decimal]` with 5 entries — one Decimal per `Interest_Rate_Index_Cd`, 12dp precision; representative mid-2025 rates (`SOFR=Decimal('0.053300000000')`, `PRIME=Decimal('0.082500000000')`, `FEDFUNDS=Decimal('0.053300000000')`, `LIBOR=Decimal('0.050000000000')`, `EURIBOR=Decimal('0.038500000000')`). Session may adjust values by ≤0.5% absolute if they find a more accurate vintage.
     - `_VARIABLE_RATE_SPREAD_CD_BY_SUBTYPE: Dict[str, str]` mapping `Feature_Classification_Cd` → `Interest_Rate_Index_Cd` for the 4 Rate Feature rows (e.g. Original Loan Term → SOFR, Current Rate → PRIME, Origination Rate → FEDFUNDS, Minimum Payment → SOFR). Exact mapping is session-defined but must use only seeded index codes.
  3. Declare `_COLS_*` list-of-str module constants for every emitted DataFrame in **DDL declaration order** (see the DDL blocks cited in ## Reads from). DI columns are appended by `stamp_di()` — do NOT include them in `_COLS_*`. Example:
     ```python
     _COLS_AGREEMENT_STATUS = [
         'Agreement_Id', 'Agreement_Status_Scheme_Cd', 'Agreement_Status_Start_Dttm',
         'Agreement_Status_Cd', 'Agreement_Status_Reason_Cd', 'Agreement_Status_End_Dttm',
     ]
     ```
  4. **Guard** at the top of `generate()`: verify `ctx.agreements` is non-empty; verify every required Tier 0 / Tier 2 upstream table is present in `ctx.tables` (use an explicit `_REQUIRED_UPSTREAM_TABLES` tuple of 6 keys); verify the FEATURE-ID-for-rate lookup succeeds (`feature_df = ctx.tables['Core_DB.FEATURE']`; `rate_feature_row = feature_df[(feature_df.Feature_Subtype_Cd == RATE_FEATURE_SUBTYPE_CD) & (feature_df.Feature_Classification_Cd == ORIGINAL_LOAN_TERM_CLASSIFICATION_CD)]`; `assert len(rate_feature_row) >= 1`); verify the profitability MODEL lookup succeeds (`model_df = ctx.tables['Core_DB.ANALYTICAL_MODEL']`; `assert (model_df.Model_Type_Cd == PROFITABILITY_MODEL_TYPE_CD).any()`). Raise `RuntimeError(...)` on any failure — do NOT silently improvise a fallback.
  5. Build `AGREEMENT_STATUS` DataFrame — per-agreement loop produces exactly **6 current rows** (one per scheme in `AGREEMENT_STATUS_SCHEMES`). For each scheme, `Agreement_Status_Start_Dttm = ag.open_dttm`, `Agreement_Status_End_Dttm = None`. Scheme-specific code selection (exact literals):
     - `'Account Status'` → `'CLOSED'` if `ag.close_dttm is not None` else `'OPEN'`
     - `'Accrual Status'` → `'NON_ACCRUING'` if `ag.is_severely_delinquent` else `'ACCRUING'`
     - `'Default Status'` → `'DEFAULT'` if `ag.is_severely_delinquent` else `'CURRENT'`
     - `'Drawn Undrawn Status'` → `'DRAWN'` if `ag.balance_amt > 0` else `'UNDRAWN'`
     - `'Frozen Status'` → `'FROZEN'` if `ag.is_frozen` else `'NOT_FROZEN'` (**literal match** — see Rules §Frozen below)
     - `'Past Due Status'` → `'DPD_90'` if `ag.is_severely_delinquent` else `'DPD_30'` if `ag.is_delinquent` else `'CURRENT'`
     `Agreement_Status_Reason_Cd = 'DELINQUENCY'` for Past Due Status rows where is_delinquent; None otherwise. Additionally, for every `is_delinquent` agreement, emit **one historical Past Due Status row** (`Agreement_Status_Cd='CURRENT'`, `Agreement_Status_Start_Dttm = ag.open_dttm`, `Agreement_Status_End_Dttm = ag.open_dttm + timedelta(days=365)`, `Agreement_Status_Reason_Cd=None`) — this provides the "prior state" transition that Layer 2 joins expect. Total row count ≈ `6 × len(ctx.agreements) + sum(is_delinquent)`.
  6. Build `AGREEMENT_CURRENCY` DataFrame — one row per agreement with `Currency_Use_Cd='preferred'`, `Agreement_Currency_Cd='USD'`, `Agreement_Currency_Start_Dt=ag.open_dttm.date()`, `Agreement_Currency_End_Dt=None`. Row count = `len(ctx.agreements)`.
  7. Build `AGREEMENT_SCORE` DataFrame — one row per agreement. `Model_Id` = the first `ANALYTICAL_MODEL.Model_Id` with `Model_Type_Cd='profitability'`. `Model_Run_Id = 1` (single run; BIGINT). `Agreement_Score_Val` = string rendering of a Decimal probability (`f'{float(score):.4f}'`, e.g. `'0.7823'`), derived from a deterministic hash of `ag.agreement_id` so same seed → identical strings. Row count = `len(ctx.agreements)`.
  8. Build `AGREEMENT_FEATURE` DataFrame — two kinds of rows:
     - **Rate-feature row** (loan agreements only — those with `is_loan_term or is_mortgage or is_credit_card or is_loan_transaction`): `Feature_Id` = the rate-feature Feature_Id resolved in the guard, `Agreement_Feature_Role_Cd='rate'`, `Agreement_Feature_Start_Dttm=ag.open_dttm`, `Agreement_Feature_End_Dttm=None`, `Agreement_Feature_Rate=ag.interest_rate`, `Agreement_Feature_UOM_Cd='PERCENT'` (a rate uses a rate UOM; if 'PERCENT' absent from UNIT_OF_MEASURE the session escalates). `Interest_Rate_Index_Cd='SOFR'` (any seeded index is valid; SOFR chosen as the US default). `Currency_Cd='USD'`.
     - **Balance-trajectory rows** (DECLINING cohort only — those with `len(ag.monthly_balances) == 6`): 6 rows per DECLINING agreement, one per month in `month_snapshots(HISTORY_START, SIM_DATE)`. Each row uses a balance-classification Feature_Id (pick the first `Feature_Subtype_Cd='Balance Feature'` row — session resolves like the rate-feature lookup), `Agreement_Feature_Role_Cd='primary'`, `Agreement_Feature_Start_Dttm=datetime(month_start)`, `Agreement_Feature_End_Dttm=datetime(month_end, 23, 59, 59)`, `Agreement_Feature_Amt=ag.monthly_balances[month_idx]`, `Agreement_Feature_UOM_Cd='USD'`, `Currency_Cd='USD'`, `Interest_Rate_Index_Cd=None`, `Agreement_Feature_Rate=None`.
     Total row count = (loan-type agreements × 1) + (DECLINING agreements × 6).
  9. Build `AGREEMENT_METRIC` DataFrame — one row per agreement. `Agreement_Metric_Type_Cd='CURRENT_BALANCE'`, `Agreement_Metric_Start_Dttm=ag.open_dttm`, `Agreement_Metric_End_Dttm=None`, `Agreement_Metric_Time_Period_Cd=None`, `Agreement_Metric_Amt=ag.balance_amt`, `Agreement_Currency_Metric_Amt=ag.balance_amt`, `Currency_Cd='USD'`, `Unit_Of_Measure_Cd='USD'`. All other fields None. Row count = `len(ctx.agreements)`.
  10. Build `AGREEMENT_RATE` DataFrame — one row per agreement. `Rate_Type_Cd='INTEREST'`, `Balance_Category_Type_Cd='PRINCIPAL'`, `Agreement_Rate_Start_Dttm=ag.open_dttm`, `Agreement_Rate_End_Dttm=None`, `Agreement_Rate_Time_Period_Cd='YEAR'`, `Agreement_Rate=ag.interest_rate`. Row count = `len(ctx.agreements)`. **Mortgage vintage** (per `06 Part I1`) is already encoded in `ag.interest_rate` by `UniverseBuilder` — this step does NOT re-sample from the vintage table.
  11. Build `INTEREST_INDEX_RATE` DataFrame — **exactly 5 rows**. One per `Interest_Rate_Index_Cd` present in `ctx.tables['Core_DB.INTEREST_RATE_INDEX']`. `Index_Rate_Effective_Dttm=HISTORY_START` (DATE; one representative effective date per index). `Interest_Index_Rate` from `_REPRESENTATIVE_INDEX_RATES`. `Discount_Factor_Pct=None`, `Zero_Coupon_Rate=None`. Row count = 5.
  12. Build `VARIABLE_INTEREST_RATE_FEATURE` DataFrame — **exactly 4 rows** (one per row in FEATURE with `Feature_Subtype_Cd='Rate Feature'`). `Feature_Id` from the matched FEATURE rows. `Interest_Rate_Index_Cd` from `_VARIABLE_RATE_SPREAD_CD_BY_SUBTYPE` (each of the 4 Rate Feature Feature_Classification_Cd values maps to a seeded index). `Spread_Rate=Decimal('0.020000000000')` (200 bp). `Upper_Limit_Rate=Decimal('0.180000000000')` (18% cap). `Lower_Limit_Rate=Decimal('0.010000000000')` (1% floor). Row count = 4 (or the exact count of Rate Feature rows in FEATURE, whichever matches — session asserts the two match).
  13. Build `TERM_FEATURE` DataFrame — **exactly 4 rows** (one per row in FEATURE with `Feature_Subtype_Cd='Term Feature'`). `Feature_Id` from the matched FEATURE rows. Populate `From_Time_Period_Cd='MONTH'`, `To_Time_Period_Cd='MONTH'`, `From_Time_Period_Num='0'`, `To_Time_Period_Num='360'` (30-year mortgage span), `Term_Type_Cd='STANDARD'`. Other fields None. Row count = 4.
  14. Apply dtype conversions — cast every `*_Id` column to `Int64` (nullable BIGINT), every rate column to Python Decimal (pandas stores as `object`), every amount column as Decimal for consistency with Tier 2. Timestamps stay as `datetime`; dates as `date`.
  15. Stamp all **9** DataFrames via `self.stamp_di(df, start_ts=_TIER7A_DI_START_TS)`. Do NOT call `stamp_valid()` (all Core_DB; no CDM/PIM tables).
  16. Return a dict with exactly these 9 keys (no more, no fewer):
      ```
      {
        'Core_DB.AGREEMENT_STATUS', 'Core_DB.AGREEMENT_CURRENCY',
        'Core_DB.AGREEMENT_SCORE', 'Core_DB.AGREEMENT_FEATURE',
        'Core_DB.AGREEMENT_METRIC', 'Core_DB.AGREEMENT_RATE',
        'Core_DB.INTEREST_INDEX_RATE', 'Core_DB.VARIABLE_INTEREST_RATE_FEATURE',
        'Core_DB.TERM_FEATURE',
      }
      ```

**Do NOT produce** in this step:
- CSVs — writer is not invoked.
- Any Agreement sub-type chain table (`FINANCIAL_AGREEMENT`, `DEPOSIT_AGREEMENT`, `DEPOSIT_TERM_AGREEMENT`, `CREDIT_AGREEMENT`, `LOAN_AGREEMENT`, `LOAN_TERM_AGREEMENT`, `LOAN_TRANSACTION_AGREEMENT`, `MORTGAGE_AGREEMENT`, `CREDIT_CARD_AGREEMENT`) — those are Step 17 (Tier 7b).
- `CARD` — Step 17 (Tier 7b).
- `INTEREST_RATE_INDEX` — already seeded in Step 8 (do NOT regenerate).
- Wiring into `main.py` — orchestrator changes are Step 25.

## Tables generated (if applicable)

After `Tier7aAgreementCrosscut().generate(ctx)` runs, `ctx.tables` gains these 9 Core_DB keys:

| Table | Approx rows | Source | Literal-match / Layer 2 constraint |
|-------|------------:|--------|------------------------------------|
| `Core_DB.AGREEMENT_STATUS` | 6 × len(agreements) + #delinquent | per-scheme loop | All 6 schemes present per agreement (02 Step 3 #1); `'Frozen Status'/'FROZEN'/'Frozen'` literal for frozen agreements (02 Step 3 #13/#21) |
| `Core_DB.AGREEMENT_CURRENCY` | len(agreements) | 1-per-agreement | `Currency_Use_Cd='preferred'` exact literal per agreement (02 Step 3 #8) |
| `Core_DB.AGREEMENT_SCORE` | len(agreements) | 1-per-agreement | FK `Model_Id` → ANALYTICAL_MODEL row with `Model_Type_Cd='profitability'` (02 Step 3 #17) |
| `Core_DB.AGREEMENT_FEATURE` | #loan-type + 6 × #declining | per-agreement | Loan agreements have ≥1 row with `Feature_Id` where `FEATURE.Feature_Subtype_Cd='Rate Feature'` (02 Step 3 #6) |
| `Core_DB.AGREEMENT_METRIC` | len(agreements) | 1-per-agreement | No Layer 2 literal; used for aggregate metrics |
| `Core_DB.AGREEMENT_RATE` | len(agreements) | 1-per-agreement | `Agreement_Rate` = `ag.interest_rate` from UniverseBuilder (mortgage vintages applied there, 06 Part I1) |
| `Core_DB.INTEREST_INDEX_RATE` | 5 | Module constant table | PK `Interest_Rate_Index_Cd` FKs to the 5-row INTEREST_RATE_INDEX seed |
| `Core_DB.VARIABLE_INTEREST_RATE_FEATURE` | 4 | Module constant table | PK `Feature_Id` FKs to FEATURE rows with `Feature_Subtype_Cd='Rate Feature'`; `Interest_Rate_Index_Cd` FKs to seeded indices |
| `Core_DB.TERM_FEATURE` | 4 | Module constant table | PK `Feature_Id` FKs to FEATURE rows with `Feature_Subtype_Cd='Term Feature'` |

All 9 emitted DataFrames have the 5-column DI tail after `stamp_di()` with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. No `stamp_valid()` is called.

## ⚠️ Conflict handling protocol (conditional — only activates if triggered during implementation)

Three upstream gaps could be discovered during implementation. Do NOT silently improvise — escalate per Handoff Protocol §2 and add a `⚠️ Conflict` block to this spec:

1. **`Unit_Of_Measure_Cd` literal mismatch.** If `Core_DB.UNIT_OF_MEASURE` (from Step 8) does not contain `'USD'` or `'PERCENT'`, the session must either (a) fall back to the first row's `Unit_Of_Measure_Cd` and document which literal was used, or (b) update `seed_data/misc_types.py` to add the missing code with a one-line justification in the session notes.
2. **`TIME_PERIOD_TYPE` code `'YEAR'` missing.** `AGREEMENT_RATE.Agreement_Rate_Time_Period_Cd` is NOT NULL. If the seed (Step 8) lacks `'YEAR'`, either update the seed or use the first row's `Time_Period_Cd`.
3. **`FEATURE.Feature_Subtype_Cd='Balance Feature'` absent.** Step 10's `_FEATURE_TEMPLATES` currently includes 4 Balance Feature rows (indices 12–15 of `_FEATURE_TEMPLATES`). If a future refactor removes them, the DECLINING balance-trajectory rows have no valid `Feature_Id`. The session must then either re-add a Balance Feature to Tier 2 or fall back to the rate-feature ID (but this conflates two Layer 2 pivots and warrants a `⚠️ Conflict` block).

## Files to modify

No files modified. `config/settings.py`, `config/code_values.py`, `config/distributions.py`, `utils/*`, `registry/*`, `seed_data/*`, all existing `generators/*.py`, `output/*`, `main.py`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/*`, `CLAUDE.md` are all **NOT touched**.

If implementation discovers that `references/07_mvp-schema-reference.md` disagrees with this spec on any column name, type, or nullability (beyond those flagged above), escalate per Handoff Protocol §2 — update the upstream reference or add a new `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new dependencies. This step uses only `pandas`, `numpy`, `python-dateutil` (all in `requirements.txt` from Step 1) plus standard library + existing project modules.

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — every `*_Id` column in every output DataFrame is emitted as pandas `Int64Dtype()` (nullable BIGINT) or `int64` (when all non-null). The DDL in `07` declares `INTEGER` for `Agreement_Id`, `Feature_Id`, `Model_Id`, `Model_Run_Id`, `Overridden_Feature_Id`, `GL_Main_Account_Segment_Id` — the BIGINT rule wins per footnotes §3103/§3104/§3118.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — **n/a for Tier 7a**: no `Party_Id` column is emitted in this step. Every row is agreement-scoped.
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on all 9 DataFrames.
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts = HIGH_TS` stamped via `stamp_di()` default. `Valid_To_Dt` **n/a**: Tier 7a is all Core_DB; no `stamp_valid()`.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — **n/a**: Tier 7a is all Core_DB. Do NOT call `stamp_valid()`.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** — every DataFrame is constructed via `pd.DataFrame(rows, columns=_COLS_<TABLE>)` where `_COLS_<TABLE>` is the authoritative business-column list (DI columns appended by `stamp_di()` at the end, matching the Tier 2 pattern at `generators/tier2_core.py:736`).
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — **n/a**: not touched in this step (Step 22).
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — **n/a**: not touched in this step.
- **No ORMs, no database connections — pure pandas → CSV** — writer not invoked; generator returns DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — Tier 7a contains **zero random sampling**. Every value is deterministic: per-agreement flags drive status codes; per-agreement `interest_rate` comes from UniverseBuilder; `Agreement_Score_Val` uses a deterministic hash of `agreement_id`; representative index rates are module constants. Two back-to-back runs must produce byte-identical DataFrames without touching `ctx.rng`.

Step-specific rules (Tier 7a):

- **Frozen_Ind literal match (Layer 2 constraints #13/#21).** For every agreement with `ag.is_frozen == True`, the `'Frozen Status'` scheme row MUST have `Agreement_Status_Cd = 'FROZEN'` (exact uppercase). The literal is exported as `FROZEN_STATUS_ROW['Agreement_Status_Cd']` from `config/code_values.py` — the session imports and uses that constant, not a hardcoded string. For non-frozen agreements, use `'NOT_FROZEN'` — this is the value seeded in `seed_data/status_types.py` for the non-frozen path.

- **Six-scheme coverage (Layer 2 constraint #1).** Every agreement emits exactly 6 current-status rows, one per scheme in `AGREEMENT_STATUS_SCHEMES`. The scheme list is the authoritative tuple from `config/code_values.py:9` — iterate over it directly. Do NOT hardcode a local list.

- **Agreement_Status_Cd uses exact literals from seeded AGREEMENT_STATUS_TYPE.** Every `(Scheme, Code)` pair emitted by this step MUST appear as a row in `ctx.tables['Core_DB.AGREEMENT_STATUS_TYPE']`. The DoD FK-coverage check enforces this. Valid codes per scheme (from `seed_data/status_types.py`):
  - `Account Status`: `OPEN | CLOSED | DORMANT | WRITE_OFF`
  - `Accrual Status`: `ACCRUING | NON_ACCRUING`
  - `Default Status`: `CURRENT | DEFAULT | CURED`
  - `Drawn Undrawn Status`: `DRAWN | UNDRAWN | PARTIAL`
  - `Frozen Status`: `FROZEN | NOT_FROZEN`
  - `Past Due Status`: `CURRENT | DPD_30 | DPD_60 | DPD_90 | DPD_120`

- **Preferred currency literal (Layer 2 constraint #8).** `Currency_Use_Cd='preferred'` is the exact literal. Use `CURRENCY_USE_CODES[0]` from `config/code_values.py:20` to avoid divergence; never hardcode the string at the call site.

- **Rate Feature FK (Layer 2 constraint #6).** The Feature_Id used for the loan rate-feature row is the first row in `ctx.tables['Core_DB.FEATURE']` with BOTH `Feature_Subtype_Cd=RATE_FEATURE_SUBTYPE_CD` AND `Feature_Classification_Cd=ORIGINAL_LOAN_TERM_CLASSIFICATION_CD` (satisfies both 02 Step 3 item #6 and item #18 simultaneously). This combined row is guaranteed by Step 10 (`generators/tier2_core.py:266`); the session fails fast if absent.

- **Profitability score FK (Layer 2 constraint #17).** `AGREEMENT_SCORE.Model_Id` = first `ANALYTICAL_MODEL.Model_Id` where `Model_Type_Cd=PROFITABILITY_MODEL_TYPE_CD`. Step 10 seeds two such rows (the "Profitability Scoring Model" and the "Customer Profitability Model" at `generators/tier2_core.py:137–172`); either is acceptable.

- **Agreement_Score_Val is a deterministic probability string.** Format: `f'{float(score):.4f}'` (4 decimal places, e.g. `'0.7823'`). Derive `score` from a **deterministic** function of `agreement_id`: `score = ((agreement_id * 2654435761) % 10_000) / 10_000` (Knuth's multiplicative hash → uniform [0,1)). Do NOT use `ctx.rng` — same `agreement_id` must always produce the same score string across runs.

- **DECLINING balance-trajectory rows span calendar months.** `Agreement_Feature_Start_Dttm` = `datetime(month_start.year, month_start.month, month_start.day, 0, 0, 0)`; `Agreement_Feature_End_Dttm` = `datetime(month_end.year, month_end.month, month_end.day, 23, 59, 59)`. Use `month_snapshots(HISTORY_START, SIM_DATE)` from `utils/date_utils.py:39` — returns exactly 6 tuples. Match index-to-balance: `monthly_balances[i]` corresponds to `month_snapshots[i]`.

- **`ag.interest_rate` is authoritative for AGREEMENT_RATE.Agreement_Rate and loan AGREEMENT_FEATURE.Agreement_Feature_Rate.** Do NOT re-sample from mortgage vintages (`06 Part I1`) — UniverseBuilder already applied the vintage lookup at Step 4. Tier 7a reads `ag.interest_rate` verbatim.

- **`INTEREST_INDEX_RATE` has exactly 5 rows.** One per `Interest_Rate_Index_Cd` in the seeded `INTEREST_RATE_INDEX` table. Do NOT generate daily/monthly history; the PK is `(Interest_Rate_Index_Cd, Index_Rate_Effective_Dttm)` but only the representative effective date `HISTORY_START` is emitted.

- **`VARIABLE_INTEREST_RATE_FEATURE` count = Rate-Feature row count.** Sessions must assert `len(VARIABLE_INTEREST_RATE_FEATURE) == len(FEATURE[Feature_Subtype_Cd='Rate Feature'])`. Step 10 currently produces 4 such rows; a future change breaking the count should fail this check.

- **`TERM_FEATURE` count = Term-Feature row count.** Same pattern, Step 10 currently produces 4 such rows.

- **No side effects on import.** `import generators.tier7a_agreement_crosscut` must not construct any DataFrames, call `generate()`, or read any file. Enforced by the "no import-time DataFrames" check in Definition of done.

- **No Faker.** `faker` is seeded in UniverseBuilder and used only there. Tier 7a uses only numeric/string literals and dates derived from `ag` fields. Enforced by a grep check in Definition of done.

- **No ctx.rng access.** Tier 7a performs zero random sampling. A grep for `ctx.rng` inside the generator must return zero matches.

- **Escalation over improvisation.** If `07` has an ambiguity beyond those flagged in the Conflict handling protocol above (column name differs, nullability unclear, DDL type surprising), stop and add a new `⚠️ Conflict` block to this spec. Do NOT invent columns.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is CWD and `python` resolves to the project's Python 3.12 environment. Each check uses a fresh ctx built via UniverseBuilder + Tier 0 + Tier 1 + Tier 2 before invoking Tier 7a.

### Module-import and API contract

- [ ] `python -c "import generators.tier7a_agreement_crosscut"` exits 0.
- [ ] Generator class inherits from `BaseGenerator` and defines `generate(ctx)`. Run:
  ```bash
  python -c "
  from generators.tier7a_agreement_crosscut import Tier7aAgreementCrosscut
  from generators.base import BaseGenerator
  import inspect
  assert issubclass(Tier7aAgreementCrosscut, BaseGenerator)
  sig = inspect.signature(Tier7aAgreementCrosscut.generate)
  assert 'ctx' in sig.parameters
  print('class contract OK')
  "
  ```

### Tables produced

- [ ] `Tier7aAgreementCrosscut().generate(ctx)` returns **exactly these 9 Core_DB keys** — no more, no fewer. Run the canonical ctx-bootstrap helper (may be DRY'd into a temp helper the session reuses across checks):
  ```bash
  python -c "
  import numpy as np
  from config.settings import SEED
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  from generators.tier7a_agreement_crosscut import Tier7aAgreementCrosscut
  import config.settings as _s
  ctx = UniverseBuilder().build(_s, np.random.default_rng(SEED))
  for t in (Tier0Lookups(), Tier1Geography(), Tier2Core()):
      ctx.tables.update(t.generate(ctx))
  out = Tier7aAgreementCrosscut().generate(ctx)
  expected = {
      'Core_DB.AGREEMENT_STATUS','Core_DB.AGREEMENT_CURRENCY','Core_DB.AGREEMENT_SCORE',
      'Core_DB.AGREEMENT_FEATURE','Core_DB.AGREEMENT_METRIC','Core_DB.AGREEMENT_RATE',
      'Core_DB.INTEREST_INDEX_RATE','Core_DB.VARIABLE_INTEREST_RATE_FEATURE',
      'Core_DB.TERM_FEATURE',
  }
  assert set(out.keys()) == expected, set(out.keys()) ^ expected
  assert len(out) == 9
  print(f'Tier7a produced {len(out)} tables (expected 9)')
  "
  ```

### Row counts

- [ ] Row counts match the per-table contract. Run (after bootstrap):
  ```bash
  python -c "
  # ... ctx bootstrap + out = Tier7a output ...
  n_ag = len(ctx.agreements)
  n_delinq = sum(1 for ag in ctx.agreements if ag.is_delinquent)
  n_decl = sum(1 for ag in ctx.agreements if len(ag.monthly_balances) == 6)
  n_loan = sum(1 for ag in ctx.agreements if ag.is_loan_term or ag.is_mortgage or ag.is_credit_card or ag.is_loan_transaction)
  assert len(out['Core_DB.AGREEMENT_STATUS']) == 6 * n_ag + n_delinq, (len(out['Core_DB.AGREEMENT_STATUS']), 6*n_ag+n_delinq)
  assert len(out['Core_DB.AGREEMENT_CURRENCY']) == n_ag
  assert len(out['Core_DB.AGREEMENT_SCORE']) == n_ag
  assert len(out['Core_DB.AGREEMENT_METRIC']) == n_ag
  assert len(out['Core_DB.AGREEMENT_RATE']) == n_ag
  assert len(out['Core_DB.AGREEMENT_FEATURE']) == n_loan + 6 * n_decl, (len(out['Core_DB.AGREEMENT_FEATURE']), n_loan + 6 * n_decl)
  assert len(out['Core_DB.INTEREST_INDEX_RATE']) == 5
  assert len(out['Core_DB.VARIABLE_INTEREST_RATE_FEATURE']) == 4
  assert len(out['Core_DB.TERM_FEATURE']) == 4
  print('row counts OK')
  "
  ```

### Six-scheme coverage per agreement (Layer 2 #1)

- [ ] Every Agreement_Id has exactly 6 current AGREEMENT_STATUS rows, one per scheme in AGREEMENT_STATUS_SCHEMES. Run:
  ```bash
  python -c "
  from config.code_values import AGREEMENT_STATUS_SCHEMES
  st = out['Core_DB.AGREEMENT_STATUS']
  current = st[st.Agreement_Status_End_Dttm.isna()]
  per_ag = current.groupby('Agreement_Id')['Agreement_Status_Scheme_Cd'].apply(set)
  target = set(AGREEMENT_STATUS_SCHEMES)
  assert len(target) == 6
  assert (per_ag == target).all(), 'some agreement missing a scheme'
  print('six-scheme coverage OK')
  "
  ```

### Frozen_Ind literal match (Layer 2 #13 / #21)

- [ ] For every `ag.is_frozen=True`, the `Frozen Status` row uses `Agreement_Status_Cd='FROZEN'`. Run:
  ```bash
  python -c "
  st = out['Core_DB.AGREEMENT_STATUS']
  frozen_ag_ids = {ag.agreement_id for ag in ctx.agreements if ag.is_frozen}
  current = st[st.Agreement_Status_End_Dttm.isna() & (st.Agreement_Status_Scheme_Cd == 'Frozen Status')]
  for _, row in current.iterrows():
      expected = 'FROZEN' if row.Agreement_Id in frozen_ag_ids else 'NOT_FROZEN'
      assert row.Agreement_Status_Cd == expected, f'agr {row.Agreement_Id}: expected {expected}, got {row.Agreement_Status_Cd}'
  # Literal 'FROZEN' must appear in AGREEMENT_STATUS_TYPE
  typ = ctx.tables['Core_DB.AGREEMENT_STATUS_TYPE']
  mask = (typ.Agreement_Status_Scheme_Cd == 'Frozen Status') & (typ.Agreement_Status_Cd == 'FROZEN')
  assert mask.any(), 'FROZEN seed row missing from AGREEMENT_STATUS_TYPE'
  print('Frozen literal match OK')
  "
  ```

### Preferred currency per agreement (Layer 2 #8)

- [ ] Every agreement has exactly one AGREEMENT_CURRENCY row with `Currency_Use_Cd='preferred'`. Run:
  ```bash
  python -c "
  ac = out['Core_DB.AGREEMENT_CURRENCY']
  preferred = ac[ac.Currency_Use_Cd == 'preferred']
  counts = preferred.groupby('Agreement_Id').size()
  assert (counts == 1).all(), 'some agreement does not have exactly one preferred row'
  assert set(preferred.Agreement_Id) == {ag.agreement_id for ag in ctx.agreements}
  assert (ac.Agreement_Currency_Cd == 'USD').all()
  print('preferred currency OK')
  "
  ```

### Rate Feature row per loan agreement (Layer 2 #6)

- [ ] Every loan-type agreement (`is_loan_term or is_mortgage or is_credit_card or is_loan_transaction`) has at least one AGREEMENT_FEATURE row with Feature_Id that resolves to a FEATURE row where `Feature_Subtype_Cd='Rate Feature'`. Run:
  ```bash
  python -c "
  af = out['Core_DB.AGREEMENT_FEATURE']
  feat = ctx.tables['Core_DB.FEATURE']
  rate_feat_ids = set(feat[feat.Feature_Subtype_Cd == 'Rate Feature'].Feature_Id)
  loan_ag_ids = {ag.agreement_id for ag in ctx.agreements if (ag.is_loan_term or ag.is_mortgage or ag.is_credit_card or ag.is_loan_transaction)}
  rate_rows = af[af.Feature_Id.isin(rate_feat_ids)]
  covered = set(rate_rows.Agreement_Id)
  missing = loan_ag_ids - covered
  assert not missing, f'{len(missing)} loan agreements missing rate feature'
  print(f'rate feature coverage OK ({len(loan_ag_ids)} loans)')
  "
  ```

### Profitability AGREEMENT_SCORE (Layer 2 #17)

- [ ] Every agreement has exactly one AGREEMENT_SCORE row, with `Model_Id` resolving to an ANALYTICAL_MODEL row with `Model_Type_Cd='profitability'`. `Agreement_Score_Val` is a 4-decimal probability string in `[0,1)`. Run:
  ```bash
  python -c "
  asc = out['Core_DB.AGREEMENT_SCORE']
  am = ctx.tables['Core_DB.ANALYTICAL_MODEL']
  prof_ids = set(am[am.Model_Type_Cd == 'profitability'].Model_Id)
  assert set(asc.Model_Id) <= prof_ids
  assert set(asc.Agreement_Id) == {ag.agreement_id for ag in ctx.agreements}
  assert asc.groupby('Agreement_Id').size().eq(1).all()
  # Score val format
  import re
  pat = re.compile(r'^0\.[0-9]{4}$')
  assert asc.Agreement_Score_Val.str.match(pat).all(), 'bad score format'
  print('AGREEMENT_SCORE profitability FK OK')
  "
  ```

### DECLINING balance trajectory

- [ ] Every DECLINING-cohort agreement has exactly 6 AGREEMENT_FEATURE rows spanning the 6 calendar months. Run:
  ```bash
  python -c "
  from utils.date_utils import month_snapshots
  from config.settings import HISTORY_START, SIM_DATE
  af = out['Core_DB.AGREEMENT_FEATURE']
  decl_ag_ids = {ag.agreement_id for ag in ctx.agreements if len(ag.monthly_balances) == 6}
  # Monthly rows are identifiable by Agreement_Feature_Role_Cd='primary' and Agreement_Feature_Amt not null
  monthly = af[(af.Agreement_Feature_Role_Cd == 'primary') & af.Agreement_Id.isin(decl_ag_ids)]
  counts = monthly.groupby('Agreement_Id').size()
  assert (counts == 6).all(), 'DECLINING agreement not getting 6 monthly rows'
  snaps = month_snapshots(HISTORY_START, SIM_DATE)
  assert len(snaps) == 6
  # Distinct start-months across the 6 rows per agreement
  for ag_id in list(decl_ag_ids)[:5]:
      months = sorted(monthly[monthly.Agreement_Id == ag_id].Agreement_Feature_Start_Dttm.dt.month.tolist())
      expected = sorted([s[0].month for s in snaps])
      assert months == expected, f'agr {ag_id}: month set mismatch {months} vs {expected}'
  print('DECLINING 6-month trajectory OK')
  "
  ```

### AGREEMENT_RATE uses ag.interest_rate

- [ ] Every agreement's `AGREEMENT_RATE.Agreement_Rate` equals its AgreementProfile `ag.interest_rate` (within Decimal precision). Run:
  ```bash
  python -c "
  from decimal import Decimal
  ar = out['Core_DB.AGREEMENT_RATE']
  ag_by_id = {ag.agreement_id: ag for ag in ctx.agreements}
  for _, row in ar.iterrows():
      exp = ag_by_id[row.Agreement_Id].interest_rate
      got = row.Agreement_Rate
      assert Decimal(str(got)) == Decimal(str(exp)), f'agr {row.Agreement_Id}: {got} != {exp}'
  # Time period and rate type literals
  assert (ar.Rate_Type_Cd == 'INTEREST').all()
  assert (ar.Balance_Category_Type_Cd == 'PRINCIPAL').all()
  assert (ar.Agreement_Rate_Time_Period_Cd == 'YEAR').all()
  print('AGREEMENT_RATE rate + literals OK')
  "
  ```

### INTEREST_INDEX_RATE / VARIABLE_INTEREST_RATE_FEATURE / TERM_FEATURE

- [ ] `INTEREST_INDEX_RATE` has exactly 5 rows, one per seeded index. Run:
  ```bash
  python -c "
  iir = out['Core_DB.INTEREST_INDEX_RATE']
  idx = ctx.tables['Core_DB.INTEREST_RATE_INDEX']
  assert set(iir.Interest_Rate_Index_Cd) == set(idx.Interest_Rate_Index_Cd)
  assert iir.Interest_Rate_Index_Cd.is_unique
  assert iir.Interest_Index_Rate.notna().all()
  print('INTEREST_INDEX_RATE OK')
  "
  ```
- [ ] `VARIABLE_INTEREST_RATE_FEATURE.Feature_Id` FK-resolves to FEATURE rows with `Feature_Subtype_Cd='Rate Feature'`; `Interest_Rate_Index_Cd` FK-resolves to INTEREST_RATE_INDEX. Run:
  ```bash
  python -c "
  vr = out['Core_DB.VARIABLE_INTEREST_RATE_FEATURE']
  feat = ctx.tables['Core_DB.FEATURE']
  idx = ctx.tables['Core_DB.INTEREST_RATE_INDEX']
  rate_ids = set(feat[feat.Feature_Subtype_Cd == 'Rate Feature'].Feature_Id)
  assert set(vr.Feature_Id) <= rate_ids
  assert len(vr) == len(rate_ids)
  assert set(vr.Interest_Rate_Index_Cd) <= set(idx.Interest_Rate_Index_Cd)
  print('VARIABLE_INTEREST_RATE_FEATURE FKs OK')
  "
  ```
- [ ] `TERM_FEATURE.Feature_Id` FK-resolves to FEATURE rows with `Feature_Subtype_Cd='Term Feature'`. Run:
  ```bash
  python -c "
  tf = out['Core_DB.TERM_FEATURE']
  feat = ctx.tables['Core_DB.FEATURE']
  term_ids = set(feat[feat.Feature_Subtype_Cd == 'Term Feature'].Feature_Id)
  assert set(tf.Feature_Id) <= term_ids
  assert len(tf) == len(term_ids)
  print('TERM_FEATURE FKs OK')
  "
  ```

### FK resolution to upstream tiers

- [ ] Every `Agreement_Id` in every Tier 7a table resolves to `Core_DB.AGREEMENT.Agreement_Id`. Run:
  ```bash
  python -c "
  ag_ids = set(ctx.tables['Core_DB.AGREEMENT'].Agreement_Id)
  tables_with_agr_id = [
      'Core_DB.AGREEMENT_STATUS','Core_DB.AGREEMENT_CURRENCY','Core_DB.AGREEMENT_SCORE',
      'Core_DB.AGREEMENT_FEATURE','Core_DB.AGREEMENT_METRIC','Core_DB.AGREEMENT_RATE',
  ]
  for key in tables_with_agr_id:
      df = out[key]
      orphans = set(df.Agreement_Id) - ag_ids
      assert not orphans, f'{key}: {len(orphans)} orphan Agreement_Ids'
  print('Agreement_Id FK coverage OK')
  "
  ```
- [ ] Every `(Scheme_Cd, Status_Cd)` pair in AGREEMENT_STATUS exists as a row in AGREEMENT_STATUS_TYPE. Run:
  ```bash
  python -c "
  st = out['Core_DB.AGREEMENT_STATUS']
  typ = ctx.tables['Core_DB.AGREEMENT_STATUS_TYPE']
  valid_pairs = set(zip(typ.Agreement_Status_Scheme_Cd, typ.Agreement_Status_Cd))
  emitted_pairs = set(zip(st.Agreement_Status_Scheme_Cd, st.Agreement_Status_Cd))
  orphans = emitted_pairs - valid_pairs
  assert not orphans, f'orphan (Scheme, Code) pairs: {orphans}'
  print('AGREEMENT_STATUS_TYPE FK coverage OK')
  "
  ```
- [ ] Every `Feature_Id` in AGREEMENT_FEATURE / TERM_FEATURE / VARIABLE_INTEREST_RATE_FEATURE resolves to `Core_DB.FEATURE.Feature_Id`. Run:
  ```bash
  python -c "
  feat_ids = set(ctx.tables['Core_DB.FEATURE'].Feature_Id)
  for key in ('Core_DB.AGREEMENT_FEATURE','Core_DB.TERM_FEATURE','Core_DB.VARIABLE_INTEREST_RATE_FEATURE'):
      df = out[key]
      orphans = set(df.Feature_Id) - feat_ids
      assert not orphans, f'{key}: Feature_Id orphans: {orphans}'
  print('Feature_Id FK coverage OK')
  "
  ```

### Agreement_Status_Start_Dttm temporal sanity

- [ ] Every current-status row has `Agreement_Status_Start_Dttm = ag.open_dttm` (full coverage, vectorized). Run:
  ```bash
  python -c "
  st = out['Core_DB.AGREEMENT_STATUS']
  current = st[st.Agreement_Status_End_Dttm.isna()]
  ag_open = {ag.agreement_id: ag.open_dttm for ag in ctx.agreements}
  expected = current.Agreement_Id.map(ag_open)
  assert (current.Agreement_Status_Start_Dttm == expected).all(), 'Agreement_Status_Start_Dttm drift on one or more rows'
  print(f'Agreement_Status_Start_Dttm OK (full coverage, {len(current)} rows)')
  "
  ```

### BIGINT enforcement (PRD §7.1)

- [ ] Every `*_Id` column in every produced DataFrame is `Int64` or `int64` dtype. Run:
  ```bash
  python -c "
  bad = []
  for key, df in out.items():
      for c in df.columns:
          if c.endswith('_Id'):
              if str(df[c].dtype) not in ('Int64','int64'):
                  bad.append(f'{key}.{c}: {df[c].dtype}')
  assert not bad, bad
  print('all *_Id columns BIGINT')
  "
  ```

### DI stamping

- [ ] Every produced DataFrame has the 5-column DI tail with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. Run:
  ```bash
  python -c "
  from config.settings import HIGH_TS
  from utils.di_columns import DI_COLUMN_ORDER
  for key, df in out.items():
      tail = list(df.columns[-5:])
      assert tail == list(DI_COLUMN_ORDER), f'{key}: DI tail {tail}'
      assert (df.di_end_ts == HIGH_TS).all(), f'{key}: di_end_ts drift'
      assert (df.di_rec_deleted_Ind == 'N').all(), f'{key}: di_rec_deleted_Ind drift'
  print('DI stamping OK across all 9 tables')
  "
  ```
- [ ] No DataFrame has `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` columns (Core_DB does not stamp them). Run:
  ```bash
  python -c "
  for key, df in out.items():
      banned = {'Valid_From_Dt','Valid_To_Dt','Del_Ind'}
      present = banned & set(df.columns)
      assert not present, f'{key} has CDM/PIM columns: {present}'
  print('no Valid/Del_Ind on Core_DB tables')
  "
  ```

### Writer compatibility

- [ ] After stamping, every table passes `output.writer._reorder_to_ddl()`. Run:
  ```bash
  python -c "
  from output.writer import _reorder_to_ddl
  for key, df in out.items():
      try: _reorder_to_ddl(df, key)
      except Exception as e: raise SystemExit(f'{key}: {e}')
  print(f'{len(out)} tables pass _reorder_to_ddl')
  "
  ```

### Prerequisite guard

- [ ] `Tier7aAgreementCrosscut.generate()` raises `RuntimeError` when an upstream prerequisite is missing. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier7a_agreement_crosscut import Tier7aAgreementCrosscut
  class Ctx:
      customers = []
      agreements = []
      ids = IdFactory(ID_RANGES)
      rng = np.random.default_rng(42)
      tables = {}
  try:
      Tier7aAgreementCrosscut().generate(Ctx())
      raise AssertionError('should have raised RuntimeError')
  except RuntimeError as e:
      assert 'AGREEMENT' in str(e) or 'FEATURE' in str(e) or 'ANALYTICAL_MODEL' in str(e) or 'Tier' in str(e)
  print('Tier7a prerequisite guard OK')
  "
  ```

### Reproducibility

- [ ] Two back-to-back runs produce byte-identical DataFrames. Run:
  ```bash
  python -c "
  import numpy as np
  import config.settings as _s
  from config.settings import SEED
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  from generators.tier7a_agreement_crosscut import Tier7aAgreementCrosscut
  def run():
      ctx = UniverseBuilder().build(_s, np.random.default_rng(SEED))
      for t in (Tier0Lookups(), Tier1Geography(), Tier2Core()):
          ctx.tables.update(t.generate(ctx))
      return Tier7aAgreementCrosscut().generate(ctx)
  a, b = run(), run()
  assert set(a) == set(b)
  for k in a:
      assert a[k].equals(b[k]), f'{k} differs between runs'
  print('reproducibility OK')
  "
  ```

### No randomness / side-effect imports

- [ ] Generator module does not import `faker`. Run:
  ```bash
  python -c "
  import re, pathlib
  pat = re.compile(r'^\s*(?:import|from)\s+faker\b')
  p = 'generators/tier7a_agreement_crosscut.py'
  bad = [f'{p}:{i}: {line}' for i, line in enumerate(pathlib.Path(p).read_text().splitlines(), 1) if pat.match(line)]
  assert not bad, bad
  print('no faker import')
  "
  ```
- [ ] Generator module does not touch `ctx.rng`. Run:
  ```bash
  python -c "
  import pathlib
  src = pathlib.Path('generators/tier7a_agreement_crosscut.py').read_text()
  assert 'ctx.rng' not in src, 'Tier 7a must be deterministic — no ctx.rng access'
  print('no ctx.rng access')
  "
  ```
- [ ] Importing the module does not construct DataFrames. Run:
  ```bash
  python -c "
  import importlib, sys, pandas as pd
  calls = {'n': 0}
  _orig = pd.DataFrame
  def _wrap(*a, **k):
      calls['n'] += 1; return _orig(*a, **k)
  pd.DataFrame = _wrap
  sys.modules.pop('generators.tier7a_agreement_crosscut', None)
  importlib.import_module('generators.tier7a_agreement_crosscut')
  pd.DataFrame = _orig
  assert calls['n'] == 0, f'{calls[\"n\"]} DataFrames built at import time'
  print('no import-time DataFrames')
  "
  ```

### Universal checks

- [ ] `git status --porcelain` shows only: `generators/tier7a_agreement_crosscut.py` (new) plus this spec file at `.claude/specs/step-16-tier7a-agreement-cross-cutting.md` (already on branch). No stray files (no `__pycache__` in stage, no output CSVs, no edits under `config/`, `utils/`, `registry/`, `output/`, `references/`, `seed_data/`, other `generators/*.py`). Run:
  ```bash
  git status --porcelain
  ```
- [ ] All new files pass `python -c "import <module>"` — covered by the first Module-import check.
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — covered by the BIGINT dtype check above. **n/a for the CSV-on-disk variant**: this step produces no CSVs; writer is not invoked.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: not touched in this step (Step 22).
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSV output; writer not invoked. Tier 7a does not touch the GEOSPATIAL skip list.

## Handoff notes

<!-- Implementation session fills this in at end — see implementation-steps.md Handoff Protocol. -->

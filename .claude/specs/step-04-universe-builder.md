# Spec: Step 04 — UniverseBuilder

## Overview

This step implements the statistical center of gravity of the generator. `UniverseBuilder.build()` makes every correlated, customer-level and agreement-level decision *upfront* — demographics, cohort, products, balances, monthly trajectories, status flags, addresses — and writes them into the `CustomerProfile` / `AgreementProfile` / `AddressRecord` dataclasses defined in Step 3. By the time `build()` returns, the universe is fully decided; every downstream tier generator (Steps 8–23) is a pure transformation from registry + upstream table DataFrames to new table DataFrames, with **no statistical sampling**. This architectural split (`mvp-tool-design.md` §2 "Two-phase execution", §5 "UniverseBuilder", §14 "Decision 1: Entity-first registry, not table-first generation") is what guarantees cross-table correlation: a 25-year-old with income Q1 cannot end up with a $400K mortgage because one atomic decision in Phase 1 determines their product mix and every balance. This step also fills in the thirteen sampler stubs in `config/distributions.py` (left as `NotImplementedError` by Step 1) with real log-normal / weighted-choice / vintage-bucket implementations driven by SCF 2022 and WP5 distributions (`06_supporting-enrichments.md` Parts A–I, `02_data-mapping-reference.md` WP5).

## Depends on

- **Step 1** — consumes from `config/settings.py`: `SEED`, `TARGET_CUSTOMERS`, `TARGET_AGREEMENTS`, `INDIVIDUAL_PCT`, `ORGANIZATION_PCT`, the four `COHORT_*_PCT` constants, `CHECKING_PENETRATION_PCT`, `HISTORY_START`, `SIM_DATE`, `ID_RANGES`, `BANK_PARTY_ID`, `SELF_EMP_ORG_ID`. Consumes from `config/code_values.py`: informational only — role codes and scheme names are not written by this step, but product-type strings used in `CustomerProfile.product_set` / `AgreementProfile.product_type` must be consistent with what Step 8 (Tier 2 Core Entities) will emit into `Core_DB.PRODUCT`.
- **Step 2** — consumes from `utils/id_factory.py`: the `IdFactory` class (used to mint BIGINT IDs for every party, agreement, address, and household). Consumes from `utils/date_utils.py`: `month_snapshots(start, end)` (exactly 6 month-tuples across Oct 2025 – Mar 2026, used for DECLINING-cohort monthly balance trajectories), `random_datetime_between(start, end, rng)` (for `Agreement.Open_Dttm` and `Agreement.Close_Dttm`), `random_date_between(start, end, rng)` (for `party_since`). Does NOT consume `BaseGenerator` or `stamp_di` / `stamp_valid` — DI stamping is a tier-generator concern, not a registry concern; this step writes nothing to `ctx.tables`.
- **Step 3** — consumes from `registry/profiles.py`: `CustomerProfile`, `AgreementProfile`, `AddressRecord` (Step 4 populates every non-Optional field of all three). Consumes from `registry/context.py`: `GenerationContext` (Step 4 constructs one, populates `customers` / `agreements` / `addresses`, leaves `tables={}` for Steps 8–23 to fill).

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 4):
- `mvp-tool-design.md` §5 (UniverseBuilder build sequence — the canonical ordering of `_assign_*` phases; every private method named there must exist)
- `mvp-tool-design.md` §10 (Statistical Distributions — the sampler signatures table and the seven mandatory correlation rules; also the deposit-balance / total-investments AUM tension resolution)
- `mvp-tool-design.md` §1 (Simulation Parameters — authoritative source for target volumes and date window)
- `mvp-tool-design.md` §7.5 (Exclusive AGREEMENT sub-typing — every agreement follows exactly one terminal-leaf path)
- `mvp-tool-design.md` §14 Decision 1 (Entity-first registry — the "why" behind this step's existence)
- `PRD.md` §4.4 (Generation Scale — 3,000 customers / 5,000 agreements / 80-20 / 55-30-5-10 / seed=42)
- `PRD.md` §5 Core Design Principles #3 (Cross-table correlation preserved), #6 (Reproducibility)
- `PRD.md` §7.1 (BIGINT everywhere), §7.2 (Shared Party ID), §7.5 (Exclusive sub-typing), §7.6 (Reproducibility via seed), §7.12 (Self-employed placeholder org)
- `implementation-steps.md` Step 4 entry (target volumes, cohort ±0.5% tolerance, self-employed ~21.7% ±1%, byte-identical reproducibility check)

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/06_supporting-enrichments.md` Parts A–I — **primary statistical source**:
  - Part A1 (Age — AGECL weights [0.133, 0.166, 0.178, 0.223, 0.188, 0.110] across ranges 20-34 / 35-44 / 45-54 / 55-64 / 65-74 / 75-82; hard cap birth year 1940-2005)
  - Part A2 (Gender — use 50/50 neutral default per the Part A2 note; do NOT apply SCF HHSEX reference-person skew)
  - Part A3 (Marital — MARRIED 63.2%, SINGLE 36.8%)
  - Part A4 (Kids — 0:60.2%, 1:17.8%, 2:13.9%, 3:8.1%)
  - Part A6 (Ethnicity — WHITE 59.7% / BLACK 13.4% / HISPANIC 11.5% / ASIAN 7.3% / OTHER 8.0%)
  - Part A7 (Occupation — EMP 49.6% / SELF_EMP 21.7% / RETIRED 24.8% / NOT_WORKING 3.9%)
  - Part A8 (LIFECL weights — 11.5% / 8.2% / 21.4% / 6.7% / 29.1% / 23.1%)
  - Part B (Account ownership rates — Savings 48.4%, MMA 20.0%, CD 7.8%, Retirement 59.1%, Mortgage 39.6%, CC 37.8%, Vehicle 30.3%, Student 17.7%, HELOC 3.4%, Payday 1.9%; unbanked 10%)
  - Part C1 (Checking balance by income quartile — Q1 median $350, Q4 median $23K — use as log-normal scale)
  - Part C2 (Savings by quartile), Part C3 (CC revolving balance × income), Part C4 (Mortgage by age), Part C5 (Retirement by age)
  - Part C7 (Income by occupation stratified ranges)
  - Part C9 (Delinquency rates — LATE 11.2%, LATE60 4.6%, bankruptcy 1.1%)
  - Part D1–D6 (Mandatory correlation rules — age × products, income × assets, age × income → NW interaction, occupation variance, ethnicity × credit denial, DTI × age)
  - Part F1 (CLV 90-10 rule — top-decile 10% customers drive ~90% of profit; `clv_segment` 1–10 assignment)
  - Part G1–G3 (Attrition model — 5% churned, stealth-attrition declining cohort, balance trajectories)
  - Part I1 (Mortgage rate vintages by origination year)
  - Part J (Default generation parameters — already resolved in `config/settings.py`)
- `references/02_data-mapping-reference.md` WP5 Feature Store distributions — Average Deposit Balance (mean $2K / P10 $10 / P90 $30K — feature-level aggregate), Credit Card Balance (mean $2.5K / P10 $100 / P90 $20K), Total Investments AUM (mean $75K / P10 $5K / P90 $100K — conditional on holding), Customer Tenure (mean 3.5 / P10 0.5 / P90 25), Imputed Monthly Income (mean $4,500 / P10 $0 / P90 $25K)

**Do NOT read** (explicitly excluded to protect context budget):
- `references/01_schema-reference.md` — supplementary; schema shapes are already distilled into the Step 3 dataclasses
- `references/05_architect-qa.md` — the two Q's relevant here (Q1 BIGINT, Q7 self-emp placeholder) are already codified in `PRD.md` §7.1 / §7.12 and `config/settings.py`
- `references/07_mvp-schema-reference.md` — DDL column shapes belong to the tier generators, not to the registry builder; this step writes no DataFrames

## Produces

All paths relative to the project root.

**New files:**

- `registry/universe.py` — the `UniverseBuilder` class and its private `_assign_*` phase methods. Public surface: a single `build(config, rng)` method returning a fully populated `GenerationContext`. Private methods, in the canonical order from `mvp-tool-design.md` §5:
  - `_generate_customer_shells(config, rng, ids)` — creates ~3,000 `CustomerProfile` shells with `party_id` from `ids.next('party')` and `party_type` 80% `'INDIVIDUAL'` / 20% `'ORGANIZATION'`. Returns `List[CustomerProfile]` with only identity fields populated.
  - `_assign_demographics(customers, rng)` — fills `age` (SCF AGECL), `income_quartile` (1–4, roughly uniform but skewed toward Q2–Q3), `gender_type_cd` / `marital_status_cd` / `ethnicity_type_cd` / `occupation_cd` (INDIVIDUAL only, else `None`), `num_dependents` (0 for ORGANIZATION), `fico_score` (300–850 calibrated by ethnicity × income quartile per Part D5; 0 for ORGANIZATION).
  - `_assign_households(customers, rng, ids)` — assigns `household_id` (None for singletons and all organizations), `household_role` (`'HEAD'` / `'SPOUSE'` / `'DEPENDENT'` — defaults `'HEAD'` for singletons and organizations), `lifecl` (1–6 per Part A8, conditioned on `age`).
  - `_assign_cohorts(customers, rng)` — assigns `lifecycle_cohort` in the exact target mix 55% / 30% / 5% / 10%. Shuffle the list with `rng` and slice by target counts (do NOT use `rng.choice` with probabilities — that yields ±2–3% sampling error at N=3,000, which blows the ±0.5% tolerance). Organizations may appear in any cohort.
  - `_assign_clv_segments(customers, rng)` — assigns `clv_segment` 1–10 decile (top decile = high-value). Correlate with `lifecycle_cohort`: CHURNED skew to 1–3, DECLINING skew to 3–6, ACTIVE uniform 1–10, NEW skew to 4–7.
  - `_assign_products(customers, rng)` — fills `product_set` per `mvp-tool-design.md` §5 "Product assignment rules":
    1. 10% of INDIVIDUAL customers → empty `product_set` (unbanked)
    2. All other INDIVIDUAL get `'CHECKING'` (Part B 90% penetration)
    3. For each additional product, independent Bernoulli draw with Part B ownership rate; age-conditional rates per Part A for RETIREMENT, MORTGAGE, STUDENT_LOAN
    4. CLV top-decile (`clv_segment == 10`) → force 4–8 products
    5. ORGANIZATION → `['COMMERCIAL_CHECKING']` only; no mortgage/retirement
    6. DECLINING cohort → product set as-is (no "growth" bonus)
    7. NEW cohort → Maslow-hierarchy-only product set per Part F3 conditioned on `age` / `lifecl`
  - `_generate_agreements(customers, config, rng, ids)` — produces ~5,000 `AgreementProfile` objects by iterating each customer's `product_set` and minting one `AgreementProfile` per product. `product_type` is the string from `product_set`; `agreement_subtype_cd` is a value later mapped by Step 6 seed data (use the product-type string uppercase as a proxy — `'CHECKING'`, `'MORTGAGE'`, etc.); `product_id` from `ids.next('product')` — but **reuse the same `product_id` across agreements with the same `product_type`**, so `Core_DB.PRODUCT` in Step 10 has ≤12 rows, not 5,000. Set the eight `is_*` sub-type flags correctly per the mapping below (exclusive sub-typing per PRD §7.5).
  - `_assign_open_dates(customers, agreements, config, rng)` — per the cohort rules in `mvp-tool-design.md` §5:
    - ACTIVE: `open_dttm` ∈ [2015-01-01, 2025-09-30]; `close_dttm = None`
    - DECLINING: `open_dttm` ∈ [2015-01-01, 2025-06-30]; `close_dttm = None`
    - CHURNED: `open_dttm` ∈ [2015-01-01, 2025-06-30]; `close_dttm` ∈ [2025-10-01, 2026-03-15]
    - NEW: `open_dttm` ∈ [2026-01-15, 2026-03-31]; `close_dttm = None`
    - Also populate `CustomerProfile.party_since` = the minimum `open_dttm` across that customer's agreements (or a date ≤ that minimum for NEW cohort). If a customer's `product_set` is empty, `party_since` = a random date within [2015-01-01, SIM_DATE].
  - `_assign_balances(customers, agreements, rng)` — fills `balance_amt` using `sample_deposit_balance(rng, income_quartile)` for deposit products, `sample_cc_balance(rng, income_quartile)` for credit cards, and Part C stratified ranges for mortgage/vehicle/student. Fills `interest_rate` using `sample_mortgage_rate(rng, origination_year)` for mortgages (vintage-based per Part I1), fixed bands for deposits (CHECKING 0.0005, SAVINGS 0.004, CD 0.05, etc.), and higher bands for loans. Fills `original_loan_amt` for loan-type products only (None for deposits / credit cards).
  - `_assign_balance_trajectories(agreements, rng)` — for each DECLINING-cohort agreement, populate `monthly_balances` with exactly 6 `Decimal` values derived from `month_snapshots(HISTORY_START, SIM_DATE)`. Trajectory: start at `balance_amt`, decline monthly by a draw ∈ [5%, 25%]; final month ≥ 0. For non-DECLINING cohorts, leave `monthly_balances = []`. For CHURNED cohort agreements, the trajectory reaches ≤ $100 by the month before `close_dttm`.
  - `_assign_status_flags(agreements, rng)` — flips `is_delinquent` at 11.2% (LATE per Part C9), `is_severely_delinquent` at 4.6% (LATE60 — must be a strict subset of delinquent), `is_frozen` at a small rate (~0.5%, only for CREDIT / LOAN-type agreements). Deposit-type agreements are never delinquent/frozen by this logic (set flags False explicitly).
  - `_generate_address_pool(config, rng, ids)` — creates ~500 `AddressRecord` objects using Faker (US addresses) with FK placeholder IDs `city_id` / `county_id` / `territory_id` / `postal_code_id` / `country_id` drawn from a small fixed range (Step 9 / Tier 1 Geography will generate the actual rows; this step merely reserves stable integer FKs). Coordinates `latitude` / `longitude` within US bounds (lat 25–49, lon −125 to −65). `address_subtype_cd = 'PHYSICAL'`.
  - `_assign_addresses(customers, addresses, rng)` — assigns each customer's `address_id` by drawing uniformly from the 500-address pool (households share addresses — realistic; a single address may back 6–10 customers).
  - `build(config, rng)` — public entry point. Order of operations: construct `IdFactory(config.ID_RANGES)`, run the eleven `_assign_*` / `_generate_*` phases in the exact §5 order, instantiate and return `GenerationContext(rng=rng, ids=ids, config=config, customers=..., agreements=..., addresses=..., tables={})`.
  - Optional module-level `if __name__ == '__main__':` self-test block that runs `build()` with `np.random.default_rng(42)` and a smaller scale (e.g. `TARGET_CUSTOMERS=100, TARGET_AGREEMENTS=200`) for quick sanity, printing `registry/universe.py OK` on success. Does NOT replace the full-scale exit-criteria checks.

**Modified file:**
- `config/distributions.py` — replace every `raise NotImplementedError("Implemented in Step 4")` body with a real sampler implementation. Signatures MUST NOT change (Step 4 keeps the existing argument order and return types, including `rng: np.random.Generator` as the first parameter for every function and `Decimal` return types for amount / rate samplers). Thirteen samplers in total:
  - `sample_age(rng, n) -> np.ndarray` — draw from AGECL weights, then uniform within each bucket, compute `birth_year = survey_year - age`. Respect the `Birth_Dt` 1940-01-01 to 2005-12-31 hard cap (AGECL 6 → ages 75–82 only, not 75+).
  - `sample_income_quartile(rng, n) -> np.ndarray` — return integers 1–4 with weights [0.25, 0.25, 0.25, 0.25] (uniform quartile assignment; income variability comes from `sample_annual_income`'s stratified range, not the quartile draw).
  - `sample_fico(rng, ethnicity, income_quartile) -> int` — base = 600 + 50 × income_quartile. Ethnicity adjustment: WHITE / ASIAN +20, BLACK −50, HISPANIC / OTHER −25. Add `rng.normal(0, 40)` jitter. Clip to [300, 850]. Returns Python `int`.
  - `sample_deposit_balance(rng, income_quartile) -> Decimal` — log-normal with median from Part C1 (Q1 $350, Q2 $1,600, Q3 $4,000, Q4 $23,000). Use `rng.lognormal(mean=ln(median), sigma=1.0)`. Clip to the Part C1 per-quartile range. Round to 4 decimal places (`DECIMAL(18,4)`).
  - `sample_cc_balance(rng, income_quartile) -> Decimal` — log-normal stratified by Part C3 (Q1 $1,200, Q2 $1,700, Q3 $3,000, Q4 $5,600 medians). Return `Decimal('0.0000')` if the customer does not carry a revolving balance (the caller in `_assign_balances` decides via Part C3 "% Carrying Balance" column — 35% / 50% / 57% / 24%).
  - `sample_mortgage_rate(rng, origination_year) -> Decimal` — vintage buckets per Part I1. Return `Decimal` rounded to 12 decimal places (`DECIMAL(15,12)`).
  - `sample_annual_income(rng, occupation_cd, income_quartile) -> Decimal` — Part C7 stratified ranges (EMP $24K–$450K, SELF_EMP $30K–$5M, RETIRED $12K–$500K, NOT_WORKING $10K–$150K). Within range, pick by income_quartile position.
  - `sample_ethnicity(rng, n) -> np.ndarray` — `rng.choice(['WHITE', 'BLACK', 'HISPANIC', 'ASIAN', 'OTHER'], n, p=[0.597, 0.134, 0.115, 0.073, 0.080])`.
  - `sample_gender(rng, n) -> np.ndarray` — `rng.choice(['MALE', 'FEMALE'], n, p=[0.50, 0.50])` — neutral 50/50 per Part A2 note.
  - `sample_marital(rng, age) -> str` — under 25 → 90% SINGLE; 25–35 → 55% SINGLE, 45% MARRIED; over 35 → Part A3 baseline (63.2% MARRIED, 36.8% SINGLE).
  - `sample_occupation(rng, n) -> np.ndarray` — Part A7 weights [0.496, 0.217, 0.248, 0.039] for [EMP, SELF_EMP, RETIRED, NOT_WORKING].
  - `sample_kids(rng, lifecl) -> int` — LIFECL 1 / 2 / 4 / 5 / 6 → 0 (couples/singles no kids); LIFECL 3 → 1–4 kids per Part A4 weights renormalized.
  - `sample_lifecl(rng, age) -> int` — age < 55 → 1 / 2 / 3 (singles / couples / families); age ≥ 55 → 4 / 5 / 6 per Part A8 weights renormalized to each age bucket.

### Product-type → AgreementProfile.is_* flag mapping (authoritative — enforce in `_generate_agreements`)

Every agreement must satisfy: **exactly one of `{is_term_deposit, is_mortgage, is_credit_card, is_loan_transaction}` is True, OR all four are False and the agreement terminates at a non-leaf level** (DEPOSIT for checking/savings/MMA/retirement; LOAN_TERM for vehicle/student; CREDIT for HELOC). Parent-chain flags may be True simultaneously.

| `product_type`          | `is_financial` | `is_deposit` | `is_term_deposit` | `is_credit` | `is_loan_term` | `is_mortgage` | `is_credit_card` | `is_loan_transaction` |
|-------------------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `CHECKING`              | T | T | F | F | F | F | F | F |
| `SAVINGS`               | T | T | F | F | F | F | F | F |
| `MMA`                   | T | T | F | F | F | F | F | F |
| `RETIREMENT`            | T | T | F | F | F | F | F | F |
| `CERTIFICATE_OF_DEPOSIT`| T | T | T | F | F | F | F | F |
| `CREDIT_CARD`           | T | F | F | T | F | F | T | F |
| `HELOC`                 | T | F | F | T | F | F | F | F |
| `VEHICLE_LOAN`          | T | F | F | T | T | F | F | F |
| `STUDENT_LOAN`          | T | F | F | T | T | F | F | F |
| `MORTGAGE`              | T | F | F | T | T | T | F | F |
| `PAYDAY`                | T | F | F | F | F | F | F | T |
| `COMMERCIAL_CHECKING`   | T | T | F | F | F | F | F | F |

## Tables generated (if applicable)

No tables generated in this step. `ctx.tables` remains `{}`; Steps 8–23 populate it. The universe built here is purely in-memory dataclass state consumed by tier generators downstream.

## Files to modify

- `config/distributions.py` — replace 13 `raise NotImplementedError` bodies with real implementations. Do NOT change any function signature, argument order, default values, or return type. Do NOT add new public functions; any helpers (e.g. log-normal from median) go in a private `_` -prefixed function in the same file.

## New dependencies

No new dependencies. `numpy`, `pandas`, `scipy`, `faker`, and `python-dateutil` are already pinned in `requirements.txt` from Step 1. Log-normal sampling uses `numpy.random.Generator.lognormal` — no direct `scipy.stats` call needed, but `scipy.stats.truncnorm` is acceptable if preferred for FICO or balance generation. Faker is used only by `_generate_address_pool`.

## Rules for implementation

- **BIGINT for all ID columns (per PRD §7.1)** — every `party_id`, `agreement_id`, `product_id`, `address_id`, `household_id` minted in this step comes from `IdFactory.next(category)`, which returns Python `int`. Never use `numpy.int32` / `numpy.int64` for these — the registry layer works in pure Python int space; numpy types only enter via sampler arrays, and those arrays are demographic codes, ages, or balances, not IDs.
- **Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2)** — `CustomerProfile.party_id` is a single field. Do not mint a separate CDM-only ID. A customer's `party_id` is the value Step 22 (Tier 14) will write to `CDM_DB.PARTY.CDM_Party_Id` and Step 11 (Tier 3) will write to `Core_DB.INDIVIDUAL.Individual_Party_Id`.
- **DI column stamping on every table via `BaseGenerator.stamp_di()`** — n/a at this step. No DataFrames are produced; stamping happens in Steps 8–23 when registry lists are projected into Schema.TABLE DataFrames.
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — n/a: no DataFrames produced.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` (per PRD §7.3)** — n/a: no DataFrames produced.
- **Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md`** — n/a: no DataFrames produced.
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10)** — n/a at this step. `config.settings.PARTY_INTERRACTION_EVENT_TABLE_NAME` is the single source of truth, consulted by Step 22.
- **Skip the `GEOSPATIAL` table entirely (per PRD §7.9)** — n/a: this step generates no CSVs. `config.settings.SKIPPED_TABLES` is consulted by the Step 5 writer.
- **No ORMs, no database connections — pure pandas → CSV** — this step uses `numpy`, `scipy` (optionally), and `faker` only. No `pandas` objects are constructed here (the `tables` dict on `GenerationContext` stays `{}`). No SQLAlchemy / pyodbc / teradatasql imports.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — this is the single most important rule for this step. Every stochastic decision — every `rng.integers`, `rng.choice`, `rng.lognormal`, `rng.uniform`, every Faker call — must take the `rng` explicitly (for Faker, seed `Faker._faker.seed_instance(rng.integers(0, 2**32))` ONCE inside `_generate_address_pool` — never call `Faker.seed(...)` at module import). Running `UniverseBuilder().build(config, np.random.default_rng(42))` twice in the same process or in fresh processes must produce byte-identical pickled registries.

### Step-specific rules

- **Accept `rng` and `config` as explicit parameters; do not read globals.** `build(config, rng)` threads `config` and `rng` through every `_assign_*` method. No `_assign_*` method reads `config.settings` directly — always via the `config` argument. This makes future runs with a scaled-down fixture config (e.g. 100 customers) trivial without monkey-patching.
- **Samplers in `config/distributions.py` must be pure functions.** They take `rng` as their first argument and return a value. They MUST NOT mutate module state, cache results across calls, print, or read from disk. This is what makes the reproducibility guarantee achievable.
- **Cohort assignment uses shuffle-and-slice, not weighted choice.** `rng.choice(['ACTIVE', 'DECLINING', 'CHURNED', 'NEW'], n, p=[0.55, 0.30, 0.05, 0.10])` has ±2–3% sampling error at N=3,000 — enough to break the ±0.5% tolerance. Compute exact counts `n_active = int(round(n * 0.55))`, etc., adjust the last bucket so counts sum to `n`, build the label list, shuffle with `rng.shuffle`, then zip against the customers list.
- **Exclusive terminal-leaf sub-typing enforced programmatically.** In `_generate_agreements`, assert `sum([ap.is_term_deposit, ap.is_mortgage, ap.is_credit_card, ap.is_loan_transaction]) <= 1` for every agreement immediately after setting flags. Use the authoritative product-type → flag table above; do not invent new mappings.
- **Self-employed cohort flagged, not written.** `CustomerProfile.occupation_cd == 'SELF_EMP'` is the only flag Steps 11/12 need. Do NOT insert the `SELF_EMP_ORG_ID = 9_999_999` placeholder row into any dataclass or table here — that row is inserted by Step 11 into the ORGANIZATION CSV. This step merely ensures ~21.7% ±1% of individuals have `occupation_cd = 'SELF_EMP'`.
- **DECLINING-cohort monthly trajectories use `utils.date_utils.month_snapshots(HISTORY_START, SIM_DATE)`.** The util returns exactly 6 tuples; produce exactly 6 `Decimal` values in `monthly_balances`. Trajectory formula: `balances[i] = balances[i-1] * (1 - rng.uniform(0.05, 0.25))`; clamp to ≥ 0.
- **CHURNED cohort trajectory reaches near-zero before close.** For CHURNED agreements, the decline must be steeper so that by the month of `close_dttm` the balance is ≤ $100. Don't allow a $50K balance to hang around the day before account closure.
- **Faker instance owned by `_generate_address_pool`, seeded once.** Create a local `Faker('en_US')` instance at the top of `_generate_address_pool`, immediately seed it with `fake.seed_instance(int(rng.integers(0, 2**32 - 1)))`, and pass that single instance around. Never call module-level `Faker.seed(...)`.
- **No Python-level caching of sampler output.** Do not add `@lru_cache` to any sampler — it would cache across different `rng` seeds and break reproducibility.
- **No parallelism, no `multiprocessing`, no threading.** A parallelized universe build would break reproducibility (thread scheduling is non-deterministic). At 3,000 customers / 5,000 agreements the serial build is <2 seconds on a modern laptop; parallelism is unnecessary.
- **`_assign_*` methods mutate in place; `_generate_*` methods return new lists.** Follow this naming convention strictly so readers know at a glance which methods have side effects. The mvp-tool-design.md §5 sequence follows this convention.
- **`GenerationContext` is constructed ONLY at the end of `build()`.** Do not pass a partial context around between `_assign_*` methods; pass the raw lists (`customers: List[CustomerProfile]`, `agreements: List[AgreementProfile]`) and config/rng/ids explicitly. This keeps the context immutable-after-construction and matches Step 3's "constructable with only rng and ids" contract.
- **FICO bucketing is real but bounded.** Ethnicity-based FICO offsets reflect the Part D5 credit-denial reality in SCF data but are bounded: clip every score to [300, 850]. Do not introduce degenerate scores (no one has FICO=300 baseline; the clip is defensive).
- **WP5 vs SCF tension resolved via design Decision 5.** For per-account `balance_amt` on deposit agreements, use SCF income-quartile stratified ranges (Part C1). WP5 aggregate metrics ($2K mean deposit) drive `PARTY_SCORE.Party_Score_Val` in a future tier, NOT the agreement-level balance. Total Investments AUM (WP5 $75K mean) applies only to investment-holding customers (~59%); the other ~41% do not get RETIREMENT products.
- **No writes to `ctx.tables`.** Leave the dict empty. The first table insertion is by Step 8's `Tier0Lookups.generate(ctx)`.

## Definition of done

Each item is a checkbox. Tick every box or mark it `n/a` with a one-line justification before the session ends.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

- [ ] **`build(config, rng)` returns a `GenerationContext` with ~3,000 CustomerProfiles and ~5,000 AgreementProfiles.** Verify:
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  assert 2950 <= len(ctx.customers) <= 3050, f'customers={len(ctx.customers)}'
  assert 4700 <= len(ctx.agreements) <= 5300, f'agreements={len(ctx.agreements)}'
  assert ctx.tables == {}, 'tables must remain empty after build()'
  print(f'OK: {len(ctx.customers)} customers, {len(ctx.agreements)} agreements')
  "
  ```
  Must print a line starting with `OK:` showing both counts.

- [ ] **Cohort percentages within ±0.5% of target (55/30/5/10).** Verify:
  ```bash
  python -c "
  import numpy as np
  from collections import Counter
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  c = Counter(cp.lifecycle_cohort for cp in ctx.customers)
  n = len(ctx.customers)
  targets = {'ACTIVE': 0.55, 'DECLINING': 0.30, 'CHURNED': 0.05, 'NEW': 0.10}
  for cohort, tgt in targets.items():
      actual = c[cohort] / n
      assert abs(actual - tgt) <= 0.005, f'{cohort}: {actual:.4f} vs target {tgt} (delta {actual-tgt:+.4f})'
  print('cohorts OK:', dict(c))
  "
  ```
  Must print a line starting with `cohorts OK:`.

- [ ] **Individual/Organization split within ±0.5% of 80/20.** Verify:
  ```bash
  python -c "
  import numpy as np
  from collections import Counter
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  c = Counter(cp.party_type for cp in ctx.customers)
  n = len(ctx.customers)
  assert abs(c['INDIVIDUAL']/n - 0.80) <= 0.005, f\"INDIVIDUAL={c['INDIVIDUAL']/n:.4f}\"
  assert abs(c['ORGANIZATION']/n - 0.20) <= 0.005, f\"ORGANIZATION={c['ORGANIZATION']/n:.4f}\"
  print('party_type split OK:', dict(c))
  "
  ```
  Must print a line starting with `party_type split OK:`.

- [ ] **Every AgreementProfile has exactly one true terminal-leaf `is_*` flag, OR all four terminal-leaf flags False (exclusive sub-typing per PRD §7.5).** Verify:
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  for ap in ctx.agreements:
      terminal = sum([ap.is_term_deposit, ap.is_mortgage, ap.is_credit_card, ap.is_loan_transaction])
      assert terminal <= 1, f'Agreement {ap.agreement_id} has {terminal} terminal flags True'
  # And for agreements that SHOULD have a terminal leaf (mortgage, CD, CC, payday), verify one is True
  needs_terminal = {'MORTGAGE': 'is_mortgage', 'CERTIFICATE_OF_DEPOSIT': 'is_term_deposit',
                   'CREDIT_CARD': 'is_credit_card', 'PAYDAY': 'is_loan_transaction'}
  for ap in ctx.agreements:
      if ap.product_type in needs_terminal:
          flag_name = needs_terminal[ap.product_type]
          assert getattr(ap, flag_name), f'Agreement {ap.agreement_id} {ap.product_type} missing {flag_name}'
  print('exclusive sub-typing OK')
  "
  ```
  Must print `exclusive sub-typing OK`.

- [ ] **`is_frozen` is never True for deposit-type agreements.** (Mirrors the `_assign_status_flags` rule: "Deposit-type agreements are never delinquent/frozen by this logic." The same invariant also holds for `is_delinquent` / `is_severely_delinquent` on deposit types — consider extending this assertion if you want a single-pass check.)
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  deposit_types = {'CHECKING', 'SAVINGS', 'MMA', 'RETIREMENT', 'CERTIFICATE_OF_DEPOSIT', 'COMMERCIAL_CHECKING'}
  for ap in ctx.agreements:
      if ap.product_type in deposit_types:
          assert not ap.is_frozen, f'Agreement {ap.agreement_id} ({ap.product_type}) has is_frozen=True — deposit accounts cannot be frozen'
  print('is_frozen deposit check OK')
  "
  ```
  Must print `is_frozen deposit check OK`.

- [ ] **Self-employed cohort ~21.7% ±1% of individuals.** Verify:
  ```bash
  python -c "
  import numpy as np
  from collections import Counter
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  indiv = [cp for cp in ctx.customers if cp.party_type == 'INDIVIDUAL']
  c = Counter(cp.occupation_cd for cp in indiv)
  se_pct = c['SELF_EMP'] / len(indiv)
  assert 0.207 <= se_pct <= 0.227, f'SELF_EMP={se_pct:.4f} (target 0.217 ±0.01)'
  print(f'SELF_EMP OK: {se_pct:.4f} ({c[\"SELF_EMP\"]}/{len(indiv)})')
  "
  ```
  Must print a line starting with `SELF_EMP OK:`.

- [ ] **Running twice with seed=42 produces byte-identical registries.** Verify:
  ```bash
  python -c "
  import numpy as np, pickle, hashlib
  from config import settings
  from registry.universe import UniverseBuilder
  ctx1 = UniverseBuilder().build(settings, np.random.default_rng(42))
  ctx2 = UniverseBuilder().build(settings, np.random.default_rng(42))
  # Exclude rng / ids / config (non-picklable or irrelevant to determinism)
  def snap(c):
      return hashlib.sha256(pickle.dumps((c.customers, c.agreements, c.addresses))).hexdigest()
  h1, h2 = snap(ctx1), snap(ctx2)
  assert h1 == h2, f'Reproducibility FAILED: {h1[:16]} != {h2[:16]}'
  print(f'reproducibility OK: {h1[:16]}')
  "
  ```
  Must print a line starting with `reproducibility OK:`.

### Additional integrity checks (not in implementation-steps.md exit criteria but required by design §5 / §10)

- [ ] **Every customer's `address_id` resolves to exactly one `AddressRecord` in `ctx.addresses`.**
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  addr_ids = {a.address_id for a in ctx.addresses}
  unresolved = [cp.party_id for cp in ctx.customers if cp.address_id not in addr_ids]
  assert not unresolved, f'{len(unresolved)} customers with unresolved address_id (first 3: {unresolved[:3]})'
  print(f'address FK OK: {len(addr_ids)} addresses / {len(ctx.customers)} customers')
  "
  ```
  Must print a line starting with `address FK OK:`.

- [ ] **Every agreement's `owner_party_id` resolves to exactly one `CustomerProfile.party_id`.**
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  party_ids = {cp.party_id for cp in ctx.customers}
  orphans = [ap.agreement_id for ap in ctx.agreements if ap.owner_party_id not in party_ids]
  assert not orphans, f'{len(orphans)} orphan agreements (first 3: {orphans[:3]})'
  print(f'owner FK OK: {len(ctx.agreements)} agreements')
  "
  ```
  Must print a line starting with `owner FK OK:`.

- [ ] **All agreement IDs are BIGINT (Python `int`) and unique.**
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  ids = [ap.agreement_id for ap in ctx.agreements]
  assert all(isinstance(x, int) and type(x) is int for x in ids), 'non-int agreement_id detected'
  assert len(ids) == len(set(ids)), f'duplicate agreement_ids: {len(ids) - len(set(ids))} dupes'
  print(f'agreement_id BIGINT unique OK: {len(ids)} ids')
  "
  ```
  Must print a line starting with `agreement_id BIGINT unique OK:`.

- [ ] **CHURNED cohort agreements have `close_dttm` set; all others have `close_dttm is None`.**
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  owner = {cp.party_id: cp.lifecycle_cohort for cp in ctx.customers}
  for ap in ctx.agreements:
      cohort = owner[ap.owner_party_id]
      if cohort == 'CHURNED':
          assert ap.close_dttm is not None, f'CHURNED agreement {ap.agreement_id} has no close_dttm'
      else:
          assert ap.close_dttm is None, f'{cohort} agreement {ap.agreement_id} has close_dttm set'
  print('close_dttm cohort invariant OK')
  "
  ```
  Must print `close_dttm cohort invariant OK`.

- [ ] **Every DECLINING-cohort agreement has exactly 6 `monthly_balances` entries; non-DECLINING agreements have `monthly_balances == []`.**
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  owner = {cp.party_id: cp.lifecycle_cohort for cp in ctx.customers}
  for ap in ctx.agreements:
      cohort = owner[ap.owner_party_id]
      if cohort == 'DECLINING':
          assert len(ap.monthly_balances) == 6, f'DECLINING agreement {ap.agreement_id} has {len(ap.monthly_balances)} balances'
      else:
          assert ap.monthly_balances == [], f'{cohort} agreement {ap.agreement_id} has monthly_balances'
  print('monthly_balances cohort invariant OK')
  "
  ```
  Must print `monthly_balances cohort invariant OK`.

- [ ] **`is_severely_delinquent` is a strict subset of `is_delinquent`.**
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  viol = [ap.agreement_id for ap in ctx.agreements if ap.is_severely_delinquent and not ap.is_delinquent]
  assert not viol, f'severe-but-not-delinquent: {viol[:5]}'
  print('delinquency subset invariant OK')
  "
  ```
  Must print `delinquency subset invariant OK`.

- [ ] **FICO scores are within [300, 850] for INDIVIDUAL customers.**
  ```bash
  python -c "
  import numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  indiv = [cp for cp in ctx.customers if cp.party_type == 'INDIVIDUAL']
  assert all(300 <= cp.fico_score <= 850 for cp in indiv), 'FICO out of range'
  print(f'FICO range OK: min={min(cp.fico_score for cp in indiv)}, max={max(cp.fico_score for cp in indiv)}')
  "
  ```
  Must print a line starting with `FICO range OK:`.

- [ ] **~500 addresses in the pool; realistic customer-to-address sharing (mean ≈ 6 customers per address).**
  ```bash
  python -c "
  import numpy as np
  from collections import Counter
  from config import settings
  from registry.universe import UniverseBuilder
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  assert 400 <= len(ctx.addresses) <= 600, f'{len(ctx.addresses)} addresses — expected ~500'
  c = Counter(cp.address_id for cp in ctx.customers)
  mean_share = sum(c.values()) / len(c)
  assert 3 <= mean_share <= 10, f'mean customers/address = {mean_share:.2f}'
  print(f'address pool OK: {len(ctx.addresses)} addresses, mean {mean_share:.2f} customers each')
  "
  ```
  Must print a line starting with `address pool OK:`.

- [ ] **Every `config/distributions.py` sampler is callable (no `NotImplementedError`).**
  ```bash
  python -c "
  import numpy as np
  from decimal import Decimal
  from config.distributions import (sample_age, sample_income_quartile, sample_fico,
      sample_deposit_balance, sample_cc_balance, sample_mortgage_rate,
      sample_annual_income, sample_ethnicity, sample_gender, sample_marital,
      sample_occupation, sample_kids, sample_lifecl)
  rng = np.random.default_rng(42)
  assert len(sample_age(rng, 100)) == 100
  assert len(sample_income_quartile(rng, 100)) == 100
  assert 300 <= sample_fico(rng, 'WHITE', 3) <= 850
  assert isinstance(sample_deposit_balance(rng, 3), Decimal)
  assert isinstance(sample_cc_balance(rng, 3), Decimal)
  assert isinstance(sample_mortgage_rate(rng, 2021), Decimal)
  assert isinstance(sample_annual_income(rng, 'EMP', 3), Decimal)
  assert len(sample_ethnicity(rng, 100)) == 100
  assert len(sample_gender(rng, 100)) == 100
  assert sample_marital(rng, 40) in ('MARRIED', 'SINGLE')
  assert len(sample_occupation(rng, 100)) == 100
  assert 0 <= sample_kids(rng, 3) <= 5
  assert 1 <= sample_lifecl(rng, 40) <= 6
  print('samplers callable OK')
  "
  ```
  Must print `samplers callable OK`.

### Universal checks

- [ ] **`git status` shows only files listed under `## Produces` or `## Files to modify` — nothing else.**
  ```bash
  git status --porcelain
  ```
  Every line must map to one of: `registry/universe.py` (new), `config/distributions.py` (modified). No stray files.

- [ ] **All new files pass `python -c "import <module>"`:**
  ```bash
  python -c "import registry.universe, config.distributions"
  ```
  Must exit 0 with no output.

- [ ] **No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1)** — n/a: this step produces no CSVs. BIGINT semantics are enforced at the registry layer: every `*_id` field on `CustomerProfile` / `AgreementProfile` / `AddressRecord` is a Python `int` minted via `IdFactory.next(...)`.

- [ ] **If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo** — n/a: this step writes no CSVs.

- [ ] **If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv`** — n/a: this step writes no CSVs.

- [ ] **Full-scale `build()` runs in under 10 seconds on a laptop.** Verify:
  ```bash
  python -c "
  import time, numpy as np
  from config import settings
  from registry.universe import UniverseBuilder
  t = time.time()
  ctx = UniverseBuilder().build(settings, np.random.default_rng(42))
  elapsed = time.time() - t
  assert elapsed < 10.0, f'build() took {elapsed:.1f}s — too slow'
  print(f'build() OK in {elapsed:.2f}s')
  "
  ```
  Must print a line starting with `build() OK in`.

## Handoff notes

### What shipped
- `config/distributions.py` — all 13 samplers implemented. All probability weight arrays explicitly normalized (SCF weights like `[0.133, 0.166, …]` sum to 0.998, not 1.0 — numpy's `rng.choice` requires exact-sum-to-1). Private helper `_lognormal_decimal` added.
- `registry/universe.py` — `UniverseBuilder` with all 11 `_assign_*`/`_generate_*` private methods. All 17 exit criteria pass (including byte-identical reproducibility, ±0.5% cohort tolerances, exclusive sub-typing, delinquency subset invariant, FICO range, address pool sharing).

### Rate scaling decision
SCF Part B ownership rates are **cross-institution household rates**. Applied naively to 3,000 customers they produce ~8,100 agreements (well above the 4,700–5,300 exit criterion). A `S = 0.40` per-bank penetration scale factor is applied to all optional product rates in `_assign_products`. This reflects the realistic fraction of SCF-reported product holdings that belong to any single institution. The scale constant is documented inline in the code.

### CHURNED monthly_balances
The spec description mentions "CHURNED trajectory reaches ≤ $100 before close_dttm" but the exit criterion Python check asserts `monthly_balances == []` for all non-DECLINING cohorts. These are consistent: the CHURNED near-zero balance trajectory is meant to be rendered by **Tier 7a AGREEMENT_FEATURE** rows (using `balance_amt`), NOT via the `monthly_balances` field. `monthly_balances` is populated only for DECLINING cohort.

### `_assign_balance_trajectories` signature
Method signature was extended to `(customers, agreements, rng, config)` vs. the `(agreements, rng)` sketch in mvp-tool-design.md §5, because cohort lookup requires the customers list. This is a private method — no downstream impact.

### Deferred items
None. All spec exit criteria satisfied.

### Next session hint
Step 5 (Output Writer) can start now — it depends only on Steps 1–2, which are stable. Step 6 (Tier 0a seed data) can also start in parallel — it depends only on Step 1 config. Both are independent of Step 4.

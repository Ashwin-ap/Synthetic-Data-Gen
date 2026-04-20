# Spec: Step 17 — Tier 7b Agreement Sub-Type Chain + Card

## Overview

This step builds **Tier 7b**, which materialises the full AGREEMENT inheritance chain for every agreement produced by Step 10 (Tier 2 Core) and emits the `CARD` rows that physically front the credit-card and checking-deposit agreements. Each agreement follows **exactly one terminal path** through the FSDM inheritance hierarchy (exclusive sub-typing per PRD §7.5), but intermediate parents in its path (FINANCIAL → DEPOSIT/CREDIT → LOAN → LOAN_TERM → terminal leaf) all get their own row in the corresponding parent table. Nine sub-type tables plus `CARD` = **10 Core_DB tables** are written to `ctx.tables`. The `is_*` flags on `AgreementProfile` (set atomically in Step 4 `UniverseBuilder` via the `_PRODUCT_FLAGS` mapping at `registry/universe.py:40`) are the sole authority for which parent/leaf rows to emit — this step performs **no sub-typing decisions**, only deterministic fan-out and DDL-conformant column population. `CARD` rows are generated Luhn-valid via `utils/luhn.generate_card_number()` (Step 2). See `mvp-tool-design.md` §7.5 (exclusive sub-typing rationale), §9 Tier 7 (authoritative table list), and `references/06_supporting-enrichments.md` Part C4/C6 (mortgage/vehicle term semantics) for the ground-truth inputs. Tier 7a (Step 16) has already populated the cross-cutting AGREEMENT_STATUS/CURRENCY/SCORE/FEATURE/METRIC/RATE + interest-rate-index tables; Tier 7b is sibling, not downstream — neither reads from the other.

## Depends on

- **Step 1** — consumes `config/settings.py` constants: `HIGH_TS`, `SIM_DATE`, `SEED`, and `ID_RANGES['card'] = 7_000_000`.
- **Step 2** — consumes `generators/base.BaseGenerator.stamp_di()` (5-column DI tail) and `utils/luhn.generate_card_number(rng, bin_prefix)` + `utils/luhn.generate_cvv(rng)` + `utils/luhn.luhn_check()` (mod-10 verification). Consumes `utils/id_factory.IdFactory.next('card')` for monotonic BIGINT `Access_Device_Id` minting.
- **Step 3** — consumes `registry/context.GenerationContext` and `registry/profiles.AgreementProfile` fields: `agreement_id`, `owner_party_id`, `product_type`, `agreement_subtype_cd`, `open_dttm`, `close_dttm`, `balance_amt`, `interest_rate`, `original_loan_amt`, and **all eight** `is_*` sub-type flags (`is_financial`, `is_deposit`, `is_term_deposit`, `is_credit`, `is_loan_term`, `is_mortgage`, `is_credit_card`, `is_loan_transaction`).
- **Step 4** — consumes `ctx.agreements` (≈5,000 `AgreementProfile` instances). The `_PRODUCT_FLAGS` table at `registry/universe.py:40` is the authoritative product-type → is-flag mapping:
  - CHECKING/SAVINGS/MMA/RETIREMENT/COMMERCIAL_CHECKING → `(is_financial, is_deposit)` (terminal at DEPOSIT)
  - CERTIFICATE_OF_DEPOSIT → `(is_financial, is_deposit, is_term_deposit)` (terminal at DEPOSIT_TERM)
  - CREDIT_CARD → `(is_financial, is_credit, is_credit_card)` (terminal at CREDIT_CARD)
  - HELOC → `(is_financial, is_credit)` (terminal at CREDIT)
  - VEHICLE_LOAN/STUDENT_LOAN → `(is_financial, is_credit, is_loan_term)` (terminal at LOAN_TERM)
  - MORTGAGE → `(is_financial, is_credit, is_loan_term, is_mortgage)` (terminal at MORTGAGE)
  - PAYDAY → `(is_financial, is_loan_transaction)` (terminal at LOAN_TRANSACTION) — note PAYDAY's `is_credit=False` per the mapping
- **Step 6** — consumes these Tier 0a seed tables (must be present in `ctx.tables` at entry):
  - `Core_DB.FINANCIAL_AGREEMENT_TYPE` — 5 codes: `DEPOSIT | LOAN | CREDIT | INVESTMENT | INSURANCE` (seeded at `seed_data/financial_types.py:10`).
  - `Core_DB.MARKET_RISK_TYPE` — 4 codes: `TRADING_BOOK | BANKING_BOOK | HELD_FOR_SALE | AVAILABLE_FOR_SALE` (seeded at `seed_data/financial_types.py:102`). Retail agreements use `BANKING_BOOK`.
  - `Core_DB.DEPOSIT_MATURITY_SUBTYPE` — 6 codes: `3M | 6M | 12M | 24M | 36M | 60M` (seeded at `seed_data/financial_types.py:63`).
  - `Core_DB.INTEREST_DISBURSEMENT_TYPE` — 4 codes: `COMPOUNDED | SIMPLE | ACCRUED | CAPITALIZED` (seeded at `seed_data/financial_types.py:72`).
  - `Core_DB.LOAN_MATURITY_SUBTYPE` — 4 codes: `SHORT_TERM | MEDIUM_TERM | LONG_TERM | PERPETUAL` (seeded at `seed_data/financial_types.py:27`).
  - `Core_DB.LOAN_TERM_SUBTYPE` — 3 codes: `INSTALLMENT | BALLOON | AMORTIZING` (seeded at `seed_data/financial_types.py:40`).
  - `Core_DB.LOAN_TRANSACTION_SUBTYPE` — 3 codes: `PAYDAY | CASH_ADVANCE | OVERDRAFT` (seeded at `seed_data/financial_types.py:34`).
  - `Core_DB.AMORTIZATION_METHOD_TYPE` — 6 codes: `STRAIGHT_LINE | EFFECTIVE_INTEREST | LEVEL_PAYMENT | INTEREST_ONLY | BULLET | CUSTOM` (seeded at `seed_data/financial_types.py:18`).
  - `Core_DB.SECURITY_TYPE` — 5 codes: `REAL_ESTATE | VEHICLE | DEPOSIT | SECURITIES | UNSECURED` (seeded at `seed_data/financial_types.py:94`).
  - `Core_DB.CREDIT_CARD_AGREEMENT_SUBTYPE` — 5 codes: `STANDARD | REWARDS | SECURED | BUSINESS | STUDENT` (seeded at `seed_data/financial_types.py:46`).
  - `Core_DB.MORTGAGE_TYPE` — 6 codes: `FIXED_RATE | ARM | FHA | VA | JUMBO | HELOC` (seeded at `seed_data/financial_types.py:54`).
- **Step 10** — consumes `ctx.tables['Core_DB.AGREEMENT']` for `Agreement_Id` FK universe. No row is invented that isn't in `AGREEMENT`.

No code from Step 5 (writer), Step 9 (Tier 1), Step 11–15 (Tier 3/4/5/6), or **Step 16 (Tier 7a)** is imported by this step. Tier 7a and Tier 7b are parallel sibling writers — neither reads the other's output. The writer is not invoked — `generate()` returns DataFrames only; orchestrator (Step 25) handles `ctx.tables.update()` and later CSV emission.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 17):
- `PRD.md` §5 (Core Design Principles — esp. correctness over completeness, explicit Layer 2 readiness), §7.1 (BIGINT), §7.3 (DI columns), §7.5 (**exclusive sub-typing — authoritative for this step**)
- `mvp-tool-design.md` §7 (BaseGenerator + DI rules), §7.5 (exclusive sub-typing), §9 Tier 7 (the 10 tables Tier 7b owns), §14 Decision 3 (BIGINT), §14 Decision 7 (none applicable here — typo is in Tier 14)
- `implementation-steps.md` Step 17 entry (exit criteria); Handoff Protocol

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the 10 in-scope tables. Open only these blocks (use SQL DDL where summary tables disagree, per CLAUDE.md "DDL verification rule" and PRD §10):
  - `FINANCIAL_AGREEMENT` (DDL §4692): 10 business + 3 DI = 13 cols. NOT NULL: `Agreement_Id`, `Market_Risk_Type_Cd`. Nullable: `Financial_Agreement_Subtype_Cd`, `Original_Maturity_Dt`, `Risk_Exposure_Mitigant_Subtype_Cd`, `Trading_Book_Cd`, `Pricing_Method_Subtype_Cd`, `Financial_Agreement_Type_Cd`, `Day_Count_Basis_Cd`, `ISO_8583_Account_Type_Cd`.
  - `DEPOSIT_AGREEMENT` (DDL §4800): 7 business + 3 DI = 10 cols. NOT NULL: `Agreement_Id`, `Interest_Disbursement_Type_Cd`. Nullable: `Deposit_Maturity_Subtype_Cd`, `Deposit_Ownership_Type_Cd`, `Original_Deposit_Amt` DECIMAL(18,4), `Original_Deposit_Dt`, `Agreement_Currency_Original_Deposit_Amt`.
  - `DEPOSIT_TERM_AGREEMENT` (DDL §4879): 3 business + 3 DI = 6 cols. NOT NULL only `Agreement_Id`. Nullable: `Next_Term_Maturity_Dt`, `Grace_Period_End_Dt`.
  - `CREDIT_AGREEMENT` (DDL §5958): 18 business + 3 DI = 21 cols. NOT NULL: `Agreement_Id`, `Obligor_Borrowing_Purpose_Cd`, `Credit_Agreement_Grace_Period_Cd`. Nullable: `Seniority_Level_Cd`, `Credit_Agreement_Reaging_Cnt` INTEGER → **BIGINT per PRD §7.1**, `Credit_Agreement_Past_Due_Amt` DECIMAL(18,4), `Credit_Agreement_Charge_Off_Amt`, `Credit_Agreement_Impairment_Amt`, `Credit_Agreement_Settlement_Dt`, `Credit_Agreement_Subtype_Cd`, `Agreement_Currency_Past_Due_Amt`, `Agreement_Currency_Charge_Off_Amt`, `Agreement_Currency_Last_Payment_Amt`, `Agreement_Currency_Impairment_Amt`, `Specialized_Lending_Type_Cd`, `Payment_Frequency_Time_Period_Cd`, `Credit_Agreement_Last_Payment_Amt`, `Credit_Agreement_Last_Payment_Dt`.
  - `LOAN_AGREEMENT` (DDL §6059): 8 business + 3 DI = 11 cols. NOT NULL: `Agreement_Id`, `Security_Type_Cd`. Nullable: `Loan_Maturity_Subtype_Cd`, `Due_Day_Num`, `Realizable_Collateral_Amt` DECIMAL(18,4), `Loan_Payoff_Amt`, `Agreement_Currency_Real_Collateral_Amt`, `Agreement_Currency_Loan_Payoff_Amt`.
  - `LOAN_TERM_AGREEMENT` (DDL §6234): 27 business + 3 DI = 30 cols. NOT NULL: `Agreement_Id`, `Amortization_Method_Cd`, `Loan_Term_Subtype_Cd`. Nullable: `Amortization_End_Dt`, `Balloon_Amt`, `Original_Loan_Amt` DECIMAL(18,4) (populated from `ag.original_loan_amt`), `Preapproved_Loan_Amt`, `Maximum_Monthly_Payment_Amt`, `Improvement_Allocation_Amt`, `Debt_Payment_Allocation_Amt`, `Down_Payment_Amt`, `Loan_Maturity_Dt`, `Loan_Termination_Dt`, `Loan_Renewal_Dt`, `Commit_Start_Dt`, `Commit_End_Dt`, `Payoff_Dt`, `Loan_Asset_Purchase_Dt`, `Agreement_Currency_Balloon_Amt`, `Agreement_Currency_Original_Loan_Amt`, `Agreement_Currency_Preapproved_Amt`, `Agreement_Currency_Maximum_Monthly_Payment_Amt`, `Agreement_Currency_Improve_Allocation_Amt`, `Agreement_Currency_Debt_Payment_Allocation_Amt`, `Loan_Refinance_Ind` CHAR(3) → `'Yes'`/`'No'`, `Agreement_Currency_Down_Payment_Amt`, `Agreement_Currency_Down_Payment_Borrow_Amt`.
  - `LOAN_TRANSACTION_AGREEMENT` (DDL §6140): 2 business + 3 DI = 5 cols. NOT NULL only `Agreement_Id`. Nullable: `Loan_Transaction_Subtype_Cd`.
  - `MORTGAGE_AGREEMENT` (DDL §6353): 10 business + 3 DI = 13 cols. NOT NULL only `Agreement_Id`. Nullable: `First_Time_Mortgage_Ind` CHAR(3) → `'Yes'`/`'No'`, `Closing_Cost_Amt` DECIMAL(18,4), `Adjustable_Payment_Cap_Amt`, `Prepayment_Penalty_Dt`, `Early_Payoff_Penalty_Amt`, `Agreement_Currency_Closing_Cost_Amt`, `Agreement_Currency_Adjustable_Cap_Amt`, `Agreement_Currency_Early_Penalty_Amt`, `Mortgage_Type_Cd`.
  - `CREDIT_CARD_AGREEMENT` (DDL §6186): 3 business + 3 DI = 6 cols. NOT NULL: `Agreement_Id`, `Credit_Card_Agreement_Subtype_Cd`. Nullable: `Credit_Card_Activation_Dttm`.
  - `CARD` (DDL §4583): 17 business + 3 DI = 20 cols. NOT NULL: `Access_Device_Id`, `Card_Association_Type_Cd`. Nullable: `Card_Subtype_Cd`, `Technology_Type_Cd`, `Card_Num` VARCHAR(50), `Card_Sequence_Num`, `Card_Expiration_Dt`, `Card_Issue_Dt`, `Card_Activation_Dt`, `Card_Deactivation_Dt`, `Card_Name`, `Card_Encrypted_Num`, `Card_Manufacture_Dt`, `Card_Replacement_Order_Dt`, `Language_Type_Cd`, `Bank_Identification_Num` VARCHAR(6), `Card_Security_Code_Num`. Per PRD §7.10, `Access_Device_Id` is BIGINT (overrides the DDL INTEGER). Note: `CARD` has **no** `Agreement_Id` column in the DDL — the agreement↔card link is handled in a separate Tier 10 event-layer table (AUTO-generated Access_Device FKs live there); for this step, the session emits `CARD` rows using fresh `Access_Device_Id` values from `ids.next('card')` **without** a cross-reference column. If the session finds the FK is expected anywhere, flag as a Conflict.
  - Footnotes §3103/§3104/§3118 — reiterate the BIGINT rule. Every `*_Id` emitted in this step is `Int64`.
- `references/06_supporting-enrichments.md` — open **only** these parts:
  - **Part C4** (§§190–209): mortgage loan term conventions (15–30 year fixed or ARM) — informs `LOAN_TERM_AGREEMENT.Loan_Maturity_Dt` offsets. Mortgages = `ag.open_dttm + 30 years`; auto loans = `+5 years`; student loans = `+10 years`; payday loans = `+30 days`; CDs use `DEPOSIT_TERM_AGREEMENT.Next_Term_Maturity_Dt` per the seeded maturity subtype (12M → `+1 year`, etc.).
  - **Part C6** (§§229–233): vehicle loan `Original_Loan_Amt` range — `$5K–$80K`, 3–5 year term. `ag.original_loan_amt` is already populated by Step 4 for all `is_loan_term` agreements — Tier 7b **reads `ag.original_loan_amt` verbatim** and does not re-sample.
  - **Part D1** (§§292–297): informs `First_Time_Mortgage_Ind`="Yes" heuristic — True when `ag.owner_party_id` owner's `CustomerProfile.age < 35` (session looks up via `{cp.party_id: cp for cp in ctx.customers}` index).

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is MVP-authoritative per PRD §10; only open `01` if `07` is ambiguous for a specific column.
- `references/05_architect-qa.md` — no Q touches Tier 7b directly (Q7 self-employment is Step 12; Q6 CDM_Address_Id is Step 22).
- `references/02_data-mapping-reference.md` — Tier 7b has **no Layer 2 literal-match requirements** (all Tier 7 Layer 2 literals are in Tier 7a: preferred currency, frozen status, rate feature, profitability score). Only open `02` if a question about a specific column's legal values cannot be answered from `07` + seed data.
- `references/06_supporting-enrichments.md` Parts A, B, C1–C3, C5, C7–C9, D2–D6, E–I, J — not needed.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `iDM_MDM_tables_DDLs.xlsx` — already distilled into `07`.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier7b_subtypes.py` — `class Tier7bSubtypes(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]`. Implementation contract:
  1. Import `BaseGenerator`; import `GenerationContext` / `AgreementProfile` under `TYPE_CHECKING` only. Import `pd`, `numpy as np` (only for RNG typing if needed — no sampling); `from datetime import datetime, date, timedelta`; `from decimal import Decimal`; `from utils.luhn import generate_card_number, generate_cvv`.
  2. Declare module-level constants (all reproducibility-friendly — **no `datetime.now()`**):
     - `_TIER7B_DI_START_TS = '2000-01-01 00:00:00.000000'` (matches `_TIER7A_DI_START_TS` convention).
     - `_BANKING_BOOK_CD = 'BANKING_BOOK'` (retail book classification — all MVP agreements).
     - `_FINANCIAL_AGREEMENT_TYPE_BY_PRODUCT: Dict[str, str]` mapping each of the 12 product types to one of `{DEPOSIT, LOAN, CREDIT, INVESTMENT, INSURANCE}` — MVP uses only DEPOSIT, LOAN, CREDIT. Deposits → `DEPOSIT`; credit card/HELOC → `CREDIT`; vehicle/student/mortgage/payday → `LOAN`.
     - `_INTEREST_DISBURSEMENT_BY_PRODUCT: Dict[str, str]` mapping each deposit product to one of `{COMPOUNDED, SIMPLE, ACCRUED, CAPITALIZED}`. Defaults: CHECKING/SAVINGS/MMA → `COMPOUNDED`; RETIREMENT → `ACCRUED`; CD → `SIMPLE`; COMMERCIAL_CHECKING → `COMPOUNDED`.
     - `_DEPOSIT_MATURITY_BY_PRODUCT: Dict[str, Optional[str]]` — CD → `'12M'` default (or distribute across 3M/6M/12M/24M/36M/60M via a deterministic hash on `ag.agreement_id` to spread). Others → `None`.
     - `_SECURITY_TYPE_BY_PRODUCT: Dict[str, str]` — VEHICLE_LOAN → `'VEHICLE'`, MORTGAGE → `'REAL_ESTATE'`, STUDENT_LOAN → `'UNSECURED'`, HELOC → `'REAL_ESTATE'`, CREDIT_CARD → `'UNSECURED'`, PAYDAY → `'UNSECURED'`.
     - `_LOAN_MATURITY_BY_PRODUCT: Dict[str, str]` — VEHICLE_LOAN → `'SHORT_TERM'`, STUDENT_LOAN → `'MEDIUM_TERM'`, MORTGAGE → `'LONG_TERM'`, PAYDAY → `'SHORT_TERM'`. (PAYDAY only appears in LOAN_TRANSACTION_AGREEMENT, not LOAN_AGREEMENT — so this mapping needs entries only for is_loan_term products.)
     - `_LOAN_TERM_SUBTYPE_BY_PRODUCT: Dict[str, str]` — VEHICLE_LOAN → `'INSTALLMENT'`, STUDENT_LOAN → `'INSTALLMENT'`, MORTGAGE → `'AMORTIZING'`.
     - `_AMORTIZATION_METHOD_BY_PRODUCT: Dict[str, str]` — VEHICLE_LOAN → `'LEVEL_PAYMENT'`, STUDENT_LOAN → `'LEVEL_PAYMENT'`, MORTGAGE → `'LEVEL_PAYMENT'` (ARMs are still level for fixed period; acceptable MVP simplification).
     - `_LOAN_TRANSACTION_SUBTYPE_BY_PRODUCT: Dict[str, str]` — PAYDAY → `'PAYDAY'`.
     - `_MORTGAGE_TYPE_BY_AG_HASH: List[str]` — mortgage distribution across `{FIXED_RATE, ARM, FHA, VA, JUMBO}` (exclude HELOC — that's its own product) via deterministic hash `ag.agreement_id % 5`. Baseline mix: FIXED_RATE 60%, ARM 20%, FHA 10%, VA 5%, JUMBO 5% — but deterministic bucketing is acceptable (session picks a simple mod-based distribution).
     - `_CC_SUBTYPE_BY_AG_HASH: List[str]` — credit-card distribution across `{STANDARD, REWARDS, SECURED, BUSINESS, STUDENT}` via deterministic hash `ag.agreement_id % 5`. Simple round-robin bucketing.
     - `_OBLIGOR_BORROWING_PURPOSE_BY_PRODUCT: Dict[str, str]` — CREDIT_CARD → `'GENERAL'`, HELOC → `'HOME_IMPROVEMENT'`, VEHICLE_LOAN → `'VEHICLE'`, STUDENT_LOAN → `'EDUCATION'`, MORTGAGE → `'HOME_PURCHASE'`. **Session verifies whether a seed table constrains these values**; if `Core_DB.PURCHASE_INTENT_TYPE` is present in `ctx.tables` (from Step 8 `misc_types.py` or similar), the literals must appear there — if they don't, either seed them or add a ⚠️ Conflict block and use whatever literals are seeded. (The DDL declares `Obligor_Borrowing_Purpose_Cd VARCHAR(50) NOT NULL` but lists no FK; the session's baseline is to use the literals above and document in handoff.)
     - `_CREDIT_GRACE_PERIOD_BY_PRODUCT: Dict[str, str]` — CREDIT_CARD → `'25_DAYS'`, HELOC → `'30_DAYS'`, VEHICLE_LOAN/STUDENT_LOAN/MORTGAGE → `'NONE'`. Same caveat about seed-table constraint — verify or document.
     - `_CARD_ASSOCIATION_TYPES: Tuple[str, ...]` — `('VISA', 'MASTERCARD', 'AMEX', 'DISCOVER')`. Assignment by deterministic hash `Access_Device_Id % 4`.
     - `_CARD_BIN_BY_ASSOCIATION: Dict[str, str]` — `{'VISA': '400000', 'MASTERCARD': '510000', 'AMEX': '340000', 'DISCOVER': '601100'}`. The first 6 digits of every Luhn-valid `Card_Num`.
     - `_CARD_SUBTYPE_BY_ROLE: Dict[str, str]` — `{'CREDIT_CARD': 'CREDIT', 'CHECKING': 'DEBIT'}` — `Card_Subtype_Cd` literal.
  3. Declare `_COLS_*` list-of-str module constants for every emitted DataFrame in **DDL declaration order** (see the DDL blocks cited in ## Reads from). DI columns are appended by `stamp_di()` — do NOT include them in `_COLS_*`. Example for DEPOSIT_AGREEMENT:
     ```python
     _COLS_DEPOSIT_AGREEMENT = [
         'Agreement_Id', 'Deposit_Maturity_Subtype_Cd', 'Interest_Disbursement_Type_Cd',
         'Deposit_Ownership_Type_Cd', 'Original_Deposit_Amt', 'Original_Deposit_Dt',
         'Agreement_Currency_Original_Deposit_Amt',
     ]
     ```
  4. **Guard** at the top of `generate()`: verify `ctx.agreements` is non-empty; verify every required Tier 0 / Tier 2 upstream table is present in `ctx.tables` (use an explicit `_REQUIRED_UPSTREAM_TABLES` tuple covering the 11 seed tables listed in ## Depends on Step 6 + `Core_DB.AGREEMENT` from Step 10). Raise `RuntimeError(f"Tier 7b prerequisite missing: {key}")` on any failure — do NOT silently improvise a fallback.
  5. Build `FINANCIAL_AGREEMENT` DataFrame — **one row per agreement where `ag.is_financial`** (currently all ~5,000). `Market_Risk_Type_Cd = _BANKING_BOOK_CD` (retail); `Financial_Agreement_Type_Cd = _FINANCIAL_AGREEMENT_TYPE_BY_PRODUCT[ag.product_type]`; `Original_Maturity_Dt` = product-specific: mortgages `ag.open_dttm.date() + timedelta(days=365*30)`, vehicle `+5y`, student `+10y`, CD per `_DEPOSIT_MATURITY_BY_PRODUCT`, others `None`. `Financial_Agreement_Subtype_Cd = ag.agreement_subtype_cd` (matches `AgreementProfile.agreement_subtype_cd`, which Step 4 set to `product_type` — `CHECKING`, `MORTGAGE`, etc.). All other nullable columns = `None`.
  6. Build `DEPOSIT_AGREEMENT` DataFrame — one row per agreement where `ag.is_deposit`. `Interest_Disbursement_Type_Cd = _INTEREST_DISBURSEMENT_BY_PRODUCT[ag.product_type]`. `Deposit_Maturity_Subtype_Cd = _DEPOSIT_MATURITY_BY_PRODUCT.get(ag.product_type)` (populated only for CDs). `Original_Deposit_Amt = ag.balance_amt` (opening deposit ≈ current balance for MVP). `Original_Deposit_Dt = ag.open_dttm.date()`. `Agreement_Currency_Original_Deposit_Amt = ag.balance_amt` (USD only). `Deposit_Ownership_Type_Cd = None`.
  7. Build `DEPOSIT_TERM_AGREEMENT` DataFrame — one row per agreement where `ag.is_term_deposit` (CDs only). `Next_Term_Maturity_Dt` = `ag.open_dttm.date() + timedelta(days=<maturity_subtype_days>)` (12M → 365, 6M → 183, etc.). `Grace_Period_End_Dt` = `Next_Term_Maturity_Dt + timedelta(days=10)`.
  8. Build `CREDIT_AGREEMENT` DataFrame — one row per agreement where `ag.is_credit`. `Obligor_Borrowing_Purpose_Cd = _OBLIGOR_BORROWING_PURPOSE_BY_PRODUCT[ag.product_type]`; `Credit_Agreement_Grace_Period_Cd = _CREDIT_GRACE_PERIOD_BY_PRODUCT[ag.product_type]`. For delinquent agreements (`ag.is_delinquent`): `Credit_Agreement_Past_Due_Amt = ag.balance_amt * Decimal('0.03')` (3% of balance as typical past-due size); `Agreement_Currency_Past_Due_Amt` = same. For severely delinquent (`ag.is_severely_delinquent`): `Credit_Agreement_Charge_Off_Amt = ag.balance_amt * Decimal('0.10')`. `Credit_Agreement_Subtype_Cd = ag.agreement_subtype_cd`. `Payment_Frequency_Time_Period_Cd = 'MONTH'` (session verifies `'MONTH'` is in seeded `TIME_PERIOD_TYPE` — if absent, fall back to any seeded code and document). `Seniority_Level_Cd = 'SENIOR'` or `None` if seed table absent. `Credit_Agreement_Reaging_Cnt = 0` (BIGINT). `Credit_Agreement_Last_Payment_Amt` / `Credit_Agreement_Last_Payment_Dt` / `Agreement_Currency_Last_Payment_Amt` populated with representative values (e.g., last_payment = balance * 0.02 monthly; last_dt = `ag.open_dttm + 30 days * (months_since_open - 1)` snapped to a date). Other nullable amount columns = `None`.
  9. Build `LOAN_AGREEMENT` DataFrame — one row per agreement where `ag.is_loan_term` (vehicle/student/mortgage). `Security_Type_Cd = _SECURITY_TYPE_BY_PRODUCT[ag.product_type]`; `Loan_Maturity_Subtype_Cd = _LOAN_MATURITY_BY_PRODUCT[ag.product_type]`. `Due_Day_Num` = `str(ag.open_dttm.day)` (matches origination day-of-month). `Loan_Payoff_Amt = ag.balance_amt` (outstanding principal); `Agreement_Currency_Loan_Payoff_Amt` = same. `Realizable_Collateral_Amt` = `ag.original_loan_amt * Decimal('1.10')` for mortgages/vehicle (collateral typically ≥ loan); `None` for unsecured. `Agreement_Currency_Real_Collateral_Amt` = same value.
  10. Build `LOAN_TERM_AGREEMENT` DataFrame — one row per agreement where `ag.is_loan_term`. `Amortization_Method_Cd = _AMORTIZATION_METHOD_BY_PRODUCT[ag.product_type]`; `Loan_Term_Subtype_Cd = _LOAN_TERM_SUBTYPE_BY_PRODUCT[ag.product_type]`. `Original_Loan_Amt = ag.original_loan_amt` (Decimal, verbatim from Step 4). `Agreement_Currency_Original_Loan_Amt` = same. `Loan_Maturity_Dt` = product-specific offset (mortgage 30y, vehicle 5y, student 10y). `Amortization_End_Dt = Loan_Maturity_Dt`. Other amounts/dates populated with plausible values where a column exists: `Down_Payment_Amt = ag.original_loan_amt * Decimal('0.20')` for mortgages (20% down), `Decimal('0')` otherwise; `Maximum_Monthly_Payment_Amt` derived from amortization formula `original_loan_amt * rate_monthly / (1 - (1 + rate_monthly)**-n)` — session may use a simplified approximation (e.g., `ag.original_loan_amt / total_months * Decimal('1.3')`) and document. `Loan_Refinance_Ind = 'No'`. Other nullable fields = `None`.
  11. Build `LOAN_TRANSACTION_AGREEMENT` DataFrame — one row per agreement where `ag.is_loan_transaction` (payday only). `Loan_Transaction_Subtype_Cd = _LOAN_TRANSACTION_SUBTYPE_BY_PRODUCT[ag.product_type]` (`'PAYDAY'`).
  12. Build `MORTGAGE_AGREEMENT` DataFrame — one row per agreement where `ag.is_mortgage`. `Mortgage_Type_Cd` = hash-bucketed across `_MORTGAGE_TYPE_BY_AG_HASH` (`FIXED_RATE | ARM | FHA | VA | JUMBO`). `First_Time_Mortgage_Ind` = `'Yes'` when the owner `CustomerProfile.age < 35`, else `'No'` — build a `{party_id: age}` lookup dict from `ctx.customers` once at the top of `generate()`. `Closing_Cost_Amt = ag.original_loan_amt * Decimal('0.03')` (3% typical). `Agreement_Currency_Closing_Cost_Amt` = same. `Adjustable_Payment_Cap_Amt = ag.original_loan_amt * Decimal('1.2')` for ARM mortgages, `None` for fixed-rate (session conditions on `Mortgage_Type_Cd`). `Early_Payoff_Penalty_Amt = ag.original_loan_amt * Decimal('0.01')` for the first 3 years then `None`; session may simplify to a flat value. `Prepayment_Penalty_Dt = ag.open_dttm.date() + timedelta(days=365*3)`.
  13. Build `CREDIT_CARD_AGREEMENT` DataFrame — one row per agreement where `ag.is_credit_card`. `Credit_Card_Agreement_Subtype_Cd` = hash-bucketed across `_CC_SUBTYPE_BY_AG_HASH` (`STANDARD | REWARDS | SECURED | BUSINESS | STUDENT`). `Credit_Card_Activation_Dttm = ag.open_dttm` (activated on agreement open).
  14. Build `CARD` DataFrame — **two sources**:
      - **Credit cards**: one row per agreement where `ag.is_credit_card`. `Access_Device_Id = ids.next('card')`; `Card_Subtype_Cd = 'CREDIT'`; `Card_Association_Type_Cd = _CARD_ASSOCIATION_TYPES[Access_Device_Id % 4]`. `Card_Num = generate_card_number(ctx.rng, bin_prefix=_CARD_BIN_BY_ASSOCIATION[Card_Association_Type_Cd])`. `Bank_Identification_Num = Card_Num[:6]`. `Card_Security_Code_Num = generate_cvv(ctx.rng)`. `Card_Issue_Dt = ag.open_dttm.date()`. `Card_Activation_Dt = ag.open_dttm.date()`. `Card_Expiration_Dt = ag.open_dttm.date() + timedelta(days=365*4)` (4-year expiry). `Card_Deactivation_Dt = None` (active). `Card_Manufacture_Dt = ag.open_dttm.date() - timedelta(days=7)`. `Card_Name = 'Visa Platinum'` / `'Mastercard Gold'` / etc. (session picks one per association). `Card_Encrypted_Num = Card_Num` (MVP — no encryption). `Technology_Type_Cd = 'CHIP_AND_PIN'`. `Language_Type_Cd = 'EN'` (ISO 639-1).
      - **Debit cards (checking deposits)**: one row per agreement where `ag.product_type == 'CHECKING' or ag.product_type == 'COMMERCIAL_CHECKING'`. Same field population as credit cards, but `Card_Subtype_Cd = 'DEBIT'`.
      - `Card_Sequence_Num = '1'` (first issued card for this account; re-issues would increment).
      - Row count = `#(is_credit_card) + #(product_type in ('CHECKING','COMMERCIAL_CHECKING'))`.
      - **Note on Luhn**: `ctx.rng` is consumed here (Tier 7b IS allowed to read `ctx.rng` — unlike Tier 7a which was pure-deterministic). Reproducibility is preserved because `ctx.rng` is seeded from `config.settings.SEED = 42`.
  15. Apply dtype conversions — cast every `*_Id` column and `Access_Device_Id` to `Int64` (nullable BIGINT), `Credit_Agreement_Reaging_Cnt` to `Int64`, every DECIMAL column to Python Decimal (pandas stores as `object`). Timestamps stay as `datetime`; dates as `date`.
  16. Stamp all **10** DataFrames via `self.stamp_di(df, start_ts=_TIER7B_DI_START_TS)`. Do NOT call `stamp_valid()` (all Core_DB; no CDM/PIM tables).
  17. Return a dict with exactly these 10 keys (no more, no fewer):
      ```
      {
        'Core_DB.FINANCIAL_AGREEMENT', 'Core_DB.DEPOSIT_AGREEMENT',
        'Core_DB.DEPOSIT_TERM_AGREEMENT', 'Core_DB.CREDIT_AGREEMENT',
        'Core_DB.LOAN_AGREEMENT', 'Core_DB.LOAN_TERM_AGREEMENT',
        'Core_DB.LOAN_TRANSACTION_AGREEMENT', 'Core_DB.MORTGAGE_AGREEMENT',
        'Core_DB.CREDIT_CARD_AGREEMENT', 'Core_DB.CARD',
      }
      ```

**Do NOT produce** in this step:
- CSVs — writer is not invoked.
- Any Tier 7a cross-cutting table (AGREEMENT_STATUS / AGREEMENT_CURRENCY / AGREEMENT_SCORE / AGREEMENT_FEATURE / AGREEMENT_METRIC / AGREEMENT_RATE / INTEREST_INDEX_RATE / VARIABLE_INTEREST_RATE_FEATURE / TERM_FEATURE) — those are Step 16.
- Any AGREEMENT top-level or AGREEMENT_SUBTYPE table — those are Step 10 / Step 8.
- Wiring into `main.py` — orchestrator changes are Step 25.

## Tables generated (if applicable)

After `Tier7bSubtypes().generate(ctx)` runs, `ctx.tables` gains these 10 Core_DB keys (row counts assume ~5,000 agreements distributed per `_PRODUCT_FLAGS` and roughly the per-product cohort rates set in Step 4):

| Table | Approx rows | Driven by | Notes |
|-------|------------:|-----------|-------|
| `Core_DB.FINANCIAL_AGREEMENT` | ≈ 5,000 (all agreements have `is_financial=True` per `_PRODUCT_FLAGS`) | per-agreement, `ag.is_financial` | `Market_Risk_Type_Cd='BANKING_BOOK'` for all MVP agreements |
| `Core_DB.DEPOSIT_AGREEMENT` | #(CHECKING+SAVINGS+MMA+RETIREMENT+CD+COMMERCIAL_CHECKING) | `ag.is_deposit` | `Interest_Disbursement_Type_Cd` NOT NULL — product-specific literal |
| `Core_DB.DEPOSIT_TERM_AGREEMENT` | #CD (terminal leaf for `is_term_deposit`) | `ag.is_term_deposit` | Only CDs populate this table |
| `Core_DB.CREDIT_AGREEMENT` | #(CREDIT_CARD+HELOC+VEHICLE_LOAN+STUDENT_LOAN+MORTGAGE) | `ag.is_credit` | PAYDAY is NOT in CREDIT chain per `_PRODUCT_FLAGS`; `Obligor_Borrowing_Purpose_Cd` + `Credit_Agreement_Grace_Period_Cd` NOT NULL |
| `Core_DB.LOAN_AGREEMENT` | #(VEHICLE_LOAN+STUDENT_LOAN+MORTGAGE) | `ag.is_loan_term` | `Security_Type_Cd` NOT NULL — product-specific literal |
| `Core_DB.LOAN_TERM_AGREEMENT` | #(VEHICLE_LOAN+STUDENT_LOAN+MORTGAGE) | `ag.is_loan_term` | `Amortization_Method_Cd` + `Loan_Term_Subtype_Cd` NOT NULL; `Original_Loan_Amt = ag.original_loan_amt` verbatim |
| `Core_DB.LOAN_TRANSACTION_AGREEMENT` | #PAYDAY | `ag.is_loan_transaction` | Terminal leaf for payday-loan path |
| `Core_DB.MORTGAGE_AGREEMENT` | #MORTGAGE | `ag.is_mortgage` | Hash-bucketed `Mortgage_Type_Cd`; `First_Time_Mortgage_Ind` per owner age<35 |
| `Core_DB.CREDIT_CARD_AGREEMENT` | #CREDIT_CARD | `ag.is_credit_card` | `Credit_Card_Agreement_Subtype_Cd` NOT NULL — hash-bucketed |
| `Core_DB.CARD` | #CREDIT_CARD + #(CHECKING+COMMERCIAL_CHECKING) | cardable-agreement union | `Card_Num` Luhn-valid 16-digit; `Bank_Identification_Num` = first 6 digits; `Card_Security_Code_Num` = 3-digit CVV |

All 10 emitted DataFrames have the 5-column DI tail after `stamp_di()` with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. No `stamp_valid()` is called.

**Exclusive-subtyping invariant:** exactly one of `{is_term_deposit, is_mortgage, is_credit_card, is_loan_transaction}` terminal flags is True per agreement **when the agreement terminates at that level** — BUT some products terminate at intermediate levels (CHECKING terminates at DEPOSIT; HELOC at CREDIT; VEHICLE_LOAN/STUDENT_LOAN at LOAN_TERM). The session's DoD uses per-product table-membership partitioning to verify the invariant rather than relying on any single "terminal" count.

## ⚠️ Conflict handling protocol (conditional — only activates if triggered during implementation)

Five upstream gaps could be discovered during implementation. Do NOT silently improvise — escalate per Handoff Protocol §2 and add a `⚠️ Conflict` block to this spec:

1. **`Obligor_Borrowing_Purpose_Cd` / `Credit_Agreement_Grace_Period_Cd` literals not seeded.** CREDIT_AGREEMENT declares both NOT NULL, and the DDL does not name an FK lookup table. Session must verify: (a) is there a `PURCHASE_INTENT_TYPE` or equivalent seeded in Step 8 that constrains `Obligor_Borrowing_Purpose_Cd`? (b) is there any seeded table for `Credit_Agreement_Grace_Period_Cd`? If either is absent, use the spec-suggested literals (`'GENERAL'`, `'HOME_IMPROVEMENT'`, etc.; `'25_DAYS'`, `'30_DAYS'`, `'NONE'`) and document the choice in a `⚠️ Conflict` block.
2. **`Card_Association_Type_Cd` literal not seeded.** CARD declares `Card_Association_Type_Cd VARCHAR(50) NOT NULL` but no association-type seed table exists in the design list. Use `{VISA, MASTERCARD, AMEX, DISCOVER}` as authoritative MVP literals and document in the handoff.
3. **`Payment_Frequency_Time_Period_Cd = 'MONTH'` not in seeded `TIME_PERIOD_TYPE`.** If Step 8 seeded only `{DAY, MONTH, YEAR}` (per Step 16 spec), this is fine; if not, fall back to the first row of `TIME_PERIOD_TYPE` and document.
4. **`CARD` has no `Agreement_Id` column per DDL.** This is expected — the DDL declares `Access_Device_Id` as PK with no back-reference. If the session finds the `agreement_id → access_device_id` link is required by a later tier (Step 20 events touch `ACCESS_DEVICE_EVENT`), flag it here and propose an internal in-memory mapping (not a CSV column change).
5. **`_PRODUCT_FLAGS` row for any product changes upstream.** Tier 7b depends on the exact flag mapping at `registry/universe.py:40`. If a future refactor alters the flags for an existing product (e.g., adds `is_credit=True` to PAYDAY), the row counts and DoD checks below will drift. The session's DoD verifies table membership partitions are consistent with the current flag definition — no change in Tier 7b code is needed, but the DoD row-count expectations will auto-adjust.

## Files to modify

No files modified. `config/settings.py`, `config/code_values.py`, `config/distributions.py`, `utils/*`, `registry/*`, `seed_data/*`, all existing `generators/*.py`, `output/*`, `main.py`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/*`, `CLAUDE.md` are all **NOT touched**.

If implementation discovers that `references/07_mvp-schema-reference.md` disagrees with this spec on any column name, type, or nullability (beyond those flagged above), escalate per Handoff Protocol §2 — update the upstream reference or add a new `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new dependencies. This step uses only `pandas`, `numpy`, `python-dateutil` (all in `requirements.txt` from Step 1) plus standard library + existing project modules (`utils.luhn`, `utils.id_factory`, `generators.base`).

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — every `*_Id` column and `Access_Device_Id` in every output DataFrame is emitted as pandas `Int64Dtype()` (nullable BIGINT) or `int64` (when all non-null). `Credit_Agreement_Reaging_Cnt` (DDL declares INTEGER) is also BIGINT. The DDL in `07` declares INTEGER for all these — the BIGINT rule wins per footnotes §3103/§3104/§3118.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — **n/a for Tier 7b**: no `Party_Id` column is emitted. Every row is agreement-scoped or device-scoped.
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on all 10 DataFrames.
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts = HIGH_TS` stamped via `stamp_di()` default. `Valid_To_Dt` **n/a**: Tier 7b is all Core_DB; no `stamp_valid()`.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — **n/a**: Tier 7b is all Core_DB. Do NOT call `stamp_valid()`.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** — every DataFrame is constructed via `pd.DataFrame(rows, columns=_COLS_<TABLE>)` where `_COLS_<TABLE>` is the authoritative business-column list (DI columns appended by `stamp_di()` at the end, matching the Tier 2/7a pattern).
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — **n/a**: not touched in this step (Step 22).
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — **n/a**: not touched in this step.
- **No ORMs, no database connections — pure pandas → CSV** — writer not invoked; generator returns DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — the only source of randomness in Tier 7b is `utils.luhn.generate_card_number(ctx.rng, ...)` and `utils.luhn.generate_cvv(ctx.rng)` for CARD rows. All other fields are deterministic (per-product literals, deterministic hashes on `ag.agreement_id` or `Access_Device_Id`). Two back-to-back runs must produce byte-identical DataFrames.

Step-specific rules (Tier 7b):

- **Exclusive sub-typing (PRD §7.5).** Tier 7b performs **no** sub-type decisions. Every row is emitted on the basis of an `ag.is_*` flag set by Step 4. The session's DoD verifies via flag-partitioning that each agreement appears in the correct **set** of tables (e.g., a mortgage appears in FINANCIAL + CREDIT + LOAN + LOAN_TERM + MORTGAGE; a checking account appears in FINANCIAL + DEPOSIT only).

- **Luhn validity (PRD §6 library mandate, Step 2 util).** Every `Card_Num` in `Core_DB.CARD` must pass `utils.luhn.luhn_check()`. The session's DoD runs `luhn_check()` on every row.

- **BIN prefix → Card Association consistency.** `Bank_Identification_Num` = `Card_Num[:6]` and must equal `_CARD_BIN_BY_ASSOCIATION[Card_Association_Type_Cd]`. The DoD verifies this equality across all rows.

- **`Access_Device_Id` uniqueness.** All CARD rows have distinct `Access_Device_Id` values (monotonic from `ids.next('card')`). DoD asserts `df.Access_Device_Id.is_unique`.

- **`ag.original_loan_amt` is authoritative for LOAN_TERM_AGREEMENT.Original_Loan_Amt and derived columns.** Do NOT re-sample from `06 Part C4/C6` — UniverseBuilder already applied the per-product range at Step 4. Tier 7b reads `ag.original_loan_amt` verbatim and derives `Down_Payment_Amt`, `Closing_Cost_Amt`, etc. from it.

- **`ag.balance_amt` is authoritative for DEPOSIT_AGREEMENT.Original_Deposit_Amt and CREDIT_AGREEMENT.*Past_Due/Charge_Off_Amt.** Do NOT re-sample from Part C1–C3 — the balance comes from Step 4.

- **Loan maturity offset rules.**
  - MORTGAGE: 30 years (`timedelta(days=365*30)`)
  - STUDENT_LOAN: 10 years
  - VEHICLE_LOAN: 5 years
  - PAYDAY (LOAN_TRANSACTION): 30 days (not used in LOAN_AGREEMENT, only if the session elects to populate `Commit_End_Dt` etc. in LOAN_TERM_AGREEMENT)
  - CD deposit term: 1 year default, or bucket per `Deposit_Maturity_Subtype_Cd` (3M=91d, 6M=183d, 12M=365d, 24M=730d, 36M=1095d, 60M=1825d).

- **First-Time-Mortgage heuristic (MVP simplification).** `First_Time_Mortgage_Ind = 'Yes'` when the owning customer's `CustomerProfile.age < 35`; else `'No'`. The session builds an `owner_age_by_party_id = {cp.party_id: cp.age for cp in ctx.customers}` dict once at the top of `generate()`.

- **CHAR(3) flags are `'Yes'` / `'No'`** (per PRD §4.3). Applies to `Loan_Refinance_Ind` (LOAN_TERM_AGREEMENT) and `First_Time_Mortgage_Ind` (MORTGAGE_AGREEMENT). No `Y`/`N` here — those are CHAR(1). DoD verifies both fields use `'Yes'`/`'No'`.

- **No side effects on import.** `import generators.tier7b_subtypes` must not construct any DataFrames, call `generate()`, read any file, or mint any IDs. Enforced by the "no import-time DataFrames" check in Definition of done.

- **No Faker.** `faker` is seeded in UniverseBuilder and used only there. Tier 7b uses only `ctx.rng` (for Luhn), numeric/string literals, and dates derived from `ag` fields. Enforced by a grep check in DoD.

- **Escalation over improvisation.** If `07` has an ambiguity beyond those flagged in the Conflict handling protocol above (column name differs, nullability unclear, DDL type surprising), stop and add a new `⚠️ Conflict` block to this spec. Do NOT invent columns.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is CWD and `python` resolves to the project's Python 3.12 environment. Each check uses a fresh ctx built via UniverseBuilder + Tier 0 + Tier 1 + Tier 2 before invoking Tier 7b. The session may DRY the bootstrap into a reusable temp helper.

### Bootstrap helper (used by subsequent checks)

```bash
cat > /tmp/_tier7b_bootstrap.py <<'PY'
import numpy as np
import config.settings as _s
from config.settings import SEED
from registry.universe import UniverseBuilder
from generators.tier0_lookups import Tier0Lookups
from generators.tier1_geography import Tier1Geography
from generators.tier2_core import Tier2Core
from generators.tier7b_subtypes import Tier7bSubtypes

def build():
    ctx = UniverseBuilder().build(_s, np.random.default_rng(SEED))
    for t in (Tier0Lookups(), Tier1Geography(), Tier2Core()):
        ctx.tables.update(t.generate(ctx))
    out = Tier7bSubtypes().generate(ctx)
    return ctx, out
PY
```

### Module-import and API contract

- [ ] `python -c "import generators.tier7b_subtypes"` exits 0.
- [ ] Generator class inherits from `BaseGenerator` and defines `generate(ctx)`. Run:
  ```bash
  python -c "
  from generators.tier7b_subtypes import Tier7bSubtypes
  from generators.base import BaseGenerator
  import inspect
  assert issubclass(Tier7bSubtypes, BaseGenerator)
  sig = inspect.signature(Tier7bSubtypes.generate)
  assert 'ctx' in sig.parameters
  print('class contract OK')
  "
  ```

### Tables produced

- [ ] `Tier7bSubtypes().generate(ctx)` returns **exactly these 10 Core_DB keys** — no more, no fewer. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  expected = {
      'Core_DB.FINANCIAL_AGREEMENT','Core_DB.DEPOSIT_AGREEMENT',
      'Core_DB.DEPOSIT_TERM_AGREEMENT','Core_DB.CREDIT_AGREEMENT',
      'Core_DB.LOAN_AGREEMENT','Core_DB.LOAN_TERM_AGREEMENT',
      'Core_DB.LOAN_TRANSACTION_AGREEMENT','Core_DB.MORTGAGE_AGREEMENT',
      'Core_DB.CREDIT_CARD_AGREEMENT','Core_DB.CARD',
  }
  assert set(out.keys()) == expected, set(out.keys()) ^ expected
  assert len(out) == 10
  print(f'Tier7b produced {len(out)} tables (expected 10)')
  "
  ```

### Row counts by flag

- [ ] Row counts match the per-flag contract. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  ags = ctx.agreements
  n_fin = sum(1 for a in ags if a.is_financial)
  n_dep = sum(1 for a in ags if a.is_deposit)
  n_td  = sum(1 for a in ags if a.is_term_deposit)
  n_cr  = sum(1 for a in ags if a.is_credit)
  n_lt  = sum(1 for a in ags if a.is_loan_term)
  n_mg  = sum(1 for a in ags if a.is_mortgage)
  n_cc  = sum(1 for a in ags if a.is_credit_card)
  n_lx  = sum(1 for a in ags if a.is_loan_transaction)
  n_chk = sum(1 for a in ags if a.product_type in ('CHECKING','COMMERCIAL_CHECKING'))
  assert len(out['Core_DB.FINANCIAL_AGREEMENT'])          == n_fin
  assert len(out['Core_DB.DEPOSIT_AGREEMENT'])            == n_dep
  assert len(out['Core_DB.DEPOSIT_TERM_AGREEMENT'])       == n_td
  assert len(out['Core_DB.CREDIT_AGREEMENT'])             == n_cr
  assert len(out['Core_DB.LOAN_AGREEMENT'])               == n_lt
  assert len(out['Core_DB.LOAN_TERM_AGREEMENT'])          == n_lt
  assert len(out['Core_DB.LOAN_TRANSACTION_AGREEMENT'])   == n_lx
  assert len(out['Core_DB.MORTGAGE_AGREEMENT'])           == n_mg
  assert len(out['Core_DB.CREDIT_CARD_AGREEMENT'])        == n_cc
  assert len(out['Core_DB.CARD'])                         == n_cc + n_chk
  print('row counts OK')
  "
  ```

### Inheritance-chain completeness (Exclusive sub-typing, PRD §7.5)

- [ ] Each agreement appears in the correct **set** of tables based on its `is_*` flags. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  fin   = set(out['Core_DB.FINANCIAL_AGREEMENT'].Agreement_Id)
  dep   = set(out['Core_DB.DEPOSIT_AGREEMENT'].Agreement_Id)
  td    = set(out['Core_DB.DEPOSIT_TERM_AGREEMENT'].Agreement_Id)
  cr    = set(out['Core_DB.CREDIT_AGREEMENT'].Agreement_Id)
  la    = set(out['Core_DB.LOAN_AGREEMENT'].Agreement_Id)
  lta   = set(out['Core_DB.LOAN_TERM_AGREEMENT'].Agreement_Id)
  lx    = set(out['Core_DB.LOAN_TRANSACTION_AGREEMENT'].Agreement_Id)
  mg    = set(out['Core_DB.MORTGAGE_AGREEMENT'].Agreement_Id)
  cc    = set(out['Core_DB.CREDIT_CARD_AGREEMENT'].Agreement_Id)
  for a in ctx.agreements:
      aid = a.agreement_id
      assert (aid in fin) == a.is_financial,         f'{aid} financial mismatch'
      assert (aid in dep) == a.is_deposit,           f'{aid} deposit mismatch'
      assert (aid in td)  == a.is_term_deposit,      f'{aid} term_deposit mismatch'
      assert (aid in cr)  == a.is_credit,            f'{aid} credit mismatch'
      assert (aid in la)  == a.is_loan_term,         f'{aid} loan_agreement mismatch'
      assert (aid in lta) == a.is_loan_term,         f'{aid} loan_term mismatch'
      assert (aid in lx)  == a.is_loan_transaction,  f'{aid} loan_transaction mismatch'
      assert (aid in mg)  == a.is_mortgage,          f'{aid} mortgage mismatch'
      assert (aid in cc)  == a.is_credit_card,       f'{aid} credit_card mismatch'
  # Spot-checks for known chains: every mortgage has all 5 rows
  mortgage_ids = {a.agreement_id for a in ctx.agreements if a.product_type == 'MORTGAGE'}
  assert mortgage_ids <= (fin & cr & la & lta & mg), 'mortgage missing an inheritance level'
  # Every CHECKING has FIN + DEP only
  checking_ids = {a.agreement_id for a in ctx.agreements if a.product_type == 'CHECKING'}
  assert checking_ids <= (fin & dep), 'checking missing FIN or DEP'
  assert not (checking_ids & (td | cr | la | lta | lx | mg | cc)), 'checking leaked into non-deposit table'
  print('inheritance chain partitioning OK')
  "
  ```

### FK resolution to AGREEMENT

- [ ] Every `Agreement_Id` in every Tier 7b sub-type table resolves to `Core_DB.AGREEMENT.Agreement_Id`. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  ag_ids = set(ctx.tables['Core_DB.AGREEMENT'].Agreement_Id)
  for key in [k for k in out if k != 'Core_DB.CARD']:
      df = out[key]
      orphans = set(df.Agreement_Id) - ag_ids
      assert not orphans, f'{key}: {len(orphans)} orphan Agreement_Ids'
  print('Agreement_Id FK coverage OK (9 tables)')
  "
  ```

### NOT-NULL column enforcement

- [ ] Every NOT NULL column per the DDL is non-null in every row. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  required = {
      'Core_DB.FINANCIAL_AGREEMENT':       ['Agreement_Id','Market_Risk_Type_Cd'],
      'Core_DB.DEPOSIT_AGREEMENT':         ['Agreement_Id','Interest_Disbursement_Type_Cd'],
      'Core_DB.DEPOSIT_TERM_AGREEMENT':    ['Agreement_Id'],
      'Core_DB.CREDIT_AGREEMENT':          ['Agreement_Id','Obligor_Borrowing_Purpose_Cd','Credit_Agreement_Grace_Period_Cd'],
      'Core_DB.LOAN_AGREEMENT':            ['Agreement_Id','Security_Type_Cd'],
      'Core_DB.LOAN_TERM_AGREEMENT':       ['Agreement_Id','Amortization_Method_Cd','Loan_Term_Subtype_Cd'],
      'Core_DB.LOAN_TRANSACTION_AGREEMENT':['Agreement_Id'],
      'Core_DB.MORTGAGE_AGREEMENT':        ['Agreement_Id'],
      'Core_DB.CREDIT_CARD_AGREEMENT':     ['Agreement_Id','Credit_Card_Agreement_Subtype_Cd'],
      'Core_DB.CARD':                      ['Access_Device_Id','Card_Association_Type_Cd'],
  }
  for key, cols in required.items():
      df = out[key]
      for c in cols:
          assert df[c].notna().all(), f'{key}.{c} has NaN'
  print('NOT NULL columns OK')
  "
  ```

### Seeded-code FK coverage

- [ ] Every emitted sub-type code resolves to a seeded Tier 0 row. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  def subset(col, df, typ_key, typ_col):
      vals = set(out[df][col].dropna())
      seed = set(ctx.tables[typ_key][typ_col])
      orphans = vals - seed
      assert not orphans, f'{df}.{col} orphans: {orphans}'
  subset('Market_Risk_Type_Cd',               'Core_DB.FINANCIAL_AGREEMENT',        'Core_DB.MARKET_RISK_TYPE',            'Market_Risk_Type_Cd')
  subset('Financial_Agreement_Type_Cd',       'Core_DB.FINANCIAL_AGREEMENT',        'Core_DB.FINANCIAL_AGREEMENT_TYPE',    'Financial_Agreement_Type_Cd')
  subset('Interest_Disbursement_Type_Cd',     'Core_DB.DEPOSIT_AGREEMENT',          'Core_DB.INTEREST_DISBURSEMENT_TYPE',  'Interest_Disbursement_Type_Cd')
  subset('Deposit_Maturity_Subtype_Cd',       'Core_DB.DEPOSIT_AGREEMENT',          'Core_DB.DEPOSIT_MATURITY_SUBTYPE',    'Deposit_Maturity_Subtype_Cd')
  subset('Security_Type_Cd',                  'Core_DB.LOAN_AGREEMENT',             'Core_DB.SECURITY_TYPE',               'Security_Type_Cd')
  subset('Loan_Maturity_Subtype_Cd',          'Core_DB.LOAN_AGREEMENT',             'Core_DB.LOAN_MATURITY_SUBTYPE',       'Loan_Maturity_Subtype_Cd')
  subset('Amortization_Method_Cd',            'Core_DB.LOAN_TERM_AGREEMENT',        'Core_DB.AMORTIZATION_METHOD_TYPE',    'Amortization_Method_Cd')
  subset('Loan_Term_Subtype_Cd',              'Core_DB.LOAN_TERM_AGREEMENT',        'Core_DB.LOAN_TERM_SUBTYPE',           'Loan_Term_Subtype_Cd')
  subset('Loan_Transaction_Subtype_Cd',       'Core_DB.LOAN_TRANSACTION_AGREEMENT', 'Core_DB.LOAN_TRANSACTION_SUBTYPE',    'Loan_Transaction_Subtype_Cd')
  subset('Credit_Card_Agreement_Subtype_Cd',  'Core_DB.CREDIT_CARD_AGREEMENT',      'Core_DB.CREDIT_CARD_AGREEMENT_SUBTYPE','Credit_Card_Agreement_Subtype_Cd')
  subset('Mortgage_Type_Cd',                  'Core_DB.MORTGAGE_AGREEMENT',         'Core_DB.MORTGAGE_TYPE',               'Mortgage_Type_Cd')
  print('seeded-code FK coverage OK')
  "
  ```

### Original_Loan_Amt and balance pass-through

- [ ] `LOAN_TERM_AGREEMENT.Original_Loan_Amt` equals `ag.original_loan_amt` for every loan-term agreement. Run:
  ```bash
  python -c "
  from decimal import Decimal
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  lta = out['Core_DB.LOAN_TERM_AGREEMENT']
  ag_by_id = {a.agreement_id: a for a in ctx.agreements}
  for _, row in lta.iterrows():
      exp = ag_by_id[row.Agreement_Id].original_loan_amt
      assert Decimal(str(row.Original_Loan_Amt)) == Decimal(str(exp)), f'{row.Agreement_Id}: {row.Original_Loan_Amt} != {exp}'
  print('Original_Loan_Amt pass-through OK')
  "
  ```
- [ ] `DEPOSIT_AGREEMENT.Original_Deposit_Amt` equals `ag.balance_amt` for every deposit agreement. Run:
  ```bash
  python -c "
  from decimal import Decimal
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  dep = out['Core_DB.DEPOSIT_AGREEMENT']
  ag_by_id = {a.agreement_id: a for a in ctx.agreements}
  for _, row in dep.iterrows():
      exp = ag_by_id[row.Agreement_Id].balance_amt
      assert Decimal(str(row.Original_Deposit_Amt)) == Decimal(str(exp)), f'{row.Agreement_Id}: {row.Original_Deposit_Amt} != {exp}'
  print('Original_Deposit_Amt pass-through OK')
  "
  ```

### CARD Luhn validity and BIN consistency

- [ ] Every `CARD.Card_Num` passes the Luhn mod-10 check. Run:
  ```bash
  python -c "
  from utils.luhn import luhn_check
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  card = out['Core_DB.CARD']
  assert card.Card_Num.notna().all()
  bad = [n for n in card.Card_Num if not luhn_check(n)]
  assert not bad, f'{len(bad)} cards failed Luhn: sample {bad[:3]}'
  print(f'{len(card)} cards all pass Luhn')
  "
  ```
- [ ] Every `CARD.Bank_Identification_Num` equals `Card_Num[:6]` and is a 6-character digit string. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  card = out['Core_DB.CARD']
  for _, row in card.iterrows():
      assert row.Card_Num[:6] == row.Bank_Identification_Num, f'BIN mismatch: {row.Card_Num} vs {row.Bank_Identification_Num}'
      assert len(row.Bank_Identification_Num) == 6 and row.Bank_Identification_Num.isdigit()
  print('BIN prefix consistency OK')
  "
  ```
- [ ] Every `CARD.Access_Device_Id` is unique and BIGINT. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  card = out['Core_DB.CARD']
  assert card.Access_Device_Id.is_unique, 'duplicate Access_Device_Id'
  assert str(card.Access_Device_Id.dtype) in ('Int64','int64'), card.Access_Device_Id.dtype
  print(f'{len(card)} unique BIGINT Access_Device_Ids')
  "
  ```
- [ ] Every `CARD.Card_Security_Code_Num` is a 3-digit string. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  card = out['Core_DB.CARD']
  assert card.Card_Security_Code_Num.str.match(r'^[0-9]{3}$').all()
  print('CVV format OK')
  "
  ```

### CARD subtype partitioning (CREDIT + DEBIT)

- [ ] CARD row count = (#credit-card agreements) + (#CHECKING + #COMMERCIAL_CHECKING agreements), and `Card_Subtype_Cd` partitions accordingly. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  card = out['Core_DB.CARD']
  n_cc  = sum(1 for a in ctx.agreements if a.is_credit_card)
  n_chk = sum(1 for a in ctx.agreements if a.product_type in ('CHECKING','COMMERCIAL_CHECKING'))
  assert len(card) == n_cc + n_chk, (len(card), n_cc + n_chk)
  counts = card.Card_Subtype_Cd.value_counts().to_dict()
  assert counts.get('CREDIT', 0) == n_cc, counts
  assert counts.get('DEBIT', 0)  == n_chk, counts
  print(f'CARD partition OK: {n_cc} CREDIT + {n_chk} DEBIT = {len(card)} rows')
  "
  ```

### CHAR(3) flag values

- [ ] `Loan_Refinance_Ind` in LOAN_TERM_AGREEMENT and `First_Time_Mortgage_Ind` in MORTGAGE_AGREEMENT use only `'Yes'`/`'No'`. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  lt_vals = set(out['Core_DB.LOAN_TERM_AGREEMENT'].Loan_Refinance_Ind.dropna())
  mg_vals = set(out['Core_DB.MORTGAGE_AGREEMENT'].First_Time_Mortgage_Ind.dropna())
  assert lt_vals <= {'Yes','No'}, lt_vals
  assert mg_vals <= {'Yes','No'}, mg_vals
  print('CHAR(3) Yes/No literals OK')
  "
  ```

### BIGINT enforcement (PRD §7.1)

- [ ] Every `*_Id` column and `Access_Device_Id` in every produced DataFrame is `Int64` or `int64` dtype; `Credit_Agreement_Reaging_Cnt` is also BIGINT. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  bad = []
  for key, df in out.items():
      for c in df.columns:
          if c.endswith('_Id') or c == 'Access_Device_Id' or c == 'Credit_Agreement_Reaging_Cnt':
              if str(df[c].dtype) not in ('Int64','int64'):
                  bad.append(f'{key}.{c}: {df[c].dtype}')
  assert not bad, bad
  print('all BIGINT columns OK')
  "
  ```

### DI stamping

- [ ] Every produced DataFrame has the 5-column DI tail with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. Run:
  ```bash
  python -c "
  from config.settings import HIGH_TS
  from utils.di_columns import DI_COLUMN_ORDER
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  for key, df in out.items():
      tail = list(df.columns[-5:])
      assert tail == list(DI_COLUMN_ORDER), f'{key}: DI tail {tail}'
      assert (df.di_end_ts == HIGH_TS).all(), f'{key}: di_end_ts drift'
      assert (df.di_rec_deleted_Ind == 'N').all(), f'{key}: di_rec_deleted_Ind drift'
  print('DI stamping OK across all 10 tables')
  "
  ```
- [ ] No DataFrame has `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` columns (Core_DB does not stamp them). Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  for key, df in out.items():
      banned = {'Valid_From_Dt','Valid_To_Dt','Del_Ind'}
      present = banned & set(df.columns)
      assert not present, f'{key} has CDM/PIM columns: {present}'
  print('no Valid/Del_Ind on Core_DB tables')
  "
  ```

### DDL column-order enforcement

- [ ] Every DataFrame's business-column prefix (columns 0..N-6, excluding the 5-column DI tail) matches the authoritative DDL declaration order verbatim. This check is independent of the generator's `_COLS_*` constants — if a `_COLS_*` list was authored in the wrong order, this check fails before the writer would silently reorder. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  EXPECTED = {
      'Core_DB.FINANCIAL_AGREEMENT': [
          'Agreement_Id','Financial_Agreement_Subtype_Cd','Market_Risk_Type_Cd',
          'Original_Maturity_Dt','Risk_Exposure_Mitigant_Subtype_Cd','Trading_Book_Cd',
          'Pricing_Method_Subtype_Cd','Financial_Agreement_Type_Cd','Day_Count_Basis_Cd',
          'ISO_8583_Account_Type_Cd',
      ],
      'Core_DB.DEPOSIT_AGREEMENT': [
          'Agreement_Id','Deposit_Maturity_Subtype_Cd','Interest_Disbursement_Type_Cd',
          'Deposit_Ownership_Type_Cd','Original_Deposit_Amt','Original_Deposit_Dt',
          'Agreement_Currency_Original_Deposit_Amt',
      ],
      'Core_DB.DEPOSIT_TERM_AGREEMENT': [
          'Agreement_Id','Next_Term_Maturity_Dt','Grace_Period_End_Dt',
      ],
      'Core_DB.CREDIT_AGREEMENT': [
          'Agreement_Id','Seniority_Level_Cd','Credit_Agreement_Reaging_Cnt',
          'Credit_Agreement_Past_Due_Amt','Credit_Agreement_Charge_Off_Amt',
          'Credit_Agreement_Impairment_Amt','Credit_Agreement_Settlement_Dt',
          'Credit_Agreement_Subtype_Cd','Obligor_Borrowing_Purpose_Cd',
          'Agreement_Currency_Past_Due_Amt','Agreement_Currency_Charge_Off_Amt',
          'Agreement_Currency_Last_Payment_Amt','Agreement_Currency_Impairment_Amt',
          'Specialized_Lending_Type_Cd','Credit_Agreement_Grace_Period_Cd',
          'Payment_Frequency_Time_Period_Cd','Credit_Agreement_Last_Payment_Amt',
          'Credit_Agreement_Last_Payment_Dt',
      ],
      'Core_DB.LOAN_AGREEMENT': [
          'Agreement_Id','Loan_Maturity_Subtype_Cd','Security_Type_Cd','Due_Day_Num',
          'Realizable_Collateral_Amt','Loan_Payoff_Amt',
          'Agreement_Currency_Real_Collateral_Amt','Agreement_Currency_Loan_Payoff_Amt',
      ],
      'Core_DB.LOAN_TERM_AGREEMENT': [
          'Agreement_Id','Amortization_Method_Cd','Amortization_End_Dt','Balloon_Amt',
          'Loan_Term_Subtype_Cd','Original_Loan_Amt','Preapproved_Loan_Amt',
          'Maximum_Monthly_Payment_Amt','Improvement_Allocation_Amt',
          'Debt_Payment_Allocation_Amt','Down_Payment_Amt','Loan_Maturity_Dt',
          'Loan_Termination_Dt','Loan_Renewal_Dt','Commit_Start_Dt','Commit_End_Dt',
          'Payoff_Dt','Loan_Asset_Purchase_Dt','Agreement_Currency_Balloon_Amt',
          'Agreement_Currency_Original_Loan_Amt','Agreement_Currency_Preapproved_Amt',
          'Agreement_Currency_Maximum_Monthly_Payment_Amt',
          'Agreement_Currency_Improve_Allocation_Amt',
          'Agreement_Currency_Debt_Payment_Allocation_Amt','Loan_Refinance_Ind',
          'Agreement_Currency_Down_Payment_Amt','Agreement_Currency_Down_Payment_Borrow_Amt',
      ],
      'Core_DB.LOAN_TRANSACTION_AGREEMENT': [
          'Agreement_Id','Loan_Transaction_Subtype_Cd',
      ],
      'Core_DB.MORTGAGE_AGREEMENT': [
          'Agreement_Id','First_Time_Mortgage_Ind','Closing_Cost_Amt',
          'Adjustable_Payment_Cap_Amt','Prepayment_Penalty_Dt','Early_Payoff_Penalty_Amt',
          'Agreement_Currency_Closing_Cost_Amt','Agreement_Currency_Adjustable_Cap_Amt',
          'Agreement_Currency_Early_Penalty_Amt','Mortgage_Type_Cd',
      ],
      'Core_DB.CREDIT_CARD_AGREEMENT': [
          'Agreement_Id','Credit_Card_Agreement_Subtype_Cd','Credit_Card_Activation_Dttm',
      ],
      'Core_DB.CARD': [
          'Access_Device_Id','Card_Subtype_Cd','Card_Association_Type_Cd',
          'Technology_Type_Cd','Card_Num','Card_Sequence_Num','Card_Expiration_Dt',
          'Card_Issue_Dt','Card_Activation_Dt','Card_Deactivation_Dt','Card_Name',
          'Card_Encrypted_Num','Card_Manufacture_Dt','Card_Replacement_Order_Dt',
          'Language_Type_Cd','Bank_Identification_Num','Card_Security_Code_Num',
      ],
  }
  assert set(EXPECTED) == set(out), 'EXPECTED/out key mismatch'
  for key, expected_cols in EXPECTED.items():
      df = out[key]
      business = list(df.columns[:-5])  # strip 5-col DI tail
      assert business == expected_cols, (
          f'{key} column order drift.\\n  expected: {expected_cols}\\n  got:      {business}'
      )
  print(f'DDL column order OK across {len(EXPECTED)} tables')
  "
  ```

### Writer compatibility

- [ ] After stamping, every table passes `output.writer._reorder_to_ddl()`. Run:
  ```bash
  python -c "
  from output.writer import _reorder_to_ddl
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  ctx, out = build()
  for key, df in out.items():
      try: _reorder_to_ddl(df, key)
      except Exception as e: raise SystemExit(f'{key}: {e}')
  print(f'{len(out)} tables pass _reorder_to_ddl')
  "
  ```

### Prerequisite guard

- [ ] `Tier7bSubtypes.generate()` raises `RuntimeError` when an upstream prerequisite is missing. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier7b_subtypes import Tier7bSubtypes
  class Ctx:
      customers = []
      agreements = []
      ids = IdFactory(ID_RANGES)
      rng = np.random.default_rng(42)
      tables = {}
  try:
      Tier7bSubtypes().generate(Ctx())
      raise AssertionError('should have raised RuntimeError')
  except RuntimeError as e:
      assert 'AGREEMENT' in str(e) or 'Tier' in str(e) or 'prerequisite' in str(e).lower()
  print('Tier7b prerequisite guard OK')
  "
  ```

### Reproducibility

- [ ] Two back-to-back runs produce byte-identical DataFrames. Run:
  ```bash
  python -c "
  exec(open('/tmp/_tier7b_bootstrap.py').read())
  _, a = build()
  _, b = build()
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
  p = 'generators/tier7b_subtypes.py'
  bad = [f'{p}:{i}: {line}' for i, line in enumerate(pathlib.Path(p).read_text().splitlines(), 1) if pat.match(line)]
  assert not bad, bad
  print('no faker import')
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
  sys.modules.pop('generators.tier7b_subtypes', None)
  importlib.import_module('generators.tier7b_subtypes')
  pd.DataFrame = _orig
  assert calls['n'] == 0, f'{calls[\"n\"]} DataFrames built at import time'
  print('no import-time DataFrames')
  "
  ```

### Universal checks

- [ ] `git status --porcelain` shows only: `generators/tier7b_subtypes.py` (new) plus this spec file at `.claude/specs/step-17-tier7b-agreement-subtype-card.md` (already on branch). No stray files (no `__pycache__` in stage, no output CSVs, no edits under `config/`, `utils/`, `registry/`, `output/`, `references/`, `seed_data/`, other `generators/*.py`). Run:
  ```bash
  git status --porcelain
  ```
- [ ] All new files pass `python -c "import <module>"` — covered by the first Module-import check.
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — covered by the BIGINT dtype check above. **n/a for the CSV-on-disk variant**: this step produces no CSVs; writer is not invoked.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: not touched in this step (Step 22).
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSV output; writer not invoked. Tier 7b does not touch the GEOSPATIAL skip list.

## Handoff notes

_To be filled in at end of implementation session._

# Spec: Step 20 — Tier 10 Events

## Overview

This step builds **Tier 10 — Events**, the nine Core_DB tables that realise the banking-interaction plane on top of the party/agreement skeleton Steps 10/11/17/19 already projected. Two event streams interleave into a single `Core_DB.EVENT` spine:

- **Customer-level discretionary events** — 1–5 events per customer per month (cohort-modulated) representing logins, contacts, transfers, and complaints.
- **Account-level periodic events** — one monthly statement-fee event + one monthly interest accrual event per agreement (plus overdraft fee events for negative-balance months) guaranteed by the Layer 2 FINANCIAL_EVENT_AMOUNT derivations.

Every `EVENT` row takes **exactly one** of four mutually-exclusive sub-type paths — `{FINANCIAL_EVENT, ACCESS_DEVICE_EVENT, DIRECT_CONTACT_EVENT, COMPLAINT_EVENT}` — following the design-doc exclusive sub-typing contract (`mvp-tool-design.md` §9 Tier 10 + §7.5 extended to events). Events on the FINANCIAL path additionally receive one or more `FINANCIAL_EVENT_AMOUNT` rows and, for the transfer-type subset, a nested `FUNDS_TRANSFER_EVENT` row. Every event gets exactly one `EVENT_PARTY` row linking it to the driving customer and one `EVENT_CHANNEL_INSTANCE` row linking it to a channel from the 20-row Tier 2 pool. Cohort rules (per `references/06_supporting-enrichments.md` Part G2): ACTIVE holds steady, DECLINING tapers to zero across the 6-month window, CHURNED truncates at `Agreement_Close_Dttm`, NEW starts only from `Agreement_Open_Dttm`. Channel cost plausibility (Part H2: ~1 call/month per checking customer) and fee pairing (Part H3: recurring statement fee + intermittent overdraft fee) are enforced at generation. `COMPLAINT_EVENT` fires for ~5% of customers; its `Event_Id` is the seed that drives Step 21's Tier 13 `PARTY_TASK.Source_Event_Id` linkage. Every random decision routes through `ctx.rng` for reproducibility (PRD §7.6), and every `*_Id` is BIGINT per PRD §7.1. See `mvp-tool-design.md` §9 Tier 10 for scope and exemplar values.

## Depends on

- **Step 1** — consumes from `config/settings.py`: `HISTORY_START = date(2025, 10, 1)`, `SIM_DATE = date(2026, 3, 31)`, `HIGH_TS = '9999-12-31 00:00:00.000000'`, `ID_RANGES['event'] = 50_000_000`. No new `ID_RANGES` category or settings constant is added.
- **Step 2** — consumes `generators/base.BaseGenerator.stamp_di()` (5-column DI stamp; 3 meaningful cols — `di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind`). Does **not** consume `stamp_valid()` — all 9 tables are Core_DB (PRD §7.3). Consumes `utils/id_factory.IdFactory.next('event')` for every `Event_Id` minted. Consumes `utils/date_utils.format_ts` (used transitively via `stamp_di`). Does **not** consume `utils/luhn` (no card numbers in this step).
- **Step 3** — consumes `registry/context.GenerationContext`, `registry/profiles.CustomerProfile`, `registry/profiles.AgreementProfile`. `Tier10Events.generate(ctx)` reads `ctx.customers` (per-customer event loop), `ctx.agreements` (per-agreement monthly fee/interest loop + the transfer-source pool), `ctx.ids` (Event_Id minting), `ctx.rng` (every Bernoulli / integer / choice draw), and `ctx.tables` (guard on `Core_DB.PARTY`, `Core_DB.AGREEMENT`, `Core_DB.CHANNEL_INSTANCE`).
- **Step 4** — consumes the built universe. Critical invariants this step depends on:
  - `CustomerProfile.party_id` ∈ `Core_DB.PARTY.Party_Id`. Organizations also receive discretionary events (commercial accounts generate activity the same way retail does).
  - `CustomerProfile.lifecycle_cohort` is exactly one of `{'ACTIVE', 'DECLINING', 'CHURNED', 'NEW'}` — the event-volume envelope branches on this field.
  - `AgreementProfile.owner_party_id` resolves to a `CustomerProfile.party_id`; used as the Event_Party.Party_Id for account-level events.
  - `AgreementProfile.open_dttm` is a `datetime` — events before this date are not generated for that agreement.
  - `AgreementProfile.close_dttm` is a `datetime` (CHURNED) or `None` (all other cohorts) — events after this date are not generated for that agreement, and the owning customer's discretionary events also stop (only CHURNED customers close all accounts; see Part G1 attrition definition).
  - `AgreementProfile.is_deposit`, `is_loan_term`, `is_mortgage`, `is_credit_card`, `is_loan_transaction` — the interest-direction decision reads these flags: deposit-path agreements → `IN`, credit/loan-path agreements → `OUT`.
  - `AgreementProfile.monthly_balances` (list of 6 Decimal) populated for the DECLINING cohort — this step **does not** read the monthly balance values (amounts are drawn independently); the fact that a DECLINING agreement *exists* is what drives envelope decay.
  - `AgreementProfile.balance_amt` (Decimal) — available for rough fee/interest scaling, but this step uses a fixed small-amount envelope rather than re-deriving from the balance (Tier 7a already captured balance; Tier 10 models *transactions*, not point-in-time balance).
- **Step 5** — n/a at generation time. Writer is not invoked; DDL column ordering enforced via `pd.DataFrame(rows, columns=_COLS_*)` at DataFrame construction.
- **Step 10** — consumes `ctx.tables['Core_DB.AGREEMENT']` and `ctx.tables['Core_DB.PARTY']` (both for FK universe guard). Also consumes `ctx.tables['Core_DB.CHANNEL_INSTANCE']` — the 20-row channel pool produced by Tier 2 Step F (rows 650–656 in `generators/tier2_core.py`). Tier 10 needs the list of `Channel_Instance_Id` values per `Channel_Type_Cd` so the random-channel-picker can route by event type (ACCESS → `ATM`/`ONLINE`, CONTACT → `CALL_CENTER`, etc.).
- **Step 11** — consumes the fact that Core_DB.PARTY contains the reserved `BANK_PARTY_ID = 9_999_999` row (Step 19 fixed this). This step does NOT emit EVENT_PARTY rows referencing BANK_PARTY_ID — every EVENT_PARTY row references a generated customer `party_id`. The reserved row is not needed as a participant in events.
- **Step 17** — consumes the fact that every `AgreementProfile` has exactly one terminal sub-type flag True; the terminal-flag fan-out in §Rules for implementation below is total (every agreement is classified). Note from Step 17 handoff: CARD has no Agreement_Id column in the DDL — the CARD↔Agreement link needs to be wired here via ACCESS_DEVICE_EVENT. Step 17 minted Access_Device_Id values via ids.next('card').
- **Step 19** — consumes only an order-dependency (Tier 9 must finish before Tier 10 in orchestration). Tier 10 does NOT read `Core_DB.PARTY_AGREEMENT` / `PARTY_RELATED` / `PARTY_CLAIM` — event-to-agreement linkage comes from `AgreementProfile.owner_party_id` and `AgreementProfile.agreement_id`, not from the PARTY_AGREEMENT bridge.

No code from Steps 6–8 (Tier 0 seeds), Step 9 (Tier 1 geography), Steps 12–14 (Tier 4), Step 15 (Tier 5/6), Step 16 (Tier 7a), Step 18 (Tier 8) is imported by this step. Step 21 (Tier 13 tasks) and Step 22 (Tier 14 CDM) consume the `COMPLAINT_EVENT` / `EVENT` output produced here — those are downstream, out of scope for Step 20.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 20):
- `PRD.md` §4.2 (enumerated table list — the 9 Tier 10 tables), §7.1 (BIGINT rule — `Event_Id`, `Agreement_Id`, `Party_Id`, `Access_Device_Id` are all Int64), §7.3 (DI column rules — 3-col Core_DB tail, no `Valid_*`/`Del_Ind`), §7.6 (reproducibility — `ctx.rng` only), §4.3 (CHAR(1) = `Y`/`N`; `Event_Multimedia_Object_Ind` is CHAR(1))
- `mvp-tool-design.md` §9 Tier 10 (**authoritative scope + exemplar row dicts for all 9 tables**), §7.5 (exclusive sub-typing — extended here to the EVENT sub-type quartet), §12 (no Layer 2 constraint #1–#22 binds Tier 10 directly; Tier 10 enables Step 3 mapping items beyond the numbered list — fee/interest amounts for FINANCIAL_EVENT_AMOUNT), §14 Decision 3 (BIGINT everywhere), §14 Decision 7 (PARTY_INTERRACTION_EVENT typo — n/a here; that table lives in CDM_DB / Tier 14)
- `implementation-steps.md` Step 20 entry (exit criteria); Handoff Protocol (post-session rules)

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/06_supporting-enrichments.md` Part G2 (§lines 454–462) — cohort rules:
  - ACTIVE 55% → stable event rate across all 6 months
  - DECLINING 30% → declining event rate (envelope: `[1.0, 0.8, 0.6, 0.4, 0.3, 0.2]` multiplier per successive month)
  - CHURNED 5% → normal rate until `Agreement_Close_Dttm`, zero thereafter
  - NEW 10% → zero events before `Agreement_Open_Dttm`, normal rate afterward (open dates are in last 2 months so NEW customers have at most ~2 months of activity)
- `references/06_supporting-enrichments.md` Part H2 (§lines 489–494) — channel cost plausibility:
  - Average telephony contact rate per checking customer: ~1 per month → target ≈1 `DIRECT_CONTACT_EVENT` per customer-month with `Contact_Event_Subtype_Cd = 'CALL'` on a `CALL_CENTER` channel.
  - Digital channels: unspecified dollar cost; higher raw count OK (we model ~1–2 `ACCESS_DEVICE_EVENT` per customer-month on `ONLINE`/`MOBILE`).
- `references/06_supporting-enrichments.md` Part H3 (§lines 496–505) — fee rules:
  - **Recurring (monthly statement fee)**: exactly one `FINANCIAL_EVENT` per agreement per month with `Financial_Event_Type_Cd = 'STATEMENT_FEE'` and `In_Out_Direction_Type_Cd = 'OUT'`. Skipped only for months outside the agreement's `[open_dttm, close_dttm]` window.
  - **Intermittent (overdraft fee)**: drawn at a small Bernoulli rate per deposit-account-month (~5%) with `Financial_Event_Type_Cd = 'OVERDRAFT_FEE'` and `In_Out_Direction_Type_Cd = 'OUT'`. Only on DEPOSIT-path agreements (CHECKING / SAVINGS / MMA / COMMERCIAL_CHECKING).
  - Fee waiver / assessed-vs-collected separation in `FINANCIAL_EVENT_AMOUNT` — **MVP deferral**: one amount row per financial event with `Financial_Event_Amount_Cd = 'principal'`; no `'assessed'` / `'collected'` split. Layer 2 still works with the single-row pattern (FINANCIAL_EVENT_AMOUNT.Event_Transaction_Amt is unambiguous).
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the 9 in-scope tables (line numbers current as of 2026-04-20; the SQL DDL wins when it disagrees with any summary table, per CLAUDE.md "DDL verification rule" and PRD §10):
  - `EVENT` (§455 summary, §3671 raw DDL) — 9 business + 3 DI = 12 cols. NOT NULL: `Event_Id`, `Event_Activity_Type_Cd`. Nullable: `Event_Desc`, `Event_Start_Dttm`, `Event_End_Dttm`, `Event_GMT_Start_Dttm`, `Event_Reason_Cd`, `Event_Subtype_Cd`, `Initiation_Type_Cd`. `Event_Id` is INTEGER in DDL → **BIGINT** per PRD §7.1. PI on `Event_Id` (NUPI).
  - `EVENT_PARTY` (§441 summary, §3643 raw DDL) — 6 business + 3 DI = 9 cols. NOT NULL: `Event_Id`, `Party_Id`, `Event_Party_Role_Cd`, `Event_Party_Start_Dttm`. Nullable: `Event_Party_End_Dttm`, `Party_Identification_Type_Cd`. Both `*_Id` INTEGER → BIGINT. PI on `Event_Id` (NUPI — multiple parties per event is legal but MVP emits exactly one row per event).
  - `FINANCIAL_EVENT` (§472 summary, §3708 raw DDL) — 9 business + 3 DI = 12 cols. NOT NULL: `Event_Id`, `Financial_Event_Type_Cd`. Nullable: `Financial_Event_Period_Start_Dt`, `Financial_Event_Period_End_Dt`, `Document_Production_Cycle_Cd`, `Event_Medium_Type_Cd`, `Debit_Credit_Cd`, `In_Out_Direction_Type_Cd`, `Financial_Event_Bill_Cnt`. `Event_Id` INTEGER → BIGINT. **Note:** `In_Out_Direction_Type_Cd` is nullable per DDL but Layer 2 requires both `'IN'` and `'OUT'` present — this step populates it on every row. PI on `Event_Id` (NUPI).
  - `EVENT_CHANNEL_INSTANCE` (§538 summary, §3851 raw DDL) — 4 business + 3 DI = 7 cols. NOT NULL: `Event_Id` (BIGINT in DDL — already correct), `Channel_Instance_Id` (INTEGER). Nullable: `Event_Channel_Start_Dttm`, `Event_Channel_End_Dttm`. PI on `Event_Id` (NUPI).
  - `FINANCIAL_EVENT_AMOUNT` (§550 summary, §3877 raw DDL) — 5 business + 3 DI = 8 cols. **Composite PK**: `Event_Id` + `Financial_Event_Amount_Cd`. NOT NULL: `Event_Id` (BIGINT), `Financial_Event_Amount_Cd`, `Financial_Event_Type_Cd`, `In_Out_Direction_Type_Cd`. Nullable: `Event_Transaction_Amt` (DECIMAL(18,4)). PI on `Event_Id` (NUPI — composite-PK rows collide on Event_Id; this is Teradata-legal because the primary-index column is not the full PK).
  - `FUNDS_TRANSFER_EVENT` (§563 summary, §3905 raw DDL) — 6 business + 3 DI = 9 cols. NOT NULL: `Event_Id` (BIGINT), `Funds_Transfer_Method_Type_Cd`, `Originating_Agreement_Id` (BIGINT). Nullable: `Originating_Account_Num`, `Destination_Agreement_Id` (BIGINT), `Destination_Account_Num`. PI on `Event_Id` (NUPI).
  - `ACCESS_DEVICE_EVENT` (§577 summary, §3935 raw DDL) — 4 business + 3 DI = 7 cols. NOT NULL: `Event_Id` (BIGINT), `Channel_Type_Cd`. Nullable: `Funds_Transfer_Method_Type_Cd`, `Access_Device_Id` (BIGINT). PI on `Event_Id` (NUPI).
  - `DIRECT_CONTACT_EVENT` (§589 summary, §3961 raw DDL) — 3 business + 3 DI = 6 cols. NOT NULL: `Event_Id` (BIGINT), `Contact_Event_Subtype_Cd`. Nullable: `Customer_Tone_Cd`. PI on `Event_Id` (NUPI).
  - `COMPLAINT_EVENT` (§615 summary, §4021 raw DDL; **customized extension table, MULTISET**) — 6 business + 3 DI (or 5 DI — DDL shows 5 DI cols including `di_data_src_cd` and `di_proc_name` both NULL) = 9 (or 11 with data_src/proc_name) cols. NOT NULL: `Event_Id` (BIGINT), `Event_Sentiment_Cd` (SMALLINT), `Event_Channel_Type_Cd` (SMALLINT), `Event_Received_Dttm` (TIMESTAMP(0)), `Event_Multimedia_Object_Ind` (CHAR(1)). Nullable: `Event_Txt` (VARCHAR(32000)). `stamp_di()` on COMPLAINT_EVENT adds its standard 5-col DI tail; the two extra nullable DI cols (`di_data_src_cd`, `di_proc_name`) are populated by `stamp_di()` as `None` in the 5-col tail already, so there is no behavioural difference.

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is MVP-authoritative per PRD §10; only open `01` if `07` is ambiguous for a specific column (it isn't — all 9 tables have complete summary rows in `07`).
- `references/05_architect-qa.md` — no Q in this file binds Tier 10. Skip.
- `references/02_data-mapping-reference.md` — no constraint in Step 3's 22-point list binds Tier 10 directly; the FINANCIAL_EVENT_AMOUNT IN/OUT coverage is captured in the DDL and design doc. Opening Step 3 for completeness risks dragging unrelated items (Tier 7 frozen-ind etc.) into the session.
- `references/06_supporting-enrichments.md` beyond Parts G2, H2, H3 — the "Reads from" line names only those three. Other parts (Part A demographics, Part C balances, Part I mortgage vintages) are for upstream tiers.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `resources/iDM_MDM_tables_DDLs.xlsx` — already distilled into `07` and `02`.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier10_events.py` — `class Tier10Events(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]` method. Implementation contract:
  1. **Imports & TYPE_CHECKING block.** Import `BaseGenerator`; import `GenerationContext` / `CustomerProfile` / `AgreementProfile` under `TYPE_CHECKING` only. Standard library: `datetime`, `timedelta`, `time`, `date`. Typing: `Dict`, `List`, `Tuple`, `Optional`. From `config.settings`: `HIGH_TS`, `HISTORY_START`, `SIM_DATE`. Third-party: `pandas as pd`, `decimal.Decimal`.
  2. **Module-level constants** (every literal reused ≥2× must be a named constant; all code values chosen to be self-consistent — no Layer 2 literal-match binding; session MAY promote any of these to `config/code_values.py` if reuse is imminent but for a single-tier step local constants keep diff surface small):
     - `_TIER10_DI_START_TS = '2000-01-01 00:00:00.000000'` — matches Tier 6/7a/7b/8/9 convention.
     - `_EVENT_SCHEMA_KEY = 'Core_DB.EVENT'` (and analogous `_{TABLE}_KEY` constants for the other 8 tables) — used so the return-dict keys are not duplicated as string literals.
     - **Event activity type codes** (drive sub-type routing):
       ```
       _ACTIVITY_TRANSACTION = 'TRANSACTION'
       _ACTIVITY_ACCESS      = 'ACCESS'
       _ACTIVITY_CONTACT     = 'CONTACT'
       _ACTIVITY_COMPLAINT   = 'COMPLAINT'
       _ACTIVITY_FEE         = 'FEE'
       _ACTIVITY_INTEREST    = 'INTEREST'
       ```
       Sub-type routing contract:
       | Activity | Sub-type table hit | Additionally |
       |----------|-------------------|--------------|
       | TRANSACTION | FINANCIAL_EVENT | FINANCIAL_EVENT_AMOUNT + FUNDS_TRANSFER_EVENT |
       | FEE | FINANCIAL_EVENT | FINANCIAL_EVENT_AMOUNT (no FUNDS_TRANSFER_EVENT) |
       | INTEREST | FINANCIAL_EVENT | FINANCIAL_EVENT_AMOUNT (no FUNDS_TRANSFER_EVENT) |
       | ACCESS | ACCESS_DEVICE_EVENT | (no FINANCIAL_EVENT / FUNDS_TRANSFER / AMOUNT) |
       | CONTACT | DIRECT_CONTACT_EVENT | (no FINANCIAL_EVENT) |
       | COMPLAINT | COMPLAINT_EVENT | (no FINANCIAL_EVENT / DIRECT_CONTACT — complaint is its own path) |
     - **Financial event type codes** (drive Layer 2 Interest_Earned / Interest_Paid):
       ```
       _FE_STATEMENT_FEE   = 'STATEMENT_FEE'
       _FE_OVERDRAFT_FEE   = 'OVERDRAFT_FEE'
       _FE_INTEREST_EARNED = 'INTEREST_EARNED'
       _FE_INTEREST_PAID   = 'INTEREST_PAID'
       _FE_TRANSFER        = 'TRANSFER'
       ```
     - **Direction codes** (Layer 2 joins on this):
       ```
       _DIR_IN  = 'IN'
       _DIR_OUT = 'OUT'
       ```
     - **Event party role code**:
       ```
       _EVENT_PARTY_ROLE_INITIATOR = 'initiator'
       ```
     - **Funds transfer method codes**:
       ```
       _FTM_ACH       = 'ACH'
       _FTM_WIRE      = 'WIRE'
       _FTM_INTRABANK = 'INTRABANK'
       _FTM_METHODS   = (_FTM_ACH, _FTM_WIRE, _FTM_INTRABANK)
       ```
     - **Access device channel type codes** (drawn from CHANNEL_INSTANCE.Channel_Type_Cd; must be a subset of the 5 literal types Tier 2 populates):
       ```
       _ACCESS_CHANNEL_TYPES  = ('ATM', 'ONLINE', 'MOBILE')
       _CONTACT_CHANNEL_TYPES = ('CALL_CENTER', 'ONLINE')
       _COMPLAINT_CHANNEL_TYPES = ('CALL_CENTER', 'ONLINE', 'MOBILE')
       _TRANSACTION_CHANNEL_TYPES = ('ONLINE', 'MOBILE', 'BRANCH', 'ATM')
       _FEE_CHANNEL_TYPES = ('ONLINE',)  # statement fee channel is a placeholder; pick ONLINE
       _INTEREST_CHANNEL_TYPES = ('ONLINE',)  # interest accrual channel placeholder
       ```
       Tier 2 generates 5 `Channel_Type_Cd` values (`BRANCH`, `ATM`, `ONLINE`, `MOBILE`, `CALL_CENTER`) with 4 instances each — the picker selects uniformly from the instance pool matching the allowed type(s) for each event activity.
     - **Contact sub-type codes**:
       ```
       _CONTACT_SUBTYPE_CALL  = 'CALL'
       _CONTACT_SUBTYPE_EMAIL = 'EMAIL'
       _CONTACT_SUBTYPE_CHAT  = 'CHAT'
       _CONTACT_SUBTYPES = (_CONTACT_SUBTYPE_CALL, _CONTACT_SUBTYPE_EMAIL, _CONTACT_SUBTYPE_CHAT)
       ```
     - **Customer tone codes** (nullable on DIRECT_CONTACT_EVENT):
       ```
       _TONE_POSITIVE = 'POSITIVE'
       _TONE_NEUTRAL  = 'NEUTRAL'
       _TONE_NEGATIVE = 'NEGATIVE'
       _TONES = (_TONE_POSITIVE, _TONE_NEUTRAL, _TONE_NEGATIVE)
       ```
     - **Complaint SMALLINT codes** (per design doc):
       ```
       # Event_Sentiment_Cd SMALLINT: 1=positive, 2=neutral, 3=negative
       _COMPLAINT_SENTIMENT_POSITIVE = 1
       _COMPLAINT_SENTIMENT_NEUTRAL  = 2
       _COMPLAINT_SENTIMENT_NEGATIVE = 3
       _COMPLAINT_SENTIMENTS = (_COMPLAINT_SENTIMENT_POSITIVE,
                                 _COMPLAINT_SENTIMENT_NEUTRAL,
                                 _COMPLAINT_SENTIMENT_NEGATIVE)
       # Event_Channel_Type_Cd SMALLINT: 1=branch, 2=atm, 3=online, 4=mobile, 5=call_center
       _COMPLAINT_CHANNEL_SMALLINTS = (1, 2, 3, 4, 5)
       # Event_Multimedia_Object_Ind CHAR(1): 'Y'/'N'
       _MULTIMEDIA_IND_Y = 'Y'
       _MULTIMEDIA_IND_N = 'N'
       ```
     - **Financial event amount codes** (composite PK key):
       ```
       _AMOUNT_CD_PRINCIPAL = 'principal'
       ```
       MVP deferral noted in §Rules: no `'assessed'` / `'collected'` split.
     - **Rate / count envelope constants** (all tunables routed to module-level so the session can adjust one place if row counts blow out):
       ```
       _MONTHLY_EVENTS_MIN        = 1     # per customer per active month
       _MONTHLY_EVENTS_MAX        = 5     # per customer per active month (inclusive)
       _DECLINING_ENVELOPE        = (1.0, 0.8, 0.6, 0.4, 0.3, 0.2)  # multiplier per month; len == 6
       _COMPLAINT_CUSTOMER_RATE   = 0.05  # Bernoulli over customer base
       _OVERDRAFT_MONTH_RATE      = 0.05  # Bernoulli per deposit-account-month
       _TRANSACTION_SPLIT         = 0.30  # share of discretionary events that are TRANSACTION
       _ACCESS_SPLIT              = 0.50  # share that are ACCESS
       _CONTACT_SPLIT             = 0.20  # share that are CONTACT; sum of three = 1.0
       # COMPLAINT events are *not* drawn from the discretionary budget; they are
       # added on top of the discretionary stream for the ~5% complaint cohort.
       ```
     - **Amount sampling envelopes** (small, reproducible — uses `ctx.rng.uniform` or `ctx.rng.integers`, never external distributions):
       ```
       _STATEMENT_FEE_AMT_RANGE   = (Decimal('5.00'),  Decimal('25.00'))   # monthly stmt fee
       _OVERDRAFT_FEE_AMT_RANGE   = (Decimal('25.00'), Decimal('40.00'))   # overdraft fee
       _INTEREST_DEPOSIT_AMT_RANGE = (Decimal('0.50'),  Decimal('50.00'))  # monthly interest IN
       _INTEREST_LOAN_AMT_RANGE    = (Decimal('25.00'), Decimal('1500.00')) # monthly interest OUT
       _TRANSFER_AMT_RANGE         = (Decimal('50.00'), Decimal('5000.00')) # discretionary transfer
       # Each amount quantised to 4dp per DECIMAL(18,4).
       ```
  3. **DDL column-order lists** (module-level, one per table; business cols only — 3-col DI tail appended by `stamp_di()`). List exactly as shown in `references/07_mvp-schema-reference.md` for each table.
  4. **Guard at top of `generate()`**: verify `ctx.customers` and `ctx.agreements` are non-empty; verify required upstream tables are present:
     ```python
     _REQUIRED_UPSTREAM_TABLES = (
         'Core_DB.PARTY',
         'Core_DB.AGREEMENT',
         'Core_DB.CHANNEL_INSTANCE',
     )
     ```
     Raise `RuntimeError(f'Tier 10 prerequisite missing: {key}')` on any failure. Also verify `len(ctx.tables['Core_DB.CHANNEL_INSTANCE']) >= 20` (Tier 2 contract — 20 channel instances). Extract a per-`Channel_Type_Cd` index list once at the top of `generate` for O(1) channel-picker access.
  5. **Build order** (6 private builders, all invoked from `generate()`):
     1. `_build_discretionary_event_stream(ctx, channel_index)` — iterate `ctx.customers × months` to produce a list of per-event records (not yet DataFrame), each carrying `(event_id, activity_type, party_id, owner_agreement_id_or_None, start_dttm, channel_instance_id, financial_type, direction, amount)` tuples. For each customer, enumerate months in `HISTORY_START..SIM_DATE` (6 months); decide the month's event count using cohort envelope; for each event draw activity (TRANSACTION/ACCESS/CONTACT per `_*_SPLIT` weights); draw a timestamp uniformly within the month; pick a channel by type; if TRANSACTION, also pick a deposit-agreement origin for FUNDS_TRANSFER_EVENT and an amount.
     2. `_build_complaint_event_stream(ctx, channel_index)` — Bernoulli over `ctx.customers` at `_COMPLAINT_CUSTOMER_RATE`; for each selected customer draw exactly one complaint event at a random timestamp in the history window; produce analogous tuples.
     3. `_build_periodic_financial_event_stream(ctx, channel_index)` — for every agreement × eligible month (months intersected with `[open_dttm, close_dttm or SIM_DATE+1day]`), emit one STATEMENT_FEE event; for deposit-path agreements also emit one INTEREST_EARNED event; for credit/loan-path agreements emit one INTEREST_PAID event; for deposit-path agreements additionally draw a `_OVERDRAFT_MONTH_RATE` Bernoulli for an OVERDRAFT_FEE event.
     4. `_assemble_event_frames(tuples)` — fan the unified tuple list out into 9 DataFrames with the correct columns, dtypes, and (composite) key ordering.
     5. Every DataFrame stamped via `self.stamp_di(df, start_ts=_TIER10_DI_START_TS)`.
     6. Return dict with exactly the 9 `'Core_DB.X'` keys.
     (The split into 3 streams + 1 assembler is an implementation suggestion; the session may refactor to 1 unified loop provided every DoD invariant still holds. The suggestion exists because the three streams have different per-unit loops — per-customer-month, per-customer, per-agreement-month — and unifying them into one loop forces awkward conditional branches.)
  6. **Event_Id minting.** Every event receives a fresh `ctx.ids.next('event')` at construction time. Event IDs are BIGINT starting at `50_000_000`. Total event count on SEED=42 should be ≈80,000–120,000 (see §Tables generated).
  7. **Dtype coercions.** Every `*_Id` column → `Int64`. Every SMALLINT column (`Event_Sentiment_Cd`, `Event_Channel_Type_Cd`) → `Int64` (pandas has no Int16; `Int64` is the project convention for all integer cols). Decimal amounts → pandas `object` dtype holding `Decimal` values. Timestamp columns → `datetime` (pandas will normalise to `datetime64[ns]` when the column is non-null; leave it as object if nulls present — session picks the simpler path).
  8. **Return dict keys** (exactly these 9, in this order for the DoD check):
     ```
     'Core_DB.EVENT',
     'Core_DB.EVENT_PARTY',
     'Core_DB.EVENT_CHANNEL_INSTANCE',
     'Core_DB.FINANCIAL_EVENT',
     'Core_DB.FINANCIAL_EVENT_AMOUNT',
     'Core_DB.FUNDS_TRANSFER_EVENT',
     'Core_DB.ACCESS_DEVICE_EVENT',
     'Core_DB.DIRECT_CONTACT_EVENT',
     'Core_DB.COMPLAINT_EVENT',
     ```
     Do NOT mutate `ctx.tables` — the orchestrator does that after the call returns.

**Do NOT produce** in this step:
- CSVs — writer is not invoked. `output/` is not touched.
- `CDM_DB.PARTY_TO_EVENT_ROLE` / `CDM_DB.PARTY_INTERRACTION_EVENT` — Step 22's responsibility (Tier 14 CDM_DB). These are CDM-schema event bridges, not Core_DB.
- `Core_DB.EVENT_PARTY` rows for the bank / self-employment placeholder `9_999_999` — events are customer-initiated; the reserved ORGANIZATION/PARTY row plays no event role in MVP.
- Seed data for event-related lookup tables (there are none; `Financial_Event_Type_Cd`, `Event_Activity_Type_Cd`, `Contact_Event_Subtype_Cd`, `Funds_Transfer_Method_Type_Cd` are free-form VARCHAR per DDL with no `*_TYPE` lookup in scope). If a future Layer 2 rule requires a literal match on one of these codes, either extend `config/code_values.py` or seed a new Tier 0 lookup — escalate per Handoff Protocol §2.
- Wiring into `main.py` — orchestrator changes are Step 25's responsibility.
- Changes to `config/settings.py` / `config/code_values.py` / `config/distributions.py` — all needed constants exist; new amount envelopes stay local to `tier10_events.py` (they are tuning knobs, not cross-cutting code values).
- Changes to `registry/profiles.py` / `registry/universe.py` — Tier 10 reads the registry as-is; it does not add new profile fields. If a future step discovers a needed profile field (e.g. per-agreement monthly transaction count), escalate rather than mutate here.

## Tables generated (if applicable)

After `Tier10Events.generate(ctx)` runs, `ctx.tables` gains these 9 Core_DB keys. Expected row counts on the standard SEED=42 universe (3,000 customers, 5,000 agreements, 6-month window). Counts are indicative — they are a random variable; DoD uses range checks, not exact equality.

| Table | Row count | Driven by | Notes |
|-------|-----------|-----------|-------|
| `Core_DB.EVENT` | ≈ 80,000–120,000 | union of discretionary + complaint + periodic streams | BIGINT Event_Id; `Event_Activity_Type_Cd` is one of `{TRANSACTION, ACCESS, CONTACT, COMPLAINT, FEE, INTEREST}`; Event_Start_Dttm lies in `[HISTORY_START, SIM_DATE]` |
| `Core_DB.EVENT_PARTY` | exactly `len(EVENT)` | one row per event | `Event_Party_Role_Cd = 'initiator'`; `Party_Id` is the driving customer (owner_party_id for account-level events, cp.party_id for customer-level events); `Event_Party_Start_Dttm = event.Event_Start_Dttm` |
| `Core_DB.EVENT_CHANNEL_INSTANCE` | exactly `len(EVENT)` | one row per event | `Channel_Instance_Id` drawn from Tier 2's 20-row pool, filtered by event-activity-compatible `Channel_Type_Cd` |
| `Core_DB.FINANCIAL_EVENT` | ≈ 60,000–90,000 | union of TRANSACTION, FEE, INTEREST activity events | Both `'IN'` and `'OUT'` In_Out_Direction_Type_Cd values present (Layer 2 requirement per design doc §9 Tier 10) |
| `Core_DB.FINANCIAL_EVENT_AMOUNT` | exactly `len(FINANCIAL_EVENT)` | one `'principal'` row per FINANCIAL_EVENT | Composite PK (`Event_Id` + `Financial_Event_Amount_Cd`); MVP deferral: no `'assessed'`/`'collected'` split |
| `Core_DB.FUNDS_TRANSFER_EVENT` | ≈ 15,000–25,000 | one row per TRANSACTION-activity event | Originating_Agreement_Id is one of the customer's deposit-path agreements; Destination_Agreement_Id is usually None (external transfer) with ~20% probability of being another agreement of the same customer (internal transfer) |
| `Core_DB.ACCESS_DEVICE_EVENT` | ≈ 25,000–40,000 | one row per ACCESS-activity event | `Channel_Type_Cd` ∈ `{ATM, ONLINE, MOBILE}`; `Access_Device_Id` NULL in MVP (no device registry table in scope) |
| `Core_DB.DIRECT_CONTACT_EVENT` | ≈ 10,000–18,000 | one row per CONTACT-activity event | `Contact_Event_Subtype_Cd` ∈ `{CALL, EMAIL, CHAT}`; `Customer_Tone_Cd` sampled from `{POSITIVE, NEUTRAL, NEGATIVE}` with NEUTRAL most likely |
| `Core_DB.COMPLAINT_EVENT` | ≈ 150 (≈5% of ~3,000 customers) | one row per complaint-cohort customer | SMALLINT `Event_Sentiment_Cd` / `Event_Channel_Type_Cd`; CHAR(1) `Event_Multimedia_Object_Ind`; `Event_Received_Dttm` populated per DDL NOT NULL; **Step 21's `PARTY_TASK.Source_Event_Id` will join on this Event_Id** |

All 9 DataFrames carry the standard Core_DB 5-column DI tail (3 meaningful + 2 null placeholders) after `stamp_di()`. None of the 9 carry `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` (PRD §7.3).

**Sub-type exclusivity** (design-doc §7.5 extended to events): every `EVENT` row appears in **exactly one** of `{FINANCIAL_EVENT, ACCESS_DEVICE_EVENT, DIRECT_CONTACT_EVENT, COMPLAINT_EVENT}` — never zero, never two. `FUNDS_TRANSFER_EVENT` is nested under `FINANCIAL_EVENT` (only TRANSACTION-activity events populate it; FEE and INTEREST events do not).

**Layer 2 readiness guaranteed by this step:**
- Both `'IN'` and `'OUT'` values appear in `FINANCIAL_EVENT.In_Out_Direction_Type_Cd` and `FINANCIAL_EVENT_AMOUNT.In_Out_Direction_Type_Cd` — Layer 2 Interest_Earned / Interest_Paid derivations will resolve.
- Every agreement has at least one `STATEMENT_FEE` FINANCIAL_EVENT per active month — Layer 2 fee-aggregation queries will not return empty sets.
- `COMPLAINT_EVENT.Event_Id` is the FK target for Step 21 Tier 13 `PARTY_TASK.Source_Event_Id` — the complaint-to-task traceability chain starts here.

## Files to modify

No files modified. Tier 10 is an additive step: one new generator file, no edits to existing modules. (The orchestrator wiring in `main.py` is deferred to Step 25 per `implementation-steps.md` Handoff Protocol §5.)

## New dependencies

No new dependencies. Uses only `pandas`, `numpy` (via `ctx.rng`), and the Python standard library (`datetime`, `decimal`, `typing`).

## Rules for implementation

**Universal rules** (apply to every step):

- BIGINT for all ID columns (per PRD §7.1) — `Event_Id`, `Party_Id`, `Agreement_Id`, `Originating_Agreement_Id`, `Destination_Agreement_Id`, `Access_Device_Id`, `Channel_Instance_Id` are all `Int64` dtype, never INTEGER, even when the DDL says INTEGER. (Channel_Instance_Id is INTEGER in DDL and remains so via the existing Tier 2 contract — Tier 10 treats it as Int64 uniformly; the writer / DDL loader can coerce as needed.)
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2). `EVENT_PARTY.Party_Id` draws from `CustomerProfile.party_id`, which is the same value later used in `CDM_DB.PARTY.CDM_Party_Id` (Step 22).
- DI column stamping on every table via `BaseGenerator.stamp_di()` with `start_ts = _TIER10_DI_START_TS = '2000-01-01 00:00:00.000000'`.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `di_rec_deleted_Ind = 'N'` for active records (every row emitted by this step).
- **Do NOT** stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` — Tier 10 is Core_DB only (PRD §7.3).
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` — enforce via `pd.DataFrame(rows, columns=_COLS_*)` construction.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — n/a this step (that table lives in CDM_DB / Tier 14).
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — n/a this step.
- No ORMs, no database connections — pure pandas → CSV.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42`. Every Bernoulli / choice / uniform draw MUST route through `ctx.rng` — never `random.random()`, never `numpy.random` module-level calls. This includes: event-count-per-month, activity-type split, timestamp-within-month, channel-instance choice, tone choice, sentiment choice, funds-transfer-method choice, destination-agreement choice, and amount sampling. There are ~200k–400k such draws — lazy use of the wrong RNG will silently break reproducibility.

**Step-specific rules:**

- **Single public entry point.** `class Tier10Events(BaseGenerator)` exposes exactly one public method: `generate(ctx) -> Dict[str, pd.DataFrame]`. Helpers are private (`_build_*`) or module-level functions.
- **No `ctx.tables` mutation.** `generate()` returns the dict; the orchestrator merges it. Mirrors Tier 6, Tier 7a, Tier 7b, Tier 8, Tier 9.
- **No `datetime.now()` for business columns.** Every timestamp is derived from `HISTORY_START` / `SIM_DATE` / an `AgreementProfile` or `CustomerProfile` field, offset by a `ctx.rng`-drawn delta. `BaseGenerator.stamp_di()` defaults to `datetime.now()` when `start_ts=None`; the session MUST pass `start_ts=_TIER10_DI_START_TS` explicitly to every `stamp_di` call for reproducibility (the Tier 6/7a/7b/8/9 convention).
- **Sub-type exclusivity (design-doc §7.5 extended to events).** Every `EVENT.Event_Id` appears in **exactly one** of `FINANCIAL_EVENT` / `ACCESS_DEVICE_EVENT` / `DIRECT_CONTACT_EVENT` / `COMPLAINT_EVENT`. The routing table in §Produces is authoritative. A TRANSACTION event that mistakenly lands in both `FINANCIAL_EVENT` and `DIRECT_CONTACT_EVENT` is a bug. DoD verifies this.
- **FUNDS_TRANSFER_EVENT coverage.** Exactly the TRANSACTION-activity subset of FINANCIAL_EVENT has a FUNDS_TRANSFER_EVENT row; FEE and INTEREST FINANCIAL_EVENTs do NOT. DoD verifies both directions: every TRANSACTION event has a FUNDS_TRANSFER_EVENT row; no FEE/INTEREST event does.
- **Originating_Agreement_Id must exist in `Core_DB.AGREEMENT`.** Same for `Destination_Agreement_Id` (when non-null). `Originating_Agreement_Id` is drawn from the *owning* customer's deposit-path agreement list; if a customer has zero deposit agreements they cannot initiate a transfer (filter those customers out of the TRANSACTION path — fall back to ACCESS activity instead). DoD verifies FK resolution.
- **`In_Out_Direction_Type_Cd` populated on every FINANCIAL_EVENT row** — even though the DDL marks it nullable, Layer 2 requires non-null. Every row emits `'IN'` or `'OUT'`, never NULL.
  - Deposit-path agreements (CHECKING, SAVINGS, MMA, RETIREMENT, CERTIFICATE_OF_DEPOSIT, COMMERCIAL_CHECKING): INTEREST_EARNED → `IN`; STATEMENT_FEE / OVERDRAFT_FEE → `OUT`.
  - Credit/loan-path agreements (CREDIT_CARD, MORTGAGE, VEHICLE_LOAN, STUDENT_LOAN, HELOC, PAYDAY): INTEREST_PAID → `OUT`; STATEMENT_FEE → `OUT`.
  - TRANSACTION (transfer): direction depends on whether the current agreement is source or destination — MVP treats TRANSFER as `OUT` from the originating deposit account (money leaving the account). Both directions appear because INTEREST_EARNED events produce `IN` rows.
- **Every customer-month has the right number of discretionary events for their cohort.** Implement envelope as:
  ```python
  def _month_events(cohort, month_idx, ag_open_date, ag_close_date, month_start, month_end):
      # Returns integer 0..MAX events for this customer-month.
      # month_idx in 0..5 (0 = first history month).
      # For CHURNED: zero after close_dttm month
      # For NEW: zero before open_dttm month
      # For DECLINING: round(base * _DECLINING_ENVELOPE[month_idx])
      # For ACTIVE: base unchanged
  ```
  Use `ctx.rng.integers(low=_MONTHLY_EVENTS_MIN, high=_MONTHLY_EVENTS_MAX + 1)` for the base (numpy semantics: `high` exclusive). DoD verifies total customer-month counts land inside the expected envelope band.
- **Discretionary event timestamps lie within their intended month.** Draw `offset_seconds = ctx.rng.integers(0, seconds_in_month)`, add to month-start. No events fall on day 31 of a 30-day month.
- **Account-level events scheduled at month-end.** STATEMENT_FEE at month-end `23:59:59` is a common banking convention; INTEREST at month-end `23:59:59`. Concrete value: use `month_end_date` at time `23:59:59` (no microseconds needed since DDL is `TIMESTAMP`, not `TIMESTAMP(6)`). Session may substitute a different convention (random time on last 3 days of month) if preferred — DoD only checks the timestamp falls within the agreement's active window.
- **Overdraft fee only on deposit-path agreements.** `_OVERDRAFT_MONTH_RATE` Bernoulli per deposit-account-month. Draw a second amount and a random mid-month timestamp. Credit/loan-path agreements do NOT get overdraft events (they have no "account balance" in the retail sense).
- **Complaint cohort is disjoint from the discretionary stream.** A customer drawing a COMPLAINT event still receives their normal discretionary ACCESS/CONTACT/TRANSACTION events that month — the complaint is additive. The complaint is also not routed through DIRECT_CONTACT_EVENT (COMPLAINT_EVENT is its own sub-type path).
- **COMPLAINT_EVENT SMALLINT codes fully populated.** `Event_Sentiment_Cd` drawn uniformly from `_COMPLAINT_SENTIMENTS` with higher weight on `3` (NEGATIVE — complaints are usually negative); `Event_Channel_Type_Cd` drawn uniformly from `_COMPLAINT_CHANNEL_SMALLINTS`; `Event_Received_Dttm` matches `EVENT.Event_Start_Dttm` for the same Event_Id; `Event_Multimedia_Object_Ind` drawn `'Y'` at 10% rate, else `'N'`; `Event_Txt` is a short Faker-like placeholder string (e.g. `'Complaint record for event {Event_Id}'`) — no Faker dependency needed, the string is cosmetic.
- **CHAR(1) flag format.** `Event_Multimedia_Object_Ind` is `'Y'` / `'N'` per PRD §4.3 (not `'1'` / `'0'`). DoD checks.
- **COMPLAINT_EVENT row count ≈ 5% of customers, strictly.** Use `ctx.rng.random() < _COMPLAINT_CUSTOMER_RATE` per customer. Range check: `0.03 * len(ctx.customers) <= len(COMPLAINT_EVENT) <= 0.07 * len(ctx.customers)`.
- **EVENT_PARTY row count == EVENT row count.** One initiator per event; no additional parties in MVP (no "beneficiary" / "co-signer" roles modelled). Every Event_Party.Event_Id is unique.
- **EVENT_CHANNEL_INSTANCE row count == EVENT row count.** Every event has exactly one channel attachment. DoD verifies the `Channel_Instance_Id` FK resolves into `Core_DB.CHANNEL_INSTANCE.Channel_Instance_Id`.
- **Decimal formatting.** Amounts quantised to 4dp (`DECIMAL(18,4)` per DDL) via `.quantize(Decimal('0.0001'))`. Rates (none in this step) are 12dp. Do not write float literals; use `Decimal` throughout.
- **No external Faker / scipy calls.** Tier 10 does not need realistic names / addresses / distribution shapes — uniform draws from `ctx.rng` suffice. Keeping imports minimal keeps reproducibility tight.
- **Every agreement must contribute at least one FINANCIAL_EVENT per eligible month.** Not just in aggregate — every `(agreement_id, year_month)` pair in the agreement's `[open_dttm, close_dttm or SIM_DATE]` window must have at least one STATEMENT_FEE row. This is Part H3's "recurring monthly statement fee" contract; an aggregate count check is insufficient because it allows double-billing one month and skipping another.
- **Required test hook — `Tier10Events.last_periodic_owner_map: Dict[int, int]`.** Because `FINANCIAL_EVENT` does not carry `Agreement_Id` as a DDL column (it joins to AGREEMENT only via FUNDS_TRANSFER_EVENT or the EVENT_PARTY → owner chain, both of which are ambiguous for multi-agreement customers), the generator MUST expose a post-`generate()` instance attribute `last_periodic_owner_map: Dict[int, int]` mapping every **periodic** financial event (STATEMENT_FEE, OVERDRAFT_FEE, INTEREST_EARNED, INTEREST_PAID) `Event_Id` → its owning `Agreement_Id`. Populated at the end of `_build_periodic_financial_event_stream` from the same tuple list that produced the DataFrames. This attribute is read by the DoD per-agreement-month coverage check; production code (orchestrator, writer, validator) does not consume it. Discretionary TRANSACTION events are not included in this map — their owner-agreement linkage is already captured by `FUNDS_TRANSFER_EVENT.Originating_Agreement_Id`.
- **Access_Device_Id NULL in MVP.** The DDL makes it nullable; there is no `ACCESS_DEVICE` table in scope; populating a fake Int64 would create dangling FKs. Null is correct.
- **`Party_Identification_Type_Cd` NULL in MVP.** DDL makes it nullable; no `PARTY_IDENTIFICATION_TYPE` lookup is in scope at event-party join granularity. Null is correct.
- **`Event_Medium_Type_Cd` / `Document_Production_Cycle_Cd` / `Debit_Credit_Cd` / `Financial_Event_Bill_Cnt` NULL on FINANCIAL_EVENT.** DDL makes them nullable; no Layer 2 rule binds them in MVP. Null is correct.

## Definition of done

The implementation session MUST tick every box or mark it n/a with a one-line justification before closing the session.

**File & import sanity:**

- [ ] `git status` shows only `generators/tier10_events.py` and `.claude/specs/step-20-tier10-events.md` as modified/added — nothing else.
- [ ] `python -c "from generators.tier10_events import Tier10Events; g = Tier10Events(); assert callable(g.generate)"` exits 0.
- [ ] `Tier10Events` subclasses `BaseGenerator`:
  ```python
  from generators.base import BaseGenerator
  from generators.tier10_events import Tier10Events
  assert issubclass(Tier10Events, BaseGenerator)
  ```
- [ ] No CSV column named `*_Id` uses INTEGER — n/a this step (no CSVs written; the writer is Step 5 / Step 25). BIGINT invariants are verified via DataFrame dtype checks below.
- [ ] `PARTY_INTERRACTION_EVENT` typo check — n/a (no such table written; CDM_DB Tier 14).
- [ ] `GEOSPATIAL.csv` absence check — n/a (no `output/` writes).

**End-to-end table emission harness** (session may use a full pipeline run or a minimal synthesised `ctx` with a ≥50-customer, ≥80-agreement, Tier 0 through Tier 9 pre-populated state; both are acceptable):

- [ ] `Tier10Events().generate(ctx)` returns a dict with exactly the 9 keys:
  ```python
  result = Tier10Events().generate(ctx)
  assert set(result) == {
      'Core_DB.EVENT', 'Core_DB.EVENT_PARTY', 'Core_DB.EVENT_CHANNEL_INSTANCE',
      'Core_DB.FINANCIAL_EVENT', 'Core_DB.FINANCIAL_EVENT_AMOUNT',
      'Core_DB.FUNDS_TRANSFER_EVENT', 'Core_DB.ACCESS_DEVICE_EVENT',
      'Core_DB.DIRECT_CONTACT_EVENT', 'Core_DB.COMPLAINT_EVENT',
  }
  ```
- [ ] Every DataFrame is non-empty (`len(df) > 0`) for all 9 keys (including COMPLAINT_EVENT — ≥1 row on a ≥50-customer harness).

**EVENT invariants:**

- [ ] Event_Id column is unique across all EVENT rows:
  ```python
  ev = result['Core_DB.EVENT']
  assert ev['Event_Id'].is_unique, f'Duplicate Event_Id: {ev["Event_Id"][ev["Event_Id"].duplicated()].tolist()[:5]}'
  ```
- [ ] Every Event_Id is BIGINT ≥ 50_000_000 (IdFactory `'event'` range start per `config/settings.py:47`):
  ```python
  assert (ev['Event_Id'].astype(int) >= 50_000_000).all()
  ```
- [ ] Event_Activity_Type_Cd ∈ `{TRANSACTION, ACCESS, CONTACT, COMPLAINT, FEE, INTEREST}`:
  ```python
  from generators.tier10_events import (
      _ACTIVITY_TRANSACTION, _ACTIVITY_ACCESS, _ACTIVITY_CONTACT,
      _ACTIVITY_COMPLAINT, _ACTIVITY_FEE, _ACTIVITY_INTEREST,
  )
  expected = {_ACTIVITY_TRANSACTION, _ACTIVITY_ACCESS, _ACTIVITY_CONTACT,
              _ACTIVITY_COMPLAINT, _ACTIVITY_FEE, _ACTIVITY_INTEREST}
  assert set(ev['Event_Activity_Type_Cd'].unique()) <= expected
  # All 6 should actually appear on a full universe; on small harness ≥3 is fine
  assert len(set(ev['Event_Activity_Type_Cd'].unique())) >= 3
  ```
- [ ] Every Event_Start_Dttm falls in `[HISTORY_START, SIM_DATE + 1 day]`:
  ```python
  from config.settings import HISTORY_START, SIM_DATE
  from datetime import datetime, timedelta
  lo = datetime.combine(HISTORY_START, datetime.min.time())
  hi = datetime.combine(SIM_DATE + timedelta(days=1), datetime.min.time())
  assert (ev['Event_Start_Dttm'] >= lo).all()
  assert (ev['Event_Start_Dttm'] < hi).all()
  ```

**Sub-type exclusivity (design-doc §7.5):**

- [ ] Every Event_Id appears in **exactly one** of FINANCIAL_EVENT / ACCESS_DEVICE_EVENT / DIRECT_CONTACT_EVENT / COMPLAINT_EVENT:
  ```python
  fe_ids   = set(result['Core_DB.FINANCIAL_EVENT']['Event_Id'].astype(int))
  ad_ids   = set(result['Core_DB.ACCESS_DEVICE_EVENT']['Event_Id'].astype(int))
  dc_ids   = set(result['Core_DB.DIRECT_CONTACT_EVENT']['Event_Id'].astype(int))
  cp_ids   = set(result['Core_DB.COMPLAINT_EVENT']['Event_Id'].astype(int))
  all_event_ids = set(ev['Event_Id'].astype(int))
  union = fe_ids | ad_ids | dc_ids | cp_ids
  assert union == all_event_ids, f'Missing sub-type rows for: {all_event_ids - union}'
  # Pairwise disjoint
  assert not (fe_ids & ad_ids) and not (fe_ids & dc_ids) and not (fe_ids & cp_ids)
  assert not (ad_ids & dc_ids) and not (ad_ids & cp_ids) and not (dc_ids & cp_ids)
  ```

**EVENT_PARTY invariants:**

- [ ] Row count equals len(EVENT):
  ```python
  ep = result['Core_DB.EVENT_PARTY']
  assert len(ep) == len(ev), f'{len(ep)} != {len(ev)}'
  ```
- [ ] Every Event_Id in EVENT_PARTY appears in EVENT and is unique:
  ```python
  assert set(ep['Event_Id'].astype(int)) == all_event_ids
  assert ep['Event_Id'].is_unique
  ```
- [ ] Every Party_Id resolves to Core_DB.PARTY.Party_Id:
  ```python
  party_ids = set(ctx.tables['Core_DB.PARTY']['Party_Id'].astype(int))
  assert set(ep['Party_Id'].astype(int)).issubset(party_ids)
  ```
- [ ] Every row has Event_Party_Role_Cd == 'initiator':
  ```python
  assert (ep['Event_Party_Role_Cd'] == 'initiator').all()
  ```
- [ ] Event_Party_Start_Dttm matches EVENT.Event_Start_Dttm on the same Event_Id:
  ```python
  ev_ts  = dict(zip(ev['Event_Id'].astype(int),  ev['Event_Start_Dttm']))
  ep_ts  = dict(zip(ep['Event_Id'].astype(int),  ep['Event_Party_Start_Dttm']))
  for eid in ev_ts:
      assert ev_ts[eid] == ep_ts[eid]
  ```

**EVENT_CHANNEL_INSTANCE invariants:**

- [ ] Row count equals len(EVENT):
  ```python
  eci = result['Core_DB.EVENT_CHANNEL_INSTANCE']
  assert len(eci) == len(ev)
  assert set(eci['Event_Id'].astype(int)) == all_event_ids
  ```
- [ ] Every Channel_Instance_Id resolves to `Core_DB.CHANNEL_INSTANCE.Channel_Instance_Id`:
  ```python
  chan_ids = set(ctx.tables['Core_DB.CHANNEL_INSTANCE']['Channel_Instance_Id'].astype(int))
  assert set(eci['Channel_Instance_Id'].astype(int)).issubset(chan_ids)
  ```
- [ ] Channel routing sanity — ACCESS events use `{ATM, ONLINE, MOBILE}` channels; CONTACT events use `{CALL_CENTER, ONLINE}`:
  ```python
  ci_df = ctx.tables['Core_DB.CHANNEL_INSTANCE']
  ci_type_map = dict(zip(ci_df['Channel_Instance_Id'].astype(int),
                          ci_df['Channel_Type_Cd']))
  ev_activity = dict(zip(ev['Event_Id'].astype(int), ev['Event_Activity_Type_Cd']))
  eci_chan = dict(zip(eci['Event_Id'].astype(int),
                       eci['Channel_Instance_Id'].astype(int)))
  for eid, act in ev_activity.items():
      ct = ci_type_map[eci_chan[eid]]
      if act == 'ACCESS':  assert ct in {'ATM', 'ONLINE', 'MOBILE'}, (eid, act, ct)
      if act == 'CONTACT': assert ct in {'CALL_CENTER', 'ONLINE'}, (eid, act, ct)
  ```

**FINANCIAL_EVENT invariants:**

- [ ] Event_Ids are exactly the TRANSACTION + FEE + INTEREST subset:
  ```python
  fe = result['Core_DB.FINANCIAL_EVENT']
  fe_activities = {ev_activity[int(eid)] for eid in fe['Event_Id']}
  assert fe_activities <= {'TRANSACTION', 'FEE', 'INTEREST'}
  non_fe_activities = {ev_activity[int(eid)] for eid in all_event_ids - set(fe['Event_Id'].astype(int))}
  assert non_fe_activities <= {'ACCESS', 'CONTACT', 'COMPLAINT'}
  ```
- [ ] Both `'IN'` and `'OUT'` In_Out_Direction_Type_Cd values appear (Layer 2 requirement):
  ```python
  assert set(fe['In_Out_Direction_Type_Cd'].unique()) == {'IN', 'OUT'}, \
         f"Missing direction: {set(fe['In_Out_Direction_Type_Cd'].unique())}"
  ```
- [ ] Financial_Event_Type_Cd is NOT NULL on every row:
  ```python
  assert fe['Financial_Event_Type_Cd'].notna().all()
  assert set(fe['Financial_Event_Type_Cd'].unique()) <= {
      'STATEMENT_FEE', 'OVERDRAFT_FEE', 'INTEREST_EARNED', 'INTEREST_PAID', 'TRANSFER'
  }
  ```
- [ ] STATEMENT_FEE events are always `OUT`; INTEREST_EARNED always `IN`; INTEREST_PAID always `OUT`:
  ```python
  for ftype, expected_dir in [
      ('STATEMENT_FEE', 'OUT'), ('INTEREST_EARNED', 'IN'),
      ('INTEREST_PAID', 'OUT'), ('OVERDRAFT_FEE', 'OUT'),
  ]:
      sub = fe[fe['Financial_Event_Type_Cd'] == ftype]
      if len(sub) > 0:
          assert (sub['In_Out_Direction_Type_Cd'] == expected_dir).all(), ftype
  ```

**FINANCIAL_EVENT_AMOUNT invariants:**

- [ ] Row count equals `len(FINANCIAL_EVENT)` (exactly one `'principal'` per financial event):
  ```python
  fea = result['Core_DB.FINANCIAL_EVENT_AMOUNT']
  assert len(fea) == len(fe), f'{len(fea)} != {len(fe)}'
  ```
- [ ] Composite PK is unique on (Event_Id, Financial_Event_Amount_Cd):
  ```python
  assert not fea.duplicated(subset=['Event_Id', 'Financial_Event_Amount_Cd']).any()
  ```
- [ ] Every row has Financial_Event_Amount_Cd == 'principal' (MVP single-amount deferral):
  ```python
  assert (fea['Financial_Event_Amount_Cd'] == 'principal').all()
  ```
- [ ] Financial_Event_Type_Cd and In_Out_Direction_Type_Cd on FINANCIAL_EVENT_AMOUNT match the parent FINANCIAL_EVENT row on the same Event_Id:
  ```python
  fe_map = dict(zip(fe['Event_Id'].astype(int), zip(fe['Financial_Event_Type_Cd'], fe['In_Out_Direction_Type_Cd'])))
  for _, row in fea.iterrows():
      eid = int(row['Event_Id'])
      assert (row['Financial_Event_Type_Cd'], row['In_Out_Direction_Type_Cd']) == fe_map[eid]
  ```
- [ ] Event_Transaction_Amt is a Decimal ≥ 0 and quantises to 4dp (DECIMAL(18,4)):
  ```python
  from decimal import Decimal
  for amt in fea['Event_Transaction_Amt']:
      assert isinstance(amt, Decimal), type(amt)
      assert amt >= Decimal('0')
      assert amt == amt.quantize(Decimal('0.0001'))
  ```

**FUNDS_TRANSFER_EVENT invariants:**

- [ ] Event_Ids are exactly the TRANSACTION-activity subset of FINANCIAL_EVENT:
  ```python
  fte = result['Core_DB.FUNDS_TRANSFER_EVENT']
  transaction_ids = {int(eid) for eid in fe['Event_Id'] if ev_activity[int(eid)] == 'TRANSACTION'}
  assert set(fte['Event_Id'].astype(int)) == transaction_ids
  ```
- [ ] Every Originating_Agreement_Id resolves to Core_DB.AGREEMENT.Agreement_Id:
  ```python
  ag_ids = set(ctx.tables['Core_DB.AGREEMENT']['Agreement_Id'].astype(int))
  assert set(fte['Originating_Agreement_Id'].astype(int)).issubset(ag_ids)
  ```
- [ ] Every non-null Destination_Agreement_Id also resolves:
  ```python
  non_null_dest = fte['Destination_Agreement_Id'].dropna().astype(int)
  assert set(non_null_dest).issubset(ag_ids)
  ```
- [ ] Funds_Transfer_Method_Type_Cd ∈ `{ACH, WIRE, INTRABANK}`:
  ```python
  assert set(fte['Funds_Transfer_Method_Type_Cd'].unique()) <= {'ACH', 'WIRE', 'INTRABANK'}
  ```

**ACCESS_DEVICE_EVENT invariants:**

- [ ] Event_Ids are exactly the ACCESS-activity subset:
  ```python
  ade = result['Core_DB.ACCESS_DEVICE_EVENT']
  access_ids = {eid for eid, act in ev_activity.items() if act == 'ACCESS'}
  assert set(ade['Event_Id'].astype(int)) == access_ids
  ```
- [ ] Channel_Type_Cd ∈ `{ATM, ONLINE, MOBILE}`:
  ```python
  assert set(ade['Channel_Type_Cd'].unique()) <= {'ATM', 'ONLINE', 'MOBILE'}
  ```
- [ ] Access_Device_Id is NULL on every row (MVP deferral):
  ```python
  assert ade['Access_Device_Id'].isna().all()
  ```

**DIRECT_CONTACT_EVENT invariants:**

- [ ] Event_Ids are exactly the CONTACT-activity subset:
  ```python
  dce = result['Core_DB.DIRECT_CONTACT_EVENT']
  contact_ids = {eid for eid, act in ev_activity.items() if act == 'CONTACT'}
  assert set(dce['Event_Id'].astype(int)) == contact_ids
  ```
- [ ] Contact_Event_Subtype_Cd ∈ `{CALL, EMAIL, CHAT}`:
  ```python
  assert set(dce['Contact_Event_Subtype_Cd'].unique()) <= {'CALL', 'EMAIL', 'CHAT'}
  ```
- [ ] Customer_Tone_Cd values ⊆ `{POSITIVE, NEUTRAL, NEGATIVE}` (nullable allowed but all populated in MVP):
  ```python
  assert set(dce['Customer_Tone_Cd'].dropna().unique()) <= {'POSITIVE', 'NEUTRAL', 'NEGATIVE'}
  ```

**COMPLAINT_EVENT invariants:**

- [ ] Row count in 3–7% of customer base:
  ```python
  ce = result['Core_DB.COMPLAINT_EVENT']
  n_cust = len(ctx.customers)
  lo = max(1, int(0.03 * n_cust))
  hi = int(0.07 * n_cust) + 1
  assert lo <= len(ce) <= hi, f'COMPLAINT_EVENT {len(ce)} outside [{lo}, {hi}]'
  ```
- [ ] Event_Ids are exactly the COMPLAINT-activity subset:
  ```python
  complaint_ids = {eid for eid, act in ev_activity.items() if act == 'COMPLAINT'}
  assert set(ce['Event_Id'].astype(int)) == complaint_ids
  ```
- [ ] Event_Sentiment_Cd SMALLINT ∈ {1, 2, 3}:
  ```python
  assert set(ce['Event_Sentiment_Cd'].astype(int).unique()) <= {1, 2, 3}
  ```
- [ ] Event_Channel_Type_Cd SMALLINT ∈ {1..5}:
  ```python
  assert set(ce['Event_Channel_Type_Cd'].astype(int).unique()) <= {1, 2, 3, 4, 5}
  ```
- [ ] Event_Multimedia_Object_Ind CHAR(1) ∈ {'Y', 'N'} and is NOT NULL:
  ```python
  assert set(ce['Event_Multimedia_Object_Ind'].unique()) <= {'Y', 'N'}
  assert ce['Event_Multimedia_Object_Ind'].notna().all()
  ```
- [ ] Event_Received_Dttm populated and matches EVENT.Event_Start_Dttm on the same Event_Id:
  ```python
  assert ce['Event_Received_Dttm'].notna().all()
  ev_ts_cpl = {int(eid): ts for eid, ts in zip(ev['Event_Id'], ev['Event_Start_Dttm']) if int(eid) in complaint_ids}
  for _, row in ce.iterrows():
      assert row['Event_Received_Dttm'] == ev_ts_cpl[int(row['Event_Id'])]
  ```

**Cohort & scheduling invariants:**

- [ ] CHURNED-cohort customers have zero discretionary events after their cohort's earliest `close_dttm`:
  ```python
  from datetime import datetime as _dt
  churned_closures = {}  # party_id -> earliest close_dttm
  for ag in ctx.agreements:
      if ag.close_dttm is not None:
          prev = churned_closures.get(ag.owner_party_id)
          if prev is None or ag.close_dttm < prev:
              churned_closures[ag.owner_party_id] = ag.close_dttm
  ep_map = dict(zip(ep['Event_Id'].astype(int), ep['Party_Id'].astype(int)))
  offending = 0
  for eid in all_event_ids:
      pid = ep_map[eid]
      if pid in churned_closures:
          act = ev_activity[eid]
          if act in {'TRANSACTION', 'ACCESS', 'CONTACT'}:  # discretionary
              ts = ev_ts[eid]
              if ts > churned_closures[pid]:
                  offending += 1
  assert offending == 0, f'{offending} discretionary events after close_dttm'
  ```
  (Periodic FEE / INTEREST events also respect the window but are tested via the next item — at least one STATEMENT_FEE per agreement-month within the agreement's window.)
- [ ] Every agreement has **exactly one** STATEMENT_FEE event in each month of its `[open_dttm, close_dttm or SIM_DATE]` window — strict per-agreement-month coverage per Part H3. Uses the required `last_periodic_owner_map` test hook:
  ```python
  from datetime import date
  from config.settings import HISTORY_START as _HIST_START
  def month_bucket(d): return (d.year, d.month)
  def months_between(start, end):
      y, m = start.year, start.month
      out = []
      while (y, m) <= (end.year, end.month):
          out.append((y, m))
          m += 1
          if m == 13: m = 1; y += 1
      return out

  gen = Tier10Events()
  result = gen.generate(ctx)
  periodic_map = gen.last_periodic_owner_map  # Dict[event_id, agreement_id]
  assert periodic_map, 'Generator did not expose last_periodic_owner_map'

  fe = result['Core_DB.FINANCIAL_EVENT']
  ev_ts_map = dict(zip(ev['Event_Id'].astype(int), ev['Event_Start_Dttm']))

  # Build {agreement_id: set of year_months present with STATEMENT_FEE}
  stmt_fee_rows = fe[fe['Financial_Event_Type_Cd'] == 'STATEMENT_FEE']
  coverage: Dict[int, List[tuple]] = {}  # ag_id -> list of (year, month) — list (not set) to detect duplicates
  for eid_raw in stmt_fee_rows['Event_Id']:
      eid = int(eid_raw)
      ag_id = periodic_map[eid]   # KeyError here is a bug — fail fast
      coverage.setdefault(ag_id, []).append(month_bucket(ev_ts_map[eid].date()))

  missing, duplicated = [], []
  for ag in ctx.agreements:
      end = ag.close_dttm.date() if ag.close_dttm else SIM_DATE
      expected = months_between(max(ag.open_dttm.date(), _HIST_START), end)
      actual = coverage.get(ag.agreement_id, [])
      # Every expected month appears at least once
      for ym in expected:
          if ym not in actual:
              missing.append((ag.agreement_id, ym))
      # Every month in actual appears exactly once (no double-billing)
      seen = {}
      for ym in actual:
          seen[ym] = seen.get(ym, 0) + 1
      for ym, n in seen.items():
          if n > 1:
              duplicated.append((ag.agreement_id, ym, n))
      # No months outside the agreement's window
      for ym in actual:
          if ym not in expected:
              missing.append(('OUT_OF_WINDOW', ag.agreement_id, ym))
  assert not missing, f'STATEMENT_FEE coverage gap (first 5): {missing[:5]}'
  assert not duplicated, f'STATEMENT_FEE duplication (first 5): {duplicated[:5]}'
  ```
- [ ] Every periodic FINANCIAL_EVENT Event_Id is in `last_periodic_owner_map` and every mapped Agreement_Id resolves to `Core_DB.AGREEMENT`:
  ```python
  periodic_types = {'STATEMENT_FEE', 'OVERDRAFT_FEE', 'INTEREST_EARNED', 'INTEREST_PAID'}
  periodic_fe_ids = set(fe[fe['Financial_Event_Type_Cd'].isin(periodic_types)]['Event_Id'].astype(int))
  assert periodic_fe_ids.issubset(periodic_map.keys()), \
      f'Periodic events missing from map: {periodic_fe_ids - periodic_map.keys()}'
  assert set(periodic_map.values()).issubset(ag_ids), \
      f'Map references unknown agreements: {set(periodic_map.values()) - ag_ids}'
  # TRANSACTION (TRANSFER) events MUST NOT be in the periodic map — they are
  # linked via FUNDS_TRANSFER_EVENT.Originating_Agreement_Id instead.
  transfer_fe_ids = set(fe[fe['Financial_Event_Type_Cd'] == 'TRANSFER']['Event_Id'].astype(int))
  assert not (transfer_fe_ids & periodic_map.keys()), \
      'TRANSFER events leaked into last_periodic_owner_map'
  ```
- [ ] NEW-cohort customers have zero discretionary events before the earliest `open_dttm` of any of their agreements:
  ```python
  from datetime import datetime as _dt
  new_opens = {}  # party_id -> earliest open_dttm among their agreements
  for ag in ctx.agreements:
      prev = new_opens.get(ag.owner_party_id)
      if prev is None or ag.open_dttm < prev:
          new_opens[ag.owner_party_id] = ag.open_dttm
  new_party_ids = {cp.party_id for cp in ctx.customers if cp.lifecycle_cohort == 'NEW'}
  offending = 0
  for eid in all_event_ids:
      pid = ep_map[eid]
      if pid in new_party_ids and pid in new_opens:
          act = ev_activity[eid]
          if act in {'TRANSACTION', 'ACCESS', 'CONTACT'}:
              ts = ev_ts[eid]
              if ts < new_opens[pid]:
                  offending += 1
  assert offending == 0, f'{offending} NEW discretionary events before open_dttm'
  ```
- [ ] DECLINING-cohort event volume in last month is ≤ 1/3 of first month (envelope proof):
  ```python
  declining_ids = {cp.party_id for cp in ctx.customers if cp.lifecycle_cohort == 'DECLINING'}
  months = months_between(HISTORY_START, SIM_DATE)
  first_month, last_month = months[0], months[-1]
  first_ct = last_ct = 0
  for eid in all_event_ids:
      pid = ep_map[eid]
      if pid in declining_ids:
          act = ev_activity[eid]
          if act in {'TRANSACTION', 'ACCESS', 'CONTACT'}:
              mb = month_bucket(ev_ts[eid].date())
              if mb == first_month: first_ct += 1
              elif mb == last_month: last_ct += 1
  # envelope 1.0 → 0.2 means last ≤ ~30% of first
  if first_ct > 20:  # avoid noise on tiny harnesses
      assert last_ct <= first_ct * 0.40, f'DECLINING envelope too flat: {last_ct}/{first_ct}'
  ```

**BIGINT / dtype invariants:**

- [ ] Every `*_Id` column in every emitted DataFrame has dtype `Int64`:
  ```python
  id_cols = {
      'Core_DB.EVENT':                  ['Event_Id'],
      'Core_DB.EVENT_PARTY':            ['Event_Id', 'Party_Id'],
      'Core_DB.EVENT_CHANNEL_INSTANCE': ['Event_Id', 'Channel_Instance_Id'],
      'Core_DB.FINANCIAL_EVENT':        ['Event_Id'],
      'Core_DB.FINANCIAL_EVENT_AMOUNT': ['Event_Id'],
      'Core_DB.FUNDS_TRANSFER_EVENT':   ['Event_Id', 'Originating_Agreement_Id', 'Destination_Agreement_Id'],
      'Core_DB.ACCESS_DEVICE_EVENT':    ['Event_Id', 'Access_Device_Id'],
      'Core_DB.DIRECT_CONTACT_EVENT':   ['Event_Id'],
      'Core_DB.COMPLAINT_EVENT':        ['Event_Id'],
  }
  for tbl, cols in id_cols.items():
      df = result[tbl]
      for c in cols:
          assert str(df[c].dtype) == 'Int64', f'{tbl}.{c}: {df[c].dtype}'
  ```
- [ ] SMALLINT columns on COMPLAINT_EVENT are Int64 (pandas has no Int16; project convention):
  ```python
  for c in ('Event_Sentiment_Cd', 'Event_Channel_Type_Cd'):
      assert str(ce[c].dtype) == 'Int64', f'COMPLAINT_EVENT.{c}: {ce[c].dtype}'
  ```
- [ ] Column order in each DataFrame matches `_COLS_*` exactly (first N columns of the DataFrame in order — the DI tail is appended after):
  ```python
  from generators.tier10_events import (
      _COLS_EVENT, _COLS_EVENT_PARTY, _COLS_EVENT_CHANNEL_INSTANCE,
      _COLS_FINANCIAL_EVENT, _COLS_FINANCIAL_EVENT_AMOUNT,
      _COLS_FUNDS_TRANSFER_EVENT, _COLS_ACCESS_DEVICE_EVENT,
      _COLS_DIRECT_CONTACT_EVENT, _COLS_COMPLAINT_EVENT,
  )
  col_lists = {
      'Core_DB.EVENT':                  _COLS_EVENT,
      'Core_DB.EVENT_PARTY':            _COLS_EVENT_PARTY,
      'Core_DB.EVENT_CHANNEL_INSTANCE': _COLS_EVENT_CHANNEL_INSTANCE,
      'Core_DB.FINANCIAL_EVENT':        _COLS_FINANCIAL_EVENT,
      'Core_DB.FINANCIAL_EVENT_AMOUNT': _COLS_FINANCIAL_EVENT_AMOUNT,
      'Core_DB.FUNDS_TRANSFER_EVENT':   _COLS_FUNDS_TRANSFER_EVENT,
      'Core_DB.ACCESS_DEVICE_EVENT':    _COLS_ACCESS_DEVICE_EVENT,
      'Core_DB.DIRECT_CONTACT_EVENT':   _COLS_DIRECT_CONTACT_EVENT,
      'Core_DB.COMPLAINT_EVENT':        _COLS_COMPLAINT_EVENT,
  }
  for tbl, cols in col_lists.items():
      df = result[tbl]
      assert list(df.columns[:len(cols)]) == cols, f'{tbl}: got {list(df.columns[:len(cols)])}'
  ```

**DI column invariants:**

- [ ] All 9 tables have the 5-col DI tail with `di_start_ts = '2000-01-01 00:00:00.000000'`, `di_end_ts = '9999-12-31 00:00:00.000000'`, `di_rec_deleted_Ind = 'N'`:
  ```python
  for tbl in result:
      df = result[tbl]
      assert (df['di_start_ts'] == '2000-01-01 00:00:00.000000').all(), tbl
      assert (df['di_end_ts'] == '9999-12-31 00:00:00.000000').all(), tbl
      assert (df['di_rec_deleted_Ind'] == 'N').all(), tbl
      # DI tail is the last 3 meaningful columns (data_src/proc_name are nullable sibs)
      assert 'di_start_ts' in df.columns and 'di_end_ts' in df.columns
  ```
- [ ] No `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` columns appear on any of the 9 tables (Core_DB only per PRD §7.3):
  ```python
  for tbl in result:
      df = result[tbl]
      for c in ('Valid_From_Dt', 'Valid_To_Dt', 'Del_Ind'):
          assert c not in df.columns, f'{tbl} has forbidden column {c}'
  ```

**Side-effect / no-mutation invariants:**

- [ ] `generate()` does not mutate `ctx.tables`:
  ```python
  tables_before = dict(ctx.tables)  # shallow copy
  _ = Tier10Events().generate(ctx)
  assert ctx.tables == tables_before
  ```
- [ ] `generate()` advances `ctx.rng` state (lots of entropy consumed — hundreds of thousands of draws):
  ```python
  before = ctx.rng.bit_generator.state
  _ = Tier10Events().generate(ctx)
  after = ctx.rng.bit_generator.state
  assert before != after, 'ctx.rng not consumed — random draws bypassed ctx.rng?'
  ```
- [ ] `generate()` advances `ctx.ids.peek('event')` by exactly `len(EVENT)`:
  ```python
  before_peek = ctx.ids.peek('event')
  result2 = Tier10Events().generate(ctx)  # fresh invocation on a fresh ctx
  # ... this requires a fresh ctx; run in isolation
  # Simpler: verify Event_Id range is contiguous within [before_peek, before_peek + N)
  evs = sorted(result2['Core_DB.EVENT']['Event_Id'].astype(int).tolist())
  assert evs[0] >= 50_000_000  # 'event' range start
  # Event_Ids need not be strictly contiguous across streams (IdFactory dispenses
  # sequentially but streams may interleave); they must all be distinct and
  # within [50_000_000, peek_after).
  assert len(set(evs)) == len(evs)
  ```

**Reproducibility:**

- [ ] Running `Tier10Events().generate(ctx)` twice on two freshly-built universes with `SEED = 42` produces byte-identical DataFrames across all 9 tables:
  ```python
  # Rebuild from scratch to avoid ctx.rng state carrying over
  import numpy as np
  from config.settings import SEED
  from registry.universe import UniverseBuilder
  # ... full Tier0..Tier9 harness run twice; assert frame-equal for all 9 keys
  r1 = build_and_run()
  r2 = build_and_run()
  for key in sorted(r1):
      pd.testing.assert_frame_equal(r1[key], r2[key], check_dtype=True)
  ```
  (Session may substitute a lighter harness as long as the reproducibility claim is demonstrated end-to-end with the full Tier 10 output.)

## Handoff notes

**Shipped (2026-04-20):**
- `generators/tier10_events.py` created — `Tier10Events(BaseGenerator)` producing all 9 Core_DB event DataFrames
- 3-stream architecture: `_build_discretionary_event_stream`, `_build_complaint_event_stream`, `_build_periodic_financial_event_stream`
- All 30+ DoD assertions pass: 99,510 events (SEED=42), sub-type exclusivity, STATEMENT_FEE coverage, BIGINT/Int64 dtypes, DI columns, reproducibility
- Event counts: EVENT=99510, FE=68654, FTE=11485, ADE=22283, DCE=8428, CE=145 (4.8% of customers)

**DoD spec correction (spec conflict §2):**
- DoD STATEMENT_FEE coverage test (line 677) had `expected = months_between(ag.open_dttm.date(), end)` — this generated expected months back to 2017 for agreements opened pre-history
- Corrected to `expected = months_between(max(ag.open_dttm.date(), _HIST_START), end)` — clips to the 6-month history window, consistent with design intent and FINANCIAL_EVENT row count estimates (60k–90k)
- Added `from config.settings import HISTORY_START as _HIST_START` import to that test block

**Deferrals:** None — all spec items implemented

**Next session hint:** Step 21 (Tier 11 CRM). Tier10Events is complete and integrated. `main.py` still a stub — the orchestrator wiring is deferred to a later step.

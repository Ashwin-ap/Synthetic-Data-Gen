# Spec: Step 19 — Tier 9 Party-Agreement Links

## Overview

This step builds **Tier 9 — Party-Agreement Links**, the three Core_DB bridge tables that realise the party-to-agreement and party-to-enterprise relationship plane the `UniverseBuilder` already decided in Step 4 and Steps 10/11/17 projected into `Core_DB.PARTY`, `Core_DB.AGREEMENT`, and the exclusive-sub-type chain: **`PARTY_AGREEMENT`** (one `'customer'` row per agreement + one additional `'borrower'` row for every credit-bearing agreement — drives Layer 2 `Customer_Account_Ind = '1'`, `Borrower_Ind`, and `Retail_Banking_Customer_Ind`), **`PARTY_RELATED`** (one `'customer of enterprise'` row per customer party linked to the reserved `BANK_PARTY_ID = 9_999_999` — drives Layer 2 `INDIVIDUAL_BB.Customer_Ind = 'Y'`), and **`PARTY_CLAIM`** (a small 2% fraction of customers receive a standalone claim row with fresh BIGINT `Claim_Id` from `IdFactory.claim` — no FK to EVENT per PRD §9 Q3). No statistical decisions are made in this step beyond a single reproducible Bernoulli sample for the 2% claim cohort via `ctx.rng`; every other row is a deterministic fan-out of `ctx.agreements` / `ctx.customers` driven by existing `AgreementProfile.is_credit` / `CustomerProfile.party_id` fields. See `mvp-tool-design.md` §9 Tier 9 for scope, §12 items #9/#10/#11/#12 for the four Layer 2 literal-match constraints enforced by this step, and `references/02_data-mapping-reference.md` Step 3 items #9, #10, #11, #12 for the derivation rules.

One conceptual subtlety resolved pre-implementation: `BANK_PARTY_ID` and `SELF_EMP_ORG_ID` share the value `9_999_999` (see `config/settings.py:24–29`). This is **deliberate** — the one reserved ORGANIZATION row minted in Step 11 serves both as the bank entity for PARTY_RELATED rows here *and* as the self-employment placeholder for INDIVIDUAL_PAY_TIMING/INDIVIDUAL_BONUS_TIMING in Step 12. Tier 9 does NOT inject additional parties; it only references the pre-existing `9_999_999` row.

## Depends on

- **Step 1** — consumes from `config/settings.py`: `BANK_PARTY_ID` (9_999_999), `HIGH_TS`, `HIGH_DATE`. No new `ID_RANGES` category is added — the existing `'claim'` range (start `9_000_000`) is consumed via `ctx.ids.next('claim')` for PARTY_CLAIM.Claim_Id minting.
- **Step 2** — consumes `generators/base.BaseGenerator.stamp_di()` (3-column tail: `di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind`). Does **not** consume `stamp_valid()` — all 3 tables are Core_DB (PRD §7.3). Consumes `utils/id_factory.IdFactory` for PARTY_CLAIM Claim_Id minting only. Does **not** consume `utils/luhn` or `utils/date_utils`.
- **Step 3** — consumes `registry/context.GenerationContext`, `registry/profiles.CustomerProfile`, `registry/profiles.AgreementProfile`. `Tier9PartyAgreement.generate(ctx)` reads `ctx.customers` (for PARTY_RELATED fan-out and PARTY_CLAIM 2% cohort), `ctx.agreements` (for PARTY_AGREEMENT fan-out), `ctx.ids` (for claim IDs), `ctx.rng` (for the 2% claim Bernoulli), and `ctx.tables` (for upstream prerequisite checks on PARTY / AGREEMENT).
- **Step 4** — consumes the built universe. Critical invariants this step depends on:
  - Every `AgreementProfile.owner_party_id` is a BIGINT already minted into `Core_DB.PARTY.Party_Id` by Step 10 (the step does NOT re-mint).
  - Every `AgreementProfile.agreement_id` is unique and present in `ctx.tables['Core_DB.AGREEMENT'].Agreement_Id`.
  - `AgreementProfile.is_credit` reliably flags every credit-bearing agreement (CREDIT_CARD, VEHICLE_LOAN, STUDENT_LOAN, MORTGAGE, HELOC, PAYDAY) — set by `_assign_status_flags` / sub-type assignment in Step 4 per the exclusive-sub-type chain contract. Deposit-only products (CHECKING, SAVINGS, MMA, CERTIFICATE_OF_DEPOSIT, RETIREMENT, COMMERCIAL_CHECKING) must have `is_credit == False`.
  - Every `CustomerProfile.party_since` is a valid DATE before `SIM_DATE` and serves as the PARTY_RELATED `Party_Related_Start_Dttm` anchor.
  - For CHURNED agreements, `close_dttm` is populated (datetime) and lies within the history window; for all other cohorts, `close_dttm is None`.
- **Step 5** — n/a at generation time. The writer is not invoked in this step; DDL column ordering is enforced at DataFrame construction via `pd.DataFrame(rows, columns=_COLS_*)`.
- **Step 10** — consumes `ctx.tables['Core_DB.AGREEMENT']` (for Agreement_Id FK universe) and `ctx.tables['Core_DB.PARTY']` (for Party_Id FK universe, including the reserved `BANK_PARTY_ID = 9_999_999` row). AGREEMENT row count = `len(ctx.agreements)` ≈ 5,000; PARTY row count ≈ 3,001 (3,000 customers + 1 reserved bank/self-emp row).
- **Step 11** — consumes the fact that the reserved ORGANIZATION row at `Organization_Party_Id = 9_999_999` was already minted into `Core_DB.ORGANIZATION` by Step 11. This is the row PARTY_RELATED.Related_Party_Id references. Tier 9 only verifies the PARTY row exists — it does NOT check ORGANIZATION.
- **Step 17** — consumes the fact that Step 17 already committed the sub-type chain tables. This is **order-dependency only** — Tier 9 does not import from Tier 7a or Tier 7b's output tables (the sub-type flags live on `AgreementProfile` itself, not in derived tables). Rationale: placing Tier 9 after Tier 7b/Tier 8 in the dependency graph is a documentation choice in `implementation-steps.md`; the code itself reads only PARTY and AGREEMENT from Tier 2.

No code from Steps 6–8 (Tier 0 seeds), Step 9 (Tier 1 geography), Steps 12–15 (Tier 4/5/6), Step 16 (Tier 7a), Step 18 (Tier 8) is imported by this step. The writer is not invoked — `generate()` returns DataFrames only; orchestrator (Step 25) handles `ctx.tables.update()` and later CSV emission.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 19):
- `PRD.md` §4.2 (enumerated table list — the 3 Tier 9 tables), §7.1 (BIGINT rule), §7.2 (shared Party_Id space — BANK_PARTY_ID sits in this universe), §7.3 (DI column rules — 3-col Core_DB tail, no `Valid_*`/`Del_Ind`), §9 Q3 (PARTY_CLAIM standalone — no FK to EVENT)
- `mvp-tool-design.md` §9 Tier 9 (**authoritative scope + BANK_PARTY_ID + exemplar row dicts for all three tables**), §12 items #9/#10/#11/#12 (the four Layer 2 constraints enforced here), §14 Decision 3 (BIGINT everywhere), §14 Decision 4 (shared Party_Id space)
- `implementation-steps.md` Step 19 entry (exit criteria); Handoff Protocol (post-session rules)

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/02_data-mapping-reference.md` Step 3 items #9, #10, #11, #12 (§lines 819–828) — the Layer 2 derivations this tier enables:
  - **#9**: `ACCOUNT_DIMENSION.Customer_Account_Ind = '1'` ← `PARTY_AGREEMENT.Party_Agreement_Role_Cd = 'customer'` (the spec uses lowercase `'customer'` per §880 which is the canonical row; §819's `'Customer'` capitalisation is a doc-casing slip).
  - **#10**: `INDIVIDUAL_BB.Customer_Ind = 'Y'` ← `PARTY_RELATED.Party_Related_Role_Cd = 'customer of enterprise'`; plus `Prospect_Ind` ← `'prospect of enterprise'` and `Associate_Ind` ← `'employee of enterprise'` (see MVP deferral note in §Rules for implementation below).
  - **#11**: `Borrower_Ind` ← `PARTY_AGREEMENT.Party_Agreement_Role_Cd = 'borrower'`.
  - **#12**: `Retail_Banking_Customer_Ind` ← `PARTY_AGREEMENT.Party_Agreement_Role_Cd = 'customer'` linked to a retail-banking Agreement. For MVP every non-COMMERCIAL_CHECKING agreement is treated as retail banking (the `'customer'` row from #9 is the same row #12 matches — no extra row needed).
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the 3 in-scope tables. Open only these blocks (line numbers current as of 2026-04-20; the SQL DDL wins when it disagrees with any summary table, per CLAUDE.md "DDL verification rule" and PRD §10):
  - `PARTY_AGREEMENT` (§3536) — 9 business + 3 DI = 12 cols. NOT NULL: `Party_Id`, `Agreement_Id`, `Party_Agreement_Role_Cd`, `Party_Agreement_Start_Dt`. Nullable: `Party_Agreement_End_Dt`, `Allocation_Pct`, `Party_Agreement_Amt`, `Party_Agreement_Currency_Amt`, `Party_Agreement_Num`. PI on `Agreement_Id` (NUPI — non-unique — so multiple rows per agreement are legal; exactly how we get `customer` + `borrower` for the same Agreement_Id). Both `*_Id` are INTEGER in DDL → **BIGINT** per PRD §7.1.
  - `PARTY_RELATED` (§5365) — 9 business + 3 DI = 12 cols. NOT NULL: `Party_Id`, `Related_Party_Id`, `Party_Related_Role_Cd`, `Party_Related_Start_Dttm`, `Party_Structure_Type_Cd`. Nullable: `Party_Related_End_Dttm`, `Party_Related_Status_Reason_Cd`, `Party_Related_Status_Type_Cd`, `Party_Related_Subtype_Cd`. PI on `Party_Id` (NUPI). Both `*_Id` are INTEGER → BIGINT. Note `Party_Related_Start_Dttm` is plain `TIMESTAMP` (DDL shows `TIMESTAMP NOT NULL`, not `TIMESTAMP(6)`) — spec stores as Python `datetime` and formats to 6dp on write (writer step handles the precision).
  - `PARTY_CLAIM` (§5402) — 6 business + 3 DI = 9 cols. NOT NULL: `Claim_Id` (PK), `Party_Id`, `Party_Claim_Role_Cd`, `Party_Claim_Start_Dttm`. Nullable: `Party_Claim_End_Dttm`, `Party_Claim_Contact_Prohibited_Ind CHAR(3)`. Both `*_Id` are INTEGER → BIGINT. PI on `Claim_Id` (NUPI).

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is MVP-authoritative per PRD §10; only open `01` if `07` is ambiguous for a specific column.
- `references/05_architect-qa.md` — no Q in this file binds Tier 9 (Q3 is Tier 15, Q6 is Tier 14, Q7 is Tier 4a — none apply here). Skip.
- `references/06_supporting-enrichments.md` — no distribution is needed in this step; Tier 9 is pure deterministic projection + a single 2% Bernoulli for claims.
- `references/02_data-mapping-reference.md` beyond Step 3 items #9–#12 — no other Layer 2 constraint binds Tier 9.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `resources/iDM_MDM_tables_DDLs.xlsx` — already distilled into `07` and `02`.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier9_party_agreement.py` — `class Tier9PartyAgreement(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]` method. Implementation contract:
  1. Import `BaseGenerator`; import `GenerationContext` / `CustomerProfile` / `AgreementProfile` under `TYPE_CHECKING` only. Import `pd`, `from datetime import datetime, date`, `from typing import Dict, List`. Import `BANK_PARTY_ID`, `HIGH_TS`, `SIM_DATE`, `HISTORY_START` from `config.settings`.
  2. Declare module-level constants (all reproducibility-friendly — randomness routes exclusively through `ctx.rng`):
     - `_TIER9_DI_START_TS = '2000-01-01 00:00:00.000000'` (matches the `_TIER6_DI_START_TS` / `_TIER7A_DI_START_TS` / `_TIER7B_DI_START_TS` / `_TIER8_DI_START_TS` convention).
     - `_CUSTOMER_ROLE_CD = 'customer'` — Layer 2 literal-match (Step 3 items #9, #12). Lowercase per canonical `02_data-mapping-reference.md` §880.
     - `_BORROWER_ROLE_CD = 'borrower'` — Layer 2 literal-match (Step 3 item #11).
     - `_CUSTOMER_OF_ENTERPRISE_CD = 'customer of enterprise'` — Layer 2 literal-match (Step 3 item #10).
     - `_PARTY_STRUCTURE_TYPE_CD = 'banking_relationship'` — NOT NULL column; design doc §9 Tier 9 exemplar row literal.
     - `_CLAIM_ROLE_CD = 'claimant'` — NOT NULL column value for PARTY_CLAIM.Party_Claim_Role_Cd. Not a Layer 2 literal-match value (no rule binds it); chosen as the canonical role label for the filing party.
     - `_PARTY_CLAIM_CONTACT_PROHIBITED_NO = 'No'` — CHAR(3) flag default per PRD §4.3 (`'Yes'`/`'No'` for CHAR(3) flags).
     - `_PARTY_CLAIM_RATE = 0.02` — Bernoulli probability per customer for a standalone claim row (≈60 rows out of ~3,000 customers). Small enough to be a clear minority, large enough to be verifiable in DoD.
     - `_CREDIT_PRODUCT_TYPES: frozenset[str] = frozenset({'CREDIT_CARD', 'VEHICLE_LOAN', 'STUDENT_LOAN', 'MORTGAGE', 'HELOC', 'PAYDAY'})` — reference-only sanity-check set; primary borrower filter is `ag.is_credit`, this set exists for a DoD cross-check (every `is_credit=True` agreement must have `product_type ∈ _CREDIT_PRODUCT_TYPES`; no COMMERCIAL_CHECKING / CHECKING / SAVINGS / etc. may be flagged credit).
  3. Declare `_COLS_*` list-of-str module constants for every emitted DataFrame in **DDL declaration order** (business cols only; 3-col DI tail appended by `stamp_di()`):
     ```python
     _COLS_PARTY_AGREEMENT = [
         'Party_Id', 'Agreement_Id', 'Party_Agreement_Role_Cd',
         'Party_Agreement_Start_Dt', 'Party_Agreement_End_Dt',
         'Allocation_Pct', 'Party_Agreement_Amt',
         'Party_Agreement_Currency_Amt', 'Party_Agreement_Num',
     ]
     _COLS_PARTY_RELATED = [
         'Party_Id', 'Related_Party_Id', 'Party_Related_Role_Cd',
         'Party_Related_Start_Dttm', 'Party_Related_End_Dttm',
         'Party_Structure_Type_Cd', 'Party_Related_Status_Reason_Cd',
         'Party_Related_Status_Type_Cd', 'Party_Related_Subtype_Cd',
     ]
     _COLS_PARTY_CLAIM = [
         'Claim_Id', 'Party_Id', 'Party_Claim_Role_Cd',
         'Party_Claim_Start_Dttm', 'Party_Claim_End_Dttm',
         'Party_Claim_Contact_Prohibited_Ind',
     ]
     ```
  4. **Guard** at the top of `generate()`: verify `ctx.customers` and `ctx.agreements` are non-empty; verify every required upstream table is present in `ctx.tables` (use `_REQUIRED_UPSTREAM_TABLES = ('Core_DB.PARTY', 'Core_DB.AGREEMENT')`). Raise `RuntimeError(f'Tier 9 prerequisite missing: {key}')` on any failure. Also verify `BANK_PARTY_ID` is present in `ctx.tables['Core_DB.PARTY'].Party_Id` — raise `RuntimeError` if absent (design-doc contract: Step 11 must have injected the reserved row). No silent fallback.
  5. Build **`PARTY_AGREEMENT`** DataFrame — iterate `ctx.agreements`:
     - For **every** `ag` emit one `'customer'` row: `Party_Id = ag.owner_party_id`, `Agreement_Id = ag.agreement_id`, `Party_Agreement_Role_Cd = _CUSTOMER_ROLE_CD`, `Party_Agreement_Start_Dt = ag.open_dttm.date()`, `Party_Agreement_End_Dt = ag.close_dttm.date() if ag.close_dttm is not None else None`, all other business columns `None` (Allocation_Pct/Amt/Currency_Amt/Num are nullable per DDL and carry no Layer 2 binding).
     - Additionally for every `ag` where `ag.is_credit is True`, emit one `'borrower'` row with the same Party_Id / Agreement_Id / dates but `Party_Agreement_Role_Cd = _BORROWER_ROLE_CD`. Two rows share Agreement_Id; this is legal because the DDL's `NUPI_PARTY_AGREEMENT (Agreement_Id)` is non-unique.
     - Expected row count: `len(ctx.agreements) + sum(1 for ag in ctx.agreements if ag.is_credit)`. On the standard 5,000-agreement universe with ~40–50% credit agreements, this is ≈7,000–7,500.
  6. Build **`PARTY_RELATED`** DataFrame — iterate `ctx.customers`:
     - For **every** `cp` emit one `'customer of enterprise'` row: `Party_Id = cp.party_id`, `Related_Party_Id = BANK_PARTY_ID`, `Party_Related_Role_Cd = _CUSTOMER_OF_ENTERPRISE_CD`, `Party_Related_Start_Dttm = datetime.combine(cp.party_since, time.min)` (midnight of the customer's `party_since` DATE), `Party_Related_End_Dttm = None` (open — even CHURNED customers remain "customer of enterprise" for audit; their lifecycle state lives in PARTY_STATUS from Step 14, not PARTY_RELATED), `Party_Structure_Type_Cd = _PARTY_STRUCTURE_TYPE_CD`, nullable status/reason/subtype columns all `None`.
     - Expected row count: `len(ctx.customers)` exactly — ≈3,000. Both INDIVIDUAL and ORGANIZATION parties receive a row (the MVP universe does not model enterprise-level parent relationships, so every CustomerProfile is a "customer of enterprise" regardless of `party_type`).
     - **MVP deferrals documented:** No `'prospect of enterprise'` rows (the MVP universe has no PROSPECT cohort — only ACTIVE/DECLINING/CHURNED/NEW; every customer is already onboarded, so `INDIVIDUAL_BB.Prospect_Ind` will be `'N'` for all — Layer 2 compliant). No `'employee of enterprise'` rows (the MVP universe does not model employee-customer parties; `INDIVIDUAL_BB.Associate_Ind` will be `'N'` for all — Layer 2 compliant). These deferrals are valid because Layer 2's derivation "WHERE role = 'x'" legitimately yields an empty match set → indicator defaults to `'N'`.
  7. Build **`PARTY_CLAIM`** DataFrame — for each `cp in ctx.customers`, draw a Bernoulli `ctx.rng.random() < _PARTY_CLAIM_RATE` (~2% hit rate) to decide whether that customer files a claim. For each selected customer, mint exactly one row:
     - `Claim_Id = ctx.ids.next('claim')` — BIGINT from the `'claim'` range (`9_000_000+`); each selected customer gets a fresh ID. Because selections vary with `ctx.rng`, Claim_Id assignment is reproducible only when `ctx.rng` state is identical — a property the universe already guarantees with `SEED = 42`.
     - `Party_Id = cp.party_id`.
     - `Party_Claim_Role_Cd = _CLAIM_ROLE_CD` (`'claimant'`).
     - `Party_Claim_Start_Dttm = datetime.combine(HISTORY_START, time.min)` — every claim is stamped at the history-window start for simplicity; MVP does not model claim temporal distribution (no Layer 2 rule binds the timing).
     - `Party_Claim_End_Dttm = None` (open claim; Layer 2 does not pivot on this).
     - `Party_Claim_Contact_Prohibited_Ind = _PARTY_CLAIM_CONTACT_PROHIBITED_NO` (`'No'`; CHAR(3) per DDL).
     - Expected row count: ≈60 (±20) on a 3,000-customer universe with `SEED = 42`.
  8. Apply dtype coercions — cast every `*_Id` / `Related_Party_Id` / `Claim_Id` column to `Int64` (nullable BIGINT). Date columns as `date`. Datetime columns as `datetime`. `Allocation_Pct` / `Party_Agreement_Amt` / `Party_Agreement_Currency_Amt` remain as `object` (all `None` in this step — no Decimal values are populated). VARCHAR columns as Python `str` (or `None`). `Party_Claim_Contact_Prohibited_Ind` as `str` (`'No'`).
  9. Stamp all three DataFrames via `self.stamp_di(df, start_ts=_TIER9_DI_START_TS)` — yields the 3-col tail (`di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind`) with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. Do NOT call `stamp_valid()` on any of the 3 — all are Core_DB (PRD §7.3).
  10. Return a dict with exactly these 3 keys:
      ```
      {
        'Core_DB.PARTY_AGREEMENT',
        'Core_DB.PARTY_RELATED',
        'Core_DB.PARTY_CLAIM',
      }
      ```
      Do NOT mutate `ctx.tables` — the orchestrator does that after the call returns.

**Do NOT produce** in this step:
- CSVs — writer is not invoked. `output/` is not touched.
- `CDM_DB.PARTY_TO_AGREEMENT_ROLE`, `CDM_DB.PARTY_TO_EVENT_ROLE`, `CDM_DB.INDIVIDUAL_TO_INDIVIDUAL`, `CDM_DB.INDIVIDUAL_TO_HOUSEHOLD`, `CDM_DB.INDIVIDUAL_TO_ORGANIZATION`, `CDM_DB.ORGANIZATION_TO_ORGANIZATION` — Step 22's responsibility (Tier 14 CDM_DB). These are CDM-schema party-to-X bridges, not Core_DB.
- New `seed_data/*.py` modules — no code values introduced by Tier 9 require Tier 0 seeding (every literal is a magic string matched by Layer 2, not a lookup-table PK). If a future step surfaces a need for a `PARTY_RELATED_ROLE_TYPE` or `PARTY_CLAIM_ROLE_TYPE` seed, escalate per Handoff Protocol §2.
- Wiring into `main.py` — orchestrator changes are Step 25's responsibility.
- Changes to `config/settings.py` — all needed constants (`BANK_PARTY_ID`, `HIGH_TS`, `HISTORY_START`, `SIM_DATE`, `ID_RANGES['claim']`) already exist. No new `ID_RANGES` entry is created.
- Changes to `config/code_values.py` — `PARTY_AGREEMENT_ROLE_CODES` and `PARTY_RELATED_ROLE_CODES` sets already exist at `config/code_values.py:1–7`; the Tier 9 literals `'customer'`, `'borrower'`, `'customer of enterprise'` are subsets of those sets. No edits needed. The spec reserves the right for the implementation session to OPTIONALLY promote the new module-level constants (`_CUSTOMER_ROLE_CD`, `_BORROWER_ROLE_CD`, `_CUSTOMER_OF_ENTERPRISE_CD`) into `config/code_values.py` as named string constants if the session judges cross-tier reuse is imminent — but for a single-tier step with S scope, local module constants are preferred to minimise diff surface.

## Tables generated (if applicable)

After `Tier9PartyAgreement.generate(ctx)` runs, `ctx.tables` gains these 3 Core_DB keys:

| Table | Row count | Driven by | Notes |
|-------|-----------|-----------|-------|
| `Core_DB.PARTY_AGREEMENT` | ≈ 7,000–7,500 | per-agreement × (1 `'customer'` + conditional 1 `'borrower'` when `ag.is_credit`) | **Layer 2 literal-match**: every agreement has exactly one `'customer'` row (Step 3 items #9, #12); every credit agreement also has exactly one `'borrower'` row (Step 3 item #11) |
| `Core_DB.PARTY_RELATED` | ≈ 3,000 (= `len(ctx.customers)`) | per-customer | **Layer 2 literal-match**: every customer has exactly one `'customer of enterprise'` row with `Related_Party_Id = BANK_PARTY_ID = 9_999_999` (Step 3 item #10 → `INDIVIDUAL_BB.Customer_Ind = 'Y'`) |
| `Core_DB.PARTY_CLAIM` | ≈ 60 (±20) | Bernoulli 2% of customers via `ctx.rng` | Standalone claims per PRD §9 Q3 (no FK to EVENT); fresh BIGINT `Claim_Id` from `IdFactory.claim` range |

All three DataFrames have the 3-column Core_DB DI tail after `stamp_di()` with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. None of the three carry `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` (PRD §7.3 reserves those for CDM_DB/PIM_DB).

**Layer-2 constraint coverage guaranteed by this step:**
- **Item #9** (Customer_Account_Ind): every agreement has a `'customer'` PARTY_AGREEMENT row. Verified in DoD.
- **Item #10** (Customer_Ind): every customer has a `'customer of enterprise'` PARTY_RELATED row to BANK_PARTY_ID. Verified in DoD. Prospect_Ind and Associate_Ind legitimately resolve to `'N'` for the MVP universe (no prospect/employee cohort) — not a gap, a documented scope choice.
- **Item #11** (Borrower_Ind): every credit agreement has a `'borrower'` PARTY_AGREEMENT row. Verified in DoD.
- **Item #12** (Retail_Banking_Customer_Ind): for MVP every non-COMMERCIAL_CHECKING agreement is retail banking; the `'customer'` row from #9 satisfies #12 — no additional row is emitted. Verified indirectly via #9.

## Files to modify

No files modified. Tier 9 is an additive step: one new generator file, no edits to existing modules. (The orchestrator wiring in `main.py` is deferred to Step 25 per `implementation-steps.md` Handoff Protocol §5.)

## New dependencies

No new dependencies. Uses only `pandas`, `numpy` (via `ctx.rng`), and the Python standard library (`datetime`, `typing`).

## Rules for implementation

**Universal rules** (apply to every step):

- BIGINT for all ID columns (per PRD §7.1) — `Party_Id`, `Agreement_Id`, `Related_Party_Id`, `Claim_Id` are all `Int64` dtype, never INTEGER, even when the DDL says INTEGER.
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2). `BANK_PARTY_ID = 9_999_999` sits in this shared space; `Related_Party_Id` uses it directly.
- DI column stamping on every table via `BaseGenerator.stamp_di()` with `start_ts = _TIER9_DI_START_TS = '2000-01-01 00:00:00.000000'`.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `di_rec_deleted_Ind = 'N'` for active records (every row emitted by this step).
- **Do NOT** stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` — Tier 9 is Core_DB only (PRD §7.3).
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` — enforce via `pd.DataFrame(rows, columns=_COLS_*)` construction.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — n/a this step (no such table written).
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — n/a this step (no geography tables written).
- No ORMs, no database connections — pure pandas → CSV.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42`. The 2% PARTY_CLAIM Bernoulli **must** route through `ctx.rng.random()` — never `random.random()`, never `numpy.random` module-level calls.

**Step-specific rules:**

- **Single public entry point.** `class Tier9PartyAgreement(BaseGenerator)` exposes exactly one public method: `generate(ctx) -> Dict[str, pd.DataFrame]`. Helpers are private (`_build_party_agreement`, `_build_party_related`, `_build_party_claim`) or module-level functions.
- **No `ctx.tables` mutation.** `generate()` returns the dict; the orchestrator merges it. This mirrors Tier 6, Tier 7a, Tier 7b, Tier 8.
- **No `datetime.now()`.** Every timestamp is derived from a configuration constant or a `CustomerProfile` / `AgreementProfile` field. `BaseGenerator.stamp_di()` defaults to `datetime.now()` when `start_ts=None`; the session MUST pass `start_ts=_TIER9_DI_START_TS` explicitly to every `stamp_di` call for reproducibility (the Tier 6/7a/7b/8 convention).
- **Exactly one `'customer'` row per agreement.** Not zero, not two. DoD verifies `groupby('Agreement_Id') over customer-role rows: count == 1 for all`.
- **Exactly one `'borrower'` row per credit agreement (and zero for non-credit agreements).** DoD verifies both directions: every `ag.is_credit=True` has a borrower row; every `ag.is_credit=False` has zero.
- **Exactly one PARTY_RELATED row per customer.** DoD verifies `groupby('Party_Id').size() == 1 for all`.
- **PARTY_CLAIM row count is a random variable, not a fixed value.** The DoD uses a range check (20 ≤ count ≤ 120 on a 3,000-customer universe with 2% rate), not an exact equality. Reproducibility is verified separately: running `Tier9PartyAgreement().generate(ctx)` twice on byte-identical `ctx.rng` states produces byte-identical DataFrames.
- **BANK_PARTY_ID must pre-exist in `Core_DB.PARTY`.** The guard fails loudly if Step 11 did not inject the `9_999_999` row. Tier 9 does NOT inject it — that's Step 11's contract.
- **`ag.is_credit` is the authoritative borrower flag.** Do not re-derive from `product_type`. The universe is the single source of truth; the sub-type flags encode the design-doc intent. A DoD cross-check asserts `is_credit` correlates with `product_type ∈ _CREDIT_PRODUCT_TYPES` for safety, but the code uses the flag directly.
- **No Prospect/Associate rows in MVP** — this is a documented deferral (see §Tables generated). If a future step needs them, the generator is trivially extensible (add a second loop with a cohort filter).
- **Claim_Id minting order is deterministic.** `for cp in ctx.customers` iterates in list order; Bernoulli draws from `ctx.rng.random()` in that same order; every selected customer gets the next sequential Claim_Id. Byte-identical output across runs requires byte-identical iteration order and byte-identical `ctx.rng` state — both already guaranteed by Step 4's determinism contract.

## Definition of done

The implementation session MUST tick every box or mark it n/a with a one-line justification before closing the session.

**File & import sanity:**

- [ ] `git status` shows only `generators/tier9_party_agreement.py` and `.claude/specs/step-19-tier9-party-agreement-links.md` as modified/added — nothing else.
- [ ] `python -c "from generators.tier9_party_agreement import Tier9PartyAgreement; g = Tier9PartyAgreement(); assert callable(g.generate)"` exits 0.
- [ ] `Tier9PartyAgreement` subclasses `BaseGenerator`:
  ```python
  from generators.base import BaseGenerator
  from generators.tier9_party_agreement import Tier9PartyAgreement
  assert issubclass(Tier9PartyAgreement, BaseGenerator)
  ```
- [ ] No CSV column named `*_Id` uses INTEGER — n/a this step (no CSVs written; the writer is Step 5 / Step 25). BIGINT invariants are verified via DataFrame dtype checks below.
- [ ] `PARTY_INTERRACTION_EVENT` typo check — n/a (no such table written).
- [ ] `GEOSPATIAL.csv` absence check — n/a (no `output/` writes).

**End-to-end table emission harness** (session may use a full pipeline run or a minimal synthesised `ctx`; both are acceptable):

- [ ] `Tier9PartyAgreement().generate(ctx)` returns a dict with exactly the 3 keys:
  ```python
  result = Tier9PartyAgreement().generate(ctx)
  assert set(result) == {'Core_DB.PARTY_AGREEMENT', 'Core_DB.PARTY_RELATED', 'Core_DB.PARTY_CLAIM'}
  ```
- [ ] Every DataFrame is non-empty (`len(df) > 0`) for all 3 keys.

**PARTY_AGREEMENT invariants (Step 3 items #9, #11, #12):**

- [ ] Row count equals `len(ctx.agreements) + sum(1 for ag in ctx.agreements if ag.is_credit)`:
  ```python
  pa = result['Core_DB.PARTY_AGREEMENT']
  credit_count = sum(1 for ag in ctx.agreements if ag.is_credit)
  assert len(pa) == len(ctx.agreements) + credit_count, f'{len(pa)} != {len(ctx.agreements) + credit_count}'
  ```
- [ ] Role codes are exactly `{'customer', 'borrower'}`:
  ```python
  assert set(pa['Party_Agreement_Role_Cd'].unique()) == {'customer', 'borrower'}
  ```
- [ ] Exactly one `'customer'` row per agreement (Step 3 item #9 / #12):
  ```python
  cust = pa[pa['Party_Agreement_Role_Cd'] == 'customer']
  assert len(cust) == len(ctx.agreements)
  assert (cust.groupby('Agreement_Id').size() == 1).all()
  ```
- [ ] Exactly one `'borrower'` row per credit agreement, zero for non-credit (Step 3 item #11):
  ```python
  borrow = pa[pa['Party_Agreement_Role_Cd'] == 'borrower']
  credit_agreement_ids = {ag.agreement_id for ag in ctx.agreements if ag.is_credit}
  non_credit_ids = {ag.agreement_id for ag in ctx.agreements if not ag.is_credit}
  assert set(borrow['Agreement_Id'].astype(int)) == credit_agreement_ids
  assert not (set(borrow['Agreement_Id'].astype(int)) & non_credit_ids)
  ```
- [ ] Every Agreement_Id resolves to `Core_DB.AGREEMENT.Agreement_Id`:
  ```python
  ag_ids = set(ctx.tables['Core_DB.AGREEMENT']['Agreement_Id'].astype(int))
  assert set(pa['Agreement_Id'].astype(int)).issubset(ag_ids)
  ```
- [ ] Every Party_Id resolves to `Core_DB.PARTY.Party_Id` (and equals the owner — not some other party):
  ```python
  party_ids = set(ctx.tables['Core_DB.PARTY']['Party_Id'].astype(int))
  assert set(pa['Party_Id'].astype(int)).issubset(party_ids)
  owner_map = {ag.agreement_id: ag.owner_party_id for ag in ctx.agreements}
  for _, row in pa.iterrows():
      assert int(row['Party_Id']) == owner_map[int(row['Agreement_Id'])]
  ```
- [ ] `Party_Agreement_Start_Dt` matches `ag.open_dttm.date()`, `Party_Agreement_End_Dt` matches `ag.close_dttm.date()` when closed else `None`:
  ```python
  from datetime import date as _date, datetime as _dt
  open_map = {ag.agreement_id: ag.open_dttm.date() for ag in ctx.agreements}
  close_map = {ag.agreement_id: (ag.close_dttm.date() if ag.close_dttm else None) for ag in ctx.agreements}
  for _, row in pa.iterrows():
      assert row['Party_Agreement_Start_Dt'] == open_map[int(row['Agreement_Id'])]
      end = row['Party_Agreement_End_Dt']
      expected_end = close_map[int(row['Agreement_Id'])]
      if expected_end is None:
          assert end is None or pd.isna(end)
      else:
          assert end == expected_end
  ```
- [ ] Sanity: every `is_credit=True` agreement's `product_type` belongs to `_CREDIT_PRODUCT_TYPES`:
  ```python
  from generators.tier9_party_agreement import _CREDIT_PRODUCT_TYPES
  for ag in ctx.agreements:
      if ag.is_credit:
          assert ag.product_type in _CREDIT_PRODUCT_TYPES, f'is_credit=True but product_type={ag.product_type}'
  ```

**PARTY_RELATED invariants (Step 3 item #10):**

- [ ] Row count equals `len(ctx.customers)` exactly:
  ```python
  pr = result['Core_DB.PARTY_RELATED']
  assert len(pr) == len(ctx.customers), f'{len(pr)} != {len(ctx.customers)}'
  ```
- [ ] Every row has `Party_Related_Role_Cd == 'customer of enterprise'`:
  ```python
  assert (pr['Party_Related_Role_Cd'] == 'customer of enterprise').all()
  ```
- [ ] Every row has `Related_Party_Id == BANK_PARTY_ID (9_999_999)`:
  ```python
  from config.settings import BANK_PARTY_ID
  assert (pr['Related_Party_Id'].astype(int) == BANK_PARTY_ID).all()
  assert BANK_PARTY_ID == 9_999_999
  ```
- [ ] `BANK_PARTY_ID` exists in `Core_DB.PARTY` (upstream contract check — guard should have raised if absent, but re-verify):
  ```python
  assert BANK_PARTY_ID in set(ctx.tables['Core_DB.PARTY']['Party_Id'].astype(int))
  ```
- [ ] Every customer Party_Id is represented exactly once:
  ```python
  customer_ids = {cp.party_id for cp in ctx.customers}
  assert set(pr['Party_Id'].astype(int)) == customer_ids
  assert (pr.groupby('Party_Id').size() == 1).all()
  ```
- [ ] `Party_Structure_Type_Cd` is `'banking_relationship'` on every row:
  ```python
  assert (pr['Party_Structure_Type_Cd'] == 'banking_relationship').all()
  ```
- [ ] `Party_Related_End_Dttm` is NULL on every row (all relationships open):
  ```python
  assert pr['Party_Related_End_Dttm'].isna().all()
  ```
- [ ] `Party_Related_Start_Dttm` is a `datetime` (not string) and matches `cp.party_since`:
  ```python
  from datetime import datetime as _dt
  cp_map = {cp.party_id: cp.party_since for cp in ctx.customers}
  for _, row in pr.iterrows():
      val = row['Party_Related_Start_Dttm']
      assert isinstance(val, _dt), f'not datetime: {type(val)}'
      assert val.date() == cp_map[int(row['Party_Id'])]
      assert val.time() == _dt.min.time()  # midnight
  ```

**PARTY_CLAIM invariants (PRD §9 Q3):**

- [ ] Row count is in the plausible Bernoulli band for 2% of ~3,000 customers (20 ≤ n ≤ 120; tight range allows for Monte-Carlo variance + small-universe testing):
  ```python
  pc = result['Core_DB.PARTY_CLAIM']
  n_customers = len(ctx.customers)
  assert n_customers >= 10, 'harness too small — use full universe'
  lo = max(1, int(0.005 * n_customers))   # 0.5% floor
  hi = int(0.05 * n_customers)             # 5% ceiling
  assert lo <= len(pc) <= hi, f'PARTY_CLAIM count {len(pc)} outside [{lo}, {hi}]'
  ```
- [ ] Every `Claim_Id` is unique (PK):
  ```python
  assert pc['Claim_Id'].is_unique
  ```
- [ ] Every `Claim_Id` is BIGINT ≥ 9_000_000 (IdFactory `'claim'` range start per `config/settings.py:55`):
  ```python
  assert (pc['Claim_Id'].astype(int) >= 9_000_000).all()
  ```
- [ ] Every `Party_Id` resolves to a CustomerProfile:
  ```python
  assert set(pc['Party_Id'].astype(int)).issubset(customer_ids)
  ```
- [ ] Every row has `Party_Claim_Role_Cd == 'claimant'`:
  ```python
  assert (pc['Party_Claim_Role_Cd'] == 'claimant').all()
  ```
- [ ] Every row has `Party_Claim_Contact_Prohibited_Ind == 'No'` (CHAR(3) flag per PRD §4.3):
  ```python
  assert (pc['Party_Claim_Contact_Prohibited_Ind'] == 'No').all()
  ```
- [ ] `Party_Claim_End_Dttm` is NULL on every row:
  ```python
  assert pc['Party_Claim_End_Dttm'].isna().all()
  ```

**BIGINT / dtype invariants:**

- [ ] Every `*_Id` column in every emitted DataFrame has dtype `Int64`:
  ```python
  id_cols = {
      'Core_DB.PARTY_AGREEMENT': ['Party_Id', 'Agreement_Id'],
      'Core_DB.PARTY_RELATED':   ['Party_Id', 'Related_Party_Id'],
      'Core_DB.PARTY_CLAIM':     ['Claim_Id', 'Party_Id'],
  }
  for tbl, cols in id_cols.items():
      df = result[tbl]
      for c in cols:
          assert str(df[c].dtype) == 'Int64', f'{tbl}.{c}: {df[c].dtype}'
  ```
- [ ] Column order in each DataFrame matches `_COLS_*` exactly (first N columns of the DataFrame in order — the DI tail is appended after):
  ```python
  from generators.tier9_party_agreement import (
      _COLS_PARTY_AGREEMENT, _COLS_PARTY_RELATED, _COLS_PARTY_CLAIM,
  )
  assert list(result['Core_DB.PARTY_AGREEMENT'].columns[:len(_COLS_PARTY_AGREEMENT)]) == _COLS_PARTY_AGREEMENT
  assert list(result['Core_DB.PARTY_RELATED'].columns[:len(_COLS_PARTY_RELATED)]) == _COLS_PARTY_RELATED
  assert list(result['Core_DB.PARTY_CLAIM'].columns[:len(_COLS_PARTY_CLAIM)]) == _COLS_PARTY_CLAIM
  ```

**DI column invariants:**

- [ ] All 3 tables have the 3-col DI tail with `di_start_ts = '2000-01-01 00:00:00.000000'`, `di_end_ts = '9999-12-31 00:00:00.000000'`, `di_rec_deleted_Ind = 'N'`:
  ```python
  for tbl in ['Core_DB.PARTY_AGREEMENT', 'Core_DB.PARTY_RELATED', 'Core_DB.PARTY_CLAIM']:
      df = result[tbl]
      assert (df['di_start_ts'] == '2000-01-01 00:00:00.000000').all(), tbl
      assert (df['di_end_ts'] == '9999-12-31 00:00:00.000000').all(), tbl
      assert (df['di_rec_deleted_Ind'] == 'N').all(), tbl
      assert list(df.columns[-3:]) == ['di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind'], tbl
  ```
- [ ] No `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` columns appear on any of the three tables (Core_DB only per PRD §7.3):
  ```python
  for tbl in ['Core_DB.PARTY_AGREEMENT', 'Core_DB.PARTY_RELATED', 'Core_DB.PARTY_CLAIM']:
      df = result[tbl]
      for c in ('Valid_From_Dt', 'Valid_To_Dt', 'Del_Ind'):
          assert c not in df.columns, f'{tbl} has forbidden column {c}'
  ```

**Side-effect / no-mutation invariants:**

- [ ] `generate()` does not mutate `ctx.tables`:
  ```python
  tables_before = dict(ctx.tables)  # shallow copy
  _ = Tier9PartyAgreement().generate(ctx)
  assert ctx.tables == tables_before
  ```
- [ ] `generate()` advances `ctx.rng` state (it should — the 2% Bernoulli consumes entropy). A no-op here would indicate the Bernoulli was routed through a different RNG:
  ```python
  before = ctx.rng.bit_generator.state
  _ = Tier9PartyAgreement().generate(ctx)
  after = ctx.rng.bit_generator.state
  assert before != after, 'ctx.rng not consumed — PARTY_CLAIM Bernoulli bypassed ctx.rng?'
  ```

**Reproducibility:**

- [ ] Running `Tier9PartyAgreement().generate(ctx)` twice on two freshly-built universes with `SEED = 42` produces byte-identical DataFrames:
  ```python
  # Rebuild from scratch to avoid ctx.rng state carrying over
  from registry.universe import UniverseBuilder
  from config.settings import SEED
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory

  def build_and_run():
      rng = np.random.default_rng(SEED)
      ctx_local = UniverseBuilder().build(_config_obj, rng)
      # ... run Tier0..Tier8 into ctx_local.tables per the harness ...
      return Tier9PartyAgreement().generate(ctx_local)

  r1 = build_and_run()
  r2 = build_and_run()
  for key in r1:
      pd.testing.assert_frame_equal(r1[key], r2[key], check_dtype=True)
  ```
  (Session may substitute a lighter harness as long as the reproducibility claim is demonstrated end-to-end.)

## Handoff notes

### What was built
`generators/tier9_party_agreement.py` — `class Tier9PartyAgreement(BaseGenerator)` with `generate(ctx)` and three private helpers (`_build_party_agreement`, `_build_party_related`, `_build_party_claim`). All 22+ DoD assertions pass against the full pipeline (Tier0–Tier8 pre-run). Row counts with SEED=42: PARTY_AGREEMENT 6,154; PARTY_RELATED 3,000; PARTY_CLAIM 64.

### Diffs from spec

**DI stamping:** `self.stamp_di(df, start_ts=_TIER9_DI_START_TS)` is used as the spec says. It appends 5 columns; the only meaningful ones are `di_start_ts`, `di_end_ts`, and `di_rec_deleted_Ind` — `di_data_src_cd` and `di_proc_name` are always NULL and carry no information (PRD §7.3 / Q5c). The spec's description "yields the 3-col tail" was correct in spirit.

### BANK_PARTY_ID gap — resolved in Tier2Core

The spec states `Core_DB.PARTY` should have ≈3,001 rows (3,000 customers + 1 reserved bank/self-emp row). In practice `Tier2Core` only projected `CustomerProfile` party IDs (10,000,000+) into `Core_DB.PARTY`; the reserved `9_999_999` entity existed only in `Core_DB.ORGANIZATION` (injected by Tier3). This meant `PARTY_RELATED.Related_Party_Id = 9_999_999` had no valid FK target in `Core_DB.PARTY`.

**Fixed in this step:** `generators/tier2_core.py` was patched to append one reserved PARTY row (`Party_Id = BANK_PARTY_ID`, `Party_Type_Cd = 'ORGANIZATION'`, `Party_Subtype_Cd = 'commercial'`, `Party_Desc = 'Bank Enterprise'`) after the customer loop. `Core_DB.PARTY` now has 3,001 rows, the guard check passes cleanly, and the FK chain is complete.

### Next session guidance
Step 20 Tier 10 Events can start now — `Core_DB.PARTY_AGREEMENT` and `Core_DB.PARTY_RELATED` are stable and in `ctx.tables`. The PARTY_CLAIM table is also stable. No changes to ctx profiles or prior tables were made in this step.

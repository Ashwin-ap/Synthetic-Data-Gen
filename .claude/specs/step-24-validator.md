# Spec: Step 24 — Validator (22-point Layer 2 constraint check)

## Overview

This step adds the **Phase 3 hard gate** that sits between tier generation (Phase 2) and CSV writing (Phase 4) per `mvp-tool-design.md` §15 orchestration. The `Validator` scans `ctx.tables` (every Core_DB / CDM_DB / PIM_DB DataFrame built by Steps 8–23) and reports every violation of the 22 Layer 2 transformation-readiness constraints enumerated in `mvp-tool-design.md` §12 plus inter-table FK integrity checks. On any failure the orchestrator (Step 25) will halt and `sys.exit(1)` — silent FK violations or a missing literal-match row (e.g. the `FROZEN` / `Frozen Status` / `'Frozen'` seed row) produce CSVs that look plausible but break Layer 2 transforms two sprints later (`mvp-tool-design.md` §14 Decision 6). This step is pure read-only analysis: no DataFrame is mutated, no CSV is touched. The validator returns a `List[str]`; an empty list means every constraint passed.

## Depends on

All of Steps 8–23 must be implemented and their tier generators callable, because the validator consumes every table they produce. Concretely:

- **Step 1** — `config/settings.py` (`BANK_PARTY_ID = 9_999_999`, `SELF_EMP_ORG_ID = 9_999_999`, `SIM_DATE`, `HIGH_DATE`, `HIGH_TS`, `SKIPPED_TABLES`).
- **Step 3** — `registry/context.GenerationContext` (the validator reads `ctx.tables`, `ctx.customers`, `ctx.agreements`).
- **Step 4** — `UniverseBuilder.build(config, rng)` returning a `GenerationContext`.
- **Step 8** — Tier 0 seeds (checks #2 lookup-desc coverage, #13 FROZEN row, #21 'Frozen' desc match).
- **Step 9** — Tier 1 (check #19 ISO_3166_COUNTRY_SUBDIVISION_STANDARD populated).
- **Step 10** — Tier 2 Core (checks #17/#18 require seeded ANALYTICAL_MODEL rows).
- **Step 11** — Tier 3 (INDIVIDUAL, ORGANIZATION registries for FK checks).
- **Step 12** — Tier 4a (check #3 INDIVIDUAL_NAME, #22 PARTY_IDENTIFICATION).
- **Step 13** — Tier 4b (check #14 ORGANIZATION NAICS/SIC/GICS primary indicator).
- **Step 14** — Tier 4c (checks #4 PARTY_LANGUAGE_USAGE, #5 PARTY_STATUS, #18 PARTY_SCORE).
- **Step 15** — Tier 5/6 (FK integrity for ADDRESS, STREET_ADDRESS, PARTY_LOCATOR).
- **Step 16** — Tier 7a (checks #1 all-6-schemes, #6 Rate Feature, #8 preferred currency, #13 FROZEN code, #17 AGREEMENT_SCORE profitability).
- **Step 17** — Tier 7b (exclusive sub-typing; cross-table FK checks for FINANCIAL/DEPOSIT/CREDIT/LOAN/MORTGAGE/CREDIT_CARD).
- **Step 18** — Tier 8 (check #7 AGREEMENT_PRODUCT 'primary' role).
- **Step 19** — Tier 9 (checks #9 customer, #10 customer of enterprise, #11 borrower, #12 retail-customer).
- **Step 20** — Tier 10 (FK integrity for EVENT, FINANCIAL_EVENT, COMPLAINT_EVENT).
- **Step 21** — Tier 11/13 (checks #15 CAMPAIGN_STATUS ≥1, #16 PROMOTION_OFFER ≤5).
- **Step 22** — Tier 14 (cross-schema Core_DB↔CDM_DB FK checks; PARTY_INTERRACTION_EVENT typo intact).
- **Step 23** — Tier 15 (check #20 PIM CLV 8-group hierarchy).

No code in any prior step is modified — the validator is a pure downstream consumer.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to:**
- `PRD.md` §5 (Core Design Principles — correctness-over-completeness, validator as hard gate), §7.1 (BIGINT), §7.10 (typo preserved), §7.11 (literal-match seed rows the validator must verify)
- `mvp-tool-design.md` §12 **Layer 2 Transformation-Readiness Checklist** — the authoritative table of 22 constraints this step must implement. Each row names the constraint, the expected invariant, and the tier that enforces it.
- `mvp-tool-design.md` §14 Decision 6 (validator is a hard gate before CSV write), §15 orchestration loop (how `main.py` calls `Validator().check_all(ctx)` and `sys.exit(1)` on non-empty return).
- `implementation-steps.md` Step 24 exit criteria (running on a complete ctx returns `[]`; deliberately corrupting a row produces a targeted error).

**Additional reference files** (named in the step's "Reads from" line — plus the DDL verification rule in `CLAUDE.md`):
- `references/02_data-mapping-reference.md` **Step 3** — the source list of 22 Layer 2 prerequisites. Cross-reference each `Validator._check_<name>` method against the item number in this file so drift is traceable. Do not read other sections of `02`.
- `references/07_mvp-schema-reference.md` — consult on demand to confirm column names and composite PKs for the tables being checked. The validator must use actual DDL column names (e.g. `Agreement_Status_Scheme_Cd`, `Agreement_Status_Cd`, `Individual_Name_Start_Dt`). Do not trust spec prose if it conflicts with DDL (CLAUDE.md DDL verification rule).
- `references/05_architect-qa.md` — consult only for the PIM recursive-root rule (Q3) when implementing check #20.

## Produces

### New module

- `output/validator.py` — the `Validator` class and a `__main__` self-test block. Contents:

  | Symbol | Purpose |
  |--------|---------|
  | `class Validator` | Public entry point; `check_all(ctx) -> List[str]` |
  | `_check_01_agreement_status_6_schemes` | Constraint #1 |
  | `_check_02_lookup_desc_populated` | Constraint #2 |
  | `_check_03_individual_name_sim_date_window` | Constraint #3 |
  | `_check_04_party_language_usage_two_rows` | Constraint #4 |
  | `_check_05_party_status_at_least_one` | Constraint #5 |
  | `_check_06_agreement_feature_rate_for_loans` | Constraint #6 |
  | `_check_07_agreement_product_primary_role` | Constraint #7 |
  | `_check_08_agreement_currency_preferred` | Constraint #8 |
  | `_check_09_party_agreement_customer_role` | Constraint #9 |
  | `_check_10_party_related_customer_of_enterprise` | Constraint #10 |
  | `_check_11_party_agreement_borrower_for_loans` | Constraint #11 |
  | `_check_12_party_agreement_customer_for_retail` | Constraint #12 |
  | `_check_13_frozen_status_code_FROZEN` | Constraint #13 |
  | `_check_14_organization_primary_naics_sic_gics` | Constraint #14 |
  | `_check_15_campaign_status_at_least_one` | Constraint #15 |
  | `_check_16_promotion_offer_at_most_five` | Constraint #16 |
  | `_check_17_agreement_score_profitability` | Constraint #17 |
  | `_check_18_party_score_customer_profitability` | Constraint #18 |
  | `_check_19_iso_3166_country_subdivision_populated` | Constraint #19 |
  | `_check_20_pim_product_group_clv_hierarchy` | Constraint #20 |
  | `_check_21_frozen_status_desc_exact_match` | Constraint #21 |
  | `_check_22_party_identification_ssn_passport_dl` | Constraint #22 |
  | `_check_fk_integrity` | Dedicated FK-resolution scan across ~20 known cross-table references |
  | `__main__` block | Runs a minimal smoke test: build a tiny `ctx` via `UniverseBuilder` + all tiers, assert `check_all() == []`; then corrupt one table and assert it returns a non-empty list mentioning the affected constraint. |

  Each `_check_XX_*` method:
  - Takes `ctx` only (never mutates).
  - Returns `List[str]` — empty if constraint passes, else one or more strings describing each violation with the triggering `Agreement_Id` / `Party_Id` / row pointer (not a count alone — first ~5 offenders at minimum).
  - Has a top-line docstring quoting the `mvp-tool-design.md` §12 row and the `references/02_data-mapping-reference.md` Step 3 item number.

## Tables generated

No tables generated in this step. The validator is read-only: `check_all(ctx)` inspects `ctx.tables` and returns violation strings. No entry is added to, removed from, or modified within `ctx.tables`.

## Files to modify

No files modified. In particular, do **not** edit `main.py` — the orchestrator wiring is Step 25's responsibility. The validator must be importable and callable as `from output.validator import Validator; Validator().check_all(ctx)` but is not yet hooked into the `main.py` pipeline by this step.

If a violation uncovers a real bug in a prior tier's generator (not just a wrong assumption in the spec), **stop and escalate via Handoff Protocol §2** — do not silently patch the upstream generator from inside this step's session.

## New dependencies

No new dependencies. Uses only `pandas`, `typing` stdlib, and existing project modules.

## Rules for implementation

**Universal rules (every step):**

- BIGINT for all ID columns (per PRD §7.1) — the validator must not cast any `*_Id` column to Python `int` in a way that loses precision on 64-bit values. Use `pandas.Int64` comparisons via `.astype('Int64')` where needed; prefer set-membership on the raw values.
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — the FK integrity check must recognise that a `Core_DB` row's `Party_Id` resolves against `CDM_DB.PARTY.CDM_Party_Id` when the Core_DB PARTY dataframe is conceptual-only. Do **not** flag cross-schema party FKs as unresolved.
- DI column stamping on every table via `BaseGenerator.stamp_di()` — n/a; validator produces no DataFrames.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records — n/a; no stamping in this step. The validator may **read** these sentinels to identify "current" rows where a check needs to scope itself (e.g. constraint #1 counts only the 6 **current** status rows per agreement; delinquency history rows with non-NULL `Agreement_Status_End_Dttm` are permitted additions, not violations).
- `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` stamped additionally on CDM_DB and PIM_DB tables (per PRD §7.3) — the validator must not require these columns on Core_DB tables and must not flag their presence on CDM_DB/PIM_DB as unexpected.
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` — n/a; writer concern, not validator concern. The validator is column-order agnostic (accesses columns by name).
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — the validator's FK integrity scan, if it references this table, must use the double-R key `CDM_DB.PARTY_INTERRACTION_EVENT`. Any assertion or error string that mentions the table uses the typo spelling.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — the validator must tolerate `ctx.tables` not containing `Core_DB.GEOSPATIAL`. It must not produce a spurious "missing table" violation for keys in `SKIPPED_TABLES`.
- No ORMs, no database connections — pure pandas.
- Reproducibility: the validator itself uses no RNG. Its `__main__` self-test builds a `ctx` with `SEED=42`; running twice must return byte-identical `List[str]` output.

**Step-specific rules:**

- **Return strings, never raise.** Every `_check_XX_*` method returns `List[str]`. The top-level `check_all()` concatenates them. Raising would halt the first constraint and hide later violations; the contract is that `check_all()` surfaces **every** violation in one pass so the user sees the full picture before re-running.
- **Violation strings are specific and actionable.** Every string must include: (a) the constraint number and short name, (b) the table or table pair involved, (c) a row pointer (Agreement_Id, Party_Id, row index), and (d) the expected-vs-actual value when relevant. Example good: `"[#8 AGREEMENT_CURRENCY preferred] Agreement_Id=100342 has 0 rows with Currency_Use_Cd='preferred' (expected ≥1)"`. Example bad: `"AGREEMENT_CURRENCY violation"`.
- **Cap at 5–10 offenders per check.** For each constraint, report the first ~5 violating rows individually, then a summary line if more exist (e.g. `"... and 342 more"`). Do not spam thousands of lines for a single broken tier — it obscures other constraint failures and slows operator review.
- **Reference `mvp-tool-design.md` §12 line numbers in docstrings.** Each `_check_XX_*` docstring opens with the verbatim `§12` table row (e.g. `"""#1 — AGREEMENT_STATUS has all 6 scheme types per agreement. Tier 7a enforces; §12 row 1; 02-map-ref Step 3 item #1."""`). This makes a drift audit trivial.
- **Constraint #1 — use the 6-scheme set from `mvp-tool-design.md` §9 Tier 7 verbatim:** `{'Account Status', 'Accrual Status', 'Default Status', 'Drawn Undrawn Status', 'Frozen Status', 'Past Due Status'}`. Check only current rows (where `Agreement_Status_End_Dttm` is NULL). Historical 'Past Due Status' rows for delinquent agreements are allowed; the constraint is that each of the 6 schemes has **at least one current row** per agreement.
- **Constraint #2 — every `*_TYPE` / `*_SUBTYPE` / `*_CLASSIFICATION` lookup table has its `*_Desc` column populated for every row.** Do not try to validate FK-to-desc joins per consumer table — the universal property is that no seed row has a NULL desc. Skip any `*_Desc` column that is not in the DDL for a particular lookup.
- **Constraint #3 — `INDIVIDUAL_NAME.Individual_Name_Start_Dt <= SIM_DATE <= Individual_Name_End_Dt`.** Use `pd.to_datetime` for comparison; `HIGH_DATE` sentinel compares greater than any real date, so `End_Dt = '9999-12-31'` satisfies the upper bound by construction.
- **Constraints #4 / #10 — literal code strings.** Constraint #4 requires exactly the strings `'primary spoken language'` and `'primary written language'` in `Language_Usage_Type_Cd`. Constraint #10 requires `'customer of enterprise'` in `Party_Related_Role_Cd`. Hardcode these strings — they are the Layer 2 match values (PRD §7.11 literal-match rows) and must not drift.
- **Constraint #13 + #21 — both scan `AGREEMENT_STATUS_TYPE` for the `FROZEN` seed row.** #13 checks that a row with `Agreement_Status_Scheme_Cd='Frozen Status'` and `Agreement_Status_Cd='FROZEN'` exists. #21 additionally asserts that row's `Agreement_Status_Desc` is exactly the string `'Frozen'` (case-sensitive). Layer 2's ACCOUNT_STATUS_DIMENSION uses the desc for a literal match.
- **Constraint #14 — exactly one primary indicator per org per industry standard.** For each `Organization_Party_Id` that appears in `ORGANIZATION_NAICS`, there must be exactly one row with `Primary_NAICS_Ind='Yes'`. Same for `Primary_SIC_Ind` in `ORGANIZATION_SIC` and `Primary_GICS_Ind` in `ORGANIZATION_GICS`. Organizations with zero rows in a given standard are allowed (industry standard coverage is not universal); the constraint is "zero-or-one `'Yes'`, never two".
- **Constraint #16 — up to 5 offers per promotion, fewer is acceptable.** The rule is `≤ 5`, not `== 5`. Do not flag promotions with 1–4 offers as violations.
- **Constraint #20 — the CLV hierarchy is exactly 8 children.** Assert `PIM_DB.PRODUCT_GROUP` has exactly one row with `Product_Group_Type_Cd == 1` (root) whose `Parent_Group_Id == Product_Group_Id` (self-ref, per `05_architect-qa.md` Q3), and exactly 8 rows with `Product_Group_Type_Cd == 2` (CLV child) whose `Parent_Group_Id == <root Id>`. Do not verify the 8 group names — they are hand-coded in Step 23's generator and already asserted there; this check verifies only the structural hierarchy.
- **Constraint #22 — `PARTY_IDENTIFICATION` all three types per individual.** Every individual party must have **all three** of `Party_Identification_Type_Cd` ∈ `{'SSN', "Driver's License", 'Passport'}` present. This matches Step 14's generator contract (`_ID_TYPES_INDIVIDUAL = ('SSN', "Driver's License", 'Passport')`, Step 14 spec line 85) and its exit criterion ("PARTY_IDENTIFICATION has exactly 3 rows per individual; each individual has all 3 required types", Step 14 spec line 374). The three type strings **are** Layer 2 literal-match values — ACCOUNT/CUSTOMER pivots depend on all three being present per individual — so hardcode them here exactly (case-sensitive, apostrophe in `Driver's License` literal). Violation reports name the missing type(s) per offending `Party_Id`. Non-individual parties (`ORGANIZATION`) must not appear in `PARTY_IDENTIFICATION`; flag any that do.
- **FK integrity scan — use a data-driven manifest.** Define a module-level `_FK_MANIFEST: List[Tuple[str, str, str, str]]` of `(child_table, child_col, parent_table, parent_col)` tuples for the ~20 highest-value cross-table FKs (every `Agreement_Id` parent/child, every `Party_Id` parent/child including the Core_DB↔CDM_DB shared-ID case, `Event_Id`, `Product_Id`, `Address_Id`, `Locator_Id`, `Campaign_Id`, `Promotion_Id`). For each, assert `set(child[col]) - {NULL} ⊆ set(parent[col])`. Report orphans per `child_table.child_col` capped at 5 examples. Do not attempt a full column-by-column FK scan — lookup-to-consumer joins (e.g. `Currency_Cd → CURRENCY.Currency_Cd`) are covered by constraint #2 and are not in the manifest.
- **Handle optional tables defensively.** If a `ctx.tables` key is missing (e.g. the test harness built only Tiers 0–5), every constraint that depends on that table emits a single violation string `"[#N check_name] required table <key> missing from ctx.tables"` and moves on. Do not `KeyError`.
- **No mutation.** Every `_check_XX_*` method reads `ctx.tables[key]` directly; never `.drop`, never `.assign` in-place. Treat all DataFrames as immutable snapshots.
- **`__main__` smoke test must not invoke `main.py`.** Build the context inline: `UniverseBuilder().build(...)`, then call each `TierN...().generate(ctx); ctx.tables.update(...)` in order, then `Validator().check_all(ctx)`. This keeps Step 24 independent of Step 25's orchestrator wiring.

## Definition of done

Tick every box before the session ends, or mark as `n/a` with a one-line justification.

**Source-of-truth & scaffolding:**

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else
- [ ] `python -c "import output.validator"` exits 0
- [ ] `python -c "from output.validator import Validator; v = Validator(); assert callable(v.check_all)"` exits 0
- [ ] Every one of the 22 constraint checks is a separately-named method:
      ```python
      import output.validator as v
      methods = [m for m in dir(v.Validator) if m.startswith('_check_') and any(m.startswith(f'_check_{n:02d}_') for n in range(1, 23))]
      assert len(methods) == 22, f'expected 22 numbered checks, got {len(methods)}: {methods}'
      ```
- [ ] FK integrity check exists as a distinct method: `assert hasattr(v.Validator, '_check_fk_integrity')`
- [ ] Docstring on every `_check_XX_*` method cites the `§12` row and the `02` Step 3 item number:
      ```python
      from output.validator import Validator
      import inspect
      for name, fn in inspect.getmembers(Validator, predicate=inspect.isfunction):
          if not name.startswith('_check_') or name == '_check_fk_integrity':
              continue
          doc = (fn.__doc__ or '').lower()
          assert '§12' in (fn.__doc__ or '') and 'step 3 item' in doc, f'{name} missing §12 / Step 3 citation'
      ```

**Happy-path: a fully-built ctx passes:**

- [ ] On a context built end-to-end with `SEED=42` through all tiers 0–15, `Validator().check_all(ctx)` returns `[]`. Concretely, the `__main__` block of `output/validator.py` must execute this and assert on it:
      ```python
      # in output/validator.py __main__
      ctx = build_full_ctx_seed_42()
      errors = Validator().check_all(ctx)
      assert errors == [], f'Expected no errors; got {len(errors)}:\n' + '\n'.join(errors[:10])
      ```

**Sad-path: corrupting a row produces a targeted violation:**

- [ ] Deliberately removing every `'preferred'` row from `ctx.tables['Core_DB.AGREEMENT_CURRENCY']` causes `check_all()` to return a non-empty list whose first relevant string mentions constraint **#8** and the table name:
      ```python
      ctx2 = deepcopy_ctx(ctx)
      df = ctx2.tables['Core_DB.AGREEMENT_CURRENCY']
      ctx2.tables['Core_DB.AGREEMENT_CURRENCY'] = df[df['Currency_Use_Cd'] != 'preferred']
      errors = Validator().check_all(ctx2)
      assert any('#8' in e and 'AGREEMENT_CURRENCY' in e for e in errors), errors
      ```
- [ ] Deliberately deleting the `FROZEN` seed row from `ctx.tables['Core_DB.AGREEMENT_STATUS_TYPE']` causes `check_all()` to return both a #13 and a #21 violation in the same pass:
      ```python
      ctx3 = deepcopy_ctx(ctx)
      df = ctx3.tables['Core_DB.AGREEMENT_STATUS_TYPE']
      ctx3.tables['Core_DB.AGREEMENT_STATUS_TYPE'] = df[df['Agreement_Status_Cd'] != 'FROZEN']
      errors = Validator().check_all(ctx3)
      assert any('#13' in e for e in errors), errors
      assert any('#21' in e for e in errors), errors
      ```
- [ ] Deliberately dropping all rows for one `Party_Id` from `ctx.tables['Core_DB.PARTY_LANGUAGE_USAGE']` produces a #4 violation naming that `Party_Id`:
      ```python
      ctx4 = deepcopy_ctx(ctx)
      df = ctx4.tables['Core_DB.PARTY_LANGUAGE_USAGE']
      victim = int(df['Party_Id'].iloc[0])
      ctx4.tables['Core_DB.PARTY_LANGUAGE_USAGE'] = df[df['Party_Id'] != victim]
      errors = Validator().check_all(ctx4)
      assert any('#4' in e and str(victim) in e for e in errors), errors
      ```
- [ ] Deliberately removing every `Passport` row from `PARTY_IDENTIFICATION` (an individual now has SSN + DL but no Passport — the exact failure mode the "≥1 row" rule would miss) produces a #22 violation naming the missing type:
      ```python
      ctx4b = deepcopy_ctx(ctx)
      df = ctx4b.tables['Core_DB.PARTY_IDENTIFICATION']
      ctx4b.tables['Core_DB.PARTY_IDENTIFICATION'] = df[df['Party_Identification_Type_Cd'] != 'Passport']
      errors = Validator().check_all(ctx4b)
      assert any('#22' in e and 'Passport' in e for e in errors), errors
      ```

**Violation-string quality:**

- [ ] No violation string is longer than 400 characters (readability).
- [ ] Every violation string contains at least one of: `#N` (constraint number), an ID value, or a table name — no bare `"violation"` stubs:
      ```python
      # given errors from a deliberately-corrupted ctx
      for e in errors:
          assert any(tok in e for tok in ('#', 'Id=', 'DB.')), f'unhelpful error: {e}'
      ```
- [ ] Per-check cap honoured: no single check emits more than 10 strings even when corrupting thousands of rows:
      ```python
      ctx5 = deepcopy_ctx(ctx)
      ctx5.tables['Core_DB.AGREEMENT_CURRENCY'] = ctx5.tables['Core_DB.AGREEMENT_CURRENCY'].iloc[0:0]
      errors = Validator().check_all(ctx5)
      check8 = [e for e in errors if '#8' in e]
      assert len(check8) <= 10, f'#8 emitted {len(check8)} strings (cap is 10)'
      ```

**FK integrity:**

- [ ] `_check_fk_integrity` runs in isolation on a valid ctx and returns `[]`:
      ```python
      assert Validator()._check_fk_integrity(ctx) == []
      ```
- [ ] The FK manifest covers (at minimum) every cross-table reference listed in the `_FK_MANIFEST` constant and the manifest has ≥ 15 entries:
      ```python
      from output.validator import _FK_MANIFEST
      assert len(_FK_MANIFEST) >= 15
      # smoke-check shape: each entry is a 4-tuple of strings
      for entry in _FK_MANIFEST:
          assert len(entry) == 4 and all(isinstance(x, str) for x in entry)
      ```
- [ ] Inserting an Agreement_Id into `PARTY_AGREEMENT` that does not exist in `AGREEMENT` is detected:
      ```python
      ctx6 = deepcopy_ctx(ctx)
      df = ctx6.tables['Core_DB.PARTY_AGREEMENT'].copy()
      df.loc[len(df)] = df.iloc[0].copy()
      df.loc[len(df) - 1, 'Agreement_Id'] = 999_999_999_999  # unlikely BIGINT
      ctx6.tables['Core_DB.PARTY_AGREEMENT'] = df
      errors = Validator().check_all(ctx6)
      assert any('PARTY_AGREEMENT' in e and 'Agreement_Id' in e for e in errors), errors
      ```

**Reproducibility & tolerance:**

- [ ] Running `check_all(ctx)` twice on the same context returns byte-identical string lists (order stable):
      ```python
      a = Validator().check_all(ctx)
      b = Validator().check_all(ctx)
      assert a == b
      ```
- [ ] Missing a `SKIPPED_TABLES` entry from `ctx.tables` does NOT produce a violation:
      ```python
      from config.settings import SKIPPED_TABLES
      for k in SKIPPED_TABLES:
          assert k not in ctx.tables  # skipped tables were never added by any tier
      assert Validator().check_all(ctx) == []
      ```
- [ ] Dropping a non-SKIPPED table that the validator needs produces a clear "missing table" violation rather than a `KeyError`:
      ```python
      ctx7 = deepcopy_ctx(ctx)
      del ctx7.tables['Core_DB.AGREEMENT_CURRENCY']
      errors = Validator().check_all(ctx7)
      assert any('AGREEMENT_CURRENCY' in e and 'missing' in e.lower() for e in errors), errors
      ```

**Miscellaneous universal checks:**

- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — n/a; this step writes no CSVs. The upstream tier-0–15 outputs are already BIGINT-compliant from their own steps.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — n/a; this step writes no files. However, any validator error string that mentions this table uses the `INTERRACTION` double-R spelling, confirmed by a spot-grep over the source:
      ```python
      src = open('output/validator.py', encoding='utf-8').read()
      if 'INTERACTION' in src:
          assert 'INTERRACTION' in src, 'single-R spelling appears without the double-R variant somewhere in validator'
      ```
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — n/a; this step writes no files.

**`__main__` self-test:**

- [ ] `python output/validator.py` exits 0 after executing the self-test (happy-path ctx returns `[]`, at least one sad-path mutation triggers the expected violation). The self-test prints one-line progress markers per check, mirroring the `output/writer.py` convention (see `output/writer.py:206` et seq.).

## Handoff notes

_(Leave blank. Fill in at end of implementation session per `implementation-steps.md` Handoff Protocol.)_

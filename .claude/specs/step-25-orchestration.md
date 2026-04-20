# Spec: Step 25 — Orchestrator & End-to-End Smoke Test

## Overview

This is the **terminal step** of the 25-step implementation plan. It replaces the stub `main.py` with a full four-phase orchestrator that composes every artifact built by Steps 1–24: Phase 1 calls `UniverseBuilder.build()` to produce the in-memory `GenerationContext` (~3,000 customers, ~5,000 agreements); Phase 2 runs the 15 tier generators in dependency order (Tier 0 → Tier 15), each mutating `ctx.tables`; Phase 3 runs `Validator().check_all(ctx)` as the hard gate defined in `mvp-tool-design.md` §14 Decision 6 and `sys.exit(1)` on any violation; Phase 4 calls `Writer(OUTPUT_DIR).write_all(ctx.tables)` to serialise every DataFrame to CSV under `output/{Core_DB,CDM_DB,PIM_DB}/`. The call sequence is the one prescribed verbatim in `mvp-tool-design.md` §15. The step also produces smoke-test evidence — `python main.py` runs end-to-end with `SEED=42`, the validator returns `[]`, and the output directory contains the expected table counts per schema (implementation-steps.md Step 25 exit criteria). No tier generator, validator method, or writer helper is changed by this step; `main.py` is the only file modified.

## Depends on

All prior steps are consumed as plain imports. In particular:

- **Step 1** — `config.settings` (`SEED`, `TARGET_CUSTOMERS`, `TARGET_AGREEMENTS`, `OUTPUT_DIR`, `CORE_DB_DIR`, `CDM_DB_DIR`, `PIM_DB_DIR`, `SKIPPED_TABLES`).
- **Step 3** — `registry.context.GenerationContext`.
- **Step 4** — `registry.universe.UniverseBuilder` with `.build(config, rng) -> GenerationContext`.
- **Step 5** — `output.writer.Writer` with `.write_all(tables) -> Dict[str, Path]`.
- **Steps 8–23** — every tier generator class (all already stable on `main`). The concrete instantiation list must match the one used in `output/validator.py:895` (`build_full_ctx_seed_42`) so orchestrator and validator self-test stay aligned:
  ```python
  Tier0Lookups(), Tier1Geography(), Tier2Core(),
  Tier3PartySubtypes(), Tier4aIndividual(), Tier4bOrganization(), Tier4cShared(),
  Tier5Location(), Tier6Links(),
  Tier7aAgreementCrosscut(), Tier7bSubtypes(),
  Tier8ProductHierarchy(), Tier9PartyAgreement(), Tier10Events(),
  Tier11CRM(), Tier13Tasks(), Tier14CDM(), Tier15PIM()
  ```
- **Step 24** — `output.validator.Validator` with `.check_all(ctx) -> List[str]`.

No prior step's code is modified. If a smoke-test run surfaces a real bug in an upstream generator (not a wrong assumption in this spec), **stop and escalate via Handoff Protocol §2** — do not silently patch upstream modules from inside this step's session.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to:**
- `PRD.md` §6 (architecture overview — the four-phase pipeline), §7.1 (BIGINT), §7.6 (reproducibility — same seed → identical output), §7.9 (skip GEOSPATIAL), §7.10 (preserve PARTY_INTERRACTION_EVENT typo)
- `mvp-tool-design.md` §2 (two-phase execution), §11 (output format rules — writer's responsibility but the orchestrator must call it), §14 Decision 6 (validator as hard gate before CSV write), §15 `main.py` **Orchestration** — the reference pseudocode this step implements
- `implementation-steps.md` Step 25 (exit criteria) and "Handoff Protocol" §1 (no git from this session) and §5 (partial smoke-test expectation — now becomes a full smoke test at this step)

**Additional reference files**: None. This step writes no seed data, reads no DDL, and does not consult `references/`. The tier generators and validator it composes have already encoded every reference requirement.

## Produces

No new source files. This step only modifies `main.py` and, as a side effect of running the orchestrator at the end of the session, produces the generated CSV tree under `output/`.

### Smoke-test artifacts (generated at exit-criteria verification time)

- `output/Core_DB/*.csv` — ~183 files per `implementation-steps.md` Step 25 exit criteria (Core_DB has 174 DDL-listed tables; the schema reference parser resolves ~183 Core_DB keys including the FSDM extensions + Unresolved-MDM tables mapped into Core_DB per `output/writer.py:203` assertion; `GEOSPATIAL.csv` is absent per PRD §7.9).
- `output/CDM_DB/*.csv` — exactly 16 files. Must include `PARTY_INTERRACTION_EVENT.csv` with the double-R typo spelled correctly (PRD §7.10).
- `output/PIM_DB/*.csv` — exactly 6 files.
- No `output/Core_DB/GEOSPATIAL.csv` (PRD §7.9 / SKIPPED_TABLES).

The `output/` tree is **not** committed. It is gitignored by the repository's existing `.gitignore` (scaffolded in Step 1). Its presence is verified by the Definition-of-done checks; `git status` after verification must still show only `main.py` as modified.

## Tables generated

No tables generated in this step. The orchestrator only composes existing tier generators — it does not produce DataFrames of its own. Every `Schema.TABLE` entry in `ctx.tables` is written by a tier class that ran in Steps 8–23. The writer then serialises that dict to one CSV per key under `output/<Schema>/<TABLE>.csv`.

## Files to modify

- `main.py` — the current stub (43 lines, all TODO-commented scaffolding as of the Step 24 merge) is replaced with the full four-phase orchestrator wiring. Verify the starting state by reading it first; do not assume the stub shape.

## New dependencies

No new dependencies. Every import (`numpy`, `pandas`, `config.settings`, `registry.universe`, all `generators.tier*` modules, `output.validator`, `output.writer`) is already present in `requirements.txt` from prior steps.

## Rules for implementation

**Universal rules (every step):**

- BIGINT for all ID columns (per PRD §7.1) — n/a at the orchestrator layer; every ID has already been minted as BIGINT by its tier generator. The orchestrator must not cast IDs anywhere.
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — n/a; guaranteed by `UniverseBuilder` + `Tier14CDM`. The orchestrator runs them in order and never rewires IDs.
- DI column stamping on every table via `BaseGenerator.stamp_di()` — n/a; orchestrator produces no DataFrames.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records — n/a; no stamping in this step.
- `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` stamped additionally on CDM_DB and PIM_DB tables (per PRD §7.3) — n/a; tier14/15 already stamp.
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` — **applied by `Writer.write_one()` via `_reorder_to_ddl`**; the orchestrator simply calls `Writer(OUTPUT_DIR).write_all(ctx.tables)` and does not reorder columns itself.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — `Tier14CDM` produces the key `CDM_DB.PARTY_INTERRACTION_EVENT` (double-R) and the writer passes it through unmodified to `output/CDM_DB/PARTY_INTERRACTION_EVENT.csv`. The orchestrator must not normalise, alias, or translate this key anywhere.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — `Writer.write_all` already honours `SKIPPED_TABLES`; the orchestrator just calls it.
- No ORMs, no database connections — pure pandas → CSV.
- Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`. Concretely, `main.main()` must create the `rng` as `np.random.default_rng(SEED)` **once**, pass it to `UniverseBuilder.build(settings, rng)`, and never create a second `rng` inside `main.py`. Every downstream tier/validator/writer reads from the single seeded generator.

**Step-specific rules:**

- **Implement `main.main()` exactly as `mvp-tool-design.md` §15 prescribes**: Phase 1 (`UniverseBuilder().build(settings, rng)`), Phase 2 (iterate tiers, `ctx.tables.update(tier.generate(ctx))`), Phase 3 (`Validator().check_all(ctx)` → if non-empty, print each error and `sys.exit(1)`), Phase 4 (`Writer(OUTPUT_DIR).write_all(ctx.tables)`). Do not invent a new layering.
- **Tier list must match `output/validator.py:895` `build_full_ctx_seed_42`.** Reproduce the same instantiation order. Any divergence (extra tier, skipped tier, reordered tier) will cause the full-ctx validator happy-path to drift from the orchestrator run and is a spec-level bug. Verify by inspection before running: `python -c "from output.validator import ... ; import main"` should not raise.
- **Config object passed to `UniverseBuilder.build` is the `config.settings` module itself.** This is the convention `UniverseBuilder.build(config, rng)` already expects — see `registry/universe.py:98` — so `import config.settings as settings` (or `from config import settings`) and pass `settings`. Do not build a wrapper dataclass; the module has the `SEED`, `TARGET_CUSTOMERS`, `INDIVIDUAL_PCT`, `ID_RANGES`, `HISTORY_START`, `SIM_DATE`, etc. attributes the builder reads.
- **Print progress, don't sprawl.** Every tier emits exactly one line: `"  <TierClassName>: {total_rows:,} rows across {n_tables} tables"`. Format match to the commented template at `main.py:25–27` in the current stub. Don't add per-table sub-bullets; don't add elapsed-time spinners; don't add colour. Keep it greppable plain stdout for CI and diff-against-reference runs.
- **Validator error handling is `sys.exit(1)` after printing every violation.** Do not `raise`. The stub at `main.py:30–34` already shows the pattern — preserve it. Each error prints on its own line prefixed with `"VALIDATION ERROR: "` so failures are greppable.
- **Writer output directory is `OUTPUT_DIR` from `config.settings`**, not a hardcoded path. `Writer.__init__` accepts a `Path | str` default, so `Writer(OUTPUT_DIR).write_all(ctx.tables)` is the canonical call. The orchestrator must not create `OUTPUT_DIR` itself — the writer already does `dest.mkdir(parents=True, exist_ok=True)` per-schema in `write_one` (see `output/writer.py:178`).
- **Guard against duplicate rng creation.** The orchestrator creates `rng = np.random.default_rng(SEED)` once, in `main()`, before Phase 1. No helper, no tier, no post-hoc shim is allowed to reseed. Two `python main.py` runs must produce byte-identical CSVs.
- **No side-effect `print()` calls at import time.** The file guard `if __name__ == '__main__': main()` is the only entry. Imports in `main.py` must not cause a generation run or writer touch.
- **No new top-level functions.** The entire orchestrator is contained in `main() -> None`. Helper functions are only acceptable for the per-tier logging line. If a helper is added, it must be local to `main.py` and private (`_log_tier(...)` style).
- **Tolerate and surface the validator's `__main__` convention.** `output/validator.py` already has a `__main__` block that builds its own ctx and runs a suite of sad-path corruptions (Step 24). The orchestrator must not invoke `validator.py` as a script; it imports `Validator` and calls `check_all(ctx)`. Running `python output/validator.py` independently is Step 24's self-test and is not part of this step's smoke test.
- **The end-of-run success line is deterministic.** On successful completion, print exactly `f"Done. Output in {OUTPUT_DIR}"` (matches the stub at `main.py:38`). Do not embellish — downstream tooling and reproducibility diffs may grep this line.

## Definition of done

Tick every box before the session ends, or mark as `n/a` with a one-line justification.

**Scaffolding & imports:**

- [ ] `git status` shows only `main.py` modified (and possibly the generated `output/` tree, which is gitignored) — nothing else
      ```bash
      git status --porcelain | awk '{print $2}' | grep -v '^output/' | sort
      # should output only: main.py
      ```
- [ ] `python -c "import main"` exits 0 without triggering a generation run
- [ ] `main.py` imports every tier class actually used, plus `UniverseBuilder`, `Validator`, `Writer`, `config.settings`, and `numpy`:
      ```python
      import ast
      src = open('main.py', encoding='utf-8').read()
      tree = ast.parse(src)
      names = {alias.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) for alias in node.names} \
            | {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
      expected = {
          'UniverseBuilder', 'Validator', 'Writer',
          'Tier0Lookups', 'Tier1Geography', 'Tier2Core',
          'Tier3PartySubtypes', 'Tier4aIndividual', 'Tier4bOrganization', 'Tier4cShared',
          'Tier5Location', 'Tier6Links',
          'Tier7aAgreementCrosscut', 'Tier7bSubtypes',
          'Tier8ProductHierarchy', 'Tier9PartyAgreement', 'Tier10Events',
          'Tier11CRM', 'Tier13Tasks', 'Tier14CDM', 'Tier15PIM',
      }
      missing = expected - names
      assert not missing, f'Missing imports in main.py: {missing}'
      ```

**Phase composition:**

- [ ] `main.main()` constructs exactly one `np.random.Generator` (no reseeding anywhere else in the file):
      ```bash
      grep -c 'default_rng' main.py
      # should output: 1
      ```
- [ ] The tier instantiation list inside `main.py` matches the order used by `output/validator.py` `build_full_ctx_seed_42`:
      ```python
      import re
      main_src = open('main.py', encoding='utf-8').read()
      val_src  = open('output/validator.py', encoding='utf-8').read()
      pat = r'Tier\w+\(\)'
      main_tiers = re.findall(pat, main_src)
      val_tiers  = re.findall(pat, val_src)
      # drop any duplicates caused by import lines in main (compare the orchestrator block only)
      # The authoritative order in validator.py is the full list inside build_full_ctx_seed_42.
      # Expected count of tier instantiations appearing inside the orchestrator block: 18
      assert main_tiers[-18:] == val_tiers[-18:], (
          f'Tier order divergence:\n  main: {main_tiers[-18:]}\n  val : {val_tiers[-18:]}'
      )
      ```
- [ ] `Validator` is called and violations cause `sys.exit(1)`:
      ```bash
      grep -n 'Validator()' main.py
      grep -n 'sys.exit' main.py
      # Both greps must return at least one match
      ```
- [ ] `Writer(OUTPUT_DIR).write_all(ctx.tables)` is the final functional call before the `Done.` print:
      ```bash
      grep -n 'Writer' main.py | tail -1
      grep -n 'Done. Output' main.py
      # Both must match; Writer line must appear above the Done line
      ```

**End-to-end smoke test (run from project root):**

- [ ] `rm -rf output/Core_DB output/CDM_DB output/PIM_DB && python main.py` exits 0
      ```bash
      rm -rf output/Core_DB output/CDM_DB output/PIM_DB
      python main.py
      echo "exit=$?"
      # last line must be: exit=0
      ```
- [ ] Per-schema CSV counts match `implementation-steps.md` Step 25 exit criteria:
      ```bash
      core_count=$(ls output/Core_DB/*.csv 2>/dev/null | wc -l)
      cdm_count=$(ls output/CDM_DB/*.csv 2>/dev/null | wc -l)
      pim_count=$(ls output/PIM_DB/*.csv 2>/dev/null | wc -l)
      echo "Core_DB=$core_count  CDM_DB=$cdm_count  PIM_DB=$pim_count"
      # Require: Core_DB between 170 and 195 (spec says ~183; tolerate ±10 to absorb DDL-resolver drift)
      # Require: CDM_DB == 16 exactly
      # Require: PIM_DB == 6 exactly
      [ "$core_count" -ge 170 ] && [ "$core_count" -le 195 ] && [ "$cdm_count" -eq 16 ] && [ "$pim_count" -eq 6 ] && echo OK
      ```
- [ ] Validator returned no violations (captured from stdout):
      ```bash
      python main.py 2>&1 | grep -c 'VALIDATION ERROR:'
      # must output: 0
      ```
- [ ] `output/Core_DB/GEOSPATIAL.csv` does not exist (PRD §7.9 / SKIPPED_TABLES):
      ```bash
      test ! -e output/Core_DB/GEOSPATIAL.csv && echo OK
      ```
- [ ] `output/CDM_DB/PARTY_INTERRACTION_EVENT.csv` exists (double-R typo preserved, PRD §7.10):
      ```bash
      test -s output/CDM_DB/PARTY_INTERRACTION_EVENT.csv && echo OK
      # single-R variant must NOT exist
      test ! -e output/CDM_DB/PARTY_INTERACTION_EVENT.csv && echo OK
      ```

**Row-count spot checks (from `implementation-steps.md` Step 25 exit criteria):**

- [ ] `Core_DB.AGREEMENT.csv` row count matches `TARGET_AGREEMENTS` ±20%:
      ```python
      import pandas as pd
      from config.settings import TARGET_AGREEMENTS
      n = len(pd.read_csv('output/Core_DB/AGREEMENT.csv'))
      assert 0.8 * TARGET_AGREEMENTS <= n <= 1.2 * TARGET_AGREEMENTS, (
          f'AGREEMENT row count {n} outside ±20% of TARGET_AGREEMENTS={TARGET_AGREEMENTS}'
      )
      ```
- [ ] `Core_DB.AGREEMENT_STATUS.csv` has ~6×N_agreements current rows (1 per scheme per agreement) plus the delinquency history rows:
      ```python
      import pandas as pd
      from config.settings import TARGET_AGREEMENTS
      df = pd.read_csv('output/Core_DB/AGREEMENT_STATUS.csv')
      current = df[df['Agreement_Status_End_Dttm'].isna()]
      n_agr = len(pd.read_csv('output/Core_DB/AGREEMENT.csv'))
      expected_current = 6 * n_agr
      # Tolerance ±1% — each agreement must have 6 current schemes (#1 Layer 2 constraint)
      assert abs(len(current) - expected_current) <= max(50, int(0.01 * expected_current)), (
          f'Current AGREEMENT_STATUS rows {len(current)} ≠ expected 6×{n_agr} = {expected_current}'
      )
      ```
- [ ] `Core_DB.PARTY_AGREEMENT.csv` contains at least one `'customer'` role per agreement (#9 Layer 2 constraint — already enforced by Tier9 + Validator, but spot-checked here):
      ```python
      import pandas as pd
      df = pd.read_csv('output/Core_DB/PARTY_AGREEMENT.csv')
      cust = df[df['Party_Agreement_Role_Cd'] == 'customer']
      n_agr = len(pd.read_csv('output/Core_DB/AGREEMENT.csv'))
      assert cust['Agreement_Id'].nunique() == n_agr, (
          f'customer-role coverage: {cust["Agreement_Id"].nunique()}/{n_agr} agreements'
      )
      ```
- [ ] `CDM_DB.PARTY.csv` row count matches Core_DB INDIVIDUAL + ORGANIZATION distinct party IDs (shared-party-ID-space, PRD §7.2):
      ```python
      import pandas as pd
      cdm_party = pd.read_csv('output/CDM_DB/PARTY.csv')
      ind = pd.read_csv('output/Core_DB/INDIVIDUAL.csv')
      org = pd.read_csv('output/Core_DB/ORGANIZATION.csv')
      # CDM_DB.PARTY includes both individuals and organizations (and the BANK_PARTY_ID entity row per Step 24 handoff notes)
      expected_min = ind['Individual_Party_Id'].nunique() + org['Organization_Party_Id'].nunique() - 1  # org 9999999 is the self-emp placeholder
      assert len(cdm_party) >= expected_min, (
          f'CDM_DB.PARTY ({len(cdm_party)}) < INDIVIDUAL+ORGANIZATION ({expected_min})'
      )
      ```
- [ ] `PIM_DB.PRODUCT_GROUP.csv` has exactly 8 CLV child rows (#20 Layer 2 constraint):
      ```python
      import pandas as pd
      df = pd.read_csv('output/PIM_DB/PRODUCT_GROUP.csv')
      clv_children = df[df['Product_Group_Type_Cd'] == 2]
      assert len(clv_children) == 8, f'expected 8 CLV children; got {len(clv_children)}'
      ```

**Reproducibility (Step 25 exit criterion "byte-identical CSVs on two runs"):**

- [ ] Running `python main.py` twice produces byte-identical CSV output across every file in `output/`:
      ```bash
      # run 1 → snapshot hashes
      rm -rf output/Core_DB output/CDM_DB output/PIM_DB
      python main.py >/dev/null 2>&1
      find output/Core_DB output/CDM_DB output/PIM_DB -name '*.csv' -print0 \
        | sort -z | xargs -0 sha256sum > /tmp/run1.sha

      # run 2 → compare
      rm -rf output/Core_DB output/CDM_DB output/PIM_DB
      python main.py >/dev/null 2>&1
      find output/Core_DB output/CDM_DB output/PIM_DB -name '*.csv' -print0 \
        | sort -z | xargs -0 sha256sum > /tmp/run2.sha

      diff /tmp/run1.sha /tmp/run2.sha && echo 'Reproducible OK'
      # diff must be empty; echo must print "Reproducible OK"
      ```

**Validator integration (Step 25 exit criterion "Validator returns no violations"):**

- [ ] On a successful run, the stdout contains zero `VALIDATION ERROR:` lines AND the final line is `"Done. Output in {OUTPUT_DIR}"`:
      ```bash
      out=$(python main.py 2>&1)
      echo "$out" | grep -c 'VALIDATION ERROR:'   # must be 0
      echo "$out" | tail -1 | grep -q 'Done. Output in'  # must succeed
      ```
- [ ] Deliberately corrupting `ctx` (injected only for the purpose of this test — NOT committed) causes the orchestrator to exit non-zero. Smoke-test this by a temporary edit in a throwaway branch or a one-shot stdin patch; revert immediately. Document the outcome in the Handoff notes but do not leave the corruption in `main.py`:
      ```bash
      # Sample technique: use a tmp python -c that monkeypatches Validator.check_all
      python -c "
      import output.validator as v, main, sys
      orig = v.Validator.check_all
      v.Validator.check_all = lambda self, ctx: ['[#8 AGREEMENT_CURRENCY preferred] simulated failure for smoke test']
      try:
          main.main()
      except SystemExit as e:
          print(f'exit_code={e.code}')
      v.Validator.check_all = orig
      " 2>&1 | tail -2
      # must include exit_code=1
      ```

**Miscellaneous universal checks:**

- [ ] No CSV column named `*_Id` uses a non-BIGINT representation (spot-check: parse values as int and assert they fit in int64):
      ```python
      import pandas as pd, pathlib
      for p in sorted(pathlib.Path('output').rglob('*.csv')):
          df = pd.read_csv(p, nrows=100)
          for col in df.columns:
              if col.endswith('_Id') or col == 'Agreement_Id' or col == 'Party_Id' or col == 'Event_Id':
                  # non-null values must be representable as int64; empty values are allowed
                  s = df[col].dropna()
                  if len(s) and s.dtype.kind in ('i', 'u'):
                      assert int(s.max()) <= 2**63 - 1, f'{p}:{col} exceeds BIGINT range'
      print('BIGINT spot-check OK')
      ```
- [ ] `PARTY_INTERRACTION_EVENT.csv` filename preserves the double-R typo — covered above.
- [ ] `output/Core_DB/GEOSPATIAL.csv` does not exist — covered above.

## Handoff notes

*Leave empty — filled in at end of implementation session per `implementation-steps.md` "Handoff Protocol".*

# CLAUDE.md — CIF Synthetic Data Generator

Python tool that generates ~3,000 synthetic banking customers and ~5,000 agreements across 206 Teradata FSDM Layer 1 tables, written as CSVs.

## Ground truth (read in this order for any session)

1. `PRD.md` — product scope, scale, key decisions, out-of-scope items
2. `mvp-tool-design.md` — architecture, tier breakdown, dataclass specs, validator checklist
3. `implementation-steps.md` — 25-step work breakdown, spec → session workflow, seed-data authoring convention
4. `references/07_mvp-schema-reference.md` — authoritative DDL for all 206 MVP tables
5. `references/` — read only sections named by a spec's `Reads from` line; never read the whole folder

## Non-negotiable rules

- BIGINT for all ID columns, even when DDL says INTEGER (PRD §7.1, design §14 Decision 3)
- Shared party ID space — `CDM_Party_Id == Party_Id` in Core_DB (PRD §7.2, design §14 Decision 4)
- `PARTY_INTERRACTION_EVENT` preserves the double-R typo in table name and CSV filename (PRD §7.10, design §14 Decision 7)
- Skip `GEOSPATIAL` entirely — `ST_Geometry` has no CSV representation (PRD §7.9, design §14 Decision 8)
- DI columns (`di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind`) stamped on every table; `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` stamped additionally on CDM_DB and PIM_DB tables (PRD §7.3)
- Active record sentinels — `di_end_ts = '9999-12-31 00:00:00.000000'`, `Valid_To_Dt = '9999-12-31'` (PRD §7.3)
- Tier 0 lookup tables are seeded from handwritten `seed_data/*.py` dicts, never randomised; literal codes from `references/02_data-mapping-reference.md` Step 3 must appear verbatim (PRD §7.11, design §14 Decision 2)
- Exclusive AGREEMENT sub-typing — each agreement follows exactly one path through the inheritance chain (PRD §7.5)
- Self-employed individuals (~21.7%) reference reserved `ORGANIZATION` row with `Organization_Party_Id = 9999999` (PRD §7.12)
- No ORMs, no database connections — pure pandas → CSV; libraries: `numpy`, `pandas`, `faker`, `scipy`, `python-dateutil` (PRD §6)
- Reproducibility — all randomness derives from `ctx.rng` seeded by `config.settings.SEED = 42` (PRD §7.6, design §14 Decision 1)

## Workflow

1. `/create-spec <N> <slug>` — writes `specs/step-N-<slug>.md` and creates the step branch
2. Enter Plan Mode in a fresh Claude Code session; align on plan with user
3. Implement the step against the spec
4. Tick every box in the spec's `## Definition of done`
5. Update the spec's `## Handoff notes` with what shipped, deferrals, and the next-session hint
6. Commit, close session, start fresh for the next step — do not carry prior-step context forward

## Conflict resolution

When references disagree, trust this order (PRD §10):

1. `references/02_data-mapping-reference.md` (+ `resources/CIF_FSDM_Mapping_MASTER.xlsx` for clarification) — authoritative; do not change values here
2. `references/07_mvp-schema-reference.md` (takes precedence over `references/01_schema-reference.md` for MVP scope) plus `references/05_architect-qa.md` — primary supporting references
3. `references/06_supporting-enrichments.md` — incorporate only where it does not contradict priority 1
4. `mvp-tool-design.md` — implementation decisions derived from the above; update upstream if a conflict is found at the source level

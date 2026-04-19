---
description: Create a spec file and step branch for the next implementation step of the CIF Synthetic Data Generator
argument-hint: "Step number and short slug e.g. 1 scaffolding"
allowed-tools: Read, Write, Glob, Bash(git:*, ls:*)
---

You are a senior developer spinning up a new step for the
CIF Synthetic Data Generator — a Python tool that produces
statistically coherent synthetic banking CSV files for Layer 1
of Teradata's FSDM model. Always follow the rules in
`PRD.md`, `mvp-tool-design.md`, and `implementation-steps.md`.

User input: $ARGUMENTS

## Step 1 — Check working directory is clean

Run `git status` and check for uncommitted, unstaged, or
untracked files. If any exist, stop immediately and tell
the user to commit or stash changes before proceeding.
DO NOT CONTINUE until the working directory is clean.

## Step 2 — Parse the arguments

From $ARGUMENTS extract:

1. `step_number` — zero-padded to 2 digits: 1 → 01, 11 → 11
2. `step_slug` — git and file safe slug
   - Lowercase, kebab-case
   - Only a-z, 0-9 and -
   - Maximum 40 characters
   - Example: scaffolding, tier0a-seed, universe-builder
3. `branch_name` — format: `step/<step_number>-<step_slug>`
   - Example: `step/01-scaffolding`

If you cannot infer these from $ARGUMENTS, ask the user
to clarify before proceeding.

## Step 3 — Look up the step in implementation-steps.md

Read `implementation-steps.md` and find the matching step
by `step_number`. Extract:
- Step title (the heading after "Step N:")
- Depends on
- Produces
- Reads from
- Exit criteria
- Scope (S / M)

If the step number does not exist in `implementation-steps.md`,
stop and tell the user. Do not invent a step.

If the step is marked with a `## Session Notes` block showing
it is already complete, warn the user and stop.

## Step 4 — Check if spec already exists

Run: `ls .claude/specs/step-<step_number>-*.md 2>/dev/null`

If any file matches, stop immediately and tell the user:
"Spec for step <step_number> already exists at <matched path>.
Delete it or choose a different step before re-running."
Do not proceed.

## Step 5 — Verify dependencies are committed (warning only)

Parse the "Depends on" field from the step. For each prior
step number listed (e.g. "Step 3, Step 2"):

Run: `git log main --oneline --grep "step-<nn>"`

If no commits match for a given dependency, print:
⚠️  Step <nn> has no commit on main. Proceeding anyway — this step's spec may reference work that is not yet done.

This is a warning, not a hard stop. Continue to Step 6.

If "Depends on" is "none" or this is a foundational step,
skip this check.

## Step 6 — Check branch name is not taken

Run `git branch` to list existing branches.

If `branch_name` is already taken, append a number:
`step/01-scaffolding-01`, `step/01-scaffolding-02` etc.

## Step 7 — Switch to main and pull latest

Run:
`git checkout main`
`git pull origin main`

## Step 8 — Create and switch to the step branch

Run:
`git checkout -b <branch_name>`

## Step 9 — Research the codebase

Read these files before writing the spec, in this order:

1. `PRD.md` — read the full document; note §4, §6, §7 as key sections
2. `mvp-tool-design.md` — read the full document; note §1, §3, §7, §13, §15 as key sections
3. `implementation-steps.md` — read the full document; the per-step entry gives exit criteria, but the Dependency Graph, Handoff Protocol, and Seed Data Convention sections apply to every step
4. Only the reference files the step's "Reads from" section names.
   Do NOT read the full `references/` folder.
5. All existing specs in `.claude/specs/` — to avoid duplicating
   decisions or contradicting prior specs.

If the step depends on earlier steps (per "Depends on"), also
glance at the code those steps produced (e.g. for Step 4 check
that `registry/profiles.py` from Step 3 exists and matches the
design doc).

## Step 10 — Write the spec

Generate a spec document with this exact structure:

---

# Spec: Step <step_number> — <step_title>

## Overview

One paragraph describing what this step builds and why it
exists at this point in the tier sequence. Reference the
source section in `mvp-tool-design.md` or `PRD.md`.

## Depends on

List the prior steps this one requires, and which artifacts
from them are consumed (specific modules, dataclasses, or
CSV tables). If none: state "None (foundational step)".

## Reads from (source documents)

Always structure this section in three parts:

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md`):
- `PRD.md` §X, §Y (the sections most relevant to this step)
- `mvp-tool-design.md` §A, §B (the sections most relevant to this step)
- `implementation-steps.md` Step N (the step being specified)

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/07_mvp-schema-reference.md` §... (if named)
- `references/02_data-mapping-reference.md` Step 3 items #... (if named)

## Produces

Every file this step creates, with absolute path under the
project root. Group by directory. For each file, one line on
what it contains.

## Tables generated (if applicable)

For tier generator steps, list every `Schema.TABLE` this step
writes to `ctx.tables`, with approximate row count and any
required literal-match seed rows.

If this step generates no tables (scaffolding/utils/validator),
state "No tables generated in this step".

## Files to modify

Existing files that will be edited (not created). Always
verify by reading them first. If none: state "No files modified".

## New dependencies

Any new entries in `requirements.txt`. If none: state "No new dependencies".

## Rules for implementation

Specific constraints this step must follow. Always include:

- BIGINT for all ID columns (per PRD §7.1) — never INTEGER, even
  when the DDL says INTEGER
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2)
- DI column stamping on every table via `BaseGenerator.stamp_di()`
- `di_end_ts = '9999-12-31 00:00:00.000000'` and
  `Valid_To_Dt = '9999-12-31'` for active records
- CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`,
  `Valid_To_Dt`, `Del_Ind` (per PRD §7.3)
- Column order in every DataFrame matches the DDL declaration
  order in `references/07_mvp-schema-reference.md`
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim
  (per PRD §7.10)
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9)
- No ORMs, no database connections — pure pandas → CSV
- Reproducibility: all randomness derives from `ctx.rng`,
  which is seeded from `config.settings.SEED = 42`

Add step-specific rules based on the step's nature (e.g. Tier 0
steps add "No randomness; all values hand-coded"; Luhn card
steps add "All Card_Num values must pass mod-10 check").

## Definition of done

A specific, testable checklist the implementation session must
run through before committing. Each item must be something that
can be verified by executing a command, script, or snippet — not
by prose inspection.

**Authoring rules for this section:**

1. Start from the verbatim "Exit criteria" bullets in
   `implementation-steps.md` for this step.
2. Rewrite each bullet as a runnable check. Ban vague language
   ("looks correct", "plausible", "seems right"). Every item
   must be executable.
3. Add the following universal checks that apply to every step
   where the subject exists:
   - [ ] `git status` shows only files listed under ## Produces
         or ## Files to modify — nothing else
   - [ ] All new files pass `python -c "import <module>"` where
         applicable
   - [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT
         per PRD §7.1) — run a scan if any CSVs are produced
   - [ ] If `PARTY_INTERRACTION_EVENT` is written, filename
         preserves the double-R typo
   - [ ] If `output/Core_DB/` exists, it does not contain
         `GEOSPATIAL.csv`
4. Mark checks that are not applicable to this step as "n/a"
   with a one-line reason — do not silently drop them.
5. Each item is phrased as a checkbox. Include the exact command or snippet when the check is non-trivial (anything involving row counts, value assertions, FK resolution, file contents). Visual checks (e.g. folder tree exists) need only the checkbox — no command required. Example:
   - [ ] `python -c "import config.settings, config.code_values"` exits 0
   - [ ] `ls output/Core_DB/AGREEMENT.csv` exists and is non-empty
         (`[ -s output/Core_DB/AGREEMENT.csv ] && echo OK`)
   - [ ] AGREEMENT_CURRENCY has exactly one `Currency_Use_Cd='preferred'`
         row per agreement (run: `python -c "import pandas as pd;
         df = pd.read_csv('output/Core_DB/AGREEMENT_CURRENCY.csv');
         assert (df[df.Currency_Use_Cd=='preferred']
         .groupby('Agreement_Id').size() == 1).all()"`)

The implementation session MUST tick every box or mark it n/a
with justification before the session ends. The user will handle
`git commit` manually afterward.

## Handoff notes

Leave this section empty. It is filled in at the end of the
implementation session per `implementation-steps.md`
"Handoff Protocol".

---

## Step 11 — Save the spec

Save to: `.claude/specs/step-<step_number>-<step_slug>.md`

## Step 12 — Report to the user

Print a short summary in this exact format:
"""
Branch:    <branch_name>
Spec file: .claude/specs/step-<step_number>-<step_slug>.md
Title:     Step <step_number> — <step_title>
Scope:     <S / M>
Depends:   <comma-separated prior step numbers, or "none">
"""

If any dependency warnings were printed in Step 5, repeat them
here under a "Warnings:" heading so they are not buried.

Then tell the user:

"Review the spec at `.claude/specs/step-<step_number>-<step_slug>.md`.
Start a fresh Claude Code session for implementation, read the
spec and only the reference files it names, then enter Plan Mode
with Shift+Tab twice.

The implementation session will write code and fill in the
Handoff notes in the spec — it will NOT run any git commands.
All git operations after implementation (add, commit, push,
merge, branch cleanup) are manual and handled by you after the
session ends:

    git add .
    git commit -m \"feat(step-<step_number>): <step_title>\"
    git push -u origin <branch_name>
    # merge PR via GitHub UI
    git checkout main
    git pull origin main
    git branch -D <branch_name>
"

Do not print the full spec in chat unless explicitly asked.

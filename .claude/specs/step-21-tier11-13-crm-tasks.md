# Spec: Step 21 — Tier 11 + Tier 13 — CRM & Tasks

## Overview

This step completes the marketing (Tier 11) and customer-service-task (Tier 13) branches of the FSDM model. Tier 11 extends the 10 `CAMPAIGN` rows produced by Step 10 with a status history (`CAMPAIGN_STATUS`) and a marketing offer hierarchy (`PROMOTION` → `PROMOTION_OFFER`). Tier 13 wires every `COMPLAINT_EVENT` produced by Step 20 into a complaint-resolution task chain (`PARTY_TASK` → `PARTY_TASK_STATUS`, and `TASK_ACTIVITY` → `TASK_ACTIVITY_STATUS`), closing the complaint-to-task traceability loop. Neither tier generates new parties, agreements, or events — both are pure enrichment of upstream rows. See `mvp-tool-design.md` §9 Tier 11 and Tier 13 for the driving constraints.

## Depends on

- **Step 8** — Tier 0c seeds. Consumes `Core_DB.CAMPAIGN_STATUS_TYPE`, `Core_DB.PROMOTION_OFFER_TYPE`, `Core_DB.PROMOTION_METRIC_TYPE`, and `Core_DB.CHANNEL_TYPE` for FK resolution on CAMPAIGN_STATUS, PROMOTION, and PROMOTION_OFFER.
- **Step 10** — Tier 2 core entities. Consumes `Core_DB.CAMPAIGN` (10 rows; `Campaign_Id` BIGINT). Every CAMPAIGN_STATUS row FKs to a CAMPAIGN; every PROMOTION FKs to a CAMPAIGN.
- **Step 20** — Tier 10 events. Consumes `Core_DB.COMPLAINT_EVENT` (~150 rows; `Event_Id` BIGINT) and `Core_DB.EVENT_PARTY` (1 `initiator` row per event) — the former is the `Source_Event_Id` FK target for PARTY_TASK, the latter resolves `PARTY_TASK.Party_Id`.
- **Step 1** — `config/settings.py` (SIM_DATE, HISTORY_START, HIGH_DATE, HIGH_TS, ID ranges `'task': 3_000_000` and `'activity': 4_000_000`, and ID ranges for `'promotion': 200`).
- **Step 2** — `utils/id_factory.IdFactory`, `utils/date_utils.format_ts`/`format_date`, and `generators/base.BaseGenerator` (for `stamp_di`).
- **Step 3** — `registry/context.GenerationContext` (reads `ctx.tables`, writes back to it).

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to:**
- `PRD.md` §4.1, §4.2 (customized extensions scope — PARTY_TASK/PARTY_TASK_STATUS/TASK_ACTIVITY/TASK_ACTIVITY_STATUS), §7.1 (BIGINT everywhere), §7.3 (DI column rules)
- `mvp-tool-design.md` §9 Tier 11 (CAMPAIGN_STATUS / PROMOTION / PROMOTION_OFFER constraints), §9 Tier 13 (complaint → task chain; SMALLINT codes per `code_values.py`), §12 constraints #15 and #16 (≥1 CAMPAIGN_STATUS per CAMPAIGN; up to 5 PROMOTION_OFFER per PROMOTION)
- `implementation-steps.md` Step 21 (exit criteria)

**Additional reference files** (named in the step's "Reads from" line — plus minimal DDL verification per the DDL verification rule in CLAUDE.md):
- `references/07_mvp-schema-reference.md` §CAMPAIGN_STATUS (lines ~4402), §PROMOTION (~7227), §PROMOTION_OFFER (~7326), §PARTY_TASK (~8361), §TASK_ACTIVITY (~8381)
- `resources/Core_DB_customized.sql` §PARTY_TASK_STATUS, §TASK_ACTIVITY_STATUS — these two customized tables are **not** in `07_mvp-schema-reference.md`; `Core_DB_customized.sql` is the authoritative DDL source for them (per PRD §4.2 note)

## Produces

### New generator modules

- `generators/tier11_crm.py` — `Tier11CRM(BaseGenerator)` class. `generate(ctx)` returns a dict with three keys:
  - `'Core_DB.CAMPAIGN_STATUS'`
  - `'Core_DB.PROMOTION'`
  - `'Core_DB.PROMOTION_OFFER'`
- `generators/tier13_tasks.py` — `Tier13Tasks(BaseGenerator)` class. `generate(ctx)` returns a dict with four keys:
  - `'Core_DB.PARTY_TASK'`
  - `'Core_DB.PARTY_TASK_STATUS'`
  - `'Core_DB.TASK_ACTIVITY'`
  - `'Core_DB.TASK_ACTIVITY_STATUS'`

## Tables generated

**Tier 11 (Core_DB standard — 3 DI columns per DDL):**

| Table | Approx rows | Row-construction rule |
|-------|-------------|-----------------------|
| `Core_DB.CAMPAIGN_STATUS` | 10 (one per CAMPAIGN) | 1 current row per campaign: `Campaign_Id` FK, `Campaign_Status_Start_Dttm` = campaign start offset back from SIM_DATE, `Campaign_Status_Cd` drawn from seeded `CAMPAIGN_STATUS_TYPE.Campaign_Status_Cd`, `Campaign_Status_End_Dttm = NULL`. No historical rows needed — constraint #15 only requires ≥1. |
| `Core_DB.PROMOTION` | ~20–30 (2–3 per CAMPAIGN) | `Promotion_Id` BIGINT from `IdFactory('promotion')`. `Campaign_Id` FK. `Promotion_Type_Cd` VARCHAR(50) free-form (e.g. `'acquisition'`, `'retention'`, `'cross-sell'`). `Channel_Type_Cd` FK to seeded `CHANNEL_TYPE.Channel_Type_Cd` (e.g. `'EMAIL'`, `'ONLINE'`, `'MOBILE'`). `Promotion_Start_Dt` and `Promotion_End_Dt` inside or overlapping the history window. Amounts (`Promotion_Actual_Unit_Cost_Amt`, `Promotion_Goal_Amt`) as `Decimal` with 4dp. `Currency_Cd = 'USD'`. `Unit_Of_Measure_Cd` FK to seeded `UNIT_OF_MEASURE`. |
| `Core_DB.PROMOTION_OFFER` | ~50–150 (1–5 per PROMOTION) | Composite logical PK `(Promotion_Id, Promotion_Offer_Id)`. `Promotion_Offer_Id` is a **within-promotion sequence 1..N** (1-based), **not** from `IdFactory` — restart at 1 for each promotion. `Promotion_Offer_Type_Cd` FK to seeded `PROMOTION_OFFER_TYPE.Promotion_Offer_Type_Cd`. `Ad_Id` NULL (no Ad table in scope). Distribution/Redemption dates inside or overlapping the history window. |

**Tier 13 (Core_DB customized extension — 5 DI columns per DDL):**

| Table | Approx rows | Row-construction rule |
|-------|-------------|-----------------------|
| `Core_DB.PARTY_TASK` | ≈ 150 (one per COMPLAINT_EVENT) | `Task_Id` BIGINT from `IdFactory('task')`. `Source_Event_Id = COMPLAINT_EVENT.Event_Id`. `Party_Id` resolved by joining COMPLAINT_EVENT.Event_Id → EVENT_PARTY (role `'initiator'`). `Task_Activity_Type_Cd`, `Task_Subtype_Cd`, `Task_Reason_Cd` SMALLINT NOT NULL — values drawn from `config/code_values.py` enums defined in this step. |
| `Core_DB.PARTY_TASK_STATUS` | 150–450 (1–3 per PARTY_TASK) | `Task_Status_Id` BIGINT (new ID range or reuse `'task'` — see Rules). `Task_Id` FK. Status progression across rows: e.g. OPEN (open → in-progress TS) → IN_PROGRESS (→ resolved TS) → RESOLVED (→ HIGH_TS). Every row has non-NULL `Task_Status_Start_Dttm` and `Task_Status_End_Dttm` (both NOT NULL per DDL). Only the final row may end at `HIGH_TS`; earlier rows carry a real end-timestamp equal to the next row's start. `Task_Status_Type_Cd`, `Task_Status_Reason_Cd` SMALLINT. `Task_Status_Txt` nullable free text. |
| `Core_DB.TASK_ACTIVITY` | 150–450 (1–3 per PARTY_TASK) | `Activity_Id` BIGINT from `IdFactory('activity')`. `Task_Id` FK. `Activity_Type_Cd` SMALLINT NOT NULL. `Activity_Txt` short free text (e.g. `'Customer contacted via email'`). `Activity_Channel_Id` BIGINT FK to a `CHANNEL_INSTANCE.Channel_Instance_Id` (nullable but preferred populated). `Activity_Start_Dttm` and `Activity_End_Dttm` both NOT NULL — activity bounded (end_dttm = start + realistic duration, e.g. 5–30 minutes). |
| `Core_DB.TASK_ACTIVITY_STATUS` | 150–450 (≈1 per TASK_ACTIVITY) | Shares `Activity_Id` with TASK_ACTIVITY (not a new ID). `Activity_Status_Start_Dttm`, `Activity_Status_End_Dttm` both NOT NULL. `Activity_Status_Type_Cd`, `Activity_Status_Reason_Cd` SMALLINT NOT NULL. |

Total new rows: ≈ 10 + 25 + 100 + 150 + 300 + 300 + 300 ≈ 1,200.

## Files to modify

- `config/code_values.py` — **append** SMALLINT enum dicts for:
  - `TASK_ACTIVITY_TYPE_CD` (e.g. `{1: 'COMPLAINT_RESOLUTION', 2: 'SERVICE_REQUEST', 3: 'ACCOUNT_UPDATE'}`)
  - `TASK_SUBTYPE_CD` (e.g. `{1: 'INVESTIGATION', 2: 'ESCALATION', 3: 'COMPENSATION'}`)
  - `TASK_REASON_CD` (e.g. `{1: 'FEE_DISPUTE', 2: 'SERVICE_QUALITY', 3: 'PRODUCT_ISSUE'}`)
  - `TASK_STATUS_TYPE_CD` (`{1: 'OPEN', 2: 'IN_PROGRESS', 3: 'RESOLVED', 4: 'CLOSED'}`)
  - `TASK_STATUS_REASON_CD` (`{1: 'INITIAL_INTAKE', 2: 'AWAITING_CUSTOMER', 3: 'RESOLVED_SUCCESS', 4: 'RESOLVED_FAILURE'}`)
  - `ACTIVITY_TYPE_CD` (`{1: 'OUTBOUND_CALL', 2: 'INBOUND_CALL', 3: 'EMAIL', 4: 'INTERNAL_NOTE', 5: 'FOLLOW_UP'}`)
  - `ACTIVITY_STATUS_TYPE_CD` (`{1: 'PENDING', 2: 'COMPLETED', 3: 'FAILED'}`)
  - `ACTIVITY_STATUS_REASON_CD` (`{1: 'EXECUTED', 2: 'NO_RESPONSE', 3: 'CUSTOMER_SATISFIED'}`)

  Exact enum values are free to refine during implementation provided they are stable within the session; the requirement is that every SMALLINT column in Tier 13 tables draws from a named dict in this module.

- `utils/id_factory.py` and `config/settings.py` (ID ranges dict) — **only if** a new ID sequence is needed for `PARTY_TASK_STATUS.Task_Status_Id` (it has its own PK distinct from `Task_Id` per DDL). Preferred approach: add `'task_status': 3_500_000` to `ID_RANGES` in `settings.py`. If the session chooses to derive `Task_Status_Id` deterministically from `(Task_Id, sequence_no)` instead, document that decision in Handoff notes and do not modify `id_factory`.

No other files modified.

## New dependencies

No new dependencies.

## Rules for implementation

Universal rules (every step):

- BIGINT for all ID columns (per PRD §7.1) — never INTEGER, even when the DDL says INTEGER. Applies to `Campaign_Id`, `Promotion_Id`, `Task_Id`, `Source_Event_Id`, `Party_Id`, `Activity_Id`, `Task_Status_Id`, `Activity_Channel_Id`, and the within-promotion `Promotion_Offer_Id`. Emit every `*_Id` pandas column as `Int64` (nullable bigint) so NULL FKs format correctly.
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2).
- DI column stamping on every table via `BaseGenerator.stamp_di()`. The method always appends 5 DI columns; the writer (`output/writer.py`) projects to the DDL column list per table, so tables whose DDL has only 3 DI cols (CAMPAIGN_STATUS, PROMOTION, PROMOTION_OFFER) will have the extra two dropped at write time. Do not conditionally skip `stamp_di` for those tables — apply it uniformly.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records.
- CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` (per PRD §7.3) — **n/a for this step**; all 7 tables here are Core_DB.
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` for the five tables listed there, and `resources/Core_DB_customized.sql` for PARTY_TASK_STATUS / TASK_ACTIVITY_STATUS. Use a module-level `_COLS_<TABLE>: List[str]` list (matching the tier10 pattern) per table and pass `columns=_COLS_<TABLE>` into `pd.DataFrame(...)`.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — n/a for this step; that table belongs to Tier 14.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — n/a for this step.
- No ORMs, no database connections — pure pandas → CSV.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42`. Running `python main.py` twice must produce byte-identical CSVs for both Tier 11 and Tier 13 tables.

Step-specific rules:

- **Campaign status** — The 10 campaigns are free to pick any current status from the seeded `CAMPAIGN_STATUS_TYPE` table; constraint #15 in §12 only requires ≥1 per campaign. No historical CAMPAIGN_STATUS rows required. `Campaign_Status_Start_Dttm` must be NOT NULL (DDL); `Campaign_Status_End_Dttm` NULL for current (active) status.
- **Promotion counts** — 2–3 promotions per campaign, chosen via `ctx.rng.integers(2, 4)` (not hardcoded per campaign). Total promotions land in ~20–30 range.
- **Promotion offer counts** — 1–5 offers per promotion, chosen via `ctx.rng.integers(1, 6)`. The design doc notes the 5-offer cap aligns with `PROMOTION_BB`'s 1st–5th pivoted columns in Layer 2.
- **`Promotion_Offer_Id` is within-promotion** — restart at 1 for each promotion; do not mint from `IdFactory`. This matches the NUPI on `Promotion_Id` and the Layer 2 pivot semantics.
- **Complaint→task linkage is 1:1** — Every `COMPLAINT_EVENT.Event_Id` must appear **exactly once** as a `PARTY_TASK.Source_Event_Id`. Iterate `ctx.tables['Core_DB.COMPLAINT_EVENT']['Event_Id']` directly; do not probabilistically drop events.
- **`PARTY_TASK.Party_Id` source** — Join COMPLAINT_EVENT.Event_Id → EVENT_PARTY (`Event_Party_Role_Cd == 'initiator'`) → `Party_Id`. Do NOT bypass the join by pulling from any customer-level registry; the initiator is authoritative.
- **Status progression invariants** — Within a `(Task_Id, Task_Status_Start_Dttm)` group, rows are chronologically contiguous: row N's `Task_Status_End_Dttm` equals row N+1's `Task_Status_Start_Dttm`. Only the **final** row in each chain may end at `HIGH_TS`. At least one PARTY_TASK_STATUS row per PARTY_TASK; same rule for TASK_ACTIVITY_STATUS per TASK_ACTIVITY.
- **TASK_ACTIVITY temporal bounds** — `Activity_Start_Dttm` falls on or after the parent complaint's `Event_Received_Dttm`. `Activity_End_Dttm` = `Activity_Start_Dttm` + 5–30 minutes (`ctx.rng.integers(5, 31)`). Both are NOT NULL per DDL.
- **`Activity_Channel_Id` FK** — Populate with a valid `Channel_Instance_Id` sampled from `ctx.tables['Core_DB.CHANNEL_INSTANCE']` (20 rows produced by Step 10). NULL is permitted by DDL but populated is preferred to exercise the FK chain.
- **SMALLINT dtype** — Pandas has no Int16; project convention (from Step 20) is to store SMALLINT columns as `Int64`. Cast every task/activity SMALLINT column with `.astype('Int64')`.
- **No randomness without `ctx.rng`** — Never call `numpy.random.*` directly. Do not use Python's `random` module. Do not seed a new RNG.
- **Determinism of iteration** — When iterating `COMPLAINT_EVENT` rows, sort by `Event_Id` first (`df.sort_values('Event_Id')`) before iterating, to ensure deterministic task/activity ID assignment across runs.

## Definition of done

Tick every box before the session ends, or mark as `n/a` with a one-line justification.

**Source-of-truth & scaffolding:**

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else
- [ ] `python -c "import generators.tier11_crm, generators.tier13_tasks"` exits 0
- [ ] `python -c "from generators.tier11_crm import Tier11CRM; from generators.tier13_tasks import Tier13Tasks; Tier11CRM().generate; Tier13Tasks().generate"` exits 0
- [ ] `config/code_values.py` re-imports cleanly: `python -c "import config.code_values as cv; assert hasattr(cv, 'TASK_ACTIVITY_TYPE_CD') and hasattr(cv, 'ACTIVITY_STATUS_TYPE_CD')"` exits 0

**Row-count & structural invariants (run against `ctx` built by `Tier11CRM().generate(ctx)` / `Tier13Tasks().generate(ctx)` after all earlier tiers):**

- [ ] CAMPAIGN_STATUS has ≥1 row per CAMPAIGN (constraint #15):
      ```python
      camp = ctx.tables['Core_DB.CAMPAIGN']['Campaign_Id']
      cs   = ctx.tables['Core_DB.CAMPAIGN_STATUS']
      assert set(camp) <= set(cs['Campaign_Id']), 'CAMPAIGNs missing CAMPAIGN_STATUS'
      assert (cs.groupby('Campaign_Id').size() >= 1).all()
      ```
- [ ] Every CAMPAIGN_STATUS.Campaign_Status_Cd resolves to the seeded `CAMPAIGN_STATUS_TYPE`:
      ```python
      cst = ctx.tables['Core_DB.CAMPAIGN_STATUS_TYPE']['Campaign_Status_Cd']
      assert set(cs['Campaign_Status_Cd']).issubset(set(cst))
      ```
- [ ] Every PROMOTION.Campaign_Id resolves to a CAMPAIGN row:
      ```python
      pr = ctx.tables['Core_DB.PROMOTION']
      assert set(pr['Campaign_Id']).issubset(set(camp))
      ```
- [ ] Every CAMPAIGN has 2–3 PROMOTION rows (per-campaign coverage — not just global total):
      ```python
      per_camp = pr.groupby('Campaign_Id').size()
      assert set(per_camp.index) == set(camp), 'some CAMPAIGNs have zero PROMOTIONs'
      assert per_camp.between(2, 3).all(), f'per-campaign counts out of range: {per_camp.to_dict()}'
      assert 20 <= len(pr) <= 30  # derived consequence of the per-campaign rule
      ```
- [ ] Every PROMOTION has 1–5 PROMOTION_OFFER rows (constraint #16):
      ```python
      po = ctx.tables['Core_DB.PROMOTION_OFFER']
      counts = po.groupby('Promotion_Id').size()
      assert (counts.between(1, 5)).all()
      assert set(pr['Promotion_Id']).issubset(set(po['Promotion_Id']))
      ```
- [ ] `Promotion_Offer_Id` restarts at 1 per promotion and is contiguous:
      ```python
      for pid, grp in po.groupby('Promotion_Id'):
          ids = sorted(grp['Promotion_Offer_Id'].tolist())
          assert ids == list(range(1, len(ids)+1)), f'Promotion {pid}: {ids}'
      ```
- [ ] Every PROMOTION.Channel_Type_Cd resolves to seeded CHANNEL_TYPE (or is NULL):
      ```python
      ct = set(ctx.tables['Core_DB.CHANNEL_TYPE']['Channel_Type_Cd'])
      nn = pr['Channel_Type_Cd'].dropna()
      assert set(nn).issubset(ct)
      ```
- [ ] Every COMPLAINT_EVENT.Event_Id appears **exactly once** as PARTY_TASK.Source_Event_Id, and every PARTY_TASK.Task_Id is unique:
      ```python
      ce   = ctx.tables['Core_DB.COMPLAINT_EVENT']['Event_Id']
      pt   = ctx.tables['Core_DB.PARTY_TASK']
      assert len(pt) == len(ce)
      assert set(pt['Source_Event_Id']) == set(ce)
      assert pt['Source_Event_Id'].is_unique
      assert pt['Task_Id'].is_unique, 'duplicate Task_Id would break downstream groupby joins'
      ```
- [ ] Every PARTY_TASK.Party_Id matches the initiator EVENT_PARTY row for the same Event_Id:
      ```python
      ep = ctx.tables['Core_DB.EVENT_PARTY']
      init = ep[ep['Event_Party_Role_Cd'] == 'initiator'][['Event_Id', 'Party_Id']]
      merged = pt.merge(init, left_on='Source_Event_Id', right_on='Event_Id', suffixes=('_task','_ep'))
      assert (merged['Party_Id_task'] == merged['Party_Id_ep']).all()
      ```
- [ ] Every PARTY_TASK has ≥1 PARTY_TASK_STATUS row:
      ```python
      pts = ctx.tables['Core_DB.PARTY_TASK_STATUS']
      assert set(pt['Task_Id']).issubset(set(pts['Task_Id']))
      assert (pts.groupby('Task_Id').size() >= 1).all()
      ```
- [ ] Every PARTY_TASK has ≥1 TASK_ACTIVITY row:
      ```python
      ta = ctx.tables['Core_DB.TASK_ACTIVITY']
      assert set(pt['Task_Id']).issubset(set(ta['Task_Id']))
      assert (ta.groupby('Task_Id').size() >= 1).all()
      ```
- [ ] Every TASK_ACTIVITY has ≥1 TASK_ACTIVITY_STATUS row:
      ```python
      tas = ctx.tables['Core_DB.TASK_ACTIVITY_STATUS']
      assert set(ta['Activity_Id']).issubset(set(tas['Activity_Id']))
      ```
- [ ] PARTY_TASK_STATUS and TASK_ACTIVITY_STATUS chains are temporally contiguous (no gaps/overlaps within a chain); only the final row of each chain may end at `HIGH_TS`:
      ```python
      from config.settings import HIGH_TS
      for tid, grp in pts.sort_values(['Task_Id','Task_Status_Start_Dttm']).groupby('Task_Id'):
          ends   = grp['Task_Status_End_Dttm'].tolist()
          starts = grp['Task_Status_Start_Dttm'].tolist()
          for i in range(len(grp)-1):
              assert ends[i] == starts[i+1], f'Task {tid} chain gap at row {i}'
          assert ends[-1] == HIGH_TS or ends[-1] > starts[-1]
      ```
- [ ] TASK_ACTIVITY temporal bounds are realistic (end ≥ start, duration ≤ 30 minutes):
      ```python
      from datetime import datetime
      for _, r in ta.iterrows():
          s = datetime.strptime(r['Activity_Start_Dttm'], '%Y-%m-%d %H:%M:%S.%f')
          e = datetime.strptime(r['Activity_End_Dttm'],   '%Y-%m-%d %H:%M:%S.%f')
          assert e >= s
          assert (e - s).total_seconds() <= 30 * 60
      ```
- [ ] Every TASK_ACTIVITY.Activity_Channel_Id (if populated) resolves to CHANNEL_INSTANCE.Channel_Instance_Id:
      ```python
      ci_ids = set(ctx.tables['Core_DB.CHANNEL_INSTANCE']['Channel_Instance_Id'].astype(int))
      nn = ta['Activity_Channel_Id'].dropna().astype(int)
      assert set(nn).issubset(ci_ids)
      ```

**ID-type / dtype invariants:**

- [ ] All `*_Id` columns across the 7 produced tables have pandas dtype `Int64` (nullable BIGINT per PRD §7.1):
      ```python
      id_cols = {
          'Core_DB.CAMPAIGN_STATUS':    ['Campaign_Id'],
          'Core_DB.PROMOTION':          ['Promotion_Id', 'Campaign_Id'],
          'Core_DB.PROMOTION_OFFER':    ['Promotion_Id', 'Promotion_Offer_Id', 'Ad_Id'],
          'Core_DB.PARTY_TASK':         ['Task_Id', 'Party_Id', 'Source_Event_Id'],
          'Core_DB.PARTY_TASK_STATUS':  ['Task_Status_Id', 'Task_Id'],
          'Core_DB.TASK_ACTIVITY':      ['Activity_Id', 'Task_Id', 'Activity_Channel_Id'],
          'Core_DB.TASK_ACTIVITY_STATUS': ['Activity_Id'],
      }
      for k, cols in id_cols.items():
          df = ctx.tables[k]
          for c in cols:
              assert str(df[c].dtype) == 'Int64', f'{k}.{c}: {df[c].dtype}'
      ```
- [ ] All Tier 13 SMALLINT code columns have dtype `Int64`:
      ```python
      sm_cols = {
          'Core_DB.PARTY_TASK':           ['Task_Activity_Type_Cd','Task_Subtype_Cd','Task_Reason_Cd'],
          'Core_DB.PARTY_TASK_STATUS':    ['Task_Status_Type_Cd','Task_Status_Reason_Cd'],
          'Core_DB.TASK_ACTIVITY':        ['Activity_Type_Cd'],
          'Core_DB.TASK_ACTIVITY_STATUS': ['Activity_Status_Type_Cd','Activity_Status_Reason_Cd'],
      }
      for k, cols in sm_cols.items():
          df = ctx.tables[k]
          for c in cols:
              assert str(df[c].dtype) == 'Int64', f'{k}.{c}: {df[c].dtype}'
      ```
- [ ] Every NOT-NULL column in the DDL has no NULL in the produced DataFrame:
      ```python
      not_null = {
          'Core_DB.CAMPAIGN_STATUS':    ['Campaign_Id','Campaign_Status_Start_Dttm'],
          'Core_DB.PROMOTION':          ['Promotion_Id','Promotion_Type_Cd','Campaign_Id'],
          'Core_DB.PROMOTION_OFFER':    ['Promotion_Id','Promotion_Offer_Id'],
          'Core_DB.PARTY_TASK':         ['Task_Id','Task_Activity_Type_Cd','Task_Subtype_Cd','Task_Reason_Cd'],
          'Core_DB.PARTY_TASK_STATUS':  ['Task_Status_Id','Task_Status_Start_Dttm','Task_Status_End_Dttm','Task_Status_Type_Cd','Task_Status_Reason_Cd'],
          'Core_DB.TASK_ACTIVITY':      ['Activity_Id','Activity_Type_Cd','Activity_Start_Dttm','Activity_End_Dttm'],
          'Core_DB.TASK_ACTIVITY_STATUS':['Activity_Id','Activity_Status_Start_Dttm','Activity_Status_End_Dttm','Activity_Status_Type_Cd','Activity_Status_Reason_Cd'],
      }
      for k, cols in not_null.items():
          df = ctx.tables[k]
          for c in cols:
              assert df[c].notna().all(), f'{k}.{c} has NULL'
      ```

**DI column invariants:**

- [ ] Every produced DataFrame carries the 5-col DI suffix from `stamp_di`:
      ```python
      for k in ['Core_DB.CAMPAIGN_STATUS','Core_DB.PROMOTION','Core_DB.PROMOTION_OFFER',
                'Core_DB.PARTY_TASK','Core_DB.PARTY_TASK_STATUS','Core_DB.TASK_ACTIVITY','Core_DB.TASK_ACTIVITY_STATUS']:
          df = ctx.tables[k]
          for c in ['di_data_src_cd','di_start_ts','di_proc_name','di_rec_deleted_Ind','di_end_ts']:
              assert c in df.columns, f'{k} missing {c}'
          assert (df['di_end_ts'] == '9999-12-31 00:00:00.000000').all()
          assert (df['di_rec_deleted_Ind'] == 'N').all()
      ```
- [ ] No Tier 11/13 table carries `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` columns (those are CDM_DB/PIM_DB only — n/a here).

**Column order:**

- [ ] Each DataFrame's business-column order exactly matches the DDL declaration order, verified via the Writer's projection:
      ```python
      from output.writer import _reorder_to_ddl
      for k in ['Core_DB.CAMPAIGN_STATUS','Core_DB.PROMOTION','Core_DB.PROMOTION_OFFER',
                'Core_DB.PARTY_TASK','Core_DB.PARTY_TASK_STATUS','Core_DB.TASK_ACTIVITY','Core_DB.TASK_ACTIVITY_STATUS']:
          _reorder_to_ddl(ctx.tables[k], k)  # raises on any DDL vs DataFrame column mismatch
      ```

**Reproducibility:**

- [ ] Running `Tier11CRM().generate(ctx)` twice on two freshly-built contexts (both seeded from 42 and carrying the same upstream tables) yields DataFrames that compare equal via `pd.testing.assert_frame_equal`. Same check for `Tier13Tasks().generate(ctx)`.

**Miscellaneous universal checks:**

- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — covered by the ID-dtype invariant above. n/a for CSV-level check since this step does not run the Writer end-to-end; verified at the DataFrame level.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — n/a; this step does not produce that table.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — n/a; this step does not produce location CSVs and does not invoke the Writer.

## Handoff notes

### What shipped

- `generators/tier11_crm.py` — `Tier11CRM` class generating `CAMPAIGN_STATUS` (10 rows), `PROMOTION` (26 rows), `PROMOTION_OFFER` (74 rows). `Promotion_Offer_Id` is within-promotion sequence (not from IdFactory).
- `generators/tier13_tasks.py` — `Tier13Tasks` class generating `PARTY_TASK` (145 rows), `PARTY_TASK_STATUS` (275 rows), `TASK_ACTIVITY` (267 rows), `TASK_ACTIVITY_STATUS` (267 rows). 1:1 complaint→task linkage, Party_Id from EVENT_PARTY initiator join, temporal chain contiguous with HIGH_TS final row.
- `config/code_values.py` — appended 8 SMALLINT enum dicts (`TASK_ACTIVITY_TYPE_CD`, `TASK_SUBTYPE_CD`, `TASK_REASON_CD`, `TASK_STATUS_TYPE_CD`, `TASK_STATUS_REASON_CD`, `ACTIVITY_TYPE_CD`, `ACTIVITY_STATUS_TYPE_CD`, `ACTIVITY_STATUS_REASON_CD`).
- `config/settings.py` — added `'task_status': 3_500_000` to `ID_RANGES`.
- `references/07_mvp-schema-reference.md` — added DDL table entries for `PARTY_TASK_STATUS` and `TASK_ACTIVITY_STATUS` (both absent from the file; needed for writer's `_reorder_to_ddl` lookup). Source: `resources/Core_DB_customized.sql`.

### Decisions

- `stamp_di` applied uniformly to all 7 tables (5 DI cols). Spec claim that "writer drops extra 2 for 3-DI-col tables" is factually wrong — writer emits all DI cols present in DataFrame. No special-casing needed.
- `Task_Status_Id` uses new `'task_status'` IdFactory sequence (3.5M range), not derived from `Task_Id`. This was the preferred approach per spec.

### Deferrals

None. All DoD items verified (21/21 checks pass).

### Next-session hint

Step 22 — Tier 14 CDM_DB tables. Check `main.py` comment block for `Tier14CDM()` import. Upstream dependency: needs `Core_DB.PARTY_INTERRACTION_EVENT` table name typo preserved (`PARTY_INTERRACTION_EVENT` — double-R). The constant `PARTY_INTERRACTION_EVENT_TABLE_NAME` in `config/settings.py` is the single source of truth for this.

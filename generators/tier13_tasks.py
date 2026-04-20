from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, List, Tuple

import pandas as pd

from config.settings import HIGH_TS
from generators.base import BaseGenerator
from utils.date_utils import format_ts

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ---------------------------------------------------------------------------
# DI start timestamp
# ---------------------------------------------------------------------------
_TIER13_DI_START_TS = '2000-01-01 00:00:00.000000'

# ---------------------------------------------------------------------------
# Schema keys
# ---------------------------------------------------------------------------
_PARTY_TASK_KEY            = 'Core_DB.PARTY_TASK'
_PARTY_TASK_STATUS_KEY     = 'Core_DB.PARTY_TASK_STATUS'
_TASK_ACTIVITY_KEY         = 'Core_DB.TASK_ACTIVITY'
_TASK_ACTIVITY_STATUS_KEY  = 'Core_DB.TASK_ACTIVITY_STATUS'

# ---------------------------------------------------------------------------
# Upstream table keys
# ---------------------------------------------------------------------------
_COMPLAINT_EVENT_KEY = 'Core_DB.COMPLAINT_EVENT'
_EVENT_PARTY_KEY     = 'Core_DB.EVENT_PARTY'
_CHANNEL_INSTANCE_KEY = 'Core_DB.CHANNEL_INSTANCE'

# ---------------------------------------------------------------------------
# Required upstream tables for guard
# ---------------------------------------------------------------------------
_REQUIRED_UPSTREAM = (
    _COMPLAINT_EVENT_KEY,
    _EVENT_PARTY_KEY,
    _CHANNEL_INSTANCE_KEY,
)

# ---------------------------------------------------------------------------
# Activity free-text pool
# ---------------------------------------------------------------------------
_ACTIVITY_TEXTS = [
    'Customer contacted via email',
    'Outbound call attempted',
    'Internal note added',
    'Follow-up scheduled',
    'Case reviewed',
]

# ---------------------------------------------------------------------------
# Column lists (business cols only; DI tail appended by stamp_di)
# ---------------------------------------------------------------------------
_COLS_PARTY_TASK: List[str] = [
    'Task_Id', 'Party_Id', 'Source_Event_Id',
    'Task_Activity_Type_Cd', 'Task_Subtype_Cd', 'Task_Reason_Cd',
]

_COLS_PARTY_TASK_STATUS: List[str] = [
    'Task_Status_Id', 'Task_Id',
    'Task_Status_Start_Dttm', 'Task_Status_End_Dttm',
    'Task_Status_Type_Cd', 'Task_Status_Reason_Cd', 'Task_Status_Txt',
]

_COLS_TASK_ACTIVITY: List[str] = [
    'Activity_Id', 'Task_Id', 'Activity_Type_Cd', 'Activity_Txt',
    'Activity_Channel_Id', 'Activity_Start_Dttm', 'Activity_End_Dttm',
]

_COLS_TASK_ACTIVITY_STATUS: List[str] = [
    'Activity_Id',
    'Activity_Status_Start_Dttm', 'Activity_Status_End_Dttm',
    'Activity_Status_Type_Cd', 'Activity_Status_Reason_Cd', 'Activity_Status_Txt',
]

# ---------------------------------------------------------------------------
# Status chain definitions: (status_type_cd, reason_cd_override_or_None)
# reason_cd is drawn randomly per row; this is just the status progression
# ---------------------------------------------------------------------------
_STATUS_CHAIN_BY_LEN = {
    1: [1],           # OPEN
    2: [1, 2],        # OPEN → IN_PROGRESS
    3: [1, 2, 3],     # OPEN → IN_PROGRESS → RESOLVED
}


# ---------------------------------------------------------------------------
# Generator class
# ---------------------------------------------------------------------------

class Tier13Tasks(BaseGenerator):

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        for key in _REQUIRED_UPSTREAM:
            if key not in ctx.tables:
                raise RuntimeError(f'Tier 13 prerequisite missing: {key}')

        rng = ctx.rng

        # Build initiator map: {event_id → party_id}
        ep_df = ctx.tables[_EVENT_PARTY_KEY]
        init_df = ep_df[ep_df['Event_Party_Role_Cd'] == 'initiator'][['Event_Id', 'Party_Id']]
        initiator_map: Dict[int, int] = dict(
            zip(init_df['Event_Id'].astype(int), init_df['Party_Id'].astype(int))
        )

        # Channel IDs for Activity_Channel_Id FK
        channel_ids: List[int] = (
            ctx.tables[_CHANNEL_INSTANCE_KEY]['Channel_Instance_Id'].astype(int).tolist()
        )

        # Sort complaints for determinism
        ce_df = ctx.tables[_COMPLAINT_EVENT_KEY].sort_values('Event_Id')

        task_rows:       List[dict] = []
        status_rows:     List[dict] = []
        act_rows:        List[dict] = []
        act_status_rows: List[dict] = []

        for _, ce_row in ce_df.iterrows():
            event_id = int(ce_row['Event_Id'])
            party_id = initiator_map.get(event_id)
            if party_id is None:
                continue

            # Parse received timestamp — stored as datetime/Timestamp by tier10
            received = ce_row['Event_Received_Dttm']
            if isinstance(received, str):
                received = datetime.strptime(received, '%Y-%m-%d %H:%M:%S.%f')
            else:
                received = received.to_pydatetime()

            task_id = ctx.ids.next('task')

            # PARTY_TASK
            task_rows.append({
                'Task_Id':               task_id,
                'Party_Id':              party_id,
                'Source_Event_Id':       event_id,
                'Task_Activity_Type_Cd': int(rng.integers(1, 4)),
                'Task_Subtype_Cd':       int(rng.integers(1, 4)),
                'Task_Reason_Cd':        int(rng.integers(1, 4)),
            })

            # Base timestamp for this task's status chain and activities
            base_ts = received + timedelta(minutes=int(rng.integers(5, 61)))

            # PARTY_TASK_STATUS chain
            chain_len = int(rng.integers(1, 4))
            status_seq = _STATUS_CHAIN_BY_LEN[chain_len]
            ts_cursor = base_ts

            for i, status_type_cd in enumerate(status_seq):
                is_last = (i == len(status_seq) - 1)
                if is_last:
                    end_ts_str = HIGH_TS
                    next_ts = None
                else:
                    delta = timedelta(hours=int(rng.integers(1, 25)))
                    next_ts = ts_cursor + delta
                    end_ts_str = format_ts(next_ts)

                status_rows.append({
                    'Task_Status_Id':        ctx.ids.next('task_status'),
                    'Task_Id':               task_id,
                    'Task_Status_Start_Dttm': format_ts(ts_cursor),
                    'Task_Status_End_Dttm':   end_ts_str,
                    'Task_Status_Type_Cd':    status_type_cd,
                    'Task_Status_Reason_Cd':  int(rng.integers(1, 5)),
                    'Task_Status_Txt':        None,
                })

                if next_ts is not None:
                    ts_cursor = next_ts

            # TASK_ACTIVITY + TASK_ACTIVITY_STATUS
            n_act = int(rng.integers(1, 4))
            for i in range(n_act):
                act_id = ctx.ids.next('activity')
                act_start = base_ts + timedelta(
                    minutes=int(rng.integers(0, 121)) + i * 60
                )
                duration_min = int(rng.integers(5, 31))
                act_end = act_start + timedelta(minutes=duration_min)
                act_text_idx = int(rng.integers(0, len(_ACTIVITY_TEXTS)))

                act_rows.append({
                    'Activity_Id':         act_id,
                    'Task_Id':             task_id,
                    'Activity_Type_Cd':    int(rng.integers(1, 6)),
                    'Activity_Txt':        _ACTIVITY_TEXTS[act_text_idx],
                    'Activity_Channel_Id': int(rng.choice(channel_ids)),
                    'Activity_Start_Dttm': format_ts(act_start),
                    'Activity_End_Dttm':   format_ts(act_end),
                })

                act_status_rows.append({
                    'Activity_Id':                act_id,
                    'Activity_Status_Start_Dttm': format_ts(act_start),
                    'Activity_Status_End_Dttm':   HIGH_TS,
                    'Activity_Status_Type_Cd':    int(rng.integers(1, 3)),
                    'Activity_Status_Reason_Cd':  int(rng.integers(1, 4)),
                    'Activity_Status_Txt':        None,
                })

        df_pt  = pd.DataFrame(task_rows,       columns=_COLS_PARTY_TASK)
        df_pts = pd.DataFrame(status_rows,     columns=_COLS_PARTY_TASK_STATUS)
        df_ta  = pd.DataFrame(act_rows,        columns=_COLS_TASK_ACTIVITY)
        df_tas = pd.DataFrame(act_status_rows, columns=_COLS_TASK_ACTIVITY_STATUS)

        # Int64 coercions — all *_Id and SMALLINT columns (BIGINT per PRD §7.1)
        for col in ['Task_Id', 'Party_Id', 'Source_Event_Id',
                    'Task_Activity_Type_Cd', 'Task_Subtype_Cd', 'Task_Reason_Cd']:
            df_pt[col] = df_pt[col].astype('Int64')

        for col in ['Task_Status_Id', 'Task_Id',
                    'Task_Status_Type_Cd', 'Task_Status_Reason_Cd']:
            df_pts[col] = df_pts[col].astype('Int64')

        for col in ['Activity_Id', 'Task_Id', 'Activity_Type_Cd', 'Activity_Channel_Id']:
            df_ta[col] = df_ta[col].astype('Int64')

        for col in ['Activity_Id', 'Activity_Status_Type_Cd', 'Activity_Status_Reason_Cd']:
            df_tas[col] = df_tas[col].astype('Int64')

        return {
            _PARTY_TASK_KEY:           self.stamp_di(df_pt,  start_ts=_TIER13_DI_START_TS),
            _PARTY_TASK_STATUS_KEY:    self.stamp_di(df_pts, start_ts=_TIER13_DI_START_TS),
            _TASK_ACTIVITY_KEY:        self.stamp_di(df_ta,  start_ts=_TIER13_DI_START_TS),
            _TASK_ACTIVITY_STATUS_KEY: self.stamp_di(df_tas, start_ts=_TIER13_DI_START_TS),
        }

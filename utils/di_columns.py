from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path
from typing import Tuple, Union

import pandas as pd

try:
    from config.settings import HIGH_DATE, HIGH_TS
    from utils.date_utils import format_date, format_ts
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from config.settings import HIGH_DATE, HIGH_TS
    from utils.date_utils import format_date, format_ts

DI_COLUMN_ORDER: Tuple[str, ...] = (
    'di_data_src_cd',
    'di_start_ts',
    'di_proc_name',
    'di_rec_deleted_Ind',
    'di_end_ts',
)

VALID_COLUMN_ORDER: Tuple[str, ...] = (
    'Valid_From_Dt',
    'Valid_To_Dt',
    'Del_Ind',
)


def stamp_di(
    df: pd.DataFrame,
    start_ts: Union[str, datetime],
    end_ts: Union[str, datetime] = HIGH_TS,
    deleted: str = 'N',
) -> pd.DataFrame:
    """Append the 5 DI metadata columns to *df* in canonical order.

    Operates on a copy; returns the modified copy.
    di_data_src_cd and di_proc_name are NULL (None) per PRD §7.3 / Q5c.
    """
    df = df.copy()
    df['di_data_src_cd'] = None
    df['di_start_ts'] = start_ts if isinstance(start_ts, str) else format_ts(start_ts)
    df['di_proc_name'] = None
    df['di_rec_deleted_Ind'] = deleted
    df['di_end_ts'] = end_ts if isinstance(end_ts, str) else format_ts(end_ts)
    return df


def stamp_valid(
    df: pd.DataFrame,
    from_dt: Union[str, date],
    to_dt: Union[str, date] = HIGH_DATE,
    del_ind: str = 'N',
) -> pd.DataFrame:
    """Append the 3 Valid_* / Del_Ind columns to *df* in canonical order.

    Only called for CDM_DB and PIM_DB tables per PRD §7.3.
    Operates on a copy; returns the modified copy.
    """
    df = df.copy()
    df['Valid_From_Dt'] = from_dt if isinstance(from_dt, str) else format_date(from_dt)
    df['Valid_To_Dt'] = to_dt if isinstance(to_dt, str) else format_date(to_dt)
    df['Del_Ind'] = del_ind
    return df


if __name__ == '__main__':
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    import pandas as pd

    base_df = pd.DataFrame({'col_a': [1, 2, 3], 'col_b': ['x', 'y', 'z']})

    # (a) stamp_di appends exactly 5 new columns in DI_COLUMN_ORDER
    stamped = stamp_di(base_df, start_ts='2026-01-01 00:00:00.000000')
    new_cols = list(stamped.columns[-5:])
    assert new_cols == list(DI_COLUMN_ORDER), f"DI cols: {new_cols}"
    assert len(stamped) == 3

    # (b) Default di_end_ts == HIGH_TS
    assert all(stamped['di_end_ts'] == HIGH_TS), "di_end_ts mismatch"

    # (c) Default di_rec_deleted_Ind == 'N'
    assert all(stamped['di_rec_deleted_Ind'] == 'N'), "di_rec_deleted_Ind mismatch"

    # (d) di_data_src_cd and di_proc_name are NaN/None
    assert stamped['di_data_src_cd'].isna().all(), "di_data_src_cd should be null"
    assert stamped['di_proc_name'].isna().all(), "di_proc_name should be null"

    # (e) stamp_valid appends exactly 3 columns in VALID_COLUMN_ORDER with defaults
    stamped_v = stamp_valid(base_df, from_dt='2025-10-01')
    new_vcols = list(stamped_v.columns[-3:])
    assert new_vcols == list(VALID_COLUMN_ORDER), f"Valid cols: {new_vcols}"
    assert all(stamped_v['Valid_To_Dt'] == HIGH_DATE), "Valid_To_Dt mismatch"
    assert all(stamped_v['Del_Ind'] == 'N'), "Del_Ind mismatch"

    # (f) stamp_di then stamp_valid leaves DI cols first, then Valid cols (at end)
    both = stamp_valid(stamp_di(base_df, start_ts='2026-01-01 00:00:00.000000'),
                       from_dt='2025-10-01')
    tail_8 = list(both.columns[-8:])
    assert tail_8[:5] == list(DI_COLUMN_ORDER), f"DI order in combined: {tail_8}"
    assert tail_8[5:] == list(VALID_COLUMN_ORDER), f"Valid order in combined: {tail_8}"

    print('di_columns OK')

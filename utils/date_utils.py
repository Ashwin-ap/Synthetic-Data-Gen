from __future__ import annotations

import calendar
import sys
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional, Tuple, Union

import numpy as np

try:
    from config.settings import HIGH_DATE, HIGH_TS, HISTORY_START, SIM_DATE
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from config.settings import HIGH_DATE, HIGH_TS, HISTORY_START, SIM_DATE


def history_start() -> date:
    return HISTORY_START


def sim_date() -> date:
    return SIM_DATE


def is_active(v: Optional[Union[str, date, datetime]]) -> bool:
    """Return True when *v* represents an open/active record sentinel."""
    if v is None:
        return True
    if isinstance(v, str):
        return v in (HIGH_TS, HIGH_DATE)
    if isinstance(v, datetime):
        return False
    if isinstance(v, date):
        return False
    return False


def month_snapshots(
    start: date, end: date
) -> List[Tuple[date, date]]:
    """Return (month_start, month_end) tuples spanning [start, end].

    The first tuple's start == *start*; the last tuple's end == *end*.
    Intermediate month boundaries follow calendar month edges.
    """
    snapshots: List[Tuple[date, date]] = []
    cur_start = start
    while cur_start <= end:
        y, m = cur_start.year, cur_start.month
        last_day = calendar.monthrange(y, m)[1]
        cur_end = date(y, m, last_day)
        if cur_end >= end:
            cur_end = end
        snapshots.append((cur_start, cur_end))
        if cur_end >= end:
            break
        # Advance to first day of next month
        if m == 12:
            cur_start = date(y + 1, 1, 1)
        else:
            cur_start = date(y, m + 1, 1)
    return snapshots


def random_datetime_between(
    start: Union[date, datetime],
    end: Union[date, datetime],
    rng: np.random.Generator,
) -> datetime:
    """Return a uniform random datetime in the closed interval [start, end]."""
    if isinstance(start, date) and not isinstance(start, datetime):
        start = datetime(start.year, start.month, start.day)
    if isinstance(end, date) and not isinstance(end, datetime):
        end = datetime(end.year, end.month, end.day, 23, 59, 59)
    delta_s = (end - start).total_seconds()
    offset_s = rng.uniform(0, delta_s)
    from datetime import timedelta
    return start + timedelta(seconds=offset_s)


def random_date_between(
    start: date,
    end: date,
    rng: np.random.Generator,
) -> date:
    """Return a uniform random date in the closed interval [start, end]."""
    delta_days = (end - start).days
    offset = int(rng.integers(0, delta_days + 1))
    from datetime import timedelta
    return start + timedelta(days=offset)


def format_ts(ts: Optional[Union[str, datetime]]) -> str:
    """Render *ts* as 'YYYY-MM-DD HH:MM:SS.ffffff'; None → HIGH_TS."""
    if ts is None or ts == HIGH_TS:
        return HIGH_TS
    if isinstance(ts, str):
        return ts
    return ts.strftime('%Y-%m-%d %H:%M:%S.%f')


def format_date(dt: Optional[Union[str, date]]) -> str:
    """Render *dt* as 'YYYY-MM-DD'; None → HIGH_DATE."""
    if dt is None or dt == HIGH_DATE:
        return HIGH_DATE
    if isinstance(dt, str):
        return dt
    return dt.strftime('%Y-%m-%d')


if __name__ == '__main__':
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    import numpy as np

    rng = np.random.default_rng(42)

    # (a) month_snapshots returns exactly 6 tuples for Oct 2025 – Mar 2026
    snaps = month_snapshots(HISTORY_START, SIM_DATE)
    assert len(snaps) == 6, f"Expected 6 snapshots, got {len(snaps)}: {snaps}"

    # Verify month boundaries
    expected_starts = [
        date(2025, 10, 1), date(2025, 11, 1), date(2025, 12, 1),
        date(2026, 1, 1),  date(2026, 2, 1),  date(2026, 3, 1),
    ]
    for i, (s, e) in enumerate(snaps):
        assert s == expected_starts[i], f"Snap {i} start: {s} != {expected_starts[i]}"

    # (b) Last tuple's end equals SIM_DATE
    assert snaps[-1][1] == SIM_DATE, f"Last snap end: {snaps[-1][1]} != {SIM_DATE}"

    # (c) is_active with HIGH_TS, HIGH_DATE, None → True
    assert is_active(HIGH_TS), "HIGH_TS not active"
    assert is_active(HIGH_DATE), "HIGH_DATE not active"
    assert is_active(None), "None not active"

    # (d) is_active with a real datetime → False
    assert not is_active(datetime(2025, 12, 31)), "Real datetime should not be active"

    # (e) format_ts(None) == HIGH_TS
    assert format_ts(None) == HIGH_TS, f"format_ts(None) = {format_ts(None)!r}"

    # (f) format_date(None) == HIGH_DATE
    assert format_date(None) == HIGH_DATE, f"format_date(None) = {format_date(None)!r}"

    # (g) random_datetime_between returns datetime in closed interval for 1000 samples
    start_dt = datetime(HISTORY_START.year, HISTORY_START.month, HISTORY_START.day)
    end_dt = datetime(SIM_DATE.year, SIM_DATE.month, SIM_DATE.day, 23, 59, 59)
    for _ in range(1000):
        dt = random_datetime_between(HISTORY_START, SIM_DATE, rng)
        assert isinstance(dt, datetime), f"Not a datetime: {dt!r}"
        assert start_dt <= dt <= end_dt, f"Out of range: {dt}"

    print('date_utils OK')

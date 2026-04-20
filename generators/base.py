from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict

import pandas as pd

try:
    from config.settings import GENERATION_TS, HIGH_DATE, HIGH_TS
    from utils.di_columns import stamp_di as _stamp_di
    from utils.di_columns import stamp_valid as _stamp_valid
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from config.settings import GENERATION_TS, HIGH_DATE, HIGH_TS
    from utils.di_columns import stamp_di as _stamp_di
    from utils.di_columns import stamp_valid as _stamp_valid


class BaseGenerator:
    """Abstract base class for all tier generators.

    Subclasses override generate() to produce a dict of DataFrames keyed
    'Schema.TABLE_NAME'. DI column stamping is delegated here so every tier
    gets identical, correctly-ordered metadata columns with zero boilerplate.
    """

    def stamp_di(
        self,
        df: pd.DataFrame,
        start_ts=None,
        end_ts: str = HIGH_TS,
        deleted: str = 'N',
    ) -> pd.DataFrame:
        """Stamp the 5 DI metadata columns onto *df*.

        If *start_ts* is None, uses GENERATION_TS — a deterministic SIM_DATE-derived
        constant — so reruns produce byte-identical CSVs (PRD §7.6).
        Delegates to utils.di_columns.stamp_di.
        """
        if start_ts is None:
            start_ts = GENERATION_TS
        return _stamp_di(df, start_ts=start_ts, end_ts=end_ts, deleted=deleted)

    def stamp_valid(
        self,
        df: pd.DataFrame,
        from_dt=None,
        to_dt: str = HIGH_DATE,
        del_ind: str = 'N',
    ) -> pd.DataFrame:
        """Stamp the 3 Valid_*/Del_Ind columns onto *df* (CDM_DB/PIM_DB only).

        Delegates to utils.di_columns.stamp_valid.
        """
        effective_from = from_dt if from_dt is not None else ''
        return _stamp_valid(df, from_dt=effective_from, to_dt=to_dt, del_ind=del_ind)

    def generate(self, ctx) -> Dict[str, pd.DataFrame]:
        """Generate and return a dict of DataFrames keyed 'Schema.TABLE'.

        Must be overridden by every tier subclass.
        """
        raise NotImplementedError(
            f'{type(self).__name__}.generate() is abstract — override in subclass'
        )

from typing import Dict

import pandas as pd

from config.code_values import AGREEMENT_STATUS_SCHEMES, FROZEN_STATUS_ROW

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}

_COLS = [
    'Agreement_Status_Scheme_Cd',
    'Agreement_Status_Cd',
    'Agreement_Status_Desc',
    'di_start_ts',
    'di_end_ts',
    'di_rec_deleted_Ind',
]

_STATUS_ROWS = [
    # Account Status
    {'Agreement_Status_Scheme_Cd': 'Account Status', 'Agreement_Status_Cd': 'OPEN',     'Agreement_Status_Desc': 'Open',     **_DI},
    {'Agreement_Status_Scheme_Cd': 'Account Status', 'Agreement_Status_Cd': 'CLOSED',   'Agreement_Status_Desc': 'Closed',   **_DI},
    {'Agreement_Status_Scheme_Cd': 'Account Status', 'Agreement_Status_Cd': 'DORMANT',  'Agreement_Status_Desc': 'Dormant',  **_DI},
    {'Agreement_Status_Scheme_Cd': 'Account Status', 'Agreement_Status_Cd': 'WRITE_OFF','Agreement_Status_Desc': 'Write Off', **_DI},
    # Accrual Status
    {'Agreement_Status_Scheme_Cd': 'Accrual Status', 'Agreement_Status_Cd': 'ACCRUING',     'Agreement_Status_Desc': 'Accruing',     **_DI},
    {'Agreement_Status_Scheme_Cd': 'Accrual Status', 'Agreement_Status_Cd': 'NON_ACCRUING', 'Agreement_Status_Desc': 'Non Accruing', **_DI},
    # Default Status
    {'Agreement_Status_Scheme_Cd': 'Default Status', 'Agreement_Status_Cd': 'CURRENT', 'Agreement_Status_Desc': 'Current', **_DI},
    {'Agreement_Status_Scheme_Cd': 'Default Status', 'Agreement_Status_Cd': 'DEFAULT', 'Agreement_Status_Desc': 'Default', **_DI},
    {'Agreement_Status_Scheme_Cd': 'Default Status', 'Agreement_Status_Cd': 'CURED',   'Agreement_Status_Desc': 'Cured',   **_DI},
    # Drawn Undrawn Status
    {'Agreement_Status_Scheme_Cd': 'Drawn Undrawn Status', 'Agreement_Status_Cd': 'DRAWN',   'Agreement_Status_Desc': 'Drawn',   **_DI},
    {'Agreement_Status_Scheme_Cd': 'Drawn Undrawn Status', 'Agreement_Status_Cd': 'UNDRAWN', 'Agreement_Status_Desc': 'Undrawn', **_DI},
    {'Agreement_Status_Scheme_Cd': 'Drawn Undrawn Status', 'Agreement_Status_Cd': 'PARTIAL', 'Agreement_Status_Desc': 'Partial', **_DI},
    # Frozen Status — FROZEN row must match FROZEN_STATUS_ROW exactly; desc='Frozen' is the Layer 2 literal match
    {**FROZEN_STATUS_ROW, **_DI},
    {'Agreement_Status_Scheme_Cd': 'Frozen Status', 'Agreement_Status_Cd': 'NOT_FROZEN', 'Agreement_Status_Desc': 'Not Frozen', **_DI},
    # Past Due Status
    {'Agreement_Status_Scheme_Cd': 'Past Due Status', 'Agreement_Status_Cd': 'CURRENT',  'Agreement_Status_Desc': 'Current',          **_DI},
    {'Agreement_Status_Scheme_Cd': 'Past Due Status', 'Agreement_Status_Cd': 'DPD_30',   'Agreement_Status_Desc': '30 Days Past Due',  **_DI},
    {'Agreement_Status_Scheme_Cd': 'Past Due Status', 'Agreement_Status_Cd': 'DPD_60',   'Agreement_Status_Desc': '60 Days Past Due',  **_DI},
    {'Agreement_Status_Scheme_Cd': 'Past Due Status', 'Agreement_Status_Cd': 'DPD_90',   'Agreement_Status_Desc': '90 Days Past Due',  **_DI},
    {'Agreement_Status_Scheme_Cd': 'Past Due Status', 'Agreement_Status_Cd': 'DPD_120',  'Agreement_Status_Desc': '120 Days Past Due', **_DI},
]


def get_status_type_tables() -> Dict[str, pd.DataFrame]:
    return {
        'Core_DB.AGREEMENT_STATUS_TYPE': pd.DataFrame(_STATUS_ROWS, columns=_COLS),
    }

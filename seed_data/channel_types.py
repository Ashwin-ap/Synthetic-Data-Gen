from typing import Dict
import pandas as pd

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}

# ── CHANNEL_TYPE ──
_cols_channel_type = [
    'Channel_Type_Cd', 'Channel_Processing_Cd', 'Channel_Type_Name', 'Channel_Type_Desc',
    'Channel_Type_Start_Dt', 'Channel_Type_End_Dt', 'Parent_Channel_Type_Cd',
    'Channel_Type_Subtype_Cd',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_channel_type_rows = [
    {'Channel_Type_Cd': 'BRANCH',       'Channel_Processing_Cd': None, 'Channel_Type_Name': 'Branch',       'Channel_Type_Desc': 'Physical branch location',          'Channel_Type_Start_Dt': None, 'Channel_Type_End_Dt': None, 'Parent_Channel_Type_Cd': None, 'Channel_Type_Subtype_Cd': None, **_DI},
    {'Channel_Type_Cd': 'ATM',          'Channel_Processing_Cd': None, 'Channel_Type_Name': 'ATM',           'Channel_Type_Desc': 'Automated teller machine',          'Channel_Type_Start_Dt': None, 'Channel_Type_End_Dt': None, 'Parent_Channel_Type_Cd': None, 'Channel_Type_Subtype_Cd': None, **_DI},
    {'Channel_Type_Cd': 'ONLINE',       'Channel_Processing_Cd': None, 'Channel_Type_Name': 'Online Banking','Channel_Type_Desc': 'Web-based online banking portal',   'Channel_Type_Start_Dt': None, 'Channel_Type_End_Dt': None, 'Parent_Channel_Type_Cd': None, 'Channel_Type_Subtype_Cd': None, **_DI},
    {'Channel_Type_Cd': 'MOBILE',       'Channel_Processing_Cd': None, 'Channel_Type_Name': 'Mobile Banking','Channel_Type_Desc': 'Mobile application banking',        'Channel_Type_Start_Dt': None, 'Channel_Type_End_Dt': None, 'Parent_Channel_Type_Cd': None, 'Channel_Type_Subtype_Cd': None, **_DI},
    {'Channel_Type_Cd': 'CALL_CENTER',  'Channel_Processing_Cd': None, 'Channel_Type_Name': 'Call Center',   'Channel_Type_Desc': 'Telephone banking call center',     'Channel_Type_Start_Dt': None, 'Channel_Type_End_Dt': None, 'Parent_Channel_Type_Cd': None, 'Channel_Type_Subtype_Cd': None, **_DI},
    {'Channel_Type_Cd': 'EMAIL',        'Channel_Processing_Cd': None, 'Channel_Type_Name': 'Email',         'Channel_Type_Desc': 'Electronic mail communications',    'Channel_Type_Start_Dt': None, 'Channel_Type_End_Dt': None, 'Parent_Channel_Type_Cd': None, 'Channel_Type_Subtype_Cd': None, **_DI},
]

# ── CHANNEL_INSTANCE_SUBTYPE ──
_cols_channel_instance_subtype = [
    'Channel_Instance_Subtype_Cd', 'Channel_Instance_Subtype_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_channel_instance_subtype_rows = [
    {'Channel_Instance_Subtype_Cd': 'MAIN_BRANCH',       'Channel_Instance_Subtype_Desc': 'Main Branch',              **_DI},
    {'Channel_Instance_Subtype_Cd': 'DRIVE_THRU_ATM',    'Channel_Instance_Subtype_Desc': 'Drive-Through ATM',        **_DI},
    {'Channel_Instance_Subtype_Cd': 'WEB_PORTAL',        'Channel_Instance_Subtype_Desc': 'Web Portal',               **_DI},
    {'Channel_Instance_Subtype_Cd': 'IOS_APP',           'Channel_Instance_Subtype_Desc': 'iOS Mobile Application',   **_DI},
    {'Channel_Instance_Subtype_Cd': 'ANDROID_APP',       'Channel_Instance_Subtype_Desc': 'Android Mobile Application', **_DI},
    {'Channel_Instance_Subtype_Cd': 'INBOUND_CALL',      'Channel_Instance_Subtype_Desc': 'Inbound Call Center',      **_DI},
    {'Channel_Instance_Subtype_Cd': 'OUTBOUND_CALL',     'Channel_Instance_Subtype_Desc': 'Outbound Call Center',     **_DI},
]

# ── CONVENIENCE_FACTOR_TYPE ──
_cols_convenience_factor_type = [
    'Convenience_Factor_Cd', 'Convenience_Factor_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_convenience_factor_type_rows = [
    {'Convenience_Factor_Cd': '24_7_AVAILABLE',       'Convenience_Factor_Desc': '24/7 Available',         **_DI},
    {'Convenience_Factor_Cd': 'BUSINESS_HOURS',       'Convenience_Factor_Desc': 'Business Hours Only',    **_DI},
    {'Convenience_Factor_Cd': 'APPOINTMENT_REQUIRED', 'Convenience_Factor_Desc': 'Appointment Required',   **_DI},
    {'Convenience_Factor_Cd': 'SELF_SERVICE',         'Convenience_Factor_Desc': 'Self Service',           **_DI},
    {'Convenience_Factor_Cd': 'ASSISTED',             'Convenience_Factor_Desc': 'Assisted Service',       **_DI},
]

# ── CHANNEL_STATUS_TYPE ──
_cols_channel_status_type = [
    'Channel_Status_Cd', 'Channel_Status_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_channel_status_type_rows = [
    {'Channel_Status_Cd': 'ACTIVE',      'Channel_Status_Desc': 'Active',       **_DI},
    {'Channel_Status_Cd': 'INACTIVE',    'Channel_Status_Desc': 'Inactive',     **_DI},
    {'Channel_Status_Cd': 'MAINTENANCE', 'Channel_Status_Desc': 'Maintenance',  **_DI},
    {'Channel_Status_Cd': 'DEPRECATED',  'Channel_Status_Desc': 'Deprecated',   **_DI},
]


def get_channel_type_tables() -> Dict[str, pd.DataFrame]:
    return {
        'Core_DB.CHANNEL_TYPE':            pd.DataFrame(_channel_type_rows,            columns=_cols_channel_type),
        'Core_DB.CHANNEL_INSTANCE_SUBTYPE': pd.DataFrame(_channel_instance_subtype_rows, columns=_cols_channel_instance_subtype),
        'Core_DB.CONVENIENCE_FACTOR_TYPE': pd.DataFrame(_convenience_factor_type_rows, columns=_cols_convenience_factor_type),
        'Core_DB.CHANNEL_STATUS_TYPE':     pd.DataFrame(_channel_status_type_rows,     columns=_cols_channel_status_type),
    }

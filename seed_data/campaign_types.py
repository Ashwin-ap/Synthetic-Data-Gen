from typing import Dict
import pandas as pd

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}

# ── CAMPAIGN_STRATEGY_TYPE ──
_cols_campaign_strategy_type = [
    'Campaign_Strategy_Cd', 'Campaign_Strategy_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_campaign_strategy_type_rows = [
    {'Campaign_Strategy_Cd': 'ACQUISITION',     'Campaign_Strategy_Desc': 'Acquisition',      **_DI},
    {'Campaign_Strategy_Cd': 'RETENTION',       'Campaign_Strategy_Desc': 'Retention',         **_DI},
    {'Campaign_Strategy_Cd': 'CROSS_SELL',      'Campaign_Strategy_Desc': 'Cross Sell',        **_DI},
    {'Campaign_Strategy_Cd': 'UP_SELL',         'Campaign_Strategy_Desc': 'Up Sell',           **_DI},
    {'Campaign_Strategy_Cd': 'WIN_BACK',        'Campaign_Strategy_Desc': 'Win Back',          **_DI},
    {'Campaign_Strategy_Cd': 'BRAND_AWARENESS', 'Campaign_Strategy_Desc': 'Brand Awareness',   **_DI},
]

# ── CAMPAIGN_TYPE ──
_cols_campaign_type = [
    'Campaign_Type_Cd', 'Campaign_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_campaign_type_rows = [
    {'Campaign_Type_Cd': 'DIRECT_MAIL',    'Campaign_Type_Desc': 'Direct Mail',       **_DI},
    {'Campaign_Type_Cd': 'EMAIL',          'Campaign_Type_Desc': 'Email',             **_DI},
    {'Campaign_Type_Cd': 'DIGITAL_ADS',    'Campaign_Type_Desc': 'Digital Ads',       **_DI},
    {'Campaign_Type_Cd': 'SOCIAL_MEDIA',   'Campaign_Type_Desc': 'Social Media',      **_DI},
    {'Campaign_Type_Cd': 'BRANCH_EVENT',   'Campaign_Type_Desc': 'Branch Event',      **_DI},
    {'Campaign_Type_Cd': 'TELEMARKETING',  'Campaign_Type_Desc': 'Telemarketing',     **_DI},
]

# ── CAMPAIGN_CLASSIFICATION ──
_cols_campaign_classification = [
    'Campaign_Classification_Cd', 'Campaign_Classification_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_campaign_classification_rows = [
    {'Campaign_Classification_Cd': 'PROSPECT',        'Campaign_Classification_Desc': 'Prospect',         **_DI},
    {'Campaign_Classification_Cd': 'CUSTOMER',        'Campaign_Classification_Desc': 'Customer',         **_DI},
    {'Campaign_Classification_Cd': 'LAPSED_CUSTOMER', 'Campaign_Classification_Desc': 'Lapsed Customer',  **_DI},
    {'Campaign_Classification_Cd': 'HIGH_VALUE',      'Campaign_Classification_Desc': 'High Value',       **_DI},
    {'Campaign_Classification_Cd': 'MASS_MARKET',     'Campaign_Classification_Desc': 'Mass Market',      **_DI},
]

# ── CAMPAIGN_STATUS_TYPE ──
_cols_campaign_status_type = [
    'Campaign_Status_Cd', 'Campaign_Status_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_campaign_status_type_rows = [
    {'Campaign_Status_Cd': 'PLANNED',    'Campaign_Status_Desc': 'Planned',    **_DI},
    {'Campaign_Status_Cd': 'ACTIVE',     'Campaign_Status_Desc': 'Active',     **_DI},
    {'Campaign_Status_Cd': 'PAUSED',     'Campaign_Status_Desc': 'Paused',     **_DI},
    {'Campaign_Status_Cd': 'COMPLETED',  'Campaign_Status_Desc': 'Completed',  **_DI},
    {'Campaign_Status_Cd': 'CANCELLED',  'Campaign_Status_Desc': 'Cancelled',  **_DI},
]

# ── PROMOTION_OFFER_TYPE ── (Promotion_Offer_Type_Desc is NOT NULL per DDL)
_cols_promotion_offer_type = [
    'Promotion_Offer_Type_Cd', 'Promotion_Offer_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_promotion_offer_type_rows = [
    {'Promotion_Offer_Type_Cd': 'DISCOUNT',          'Promotion_Offer_Type_Desc': 'Discount',           **_DI},
    {'Promotion_Offer_Type_Cd': 'RATE_REDUCTION',    'Promotion_Offer_Type_Desc': 'Rate Reduction',     **_DI},
    {'Promotion_Offer_Type_Cd': 'FEE_WAIVER',        'Promotion_Offer_Type_Desc': 'Fee Waiver',         **_DI},
    {'Promotion_Offer_Type_Cd': 'CASH_BONUS',        'Promotion_Offer_Type_Desc': 'Cash Bonus',         **_DI},
    {'Promotion_Offer_Type_Cd': 'POINTS_MULTIPLIER', 'Promotion_Offer_Type_Desc': 'Points Multiplier',  **_DI},
    {'Promotion_Offer_Type_Cd': 'FREE_SERVICE',      'Promotion_Offer_Type_Desc': 'Free Service',       **_DI},
]

# ── PROMOTION_METRIC_TYPE ──
_cols_promotion_metric_type = [
    'Promotion_Metric_Type_Cd', 'Promotion_Metric_Type_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_promotion_metric_type_rows = [
    {'Promotion_Metric_Type_Cd': 'CONVERSION_RATE',   'Promotion_Metric_Type_Desc': 'Conversion Rate',    **_DI},
    {'Promotion_Metric_Type_Cd': 'RESPONSE_RATE',     'Promotion_Metric_Type_Desc': 'Response Rate',      **_DI},
    {'Promotion_Metric_Type_Cd': 'REDEMPTION_RATE',   'Promotion_Metric_Type_Desc': 'Redemption Rate',    **_DI},
    {'Promotion_Metric_Type_Cd': 'CLICK_THROUGH',     'Promotion_Metric_Type_Desc': 'Click Through Rate', **_DI},
    {'Promotion_Metric_Type_Cd': 'ACQUISITION_COST',  'Promotion_Metric_Type_Desc': 'Acquisition Cost',   **_DI},
]


def get_campaign_type_tables() -> Dict[str, pd.DataFrame]:
    return {
        'Core_DB.CAMPAIGN_STRATEGY_TYPE':  pd.DataFrame(_campaign_strategy_type_rows,  columns=_cols_campaign_strategy_type),
        'Core_DB.CAMPAIGN_TYPE':           pd.DataFrame(_campaign_type_rows,            columns=_cols_campaign_type),
        'Core_DB.CAMPAIGN_CLASSIFICATION': pd.DataFrame(_campaign_classification_rows,  columns=_cols_campaign_classification),
        'Core_DB.CAMPAIGN_STATUS_TYPE':    pd.DataFrame(_campaign_status_type_rows,     columns=_cols_campaign_status_type),
        'Core_DB.PROMOTION_OFFER_TYPE':    pd.DataFrame(_promotion_offer_type_rows,     columns=_cols_promotion_offer_type),
        'Core_DB.PROMOTION_METRIC_TYPE':   pd.DataFrame(_promotion_metric_type_rows,    columns=_cols_promotion_metric_type),
    }

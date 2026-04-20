from typing import Dict

import pandas as pd

from config.code_values import ORIGINAL_LOAN_TERM_CLASSIFICATION_CD, RATE_FEATURE_SUBTYPE_CD

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}


def get_feature_type_tables() -> Dict[str, pd.DataFrame]:
    # Rate Feature must be first to make it easy to locate; desc preserves the Layer 2 literal string
    feature_subtypes = [
        {'Feature_Subtype_Cd': RATE_FEATURE_SUBTYPE_CD,  'Feature_Subtype_Desc': 'Rate Feature',      **_DI},
        {'Feature_Subtype_Cd': 'Fee Feature',             'Feature_Subtype_Desc': 'Fee Feature',       **_DI},
        {'Feature_Subtype_Cd': 'Term Feature',            'Feature_Subtype_Desc': 'Term Feature',      **_DI},
        {'Feature_Subtype_Cd': 'Balance Feature',         'Feature_Subtype_Desc': 'Balance Feature',   **_DI},
        {'Feature_Subtype_Cd': 'Reward Feature',          'Feature_Subtype_Desc': 'Reward Feature',    **_DI},
        {'Feature_Subtype_Cd': 'Insurance Feature',       'Feature_Subtype_Desc': 'Insurance Feature', **_DI},
        {'Feature_Subtype_Cd': 'Payment Feature',         'Feature_Subtype_Desc': 'Payment Feature',   **_DI},
    ]

    insurance_subtypes = [
        {'Feature_Insurance_Subtype_Cd': 'LIFE',         'Feature_Insurance_Subtype_Desc': 'Life',         **_DI},
        {'Feature_Insurance_Subtype_Cd': 'DISABILITY',   'Feature_Insurance_Subtype_Desc': 'Disability',   **_DI},
        {'Feature_Insurance_Subtype_Cd': 'UNEMPLOYMENT', 'Feature_Insurance_Subtype_Desc': 'Unemployment', **_DI},
        {'Feature_Insurance_Subtype_Cd': 'PROPERTY',     'Feature_Insurance_Subtype_Desc': 'Property',     **_DI},
        {'Feature_Insurance_Subtype_Cd': 'CREDIT',       'Feature_Insurance_Subtype_Desc': 'Credit',       **_DI},
    ]

    # Original Loan Term must be present; desc preserves the Layer 2 literal string
    classification_types = [
        {'Feature_Classification_Cd': ORIGINAL_LOAN_TERM_CLASSIFICATION_CD, 'Feature_Classification_Desc': 'Original Loan Term', **_DI},
        {'Feature_Classification_Cd': 'Current Rate',       'Feature_Classification_Desc': 'Current Rate',       **_DI},
        {'Feature_Classification_Cd': 'Origination Rate',   'Feature_Classification_Desc': 'Origination Rate',   **_DI},
        {'Feature_Classification_Cd': 'Minimum Balance',    'Feature_Classification_Desc': 'Minimum Balance',    **_DI},
        {'Feature_Classification_Cd': 'Maximum Balance',    'Feature_Classification_Desc': 'Maximum Balance',    **_DI},
        {'Feature_Classification_Cd': 'Minimum Payment',    'Feature_Classification_Desc': 'Minimum Payment',    **_DI},
        {'Feature_Classification_Cd': 'Maturity Date',      'Feature_Classification_Desc': 'Maturity Date',      **_DI},
    ]

    _cols_subtype        = ['Feature_Subtype_Cd',           'Feature_Subtype_Desc',           'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_ins_subtype    = ['Feature_Insurance_Subtype_Cd', 'Feature_Insurance_Subtype_Desc', 'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']
    _cols_classification = ['Feature_Classification_Cd',   'Feature_Classification_Desc',    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']

    return {
        'Core_DB.FEATURE_SUBTYPE':            pd.DataFrame(feature_subtypes,    columns=_cols_subtype),
        'Core_DB.FEATURE_INSURANCE_SUBTYPE':  pd.DataFrame(insurance_subtypes,  columns=_cols_ins_subtype),
        'Core_DB.FEATURE_CLASSIFICATION_TYPE':pd.DataFrame(classification_types, columns=_cols_classification),
    }

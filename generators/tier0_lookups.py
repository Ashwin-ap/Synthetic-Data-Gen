from __future__ import annotations

from typing import TYPE_CHECKING, Dict

import pandas as pd

from generators.base import BaseGenerator
from seed_data.agreement_types import get_agreement_type_tables
from seed_data.status_types import get_status_type_tables
from seed_data.financial_types import get_financial_type_tables
from seed_data.feature_types import get_feature_type_tables
from seed_data.party_types import get_party_type_tables
from seed_data.industry_codes import get_industry_code_tables
from seed_data.channel_types import get_channel_type_tables
from seed_data.campaign_types import get_campaign_type_tables
from seed_data.address_types import get_address_type_tables
from seed_data.currency import get_currency_tables
from seed_data.interest_rate_indices import get_interest_rate_index_tables
from seed_data.misc_types import get_misc_type_tables

if TYPE_CHECKING:
    from registry.context import GenerationContext

# Fixed order ensures deterministic duplicate detection across sessions.
_SEED_LOADERS = [
    get_agreement_type_tables,
    get_status_type_tables,
    get_financial_type_tables,
    get_feature_type_tables,
    get_party_type_tables,
    get_industry_code_tables,
    get_channel_type_tables,
    get_campaign_type_tables,
    get_address_type_tables,
    get_currency_tables,
    get_interest_rate_index_tables,
    get_misc_type_tables,
]

_DI_PLACEHOLDERS = ['di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind']


class Tier0Lookups(BaseGenerator):
    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        combined: Dict[str, pd.DataFrame] = {}
        for loader in _SEED_LOADERS:
            for key, df in loader().items():
                if key in combined:
                    raise ValueError(
                        f'Duplicate Tier 0 table key: {key} (authored in two seed modules)'
                    )
                for bad_col in ('di_data_src_cd', 'di_proc_name'):
                    if bad_col in df.columns:
                        raise ValueError(
                            f'{key}: unexpected column {bad_col!r} present before DI stamping'
                        )
                combined[key] = df

        stamped: Dict[str, pd.DataFrame] = {}
        for key, df in combined.items():
            df = df.drop(columns=_DI_PLACEHOLDERS)
            stamped[key] = self.stamp_di(df)
        return stamped

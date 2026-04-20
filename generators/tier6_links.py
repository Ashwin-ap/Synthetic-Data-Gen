"""Tier 6 — Links generator.

Produces Core_DB.PARTY_LOCATOR: one row per CustomerProfile linking every party to
their address with Locator_Usage_Type_Cd = 'physical_primary'.

The reserved self-employment placeholder ORGANIZATION (Organization_Party_Id = 9_999_999)
has no CustomerProfile entry and therefore receives no PARTY_LOCATOR row — correct by design.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict

import pandas as pd

from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

_TIER6_DI_START_TS = '2000-01-01 00:00:00.000000'

# Layer 2 filters on this exact string (mvp-tool-design.md §9 Tier 6).
_PRIMARY_LOCATOR_USAGE = 'physical_primary'

_COLS_PARTY_LOCATOR = [
    'Party_Id',
    'Locator_Id',
    'Locator_Usage_Type_Cd',
    'Party_Locator_Start_Dttm',
    'Party_Locator_End_Dttm',
    'Data_Quality_Cd',
]


class Tier6Links(BaseGenerator):
    """Generate Core_DB.PARTY_LOCATOR linking every party to their address."""

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # --- Guards ---
        if 'Core_DB.ADDRESS' not in ctx.tables:
            raise RuntimeError('Tier6Links requires Core_DB.ADDRESS — run Tier5Location first')
        if not ctx.customers:
            raise RuntimeError('Tier6Links requires ctx.customers — run UniverseBuilder.build() first')

        # --- Validate all customer address IDs resolve to ADDRESS pool ---
        valid_address_ids = set(ctx.tables['Core_DB.ADDRESS']['Address_Id'])
        for cp in ctx.customers:
            if cp.address_id not in valid_address_ids:
                raise ValueError(
                    f'CustomerProfile party_id={cp.party_id} has address_id={cp.address_id} '
                    f'which is not in Core_DB.ADDRESS pool'
                )

        # --- Build PARTY_LOCATOR (one row per CustomerProfile) ---
        rows = [
            {
                'Party_Id':                cp.party_id,
                'Locator_Id':              cp.address_id,
                'Locator_Usage_Type_Cd':   _PRIMARY_LOCATOR_USAGE,
                'Party_Locator_Start_Dttm': str(cp.party_since),
                'Party_Locator_End_Dttm':  None,
                'Data_Quality_Cd':         'verified',
            }
            for cp in ctx.customers
        ]
        df = pd.DataFrame(rows, columns=_COLS_PARTY_LOCATOR)
        df['Party_Id']   = df['Party_Id'].astype('Int64')
        df['Locator_Id'] = df['Locator_Id'].astype('Int64')

        df = self.stamp_di(df, start_ts=_TIER6_DI_START_TS)

        return {'Core_DB.PARTY_LOCATOR': df}

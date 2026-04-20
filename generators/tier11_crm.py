from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import TYPE_CHECKING, Dict, List, Tuple

import pandas as pd

from config.settings import HISTORY_START, SIM_DATE
from generators.base import BaseGenerator
from utils.date_utils import format_date, format_ts, random_date_between, random_datetime_between

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ---------------------------------------------------------------------------
# DI start timestamp
# ---------------------------------------------------------------------------
_TIER11_DI_START_TS = '2000-01-01 00:00:00.000000'

# ---------------------------------------------------------------------------
# Schema keys
# ---------------------------------------------------------------------------
_CAMPAIGN_STATUS_KEY  = 'Core_DB.CAMPAIGN_STATUS'
_PROMOTION_KEY        = 'Core_DB.PROMOTION'
_PROMOTION_OFFER_KEY  = 'Core_DB.PROMOTION_OFFER'

# ---------------------------------------------------------------------------
# Upstream table keys
# ---------------------------------------------------------------------------
_CAMPAIGN_KEY             = 'Core_DB.CAMPAIGN'
_CAMPAIGN_STATUS_TYPE_KEY = 'Core_DB.CAMPAIGN_STATUS_TYPE'
_CHANNEL_TYPE_KEY         = 'Core_DB.CHANNEL_TYPE'
_UNIT_OF_MEASURE_KEY      = 'Core_DB.UNIT_OF_MEASURE'
_PROMOTION_OFFER_TYPE_KEY = 'Core_DB.PROMOTION_OFFER_TYPE'

# ---------------------------------------------------------------------------
# Required upstream tables for guard
# ---------------------------------------------------------------------------
_REQUIRED_UPSTREAM = (
    _CAMPAIGN_KEY,
    _CAMPAIGN_STATUS_TYPE_KEY,
    _CHANNEL_TYPE_KEY,
    _UNIT_OF_MEASURE_KEY,
    _PROMOTION_OFFER_TYPE_KEY,
)

# ---------------------------------------------------------------------------
# Promotion type codes (free-form VARCHAR)
# ---------------------------------------------------------------------------
_PROMOTION_TYPES = ('acquisition', 'retention', 'cross-sell')

# ---------------------------------------------------------------------------
# Amount ranges (Decimal pairs — lo, hi inclusive)
# ---------------------------------------------------------------------------
_PROMO_COST_RANGE = (Decimal('100.0000'),    Decimal('50000.0000'))
_PROMO_GOAL_RANGE = (Decimal('500.0000'),  Decimal('200000.0000'))

# ---------------------------------------------------------------------------
# Column lists (business cols only; DI tail appended by stamp_di)
# Verified against references/07_mvp-schema-reference.md DDL
# ---------------------------------------------------------------------------
_COLS_CAMPAIGN_STATUS: List[str] = [
    'Campaign_Id', 'Campaign_Status_Start_Dttm', 'Campaign_Status_Cd',
    'Campaign_Status_End_Dttm',
]

_COLS_PROMOTION: List[str] = [
    'Promotion_Id', 'Promotion_Type_Cd', 'Campaign_Id', 'Promotion_Classification_Cd',
    'Channel_Type_Cd', 'Internal_Promotion_Name', 'Promotion_Desc',
    'Promotion_Objective_Txt', 'Promotion_Start_Dt', 'Promotion_End_Dt',
    'Promotion_Actual_Unit_Cost_Amt', 'Promotion_Goal_Amt', 'Currency_Cd',
    'Promotion_Actual_Unit_Cnt', 'Promotion_Break_Even_Order_Cnt', 'Unit_Of_Measure_Cd',
]

_COLS_PROMOTION_OFFER: List[str] = [
    'Promotion_Id', 'Promotion_Offer_Id', 'Promotion_Offer_Type_Cd',
    'Promotion_Offer_Desc', 'Ad_Id', 'Distribution_Start_Dt', 'Distribution_End_Dt',
    'Redemption_Start_Dt', 'Redemption_End_Dt',
]


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _draw_amount(rng, lo: Decimal, hi: Decimal) -> Decimal:
    raw = rng.uniform(float(lo), float(hi))
    return Decimal(str(raw)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------------------
# Generator class
# ---------------------------------------------------------------------------

class Tier11CRM(BaseGenerator):

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        for key in _REQUIRED_UPSTREAM:
            if key not in ctx.tables:
                raise RuntimeError(f'Tier 11 prerequisite missing: {key}')

        # Build lookup lists from upstream seed tables
        status_codes: List[str] = ctx.tables[_CAMPAIGN_STATUS_TYPE_KEY]['Campaign_Status_Cd'].tolist()
        channel_codes: List[str] = ctx.tables[_CHANNEL_TYPE_KEY]['Channel_Type_Cd'].tolist()
        uom_codes: List[str] = ctx.tables[_UNIT_OF_MEASURE_KEY]['Unit_Of_Measure_Cd'].tolist()
        offer_type_codes: List[str] = (
            ctx.tables[_PROMOTION_OFFER_TYPE_KEY]['Promotion_Offer_Type_Cd'].tolist()
        )

        cs_rows, pr_rows, po_rows = self._build_rows(
            ctx, status_codes, channel_codes, uom_codes, offer_type_codes,
        )

        df_cs = pd.DataFrame(cs_rows, columns=_COLS_CAMPAIGN_STATUS)
        df_pr = pd.DataFrame(pr_rows, columns=_COLS_PROMOTION)
        df_po = pd.DataFrame(po_rows, columns=_COLS_PROMOTION_OFFER)

        # Int64 coercions — all *_Id columns (BIGINT per PRD §7.1)
        df_cs['Campaign_Id'] = df_cs['Campaign_Id'].astype('Int64')

        df_pr['Promotion_Id'] = df_pr['Promotion_Id'].astype('Int64')
        df_pr['Campaign_Id']  = df_pr['Campaign_Id'].astype('Int64')

        df_po['Promotion_Id']       = df_po['Promotion_Id'].astype('Int64')
        df_po['Promotion_Offer_Id'] = df_po['Promotion_Offer_Id'].astype('Int64')
        df_po['Ad_Id']              = df_po['Ad_Id'].astype('Int64')

        return {
            _CAMPAIGN_STATUS_KEY: self.stamp_di(df_cs, start_ts=_TIER11_DI_START_TS),
            _PROMOTION_KEY:       self.stamp_di(df_pr, start_ts=_TIER11_DI_START_TS),
            _PROMOTION_OFFER_KEY: self.stamp_di(df_po, start_ts=_TIER11_DI_START_TS),
        }

    # ------------------------------------------------------------------
    # Row builder
    # ------------------------------------------------------------------

    def _build_rows(
        self,
        ctx: 'GenerationContext',
        status_codes: List[str],
        channel_codes: List[str],
        uom_codes: List[str],
        offer_type_codes: List[str],
    ) -> Tuple[List[dict], List[dict], List[dict]]:
        rng = ctx.rng
        cs_rows: List[dict] = []
        pr_rows: List[dict] = []
        po_rows: List[dict] = []

        # Iterate campaigns sorted by Campaign_Id for determinism
        camp_df = ctx.tables[_CAMPAIGN_KEY].sort_values('Campaign_Id')

        for _, camp_row in camp_df.iterrows():
            campaign_id = int(camp_row['Campaign_Id'])

            # CAMPAIGN_STATUS — one current row per campaign
            cs_rows.append({
                'Campaign_Id':               campaign_id,
                'Campaign_Status_Start_Dttm': format_ts(
                    random_datetime_between(HISTORY_START, SIM_DATE, rng)
                ),
                'Campaign_Status_Cd':         str(rng.choice(status_codes)),
                'Campaign_Status_End_Dttm':   None,
            })

            # PROMOTION — 2–3 per campaign
            n_promo = int(rng.integers(2, 4))
            for _ in range(n_promo):
                promo_id   = ctx.ids.next('promotion')
                promo_type = str(rng.choice(_PROMOTION_TYPES))
                channel_cd = str(rng.choice(channel_codes))
                uom_cd     = str(rng.choice(uom_codes))

                start_dt = random_date_between(HISTORY_START, SIM_DATE, rng)
                end_dt   = start_dt + timedelta(days=int(rng.integers(30, 91)))

                pr_rows.append({
                    'Promotion_Id':                 promo_id,
                    'Promotion_Type_Cd':            promo_type,
                    'Campaign_Id':                  campaign_id,
                    'Promotion_Classification_Cd':  None,
                    'Channel_Type_Cd':              channel_cd,
                    'Internal_Promotion_Name':      None,
                    'Promotion_Desc':               None,
                    'Promotion_Objective_Txt':      None,
                    'Promotion_Start_Dt':           format_date(start_dt),
                    'Promotion_End_Dt':             format_date(end_dt),
                    'Promotion_Actual_Unit_Cost_Amt': _draw_amount(rng, *_PROMO_COST_RANGE),
                    'Promotion_Goal_Amt':           _draw_amount(rng, *_PROMO_GOAL_RANGE),
                    'Currency_Cd':                  'USD',
                    'Promotion_Actual_Unit_Cnt':    None,
                    'Promotion_Break_Even_Order_Cnt': None,
                    'Unit_Of_Measure_Cd':           uom_cd,
                })

                # PROMOTION_OFFER — 1–5 per promotion; Promotion_Offer_Id is within-promo seq
                n_offer = int(rng.integers(1, 6))
                for seq in range(1, n_offer + 1):
                    offer_type_cd = str(rng.choice(offer_type_codes))
                    dist_start  = random_date_between(HISTORY_START, SIM_DATE, rng)
                    dist_end    = dist_start + timedelta(days=int(rng.integers(7, 61)))
                    redemp_start = dist_start + timedelta(days=int(rng.integers(0, 8)))
                    redemp_end   = dist_end   + timedelta(days=int(rng.integers(0, 15)))
                    po_rows.append({
                        'Promotion_Id':           promo_id,
                        'Promotion_Offer_Id':     seq,
                        'Promotion_Offer_Type_Cd': offer_type_cd,
                        'Promotion_Offer_Desc':   None,
                        'Ad_Id':                  None,
                        'Distribution_Start_Dt':  format_date(dist_start),
                        'Distribution_End_Dt':    format_date(dist_end),
                        'Redemption_Start_Dt':    format_date(redemp_start),
                        'Redemption_End_Dt':      format_date(redemp_end),
                    })

        return cs_rows, pr_rows, po_rows

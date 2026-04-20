from __future__ import annotations

import calendar
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import TYPE_CHECKING, Dict, List, Optional

import pandas as pd

from config.settings import HISTORY_START, SIM_DATE
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ---------------------------------------------------------------------------
# DI start timestamp (matches Tier 6–9 convention)
# ---------------------------------------------------------------------------
_TIER10_DI_START_TS = '2000-01-01 00:00:00.000000'

# ---------------------------------------------------------------------------
# Schema keys
# ---------------------------------------------------------------------------
_EVENT_KEY           = 'Core_DB.EVENT'
_EVENT_PARTY_KEY     = 'Core_DB.EVENT_PARTY'
_EVENT_CHANNEL_KEY   = 'Core_DB.EVENT_CHANNEL_INSTANCE'
_FINANCIAL_EVENT_KEY = 'Core_DB.FINANCIAL_EVENT'
_FIN_AMOUNT_KEY      = 'Core_DB.FINANCIAL_EVENT_AMOUNT'
_FUNDS_TRANSFER_KEY  = 'Core_DB.FUNDS_TRANSFER_EVENT'
_ACCESS_DEVICE_KEY   = 'Core_DB.ACCESS_DEVICE_EVENT'
_DIRECT_CONTACT_KEY  = 'Core_DB.DIRECT_CONTACT_EVENT'
_COMPLAINT_KEY       = 'Core_DB.COMPLAINT_EVENT'

# ---------------------------------------------------------------------------
# Activity type codes
# ---------------------------------------------------------------------------
_ACTIVITY_TRANSACTION = 'TRANSACTION'
_ACTIVITY_ACCESS      = 'ACCESS'
_ACTIVITY_CONTACT     = 'CONTACT'
_ACTIVITY_COMPLAINT   = 'COMPLAINT'
_ACTIVITY_FEE         = 'FEE'
_ACTIVITY_INTEREST    = 'INTEREST'

# ---------------------------------------------------------------------------
# Financial event type codes
# ---------------------------------------------------------------------------
_FE_STATEMENT_FEE   = 'STATEMENT_FEE'
_FE_OVERDRAFT_FEE   = 'OVERDRAFT_FEE'
_FE_INTEREST_EARNED = 'INTEREST_EARNED'
_FE_INTEREST_PAID   = 'INTEREST_PAID'
_FE_TRANSFER        = 'TRANSFER'

# ---------------------------------------------------------------------------
# Direction codes
# ---------------------------------------------------------------------------
_DIR_IN  = 'IN'
_DIR_OUT = 'OUT'

# ---------------------------------------------------------------------------
# Event party role
# ---------------------------------------------------------------------------
_EVENT_PARTY_ROLE_INITIATOR = 'initiator'

# ---------------------------------------------------------------------------
# Funds transfer method codes
# ---------------------------------------------------------------------------
_FTM_ACH       = 'ACH'
_FTM_WIRE      = 'WIRE'
_FTM_INTRABANK = 'INTRABANK'
_FTM_EXTERNAL  = (_FTM_ACH, _FTM_WIRE)

# ---------------------------------------------------------------------------
# Channel type sets per activity
# ---------------------------------------------------------------------------
_ACCESS_CHANNEL_TYPES      = ('ATM', 'ONLINE', 'MOBILE')
_CONTACT_CHANNEL_TYPES     = ('CALL_CENTER', 'ONLINE')
_COMPLAINT_CHANNEL_TYPES   = ('CALL_CENTER', 'ONLINE', 'MOBILE')
_TRANSACTION_CHANNEL_TYPES = ('ONLINE', 'MOBILE', 'BRANCH', 'ATM')
_FEE_CHANNEL_TYPES         = ('ONLINE',)
_INTEREST_CHANNEL_TYPES    = ('ONLINE',)

# ---------------------------------------------------------------------------
# Contact subtype and customer tone codes
# ---------------------------------------------------------------------------
_CONTACT_SUBTYPE_CALL  = 'CALL'
_CONTACT_SUBTYPE_EMAIL = 'EMAIL'
_CONTACT_SUBTYPE_CHAT  = 'CHAT'
_CONTACT_SUBTYPES      = (_CONTACT_SUBTYPE_CALL, _CONTACT_SUBTYPE_EMAIL, _CONTACT_SUBTYPE_CHAT)

_TONE_POSITIVE = 'POSITIVE'
_TONE_NEUTRAL  = 'NEUTRAL'
_TONE_NEGATIVE = 'NEGATIVE'
_TONES         = (_TONE_POSITIVE, _TONE_NEUTRAL, _TONE_NEGATIVE)

# ---------------------------------------------------------------------------
# Complaint SMALLINT codes
# ---------------------------------------------------------------------------
_COMPLAINT_SENTIMENT_POSITIVE = 1
_COMPLAINT_SENTIMENT_NEUTRAL  = 2
_COMPLAINT_SENTIMENT_NEGATIVE = 3
_COMPLAINT_SENTIMENTS         = (
    _COMPLAINT_SENTIMENT_POSITIVE,
    _COMPLAINT_SENTIMENT_NEUTRAL,
    _COMPLAINT_SENTIMENT_NEGATIVE,
)
_COMPLAINT_SENTIMENT_WEIGHTS  = (0.15, 0.15, 0.70)  # higher weight on NEGATIVE
_COMPLAINT_CHANNEL_SMALLINTS  = (1, 2, 3, 4, 5)
_MULTIMEDIA_IND_Y  = 'Y'
_MULTIMEDIA_IND_N  = 'N'
_MULTIMEDIA_Y_RATE = 0.10

# ---------------------------------------------------------------------------
# Financial event amount code (MVP single-row deferral)
# ---------------------------------------------------------------------------
_AMOUNT_CD_PRINCIPAL = 'principal'

# ---------------------------------------------------------------------------
# Envelope / rate constants
# ---------------------------------------------------------------------------
_MONTHLY_EVENTS_MIN      = 1
_MONTHLY_EVENTS_MAX      = 5
_DECLINING_ENVELOPE      = (1.0, 0.8, 0.6, 0.4, 0.3, 0.2)
_COMPLAINT_CUSTOMER_RATE = 0.05
_OVERDRAFT_MONTH_RATE    = 0.05
_TRANSACTION_SPLIT       = 0.30
_ACCESS_SPLIT            = 0.50
_CONTACT_SPLIT           = 0.20
_INTERNAL_TRANSFER_RATE  = 0.20

# ---------------------------------------------------------------------------
# Amount ranges (Decimal pairs — lo, hi inclusive)
# ---------------------------------------------------------------------------
_STATEMENT_FEE_AMT_RANGE    = (Decimal('5.00'),   Decimal('25.00'))
_OVERDRAFT_FEE_AMT_RANGE    = (Decimal('25.00'),  Decimal('40.00'))
_INTEREST_DEPOSIT_AMT_RANGE = (Decimal('0.50'),   Decimal('50.00'))
_INTEREST_LOAN_AMT_RANGE    = (Decimal('25.00'),  Decimal('1500.00'))
_TRANSFER_AMT_RANGE         = (Decimal('50.00'),  Decimal('5000.00'))

# ---------------------------------------------------------------------------
# Required upstream tables for guard
# ---------------------------------------------------------------------------
_REQUIRED_UPSTREAM = ('Core_DB.PARTY', 'Core_DB.AGREEMENT', 'Core_DB.CHANNEL_INSTANCE')

# ---------------------------------------------------------------------------
# Column lists (business cols only; DI tail appended by stamp_di)
# Verified against references/07_mvp-schema-reference.md DDL
# ---------------------------------------------------------------------------
_COLS_EVENT: List[str] = [
    'Event_Id', 'Event_Desc', 'Event_Start_Dttm', 'Event_End_Dttm',
    'Event_GMT_Start_Dttm', 'Event_Activity_Type_Cd', 'Event_Reason_Cd',
    'Event_Subtype_Cd', 'Initiation_Type_Cd',
]
_COLS_EVENT_PARTY: List[str] = [
    'Event_Id', 'Party_Id', 'Event_Party_Role_Cd',
    'Event_Party_Start_Dttm', 'Event_Party_End_Dttm', 'Party_Identification_Type_Cd',
]
_COLS_EVENT_CHANNEL_INSTANCE: List[str] = [
    'Event_Id', 'Channel_Instance_Id', 'Event_Channel_Start_Dttm', 'Event_Channel_End_Dttm',
]
_COLS_FINANCIAL_EVENT: List[str] = [
    'Event_Id', 'Financial_Event_Period_Start_Dt', 'Financial_Event_Period_End_Dt',
    'Financial_Event_Type_Cd', 'Document_Production_Cycle_Cd', 'Event_Medium_Type_Cd',
    'Debit_Credit_Cd', 'In_Out_Direction_Type_Cd', 'Financial_Event_Bill_Cnt',
]
_COLS_FINANCIAL_EVENT_AMOUNT: List[str] = [
    'Event_Id', 'Financial_Event_Amount_Cd', 'Event_Transaction_Amt',
    'Financial_Event_Type_Cd', 'In_Out_Direction_Type_Cd',
]
_COLS_FUNDS_TRANSFER_EVENT: List[str] = [
    'Event_Id', 'Funds_Transfer_Method_Type_Cd', 'Originating_Agreement_Id',
    'Originating_Account_Num', 'Destination_Agreement_Id', 'Destination_Account_Num',
]
_COLS_ACCESS_DEVICE_EVENT: List[str] = [
    'Event_Id', 'Channel_Type_Cd', 'Funds_Transfer_Method_Type_Cd', 'Access_Device_Id',
]
_COLS_DIRECT_CONTACT_EVENT: List[str] = [
    'Event_Id', 'Contact_Event_Subtype_Cd', 'Customer_Tone_Cd',
]
_COLS_COMPLAINT_EVENT: List[str] = [
    'Event_Id', 'Event_Sentiment_Cd', 'Event_Channel_Type_Cd',
    'Event_Received_Dttm', 'Event_Txt', 'Event_Multimedia_Object_Ind',
]

# ---------------------------------------------------------------------------
# Pre-computed 6-month history window: list of (year, month, month_idx)
# ---------------------------------------------------------------------------
_MONTHS: List[tuple] = []
_y, _m = HISTORY_START.year, HISTORY_START.month
for _mi in range(6):
    _MONTHS.append((_y, _m, _mi))
    _m += 1
    if _m == 13:
        _m = 1
        _y += 1
del _y, _m, _mi

# Pre-computed complaint history window bounds
_HIST_START_DT = datetime(HISTORY_START.year, HISTORY_START.month, HISTORY_START.day, 0, 0, 0)
_HIST_END_DT   = datetime(SIM_DATE.year, SIM_DATE.month, SIM_DATE.day, 23, 59, 59)
_HIST_TOTAL_SECONDS = int((_HIST_END_DT - _HIST_START_DT).total_seconds())


# ---------------------------------------------------------------------------
# Module-level helper functions
# ---------------------------------------------------------------------------

def _draw_amount(rng, lo: Decimal, hi: Decimal) -> Decimal:
    raw = rng.uniform(float(lo), float(hi))
    return Decimal(str(raw)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)


def _channel_types_for(activity_type: str) -> tuple:
    if activity_type == _ACTIVITY_ACCESS:
        return _ACCESS_CHANNEL_TYPES
    if activity_type == _ACTIVITY_CONTACT:
        return _CONTACT_CHANNEL_TYPES
    if activity_type == _ACTIVITY_TRANSACTION:
        return _TRANSACTION_CHANNEL_TYPES
    if activity_type == _ACTIVITY_FEE:
        return _FEE_CHANNEL_TYPES
    if activity_type == _ACTIVITY_INTEREST:
        return _INTEREST_CHANNEL_TYPES
    if activity_type == _ACTIVITY_COMPLAINT:
        return _COMPLAINT_CHANNEL_TYPES
    return _ACCESS_CHANNEL_TYPES  # fallback


def _apply_envelope(
    cohort: str,
    month_idx: int,
    base: int,
    open_dttm: Optional[datetime],
    close_dttm: Optional[datetime],
    month_start_dt: datetime,
    month_end_dt: datetime,
) -> int:
    if cohort == 'CHURNED':
        if close_dttm is not None and month_start_dt > close_dttm:
            return 0
    elif cohort == 'NEW':
        if open_dttm is not None and month_end_dt < open_dttm:
            return 0
    if cohort == 'DECLINING':
        return max(0, round(base * _DECLINING_ENVELOPE[month_idx]))
    return base


def _draw_ts_in_window(
    rng,
    month_start_dt: datetime,
    month_end_dt: datetime,
    open_dttm: Optional[datetime],
    close_dttm: Optional[datetime],
    cohort: str,
) -> datetime:
    lo = month_start_dt
    hi = month_end_dt
    if cohort == 'NEW' and open_dttm is not None and open_dttm > lo:
        lo = open_dttm
    if cohort == 'CHURNED' and close_dttm is not None and close_dttm < hi:
        hi = close_dttm
    total_secs = int((hi - lo).total_seconds())
    if total_secs <= 0:
        total_secs = 1
    return lo + timedelta(seconds=int(rng.integers(0, total_secs)))


def _make_fee_rec(
    event_id: int,
    party_id: int,
    ts: datetime,
    financial_type: str,
    direction: str,
    amount: Decimal,
    channel_index: Dict[str, List[int]],
    channel_type_of: Dict[int, str],
    rng,
) -> dict:
    act = (
        _ACTIVITY_INTEREST
        if financial_type in (_FE_INTEREST_EARNED, _FE_INTEREST_PAID)
        else _ACTIVITY_FEE
    )
    allowed = _channel_types_for(act)
    type_cd = str(rng.choice(allowed))
    instance_id = int(rng.choice(channel_index[type_cd]))
    return {
        'event_id': event_id,
        'activity_type': act,
        'party_id': party_id,
        'start_dttm': ts,
        'channel_instance_id': instance_id,
        'channel_type_cd': channel_type_of[instance_id],
        'financial_event_type_cd': financial_type,
        'direction': direction,
        'amount': amount,
        'originating_agreement_id': None,
        'destination_agreement_id': None,
        'transfer_method': None,
        'contact_subtype_cd': None,
        'customer_tone_cd': None,
        'sentiment_cd': None,
        'complaint_channel_cd': None,
        'multimedia_ind': None,
        'event_txt': None,
        'owner_agreement_id': None,
    }


# ---------------------------------------------------------------------------
# Generator class
# ---------------------------------------------------------------------------

class Tier10Events(BaseGenerator):

    def __init__(self) -> None:
        self.last_periodic_owner_map: Dict[int, int] = {}

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # Guards
        if not ctx.customers:
            raise RuntimeError('Tier 10 prerequisite missing: ctx.customers is empty')
        if not ctx.agreements:
            raise RuntimeError('Tier 10 prerequisite missing: ctx.agreements is empty')
        for key in _REQUIRED_UPSTREAM:
            if key not in ctx.tables:
                raise RuntimeError(f'Tier 10 prerequisite missing: {key}')
        ci_df = ctx.tables['Core_DB.CHANNEL_INSTANCE']
        if len(ci_df) < 20:
            raise RuntimeError('Tier 10: CHANNEL_INSTANCE has fewer than 20 rows')

        # Build channel lookup structures (O(1) channel-picker access)
        channel_index: Dict[str, List[int]] = {}
        channel_type_of: Dict[int, str] = {}
        for _, row in ci_df.iterrows():
            ctype = str(row['Channel_Type_Cd'])
            cid = int(row['Channel_Instance_Id'])
            channel_index.setdefault(ctype, []).append(cid)
            channel_type_of[cid] = ctype

        # Per-customer agreement maps
        cust_ag_map: Dict[int, List] = {}
        cust_deposit_map: Dict[int, List] = {}
        for ag in ctx.agreements:
            cust_ag_map.setdefault(ag.owner_party_id, []).append(ag)
            if ag.is_deposit:
                cust_deposit_map.setdefault(ag.owner_party_id, []).append(ag)

        # Build three event streams
        disc_records = self._build_discretionary_event_stream(
            ctx, channel_index, channel_type_of, cust_deposit_map, cust_ag_map,
        )
        comp_records = self._build_complaint_event_stream(
            ctx, channel_index, channel_type_of,
        )
        peri_records = self._build_periodic_financial_event_stream(
            ctx, channel_index, channel_type_of,
        )

        all_records = disc_records + comp_records + peri_records
        frames = self._assemble_event_frames(all_records)
        return {key: self.stamp_di(df, start_ts=_TIER10_DI_START_TS) for key, df in frames.items()}

    # ------------------------------------------------------------------
    # Stream builders
    # ------------------------------------------------------------------

    def _build_discretionary_event_stream(
        self,
        ctx: 'GenerationContext',
        channel_index: Dict[str, List[int]],
        channel_type_of: Dict[int, str],
        cust_deposit_map: Dict[int, List],
        cust_ag_map: Dict[int, List],
    ) -> List[dict]:
        records: List[dict] = []
        rng = ctx.rng

        for cp in ctx.customers:
            cohort = cp.lifecycle_cohort
            deposit_ags = cust_deposit_map.get(cp.party_id, [])
            cust_ags = cust_ag_map.get(cp.party_id, [])

            # Effective open/close datetimes for cohort envelope
            close_dttm: Optional[datetime] = None
            open_dttm: Optional[datetime] = None
            if cohort == 'CHURNED' and cust_ags:
                close_candidates = [ag.close_dttm for ag in cust_ags if ag.close_dttm is not None]
                close_dttm = min(close_candidates) if close_candidates else None
            elif cohort == 'NEW' and cust_ags:
                open_dttm = min(ag.open_dttm for ag in cust_ags)

            for (year, month, month_idx) in _MONTHS:
                month_start_dt = datetime(year, month, 1, 0, 0, 0)
                last_day = calendar.monthrange(year, month)[1]
                month_end_dt = datetime(year, month, last_day, 23, 59, 59)

                base = int(rng.integers(_MONTHLY_EVENTS_MIN, _MONTHLY_EVENTS_MAX + 1))
                event_count = _apply_envelope(
                    cohort, month_idx, base,
                    open_dttm, close_dttm,
                    month_start_dt, month_end_dt,
                )

                for _ in range(event_count):
                    event_id = ctx.ids.next('event')
                    ts = _draw_ts_in_window(
                        rng, month_start_dt, month_end_dt,
                        open_dttm, close_dttm, cohort,
                    )

                    # Weighted activity draw; TRANSACTION falls back to ACCESS if no deposits
                    act_raw = rng.choice(
                        [_ACTIVITY_TRANSACTION, _ACTIVITY_ACCESS, _ACTIVITY_CONTACT],
                        p=[_TRANSACTION_SPLIT, _ACCESS_SPLIT, _CONTACT_SPLIT],
                    )
                    act = str(act_raw)
                    if act == _ACTIVITY_TRANSACTION and not deposit_ags:
                        act = _ACTIVITY_ACCESS

                    # Channel selection
                    allowed_types = _channel_types_for(act)
                    type_cd = str(rng.choice(allowed_types))
                    instance_id = int(rng.choice(channel_index[type_cd]))

                    rec: dict = {
                        'event_id': event_id,
                        'activity_type': act,
                        'party_id': cp.party_id,
                        'start_dttm': ts,
                        'channel_instance_id': instance_id,
                        'channel_type_cd': channel_type_of[instance_id],
                        'financial_event_type_cd': None,
                        'direction': None,
                        'amount': None,
                        'originating_agreement_id': None,
                        'destination_agreement_id': None,
                        'transfer_method': None,
                        'contact_subtype_cd': None,
                        'customer_tone_cd': None,
                        'sentiment_cd': None,
                        'complaint_channel_cd': None,
                        'multimedia_ind': None,
                        'event_txt': None,
                        'owner_agreement_id': None,
                    }

                    if act == _ACTIVITY_TRANSACTION:
                        orig_idx = int(rng.integers(0, len(deposit_ags)))
                        orig_ag = deposit_ags[orig_idx]
                        rec['financial_event_type_cd'] = _FE_TRANSFER
                        rec['direction'] = _DIR_OUT
                        rec['amount'] = _draw_amount(rng, *_TRANSFER_AMT_RANGE)
                        rec['originating_agreement_id'] = orig_ag.agreement_id
                        # ~20% internal transfer (requires >1 deposit agreement)
                        if rng.random() < _INTERNAL_TRANSFER_RATE and len(deposit_ags) > 1:
                            others = [
                                a for a in deposit_ags
                                if a.agreement_id != orig_ag.agreement_id
                            ]
                            dest_idx = int(rng.integers(0, len(others)))
                            rec['destination_agreement_id'] = others[dest_idx].agreement_id
                            rec['transfer_method'] = _FTM_INTRABANK
                        else:
                            rec['transfer_method'] = str(rng.choice(_FTM_EXTERNAL))

                    elif act == _ACTIVITY_CONTACT:
                        rec['contact_subtype_cd'] = str(rng.choice(_CONTACT_SUBTYPES))
                        rec['customer_tone_cd'] = str(rng.choice(_TONES))

                    records.append(rec)

        return records

    # ------------------------------------------------------------------

    def _build_complaint_event_stream(
        self,
        ctx: 'GenerationContext',
        channel_index: Dict[str, List[int]],
        channel_type_of: Dict[int, str],
    ) -> List[dict]:
        records: List[dict] = []
        rng = ctx.rng

        for cp in ctx.customers:
            if rng.random() >= _COMPLAINT_CUSTOMER_RATE:
                continue

            event_id = ctx.ids.next('event')
            offset_secs = int(rng.integers(0, _HIST_TOTAL_SECONDS + 1))
            ts = _HIST_START_DT + timedelta(seconds=offset_secs)

            type_cd = str(rng.choice(_COMPLAINT_CHANNEL_TYPES))
            instance_id = int(rng.choice(channel_index[type_cd]))

            sentiment = int(rng.choice(
                _COMPLAINT_SENTIMENTS,
                p=list(_COMPLAINT_SENTIMENT_WEIGHTS),
            ))
            comp_channel = int(rng.choice(_COMPLAINT_CHANNEL_SMALLINTS))
            multimedia = _MULTIMEDIA_IND_Y if rng.random() < _MULTIMEDIA_Y_RATE else _MULTIMEDIA_IND_N

            records.append({
                'event_id': event_id,
                'activity_type': _ACTIVITY_COMPLAINT,
                'party_id': cp.party_id,
                'start_dttm': ts,
                'channel_instance_id': instance_id,
                'channel_type_cd': channel_type_of[instance_id],
                'financial_event_type_cd': None,
                'direction': None,
                'amount': None,
                'originating_agreement_id': None,
                'destination_agreement_id': None,
                'transfer_method': None,
                'contact_subtype_cd': None,
                'customer_tone_cd': None,
                'sentiment_cd': sentiment,
                'complaint_channel_cd': comp_channel,
                'multimedia_ind': multimedia,
                'event_txt': f'Complaint record for event {event_id}',
                'owner_agreement_id': None,
            })

        return records

    # ------------------------------------------------------------------

    def _build_periodic_financial_event_stream(
        self,
        ctx: 'GenerationContext',
        channel_index: Dict[str, List[int]],
        channel_type_of: Dict[int, str],
    ) -> List[dict]:
        records: List[dict] = []
        owner_map: Dict[int, int] = {}
        rng = ctx.rng

        for ag in ctx.agreements:
            party_id = ag.owner_party_id
            is_deposit_path = ag.is_deposit or ag.is_term_deposit
            interest_type = _FE_INTEREST_EARNED if is_deposit_path else _FE_INTEREST_PAID
            interest_dir  = _DIR_IN             if is_deposit_path else _DIR_OUT
            interest_amt_range = (
                _INTEREST_DEPOSIT_AMT_RANGE if is_deposit_path else _INTEREST_LOAN_AMT_RANGE
            )

            ag_end_date = ag.close_dttm.date() if ag.close_dttm else SIM_DATE

            for (year, month, _month_idx) in _MONTHS:
                ym = (year, month)
                if ym < (ag.open_dttm.year, ag.open_dttm.month):
                    continue
                if ym > (ag_end_date.year, ag_end_date.month):
                    continue

                last_day = calendar.monthrange(year, month)[1]
                month_end_dt = datetime(year, month, last_day, 23, 59, 59)

                # 1. STATEMENT_FEE — always one per eligible agreement-month
                stmt_id = ctx.ids.next('event')
                records.append(_make_fee_rec(
                    stmt_id, party_id, month_end_dt,
                    _FE_STATEMENT_FEE, _DIR_OUT,
                    _draw_amount(rng, *_STATEMENT_FEE_AMT_RANGE),
                    channel_index, channel_type_of, rng,
                ))
                owner_map[stmt_id] = ag.agreement_id

                # 2. INTEREST — always one per eligible agreement-month
                int_id = ctx.ids.next('event')
                records.append(_make_fee_rec(
                    int_id, party_id, month_end_dt,
                    interest_type, interest_dir,
                    _draw_amount(rng, *interest_amt_range),
                    channel_index, channel_type_of, rng,
                ))
                owner_map[int_id] = ag.agreement_id

                # 3. OVERDRAFT_FEE — deposit path only, Bernoulli
                if is_deposit_path and rng.random() < _OVERDRAFT_MONTH_RATE:
                    secs_in_month = last_day * 86400
                    od_ts = datetime(year, month, 1) + timedelta(
                        seconds=int(rng.integers(0, secs_in_month))
                    )
                    od_id = ctx.ids.next('event')
                    records.append(_make_fee_rec(
                        od_id, party_id, od_ts,
                        _FE_OVERDRAFT_FEE, _DIR_OUT,
                        _draw_amount(rng, *_OVERDRAFT_FEE_AMT_RANGE),
                        channel_index, channel_type_of, rng,
                    ))
                    owner_map[od_id] = ag.agreement_id

        self.last_periodic_owner_map = owner_map
        return records

    # ------------------------------------------------------------------
    # Assembler
    # ------------------------------------------------------------------

    def _assemble_event_frames(
        self,
        event_records: List[dict],
    ) -> Dict[str, pd.DataFrame]:
        ev_rows:  List[dict] = []
        ep_rows:  List[dict] = []
        eci_rows: List[dict] = []
        fe_rows:  List[dict] = []
        fea_rows: List[dict] = []
        fte_rows: List[dict] = []
        ade_rows: List[dict] = []
        dce_rows: List[dict] = []
        ce_rows:  List[dict] = []

        for r in event_records:
            eid = r['event_id']
            act = r['activity_type']
            ts  = r['start_dttm']

            # EVENT (every record)
            ev_rows.append({
                'Event_Id':              eid,
                'Event_Desc':            None,
                'Event_Start_Dttm':      ts,
                'Event_End_Dttm':        None,
                'Event_GMT_Start_Dttm':  None,
                'Event_Activity_Type_Cd': act,
                'Event_Reason_Cd':       None,
                'Event_Subtype_Cd':      None,
                'Initiation_Type_Cd':    None,
            })

            # EVENT_PARTY (every record — exactly one initiator per event)
            ep_rows.append({
                'Event_Id':                   eid,
                'Party_Id':                   r['party_id'],
                'Event_Party_Role_Cd':         _EVENT_PARTY_ROLE_INITIATOR,
                'Event_Party_Start_Dttm':      ts,
                'Event_Party_End_Dttm':        None,
                'Party_Identification_Type_Cd': None,
            })

            # EVENT_CHANNEL_INSTANCE (every record — one channel per event)
            eci_rows.append({
                'Event_Id':               eid,
                'Channel_Instance_Id':    r['channel_instance_id'],
                'Event_Channel_Start_Dttm': ts,
                'Event_Channel_End_Dttm': None,
            })

            # Sub-type routing (exclusive per design §7.5)
            if act in (_ACTIVITY_TRANSACTION, _ACTIVITY_FEE, _ACTIVITY_INTEREST):
                fe_rows.append({
                    'Event_Id':                        eid,
                    'Financial_Event_Period_Start_Dt': None,
                    'Financial_Event_Period_End_Dt':   None,
                    'Financial_Event_Type_Cd':         r['financial_event_type_cd'],
                    'Document_Production_Cycle_Cd':    None,
                    'Event_Medium_Type_Cd':            None,
                    'Debit_Credit_Cd':                 None,
                    'In_Out_Direction_Type_Cd':        r['direction'],
                    'Financial_Event_Bill_Cnt':        None,
                })
                fea_rows.append({
                    'Event_Id':                   eid,
                    'Financial_Event_Amount_Cd':  _AMOUNT_CD_PRINCIPAL,
                    'Event_Transaction_Amt':      r['amount'],
                    'Financial_Event_Type_Cd':    r['financial_event_type_cd'],
                    'In_Out_Direction_Type_Cd':   r['direction'],
                })
                if act == _ACTIVITY_TRANSACTION:
                    fte_rows.append({
                        'Event_Id':                    eid,
                        'Funds_Transfer_Method_Type_Cd': r['transfer_method'],
                        'Originating_Agreement_Id':    r['originating_agreement_id'],
                        'Originating_Account_Num':     None,
                        'Destination_Agreement_Id':    r['destination_agreement_id'],
                        'Destination_Account_Num':     None,
                    })

            elif act == _ACTIVITY_ACCESS:
                ade_rows.append({
                    'Event_Id':                      eid,
                    'Channel_Type_Cd':               r['channel_type_cd'],
                    'Funds_Transfer_Method_Type_Cd': None,
                    'Access_Device_Id':              None,
                })

            elif act == _ACTIVITY_CONTACT:
                dce_rows.append({
                    'Event_Id':                  eid,
                    'Contact_Event_Subtype_Cd':  r['contact_subtype_cd'],
                    'Customer_Tone_Cd':          r['customer_tone_cd'],
                })

            elif act == _ACTIVITY_COMPLAINT:
                ce_rows.append({
                    'Event_Id':                   eid,
                    'Event_Sentiment_Cd':         r['sentiment_cd'],
                    'Event_Channel_Type_Cd':      r['complaint_channel_cd'],
                    'Event_Received_Dttm':        ts,
                    'Event_Txt':                  r['event_txt'],
                    'Event_Multimedia_Object_Ind': r['multimedia_ind'],
                })

        # Construct DataFrames with explicit DDL column order
        df_ev  = pd.DataFrame(ev_rows,  columns=_COLS_EVENT)
        df_ep  = pd.DataFrame(ep_rows,  columns=_COLS_EVENT_PARTY)
        df_eci = pd.DataFrame(eci_rows, columns=_COLS_EVENT_CHANNEL_INSTANCE)
        df_fe  = pd.DataFrame(fe_rows,  columns=_COLS_FINANCIAL_EVENT)
        df_fea = pd.DataFrame(fea_rows, columns=_COLS_FINANCIAL_EVENT_AMOUNT)
        df_fte = pd.DataFrame(fte_rows, columns=_COLS_FUNDS_TRANSFER_EVENT)
        df_ade = pd.DataFrame(ade_rows, columns=_COLS_ACCESS_DEVICE_EVENT)
        df_dce = pd.DataFrame(dce_rows, columns=_COLS_DIRECT_CONTACT_EVENT)
        df_ce  = pd.DataFrame(ce_rows,  columns=_COLS_COMPLAINT_EVENT)

        # Type coercions — all *_Id columns → Int64 (BIGINT per PRD §7.1)
        df_ev['Event_Id'] = df_ev['Event_Id'].astype('Int64')

        df_ep['Event_Id']  = df_ep['Event_Id'].astype('Int64')
        df_ep['Party_Id']  = df_ep['Party_Id'].astype('Int64')

        df_eci['Event_Id']           = df_eci['Event_Id'].astype('Int64')
        df_eci['Channel_Instance_Id'] = df_eci['Channel_Instance_Id'].astype('Int64')

        df_fe['Event_Id'] = df_fe['Event_Id'].astype('Int64')

        df_fea['Event_Id'] = df_fea['Event_Id'].astype('Int64')

        df_fte['Event_Id']                 = df_fte['Event_Id'].astype('Int64')
        df_fte['Originating_Agreement_Id'] = df_fte['Originating_Agreement_Id'].astype('Int64')
        df_fte['Destination_Agreement_Id'] = df_fte['Destination_Agreement_Id'].astype('Int64')

        df_ade['Event_Id']       = df_ade['Event_Id'].astype('Int64')
        df_ade['Access_Device_Id'] = df_ade['Access_Device_Id'].astype('Int64')  # all-NA MVP

        df_dce['Event_Id'] = df_dce['Event_Id'].astype('Int64')

        df_ce['Event_Id']              = df_ce['Event_Id'].astype('Int64')
        df_ce['Event_Sentiment_Cd']    = df_ce['Event_Sentiment_Cd'].astype('Int64')
        df_ce['Event_Channel_Type_Cd'] = df_ce['Event_Channel_Type_Cd'].astype('Int64')

        return {
            _EVENT_KEY:           df_ev,
            _EVENT_PARTY_KEY:     df_ep,
            _EVENT_CHANNEL_KEY:   df_eci,
            _FINANCIAL_EVENT_KEY: df_fe,
            _FIN_AMOUNT_KEY:      df_fea,
            _FUNDS_TRANSFER_KEY:  df_fte,
            _ACCESS_DEVICE_KEY:   df_ade,
            _DIRECT_CONTACT_KEY:  df_dce,
            _COMPLAINT_KEY:       df_ce,
        }

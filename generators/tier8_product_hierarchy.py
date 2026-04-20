from __future__ import annotations

from datetime import datetime, time
from decimal import Decimal
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import pandas as pd

from config.code_values import ORIGINAL_LOAN_TERM_CLASSIFICATION_CD, RATE_FEATURE_SUBTYPE_CD
from config.settings import HIGH_DATE, HIGH_TS, HISTORY_START
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ── Tier-level constants ───────────────────────────────────────────────────────

_TIER8_DI_START_TS   = '2000-01-01 00:00:00.000000'
_TIER8_VALID_FROM_DT = HISTORY_START.isoformat()   # '2025-10-01'

_PRIMARY_ROLE_CD        = 'primary'
_PRODUCT_GROUP_TYPE_CLV = 'CLV'
_USD_CURRENCY_CD        = 'USD'

# ── Product-group hierarchy ────────────────────────────────────────────────────

_PRODUCT_GROUP_IDS: Dict[str, int] = {
    'ROOT':         92_000_000,
    'CHECKING':     92_000_001,
    'SAVINGS':      92_000_002,
    'RETIREMENT':   92_000_003,
    'CREDIT_CARD':  92_000_004,
    'VEHICLE_LOAN': 92_000_005,
    'MORTGAGE':     92_000_006,
    'INVESTMENTS':  92_000_007,
    'INSURANCE':    92_000_008,
}

# Maps each of the 12 MVP product types to its CLV group key.
# STUDENT_LOAN → VEHICLE_LOAN and PAYDAY → CREDIT_CARD are deliberate simplifications:
# the standard 8-type CLV hierarchy has no Education or Short-Term-Credit bucket.
_PRODUCT_TO_CLV_GROUP: Dict[str, str] = {
    'CHECKING':               'CHECKING',
    'COMMERCIAL_CHECKING':    'CHECKING',
    'SAVINGS':                'SAVINGS',
    'MMA':                    'SAVINGS',
    'CERTIFICATE_OF_DEPOSIT': 'SAVINGS',
    'RETIREMENT':             'RETIREMENT',
    'CREDIT_CARD':            'CREDIT_CARD',
    'PAYDAY':                 'CREDIT_CARD',
    'VEHICLE_LOAN':           'VEHICLE_LOAN',
    'STUDENT_LOAN':           'VEHICLE_LOAN',
    'MORTGAGE':               'MORTGAGE',
    'HELOC':                  'MORTGAGE',
}

# 9 literal PRODUCT_GROUP rows: 1 root (self-referential) + 8 CLV children.
_PRODUCT_GROUP_ROWS: List[Dict] = [
    {
        'Product_Group_Id':   _PRODUCT_GROUP_IDS['ROOT'],
        'Parent_Group_Id':    _PRODUCT_GROUP_IDS['ROOT'],
        'Product_Group_Type_Cd': _PRODUCT_GROUP_TYPE_CLV,
        'Product_Group_Name': 'Root',
        'Product_Group_Desc': (
            'Root of Core_DB product group hierarchy — '
            'self-referential per 05_architect-qa.md Q3'
        ),
    },
    {
        'Product_Group_Id':   _PRODUCT_GROUP_IDS['CHECKING'],
        'Parent_Group_Id':    _PRODUCT_GROUP_IDS['ROOT'],
        'Product_Group_Type_Cd': _PRODUCT_GROUP_TYPE_CLV,
        'Product_Group_Name': 'Checking',
        'Product_Group_Desc': None,
    },
    {
        'Product_Group_Id':   _PRODUCT_GROUP_IDS['SAVINGS'],
        'Parent_Group_Id':    _PRODUCT_GROUP_IDS['ROOT'],
        'Product_Group_Type_Cd': _PRODUCT_GROUP_TYPE_CLV,
        'Product_Group_Name': 'Savings',
        'Product_Group_Desc': None,
    },
    {
        'Product_Group_Id':   _PRODUCT_GROUP_IDS['RETIREMENT'],
        'Parent_Group_Id':    _PRODUCT_GROUP_IDS['ROOT'],
        'Product_Group_Type_Cd': _PRODUCT_GROUP_TYPE_CLV,
        'Product_Group_Name': 'Retirement',
        'Product_Group_Desc': None,
    },
    {
        'Product_Group_Id':   _PRODUCT_GROUP_IDS['CREDIT_CARD'],
        'Parent_Group_Id':    _PRODUCT_GROUP_IDS['ROOT'],
        'Product_Group_Type_Cd': _PRODUCT_GROUP_TYPE_CLV,
        'Product_Group_Name': 'Credit Card',
        'Product_Group_Desc': None,
    },
    {
        'Product_Group_Id':   _PRODUCT_GROUP_IDS['VEHICLE_LOAN'],
        'Parent_Group_Id':    _PRODUCT_GROUP_IDS['ROOT'],
        'Product_Group_Type_Cd': _PRODUCT_GROUP_TYPE_CLV,
        'Product_Group_Name': 'Vehicle Loan',
        'Product_Group_Desc': None,
    },
    {
        'Product_Group_Id':   _PRODUCT_GROUP_IDS['MORTGAGE'],
        'Parent_Group_Id':    _PRODUCT_GROUP_IDS['ROOT'],
        'Product_Group_Type_Cd': _PRODUCT_GROUP_TYPE_CLV,
        'Product_Group_Name': 'Mortgage',
        'Product_Group_Desc': None,
    },
    {
        'Product_Group_Id':   _PRODUCT_GROUP_IDS['INVESTMENTS'],
        'Parent_Group_Id':    _PRODUCT_GROUP_IDS['ROOT'],
        'Product_Group_Type_Cd': _PRODUCT_GROUP_TYPE_CLV,
        'Product_Group_Name': 'Investments',
        'Product_Group_Desc': None,
    },
    {
        'Product_Group_Id':   _PRODUCT_GROUP_IDS['INSURANCE'],
        'Parent_Group_Id':    _PRODUCT_GROUP_IDS['ROOT'],
        'Product_Group_Type_Cd': _PRODUCT_GROUP_TYPE_CLV,
        'Product_Group_Name': 'Insurance',
        'Product_Group_Desc': None,
    },
]

# ── Cost recipe ────────────────────────────────────────────────────────────────
# 2 rows per product: ACQUISITION + MAINTENANCE (illustrative amounts only;
# no Layer 2 rule binds these values).

_PRODUCT_COST_RECIPE: Dict[str, List[Tuple[str, Decimal]]] = {
    'CHECKING':               [('ACQUISITION', Decimal('12.0000')),  ('MAINTENANCE', Decimal('5.0000'))],
    'SAVINGS':                [('ACQUISITION', Decimal('0.0000')),   ('MAINTENANCE', Decimal('3.0000'))],
    'MMA':                    [('ACQUISITION', Decimal('0.0000')),   ('MAINTENANCE', Decimal('10.0000'))],
    'CERTIFICATE_OF_DEPOSIT': [('ACQUISITION', Decimal('25.0000')),  ('MAINTENANCE', Decimal('0.0000'))],
    'RETIREMENT':             [('ACQUISITION', Decimal('50.0000')),  ('MAINTENANCE', Decimal('15.0000'))],
    'MORTGAGE':               [('ACQUISITION', Decimal('500.0000')), ('MAINTENANCE', Decimal('50.0000'))],
    'CREDIT_CARD':            [('ACQUISITION', Decimal('0.0000')),   ('MAINTENANCE', Decimal('99.0000'))],
    'VEHICLE_LOAN':           [('ACQUISITION', Decimal('100.0000')), ('MAINTENANCE', Decimal('25.0000'))],
    'STUDENT_LOAN':           [('ACQUISITION', Decimal('50.0000')),  ('MAINTENANCE', Decimal('10.0000'))],
    'HELOC':                  [('ACQUISITION', Decimal('200.0000')), ('MAINTENANCE', Decimal('50.0000'))],
    'PAYDAY':                 [('ACQUISITION', Decimal('15.0000')),  ('MAINTENANCE', Decimal('15.0000'))],
    'COMMERCIAL_CHECKING':    [('ACQUISITION', Decimal('50.0000')),  ('MAINTENANCE', Decimal('25.0000'))],
}

# ── Feature recipe ─────────────────────────────────────────────────────────────
# Each entry specifies which seeded FEATURE row to use (by subtype + classification)
# and what PRODUCT_FEATURE columns to populate.
# 'classification' must match Feature_Classification_Cd exactly as seeded in tier2_core.
# Available subtypes: 'Rate Feature', 'Fee Feature', 'Term Feature', 'Balance Feature',
#                     'Reward Feature', 'Insurance Feature', 'Payment Feature'.
# 'Deposit Feature' is NOT seeded — any entry referencing it would be skipped.

def _rf(classification: str, product_feature_type: str,
        rate: Optional[Decimal] = None,
        amt: Optional[Decimal] = None,
        qty: Optional[Decimal] = None,
        uom: Optional[str] = None) -> Dict:
    return {
        'feature_subtype': RATE_FEATURE_SUBTYPE_CD,
        'classification': classification,
        'product_feature_type': product_feature_type,
        'rate': rate, 'amt': amt, 'qty': qty, 'uom': uom,
    }


def _ff(classification: str, product_feature_type: str,
        rate: Optional[Decimal] = None,
        amt: Optional[Decimal] = None,
        qty: Optional[Decimal] = None,
        uom: Optional[str] = None) -> Dict:
    return {
        'feature_subtype': 'Fee Feature',
        'classification': classification,
        'product_feature_type': product_feature_type,
        'rate': rate, 'amt': amt, 'qty': qty, 'uom': uom,
    }


def _bf(classification: str, product_feature_type: str,
        amt: Optional[Decimal] = None,
        qty: Optional[Decimal] = None,
        uom: Optional[str] = None) -> Dict:
    return {
        'feature_subtype': 'Balance Feature',
        'classification': classification,
        'product_feature_type': product_feature_type,
        'rate': None, 'amt': amt, 'qty': qty, 'uom': uom,
    }


def _rwf(classification: str, product_feature_type: str,
         rate: Optional[Decimal] = None,
         qty: Optional[Decimal] = None,
         uom: Optional[str] = None) -> Dict:
    return {
        'feature_subtype': 'Reward Feature',
        'classification': classification,
        'product_feature_type': product_feature_type,
        'rate': rate, 'amt': None, 'qty': qty, 'uom': uom,
    }


_PRODUCT_FEATURE_RECIPE: Dict[str, List[Dict]] = {
    'CHECKING': [
        _rf('Current Rate',   'rate', rate=Decimal('0.000100000000'), uom='PCT'),
        _ff('Minimum Balance','fee',  amt=Decimal('25.0000'),         uom='USD'),
    ],
    'SAVINGS': [
        _rf('Current Rate',   'rate', rate=Decimal('0.005000000000'), uom='PCT'),
        _bf('Minimum Balance','balance', amt=Decimal('500.0000'),     uom='USD'),
    ],
    'MMA': [
        _rf('Current Rate',   'rate', rate=Decimal('0.010000000000'), uom='PCT'),
        _bf('Minimum Balance','balance', amt=Decimal('1000.0000'),    uom='USD'),
    ],
    'CERTIFICATE_OF_DEPOSIT': [
        _rf('Current Rate',   'rate', rate=Decimal('0.047500000000'), uom='PCT'),
        _ff('Maturity Date',  'fee',  amt=Decimal('50.0000'),         uom='USD'),
    ],
    'RETIREMENT': [
        _rf('Current Rate',   'rate', rate=Decimal('0.040000000000'), uom='PCT'),
    ],
    'MORTGAGE': [
        _rf('Origination Rate',            'rate', rate=Decimal('0.065000000000'), uom='PCT'),
        _rf(ORIGINAL_LOAN_TERM_CLASSIFICATION_CD, 'term', qty=Decimal('30.0000'),  uom='YR'),
    ],
    'CREDIT_CARD': [
        _rf('Current Rate',   'rate', rate=Decimal('0.209900000000'), uom='PCT'),
        _rwf('Current Rate',  'reward', qty=Decimal('1.0000')),
    ],
    'VEHICLE_LOAN': [
        _rf('Origination Rate',            'rate', rate=Decimal('0.069900000000'), uom='PCT'),
        _rf(ORIGINAL_LOAN_TERM_CLASSIFICATION_CD, 'term', qty=Decimal('5.0000'),   uom='YR'),
    ],
    'STUDENT_LOAN': [
        _rf('Origination Rate',            'rate', rate=Decimal('0.055000000000'), uom='PCT'),
        _rf(ORIGINAL_LOAN_TERM_CLASSIFICATION_CD, 'term', qty=Decimal('10.0000'),  uom='YR'),
    ],
    'HELOC': [
        _rf('Current Rate',   'rate', rate=Decimal('0.085000000000'), uom='PCT'),
        _ff('Current Rate',   'fee',  amt=Decimal('75.0000'),         uom='USD'),
    ],
    'PAYDAY': [
        _rf('Current Rate',   'rate', rate=Decimal('0.399000000000'), uom='PCT'),
        _ff('Current Rate',   'fee',  amt=Decimal('15.0000'),         uom='USD'),
    ],
    'COMMERCIAL_CHECKING': [
        _rf('Current Rate',   'rate', rate=Decimal('0.000200000000'), uom='PCT'),
        _ff('Minimum Balance','fee',  amt=Decimal('50.0000'),         uom='USD'),
    ],
}

# ── Upstream prerequisite list ─────────────────────────────────────────────────

_REQUIRED_UPSTREAM_TABLES: Tuple[str, ...] = (
    'Core_DB.AGREEMENT',
    'Core_DB.PRODUCT',
    'Core_DB.FEATURE',
    'Core_DB.CURRENCY',
    'Core_DB.UNIT_OF_MEASURE',
)

# ── DDL column lists (business columns only; DI appended inline below) ─────────
# Column order matches references/07_mvp-schema-reference.md DDL declaration order.
# DI columns are NOT included here — they are appended inline in generate() to
# satisfy both the DDL 3-col tail and the DoD column-order assertions.

_COLS_AGREEMENT_PRODUCT = [
    'Agreement_Id', 'Product_Id', 'Agreement_Product_Role_Cd',
    'Agreement_Product_Start_Dt', 'Agreement_Product_End_Dt',
]

_COLS_PRODUCT_FEATURE = [
    'Product_Id', 'Feature_Id', 'Product_Feature_Type_Cd',
    'Product_Feature_Start_Dttm', 'Product_Feature_End_Dttm',
    'Product_Feature_Amt', 'Product_Feature_Rate', 'Product_Feature_Qty',
    'Product_Feature_Num', 'Currency_Cd', 'Unit_Of_Measure_Cd',
]

_COLS_PRODUCT_COST = [
    'Product_Id', 'Cost_Cd', 'Product_Cost_Amt',
    'Product_Cost_Start_Dttm', 'Product_Cost_End_Dttm',
]

_COLS_PRODUCT_GROUP = [
    'Product_Group_Id', 'Parent_Group_Id', 'Product_Group_Type_Cd',
    'Product_Group_Name', 'Product_Group_Desc',
]

# PRODUCT_TO_GROUP has Valid_* as business columns (DDL-mandated; ⚠️ Conflict A).
_COLS_PRODUCT_TO_GROUP = [
    'PIM_Id', 'Group_Id', 'Valid_From_Dt', 'Valid_To_Dt', 'Del_Ind',
]


# ── Generator ─────────────────────────────────────────────────────────────────

class Tier8ProductHierarchy(BaseGenerator):
    """Produces 5 Core_DB product-hierarchy tables.

    Pure deterministic projection — no RNG, no IdFactory advancement.
    """

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:  # type: ignore[override]
        # ── Guards ────────────────────────────────────────────────────────────
        if not ctx.agreements:
            raise RuntimeError('Tier 8 prerequisite: ctx.agreements is empty')
        if not ctx.customers:
            raise RuntimeError('Tier 8 prerequisite: ctx.customers is empty')
        missing = [t for t in _REQUIRED_UPSTREAM_TABLES if t not in ctx.tables]
        if missing:
            raise RuntimeError(f'Tier 8 prerequisite missing: {missing}')

        # ── Lookup: product_subtype → Product_Id ─────────────────────────────
        product_id_by_subtype: Dict[str, int] = {
            str(row['Product_Subtype_Cd']): int(row['Product_Id'])
            for _, row in ctx.tables['Core_DB.PRODUCT'].iterrows()
        }

        # ── Lookup: (feature_subtype_cd, classification_cd) → Feature_Id ─────
        # setdefault so first-seeded row wins for each key; classification-specific
        # key always takes precedence over subtype-only key in recipe resolution.
        feature_id_map: Dict[Tuple[str, Optional[str]], int] = {}
        for _, row in ctx.tables['Core_DB.FEATURE'].iterrows():
            subtype = str(row['Feature_Subtype_Cd'])
            classif = row['Feature_Classification_Cd']
            classif = str(classif) if classif is not None and not (isinstance(classif, float)) else None
            fid = int(row['Feature_Id'])
            feature_id_map.setdefault((subtype, classif), fid)
            feature_id_map.setdefault((subtype, None), fid)

        # ── Invariant: every agreement's product_id must exist in PRODUCT ─────
        known_product_ids = set(product_id_by_subtype.values())
        bad = [ag.agreement_id for ag in ctx.agreements if ag.product_id not in known_product_ids]
        if bad:
            raise RuntimeError(
                f'Tier 8: {len(bad)} agreements reference unknown product_id — '
                f'universe/PRODUCT mismatch. First offenders: {bad[:5]}'
            )

        # ── Shared datetime anchor ────────────────────────────────────────────
        _hist_start_dttm = datetime.combine(HISTORY_START, time.min)

        # ── AGREEMENT_PRODUCT ─────────────────────────────────────────────────
        ap_rows: List[Dict] = []
        for ag in ctx.agreements:
            ap_rows.append({
                'Agreement_Id':              ag.agreement_id,
                'Product_Id':               ag.product_id,
                'Agreement_Product_Role_Cd': _PRIMARY_ROLE_CD,
                'Agreement_Product_Start_Dt': ag.open_dttm.date(),
                'Agreement_Product_End_Dt': (
                    ag.close_dttm.date() if ag.close_dttm is not None else None
                ),
            })
        df_ap = pd.DataFrame(ap_rows, columns=_COLS_AGREEMENT_PRODUCT)
        df_ap['Agreement_Id'] = df_ap['Agreement_Id'].astype('Int64')
        df_ap['Product_Id']   = df_ap['Product_Id'].astype('Int64')

        # ── PRODUCT_FEATURE ───────────────────────────────────────────────────
        pf_rows: List[Dict] = []
        skipped_pf: List[str] = []
        for _, prod_row in ctx.tables['Core_DB.PRODUCT'].iterrows():
            subtype = str(prod_row['Product_Subtype_Cd'])
            prod_id = int(prod_row['Product_Id'])
            recipe  = _PRODUCT_FEATURE_RECIPE.get(subtype, [])
            built   = 0
            for entry in recipe:
                key = (entry['feature_subtype'], entry.get('classification'))
                fid = feature_id_map.get(key)
                if fid is None:
                    skipped_pf.append(
                        f'{subtype}: {entry["feature_subtype"]}/{entry.get("classification")}'
                    )
                    continue
                pf_rows.append({
                    'Product_Id':               prod_id,
                    'Feature_Id':               fid,
                    'Product_Feature_Type_Cd':   entry['product_feature_type'],
                    'Product_Feature_Start_Dttm': _hist_start_dttm,
                    'Product_Feature_End_Dttm':  None,
                    'Product_Feature_Amt':        entry['amt'],
                    'Product_Feature_Rate':       entry['rate'],
                    'Product_Feature_Qty':        entry['qty'],
                    'Product_Feature_Num':        None,
                    'Currency_Cd': _USD_CURRENCY_CD if entry['amt'] is not None else None,
                    'Unit_Of_Measure_Cd': entry['uom'],
                })
                built += 1
            if built == 0:
                # Fallback: guarantee every product has ≥1 PRODUCT_FEATURE row.
                fallback_fid = feature_id_map.get((RATE_FEATURE_SUBTYPE_CD, 'Current Rate'))
                if fallback_fid is None:
                    raise RuntimeError(
                        f"Tier 8: cannot build PRODUCT_FEATURE for '{subtype}' — "
                        f"'Rate Feature'/'Current Rate' not seeded in Core_DB.FEATURE"
                    )
                pf_rows.append({
                    'Product_Id':               prod_id,
                    'Feature_Id':               fallback_fid,
                    'Product_Feature_Type_Cd':   'rate',
                    'Product_Feature_Start_Dttm': _hist_start_dttm,
                    'Product_Feature_End_Dttm':  None,
                    'Product_Feature_Amt':        None,
                    'Product_Feature_Rate':       Decimal('0.000000000000'),
                    'Product_Feature_Qty':        None,
                    'Product_Feature_Num':        None,
                    'Currency_Cd':                None,
                    'Unit_Of_Measure_Cd':         'PCT',
                })
                skipped_pf.append(f'{subtype}: used fallback Rate Feature row')

        df_pf = pd.DataFrame(pf_rows, columns=_COLS_PRODUCT_FEATURE)
        df_pf['Product_Id'] = df_pf['Product_Id'].astype('Int64')
        df_pf['Feature_Id'] = df_pf['Feature_Id'].astype('Int64')

        # ── PRODUCT_COST ──────────────────────────────────────────────────────
        pc_rows: List[Dict] = []
        for _, prod_row in ctx.tables['Core_DB.PRODUCT'].iterrows():
            subtype = str(prod_row['Product_Subtype_Cd'])
            prod_id = int(prod_row['Product_Id'])
            for cost_cd, cost_amt in _PRODUCT_COST_RECIPE[subtype]:
                pc_rows.append({
                    'Product_Id':            prod_id,
                    'Cost_Cd':               cost_cd,
                    'Product_Cost_Amt':      cost_amt,
                    'Product_Cost_Start_Dttm': _hist_start_dttm,
                    'Product_Cost_End_Dttm': None,
                })
        df_pc = pd.DataFrame(pc_rows, columns=_COLS_PRODUCT_COST)
        df_pc['Product_Id'] = df_pc['Product_Id'].astype('Int64')

        # ── PRODUCT_GROUP ─────────────────────────────────────────────────────
        df_pg = pd.DataFrame(_PRODUCT_GROUP_ROWS, columns=_COLS_PRODUCT_GROUP)
        df_pg['Product_Group_Id'] = df_pg['Product_Group_Id'].astype('Int64')
        df_pg['Parent_Group_Id']  = df_pg['Parent_Group_Id'].astype('Int64')

        # ── PRODUCT_TO_GROUP ──────────────────────────────────────────────────
        # PIM_Id holds Core_DB.Product_Id (DDL column name is legacy; ⚠️ Conflict A).
        ptg_rows: List[Dict] = []
        for _, prod_row in ctx.tables['Core_DB.PRODUCT'].iterrows():
            subtype   = str(prod_row['Product_Subtype_Cd'])
            group_key = _PRODUCT_TO_CLV_GROUP[subtype]
            ptg_rows.append({
                'PIM_Id':       int(prod_row['Product_Id']),
                'Group_Id':     _PRODUCT_GROUP_IDS[group_key],
                'Valid_From_Dt': _TIER8_VALID_FROM_DT,
                'Valid_To_Dt':   HIGH_DATE,
                'Del_Ind':      'N',
            })
        df_ptg = pd.DataFrame(ptg_rows, columns=_COLS_PRODUCT_TO_GROUP)
        df_ptg['PIM_Id']   = df_ptg['PIM_Id'].astype('Int64')
        df_ptg['Group_Id'] = df_ptg['Group_Id'].astype('Int64')

        # ── DI stamping — INLINE only ─────────────────────────────────────────
        # stamp_di() appends 5 columns (di_data_src_cd, di_start_ts, di_proc_name,
        # di_rec_deleted_Ind, di_end_ts) in that order, which does not match the DDL
        # 3-col tail (di_start_ts, di_end_ts, di_rec_deleted_Ind) for the 4 standard
        # tables. Inline assignment preserves the correct DDL column order and satisfies
        # the DoD assertion 'di_data_src_cd' not in df.columns.

        for df in (df_ap, df_pf, df_pc, df_pg):
            df['di_start_ts']        = _TIER8_DI_START_TS
            df['di_end_ts']          = HIGH_TS
            df['di_rec_deleted_Ind'] = 'N'

        # PRODUCT_TO_GROUP: non-standard 5-col DI tail per DDL §8436 (⚠️ Conflict A).
        df_ptg['di_data_src_cd']     = None
        df_ptg['di_start_ts']        = _TIER8_DI_START_TS
        df_ptg['di_proc_name']       = None
        df_ptg['di_rec_deleted_Ind'] = 'N'
        df_ptg['di_end_ts']          = HIGH_TS

        return {
            'Core_DB.AGREEMENT_PRODUCT': df_ap,
            'Core_DB.PRODUCT_FEATURE':   df_pf,
            'Core_DB.PRODUCT_COST':      df_pc,
            'Core_DB.PRODUCT_GROUP':     df_pg,
            'Core_DB.PRODUCT_TO_GROUP':  df_ptg,
        }

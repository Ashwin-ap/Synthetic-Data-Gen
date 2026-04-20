from __future__ import annotations

from typing import Dict, List, Tuple, TYPE_CHECKING

import pandas as pd

from config import settings
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ---------------------------------------------------------------------------
# DI / Valid sentinels
# ---------------------------------------------------------------------------

_PIM_DI_START_TS   = '2000-01-01 00:00:00.000000'
_PIM_VALID_FROM_DT = str(settings.HISTORY_START)   # '2025-10-01'

# ---------------------------------------------------------------------------
# DDL column order (business columns only; DI/Valid appended by stamp_*)
# ---------------------------------------------------------------------------

_COLS_PRODUCT_GROUP_TYPE: List[str] = [
    'Product_Group_Type_Cd',
    'Product_Group_Type_Name',
    'Product_Group_Type_Desc',
]

_COLS_PRODUCT_GROUP: List[str] = [
    'Product_Group_Id',
    'Parent_Group_Id',
    'Product_Group_Type_Cd',
]

_COLS_PRODUCT_PARAMETER_TYPE: List[str] = [
    'PIM_Parameter_Type_Cd',
    'PIM_Parameter_Type_Desc',
]

_COLS_PRODUCT: List[str] = [
    'PIM_Id',
    'Product_Id',
    'PIM_Product_Name',
    'PIM_Product_Desc',
]

_COLS_PRODUCT_TO_GROUP: List[str] = [
    'PIM_Id',
    'Group_Id',
]

_COLS_PRODUCT_PARAMETERS: List[str] = [
    'PIM_Parameter_Id',
    'PIM_Id',
    'PIM_Parameter_Type_Cd',
    'PIM_Parameter_Value',
]

# ---------------------------------------------------------------------------
# CLV group hierarchy
# ---------------------------------------------------------------------------

_CLV_GROUPS: List[str] = [
    'Checking',
    'Savings',
    'Retirement',
    'Credit Card',
    'Vehicle Loan',
    'Mortgage',
    'Investments',
    'Insurance',
]

# Total function — every Product_Subtype_Cd that can appear in Core_DB.PRODUCT
# must appear here.  generate() raises ValueError on any miss.
_PRODUCT_TYPE_TO_CLV_GROUP: Dict[str, str] = {
    'CHECKING':               'Checking',
    'COMMERCIAL_CHECKING':    'Checking',
    'SAVINGS':                'Savings',
    'MMA':                    'Savings',
    'CERTIFICATE_OF_DEPOSIT': 'Savings',
    'RETIREMENT':             'Retirement',
    'CREDIT_CARD':            'Credit Card',
    'VEHICLE_LOAN':           'Vehicle Loan',
    'STUDENT_LOAN':           'Vehicle Loan',
    'PAYDAY':                 'Vehicle Loan',
    'MORTGAGE':               'Mortgage',
    'HELOC':                  'Mortgage',
}

# Deterministic parameter values per product subtype.
# Tuple = (PIM_Parameter_Type_Cd, PIM_Parameter_Value string).
# No RNG consumed — same inputs always produce the same rows.
_PRODUCT_PARAMETERS_BY_TYPE: Dict[str, List[Tuple[int, str]]] = {
    'CHECKING':               [(1, '500.00'),  (2, '0.0005'), (3, '15.00')],
    'COMMERCIAL_CHECKING':    [(1, '1000.00'), (2, '0.0003'), (3, '25.00')],
    'SAVINGS':                [(1, '100.00'),  (2, '0.0200'), (3, '5.00')],
    'MMA':                    [(1, '2500.00'), (2, '0.0450'), (3, '10.00')],
    'CERTIFICATE_OF_DEPOSIT': [(1, '1000.00'), (2, '0.0500'), (3, '0.00'), (4, '12')],
    'RETIREMENT':             [(1, '500.00'),  (2, '0.0700')],
    'CREDIT_CARD':            [(2, '0.1999'),  (3, '99.00'),  (5, '5000.00')],
    'VEHICLE_LOAN':           [(2, '0.0699'),  (3, '250.00'), (4, '60')],
    'STUDENT_LOAN':           [(2, '0.0540'),  (3, '0.00'),   (4, '120')],
    'PAYDAY':                 [(2, '0.3600'),  (3, '15.00'),  (4, '1')],
    'MORTGAGE':               [(2, '0.0699'),  (3, '1500.00'), (4, '360')],
    'HELOC':                  [(2, '0.0750'),  (3, '75.00'),  (4, '120')],
}


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class Tier15PIM(BaseGenerator):
    """Generates all 6 PIM_DB tables from Core_DB.PRODUCT."""

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        core_prod = ctx.tables['Core_DB.PRODUCT'].copy()

        df_pgt                   = self._build_product_group_type()
        df_pg, clv_name_to_gid   = self._build_product_group(ctx)
        df_ppt                   = self._build_product_parameter_type()
        df_prod, subtype_to_pim  = self._build_product(ctx, core_prod)
        df_p2g                   = self._build_product_to_group(
                                       df_prod, core_prod, clv_name_to_gid)
        df_pp                    = self._build_product_parameters(
                                       ctx, df_prod, core_prod)

        tables: Dict[str, pd.DataFrame] = {
            'PIM_DB.PRODUCT_GROUP_TYPE':     df_pgt,
            'PIM_DB.PRODUCT_GROUP':          df_pg,
            'PIM_DB.PRODUCT_PARAMETER_TYPE': df_ppt,
            'PIM_DB.PRODUCT':                df_prod,
            'PIM_DB.PRODUCT_TO_GROUP':       df_p2g,
            'PIM_DB.PRODUCT_PARAMETERS':     df_pp,
        }

        result: Dict[str, pd.DataFrame] = {}
        for key, df in tables.items():
            df = self.stamp_di(df, start_ts=_PIM_DI_START_TS)
            df = self.stamp_valid(df, from_dt=_PIM_VALID_FROM_DT)
            result[key] = df

        return result

    # ------------------------------------------------------------------
    # Private builders
    # ------------------------------------------------------------------

    def _build_product_group_type(self) -> pd.DataFrame:
        rows = [
            {
                'Product_Group_Type_Cd':   1,
                'Product_Group_Type_Name': 'ROOT',
                'Product_Group_Type_Desc': 'Root product grouping',
            },
            {
                'Product_Group_Type_Cd':   2,
                'Product_Group_Type_Name': 'CLV_TYPE',
                'Product_Group_Type_Desc': 'CLV product type grouping',
            },
        ]
        df = pd.DataFrame(rows, columns=_COLS_PRODUCT_GROUP_TYPE)
        df['Product_Group_Type_Cd'] = df['Product_Group_Type_Cd'].astype('Int64')
        return df

    def _build_product_group(
        self, ctx: 'GenerationContext'
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        rows = []

        root_id = ctx.ids.next('group_id')
        rows.append({
            'Product_Group_Id':      root_id,
            'Parent_Group_Id':       root_id,   # self-reference — Q3
            'Product_Group_Type_Cd': 1,
        })

        clv_name_to_gid: Dict[str, int] = {}
        for name in _CLV_GROUPS:
            gid = ctx.ids.next('group_id')
            clv_name_to_gid[name] = gid
            rows.append({
                'Product_Group_Id':      gid,
                'Parent_Group_Id':       root_id,
                'Product_Group_Type_Cd': 2,
            })

        df = pd.DataFrame(rows, columns=_COLS_PRODUCT_GROUP)
        for col in ('Product_Group_Id', 'Parent_Group_Id', 'Product_Group_Type_Cd'):
            df[col] = df[col].astype('Int64')

        return df, clv_name_to_gid

    def _build_product_parameter_type(self) -> pd.DataFrame:
        desc_map = {
            1: 'Minimum balance requirement',
            2: 'Annual interest rate',
            3: 'Periodic fee amount',
            4: 'Term length in months',
            5: 'Maximum credit limit',
        }
        rows = [
            {'PIM_Parameter_Type_Cd': cd, 'PIM_Parameter_Type_Desc': desc_map[cd]}
            for cd in range(1, 6)
        ]
        df = pd.DataFrame(rows, columns=_COLS_PRODUCT_PARAMETER_TYPE)
        df['PIM_Parameter_Type_Cd'] = df['PIM_Parameter_Type_Cd'].astype('Int64')
        return df

    def _build_product(
        self,
        ctx: 'GenerationContext',
        core_prod: pd.DataFrame,
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        rows = []
        subtype_to_pim_id: Dict[str, int] = {}

        for _, row in core_prod.iterrows():
            pim_id  = ctx.ids.next('pim_id')
            subtype = row['Product_Subtype_Cd']
            name    = row.get('Product_Name') or None
            if not name:
                name = subtype.replace('_', ' ').title()

            subtype_to_pim_id[subtype] = pim_id
            rows.append({
                'PIM_Id':           pim_id,
                'Product_Id':       int(row['Product_Id']),
                'PIM_Product_Name': name,
                'PIM_Product_Desc': None,
            })

        df = pd.DataFrame(rows, columns=_COLS_PRODUCT)
        df['PIM_Id']     = df['PIM_Id'].astype('Int64')
        df['Product_Id'] = df['Product_Id'].astype('Int64')
        return df, subtype_to_pim_id

    def _build_product_to_group(
        self,
        product_df: pd.DataFrame,
        core_prod: pd.DataFrame,
        clv_name_to_gid: Dict[str, int],
    ) -> pd.DataFrame:
        pid_to_subtype: Dict[int, str] = {
            int(r['Product_Id']): r['Product_Subtype_Cd']
            for _, r in core_prod.iterrows()
        }

        rows = []
        for _, row in product_df.iterrows():
            prod_id = int(row['Product_Id'])
            subtype = pid_to_subtype[prod_id]

            clv_name = _PRODUCT_TYPE_TO_CLV_GROUP.get(subtype)
            if clv_name is None:
                raise ValueError(f'unmapped product subtype: {subtype}')

            rows.append({
                'PIM_Id':   int(row['PIM_Id']),
                'Group_Id': clv_name_to_gid[clv_name],
            })

        df = pd.DataFrame(rows, columns=_COLS_PRODUCT_TO_GROUP)
        df['PIM_Id']   = df['PIM_Id'].astype('Int64')
        df['Group_Id'] = df['Group_Id'].astype('Int64')
        return df

    def _build_product_parameters(
        self,
        ctx: 'GenerationContext',
        product_df: pd.DataFrame,
        core_prod: pd.DataFrame,
    ) -> pd.DataFrame:
        pid_to_subtype: Dict[int, str] = {
            int(r['Product_Id']): r['Product_Subtype_Cd']
            for _, r in core_prod.iterrows()
        }

        rows = []
        for _, row in product_df.iterrows():
            pim_id  = int(row['PIM_Id'])
            subtype = pid_to_subtype[int(row['Product_Id'])]
            params  = _PRODUCT_PARAMETERS_BY_TYPE.get(subtype, [])

            for type_cd, value_str in params:
                rows.append({
                    'PIM_Parameter_Id':      ctx.ids.next('pim_parameter'),
                    'PIM_Id':                pim_id,
                    'PIM_Parameter_Type_Cd': type_cd,
                    'PIM_Parameter_Value':   value_str,
                })

        df = pd.DataFrame(rows, columns=_COLS_PRODUCT_PARAMETERS)
        df['PIM_Parameter_Id']      = df['PIM_Parameter_Id'].astype('Int64')
        df['PIM_Id']                = df['PIM_Id'].astype('Int64')
        df['PIM_Parameter_Type_Cd'] = df['PIM_Parameter_Type_Cd'].astype('Int64')
        return df

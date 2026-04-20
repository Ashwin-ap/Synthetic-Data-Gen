from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Dict, List, Tuple

import pandas as pd

from config.settings import HIGH_DATE, SELF_EMP_ORG_ID, SIM_DATE
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ── Module-level constants ────────────────────────────────────────────────────

_TIER4B_DI_START_TS = '2000-01-01 00:00:00.000000'

_NAME_TYPE_CDS: Tuple[str, ...] = (
    'brand name', 'business name', 'legal name', 'registered name'
)

_PRIMARY_YES = 'Yes'
_PRIMARY_NO  = 'No'  # declared for reference; not emitted in this step

_REQUIRED_TIER0_TABLES: Tuple[str, ...] = (
    'Core_DB.NAICS_INDUSTRY',
    'Core_DB.NACE_CLASS',
    'Core_DB.SIC',
    'Core_DB.GICS_SUBINDUSTRY_TYPE',
)
_REQUIRED_TIER3_TABLES: Tuple[str, ...] = ('Core_DB.ORGANIZATION',)

_COLS_ORGANIZATION_NAICS: List[str] = [
    'Organization_Party_Id', 'NAICS_National_Industry_Cd', 'Organization_NAICS_Start_Dt',
    'NAICS_Sector_Cd', 'NAICS_Subsector_Cd', 'NAICS_Industry_Group_Cd', 'NAICS_Industry_Cd',
    'Organization_NAICS_End_Dt', 'Primary_NAICS_Ind',
]
_COLS_ORGANIZATION_NACE: List[str] = [
    'Organization_Party_Id', 'NACE_Class_Cd', 'NACE_Group_Cd', 'NACE_Division_Cd',
    'NACE_Section_Cd', 'Organization_NACE_Start_Dt', 'Organization_NACE_End_Dt',
    'Importance_Order_NACE_Num',
]
_COLS_ORGANIZATION_SIC: List[str] = [
    'Organization_Party_Id', 'SIC_Cd', 'Organization_SIC_Start_Dt',
    'Organization_SIC_End_Dt', 'Primary_SIC_Ind',
]
_COLS_ORGANIZATION_GICS: List[str] = [
    'Organization_Party_Id', 'GICS_Subindustry_Cd', 'GICS_Industry_Cd',
    'GICS_Industry_Group_Cd', 'GICS_Sector_Cd', 'Organization_GICS_Start_Dt',
    'Organization_GICS_End_Dt', 'Primary_GICS_Ind',
]
_COLS_ORGANIZATION_NAME: List[str] = [
    'Organization_Party_Id', 'Name_Type_Cd', 'Organization_Name_Start_Dt',
    'Organization_Name', 'Organization_Name_Desc', 'Organization_Name_End_Dt',
]


class Tier4bOrganization(BaseGenerator):
    """Generates 5 Core_DB organization-attribute tables for every real ORGANIZATION row."""

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # ── Guards ────────────────────────────────────────────────────────────
        if not ctx.customers:
            raise RuntimeError(
                'Tier4bOrganization requires a populated ctx.customers — '
                'run UniverseBuilder.build() first'
            )
        for key in _REQUIRED_TIER0_TABLES + _REQUIRED_TIER3_TABLES:
            if key not in ctx.tables:
                raise RuntimeError(
                    f'Tier4bOrganization requires {key} to be loaded first'
                )
        org_cps = [cp for cp in ctx.customers if cp.party_type == 'ORGANIZATION']
        if not org_cps:
            raise RuntimeError(
                'Tier4bOrganization requires at least one ORGANIZATION '
                'CustomerProfile — universe has none'
            )

        # ── Pre-compute lookup pools ──────────────────────────────────────────
        naics_df = ctx.tables.get('Core_DB.NAICS_INDUSTRY')
        nace_df  = ctx.tables.get('Core_DB.NACE_CLASS')
        gics_df  = ctx.tables.get('Core_DB.GICS_SUBINDUSTRY_TYPE')
        sic_df   = ctx.tables.get('Core_DB.SIC')

        # SIC_Cd override: cp.sic_cd is not guaranteed to match the seeded pool
        sic_codes: List[str] = sorted(sic_df['SIC_Cd'].tolist())

        # NAICS_National_Industry_Cd synthesised from NAICS_Industry_Cd (no separate seed)
        naics_by_sector: Dict[str, List[Tuple]] = {}
        for sec, grp in naics_df.groupby('NAICS_Sector_Cd'):
            pool = sorted(zip(
                grp['NAICS_Industry_Cd'],        # national_industry_cd (synthesised)
                grp['NAICS_Industry_Cd'],        # industry_cd
                grp['NAICS_Industry_Group_Cd'],
                grp['NAICS_Subsector_Cd'],
                grp['NAICS_Sector_Cd'],
            ))
            naics_by_sector[str(sec)] = pool
        _naics_fallback = sorted(t for lst in naics_by_sector.values() for t in lst)

        gics_by_sector: Dict[str, List[Tuple]] = {}
        for sec, grp in gics_df.groupby('GICS_Sector_Cd'):
            pool = sorted(zip(
                grp['GICS_Subindustry_Cd'],
                grp['GICS_Industry_Cd'],
                grp['GICS_Industry_Group_Cd'],
                grp['GICS_Sector_Cd'],
            ))
            gics_by_sector[str(sec)] = pool
        _gics_fallback = sorted(t for lst in gics_by_sector.values() for t in lst)

        nace_rows: List[Tuple] = sorted(zip(
            nace_df['NACE_Class_Cd'], nace_df['NACE_Group_Cd'],
            nace_df['NACE_Division_Cd'], nace_df['NACE_Section_Cd'],
        ))

        def pick(pool, key: int):
            return pool[key % len(pool)]

        # ── ORGANIZATION_NAME (4 rows per org) ────────────────────────────────
        rows_name = []
        for cp in org_cps:
            for nt in _NAME_TYPE_CDS:
                rows_name.append({
                    'Organization_Party_Id':      cp.party_id,
                    'Name_Type_Cd':               nt,
                    'Organization_Name_Start_Dt': cp.party_since,
                    'Organization_Name':          cp.org_name,
                    'Organization_Name_Desc':     None,
                    'Organization_Name_End_Dt':   None,
                })
        df_name = pd.DataFrame(rows_name, columns=_COLS_ORGANIZATION_NAME)
        df_name['Organization_Party_Id'] = df_name['Organization_Party_Id'].astype('Int64')
        df_name = self.stamp_di(df_name, start_ts=_TIER4B_DI_START_TS)

        # ── ORGANIZATION_NAICS (1 row per org) ────────────────────────────────
        rows_naics = []
        for cp in org_cps:
            pool = naics_by_sector.get(cp.naics_sector_cd) or _naics_fallback
            nat_ind, ind, grp, sub, sec = pick(pool, cp.party_id)
            rows_naics.append({
                'Organization_Party_Id':       cp.party_id,
                'NAICS_National_Industry_Cd':  nat_ind,
                'Organization_NAICS_Start_Dt': cp.party_since,
                'NAICS_Sector_Cd':             sec,
                'NAICS_Subsector_Cd':          sub,
                'NAICS_Industry_Group_Cd':     grp,
                'NAICS_Industry_Cd':           ind,
                'Organization_NAICS_End_Dt':   None,
                'Primary_NAICS_Ind':           _PRIMARY_YES,
            })
        df_naics = pd.DataFrame(rows_naics, columns=_COLS_ORGANIZATION_NAICS)
        df_naics['Organization_Party_Id'] = df_naics['Organization_Party_Id'].astype('Int64')
        df_naics = self.stamp_di(df_naics, start_ts=_TIER4B_DI_START_TS)

        # ── ORGANIZATION_NACE (1 row per org) ─────────────────────────────────
        rows_nace = []
        for cp in org_cps:
            cls, grp, div, sec = pick(nace_rows, cp.party_id)
            rows_nace.append({
                'Organization_Party_Id':      cp.party_id,
                'NACE_Class_Cd':              cls,
                'NACE_Group_Cd':              grp,
                'NACE_Division_Cd':           div,
                'NACE_Section_Cd':            sec,
                'Organization_NACE_Start_Dt': cp.party_since,
                'Organization_NACE_End_Dt':   None,
                'Importance_Order_NACE_Num':  '1',
            })
        df_nace = pd.DataFrame(rows_nace, columns=_COLS_ORGANIZATION_NACE)
        df_nace['Organization_Party_Id'] = df_nace['Organization_Party_Id'].astype('Int64')
        df_nace = self.stamp_di(df_nace, start_ts=_TIER4B_DI_START_TS)

        # ── ORGANIZATION_SIC (1 row per org) ──────────────────────────────────
        rows_sic = []
        for cp in org_cps:
            rows_sic.append({
                'Organization_Party_Id':    cp.party_id,
                'SIC_Cd':                   pick(sic_codes, cp.party_id),
                'Organization_SIC_Start_Dt': cp.party_since,
                'Organization_SIC_End_Dt':  None,
                'Primary_SIC_Ind':          _PRIMARY_YES,
            })
        df_sic = pd.DataFrame(rows_sic, columns=_COLS_ORGANIZATION_SIC)
        df_sic['Organization_Party_Id'] = df_sic['Organization_Party_Id'].astype('Int64')
        df_sic = self.stamp_di(df_sic, start_ts=_TIER4B_DI_START_TS)

        # ── ORGANIZATION_GICS (1 row per org) ─────────────────────────────────
        rows_gics = []
        for cp in org_cps:
            pool = gics_by_sector.get(cp.gics_sector_cd) or _gics_fallback
            sub, ind, grp, sec = pick(pool, cp.party_id)
            rows_gics.append({
                'Organization_Party_Id':       cp.party_id,
                'GICS_Subindustry_Cd':         sub,
                'GICS_Industry_Cd':            ind,
                'GICS_Industry_Group_Cd':      grp,
                'GICS_Sector_Cd':              sec,
                'Organization_GICS_Start_Dt':  cp.party_since,
                'Organization_GICS_End_Dt':    None,
                'Primary_GICS_Ind':            _PRIMARY_YES,
            })
        df_gics = pd.DataFrame(rows_gics, columns=_COLS_ORGANIZATION_GICS)
        df_gics['Organization_Party_Id'] = df_gics['Organization_Party_Id'].astype('Int64')
        df_gics = self.stamp_di(df_gics, start_ts=_TIER4B_DI_START_TS)

        return {
            'Core_DB.ORGANIZATION_NAME':  df_name,
            'Core_DB.ORGANIZATION_NAICS': df_naics,
            'Core_DB.ORGANIZATION_NACE':  df_nace,
            'Core_DB.ORGANIZATION_SIC':   df_sic,
            'Core_DB.ORGANIZATION_GICS':  df_gics,
        }

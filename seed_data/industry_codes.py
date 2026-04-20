import pandas as pd
from typing import Dict

_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}

# ── NAICS_INDUSTRY ────────────────────────────────────────────────────────────
# DDL has 4 NOT-NULL code columns (Sector→Subsector→Industry_Group→Industry_Cd).
# The bridge ORGANIZATION_NAICS carries NAICS_National_Industry_Cd separately;
# that column does not exist in this parent table per the 07 DDL.
# Covers required sectors: 52 (Finance), 62 (Health Care), 44/45 (Retail), 51 (Info),
#                          72 (Accommodation & Food), 81 (Other Services)
_cols_naics_industry = [
    'NAICS_Industry_Cd', 'NAICS_Sector_Cd', 'NAICS_Subsector_Cd',
    'NAICS_Industry_Group_Cd', 'NAICS_Industry_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_naics_industry_rows = [
    # Sector 52 — Finance & Insurance
    {'NAICS_Industry_Cd': '52211', 'NAICS_Sector_Cd': '52', 'NAICS_Subsector_Cd': '522', 'NAICS_Industry_Group_Cd': '5221', 'NAICS_Industry_Desc': 'Commercial Banking', **_DI},
    {'NAICS_Industry_Cd': '52213', 'NAICS_Sector_Cd': '52', 'NAICS_Subsector_Cd': '522', 'NAICS_Industry_Group_Cd': '5221', 'NAICS_Industry_Desc': 'Credit Unions', **_DI},
    {'NAICS_Industry_Cd': '52232', 'NAICS_Sector_Cd': '52', 'NAICS_Subsector_Cd': '522', 'NAICS_Industry_Group_Cd': '5223', 'NAICS_Industry_Desc': 'Financial Transactions Processing, Reserve, and Clearinghouse Activities', **_DI},
    # Sector 62 — Health Care & Social Assistance
    {'NAICS_Industry_Cd': '62111', 'NAICS_Sector_Cd': '62', 'NAICS_Subsector_Cd': '621', 'NAICS_Industry_Group_Cd': '6211', 'NAICS_Industry_Desc': 'Offices of Physicians', **_DI},
    # Sector 44 — Retail Trade (Motor Vehicle & Parts)
    {'NAICS_Industry_Cd': '44111', 'NAICS_Sector_Cd': '44', 'NAICS_Subsector_Cd': '441', 'NAICS_Industry_Group_Cd': '4411', 'NAICS_Industry_Desc': 'New Car Dealers', **_DI},
    # Sector 45 — Retail Trade (General Merchandise)
    {'NAICS_Industry_Cd': '45211', 'NAICS_Sector_Cd': '45', 'NAICS_Subsector_Cd': '452', 'NAICS_Industry_Group_Cd': '4521', 'NAICS_Industry_Desc': 'Department Stores', **_DI},
    # Sector 51 — Information
    {'NAICS_Industry_Cd': '51121', 'NAICS_Sector_Cd': '51', 'NAICS_Subsector_Cd': '511', 'NAICS_Industry_Group_Cd': '5112', 'NAICS_Industry_Desc': 'Software Publishers', **_DI},
    # Sector 72 — Accommodation & Food Services
    {'NAICS_Industry_Cd': '72211', 'NAICS_Sector_Cd': '72', 'NAICS_Subsector_Cd': '722', 'NAICS_Industry_Group_Cd': '7221', 'NAICS_Industry_Desc': 'Full-Service Restaurants', **_DI},
    # Sector 81 — Other Services (except Public Administration)
    {'NAICS_Industry_Cd': '81211', 'NAICS_Sector_Cd': '81', 'NAICS_Subsector_Cd': '812', 'NAICS_Industry_Group_Cd': '8121', 'NAICS_Industry_Desc': 'Hair, Nail, and Skin Care Services', **_DI},
]

# ── NACE_CLASS ────────────────────────────────────────────────────────────────
# 4 NOT-NULL code columns: Class→Group→Division→Section
# Covers sections A (Agriculture), C (Manufacturing), G (Wholesale & Retail),
#               K (Financial & Insurance), N (Administrative & Support)
_cols_nace_class = [
    'NACE_Class_Cd', 'NACE_Group_Cd', 'NACE_Division_Cd', 'NACE_Section_Cd', 'NACE_Class_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_nace_class_rows = [
    # Section A — Agriculture, Forestry, Fishing
    {'NACE_Class_Cd': '0111', 'NACE_Group_Cd': '01.1', 'NACE_Division_Cd': '01', 'NACE_Section_Cd': 'A', 'NACE_Class_Desc': 'Growing of cereals (except rice), leguminous crops and oil seeds', **_DI},
    # Section C — Manufacturing
    {'NACE_Class_Cd': '1011', 'NACE_Group_Cd': '10.1', 'NACE_Division_Cd': '10', 'NACE_Section_Cd': 'C', 'NACE_Class_Desc': 'Processing and preserving of meat', **_DI},
    # Section G — Wholesale and Retail Trade
    {'NACE_Class_Cd': '4611', 'NACE_Group_Cd': '46.1', 'NACE_Division_Cd': '46', 'NACE_Section_Cd': 'G', 'NACE_Class_Desc': 'Agents involved in the sale of agricultural raw materials, live animals, textile raw materials and agricultural semi-finished goods', **_DI},
    # Section K — Financial and Insurance Activities
    {'NACE_Class_Cd': '6411', 'NACE_Group_Cd': '64.1', 'NACE_Division_Cd': '64', 'NACE_Section_Cd': 'K', 'NACE_Class_Desc': 'Central banking', **_DI},
    {'NACE_Class_Cd': '6419', 'NACE_Group_Cd': '64.1', 'NACE_Division_Cd': '64', 'NACE_Section_Cd': 'K', 'NACE_Class_Desc': 'Other monetary intermediation', **_DI},
    # Section N — Administrative and Support Service Activities
    {'NACE_Class_Cd': '7810', 'NACE_Group_Cd': '78.1', 'NACE_Division_Cd': '78', 'NACE_Section_Cd': 'N', 'NACE_Class_Desc': 'Activities of employment placement agencies', **_DI},
]

# ── SIC ───────────────────────────────────────────────────────────────────────
# SIC_Group_Cd = 2-digit major group code
# Covers divisions H (Finance), I (Services), F (Retail Trade)
_cols_sic = [
    'SIC_Cd', 'SIC_Desc', 'SIC_Group_Cd',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_sic_rows = [
    # Division H — Finance, Insurance, and Real Estate
    {'SIC_Cd': '6020', 'SIC_Desc': 'State Commercial Banks and Trust Companies', 'SIC_Group_Cd': '60', **_DI},
    {'SIC_Cd': '6110', 'SIC_Desc': 'Federal and Federally-Sponsored Credit Agencies', 'SIC_Group_Cd': '61', **_DI},
    {'SIC_Cd': '6120', 'SIC_Desc': 'Savings Institutions, Federally Chartered', 'SIC_Group_Cd': '61', **_DI},
    {'SIC_Cd': '6140', 'SIC_Desc': 'Personal Credit Institutions', 'SIC_Group_Cd': '61', **_DI},
    {'SIC_Cd': '6211', 'SIC_Desc': 'Security Brokers, Dealers, and Flotation Companies', 'SIC_Group_Cd': '62', **_DI},
    {'SIC_Cd': '6311', 'SIC_Desc': 'Life Insurance', 'SIC_Group_Cd': '63', **_DI},
    # Division I — Services
    {'SIC_Cd': '7011', 'SIC_Desc': 'Hotels and Motels', 'SIC_Group_Cd': '70', **_DI},
    {'SIC_Cd': '8011', 'SIC_Desc': 'Offices and Clinics of Doctors of Medicine', 'SIC_Group_Cd': '80', **_DI},
    {'SIC_Cd': '8021', 'SIC_Desc': 'Offices and Clinics of Dentists', 'SIC_Group_Cd': '80', **_DI},
    {'SIC_Cd': '8049', 'SIC_Desc': 'Offices of Other Health Practitioners', 'SIC_Group_Cd': '80', **_DI},
    # Division F — Retail Trade
    {'SIC_Cd': '5411', 'SIC_Desc': 'Grocery Stores', 'SIC_Group_Cd': '54', **_DI},
    {'SIC_Cd': '5511', 'SIC_Desc': 'New and Used Car Dealers', 'SIC_Group_Cd': '55', **_DI},
]

# ── GICS_SECTOR_TYPE ──────────────────────────────────────────────────────────
# All 11 GICS sectors required
_cols_gics_sector_type = [
    'GICS_Sector_Cd', 'GICS_Sector_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_gics_sector_type_rows = [
    {'GICS_Sector_Cd': '10', 'GICS_Sector_Desc': 'Energy',                   **_DI},
    {'GICS_Sector_Cd': '15', 'GICS_Sector_Desc': 'Materials',                **_DI},
    {'GICS_Sector_Cd': '20', 'GICS_Sector_Desc': 'Industrials',              **_DI},
    {'GICS_Sector_Cd': '25', 'GICS_Sector_Desc': 'Consumer Discretionary',   **_DI},
    {'GICS_Sector_Cd': '30', 'GICS_Sector_Desc': 'Consumer Staples',         **_DI},
    {'GICS_Sector_Cd': '35', 'GICS_Sector_Desc': 'Health Care',              **_DI},
    {'GICS_Sector_Cd': '40', 'GICS_Sector_Desc': 'Financials',               **_DI},
    {'GICS_Sector_Cd': '45', 'GICS_Sector_Desc': 'Information Technology',   **_DI},
    {'GICS_Sector_Cd': '50', 'GICS_Sector_Desc': 'Communication Services',   **_DI},
    {'GICS_Sector_Cd': '55', 'GICS_Sector_Desc': 'Utilities',                **_DI},
    {'GICS_Sector_Cd': '60', 'GICS_Sector_Desc': 'Real Estate',              **_DI},
]

# ── GICS_INDUSTRY_GROUP_TYPE ──────────────────────────────────────────────────
# One industry group per sector; GICS_Sector_Cd FKs to GICS_SECTOR_TYPE
_cols_gics_industry_group_type = [
    'GICS_Industry_Group_Cd', 'GICS_Sector_Cd', 'GICS_Industry_Group_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_gics_industry_group_type_rows = [
    {'GICS_Industry_Group_Cd': '1010', 'GICS_Sector_Cd': '10', 'GICS_Industry_Group_Desc': 'Energy',                                               **_DI},
    {'GICS_Industry_Group_Cd': '1510', 'GICS_Sector_Cd': '15', 'GICS_Industry_Group_Desc': 'Materials',                                            **_DI},
    {'GICS_Industry_Group_Cd': '2010', 'GICS_Sector_Cd': '20', 'GICS_Industry_Group_Desc': 'Capital Goods',                                        **_DI},
    {'GICS_Industry_Group_Cd': '2510', 'GICS_Sector_Cd': '25', 'GICS_Industry_Group_Desc': 'Automobiles And Components',                           **_DI},
    {'GICS_Industry_Group_Cd': '3010', 'GICS_Sector_Cd': '30', 'GICS_Industry_Group_Desc': 'Food Beverage And Tobacco',                            **_DI},
    {'GICS_Industry_Group_Cd': '3510', 'GICS_Sector_Cd': '35', 'GICS_Industry_Group_Desc': 'Pharmaceuticals Biotechnology And Life Sciences',      **_DI},
    {'GICS_Industry_Group_Cd': '4010', 'GICS_Sector_Cd': '40', 'GICS_Industry_Group_Desc': 'Banks',                                               **_DI},
    {'GICS_Industry_Group_Cd': '4510', 'GICS_Sector_Cd': '45', 'GICS_Industry_Group_Desc': 'Software And Services',                               **_DI},
    {'GICS_Industry_Group_Cd': '5010', 'GICS_Sector_Cd': '50', 'GICS_Industry_Group_Desc': 'Telecommunication Services',                          **_DI},
    {'GICS_Industry_Group_Cd': '5510', 'GICS_Sector_Cd': '55', 'GICS_Industry_Group_Desc': 'Utilities',                                           **_DI},
    {'GICS_Industry_Group_Cd': '6010', 'GICS_Sector_Cd': '60', 'GICS_Industry_Group_Desc': 'Equity Real Estate Investment Trusts',                **_DI},
]

# ── GICS_INDUSTRY_TYPE ────────────────────────────────────────────────────────
# (GICS_Industry_Group_Cd, GICS_Sector_Cd) FKs to GICS_INDUSTRY_GROUP_TYPE
_cols_gics_industry_type = [
    'GICS_Industry_Cd', 'GICS_Industry_Group_Cd', 'GICS_Sector_Cd', 'GICS_Industry_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_gics_industry_type_rows = [
    {'GICS_Industry_Cd': '101010', 'GICS_Industry_Group_Cd': '1010', 'GICS_Sector_Cd': '10', 'GICS_Industry_Desc': 'Energy Equipment And Services',                        **_DI},
    {'GICS_Industry_Cd': '151010', 'GICS_Industry_Group_Cd': '1510', 'GICS_Sector_Cd': '15', 'GICS_Industry_Desc': 'Chemicals',                                            **_DI},
    {'GICS_Industry_Cd': '201010', 'GICS_Industry_Group_Cd': '2010', 'GICS_Sector_Cd': '20', 'GICS_Industry_Desc': 'Aerospace And Defense',                                **_DI},
    {'GICS_Industry_Cd': '251010', 'GICS_Industry_Group_Cd': '2510', 'GICS_Sector_Cd': '25', 'GICS_Industry_Desc': 'Automobiles',                                          **_DI},
    {'GICS_Industry_Cd': '301010', 'GICS_Industry_Group_Cd': '3010', 'GICS_Sector_Cd': '30', 'GICS_Industry_Desc': 'Beverages',                                            **_DI},
    {'GICS_Industry_Cd': '351010', 'GICS_Industry_Group_Cd': '3510', 'GICS_Sector_Cd': '35', 'GICS_Industry_Desc': 'Biotechnology',                                        **_DI},
    {'GICS_Industry_Cd': '401010', 'GICS_Industry_Group_Cd': '4010', 'GICS_Sector_Cd': '40', 'GICS_Industry_Desc': 'Banks',                                               **_DI},
    {'GICS_Industry_Cd': '451020', 'GICS_Industry_Group_Cd': '4510', 'GICS_Sector_Cd': '45', 'GICS_Industry_Desc': 'IT Services',                                         **_DI},
    {'GICS_Industry_Cd': '501010', 'GICS_Industry_Group_Cd': '5010', 'GICS_Sector_Cd': '50', 'GICS_Industry_Desc': 'Diversified Telecommunication Services',               **_DI},
    {'GICS_Industry_Cd': '551010', 'GICS_Industry_Group_Cd': '5510', 'GICS_Sector_Cd': '55', 'GICS_Industry_Desc': 'Electric Utilities',                                  **_DI},
    {'GICS_Industry_Cd': '601010', 'GICS_Industry_Group_Cd': '6010', 'GICS_Sector_Cd': '60', 'GICS_Industry_Desc': 'Diversified Real Estate Investment Trusts',           **_DI},
]

# ── GICS_SUBINDUSTRY_TYPE ─────────────────────────────────────────────────────
# (GICS_Industry_Cd, GICS_Industry_Group_Cd, GICS_Sector_Cd) FKs to GICS_INDUSTRY_TYPE
_cols_gics_subindustry_type = [
    'GICS_Subindustry_Cd', 'GICS_Industry_Cd', 'GICS_Industry_Group_Cd', 'GICS_Sector_Cd', 'GICS_Subindustry_Desc',
    'di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind',
]
_gics_subindustry_type_rows = [
    {'GICS_Subindustry_Cd': '10101010', 'GICS_Industry_Cd': '101010', 'GICS_Industry_Group_Cd': '1010', 'GICS_Sector_Cd': '10', 'GICS_Subindustry_Desc': 'Oil And Gas Drilling',                              **_DI},
    {'GICS_Subindustry_Cd': '15101010', 'GICS_Industry_Cd': '151010', 'GICS_Industry_Group_Cd': '1510', 'GICS_Sector_Cd': '15', 'GICS_Subindustry_Desc': 'Commodity Chemicals',                              **_DI},
    {'GICS_Subindustry_Cd': '20101010', 'GICS_Industry_Cd': '201010', 'GICS_Industry_Group_Cd': '2010', 'GICS_Sector_Cd': '20', 'GICS_Subindustry_Desc': 'Aerospace And Defense',                            **_DI},
    {'GICS_Subindustry_Cd': '25101010', 'GICS_Industry_Cd': '251010', 'GICS_Industry_Group_Cd': '2510', 'GICS_Sector_Cd': '25', 'GICS_Subindustry_Desc': 'Auto Parts And Equipment',                         **_DI},
    {'GICS_Subindustry_Cd': '30101010', 'GICS_Industry_Cd': '301010', 'GICS_Industry_Group_Cd': '3010', 'GICS_Sector_Cd': '30', 'GICS_Subindustry_Desc': 'Brewers',                                          **_DI},
    {'GICS_Subindustry_Cd': '35101010', 'GICS_Industry_Cd': '351010', 'GICS_Industry_Group_Cd': '3510', 'GICS_Sector_Cd': '35', 'GICS_Subindustry_Desc': 'Biotechnology',                                    **_DI},
    {'GICS_Subindustry_Cd': '40101010', 'GICS_Industry_Cd': '401010', 'GICS_Industry_Group_Cd': '4010', 'GICS_Sector_Cd': '40', 'GICS_Subindustry_Desc': 'Diversified Banks',                               **_DI},
    {'GICS_Subindustry_Cd': '45102010', 'GICS_Industry_Cd': '451020', 'GICS_Industry_Group_Cd': '4510', 'GICS_Sector_Cd': '45', 'GICS_Subindustry_Desc': 'IT Consulting And Other Services',                **_DI},
    {'GICS_Subindustry_Cd': '50101010', 'GICS_Industry_Cd': '501010', 'GICS_Industry_Group_Cd': '5010', 'GICS_Sector_Cd': '50', 'GICS_Subindustry_Desc': 'Integrated Telecommunication Services',            **_DI},
    {'GICS_Subindustry_Cd': '55101010', 'GICS_Industry_Cd': '551010', 'GICS_Industry_Group_Cd': '5510', 'GICS_Sector_Cd': '55', 'GICS_Subindustry_Desc': 'Electric Utilities',                              **_DI},
    {'GICS_Subindustry_Cd': '60101010', 'GICS_Industry_Cd': '601010', 'GICS_Industry_Group_Cd': '6010', 'GICS_Sector_Cd': '60', 'GICS_Subindustry_Desc': 'Diversified Real Estate Investment Trusts',       **_DI},
]


def get_industry_code_tables() -> Dict[str, pd.DataFrame]:
    return {
        'Core_DB.NAICS_INDUSTRY':           pd.DataFrame(_naics_industry_rows,           columns=_cols_naics_industry),
        'Core_DB.NACE_CLASS':               pd.DataFrame(_nace_class_rows,               columns=_cols_nace_class),
        'Core_DB.SIC':                      pd.DataFrame(_sic_rows,                      columns=_cols_sic),
        'Core_DB.GICS_SECTOR_TYPE':         pd.DataFrame(_gics_sector_type_rows,         columns=_cols_gics_sector_type),
        'Core_DB.GICS_INDUSTRY_GROUP_TYPE': pd.DataFrame(_gics_industry_group_type_rows, columns=_cols_gics_industry_group_type),
        'Core_DB.GICS_INDUSTRY_TYPE':       pd.DataFrame(_gics_industry_type_rows,       columns=_cols_gics_industry_type),
        'Core_DB.GICS_SUBINDUSTRY_TYPE':    pd.DataFrame(_gics_subindustry_type_rows,    columns=_cols_gics_subindustry_type),
    }

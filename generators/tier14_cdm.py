"""Tier 14 — CDM_DB generator.

Produces all 16 CDM_DB MULTISET tables by projecting CustomerProfile /
AgreementProfile registries and denormalising the Core_DB address chain.
15 tables receive both DI and Valid stamps; PARTY_INTERRACTION_EVENT is DI-only.
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import pandas as pd
from faker import Faker

import config.code_values as cv
import config.settings as settings
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ── module-level constants ────────────────────────────────────────────────────

_CDM_DI_START_TS   = '2000-01-01 00:00:00.000000'
_CDM_VALID_FROM_DT = str(settings.HISTORY_START)   # '2025-10-01'

_LIFECYCLE_PHASE_MAP: Dict[str, int] = {
    'ACTIVE':    3,
    'DECLINING': 3,
    'CHURNED':   3,
    'NEW':       2,
}

# str label → SMALLINT code; inverse of HOUSEHOLD_ROLE_TO_CD {1:'HEAD', ...}
_HOUSEHOLD_ROLE_INV: Dict[str, int] = {v: k for k, v in cv.HOUSEHOLD_ROLE_TO_CD.items()}

# ISO 3-digit numeric codes → ADDRESS_COUNTRY_CD SMALLINT (geography_ref.py order)
_ISO_NUM_TO_ADDR_CD: Dict[str, int] = {
    '840':  1, '124':  2, '826':  3, '276':  4, '250':  5,
    '392':  6, '036':  7, '484':  8, '076':  9, '156': 10,
    '356': 11, '724': 12, '380': 13, '528': 14, '756': 15,
    '752': 16, '372': 17, '702': 18, '710': 19, '578': 20,
}

# ── column lists (business columns only — DI/Valid appended by stamp_*) ───────

_COLS_PARTY = [
    'Source_Cd', 'CDM_Party_Id', 'Source_Party_Id', 'Party_Type_Cd',
    'Party_Lifecycle_Phase_Cd', 'Party_Since', 'Survival_Record_Ind', 'DQ_Score',
]

_COLS_INDIVIDUAL = [
    'CDM_Party_Id', 'First_Name', 'Middle_Name', 'Last_Name',
    'Birth_Dt', 'Gender', 'Salutation', 'DQ_Score',
]

_COLS_ORGANIZATION = [
    'CDM_Party_Id', 'Organization_Name', 'Business_Identifier',
]

_COLS_HOUSEHOLD = [
    'CDM_Household_Id', 'Household_Name', 'Household_Desc',
]

_COLS_INDIVIDUAL_TO_HOUSEHOLD = [
    'CDM_Party_Id', 'CDM_Household_Id', 'Role_Type_Cd', 'Probability',
]

_COLS_RELATIONSHIP = [
    'CDM_Party_Id', 'Parent_CDM_Party_Id', 'Relationship_Type_Cd',
    'Relationship_Value_Cd', 'Probability',
]

_COLS_PARTY_TO_AGREEMENT_ROLE = [
    'CDM_Party_Id', 'Agreement_Id', 'Role_Type_Cd',
]

_COLS_PARTY_TO_EVENT_ROLE = [
    'CDM_Party_Id', 'Event_Id', 'Role_Type_Cd',
]

_COLS_PARTY_SEGMENT = [
    'CDM_Party_Id', 'Segment_Type_Cd', 'Segment_Value_Cd',
]

_COLS_ADDRESS = [
    'CDM_Address_Id', 'Address_Id', 'Address_Type', 'Address_Country_Cd',
    'Address_County', 'Address_City', 'Address_Street', 'Address_Postal_Code',
    'Primary_Address_Flag', 'Geo_Latitude', 'Geo_Longitude',
]

_COLS_ADDRESS_TO_AGREEMENT = [
    'Address_Id', 'Agreement_Id',
]

_COLS_PARTY_CONTACT = [
    'Contact_Id', 'Contact_Type_Cd', 'Contact_Value', 'Primary_Contact_Ind',
]

_COLS_CONTACT_TO_AGREEMENT = [
    'Contact_Id', 'Agreement_Id',
]

_COLS_PIE = [
    'Event_Id', 'CDM_Party_Id', 'Event_Type_Cd', 'Event_Channel_Type_Cd',
    'Event_Dt', 'Event_Sentiment_Cd',
]

# ── helper functions ──────────────────────────────────────────────────────────


def _build_name_map(ctx: 'GenerationContext') -> Dict[int, Dict[str, Optional[str]]]:
    name_df = ctx.tables.get('Core_DB.INDIVIDUAL_NAME')
    if name_df is None or len(name_df) == 0:
        return {}
    active = name_df[
        (name_df['Name_Type_Cd'] == 'legal') &
        (name_df['Individual_Name_End_Dt'].astype(str) == settings.HIGH_DATE)
    ]
    result: Dict[int, Dict[str, Optional[str]]] = {}
    for _, row in active.iterrows():
        pid = int(row['Individual_Party_Id'])
        result[pid] = {
            'Given_Name':  row['Given_Name'],
            'Middle_Name': row['Middle_Name'],
            'Family_Name': row['Family_Name'],
        }
    return result


def _build_birth_map(ctx: 'GenerationContext') -> Dict[int, Optional[str]]:
    indiv_df = ctx.tables.get('Core_DB.INDIVIDUAL')
    if indiv_df is None or len(indiv_df) == 0:
        return {}
    result: Dict[int, Optional[str]] = {}
    for _, row in indiv_df.iterrows():
        pid = int(row['Individual_Party_Id'])
        val = row['Birth_Dt']
        result[pid] = str(val) if pd.notna(val) else None
    return result


def _gen_party(customers: list) -> pd.DataFrame:
    rows = [
        {
            'Source_Cd':                 1,
            'CDM_Party_Id':              cp.party_id,
            'Source_Party_Id':           cp.party_id,
            'Party_Type_Cd':             1 if cp.party_type == 'INDIVIDUAL' else 2,
            'Party_Lifecycle_Phase_Cd':  _LIFECYCLE_PHASE_MAP[cp.lifecycle_cohort],
            'Party_Since':               str(cp.party_since),
            'Survival_Record_Ind':       'Y',
            'DQ_Score':                  Decimal('100.00'),
        }
        for cp in customers
    ]
    # Reserved bank/self-emp placeholder — mirrors the Core_DB.PARTY reserved row so
    # CDM_DB.PARTY.CDM_Party_Id universe == Core_DB.PARTY.Party_Id universe.
    customer_ids = {cp.party_id for cp in customers}
    if settings.BANK_PARTY_ID not in customer_ids:
        rows.append({
            'Source_Cd':                 1,
            'CDM_Party_Id':              settings.BANK_PARTY_ID,
            'Source_Party_Id':           settings.BANK_PARTY_ID,
            'Party_Type_Cd':             2,
            'Party_Lifecycle_Phase_Cd':  1,
            'Party_Since':               str(settings.HISTORY_START),
            'Survival_Record_Ind':       'Y',
            'DQ_Score':                  Decimal('100.00'),
        })
    df = pd.DataFrame(rows, columns=_COLS_PARTY)
    df['CDM_Party_Id']   = df['CDM_Party_Id'].astype('Int64')
    df['Source_Party_Id'] = df['Source_Party_Id'].astype('Int64')
    for col in ('Source_Cd', 'Party_Type_Cd', 'Party_Lifecycle_Phase_Cd'):
        df[col] = df[col].astype('Int64')
    return df


def _gen_individual(
    customers: list,
    name_map: Dict[int, Dict[str, Optional[str]]],
    birth_map: Dict[int, Optional[str]],
) -> pd.DataFrame:
    rows = []
    for cp in customers:
        if cp.party_type != 'INDIVIDUAL':
            continue
        names = name_map.get(cp.party_id, {})
        rows.append({
            'CDM_Party_Id': cp.party_id,
            'First_Name':   names.get('Given_Name'),
            'Middle_Name':  names.get('Middle_Name'),
            'Last_Name':    names.get('Family_Name'),
            'Birth_Dt':     birth_map.get(cp.party_id),
            'Gender':       'Male' if cp.gender_type_cd == 'MALE' else 'Female',
            'Salutation':   'Mr.' if cp.gender_type_cd == 'MALE' else 'Ms.',
            'DQ_Score':     Decimal('100.00'),
        })
    df = pd.DataFrame(rows, columns=_COLS_INDIVIDUAL)
    df['CDM_Party_Id'] = df['CDM_Party_Id'].astype('Int64')
    return df


def _gen_organization(customers: list) -> pd.DataFrame:
    rows = []
    seen: set = set()
    for cp in customers:
        if cp.party_type != 'ORGANIZATION' or cp.party_id in seen:
            continue
        seen.add(cp.party_id)
        rows.append({
            'CDM_Party_Id':        cp.party_id,
            'Organization_Name':   cp.org_name,
            'Business_Identifier': f'{cp.party_id % 1_000_000_000:09d}',
        })
    if settings.SELF_EMP_ORG_ID not in seen:
        rows.append({
            'CDM_Party_Id':        settings.SELF_EMP_ORG_ID,
            'Organization_Name':   'Self-Employment Organization',
            'Business_Identifier': f'{settings.SELF_EMP_ORG_ID % 1_000_000_000:09d}',
        })
    df = pd.DataFrame(rows, columns=_COLS_ORGANIZATION)
    df['CDM_Party_Id'] = df['CDM_Party_Id'].astype('Int64')
    return df


def _gen_household(customers: list) -> pd.DataFrame:
    hh_ids = sorted({cp.household_id for cp in customers if cp.household_id is not None})
    rows = [
        {
            'CDM_Household_Id': hid,
            'Household_Name':   f'Household {hid}',
            'Household_Desc':   None,
        }
        for hid in hh_ids
    ]
    df = pd.DataFrame(rows, columns=_COLS_HOUSEHOLD)
    df['CDM_Household_Id'] = df['CDM_Household_Id'].astype('Int64')
    return df


def _gen_i2h(customers: list) -> pd.DataFrame:
    rows = [
        {
            'CDM_Party_Id':     cp.party_id,
            'CDM_Household_Id': cp.household_id,
            'Role_Type_Cd':     _HOUSEHOLD_ROLE_INV[cp.household_role],
            'Probability':      Decimal('1.0000'),
        }
        for cp in customers
        if cp.party_type == 'INDIVIDUAL' and cp.household_id is not None
    ]
    df = pd.DataFrame(rows, columns=_COLS_INDIVIDUAL_TO_HOUSEHOLD)
    df['CDM_Party_Id']     = df['CDM_Party_Id'].astype('Int64')
    df['CDM_Household_Id'] = df['CDM_Household_Id'].astype('Int64')
    df['Role_Type_Cd']     = df['Role_Type_Cd'].astype('Int64')
    return df


def _gen_i2i(customers: list) -> pd.DataFrame:
    hh_head: Dict[int, int] = {}
    for cp in customers:
        if cp.party_type == 'INDIVIDUAL' and cp.household_id is not None and cp.household_role == 'HEAD':
            hh_head[cp.household_id] = cp.party_id

    rows = []
    for cp in customers:
        if cp.party_type != 'INDIVIDUAL' or cp.household_id is None or cp.household_role == 'HEAD':
            continue
        head_id = hh_head.get(cp.household_id)
        if head_id is None:
            continue
        rel_val = 1 if cp.household_role == 'SPOUSE' else 2
        rows.append({
            'CDM_Party_Id':          cp.party_id,
            'Parent_CDM_Party_Id':   head_id,
            'Relationship_Type_Cd':  1,
            'Relationship_Value_Cd': rel_val,
            'Probability':           Decimal('1.0000'),
        })
    df = pd.DataFrame(rows, columns=_COLS_RELATIONSHIP)
    df['CDM_Party_Id']        = df['CDM_Party_Id'].astype('Int64')
    df['Parent_CDM_Party_Id'] = df['Parent_CDM_Party_Id'].astype('Int64')
    for col in ('Relationship_Type_Cd', 'Relationship_Value_Cd'):
        df[col] = df[col].astype('Int64')
    return df


def _gen_i2o(customers: list, org_ids: List[int], rng) -> pd.DataFrame:
    rows = []
    for cp in customers:
        if cp.party_type != 'INDIVIDUAL' or cp.occupation_cd != 'EMP':
            continue
        if not org_ids:
            continue
        rows.append({
            'CDM_Party_Id':          cp.party_id,
            'Parent_CDM_Party_Id':   int(rng.choice(org_ids)),
            'Relationship_Type_Cd':  2,
            'Relationship_Value_Cd': 1,
            'Probability':           Decimal('1.0000'),
        })
    df = pd.DataFrame(rows, columns=_COLS_RELATIONSHIP)
    df['CDM_Party_Id']        = df['CDM_Party_Id'].astype('Int64')
    df['Parent_CDM_Party_Id'] = df['Parent_CDM_Party_Id'].astype('Int64')
    for col in ('Relationship_Type_Cd', 'Relationship_Value_Cd'):
        df[col] = df[col].astype('Int64')
    return df


def _gen_o2o(org_ids: List[int], rng) -> pd.DataFrame:
    if len(org_ids) < 20:
        return pd.DataFrame(columns=_COLS_RELATIONSHIP)
    pairs: set = set()
    attempts = 0
    while len(pairs) < 10 and attempts < 1000:
        child  = int(rng.choice(org_ids))
        parent = int(rng.choice(org_ids))
        if child != parent:
            pairs.add((child, parent))
        attempts += 1
    rows = [
        {
            'CDM_Party_Id':          child,
            'Parent_CDM_Party_Id':   parent,
            'Relationship_Type_Cd':  3,
            'Relationship_Value_Cd': 1,
            'Probability':           Decimal('1.0000'),
        }
        for child, parent in pairs
    ]
    df = pd.DataFrame(rows, columns=_COLS_RELATIONSHIP)
    df['CDM_Party_Id']        = df['CDM_Party_Id'].astype('Int64')
    df['Parent_CDM_Party_Id'] = df['Parent_CDM_Party_Id'].astype('Int64')
    for col in ('Relationship_Type_Cd', 'Relationship_Value_Cd'):
        df[col] = df[col].astype('Int64')
    return df


def _gen_segment(customers: list) -> pd.DataFrame:
    rows = [
        {
            'CDM_Party_Id':    cp.party_id,
            'Segment_Type_Cd': 1,
            'Segment_Value_Cd': cp.clv_segment,
        }
        for cp in customers
    ]
    df = pd.DataFrame(rows, columns=_COLS_PARTY_SEGMENT)
    df['CDM_Party_Id'] = df['CDM_Party_Id'].astype('Int64')
    for col in ('Segment_Type_Cd', 'Segment_Value_Cd'):
        df[col] = df[col].astype('Int64')
    return df


def _gen_address(ctx: 'GenerationContext') -> Tuple[pd.DataFrame, Dict[int, int]]:
    street_df = ctx.tables.get('Core_DB.STREET_ADDRESS', pd.DataFrame())
    postal_df  = ctx.tables.get('Core_DB.POSTAL_CODE',   pd.DataFrame())
    iso_df     = ctx.tables.get('Core_DB.ISO_3166_COUNTRY_STANDARD', pd.DataFrame())

    # street_address_id → {country_id, postal_code_id} from Core_DB STREET_ADDRESS
    street_map: Dict[int, Dict[str, Optional[int]]] = {}
    for _, row in street_df.iterrows():
        sid = int(row['Street_Address_Id'])
        cid = row['Country_Id']
        pid = row['Postal_Code_Id']
        street_map[sid] = {
            'country_id':     int(cid) if pd.notna(cid) else None,
            'postal_code_id': int(pid) if pd.notna(pid) else None,
        }

    # postal_code_id → Postal_Code_Num string
    postal_num_map: Dict[int, Optional[str]] = {}
    for _, row in postal_df.iterrows():
        val = row['Postal_Code_Num']
        postal_num_map[int(row['Postal_Code_Id'])] = str(val) if pd.notna(val) else None

    # country_id → ADDRESS_COUNTRY_CD SMALLINT via ISO numeric code
    country_addr_cd_map: Dict[int, int] = {}
    for _, row in iso_df.iterrows():
        iso_num = str(row['ISO_3166_Country_3_Num']).strip()
        country_addr_cd_map[int(row['Country_Id'])] = _ISO_NUM_TO_ADDR_CD.get(iso_num, 1)

    rows = []
    cdm_addr_map: Dict[int, int] = {}
    for ar in ctx.addresses:
        cdm_id = ctx.ids.next('cdm_address')
        cdm_addr_map[ar.address_id] = cdm_id

        sm          = street_map.get(ar.address_id, {})
        country_id  = sm.get('country_id')
        postal_id   = sm.get('postal_code_id')
        addr_cd     = country_addr_cd_map.get(country_id, 1) if country_id is not None else 1
        postal_num  = postal_num_map.get(postal_id) if postal_id is not None else None

        rows.append({
            'CDM_Address_Id':       cdm_id,
            'Address_Id':           ar.address_id,
            'Address_Type':         ar.address_subtype_cd,
            'Address_Country_Cd':   addr_cd,
            'Address_County':       None,
            'Address_City':         None,
            'Address_Street':       ar.street_line_1,
            'Address_Postal_Code':  postal_num,
            'Primary_Address_Flag': 'Y',
            'Geo_Latitude':         round(ar.latitude, 6),
            'Geo_Longitude':        round(ar.longitude, 6),
        })

    df = pd.DataFrame(rows, columns=_COLS_ADDRESS)
    df['CDM_Address_Id']    = df['CDM_Address_Id'].astype('Int64')
    df['Address_Id']        = df['Address_Id'].astype('Int64')
    df['Address_Country_Cd'] = df['Address_Country_Cd'].astype('Int64')
    return df, cdm_addr_map


def _gen_addr_to_agreement(agreements: list, cust_addr: Dict[int, int]) -> pd.DataFrame:
    rows = [
        {
            'Address_Id':   cust_addr[ap.owner_party_id],
            'Agreement_Id': ap.agreement_id,
        }
        for ap in agreements
        if ap.owner_party_id in cust_addr
    ]
    df = pd.DataFrame(rows, columns=_COLS_ADDRESS_TO_AGREEMENT)
    df['Address_Id']   = df['Address_Id'].astype('Int64')
    df['Agreement_Id'] = df['Agreement_Id'].astype('Int64')
    return df


def _gen_party_contact(
    customers: list,
    ids,
) -> Tuple[pd.DataFrame, Dict[int, int]]:
    rows: list = []
    email_contact_map: Dict[int, int] = {}
    for cp in customers:
        fk = Faker()
        fk.seed_instance(int(cp.party_id))
        email_cid = ids.next('contact')
        phone_cid = ids.next('contact')
        email_contact_map[cp.party_id] = email_cid
        rows.append({
            'Contact_Id':          email_cid,
            'Contact_Type_Cd':     1,
            'Contact_Value':       fk.email(),
            'Primary_Contact_Ind': 'Y',
        })
        rows.append({
            'Contact_Id':          phone_cid,
            'Contact_Type_Cd':     2,
            'Contact_Value':       fk.phone_number(),
            'Primary_Contact_Ind': 'N',
        })
    df = pd.DataFrame(rows, columns=_COLS_PARTY_CONTACT)
    df['Contact_Id']      = df['Contact_Id'].astype('Int64')
    df['Contact_Type_Cd'] = df['Contact_Type_Cd'].astype('Int64')
    return df, email_contact_map


def _gen_contact_to_agreement(
    agreements: list,
    email_contact_map: Dict[int, int],
) -> pd.DataFrame:
    rows = [
        {
            'Contact_Id':   email_contact_map[ap.owner_party_id],
            'Agreement_Id': ap.agreement_id,
        }
        for ap in agreements
        if ap.owner_party_id in email_contact_map
    ]
    df = pd.DataFrame(rows, columns=_COLS_CONTACT_TO_AGREEMENT)
    df['Contact_Id']   = df['Contact_Id'].astype('Int64')
    df['Agreement_Id'] = df['Agreement_Id'].astype('Int64')
    return df


def _gen_party_to_agreement_role(agreements: list) -> pd.DataFrame:
    rows = [
        {
            'CDM_Party_Id': ap.owner_party_id,
            'Agreement_Id': ap.agreement_id,
            'Role_Type_Cd': 1,
        }
        for ap in agreements
    ]
    df = pd.DataFrame(rows, columns=_COLS_PARTY_TO_AGREEMENT_ROLE)
    df['CDM_Party_Id'] = df['CDM_Party_Id'].astype('Int64')
    df['Agreement_Id'] = df['Agreement_Id'].astype('Int64')
    df['Role_Type_Cd'] = df['Role_Type_Cd'].astype('Int64')
    return df


def _gen_party_to_event_role(ctx: 'GenerationContext') -> pd.DataFrame:
    ep_df = ctx.tables.get('Core_DB.EVENT_PARTY')
    if ep_df is None or len(ep_df) == 0:
        return pd.DataFrame(columns=_COLS_PARTY_TO_EVENT_ROLE)
    rows = []
    for _, row in ep_df.sort_values('Event_Id').iterrows():
        role_str = row['Event_Party_Role_Cd']
        if role_str not in cv.EVENT_PARTY_ROLE_TO_CD:
            raise ValueError(f'Unknown Event_Party_Role_Cd: {role_str!r}')
        rows.append({
            'CDM_Party_Id': int(row['Party_Id']),
            'Event_Id':     int(row['Event_Id']),
            'Role_Type_Cd': cv.EVENT_PARTY_ROLE_TO_CD[role_str],
        })
    df = pd.DataFrame(rows, columns=_COLS_PARTY_TO_EVENT_ROLE)
    df['CDM_Party_Id'] = df['CDM_Party_Id'].astype('Int64')
    df['Event_Id']     = df['Event_Id'].astype('Int64')
    df['Role_Type_Cd'] = df['Role_Type_Cd'].astype('Int64')
    return df


def _gen_party_interraction_event(ctx: 'GenerationContext') -> pd.DataFrame:
    ce_df = ctx.tables.get('Core_DB.COMPLAINT_EVENT')
    ep_df = ctx.tables.get('Core_DB.EVENT_PARTY')

    if ce_df is None or len(ce_df) == 0:
        return pd.DataFrame(columns=_COLS_PIE)

    initiator_map: Dict[int, int] = {}
    if ep_df is not None and len(ep_df) > 0:
        for _, row in ep_df[ep_df['Event_Party_Role_Cd'] == 'initiator'].iterrows():
            initiator_map[int(row['Event_Id'])] = int(row['Party_Id'])

    rows = []
    for _, row in ce_df.sort_values('Event_Id').iterrows():
        eid = int(row['Event_Id'])
        rows.append({
            'Event_Id':              eid,
            'CDM_Party_Id':          initiator_map.get(eid),
            'Event_Type_Cd':         1,
            'Event_Channel_Type_Cd': int(row['Event_Channel_Type_Cd']),
            'Event_Dt':              str(row['Event_Received_Dttm'])[:10],
            'Event_Sentiment_Cd':    int(row['Event_Sentiment_Cd']),
        })
    df = pd.DataFrame(rows, columns=_COLS_PIE)
    df['Event_Id']     = df['Event_Id'].astype('Int64')
    df['CDM_Party_Id'] = df['CDM_Party_Id'].astype('Int64')
    for col in ('Event_Type_Cd', 'Event_Channel_Type_Cd', 'Event_Sentiment_Cd'):
        df[col] = df[col].astype('Int64')
    return df


# ── generator class ───────────────────────────────────────────────────────────


class Tier14CDM(BaseGenerator):
    """Generate all 16 CDM_DB tables from CustomerProfile / AgreementProfile registries."""

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        customers  = sorted(ctx.customers,  key=lambda cp: cp.party_id)
        agreements = sorted(ctx.agreements, key=lambda ap: ap.agreement_id)

        name_map  = _build_name_map(ctx)
        birth_map = _build_birth_map(ctx)

        org_ids: List[int] = sorted(
            cp.party_id for cp in customers
            if cp.party_type == 'ORGANIZATION'
            and cp.party_id != settings.SELF_EMP_ORG_ID
        )
        cust_addr: Dict[int, int] = {cp.party_id: cp.address_id for cp in customers}

        df_party                     = _gen_party(customers)
        df_indiv                     = _gen_individual(customers, name_map, birth_map)
        df_org                       = _gen_organization(customers)
        df_hh                        = _gen_household(customers)
        df_i2h                       = _gen_i2h(customers)
        df_i2i                       = _gen_i2i(customers)
        df_i2o                       = _gen_i2o(customers, org_ids, ctx.rng)
        df_o2o                       = _gen_o2o(org_ids, ctx.rng)
        df_seg                       = _gen_segment(customers)
        df_addr, _                   = _gen_address(ctx)
        df_a2a                       = _gen_addr_to_agreement(agreements, cust_addr)
        df_contact, email_cmap       = _gen_party_contact(customers, ctx.ids)
        df_c2a                       = _gen_contact_to_agreement(agreements, email_cmap)
        df_ptar                      = _gen_party_to_agreement_role(agreements)
        df_ptev                      = _gen_party_to_event_role(ctx)
        df_pie                       = _gen_party_interraction_event(ctx)

        _PIE_KEY = f'CDM_DB.{settings.PARTY_INTERRACTION_EVENT_TABLE_NAME}'
        tables: Dict[str, pd.DataFrame] = {
            'CDM_DB.PARTY':                        df_party,
            'CDM_DB.INDIVIDUAL':                   df_indiv,
            'CDM_DB.ORGANIZATION':                 df_org,
            'CDM_DB.HOUSEHOLD':                    df_hh,
            'CDM_DB.INDIVIDUAL_TO_HOUSEHOLD':      df_i2h,
            'CDM_DB.INDIVIDUAL_TO_INDIVIDUAL':     df_i2i,
            'CDM_DB.INDIVIDUAL_TO_ORGANIZATION':   df_i2o,
            'CDM_DB.ORGANIZATION_TO_ORGANIZATION': df_o2o,
            'CDM_DB.PARTY_SEGMENT':                df_seg,
            'CDM_DB.ADDRESS':                      df_addr,
            'CDM_DB.ADDRESS_TO_AGREEMENT':         df_a2a,
            'CDM_DB.PARTY_CONTACT':                df_contact,
            'CDM_DB.CONTACT_TO_AGREEMENT':         df_c2a,
            'CDM_DB.PARTY_TO_AGREEMENT_ROLE':      df_ptar,
            'CDM_DB.PARTY_TO_EVENT_ROLE':          df_ptev,
            _PIE_KEY:                              df_pie,
        }

        result: Dict[str, pd.DataFrame] = {}
        for key, df in tables.items():
            df = self.stamp_di(df, start_ts=_CDM_DI_START_TS)
            if key != _PIE_KEY:
                df = self.stamp_valid(df, from_dt=_CDM_VALID_FROM_DT)
            result[key] = df
        return result

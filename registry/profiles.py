from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional


@dataclass
class CustomerProfile:
    # Identity
    party_id: int                        # BIGINT — shared with CDM_Party_Id
    party_type: str                      # 'INDIVIDUAL' | 'ORGANIZATION'

    # Demographics
    age: int
    income_quartile: int                 # 1–4
    lifecycle_cohort: str                # 'ACTIVE' | 'DECLINING' | 'CHURNED' | 'NEW'
    clv_segment: int                     # 1–10 decile

    # Individual attributes (None for ORGANIZATION)
    gender_type_cd: Optional[str]
    marital_status_cd: Optional[str]
    ethnicity_type_cd: Optional[str]
    occupation_cd: Optional[str]         # 'EMP'|'SELF_EMP'|'RETIRED'|'NOT_WORKING'; None for ORG
    num_dependents: int                  # 0 for orgs
    fico_score: int                      # 0 for orgs

    # Household
    household_id: Optional[int]          # None for singletons/orgs
    household_role: str                  # 'HEAD' | 'SPOUSE' | 'DEPENDENT'
    lifecl: int                          # 1–6 (SCF LIFECL stage)

    # Channel / contact
    has_internet: bool
    preferred_channel_cd: int            # SMALLINT: 1=BRANCH, 3=ONLINE, 4=MOBILE

    # Dates — required, no default (Step 4 must populate)
    party_since: date

    # Address reference — required, no default (Step 4 must populate)
    address_id: int                      # BIGINT FK to AddressRecord.address_id

    # Products decided — mutable, defaulted (Step 4 populates via _assign_products)
    product_set: List[str] = field(default_factory=list)

    # Org-specific (None for INDIVIDUAL)
    org_name: Optional[str] = None
    naics_sector_cd: Optional[str] = None
    sic_cd: Optional[str] = None
    gics_sector_cd: Optional[str] = None


@dataclass
class AgreementProfile:
    # Identity
    agreement_id: int                    # BIGINT
    owner_party_id: int                  # BIGINT FK to CustomerProfile.party_id
    product_type: str
    agreement_subtype_cd: str            # matches AGREEMENT_SUBTYPE seed table code
    product_id: int                      # BIGINT FK to Core_DB.PRODUCT

    # Temporal
    open_dttm: datetime
    close_dttm: Optional[datetime]       # None = open; set for CHURNED cohort only

    # Financial
    balance_amt: Decimal
    interest_rate: Decimal
    original_loan_amt: Optional[Decimal] # loan/mortgage only

    # Status flags
    is_delinquent: bool
    is_severely_delinquent: bool
    is_frozen: bool

    # Balance trajectory (DECLINING cohort — 6 monthly snapshots)
    monthly_balances: List[Decimal] = field(default_factory=list)

    # Agreement sub-type path flags (exclusive at terminal leaf)
    # Parent-chain flags may be True simultaneously with their descendants
    is_financial: bool = False
    is_deposit: bool = False
    is_term_deposit: bool = False        # terminal leaf
    is_credit: bool = False
    is_loan_term: bool = False
    is_mortgage: bool = False            # terminal leaf
    is_credit_card: bool = False         # terminal leaf
    is_loan_transaction: bool = False    # terminal leaf


@dataclass
class AddressRecord:
    # Identity
    address_id: int                      # BIGINT FK from CustomerProfile and PARTY_LOCATOR
    address_subtype_cd: str              # 'PHYSICAL' primary type

    # Street fields
    street_line_1: str
    street_line_2: Optional[str]
    house_num: str                       # Street_Address_Num NOT NULL per DDL
    street_name: str
    street_direction_type_cd: str        # → DIRECTION_TYPE
    street_suffix_cd: str                # → STREET_SUFFIX_TYPE

    # Geography FKs (all BIGINT)
    city_id: int                         # FK to Tier 1 CITY
    county_id: Optional[int]             # nullable — PO-box/parcel addresses may lack one
    territory_id: int                    # FK to Tier 1 TERRITORY
    postal_code_id: int                  # FK to Tier 1 POSTAL_CODE
    country_id: int                      # FK to Tier 1 COUNTRY

    # Coordinates (DECIMAL(18,4) in DDL)
    latitude: float
    longitude: float


if __name__ == '__main__':
    from datetime import date as _date
    from decimal import Decimal as _Dec

    cp = CustomerProfile(
        party_id=10_000_000, party_type='INDIVIDUAL',
        age=42, income_quartile=3, lifecycle_cohort='ACTIVE', clv_segment=7,
        gender_type_cd='MALE', marital_status_cd='MARRIED',
        ethnicity_type_cd='WHITE', occupation_cd='EMP',
        num_dependents=2, fico_score=720,
        household_id=8_000_000, household_role='HEAD', lifecl=3,
        has_internet=True, preferred_channel_cd=3,
        party_since=_date(2018, 6, 15),
        address_id=1_000_000,
        product_set=['CHECKING', 'SAVINGS'],
        org_name=None, naics_sector_cd=None, sic_cd=None, gics_sector_cd=None,
    )
    assert cp.party_id == 10_000_000 and isinstance(cp.party_id, int)
    assert cp.product_set == ['CHECKING', 'SAVINGS']

    ap = AgreementProfile(
        agreement_id=100_000, owner_party_id=10_000_000,
        product_type='MORTGAGE', agreement_subtype_cd='MORTGAGE',
        product_id=1_000,
        open_dttm=datetime(2020, 4, 1, 9, 30),
        close_dttm=None,
        balance_amt=_Dec('250000.0000'),
        interest_rate=_Dec('0.035000000000'),
        original_loan_amt=_Dec('300000.0000'),
        is_delinquent=False, is_severely_delinquent=False, is_frozen=False,
        monthly_balances=[],
        is_financial=True, is_deposit=False, is_term_deposit=False,
        is_credit=True, is_loan_term=True, is_mortgage=True,
        is_credit_card=False, is_loan_transaction=False,
    )
    terminal_leaves = [ap.is_term_deposit, ap.is_mortgage, ap.is_credit_card, ap.is_loan_transaction]
    assert sum(terminal_leaves) == 1, 'Exactly one terminal sub-type must be True'

    ar = AddressRecord(
        address_id=1_000_000, address_subtype_cd='PHYSICAL',
        street_line_1='123 Main St', street_line_2=None,
        house_num='123', street_name='Main',
        street_direction_type_cd='N', street_suffix_cd='ST',
        city_id=1, county_id=None, territory_id=1,
        postal_code_id=1, country_id=1,
        latitude=37.7749, longitude=-122.4194,
    )
    for f in ('address_id', 'city_id', 'territory_id', 'postal_code_id', 'country_id'):
        assert isinstance(getattr(ar, f), int), f'{f} not int'

    print('registry/profiles.py OK')

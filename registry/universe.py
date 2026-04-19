"""
UniverseBuilder — Phase 1 of the generator.

build() makes every correlated customer-level and agreement-level decision
upfront. Downstream tier generators (Steps 8-23) are pure transformations
with no statistical sampling.
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List

import numpy as np
from faker import Faker

from config.distributions import (
    sample_age, sample_cc_balance, sample_deposit_balance,
    sample_ethnicity, sample_gender, sample_income_quartile, sample_kids,
    sample_lifecl, sample_marital, sample_mortgage_rate, sample_occupation,
    sample_fico,
)
from registry.context import GenerationContext
from registry.profiles import AddressRecord, AgreementProfile, CustomerProfile
from utils.date_utils import month_snapshots, random_date_between, random_datetime_between
from utils.id_factory import IdFactory


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

_DEPOSIT_TYPES = frozenset({
    'CHECKING', 'SAVINGS', 'MMA', 'RETIREMENT',
    'CERTIFICATE_OF_DEPOSIT', 'COMMERCIAL_CHECKING',
})

# Authoritative product-type → is_* flag mapping (spec §"Product-type → AgreementProfile.is_* flag mapping")
# Columns: is_financial, is_deposit, is_term_deposit, is_credit, is_loan_term, is_mortgage, is_credit_card, is_loan_transaction
_PRODUCT_FLAGS: Dict[str, tuple] = {
    'CHECKING':              (True,  True,  False, False, False, False, False, False),
    'SAVINGS':               (True,  True,  False, False, False, False, False, False),
    'MMA':                   (True,  True,  False, False, False, False, False, False),
    'RETIREMENT':            (True,  True,  False, False, False, False, False, False),
    'CERTIFICATE_OF_DEPOSIT':(True,  True,  True,  False, False, False, False, False),
    'CREDIT_CARD':           (True,  False, False, True,  False, False, True,  False),
    'HELOC':                 (True,  False, False, True,  False, False, False, False),
    'VEHICLE_LOAN':          (True,  False, False, True,  True,  False, False, False),
    'STUDENT_LOAN':          (True,  False, False, True,  True,  False, False, False),
    'MORTGAGE':              (True,  False, False, True,  True,  True,  False, False),
    'PAYDAY':                (True,  False, False, False, False, False, False, True),
    'COMMERCIAL_CHECKING':   (True,  True,  False, False, False, False, False, False),
}

# CLV segment weight arrays per cohort (10 values, indices map to segments 1–10)
_CLV_W: Dict[str, np.ndarray] = {
    'CHURNED':  np.array([0.20, 0.20, 0.20, 0.15, 0.10, 0.07, 0.04, 0.02, 0.01, 0.01]),
    'DECLINING': np.array([0.05, 0.08, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05, 0.01, 0.01]),
    'ACTIVE':   np.array([0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10]),
    'NEW':      np.array([0.02, 0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.08, 0.04, 0.01]),
}

# NAICS/SIC/GICS fixed sets for organizations
_NAICS_SECTORS = ['52', '62', '44', '51', '72', '81']
_SIC_CODES     = ['6020', '6210', '5411', '5912', '7011', '8011']
_GICS_SECTORS  = ['10', '20', '25', '35', '40', '45', '50', '55']

# Cohort open-date windows as (start_date, end_date)
_COHORT_OPEN_WINDOWS = {
    'ACTIVE':   (date(2015, 1, 1),  date(2025, 9, 30)),
    'DECLINING':(date(2015, 1, 1),  date(2025, 6, 30)),
    'CHURNED':  (date(2015, 1, 1),  date(2025, 6, 30)),
    'NEW':      (date(2026, 1, 15), date(2026, 3, 31)),
}
_CHURNED_CLOSE_WINDOW = (date(2025, 10, 1), date(2026, 3, 15))

# CC carrying rates by income quartile (Part C3)
_CC_CARRY_RATE = {1: 0.35, 2: 0.50, 3: 0.57, 4: 0.24}

# Fixed interest rates for deposit and simple credit products
_FIXED_RATES: Dict[str, Decimal] = {
    'CHECKING':               Decimal('0.000500000000'),
    'SAVINGS':                Decimal('0.004000000000'),
    'MMA':                    Decimal('0.002500000000'),
    'CERTIFICATE_OF_DEPOSIT': Decimal('0.050000000000'),
    'RETIREMENT':             Decimal('0.070000000000'),
    'COMMERCIAL_CHECKING':    Decimal('0.000300000000'),
    'CREDIT_CARD':            Decimal('0.189900000000'),
    'HELOC':                  Decimal('0.085000000000'),
    'VEHICLE_LOAN':           Decimal('0.062500000000'),
    'STUDENT_LOAN':           Decimal('0.055000000000'),
    'PAYDAY':                 Decimal('0.400000000000'),
}


class UniverseBuilder:

    def build(self, config, rng: np.random.Generator) -> GenerationContext:
        ids = IdFactory(config.ID_RANGES)
        customers = self._generate_customer_shells(config, rng, ids)
        self._assign_demographics(customers, rng)
        self._assign_households(customers, rng, ids)
        self._assign_cohorts(customers, rng, config)
        self._assign_clv_segments(customers, rng)
        self._assign_products(customers, rng)
        agreements = self._generate_agreements(customers, config, rng, ids)
        self._assign_open_dates(customers, agreements, config, rng)
        self._assign_balances(customers, agreements, rng)
        self._assign_balance_trajectories(customers, agreements, rng, config)
        self._assign_status_flags(agreements, rng)
        addresses = self._generate_address_pool(config, rng, ids)
        self._assign_addresses(customers, addresses, rng)
        return GenerationContext(
            rng=rng,
            ids=ids,
            config=config,
            customers=customers,
            agreements=agreements,
            addresses=addresses,
            tables={},
        )

    # ------------------------------------------------------------------
    # Phase methods
    # ------------------------------------------------------------------

    def _generate_customer_shells(
        self, config, rng: np.random.Generator, ids: IdFactory
    ) -> List[CustomerProfile]:
        n = config.TARGET_CUSTOMERS
        n_ind = round(n * config.INDIVIDUAL_PCT)
        n_org = n - n_ind

        party_types: List[str] = ['INDIVIDUAL'] * n_ind + ['ORGANIZATION'] * n_org
        rng.shuffle(party_types)

        party_ids = ids.next_many('party', n)

        _placeholder_date = date(2000, 1, 1)

        customers: List[CustomerProfile] = []
        for pid, ptype in zip(party_ids, party_types):
            cp = CustomerProfile(
                party_id=pid,
                party_type=ptype,
                age=0,
                income_quartile=1,
                lifecycle_cohort='',
                clv_segment=1,
                gender_type_cd=None,
                marital_status_cd=None,
                ethnicity_type_cd=None,
                occupation_cd=None,
                num_dependents=0,
                fico_score=0,
                household_id=None,
                household_role='HEAD',
                lifecl=1,
                has_internet=False,
                preferred_channel_cd=1,
                party_since=_placeholder_date,
                address_id=0,
            )
            customers.append(cp)
        return customers

    def _assign_demographics(
        self, customers: List[CustomerProfile], rng: np.random.Generator
    ) -> None:
        individuals = [cp for cp in customers if cp.party_type == 'INDIVIDUAL']
        organizations = [cp for cp in customers if cp.party_type == 'ORGANIZATION']
        n_ind = len(individuals)

        # Batch demographic draws for individuals
        ages        = sample_age(rng, n_ind)
        ethnicities = sample_ethnicity(rng, n_ind)
        genders     = sample_gender(rng, n_ind)
        occupations = sample_occupation(rng, n_ind)
        # All customers get income quartile (orgs too — used for product decisions)
        all_iqs = sample_income_quartile(rng, len(customers))

        # Build a map from party_id to index in all_customers for IQ assignment
        for i, cp in enumerate(customers):
            cp.income_quartile = int(all_iqs[i])

        for i, cp in enumerate(individuals):
            cp.age            = int(ages[i])
            cp.ethnicity_type_cd = str(ethnicities[i])
            cp.gender_type_cd    = str(genders[i])
            cp.occupation_cd     = str(occupations[i])
            cp.marital_status_cd = sample_marital(rng, cp.age)
            cp.fico_score        = sample_fico(rng, cp.ethnicity_type_cd, cp.income_quartile)
            cp.has_internet      = bool(rng.random() < 0.897)
            if cp.has_internet:
                cp.preferred_channel_cd = int(rng.choice([3, 4]))
            else:
                cp.preferred_channel_cd = 1

        # Organizations
        if organizations:
            fake_org = Faker('en_US')
            fake_org.seed_instance(int(rng.integers(0, 2**32 - 1)))
            naics_arr = rng.choice(_NAICS_SECTORS, size=len(organizations))
            sic_arr   = rng.choice(_SIC_CODES,     size=len(organizations))
            gics_arr  = rng.choice(_GICS_SECTORS,  size=len(organizations))

            for i, cp in enumerate(organizations):
                cp.age                = 0
                cp.gender_type_cd     = None
                cp.marital_status_cd  = None
                cp.ethnicity_type_cd  = None
                cp.occupation_cd      = None
                cp.num_dependents     = 0
                cp.fico_score         = 0
                cp.has_internet       = False
                cp.preferred_channel_cd = 1
                cp.org_name           = fake_org.company()
                cp.naics_sector_cd    = str(naics_arr[i])
                cp.sic_cd             = str(sic_arr[i])
                cp.gics_sector_cd     = str(gics_arr[i])

    def _assign_households(
        self, customers: List[CustomerProfile], rng: np.random.Generator, ids: IdFactory
    ) -> None:
        for cp in customers:
            if cp.party_type == 'ORGANIZATION':
                cp.lifecl         = 1
                cp.household_id   = None
                cp.household_role = 'HEAD'
                continue
            cp.lifecl = sample_lifecl(rng, cp.age)
            cp.num_dependents = sample_kids(rng, cp.lifecl)

        # Pair MARRIED individuals with lifecl 2 or 3 into households
        candidates = [
            cp for cp in customers
            if cp.party_type == 'INDIVIDUAL'
            and cp.marital_status_cd == 'MARRIED'
            and cp.lifecl in {2, 3}
        ]
        # Shuffle candidates so pairings are random but reproducible
        indices = list(range(len(candidates)))
        rng.shuffle(indices)
        shuffled = [candidates[i] for i in indices]

        i = 0
        while i + 1 < len(shuffled):
            head = shuffled[i]
            spouse = shuffled[i + 1]
            hid = ids.next('household')
            head.household_id   = hid
            head.household_role = 'HEAD'
            spouse.household_id = hid
            spouse.household_role = 'SPOUSE'
            i += 2

    def _assign_cohorts(
        self, customers: List[CustomerProfile], rng: np.random.Generator, config
    ) -> None:
        n = len(customers)
        n_active   = round(n * config.COHORT_ACTIVE_PCT)
        n_declining = round(n * config.COHORT_DECLINING_PCT)
        n_churned  = round(n * config.COHORT_CHURNED_PCT)
        n_new      = n - n_active - n_declining - n_churned

        labels: List[str] = (
            ['ACTIVE']    * n_active +
            ['DECLINING'] * n_declining +
            ['CHURNED']   * n_churned +
            ['NEW']       * n_new
        )
        rng.shuffle(labels)
        for cp, label in zip(customers, labels):
            cp.lifecycle_cohort = label

    def _assign_clv_segments(
        self, customers: List[CustomerProfile], rng: np.random.Generator
    ) -> None:
        segments = np.arange(1, 11)
        for cp in customers:
            weights = _CLV_W[cp.lifecycle_cohort]
            cp.clv_segment = int(rng.choice(segments, p=weights))

    def _assign_products(
        self, customers: List[CustomerProfile], rng: np.random.Generator
    ) -> None:
        for cp in customers:
            if cp.party_type == 'ORGANIZATION':
                cp.product_set = ['COMMERCIAL_CHECKING']
                continue

            age = cp.age
            iq  = cp.income_quartile
            lc  = cp.lifecl
            cohort = cp.lifecycle_cohort

            # 10% unbanked
            if rng.random() < 0.10:
                cp.product_set = []
                continue

            products: List[str] = ['CHECKING']

            # Age-conditional ownership rates
            retirement_rate = 0.591
            if age < 35:
                retirement_rate = 0.451
            elif age >= 55:
                retirement_rate = 0.646
            # Q4 income boosts retirement ownership
            if iq == 4:
                retirement_rate = min(0.90, retirement_rate * 1.30)
            elif iq == 1:
                retirement_rate = max(0.13, retirement_rate * 0.50)

            mortgage_rate = 0.396
            if age < 35:
                mortgage_rate = 0.237
            elif 45 <= age <= 64:
                mortgage_rate = 0.500

            student_rate = 0.177
            if age < 35:
                student_rate = 0.350
            elif age > 50:
                student_rate = 0.020

            vehicle_rate = 0.303
            if lc == 3:
                vehicle_rate = min(0.55, vehicle_rate * 1.30)

            # Scale factor ~0.40: SCF rates are all-institution ownership rates;
            # per-bank penetration is roughly 40% of that, calibrated to yield
            # ~5,000 total agreements from ~3,000 customers.
            S = 0.40
            checks = [
                ('SAVINGS',               0.484 * S),
                ('MMA',                   0.200 * S),
                ('CERTIFICATE_OF_DEPOSIT',0.078 * S),
                ('RETIREMENT',            retirement_rate * S),
                ('MORTGAGE',              mortgage_rate * S),
                ('CREDIT_CARD',           0.378 * S),
                ('VEHICLE_LOAN',          vehicle_rate * S),
                ('STUDENT_LOAN',          student_rate * S),
                ('PAYDAY',                0.019 * S),
            ]

            for product, rate in checks:
                if rng.random() < rate:
                    products.append(product)

            # HELOC requires MORTGAGE
            if 'MORTGAGE' in products and rng.random() < 0.034 * S:
                products.append('HELOC')

            # CLV top-decile: force at least 4 products (up to 8)
            if cp.clv_segment == 10 and len(products) < 4:
                extras = [
                    p for p in ['SAVINGS', 'RETIREMENT', 'CREDIT_CARD', 'VEHICLE_LOAN',
                                 'CERTIFICATE_OF_DEPOSIT', 'MORTGAGE']
                    if p not in products
                ]
                rng.shuffle(extras)
                for p in extras:
                    if len(products) >= 4:
                        break
                    products.append(p)

            # NEW cohort — simpler Maslow-hierarchy product set
            if cohort == 'NEW':
                keep = {'CHECKING'}
                if age < 35:
                    keep.update(p for p in products if p in {'SAVINGS', 'STUDENT_LOAN'})
                elif age < 55:
                    keep.update(p for p in products if p in {'SAVINGS', 'MORTGAGE', 'VEHICLE_LOAN'})
                else:
                    keep.update(p for p in products if p in {'SAVINGS', 'RETIREMENT'})
                products = [p for p in products if p in keep]

            cp.product_set = products

    def _generate_agreements(
        self,
        customers: List[CustomerProfile],
        config,
        rng: np.random.Generator,
        ids: IdFactory,
    ) -> List[AgreementProfile]:
        # Mint one product_id per distinct product type
        all_types = {p for cp in customers for p in cp.product_set}
        product_type_ids: Dict[str, int] = {}
        for pt in sorted(all_types):  # sorted for determinism
            product_type_ids[pt] = ids.next('product')

        agreements: List[AgreementProfile] = []
        _placeholder_dt = datetime(2000, 1, 1)
        _zero = Decimal('0.0000')
        _zero_rate = Decimal('0.000000000000')

        for cp in customers:
            for product_type in cp.product_set:
                flags = _PRODUCT_FLAGS[product_type]
                (is_fin, is_dep, is_td, is_cr, is_lt, is_mort, is_cc, is_lx) = flags

                terminal = sum([is_td, is_mort, is_cc, is_lx])
                assert terminal <= 1, (
                    f"product_type={product_type!r} has {terminal} terminal flags — "
                    "check _PRODUCT_FLAGS"
                )

                ap = AgreementProfile(
                    agreement_id=ids.next('agreement'),
                    owner_party_id=cp.party_id,
                    product_type=product_type,
                    agreement_subtype_cd=product_type,
                    product_id=product_type_ids[product_type],
                    open_dttm=_placeholder_dt,
                    close_dttm=None,
                    balance_amt=_zero,
                    interest_rate=_zero_rate,
                    original_loan_amt=None,
                    is_delinquent=False,
                    is_severely_delinquent=False,
                    is_frozen=False,
                    monthly_balances=[],
                    is_financial=is_fin,
                    is_deposit=is_dep,
                    is_term_deposit=is_td,
                    is_credit=is_cr,
                    is_loan_term=is_lt,
                    is_mortgage=is_mort,
                    is_credit_card=is_cc,
                    is_loan_transaction=is_lx,
                )
                agreements.append(ap)

        return agreements

    def _assign_open_dates(
        self,
        customers: List[CustomerProfile],
        agreements: List[AgreementProfile],
        config,
        rng: np.random.Generator,
    ) -> None:
        owner_to_cohort: Dict[int, str] = {cp.party_id: cp.lifecycle_cohort for cp in customers}

        # Group agreements by owner for party_since computation
        owner_agreements: Dict[int, List[AgreementProfile]] = {}
        for ap in agreements:
            owner_agreements.setdefault(ap.owner_party_id, []).append(ap)

        for ap in agreements:
            cohort = owner_to_cohort[ap.owner_party_id]
            lo, hi = _COHORT_OPEN_WINDOWS[cohort]
            ap.open_dttm = random_datetime_between(lo, hi, rng)

            if cohort == 'CHURNED':
                clo, chi = _CHURNED_CLOSE_WINDOW
                ap.close_dttm = random_datetime_between(clo, chi, rng)
            else:
                ap.close_dttm = None

        # Assign party_since per customer
        owner_set: Dict[int, str] = {cp.party_id: cp.lifecycle_cohort for cp in customers}
        for cp in customers:
            own_ags = owner_agreements.get(cp.party_id, [])
            cohort = owner_set[cp.party_id]

            if not own_ags:
                # Unbanked / empty product_set
                cp.party_since = random_date_between(date(2015, 1, 1), config.SIM_DATE, rng)
            elif cohort == 'NEW':
                cp.party_since = random_date_between(date(2026, 1, 15), date(2026, 3, 31), rng)
            else:
                cp.party_since = min(ag.open_dttm.date() for ag in own_ags)

    def _assign_balances(
        self,
        customers: List[CustomerProfile],
        agreements: List[AgreementProfile],
        rng: np.random.Generator,
    ) -> None:
        owner_to_cp: Dict[int, CustomerProfile] = {cp.party_id: cp for cp in customers}

        _mortgage_age_medians = {
            'u35': 194_000.0, '35_44': 180_000.0, '45_54': 160_000.0,
            '55_64': 140_000.0, '65p': 130_000.0,
        }

        for ap in agreements:
            cp = owner_to_cp[ap.owner_party_id]
            iq = cp.income_quartile
            pt = ap.product_type

            if pt in _DEPOSIT_TYPES:
                ap.balance_amt = sample_deposit_balance(rng, iq)
                ap.interest_rate = _FIXED_RATES[pt]
                ap.original_loan_amt = None

            elif pt == 'CREDIT_CARD':
                carry_rate = _CC_CARRY_RATE[iq]
                if rng.random() < carry_rate:
                    ap.balance_amt = sample_cc_balance(rng, iq)
                else:
                    ap.balance_amt = Decimal('0.0000')
                ap.interest_rate = _FIXED_RATES['CREDIT_CARD']
                ap.original_loan_amt = None

            elif pt == 'HELOC':
                ap.balance_amt = _lognormal_decimal_local(rng, 25_000.0, 0.8, 0.0, 250_000.0)
                ap.interest_rate = _FIXED_RATES['HELOC']
                ap.original_loan_amt = None

            elif pt == 'MORTGAGE':
                age = cp.age
                if age < 35:
                    median = _mortgage_age_medians['u35']
                elif age < 45:
                    median = _mortgage_age_medians['35_44']
                elif age < 55:
                    median = _mortgage_age_medians['45_54']
                elif age < 65:
                    median = _mortgage_age_medians['55_64']
                else:
                    median = _mortgage_age_medians['65p']
                ap.balance_amt = _lognormal_decimal_local(rng, median, 0.5, 5_000.0, 1_500_000.0)
                ap.interest_rate = sample_mortgage_rate(rng, ap.open_dttm.year)
                ap.original_loan_amt = (ap.balance_amt * Decimal('1.15')).quantize(Decimal('0.0001'))

            elif pt == 'VEHICLE_LOAN':
                ap.balance_amt = _lognormal_decimal_local(rng, 15_000.0, 0.6, 500.0, 80_000.0)
                ap.interest_rate = _FIXED_RATES['VEHICLE_LOAN']
                ap.original_loan_amt = (ap.balance_amt * Decimal('1.3')).quantize(Decimal('0.0001'))

            elif pt == 'STUDENT_LOAN':
                age = cp.age
                median = 18_000.0 if age < 30 else (25_000.0 if age < 40 else 15_000.0)
                ap.balance_amt = _lognormal_decimal_local(rng, median, 0.7, 500.0, 200_000.0)
                ap.interest_rate = _FIXED_RATES['STUDENT_LOAN']
                ap.original_loan_amt = (ap.balance_amt * Decimal('1.1')).quantize(Decimal('0.0001'))

            elif pt == 'PAYDAY':
                ap.balance_amt = Decimal('500.0000')
                ap.interest_rate = _FIXED_RATES['PAYDAY']
                ap.original_loan_amt = None

            else:
                # Fallback — should not occur with the defined product types
                ap.balance_amt = Decimal('0.0000')
                ap.interest_rate = Decimal('0.000000000000')
                ap.original_loan_amt = None

    def _assign_balance_trajectories(
        self,
        customers: List[CustomerProfile],
        agreements: List[AgreementProfile],
        rng: np.random.Generator,
        config,
    ) -> None:
        """Populate monthly_balances for DECLINING and CHURNED cohort agreements."""
        month_snapshots(config.HISTORY_START, config.SIM_DATE)  # assert 6 tuples exist

        owner_to_cohort: Dict[int, str] = {cp.party_id: cp.lifecycle_cohort for cp in customers}

        for ap in agreements:
            cohort = owner_to_cohort[ap.owner_party_id]

            if cohort == 'DECLINING':
                # Decline 5–25% per month across 6 months
                bal = ap.balance_amt
                balances: List[Decimal] = [bal]
                for _ in range(5):
                    pct = Decimal(str(round(rng.uniform(0.05, 0.25), 6)))
                    bal = (bal * (Decimal('1') - pct)).quantize(Decimal('0.0001'))
                    if bal < Decimal('0'):
                        bal = Decimal('0.0000')
                    balances.append(bal)
                ap.monthly_balances = balances

            else:
                # CHURNED, ACTIVE, NEW — no monthly_balances trajectory.
                # CHURNED near-zero balance at close is handled by Tier 7a
                # AGREEMENT_FEATURE rows using balance_amt directly.
                ap.monthly_balances = []

    def _assign_status_flags(
        self, agreements: List[AgreementProfile], rng: np.random.Generator
    ) -> None:
        for ap in agreements:
            if ap.product_type in _DEPOSIT_TYPES:
                ap.is_delinquent          = False
                ap.is_severely_delinquent = False
                ap.is_frozen              = False
            else:
                ap.is_delinquent = bool(rng.random() < 0.112)
                # is_severely_delinquent is a strict subset of is_delinquent
                # conditional probability: P(LATE60|LATE) = 0.046/0.112 ≈ 0.411
                if ap.is_delinquent:
                    ap.is_severely_delinquent = bool(rng.random() < (0.046 / 0.112))
                else:
                    ap.is_severely_delinquent = False
                # is_frozen only for credit / loan agreements, ~0.5%
                if ap.is_credit or ap.is_loan_term:
                    ap.is_frozen = bool(rng.random() < 0.005)
                else:
                    ap.is_frozen = False

    def _generate_address_pool(
        self, config, rng: np.random.Generator, ids: IdFactory
    ) -> List[AddressRecord]:
        n = 500
        fake = Faker('en_US')
        fake.seed_instance(int(rng.integers(0, 2**32 - 1)))

        city_ids       = rng.integers(1, 101,  size=n)
        county_ids     = rng.integers(1, 51,   size=n)
        territory_ids  = rng.integers(1, 51,   size=n)
        postal_ids     = rng.integers(1, 201,  size=n)
        latitudes      = rng.uniform(25.0, 49.0,    size=n)
        longitudes     = rng.uniform(-125.0, -65.0, size=n)

        _directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
        _suffixes   = ['ST', 'AVE', 'BLVD', 'DR', 'LN', 'CT', 'RD', 'WAY']
        dir_arr = rng.choice(_directions, size=n)
        suf_arr = rng.choice(_suffixes,   size=n)

        addresses: List[AddressRecord] = []
        for i in range(n):
            street = fake.street_address()
            # Extract house number (first token) and remainder as street name
            parts = street.split(' ', 1)
            house_num   = parts[0] if len(parts) > 0 else '1'
            street_name = parts[1] if len(parts) > 1 else street

            ar = AddressRecord(
                address_id=ids.next('address'),
                address_subtype_cd='PHYSICAL',
                street_line_1=street,
                street_line_2=None,
                house_num=house_num,
                street_name=street_name,
                street_direction_type_cd=str(dir_arr[i]),
                street_suffix_cd=str(suf_arr[i]),
                city_id=int(city_ids[i]),
                county_id=int(county_ids[i]),
                territory_id=int(territory_ids[i]),
                postal_code_id=int(postal_ids[i]),
                country_id=1,
                latitude=float(latitudes[i]),
                longitude=float(longitudes[i]),
            )
            addresses.append(ar)
        return addresses

    def _assign_addresses(
        self,
        customers: List[CustomerProfile],
        addresses: List[AddressRecord],
        rng: np.random.Generator,
    ) -> None:
        addr_ids = [a.address_id for a in addresses]
        n_addr = len(addr_ids)
        indices = rng.integers(0, n_addr, size=len(customers))
        for cp, idx in zip(customers, indices):
            cp.address_id = addr_ids[int(idx)]


def _lognormal_decimal_local(
    rng: np.random.Generator,
    median: float,
    sigma: float,
    lo: float,
    hi: float,
) -> Decimal:
    raw = float(np.clip(rng.lognormal(mean=np.log(median), sigma=sigma), lo, hi))
    return round(Decimal(str(raw)), 4)


if __name__ == '__main__':
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    import numpy as _np
    from config import settings as _settings

    ctx = UniverseBuilder().build(_settings, _np.random.default_rng(42))
    assert 2950 <= len(ctx.customers) <= 3050, f'customers={len(ctx.customers)}'
    assert 4700 <= len(ctx.agreements) <= 5300, f'agreements={len(ctx.agreements)}'
    assert ctx.tables == {}, 'tables must be empty'
    print(f'registry/universe.py OK: {len(ctx.customers)} customers, {len(ctx.agreements)} agreements')

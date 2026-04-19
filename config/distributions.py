"""
Statistical samplers — SCF 2022 and WP5 distributions.
All functions are pure: they take rng as the first argument, return a value,
and never mutate module state, cache results, print, or read from disk.
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _lognormal_decimal(
    rng: np.random.Generator,
    median: float,
    sigma: float,
    lo: float,
    hi: float,
    decimals: int = 4,
) -> Decimal:
    raw = float(np.clip(rng.lognormal(mean=np.log(median), sigma=sigma), lo, hi))
    return round(Decimal(str(raw)), decimals)


# ---------------------------------------------------------------------------
# Public samplers
# ---------------------------------------------------------------------------

# AGECL bucket definitions (inclusive ranges)
_AGE_BUCKETS = [(20, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 82)]
_AGE_WEIGHTS = np.array([0.133, 0.166, 0.178, 0.223, 0.188, 0.110])
_AGE_WEIGHTS = _AGE_WEIGHTS / _AGE_WEIGHTS.sum()


def sample_age(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n ages drawn from SCF AGECL distribution (ranges 20-34 … 75-82)."""
    buckets = rng.choice(len(_AGE_BUCKETS), size=n, p=_AGE_WEIGHTS)
    ages = np.empty(n, dtype=np.int64)
    for i, (lo, hi) in enumerate(_AGE_BUCKETS):
        mask = buckets == i
        if mask.any():
            ages[mask] = rng.integers(lo, hi + 1, size=int(mask.sum()))
    return ages


def sample_income_quartile(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n income quartile labels (1–4) from SCF INCQRTCAT distribution."""
    return rng.choice([1, 2, 3, 4], size=n, p=[0.25, 0.25, 0.25, 0.25])


_FICO_ETH_ADJ = {
    'WHITE': 20, 'ASIAN': 20,
    'BLACK': -50, 'HISPANIC': -25, 'OTHER': -25,
}


def sample_fico(
    rng: np.random.Generator,
    ethnicity: str,
    income_quartile: int,
) -> int:
    """Return a FICO score (300–850) calibrated by ethnicity and income quartile."""
    base = 600 + 50 * income_quartile
    adj = _FICO_ETH_ADJ.get(ethnicity, 0)
    jitter = rng.normal(0.0, 40.0)
    return int(np.clip(base + adj + jitter, 300, 850))


_DEPOSIT_MEDIANS = {1: 350.0, 2: 1_600.0, 3: 4_000.0, 4: 23_000.0}
_DEPOSIT_CLIPS = {1: (1.0, 5_000.0), 2: (1.0, 50_000.0),
                  3: (1.0, 150_000.0), 4: (1.0, 500_000.0)}


def sample_deposit_balance(
    rng: np.random.Generator,
    income_quartile: int,
) -> Decimal:
    """Return a deposit balance (Decimal) from SCF income-quartile stratified log-normal."""
    median = _DEPOSIT_MEDIANS[income_quartile]
    lo, hi = _DEPOSIT_CLIPS[income_quartile]
    return _lognormal_decimal(rng, median, sigma=1.0, lo=lo, hi=hi, decimals=4)


_CC_MEDIANS = {1: 1_200.0, 2: 1_700.0, 3: 3_000.0, 4: 5_600.0}


def sample_cc_balance(
    rng: np.random.Generator,
    income_quartile: int,
) -> Decimal:
    """Return a credit-card balance (Decimal) conditioned on income quartile.

    Always returns the lognormal draw. The caller (_assign_balances) decides
    whether to use it or substitute Decimal('0.0000') based on the carrying rate.
    """
    median = _CC_MEDIANS[income_quartile]
    return _lognormal_decimal(rng, median, sigma=0.9, lo=1.0, hi=50_000.0, decimals=4)


def sample_mortgage_rate(
    rng: np.random.Generator,
    origination_year: int,
) -> Decimal:
    """Return a mortgage rate (Decimal) based on origination-year vintage (Part I1)."""
    if origination_year < 2020:
        rate = rng.uniform(3.5, 4.5)
    elif origination_year == 2020:
        rate = rng.uniform(2.8, 3.2)
    elif origination_year == 2021:
        rate = rng.uniform(2.9, 3.3)
    elif origination_year == 2022:
        rate = rng.uniform(5.0, 7.0)
    else:
        rate = rng.uniform(6.5, 7.5)
    # Store as a fraction (0.035 not 3.5) rounded to 12 dp
    return round(Decimal(str(rate / 100.0)), 12)


_INCOME_RANGES = {
    'EMP':         (24_000.0,   450_000.0),
    'SELF_EMP':    (30_000.0, 5_000_000.0),
    'RETIRED':     (12_000.0,   500_000.0),
    'NOT_WORKING': (10_000.0,   150_000.0),
}


def sample_annual_income(
    rng: np.random.Generator,
    occupation_cd: str,
    income_quartile: int,
) -> Decimal:
    """Return annual income (Decimal) from occupation-based stratified ranges."""
    lo, hi = _INCOME_RANGES.get(occupation_cd, (10_000.0, 150_000.0))
    span = hi - lo
    q_lo = lo + span * (income_quartile - 1) * 0.25
    q_hi = lo + span * income_quartile * 0.25
    raw = rng.uniform(q_lo, q_hi)
    return round(Decimal(str(raw)), 4)


_ETH_W = np.array([0.597, 0.134, 0.115, 0.073, 0.080])
_ETH_W = _ETH_W / _ETH_W.sum()


def sample_ethnicity(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n ethnicity codes from SCF distribution."""
    return rng.choice(
        ['WHITE', 'BLACK', 'HISPANIC', 'ASIAN', 'OTHER'],
        size=n,
        p=_ETH_W,
    )


def sample_gender(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n gender type codes (50/50 neutral per Part A2 note)."""
    return rng.choice(['MALE', 'FEMALE'], size=n, p=[0.50, 0.50])


def sample_marital(rng: np.random.Generator, age: int) -> str:
    """Return a marital status code conditioned on age."""
    if age < 25:
        p_single = 0.90
    elif age <= 35:
        p_single = 0.55
    else:
        p_single = 0.368
    return 'SINGLE' if rng.random() < p_single else 'MARRIED'


_OCC_W = np.array([0.496, 0.217, 0.248, 0.039])
_OCC_W = _OCC_W / _OCC_W.sum()


def sample_occupation(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n occupation codes from SCF distribution (Part A7)."""
    return rng.choice(
        ['EMP', 'SELF_EMP', 'RETIRED', 'NOT_WORKING'],
        size=n,
        p=_OCC_W,
    )


# Part A4 weights for 1/2/3+ kids, renormalized to sum=1 over {1,2,3}
_KIDS_P = np.array([17.8, 13.9, 8.1])
_KIDS_P = _KIDS_P / _KIDS_P.sum()


def sample_kids(rng: np.random.Generator, lifecl: int) -> int:
    """Return number of dependents (0–5) conditioned on household lifecycle stage."""
    if lifecl in {1, 2, 4, 5, 6}:
        return 0
    # LIFECL 3 — families with children
    return int(rng.choice([1, 2, 3], p=_KIDS_P))


# Part A8 weights [LIFECL1..6] = [11.5, 8.2, 21.4, 6.7, 29.1, 23.1]
# Under-55 subset: LIFECL 1/2/3, renormalized
_LIFECL_YOUNG_W = np.array([11.5, 8.2, 21.4])
_LIFECL_YOUNG_W = _LIFECL_YOUNG_W / _LIFECL_YOUNG_W.sum()
# 55+ subset: LIFECL 4/5/6, renormalized
_LIFECL_OLD_W = np.array([6.7, 29.1, 23.1])
_LIFECL_OLD_W = _LIFECL_OLD_W / _LIFECL_OLD_W.sum()


def sample_lifecl(rng: np.random.Generator, age: int) -> int:
    """Return household lifecycle stage (1–6) conditioned on age."""
    if age < 55:
        return int(rng.choice([1, 2, 3], p=_LIFECL_YOUNG_W))
    return int(rng.choice([4, 5, 6], p=_LIFECL_OLD_W))

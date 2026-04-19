"""
Statistical sampler stubs. Signatures and docstrings only.
Real implementations are delivered in Step 4 (UniverseBuilder).
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    pass


def sample_age(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n ages drawn from SCF AGECL distribution (ranges 20-34 … 75-82)."""
    raise NotImplementedError("Implemented in Step 4")


def sample_income_quartile(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n income quartile labels (1–4) from SCF INCQRTCAT distribution."""
    raise NotImplementedError("Implemented in Step 4")


def sample_fico(
    rng: np.random.Generator,
    ethnicity: str,
    income_quartile: int,
) -> int:
    """Return a FICO score (300–850) calibrated by ethnicity and income quartile."""
    raise NotImplementedError("Implemented in Step 4")


def sample_deposit_balance(
    rng: np.random.Generator,
    income_quartile: int,
) -> Decimal:
    """Return a deposit balance (Decimal) from SCF income-quartile stratified log-normal."""
    raise NotImplementedError("Implemented in Step 4")


def sample_cc_balance(
    rng: np.random.Generator,
    income_quartile: int,
) -> Decimal:
    """Return a credit-card balance (Decimal) conditioned on income quartile."""
    raise NotImplementedError("Implemented in Step 4")


def sample_mortgage_rate(
    rng: np.random.Generator,
    origination_year: int,
) -> Decimal:
    """Return a mortgage rate (Decimal) based on origination-year vintage."""
    raise NotImplementedError("Implemented in Step 4")


def sample_annual_income(
    rng: np.random.Generator,
    occupation_cd: str,
    income_quartile: int,
) -> Decimal:
    """Return annual income (Decimal) from occupation-based stratified ranges."""
    raise NotImplementedError("Implemented in Step 4")


def sample_ethnicity(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n ethnicity codes from SCF distribution."""
    raise NotImplementedError("Implemented in Step 4")


def sample_gender(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n gender type codes."""
    raise NotImplementedError("Implemented in Step 4")


def sample_marital(rng: np.random.Generator, age: int) -> str:
    """Return a marital status code conditioned on age."""
    raise NotImplementedError("Implemented in Step 4")


def sample_occupation(rng: np.random.Generator, n: int) -> np.ndarray:
    """Return n occupation codes from SCF distribution."""
    raise NotImplementedError("Implemented in Step 4")


def sample_kids(rng: np.random.Generator, lifecl: int) -> int:
    """Return number of dependents (0–5) conditioned on household lifecycle stage."""
    raise NotImplementedError("Implemented in Step 4")


def sample_lifecl(rng: np.random.Generator, age: int) -> int:
    """Return household lifecycle stage (1–6) conditioned on age."""
    raise NotImplementedError("Implemented in Step 4")

# Spec: Step 03 — Registry Profiles & GenerationContext

## Overview

This step defines the in-memory data containers that carry every correlated decision through the generator. `CustomerProfile`, `AgreementProfile`, and `AddressRecord` are the three dataclasses the `UniverseBuilder` (Step 4) populates before any CSV is written; `GenerationContext` is the single object threaded through every tier generator. Per `mvp-tool-design.md` §4 "Registry Design" and §6 "GenerationContext", these are **pure data containers — no statistical sampling, no I/O, no business logic**. Every field shape on these dataclasses is fixed by the tier generators that read them downstream (Steps 10–23). This step exists before Step 4 so the UniverseBuilder has concrete types to populate, and before every tier generator so `ctx.customers` / `ctx.agreements` / `ctx.addresses` / `ctx.tables` have a stable shape.

## Depends on

- **Step 1** (`afa2f27` on `main`). Consumes from `config/settings.py`: `ID_RANGES` (for `IdFactory` construction later in Step 4), `SEED` (informational — the `rng` held on `GenerationContext` is seeded from this by Step 4's orchestrator, not by this step). No direct consumption of `code_values.py` or `distributions.py`.
- **Step 2** (`fdc5561` on `main`). Consumes from `utils/id_factory.py`: the `IdFactory` class — used as the type annotation for `GenerationContext.ids`. No consumption of `BaseGenerator`, `stamp_di`, `stamp_valid`, `luhn`, or `date_utils` — those are tier-generator concerns, not registry concerns.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 3):
- `mvp-tool-design.md` §4 (Registry Design — `CustomerProfile` and `AgreementProfile` full field lists, types, nullability)
- `mvp-tool-design.md` §6 (`GenerationContext` — fields: customers, agreements, addresses, config, rng, ids, tables dict; Schema.TABLE keying convention)
- `mvp-tool-design.md` §5 (UniverseBuilder build sequence — informs what AddressRecord must carry, since `_generate_address_pool` and `_assign_addresses` populate the address pool before tiers run)
- `mvp-tool-design.md` §9 Tier 5 (location CSVs — the tier that eventually writes AddressRecord data out; determines the minimum fields AddressRecord must carry so Tier 5 is a pure transformation)
- `PRD.md` §7.1 (BIGINT everywhere — every `*_id` field on every dataclass is a Python `int` with BIGINT semantics; no INTEGER truncation, no UUID/string IDs)
- `PRD.md` §7.2 (Shared party ID space — `CustomerProfile.party_id` is the single value used as both `Core_DB.Party_Id` and `CDM_DB.CDM_Party_Id`)
- `PRD.md` §7.5 (Exclusive AGREEMENT sub-typing — the `AgreementProfile.is_*` flags are mutually exclusive where the DDL inheritance chain demands it)
- `PRD.md` §7.12 (Self-employed placeholder — `CustomerProfile.occupation_cd == 'SELF_EMP'` is the flag Step 4/11 will use to route `INDIVIDUAL_PAY_TIMING.Business_Party_Id` to `SELF_EMP_ORG_ID`)
- `implementation-steps.md` Step 3 entry

**Additional reference files** (only those named in the step's "Reads from" line):
- None. `implementation-steps.md` Step 3 lists only `mvp-tool-design.md` §4, §6. No `references/*.md` file is required for this step.

## Produces

All paths relative to the project root.

**`registry/` package** (directory exists from Step 1 but is currently empty):

- `registry/__init__.py` — empty marker so `registry` is importable as a package.
- `registry/profiles.py` — the three in-memory profile dataclasses populated by `UniverseBuilder` in Step 4. All three use `@dataclass` (not `@dataclass(frozen=True)` — Step 4 mutates fields across its `_assign_*` phases). Field lists below are the contract; Step 4 MUST populate every non-Optional field before returning from `build()`.
  - `CustomerProfile` — fields per `mvp-tool-design.md` §4:
    - Identity: `party_id: int` (BIGINT), `party_type: str` (`'INDIVIDUAL' | 'ORGANIZATION'`)
    - Demographics: `age: int`, `income_quartile: int` (1–4), `lifecycle_cohort: str` (`'ACTIVE' | 'DECLINING' | 'CHURNED' | 'NEW'`), `clv_segment: int` (1–10 decile)
    - Individual attributes (all `Optional` — `None` for ORGANIZATION): `gender_type_cd: Optional[str]`, `marital_status_cd: Optional[str]`, `ethnicity_type_cd: Optional[str]`, `occupation_cd: Optional[str]`, `num_dependents: int` (defaults 0 for orgs), `fico_score: int` (defaults 0 for orgs — never NULL because Step 4 always samples or zero-fills)
    - Household: `household_id: Optional[int]`, `household_role: str` (`'HEAD' | 'SPOUSE' | 'DEPENDENT'` — defaults `'HEAD'` for singletons/orgs), `lifecl: int` (1–6; SCF LIFECL stage)
    - Channel / contact: `has_internet: bool`, `preferred_channel_cd: int` (SMALLINT per `01_schema-reference.md` SMALLINT Code Enumerations — CDM `Channel_Type_Cd`: 1=BRANCH, 3=ONLINE, 4=MOBILE)
    - Products: `product_set: List[str]` (default_factory=list; values from the product type enumeration in `config/code_values.py` / Step 1 — e.g. `'CHECKING'`, `'SAVINGS'`, `'MMA'`, `'CERTIFICATE_OF_DEPOSIT'`, `'RETIREMENT'`, `'MORTGAGE'`, `'CREDIT_CARD'`, `'VEHICLE_LOAN'`, `'STUDENT_LOAN'`, `'HELOC'`, `'PAYDAY'`, `'COMMERCIAL_CHECKING'`)
    - Dates: `party_since: date`
    - Address: `address_id: int` (BIGINT — FK to `AddressRecord.address_id` in `ctx.addresses`)
    - Org-specific (all `Optional` — `None` for INDIVIDUAL): `org_name: Optional[str]`, `naics_sector_cd: Optional[str]`, `sic_cd: Optional[str]`, `gics_sector_cd: Optional[str]`
  - `AgreementProfile` — fields per `mvp-tool-design.md` §4:
    - Identity: `agreement_id: int` (BIGINT), `owner_party_id: int` (BIGINT — FK to `CustomerProfile.party_id`), `product_type: str` (one of the product-type strings above), `agreement_subtype_cd: str` (matches `AGREEMENT_SUBTYPE` seed table code), `product_id: int` (BIGINT — FK to Core_DB.PRODUCT)
    - Temporal: `open_dttm: datetime`, `close_dttm: Optional[datetime]` (None = open; set for CHURNED cohort only)
    - Financial: `balance_amt: Decimal`, `interest_rate: Decimal`, `original_loan_amt: Optional[Decimal]` (only loan/mortgage agreements)
    - Status flags: `is_delinquent: bool`, `is_severely_delinquent: bool`, `is_frozen: bool`
    - Balance trajectory: `monthly_balances: List[Decimal]` (default_factory=list; exactly 6 values for DECLINING cohort, else may be empty)
    - Agreement sub-type path flags (exclusive sub-typing — every agreement follows exactly one terminal-leaf path per PRD §7.5; parent-chain flags `is_financial`, `is_deposit`, `is_credit`, `is_loan_term` may be True simultaneously with their descendants): `is_financial: bool`, `is_deposit: bool`, `is_term_deposit: bool`, `is_credit: bool`, `is_loan_term: bool`, `is_mortgage: bool`, `is_credit_card: bool`, `is_loan_transaction: bool`
  - `AddressRecord` — shared-address pool; populated by `UniverseBuilder._generate_address_pool` in Step 4 and written out by Tier 5 in Step 15. Fields chosen as the minimum set that makes Tier 5 a pure transformation (no re-sampling):
    - `address_id: int` (BIGINT — referenced by `CustomerProfile.address_id` and by `PARTY_LOCATOR` in Tier 6)
    - `address_subtype_cd: str` (defaults `'PHYSICAL'`; maps to `ADDRESS_SUBTYPE` TITLE `'Locator Type Cd'` per `01_schema-reference.md`)
    - `street_line_1: str` (Faker-generated at universe-build time)
    - `street_line_2: Optional[str]`
    - `house_num: str` (Street_Address_Num NOT NULL per `01_schema-reference.md` STREET_ADDRESS_DETAIL)
    - `street_name: str`
    - `street_direction_type_cd: str` (→ `DIRECTION_TYPE`)
    - `street_suffix_cd: str` (→ `STREET_SUFFIX_TYPE`)
    - `city_id: int` (BIGINT — FK to Tier 1 `CITY`)
    - `county_id: Optional[int]` (BIGINT — FK to Tier 1 `COUNTY`; nullable because some PO-box / parcel addresses will not have one)
    - `territory_id: int` (BIGINT — FK to Tier 1 `TERRITORY`)
    - `postal_code_id: int` (BIGINT — FK to Tier 1 `POSTAL_CODE`)
    - `country_id: int` (BIGINT — FK to Tier 1 `COUNTRY`)
    - `latitude: float` (DECIMAL(18,4) in DDL; rendered by the writer in Step 5)
    - `longitude: float`
- `registry/context.py` — the `GenerationContext` dataclass passed through every tier per `mvp-tool-design.md` §6:
  - `customers: List[CustomerProfile]` (default_factory=list)
  - `agreements: List[AgreementProfile]` (default_factory=list)
  - `addresses: List[AddressRecord]` (default_factory=list)
  - `config: Any` (typed as `Any` or `ModuleType` — `config.settings` is a module, not a class; do not invent a `Config` dataclass just to satisfy a type hint)
  - `rng: np.random.Generator`
  - `ids: IdFactory` (imported from `utils.id_factory`)
  - `tables: Dict[str, pd.DataFrame]` (default_factory=dict; keys are `'Schema.TABLE'` strings — e.g. `'Core_DB.AGREEMENT'`, `'CDM_DB.PARTY_INTERRACTION_EVENT'`, `'PIM_DB.PRODUCT_GROUP'`)

## Tables generated (if applicable)

No tables generated in this step. Registry dataclasses only — the `GenerationContext.tables` dict starts empty and is populated by tier generators in Steps 8–23.

## Files to modify

No files modified. All seven produced files are new (`registry/` directory exists but is empty per the Step 1 scaffolding).

## New dependencies

No new dependencies. `numpy`, `pandas`, and `python-dateutil` are already pinned in `requirements.txt` from Step 1. `Decimal` and `date`/`datetime` come from the Python stdlib.

## Rules for implementation

- **BIGINT for all ID columns (per PRD §7.1)** — every `*_id` field on every dataclass is typed as `int`. Python `int` is arbitrary precision, so BIGINT semantics are preserved at the registry layer by construction. Do NOT use `numpy.int32`, `numpy.int64`, or any other narrower type; downstream serialization expects plain Python `int`.
- **Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2)** — `CustomerProfile.party_id` is a single field. Do NOT add a separate `cdm_party_id` field; the one value serves as both `Core_DB.Party_Id` and `CDM_DB.CDM_Party_Id`. This is why `IdFactory` has only one `'party'` category.
- **DI column stamping on every table via `BaseGenerator.stamp_di()`** — n/a at this step: registry dataclasses are in-memory objects, not DataFrames. DI stamping happens in tier generators (Step 8 onwards) when dataclass lists are projected into DataFrames.
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — n/a: no DataFrames produced.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` (per PRD §7.3)** — n/a: no DataFrames produced.
- **Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md`** — n/a: no DataFrames produced. Dataclass field order is a dev-ergonomics concern, not a DDL-order concern.
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10)** — n/a at this step (no table keys written). `config.settings.PARTY_INTERRACTION_EVENT_TABLE_NAME` is the single source of truth and will be read by Step 22.
- **Skip the `GEOSPATIAL` table entirely (per PRD §7.9)** — n/a: no CSV writing in this step.
- **No ORMs, no database connections — pure pandas → CSV.** Registry types use plain Python stdlib (`dataclasses`, `datetime`, `decimal`, `typing`) plus `numpy.random.Generator` and `pandas.DataFrame` type annotations. No SQLAlchemy, no pyodbc, no teradatasql.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — this step does NOT call `rng` at all (no sampling happens here). `rng` is merely stored on `GenerationContext` so downstream tiers can draw from the same sequence. Do NOT instantiate a default `rng` in the dataclass default factory — Step 4's orchestrator passes it in explicitly.

### Step-specific rules

- **Pure containers, no logic.** These dataclasses must not have custom `__init__`, no business-logic methods, no validators. No `@property` that does computation. No `__post_init__` that calls samplers. The only acceptable `__post_init__` would be a trivial type coercion, and even that is discouraged — prefer leaving the types exactly as specified and trust Step 4 to populate them correctly.
- **Use `@dataclass` (mutable), not `@dataclass(frozen=True)`.** Step 4 mutates fields across its `_assign_*` phases (e.g. creates the `CustomerProfile` with identity fields filled, then `_assign_demographics` mutates demographic fields, then `_assign_products` mutates `product_set`). Freezing would force wholesale object replacement.
- **Use `field(default_factory=list)` / `field(default_factory=dict)` for all mutable defaults.** Never use `= []` or `= {}` as a default — the shared-mutable-default bug is the single most common Python dataclass footgun.
- **Optional fields use `Optional[T]` from `typing`, not `T | None`.** Python 3.9 compatibility; also matches the mvp-tool-design.md §4 style so future readers can cross-reference the spec and the code side-by-side without mental translation.
- **Do NOT import `faker`, `scipy`, `config.distributions`, or anything from `seed_data/` / `generators/`.** These are Step 4+ dependencies; the registry layer is strictly upstream of statistical sampling and of every tier generator. Allowed imports: `dataclasses`, `datetime`, `decimal`, `typing`, `numpy` (for `np.random.Generator` type hint), `pandas` (for `pd.DataFrame` type hint on `GenerationContext.tables`), `utils.id_factory` (for `IdFactory` type hint), `config.settings` (ONLY if a literal from settings is needed — not required per the field list above).
- **No cross-module side effects at import time.** Importing `registry.profiles` or `registry.context` must not trigger any I/O, any `print`, any filesystem touch, or any module-level computation beyond the dataclass decorator expanding.
- **Every `*.py` in `registry/` includes an `if __name__ == '__main__':` self-test block** that instantiates each dataclass with dummy values and prints `registry/<file> OK`. Mirrors the self-test convention from Step 2's `utils/` files. The test block is NOT an exhaustive validator — it confirms the dataclasses instantiate cleanly, the types are accepted by the dataclass runtime, and defaults work.
- **`GenerationContext` must be constructable with only `rng` and `ids` supplied** — every other field has a `default_factory` or acceptable None. This makes Step 4's orchestrator cleanly builds an empty context, then populates `customers`/`agreements`/`addresses`/`tables` across its phases.

## Definition of done

Each item is a checkbox. Tick every box or mark it `n/a` with a one-line justification before the session ends.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

- [ ] **Dataclasses instantiate with dummy values; all fields typed correctly.** Verify `CustomerProfile`:
  ```bash
  python -c "
  from datetime import date
  from decimal import Decimal
  from registry.profiles import CustomerProfile
  cp = CustomerProfile(
      party_id=10_000_000, party_type='INDIVIDUAL',
      age=42, income_quartile=3, lifecycle_cohort='ACTIVE', clv_segment=7,
      gender_type_cd='MALE', marital_status_cd='MARRIED',
      ethnicity_type_cd='WHITE', occupation_cd='EMP',
      num_dependents=2, fico_score=720,
      household_id=8_000_000, household_role='HEAD', lifecl=3,
      has_internet=True, preferred_channel_cd=3,
      product_set=['CHECKING', 'SAVINGS'],
      party_since=date(2018, 6, 15),
      address_id=1_000_000,
      org_name=None, naics_sector_cd=None, sic_cd=None, gics_sector_cd=None,
  )
  assert cp.party_id == 10_000_000 and isinstance(cp.party_id, int)
  assert cp.product_set == ['CHECKING', 'SAVINGS']
  print('CustomerProfile OK')
  "
  ```
  Must print `CustomerProfile OK`.

- [ ] **`AgreementProfile` instantiates with dummy values including all 8 sub-type flags:**
  ```bash
  python -c "
  from datetime import datetime
  from decimal import Decimal
  from registry.profiles import AgreementProfile
  ap = AgreementProfile(
      agreement_id=100_000, owner_party_id=10_000_000,
      product_type='MORTGAGE', agreement_subtype_cd='MORTGAGE',
      product_id=1_000,
      open_dttm=datetime(2020, 4, 1, 9, 30),
      close_dttm=None,
      balance_amt=Decimal('250000.0000'),
      interest_rate=Decimal('0.035000000000'),
      original_loan_amt=Decimal('300000.0000'),
      is_delinquent=False, is_severely_delinquent=False, is_frozen=False,
      monthly_balances=[],
      is_financial=True, is_deposit=False, is_term_deposit=False,
      is_credit=True, is_loan_term=True, is_mortgage=True,
      is_credit_card=False, is_loan_transaction=False,
  )
  # Exclusive sub-typing at the terminal leaf: exactly one of the 4 terminal flags is True
  terminal_leaves = [ap.is_term_deposit, ap.is_mortgage, ap.is_credit_card, ap.is_loan_transaction]
  assert sum(terminal_leaves) == 1, 'Exactly one terminal sub-type must be True'
  print('AgreementProfile OK')
  "
  ```
  Must print `AgreementProfile OK`.

- [ ] **`AddressRecord` instantiates with dummy values and all FK fields are Python `int`:**
  ```bash
  python -c "
  from registry.profiles import AddressRecord
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
  print('AddressRecord OK')
  "
  ```
  Must print `AddressRecord OK`.

- [ ] **`GenerationContext.tables` defaults to an empty dict and accepts `'Schema.TABLE'` keys.** Verify:
  ```bash
  python -c "
  import numpy as np
  import pandas as pd
  from registry.context import GenerationContext
  from utils.id_factory import IdFactory
  from config.settings import ID_RANGES
  ctx = GenerationContext(rng=np.random.default_rng(42), ids=IdFactory(ID_RANGES))
  assert ctx.tables == {}, 'tables default must be empty dict'
  assert ctx.customers == [] and ctx.agreements == [] and ctx.addresses == []
  ctx.tables['Core_DB.AGREEMENT'] = pd.DataFrame({'Agreement_Id': [100_000]})
  ctx.tables['CDM_DB.PARTY_INTERRACTION_EVENT'] = pd.DataFrame({'Event_Id': [50_000_000]})
  assert set(ctx.tables.keys()) == {'Core_DB.AGREEMENT', 'CDM_DB.PARTY_INTERRACTION_EVENT'}
  print('GenerationContext OK')
  "
  ```
  Must print `GenerationContext OK`.

- [ ] **No logic beyond data containers — statistical decisions live in Step 4.** Verify no sampling or state mutation is triggered by construction:
  ```bash
  python -c "
  import ast, pathlib
  for p in ('registry/profiles.py', 'registry/context.py'):
      tree = ast.parse(pathlib.Path(p).read_text())
      for node in ast.walk(tree):
          if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
              # Allow __post_init__, __repr__, __eq__ etc. but flag anything else
              if not (node.name.startswith('__') and node.name.endswith('__')):
                  raise AssertionError(f'{p}: custom method {node.name!r} violates pure-container rule')
      # No module-level calls (besides imports and dataclass decoration)
      for node in tree.body:
          if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
              raise AssertionError(f'{p}: module-level call violates no-side-effect rule')
  print('pure-container OK')
  "
  ```
  Must print `pure-container OK`.

- [ ] **Module self-tests pass as `__main__`:**
  ```bash
  python registry/profiles.py && python registry/context.py
  ```
  Both must exit 0 and print `registry/<file> OK`.

- [ ] **Every mutable default uses `field(default_factory=...)` — no bare `= []` or `= {}`.** Static check:
  ```bash
  python -c "
  import pathlib, re
  for p in ('registry/profiles.py', 'registry/context.py'):
      text = pathlib.Path(p).read_text()
      # Look for ': List[...] = []' or ': Dict[...] = {}' patterns
      for pattern, label in [(r':\s*List\[[^\]]+\]\s*=\s*\[\s*\]', 'bare []'),
                             (r':\s*Dict\[[^\]]+\]\s*=\s*\{\s*\}', 'bare {}')]:
          if re.search(pattern, text):
              raise AssertionError(f'{p}: {label} default found — must use field(default_factory=...)')
  print('defaults OK')
  "
  ```
  Must print `defaults OK`.

### Universal checks

- [ ] **`git status` shows only files listed under `## Produces` — nothing else.** Run:
  ```bash
  git status --porcelain
  ```
  Every line must map to one of: `registry/__init__.py`, `registry/profiles.py`, `registry/context.py`. No stray files, no edits outside `registry/`.

- [ ] **All new files pass `python -c "import <module>"`:**
  ```bash
  python -c "import registry.profiles, registry.context"
  ```
  Must exit 0 with no output.

- [ ] **No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1)** — n/a: this step produces no CSVs. BIGINT semantics are enforced at the registry layer by typing every `*_id` as Python `int`; the first test of CSV-level BIGINT rendering happens in Step 5 (writer).

- [ ] **If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo** — n/a: this step writes no CSVs. The constant `config.settings.PARTY_INTERRACTION_EVENT_TABLE_NAME` remains the single source of truth.

- [ ] **If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv`** — n/a: this step writes no CSVs.

- [ ] **`registry/__init__.py` exists so Step 4 can `from registry.profiles import CustomerProfile`:**
  ```bash
  [ -f registry/__init__.py ] && echo OK || echo MISSING
  ```
  Must print `OK`.

- [ ] **`GenerationContext` type hints resolve without forward-reference errors at runtime:**
  ```bash
  python -c "
  from typing import get_type_hints
  from registry.context import GenerationContext
  hints = get_type_hints(GenerationContext)
  for required_field in ('customers', 'agreements', 'addresses', 'rng', 'ids', 'tables', 'config'):
      assert required_field in hints, f'missing field: {required_field}'
  print('type hints OK:', sorted(hints.keys()))
  "
  ```
  Must print a line starting with `type hints OK:` listing all 7 fields.

## Handoff notes

### What shipped
- `registry/__init__.py` — empty package marker
- `registry/profiles.py` — `CustomerProfile`, `AgreementProfile`, `AddressRecord` dataclasses; all fields match spec exactly; `@dataclass` (mutable); all `*_id` fields typed as Python `int`; mutable defaults use `field(default_factory=...)`; `Optional[T]` syntax throughout; `if __name__ == '__main__':` self-test passes
- `registry/context.py` — `GenerationContext` dataclass; `rng` and `ids` are required (no defaults), all other fields defaulted; constructable with `GenerationContext(rng=..., ids=...)` only; `if __name__ == '__main__':` self-test passes

### Field-ordering note (non-obvious)
`CustomerProfile` places `party_since: date` and `address_id: int` immediately **before** `product_set` (the first field with a `default_factory`). This deviates from the spec's logical grouping order (dates → address → products) but is required by Python's dataclass rule: non-default fields must precede default fields. The spec explicitly permits reordering: "Dataclass field order is a dev-ergonomics concern, not a DDL-order concern."

### Import pattern for `context.py` (non-obvious)
`registry/context.py` guards its project-level imports (`from utils.id_factory import IdFactory`, `from registry.profiles import ...`) inside a `try/except ImportError: pass` block. This matches the `id_factory.py` convention from Step 2 — project imports are not available when running `python registry/context.py` directly (project root is not on sys.path). The `__main__` block adds the root via `sys.path.insert` first, mirroring `utils/id_factory.py`. When imported normally (project root in sys.path), the try/except succeeds and names are in module globals so `get_type_hints()` resolves all 7 fields correctly.

### No spec conflicts found
All field names, types, and nullability match `mvp-tool-design.md` §4 and §6 exactly.

### Next session hint
Step 4 (UniverseBuilder) can start now — `registry/` is stable. Step 4 reads `registry/profiles.py` and `registry/context.py` directly and must populate every non-Optional field of `CustomerProfile` before `build()` returns.

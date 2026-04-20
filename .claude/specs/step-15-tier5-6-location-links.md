# Spec: Step 15 — Tier 5 + Tier 6 — Location & Links

## Overview

This step builds **Tier 5 (Location)** and **Tier 6 (Links)**, the bridge between the Tier 1 geography backbone (countries, territories, cities, postal codes — already present in `ctx.tables` from Step 9) and every party in the universe. It produces the seven Core_DB address/locator tables (`ADDRESS`, `STREET_ADDRESS`, `STREET_ADDRESS_DETAIL`, `PARCEL_ADDRESS`, `POST_OFFICE_BOX_ADDRESS`, `GEOSPATIAL_POINT`, `LOCATOR_RELATED`) plus the single Tier 6 link table (`PARTY_LOCATOR`) — eight tables total. The `mvp-tool-design.md` §9 Tier 5 phrasing "POSTAL_CODE (additional rows)" is interpreted as "Tier 1 POSTAL_CODE pool is sufficient; no deltas authored here" (see ## Rules below). See `mvp-tool-design.md` §9 Tier 5 and Tier 6 for the authoritative scope. Per `PRD.md` §7.9, the `Core_DB.GEOSPATIAL` table is **entirely skipped** in this step because its `ST_Geometry` column has no CSV representation — only `GEOSPATIAL_POINT` (lat/lon as DECIMAL) is produced. The core design commitment is a small, realistic **~500-address pool shared across ~3,000 parties** (mirroring the real-world pattern where household members and some organizations share a physical address), with one current `PARTY_LOCATOR` row per party flagged `Locator_Usage_Type_Cd='physical_primary'`. The pre-existing `AddressRecord` pool in `ctx.addresses` provides address identities (`address_id`, `street_line_1`, `house_num`, `street_name`, `street_direction_type_cd`, `street_suffix_cd`, `latitude`, `longitude`) — but its placeholder geography FKs (`city_id`, `county_id`, `territory_id`, `postal_code_id`, `country_id`) were minted in `UniverseBuilder._generate_address_pool` before Tier 1 Geography ran and therefore **do not resolve to real Tier 1 rows**; Tier 5 must re-derive those FKs from `ctx.tables['Core_DB.CITY' | 'COUNTY' | 'TERRITORY' | 'POSTAL_CODE' | 'COUNTRY']` with coherent chain semantics (a postal code's country matches its city's territory's country). See ⚠️ Conflict block below and ## Rules for implementation for the exact re-wiring contract.

## Depends on

- **Step 1** — consumes from `config/settings.py`:
  - `HIGH_TS`, `HIGH_DATE`, `HISTORY_START`, `SIM_DATE` (used for DI stamping defaults and `Party_Locator_Start_Dttm` values).
  - `SKIPPED_TABLES` — must contain `'Core_DB.GEOSPATIAL'`; this step does not emit that key.
  - `ID_RANGES` — adds **three new category entries** (`street_address`, `parcel_address`, `post_office_box`) for sub-type tables that do not reuse `Address_Id`. See ## Files to modify.
- **Step 2** — consumes `generators/base.BaseGenerator` (`stamp_di()`) and `utils/id_factory.IdFactory` (`next(category)` / `next_many(category, n)`). Also consumes `utils/date_utils.format_ts` if a non-default `start_ts` is needed (the implementation may instead reuse a fixed module-level `_GEO_DI_START_TS` like Tier 1 does).
- **Step 3** — consumes `registry/context.GenerationContext` (fields `customers`, `addresses`, `ids`, `rng`, `tables`) and `registry/profiles.AddressRecord` (fields `address_id`, `address_subtype_cd`, `street_line_1`, `street_line_2`, `house_num`, `street_name`, `street_direction_type_cd`, `street_suffix_cd`, `latitude`, `longitude`; geography FK fields `city_id`/`county_id`/`territory_id`/`postal_code_id`/`country_id` are **ignored** — see ⚠️ Conflict below).
- **Step 4** — consumes `ctx.addresses` (List[AddressRecord], 500 entries, all `address_subtype_cd='PHYSICAL'`) and `ctx.customers` (each has `cp.address_id` pointing at one entry from `ctx.addresses`).
- **Step 8** — consumes these Tier 0 seed tables (must all be present in `ctx.tables` at Step 15 entry):
  - `Core_DB.ADDRESS_SUBTYPE` — defines legal codes for `ADDRESS.Address_Subtype_Cd` (`PHYSICAL`, `MAILING`, `BILLING`, `WORK`, `VACATION`, `PO_BOX`).
  - `Core_DB.DIRECTION_TYPE` — 8 points; `STREET_ADDRESS_DETAIL.Street_Direction_Type_Cd` FKs here.
  - `Core_DB.STREET_SUFFIX_TYPE` — 15 USPS codes; `STREET_ADDRESS_DETAIL.Street_Suffix_Cd` FKs here.
  - `Core_DB.UNIT_OF_MEASURE` (if present) — `GEOSPATIAL_POINT.Elevation_UOM_Cd` FKs here when populated; `None` acceptable.
- **Step 9** — consumes the Tier 1 geography pool (`ctx.tables['Core_DB.CITY']`, `COUNTY`, `TERRITORY`, `POSTAL_CODE`, `COUNTRY`). This step treats those as read-only; it does not mutate any Tier 1 DataFrame.
- **Step 11** — consumes Tier 3 party sets: `ctx.tables['Core_DB.INDIVIDUAL']` and `ctx.tables['Core_DB.ORGANIZATION']`. `PARTY_LOCATOR` emits one row per party in the union of `Individual_Party_Id` and `Organization_Party_Id` (but **not** the reserved self-employment placeholder row `Organization_Party_Id = 9_999_999` — it has no real address).

No code from Step 10 (Tier 2 Core), Step 12 / 13 / 14 (Tier 4 attrs), or Step 5 (Writer) is imported by this step. The writer is not invoked — generator returns DataFrames only, orchestrator (Step 25) handles `ctx.tables.update()` and later CSV emission.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 15):
- `PRD.md` §4.2 "Address & Location" (authoritative table enumeration), §7.1 (BIGINT rule for all `*_Id`), §7.3 (DI column rules; active-record sentinels), §7.9 (GEOSPATIAL skip — **directly enforced in this step**)
- `mvp-tool-design.md` §7 (`BaseGenerator` + DI rules), §8 (ID Factory — must add the 3 new sub-type categories without reordering prior entries), §9 Tier 5 Location and Tier 6 Links (authoritative scope and per-table rules), §14 Decision 8 (GEOSPATIAL rationale), §15 (orchestrator signature — `Tier5Location()` and `Tier6Links()` follow `Tier4*()` in the tiers list)
- `implementation-steps.md` Step 15 entry (exit criteria); Handoff Protocol

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the nine in-scope tables and the skipped one. Open only these blocks (the implementation session may open the summary tables at §§2130–2200 first, then cross-check against the SQL DDL blocks below which are authoritative where the two differ):
  - `ADDRESS` (DDL §4228): `Address_Id INTEGER NOT NULL` (PK), `Address_Subtype_Cd VARCHAR(50) NULL`, + 3 DI. Five business+DI columns total.
  - `STREET_ADDRESS` (DDL §7384): `Street_Address_Id INTEGER NOT NULL` (PK; **= the parent `Address_Id`** per locator-inheritance convention), `Address_Line_1_Txt`/`_2_Txt`/`_3_Txt` VARCHAR(1000) NULL, `Dwelling_Type_Cd` NULL, `Census_Block_Id INTEGER NULL`, `City_Id`/`County_Id`/`Territory_Id`/`Postal_Code_Id`/`Country_Id` INTEGER NULL, `Carrier_Route_Txt` NULL, + 3 DI.
  - `STREET_ADDRESS_DETAIL` (DDL §7427): `Street_Address_Id INTEGER NOT NULL` (PK; = `Address_Id`). **Note ⚠️ Conflict — summary table (§2148) lists 14 business + 3 DI = 17 columns; SQL DDL (§7430) adds two `TIME NOT NULL` columns `Mail_Pickup_Tm` and `Mail_Delivery_Tm` for 16 business + 3 DI = 19 columns. Per CLAUDE.md "DDL wins" and PRD §10, the session uses the SQL DDL column set.** NOT NULL business fields: `Street_Address_Num` (= `house_num`), `Street_Direction_Type_Cd`, `Street_Name`, `Street_Suffix_Cd`, `Mail_Pickup_Tm`, `Mail_Delivery_Tm`, `Mail_Stop_Num`, `Mail_Box_Num`. Use representative constants for mail-ops fields (`'09:00:00'`, `'15:00:00'`, `'000'`, `'N/A'`) to satisfy NOT NULL without fabricating per-address variance.
  - `PARCEL_ADDRESS` (DDL §7788): `Parcel_Address_Id INTEGER NOT NULL` (PK — **independent ID; not tied to the customer address pool**), `Page_Num`, `Map_Num`, `Parcel_Num` VARCHAR(50) NULL, `City_Id`/`County_Id`/`Country_Id`/`Postal_Code_Id`/`Territory_Id` INTEGER NULL, + 3 DI.
  - `POST_OFFICE_BOX_ADDRESS` (DDL §7825): `Post_Office_Box_Id INTEGER NOT NULL` (PK — **independent ID; not tied to the customer address pool**), `Post_Office_Box_Num` VARCHAR(50) NULL, `City_Id`/`County_Id`/`Country_Id`/`Postal_Code_Id`/`Territory_Id` INTEGER NULL, + 3 DI.
  - `POSTAL_CODE` (summary §2202, DDL section in 07) — **no additional rows authored in this step**. The Tier 1 pool is sufficient; Step 15 references existing `Postal_Code_Id` values. (The `mvp-tool-design.md` §9 Tier 5 phrasing "POSTAL_CODE (additional rows)" is interpreted here as "does not preclude additions but none are required"; if a particular address needs a postal code not already in Tier 1, prefer sampling from Tier 1 rather than adding new rows.)
  - `GEOSPATIAL_POINT` (DDL §7931): `Geospatial_Point_Id INTEGER NOT NULL` (PK), `Latitude_Meas`/`Longitude_Meas`/`Elevation_Meas` DECIMAL(18,4) NULL, `Elevation_UOM_Cd` VARCHAR(50) NULL, + 3 DI.
  - `GEOSPATIAL` (DDL §7960): **DO NOT GENERATE** — `ST_Geometry` column has no CSV representation (PRD §7.9). `'Core_DB.GEOSPATIAL'` key must NOT appear in the returned dict.
  - `LOCATOR_RELATED` (DDL §8010): `Locator_Id`/`Related_Locator_Id` INTEGER NOT NULL (composite PK chain — both = ADDRESS.Address_Id from the pool), `Locator_Related_Reason_Cd` VARCHAR(50) NOT NULL, `Locator_Related_Start_Dt` DATE NOT NULL, `Locator_Related_End_Dt` DATE NULL, + 3 DI.
  - `PARTY_LOCATOR` (DDL §8214): `Party_Id INTEGER NOT NULL` (= CustomerProfile.party_id), `Locator_Id INTEGER NOT NULL` (= ADDRESS.Address_Id), `Locator_Usage_Type_Cd VARCHAR(50) NOT NULL`, `Party_Locator_Start_Dttm DATE NOT NULL` (column name says "Dttm" but DDL type is DATE — store as date string), `Party_Locator_End_Dttm DATE NULL`, `Data_Quality_Cd VARCHAR(50) NOT NULL`, + 3 DI.
  - Footnote §3125 (`LOCATOR_RELATED.Related_Locator_Id` INTEGER FK candidate → BIGINT) and §3126 (`PARTY_LOCATOR.Locator_Id` INTEGER FK candidate → BIGINT) — **both reiterate the universal BIGINT rule for non-PK `_Id` columns**; every `*_Id` in this step's output is emitted as `Int64`.
- `PRD.md` §7.9 (GEOSPATIAL skip justification) — cited inside the generator as a module-level docstring reference.

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is MVP-authoritative per PRD §10; only open `01` if `07` is ambiguous for a specific column.
- `references/05_architect-qa.md` — no Q touches Tier 5 or Tier 6. (Q6 `CDM_DB.ADDRESS` surrogate key is Step 22, not this step.)
- `references/06_supporting-enrichments.md` — no distribution relevant to pure address/locator wiring.
- `references/02_data-mapping-reference.md` — no literal-match constraint on Tier 5/6 tables. (Layer 2 uses `Locator_Usage_Type_Cd='physical_primary'` as a filter; this is enforced by the implementation and validated in ## Definition of done.)
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `iDM_MDM_tables_DDLs.xlsx` — already distilled into `07`.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier5_location.py` — `class Tier5Location(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]`. Implementation contract:
  1. Import `BaseGenerator`; import `GenerationContext` under `TYPE_CHECKING` only. Import `pd`, `numpy as np`; `from config.settings import SKIPPED_TABLES`; `from registry.profiles import AddressRecord`.
  2. Guard: verify `ctx.addresses` is non-empty and all Tier 1 + Tier 0 prerequisite tables are in `ctx.tables` (list: `Core_DB.CITY`, `Core_DB.COUNTY`, `Core_DB.TERRITORY`, `Core_DB.POSTAL_CODE`, `Core_DB.COUNTRY`, `Core_DB.ADDRESS_SUBTYPE`, `Core_DB.DIRECTION_TYPE`, `Core_DB.STREET_SUFFIX_TYPE`). Raise `RuntimeError(f'Tier5Location requires {key} in ctx.tables')` if any missing.
  3. **Re-derive FK chain per AddressRecord** (see ## Rules for implementation for the exact chain algorithm). Build an `address_fks: Dict[int, Dict[str, int]]` keyed by `address_id`, storing `{city_id, county_id, territory_id, postal_code_id, country_id}` drawn deterministically from `ctx.rng` with coherent chain semantics. **Do not read `ar.city_id` etc. — those placeholder values from Step 4 are ignored.**
  4. Build `ADDRESS` DataFrame — one row per AddressRecord. `Address_Id = ar.address_id`; `Address_Subtype_Cd = ar.address_subtype_cd` (='PHYSICAL' for every row under current universe state).
  5. Build `STREET_ADDRESS` DataFrame — one row per AddressRecord. `Street_Address_Id = ar.address_id` (inheritance from ADDRESS). `Address_Line_1_Txt = ar.street_line_1`; `Address_Line_2_Txt = ar.street_line_2`; `Address_Line_3_Txt = None`. `Dwelling_Type_Cd = None`. `Census_Block_Id = None`. FK fields from `address_fks[ar.address_id]`. `Carrier_Route_Txt = None`.
  6. Build `STREET_ADDRESS_DETAIL` DataFrame — one row per AddressRecord. `Street_Address_Id = ar.address_id`. NOT-NULL fields: `Street_Address_Num = ar.house_num`, `Street_Direction_Type_Cd = ar.street_direction_type_cd`, `Street_Name = ar.street_name`, `Street_Suffix_Cd = ar.street_suffix_cd`, `Mail_Pickup_Tm = '09:00:00'`, `Mail_Delivery_Tm = '15:00:00'`, `Mail_Stop_Num = 'N/A'`, `Mail_Box_Num = 'N/A'`. Nullable fields: `Street_Address_Number_Modifier_Val`, `Street_Num`, `Building_Num`, `Unit_Num`, `Floor_Val`, `Workspace_Num`, `Route_Num` → all `None`.
  7. Build `PARCEL_ADDRESS` DataFrame — small reference set of **exactly 15 rows** (commercial-use scenarios). `Parcel_Address_Id` = `ctx.ids.next('parcel_address')` — **IDs are distinct from the AddressRecord pool**. FK chain sampled from Tier 1 (any US state with a valid city/county). `Page_Num`/`Map_Num`/`Parcel_Num` use deterministic patterns (`'P{idx:03d}'`, `'M{idx:03d}'`, `'APN-{idx:06d}'`). Does not FK to ADDRESS.
  8. Build `POST_OFFICE_BOX_ADDRESS` DataFrame — **exactly 15 rows**. `Post_Office_Box_Id` = `ctx.ids.next('post_office_box')` — also distinct from AddressRecord pool. `Post_Office_Box_Num` deterministic `'PO Box {1000+idx}'`. FK chain sampled from Tier 1.
  9. Build `GEOSPATIAL_POINT` DataFrame — one row per AddressRecord. `Geospatial_Point_Id = ar.address_id` (reuse parent ID — conventional 1:1 link). `Latitude_Meas = Decimal(str(ar.latitude)).quantize(0.0001)` and `Longitude_Meas = Decimal(str(ar.longitude)).quantize(0.0001)` as `DECIMAL(18,4)`. `Elevation_Meas = None`; `Elevation_UOM_Cd = None`.
  10. Build `LOCATOR_RELATED` DataFrame — **exactly 20 rows** sampled deterministically from `ctx.addresses`. Each row pairs two distinct address IDs with `Locator_Related_Reason_Cd = 'mailing_for_physical'` and `Locator_Related_Start_Dt = HISTORY_START`. Both IDs must exist in the ADDRESS pool.
  11. Do **not** emit `Core_DB.GEOSPATIAL` or `Core_DB.POSTAL_CODE` (the latter lives in Tier 1).
  12. Stamp all **seven** DataFrames via `self.stamp_di()`. Do NOT call `stamp_valid()` (all Core_DB).
  13. Return `{'Core_DB.ADDRESS': df_address, 'Core_DB.STREET_ADDRESS': df_street, 'Core_DB.STREET_ADDRESS_DETAIL': df_detail, 'Core_DB.PARCEL_ADDRESS': df_parcel, 'Core_DB.POST_OFFICE_BOX_ADDRESS': df_pobox, 'Core_DB.GEOSPATIAL_POINT': df_geo, 'Core_DB.LOCATOR_RELATED': df_loc_rel}`. **Seven tables total** from Tier 5; the eighth in-scope Tier-5/6 table (`Core_DB.PARTY_LOCATOR`) is produced by `Tier6Links` below.

- `generators/tier6_links.py` — `class Tier6Links(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]`. Implementation contract:
  1. Guard: verify `ctx.tables['Core_DB.ADDRESS']` is present (Tier 5 must have run) and `ctx.customers` is non-empty. Raise `RuntimeError` otherwise.
  2. Build a set `valid_address_ids = set(ctx.tables['Core_DB.ADDRESS'].Address_Id)` for O(1) FK validation.
  3. For **every** `CustomerProfile` in `ctx.customers`, emit one `PARTY_LOCATOR` row:
     - `Party_Id = cp.party_id`
     - `Locator_Id = cp.address_id` — must be in `valid_address_ids`; raise `ValueError` if any customer's assigned address is missing from the pool.
     - `Locator_Usage_Type_Cd = 'physical_primary'` (exact string — constant at module top; Layer 2 filters on this)
     - `Party_Locator_Start_Dttm = cp.party_since` (DATE)
     - `Party_Locator_End_Dttm = None` (open-ended current record)
     - `Data_Quality_Cd = 'verified'`
  4. The reserved self-employment placeholder ORGANIZATION row (`Organization_Party_Id = 9_999_999`, created in Step 11) has no real address and has no `CustomerProfile` entry — therefore receives **no `PARTY_LOCATOR` row**. This is correct: the placeholder is a Step 3/4 FK target only.
  5. Build one `pd.DataFrame`; column order matches DDL (Party_Id, Locator_Id, Locator_Usage_Type_Cd, Party_Locator_Start_Dttm, Party_Locator_End_Dttm, Data_Quality_Cd + DI tail).
  6. Stamp via `self.stamp_di()`. Return `{'Core_DB.PARTY_LOCATOR': df}`.

**Do NOT produce** in this step:
- CSVs — writer is not invoked.
- Wiring into `main.py` — orchestrator changes are Step 25.
- `Core_DB.GEOSPATIAL` — explicitly skipped (PRD §7.9, design §14 Decision 8).
- `Core_DB.POSTAL_CODE` additional rows — Tier 1 pool is sufficient; if implementation discovers a gap, escalate per Handoff Protocol §2 and extend Tier 1 rather than Tier 5.
- CDM_DB variants of address tables — those are Step 22 (Tier 14 CDM_DB).

## Tables generated (if applicable)

After `Tier5Location().generate(ctx)` and `Tier6Links().generate(ctx)` run, `ctx.tables` gains these nine Core_DB keys:

| Table | Exact rows | Source | Constraints enforced |
|-------|-----------:|--------|----------------------|
| `Core_DB.ADDRESS` | `len(ctx.addresses)` (500) | One per AddressRecord | `Address_Subtype_Cd = 'PHYSICAL'` (sourced from AddressRecord) |
| `Core_DB.STREET_ADDRESS` | `len(ctx.addresses)` (500) | One per AddressRecord | FK chain `City_Id → POSTAL_CODE.Country_Id` coherent with `Country_Id`; all FKs resolve to Tier 1 |
| `Core_DB.STREET_ADDRESS_DETAIL` | `len(ctx.addresses)` (500) | One per AddressRecord | All 8 NOT-NULL columns populated; `Mail_Pickup_Tm`/`Mail_Delivery_Tm` use fixed constants |
| `Core_DB.PARCEL_ADDRESS` | 15 | Minted in-generator | Independent `Parcel_Address_Id` sequence; FK chain coherent |
| `Core_DB.POST_OFFICE_BOX_ADDRESS` | 15 | Minted in-generator | Independent `Post_Office_Box_Id` sequence; `Post_Office_Box_Num` populated |
| `Core_DB.GEOSPATIAL_POINT` | `len(ctx.addresses)` (500) | One per AddressRecord | `Geospatial_Point_Id = Address_Id`; lat/lon DECIMAL(18,4) |
| `Core_DB.LOCATOR_RELATED` | 20 | Sampled from AddressRecord pool | Both IDs resolve to ADDRESS; `Locator_Id != Related_Locator_Id` per row |
| `Core_DB.PARTY_LOCATOR` | `len(ctx.customers)` (3,000) | One per CustomerProfile | Every `Locator_Id` resolves to ADDRESS; every row has `Locator_Usage_Type_Cd = 'physical_primary'` |
| `Core_DB.GEOSPATIAL` | **n/a — skipped** | PRD §7.9 | Must not appear in the returned dict |

All eight emitted DataFrames (seven from `Tier5Location` + one from `Tier6Links`) have the 5-column DI tail after `stamp_di()`, with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. No `stamp_valid()` is called.

## ⚠️ Conflict — AddressRecord placeholder FKs

`UniverseBuilder._generate_address_pool` (registry/universe.py:609) mints placeholder geography FKs using small-range random integers (`city_ids = rng.integers(1, 101)`, `territory_ids = rng.integers(1, 51)`, `postal_ids = rng.integers(1, 201)`, `county_ids = rng.integers(1, 51)`, `country_id=1`). These values DO NOT match the BIGINT offsets minted later by `Tier1Geography.generate()` (country=700+, region=800+, territory=900+, county=1_100+, city=1_400+, postal_code=1_600+). As a result, `AddressRecord.city_id` / `.county_id` / `.territory_id` / `.postal_code_id` / `.country_id` are **NOT valid FKs into Tier 1**.

**Resolution chosen for this step:** Tier 5 ignores those placeholder fields entirely and re-derives a coherent FK chain for each AddressRecord at generation time by sampling from `ctx.tables['Core_DB.CITY']` and walking the chain. This is transparent (no mutation of `AddressRecord`) and deterministic (uses `ctx.rng`).

**Downstream implication:** No other tier reads `AddressRecord` geography FK fields — verified: grep `AddressRecord\.(city|county|territory|postal|country)_id` across `generators/` returns no matches as of this spec. If a future step adds such a read, that step must also re-derive the FK rather than trusting the placeholder.

**Upstream follow-up (optional, not in this step's scope):** A future cleanup PR could either (a) delete the unused FK fields from `AddressRecord`, or (b) reorder the universe build so `UniverseBuilder._generate_address_pool` runs after Tier 1 and populates real FKs. Neither is required for Step 15 to ship correctly.

## ⚠️ Conflict — STREET_ADDRESS_DETAIL column count

`references/07_mvp-schema-reference.md` §2148 summary table lists 14 business + 3 DI = 17 columns. The SQL DDL block §7430 adds `Mail_Pickup_Tm TIME NOT NULL` and `Mail_Delivery_Tm TIME NOT NULL` for 16 business + 3 DI = 19 columns. Per `CLAUDE.md` "DDL verification rule" and PRD §10 priority, **the SQL DDL wins**. The implementation emits 19 columns and fills both TIME columns with `'09:00:00'` and `'15:00:00'` respectively (representative values, not per-address randomised).

**Upstream follow-up:** The summary table at 07 §2148 should be corrected in a dedicated docs PR to match the SQL DDL. This step should append a one-line note to its Session Notes flagging that the upstream reference needs a sync. No change to `references/07_mvp-schema-reference.md` is required from this step.

## Files to modify

- `config/settings.py` — append **three new entries** to `ID_RANGES` below the existing Tier 1 block, keeping existing entries and values unchanged:
  ```python
  # Tier 5 — Location (Step 15)
  'street_address':      2_100_000,   # distinct from 'address' (1_000_000) reserved for PARCEL/PO_BOX sub-type IDs
  'parcel_address':      2_200_000,
  'post_office_box':     2_300_000,
  ```
  Rationale: `STREET_ADDRESS.Street_Address_Id` uses the parent `Address_Id` (1_000_000-range) per locator-inheritance convention and does NOT need a new range — so `'street_address'` is **reserved but unused in this step**. Including it now prevents collision if a future refactor ever mints standalone street-address IDs. `'parcel_address'` and `'post_office_box'` are actively used because those tables are independent of the customer address pool. All three starting offsets lie in the 2M+ band (above `locator`=2M, below `task`=3M) — the 2.1M / 2.2M / 2.3M spacing gives ~100K headroom each.

  **Do not reorder or change existing ID_RANGES entries.** Reordering breaks reproducibility of any entity already minted in dev environments.

- No other files modified. `config/code_values.py`, `config/distributions.py`, `utils/*`, `registry/*`, `output/*`, `main.py`, `CLAUDE.md`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/*`, all existing `seed_data/*.py`, all existing `generators/*.py` are **NOT touched**.

- `generators/__init__.py` is already empty — do NOT modify.

If implementation discovers that `references/07_mvp-schema-reference.md` disagrees with this spec on any column name, type, or nullability not already flagged above, escalate per Handoff Protocol §2 — update the upstream reference or add a new `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new dependencies. This step uses only `pandas`, `numpy`, `python-dateutil` (all in `requirements.txt` from Step 1) plus standard library + existing project modules.

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — every `*_Id` column in every output DataFrame is emitted as pandas `Int64Dtype()` (nullable BIGINT) or `int64` (when all non-null). The DDL in `07` declares `INTEGER` for these columns; footnotes §3125/§3126 flag them as INTEGER-FK candidates to migrate to BIGINT. The BIGINT rule wins on every `_Id`.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — `PARTY_LOCATOR.Party_Id` draws from `CustomerProfile.party_id` which is the single shared ID space.
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on all seven Tier 5 DataFrames and the one Tier 6 DataFrame (eight total).
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts = HIGH_TS` stamped via `stamp_di()` default. `Valid_To_Dt` **n/a**: Tier 5 and Tier 6 are all Core_DB; no `stamp_valid()`.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — **n/a**: Tier 5 and Tier 6 are all Core_DB. Do NOT call `stamp_valid()`.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** — every DataFrame is constructed via `pd.DataFrame(rows, columns=_COLS_<TABLE>)` where `_COLS_<TABLE>` is the authoritative business-column list (DI columns appended by `stamp_di()` at the end, matching the Tier 1 pattern).
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — **n/a**: not touched in this step.
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — **directly enforced**: `Core_DB.GEOSPATIAL` must not appear in the returned dict; `SKIPPED_TABLES` constant verified at module top.
- **No ORMs, no database connections — pure pandas → CSV** — writer not invoked; generators return DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — every stochastic choice (FK chain sampling, LOCATOR_RELATED pair selection, PARCEL/PO_BOX FK selection) must use `ctx.rng`. Two back-to-back runs produce byte-identical DataFrames.

Step-specific rules (Tier 5 + Tier 6):

- **FK chain algorithm.** For each AddressRecord (and for each PARCEL/PO_BOX row), pick a coherent `(country_id, territory_id, county_id, city_id, postal_code_id)` tuple as follows:
  1. Restrict to US cities: filter `ctx.tables['Core_DB.CITY']` rows where the resolved Territory Country is USA. (Either: inner-join to TERRITORY on `Territory_Id` and to COUNTRY on `Country_Id`, filter USA; or: use a precomputed set of US-state `Territory_Id`s from `ISO_3166_COUNTRY_SUBDIVISION_STANDARD.Territory_Id`.)
  2. Sample one city using `ctx.rng`. Capture its `City_Id` and `Territory_Id`.
  3. `country_id` = the country whose `Country_Id` matches `TERRITORY[territory_id].Country_Id` (will be USA).
  4. `county_id` = sample one `County_Id` from `COUNTY` rows where `County.Territory_Id == territory_id`; if no county exists for that state, set `county_id = None` (column is nullable in STREET_ADDRESS; not nullable in PARCEL/PO_BOX — for those, ensure the chosen state has at least one county, or pick a fallback).
  5. `postal_code_id` = sample one `Postal_Code_Id` from `POSTAL_CODE` rows where `POSTAL_CODE.Country_Id == country_id`. Prefer rows where `POSTAL_CODE.County_Id == county_id` if any exist (optional optimization; simple filter on country is sufficient).
  6. Cache `(city_id, territory_id, country_id, county_id)` into `address_fks[ar.address_id]` so the STREET_ADDRESS, STREET_ADDRESS_DETAIL (doesn't need FKs), PARCEL, and PO_BOX builders all see the same choice per address.

  A single deterministic `_resolve_fk_chain(rng, tier1_tables) -> Dict[str, int | None]` helper keeps the logic in one place. PARCEL and PO_BOX rows call the same helper with fresh draws (not reusing any AddressRecord's chain).

- **No random street/house/lat/lon generation.** `ar.street_line_1`, `ar.house_num`, `ar.street_name`, `ar.street_direction_type_cd`, `ar.street_suffix_cd`, `ar.latitude`, `ar.longitude` are taken verbatim from the AddressRecord — no new Faker call in this step. (Universe already seeded Faker with an rng-derived seed.)

- **AddressRecord fk fields ignored.** Do not read `ar.city_id`, `ar.county_id`, `ar.territory_id`, `ar.postal_code_id`, `ar.country_id`. They are placeholder values from Step 4 and will not resolve to real Tier 1 IDs (see ⚠️ Conflict above). A lint-style grep for those references inside `generators/tier5_location.py` must return zero matches.

- **PARTY_LOCATOR coverage.** Exactly one row per `CustomerProfile` in `ctx.customers`. No rows for the reserved placeholder `Organization_Party_Id = 9_999_999` (it has no CustomerProfile entry). The total row count equals `len(ctx.customers)` ≈ 3,000.

- **`Locator_Usage_Type_Cd = 'physical_primary'` exact string.** Declared as a module-level constant `_PRIMARY_LOCATOR_USAGE = 'physical_primary'` and used on every PARTY_LOCATOR row. Lowercase-with-underscore matches the convention used in other Tier 4+ tables (e.g. `PARTY_CONTACT_PREFERENCE`).

- **LOCATOR_RELATED inter-address relationships.** 20 rows (hard-coded row count is fine; no distribution needed for a reference table). Pair construction: sample 20 distinct pairs `(locator_id, related_locator_id)` from `ctx.addresses` using `ctx.rng.choice(..., size=2, replace=False)` per row; reject any pair where both ends are the same address. Use `Locator_Related_Reason_Cd = 'mailing_for_physical'` — descriptive, no FK to a seed table (DDL column is VARCHAR(50) free-form).

- **GEOSPATIAL_POINT Geospatial_Point_Id = Address_Id.** Reusing the parent ID is conventional for inheritance-style tables (same as STREET_ADDRESS.Street_Address_Id = Address_Id). No new `geospatial_point` ID_RANGES entry is required; the range reserved in prior specs is unused by this implementation.

- **No side effects on import.** `import generators.tier5_location` and `import generators.tier6_links` must not construct any DataFrames, call `generate()`, or read any file. Enforced by the "no import-time DataFrames" check in Definition of done.

- **Escalation over improvisation.** If `07` has an ambiguity beyond those flagged above (column name differs, nullability unclear), stop and add a new `⚠️ Conflict` block to this spec. Do NOT invent columns.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is CWD and `python` resolves to the project's Python 3.12 environment. Each check builds a full ctx (UniverseBuilder + Tier 0 + Tier 1 + Tier 3) before invoking Tier 5/6.

### Module-import and API contract

- [ ] `python -c "import generators.tier5_location, generators.tier6_links"` exits 0.
- [ ] Both generator classes inherit from `BaseGenerator` and define `generate(ctx)`. Run:
  ```bash
  python -c "
  from generators.tier5_location import Tier5Location
  from generators.tier6_links import Tier6Links
  from generators.base import BaseGenerator
  import inspect
  for cls in (Tier5Location, Tier6Links):
      assert issubclass(cls, BaseGenerator), cls
      sig = inspect.signature(cls.generate)
      assert 'ctx' in sig.parameters, cls
  print('class contract OK')
  "
  ```

### Tables produced

- [ ] `Tier5Location().generate(ctx)` returns **exactly these 7 Core_DB keys** — no more, no fewer, and **never** `Core_DB.GEOSPATIAL` (PRD §7.9 skip) or `Core_DB.POSTAL_CODE` (owned by Tier 1). Run the canonical ctx-bootstrap helper from the repo root (spelled out inline here; the session may DRY this into a temp helper):
  ```bash
  python -c "
  import numpy as np
  from config.settings import SEED, ID_RANGES
  from utils.id_factory import IdFactory
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  from generators.tier3_party_subtypes import Tier3PartySubtypes
  from generators.tier5_location import Tier5Location
  import config.settings as _s
  ctx = UniverseBuilder().build(_s, np.random.default_rng(SEED))
  for t in (Tier0Lookups(), Tier1Geography(), Tier2Core(), Tier3PartySubtypes()):
      ctx.tables.update(t.generate(ctx))
  out = Tier5Location().generate(ctx)
  expected = {
      'Core_DB.ADDRESS','Core_DB.STREET_ADDRESS','Core_DB.STREET_ADDRESS_DETAIL',
      'Core_DB.PARCEL_ADDRESS','Core_DB.POST_OFFICE_BOX_ADDRESS',
      'Core_DB.GEOSPATIAL_POINT','Core_DB.LOCATOR_RELATED',
  }
  assert set(out.keys()) == expected, set(out.keys()) ^ expected
  assert len(out) == 7
  assert 'Core_DB.GEOSPATIAL' not in out
  assert 'Core_DB.POSTAL_CODE' not in out
  print(f'Tier5Location produced {len(out)} tables (expected 7)')
  "
  ```
- [ ] `Tier6Links().generate(ctx)` returns exactly `{'Core_DB.PARTY_LOCATOR'}`. Run the same bootstrap plus:
  ```bash
  python -c "
  # ... (same ctx bootstrap as above) ...
  from generators.tier5_location import Tier5Location
  from generators.tier6_links import Tier6Links
  ctx.tables.update(Tier5Location().generate(ctx))
  out6 = Tier6Links().generate(ctx)
  assert set(out6.keys()) == {'Core_DB.PARTY_LOCATOR'}
  print('Tier6Links produced 1 table')
  "
  ```

### Row counts

- [ ] Row counts match spec exactly. Run:
  ```bash
  python -c "
  # ... ctx bootstrap with Tier 5 run ...
  # assertions:
  N = len(ctx.addresses)
  assert len(out['Core_DB.ADDRESS']) == N
  assert len(out['Core_DB.STREET_ADDRESS']) == N
  assert len(out['Core_DB.STREET_ADDRESS_DETAIL']) == N
  assert len(out['Core_DB.GEOSPATIAL_POINT']) == N
  assert len(out['Core_DB.PARCEL_ADDRESS']) == 15
  assert len(out['Core_DB.POST_OFFICE_BOX_ADDRESS']) == 15
  assert len(out['Core_DB.LOCATOR_RELATED']) == 20
  assert len(out6['Core_DB.PARTY_LOCATOR']) == len(ctx.customers)
  print('row counts OK')
  "
  ```

### FK resolution

- [ ] Every `STREET_ADDRESS.City_Id` resolves to `CITY.City_Id`; every `STREET_ADDRESS.Territory_Id` resolves to `TERRITORY.Territory_Id`; every `STREET_ADDRESS.Country_Id` resolves to `COUNTRY.Country_Id`; every `STREET_ADDRESS.Postal_Code_Id` resolves to `POSTAL_CODE.Postal_Code_Id`. County is nullable — check only non-null values. Run:
  ```bash
  python -c "
  # ... ctx bootstrap including Tier 5 ...
  sa = out['Core_DB.STREET_ADDRESS']
  city_ids = set(ctx.tables['Core_DB.CITY'].City_Id)
  terr_ids = set(ctx.tables['Core_DB.TERRITORY'].Territory_Id)
  country_ids = set(ctx.tables['Core_DB.COUNTRY'].Country_Id)
  postal_ids = set(ctx.tables['Core_DB.POSTAL_CODE'].Postal_Code_Id)
  county_ids = set(ctx.tables['Core_DB.COUNTY'].County_Id)
  assert set(sa.City_Id.dropna()) <= city_ids, 'STREET_ADDRESS.City_Id orphans'
  assert set(sa.Territory_Id.dropna()) <= terr_ids, 'STREET_ADDRESS.Territory_Id orphans'
  assert set(sa.Country_Id.dropna()) <= country_ids
  assert set(sa.Postal_Code_Id.dropna()) <= postal_ids
  assert set(sa.County_Id.dropna()) <= county_ids
  print('STREET_ADDRESS FK chain OK')
  "
  ```
- [ ] Every `PARCEL_ADDRESS` geography FK resolves to Tier 1 (`County_Id` nullable; all other `_Id` columns may be NULL per DDL but any populated value must resolve). Run:
  ```bash
  python -c "
  # ... ctx bootstrap including Tier 5 ...
  pa = out['Core_DB.PARCEL_ADDRESS']
  city_ids    = set(ctx.tables['Core_DB.CITY'].City_Id)
  terr_ids    = set(ctx.tables['Core_DB.TERRITORY'].Territory_Id)
  country_ids = set(ctx.tables['Core_DB.COUNTRY'].Country_Id)
  postal_ids  = set(ctx.tables['Core_DB.POSTAL_CODE'].Postal_Code_Id)
  county_ids  = set(ctx.tables['Core_DB.COUNTY'].County_Id)
  assert set(pa.City_Id.dropna())        <= city_ids,    'PARCEL City_Id orphans'
  assert set(pa.Territory_Id.dropna())   <= terr_ids,    'PARCEL Territory_Id orphans'
  assert set(pa.Country_Id.dropna())     <= country_ids, 'PARCEL Country_Id orphans'
  assert set(pa.Postal_Code_Id.dropna()) <= postal_ids,  'PARCEL Postal_Code_Id orphans'
  assert set(pa.County_Id.dropna())      <= county_ids,  'PARCEL County_Id orphans'
  # Chain coherence: every non-null Territory_Id must belong to the row's Country_Id.
  terr_df = ctx.tables['Core_DB.TERRITORY'].set_index('Territory_Id')['Country_Id'].to_dict()
  for _, row in pa.iterrows():
      tid, cid = row.Territory_Id, row.Country_Id
      if tid is not None and str(tid) != '<NA>' and cid is not None and str(cid) != '<NA>':
          assert terr_df[int(tid)] == int(cid), f'PARCEL territory/country mismatch row={row}'
  print('PARCEL_ADDRESS FK chain OK')
  "
  ```
- [ ] Every `POST_OFFICE_BOX_ADDRESS` geography FK resolves to Tier 1 (same nullability + chain-coherence rules as PARCEL). Run:
  ```bash
  python -c "
  # ... ctx bootstrap including Tier 5 ...
  po = out['Core_DB.POST_OFFICE_BOX_ADDRESS']
  city_ids    = set(ctx.tables['Core_DB.CITY'].City_Id)
  terr_ids    = set(ctx.tables['Core_DB.TERRITORY'].Territory_Id)
  country_ids = set(ctx.tables['Core_DB.COUNTRY'].Country_Id)
  postal_ids  = set(ctx.tables['Core_DB.POSTAL_CODE'].Postal_Code_Id)
  county_ids  = set(ctx.tables['Core_DB.COUNTY'].County_Id)
  assert set(po.City_Id.dropna())        <= city_ids,    'PO_BOX City_Id orphans'
  assert set(po.Territory_Id.dropna())   <= terr_ids,    'PO_BOX Territory_Id orphans'
  assert set(po.Country_Id.dropna())     <= country_ids, 'PO_BOX Country_Id orphans'
  assert set(po.Postal_Code_Id.dropna()) <= postal_ids,  'PO_BOX Postal_Code_Id orphans'
  assert set(po.County_Id.dropna())      <= county_ids,  'PO_BOX County_Id orphans'
  terr_df = ctx.tables['Core_DB.TERRITORY'].set_index('Territory_Id')['Country_Id'].to_dict()
  for _, row in po.iterrows():
      tid, cid = row.Territory_Id, row.Country_Id
      if tid is not None and str(tid) != '<NA>' and cid is not None and str(cid) != '<NA>':
          assert terr_df[int(tid)] == int(cid), f'PO_BOX territory/country mismatch row={row}'
  print('POST_OFFICE_BOX_ADDRESS FK chain OK')
  "
  ```
- [ ] Every `GEOSPATIAL_POINT.Geospatial_Point_Id` equals an `ADDRESS.Address_Id`. Run:
  ```bash
  python -c "
  addr_ids = set(out['Core_DB.ADDRESS'].Address_Id)
  gp_ids = set(out['Core_DB.GEOSPATIAL_POINT'].Geospatial_Point_Id)
  assert gp_ids == addr_ids, gp_ids ^ addr_ids
  print('GEOSPATIAL_POINT <=> ADDRESS bijection OK')
  "
  ```
- [ ] Every `LOCATOR_RELATED.Locator_Id` and `.Related_Locator_Id` resolves to `ADDRESS.Address_Id`, and `Locator_Id != Related_Locator_Id` on every row. Run:
  ```bash
  python -c "
  addr_ids = set(out['Core_DB.ADDRESS'].Address_Id)
  lr = out['Core_DB.LOCATOR_RELATED']
  assert set(lr.Locator_Id) <= addr_ids
  assert set(lr.Related_Locator_Id) <= addr_ids
  assert (lr.Locator_Id != lr.Related_Locator_Id).all()
  print('LOCATOR_RELATED pair validity OK')
  "
  ```
- [ ] Every `PARTY_LOCATOR.Party_Id` equals some `CustomerProfile.party_id`; every `PARTY_LOCATOR.Locator_Id` equals some `ADDRESS.Address_Id`. Run:
  ```bash
  python -c "
  addr_ids = set(ctx.tables['Core_DB.ADDRESS'].Address_Id)
  party_ids = {cp.party_id for cp in ctx.customers}
  pl = out6['Core_DB.PARTY_LOCATOR']
  assert set(pl.Party_Id) == party_ids, (party_ids - set(pl.Party_Id))
  assert set(pl.Locator_Id) <= addr_ids
  print('PARTY_LOCATOR FK OK; every party has exactly 1 row')
  assert pl.groupby('Party_Id').size().eq(1).all()
  "
  ```

### Literal-match constraints

- [ ] Every `PARTY_LOCATOR.Locator_Usage_Type_Cd == 'physical_primary'`. Run:
  ```bash
  python -c "
  pl = out6['Core_DB.PARTY_LOCATOR']
  assert (pl.Locator_Usage_Type_Cd == 'physical_primary').all()
  print('physical_primary literal OK')
  "
  ```
- [ ] Every `ADDRESS.Address_Subtype_Cd` resolves to `Core_DB.ADDRESS_SUBTYPE.Address_Subtype_Cd`. Run:
  ```bash
  python -c "
  valid = set(ctx.tables['Core_DB.ADDRESS_SUBTYPE'].Address_Subtype_Cd)
  a = out['Core_DB.ADDRESS']
  assert set(a.Address_Subtype_Cd) <= valid, set(a.Address_Subtype_Cd) - valid
  print('ADDRESS.Address_Subtype_Cd FK OK')
  "
  ```
- [ ] Every `STREET_ADDRESS_DETAIL.Street_Direction_Type_Cd` resolves to `DIRECTION_TYPE`, and every `Street_Suffix_Cd` to `STREET_SUFFIX_TYPE`. Run the analogous membership check.

### STREET_ADDRESS_DETAIL NOT-NULL fields

- [ ] All 8 NOT-NULL business columns of `STREET_ADDRESS_DETAIL` are populated. Run:
  ```bash
  python -c "
  d = out['Core_DB.STREET_ADDRESS_DETAIL']
  required = ['Street_Address_Num','Street_Direction_Type_Cd','Street_Name','Street_Suffix_Cd',
              'Mail_Pickup_Tm','Mail_Delivery_Tm','Mail_Stop_Num','Mail_Box_Num']
  for c in required:
      assert c in d.columns, f'missing {c}'
      assert d[c].notna().all(), f'nulls in {c}'
  assert (d.Mail_Pickup_Tm == '09:00:00').all()
  assert (d.Mail_Delivery_Tm == '15:00:00').all()
  print('STREET_ADDRESS_DETAIL NOT-NULL constraints OK')
  "
  ```

### BIGINT enforcement (PRD §7.1)

- [ ] Every `*_Id` column in every produced DataFrame is `Int64` or `int64` dtype. Run:
  ```bash
  python -c "
  bad = []
  for key, df in {**out, **out6}.items():
      for c in df.columns:
          if c.endswith('_Id'):
              if str(df[c].dtype) not in ('Int64','int64'):
                  bad.append(f'{key}.{c}: {df[c].dtype}')
  assert not bad, bad
  print('all *_Id columns BIGINT')
  "
  ```

### GEOSPATIAL skip (PRD §7.9)

- [ ] `Core_DB.GEOSPATIAL` does not appear anywhere in the returned dicts. Run:
  ```bash
  python -c "
  keys = set(out) | set(out6)
  assert 'Core_DB.GEOSPATIAL' not in keys, 'GEOSPATIAL must be skipped'
  from config.settings import SKIPPED_TABLES
  assert 'Core_DB.GEOSPATIAL' in SKIPPED_TABLES
  print('GEOSPATIAL skip OK')
  "
  ```

### DI stamping

- [ ] Every produced DataFrame has the 5-column DI tail with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. Run:
  ```bash
  python -c "
  from config.settings import HIGH_TS
  from utils.di_columns import DI_COLUMN_ORDER
  for key, df in {**out, **out6}.items():
      tail = list(df.columns[-5:])
      assert tail == list(DI_COLUMN_ORDER), f'{key}: DI tail {tail}'
      assert (df.di_end_ts == HIGH_TS).all(), f'{key}: di_end_ts drift'
      assert (df.di_rec_deleted_Ind == 'N').all(), f'{key}: di_rec_deleted_Ind drift'
  print('DI stamping OK across all tables')
  "
  ```
- [ ] No DataFrame has `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` columns (Core_DB does not stamp them). Run:
  ```bash
  python -c "
  for key, df in {**out, **out6}.items():
      banned = {'Valid_From_Dt','Valid_To_Dt','Del_Ind'}
      present = banned & set(df.columns)
      assert not present, f'{key} has CDM/PIM columns: {present}'
  print('no Valid/Del_Ind on Core_DB tables')
  "
  ```

### Writer compatibility

- [ ] After stamping, every table passes `output.writer._reorder_to_ddl()`. Run:
  ```bash
  python -c "
  from output.writer import _reorder_to_ddl
  for key, df in {**out, **out6}.items():
      try: _reorder_to_ddl(df, key)
      except Exception as e: raise SystemExit(f'{key}: {e}')
  print(f'{len({**out, **out6})} tables pass _reorder_to_ddl')
  "
  ```

### Prerequisite guard

- [ ] `Tier5Location.generate()` raises `RuntimeError` when a Tier 1 prerequisite is missing. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier5_location import Tier5Location
  class Ctx:
      addresses = []
      customers = []
      ids = IdFactory(ID_RANGES)
      rng = np.random.default_rng(42)
      tables = {}
  try:
      Tier5Location().generate(Ctx())
      raise AssertionError('should have raised RuntimeError')
  except RuntimeError as e:
      assert 'Tier' in str(e) or 'CITY' in str(e) or 'TERRITORY' in str(e), str(e)
  print('Tier5Location prerequisite guard OK')
  "
  ```
- [ ] `Tier6Links.generate()` raises `RuntimeError` when `Core_DB.ADDRESS` is missing. Same pattern.

### Reproducibility

- [ ] Two back-to-back runs produce byte-identical DataFrames. Run:
  ```bash
  python -c "
  import numpy as np
  import config.settings as _s
  from config.settings import SEED
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  from generators.tier3_party_subtypes import Tier3PartySubtypes
  from generators.tier5_location import Tier5Location
  from generators.tier6_links import Tier6Links
  def run():
      ctx = UniverseBuilder().build(_s, np.random.default_rng(SEED))
      for t in (Tier0Lookups(), Tier1Geography(), Tier2Core(), Tier3PartySubtypes()):
          ctx.tables.update(t.generate(ctx))
      ctx.tables.update(Tier5Location().generate(ctx))
      return Tier5Location().generate(ctx), Tier6Links().generate(ctx)
  (a5, a6), (b5, b6) = run(), run()
  for d1, d2 in ((a5, b5), (a6, b6)):
      assert set(d1) == set(d2)
      for k in d1:
          assert d1[k].equals(d2[k]), f'{k} differs between runs'
  print('reproducibility OK')
  "
  ```

### No randomness / side-effect imports

- [ ] Generator modules do not import `faker` (Faker usage belongs to UniverseBuilder, not downstream tiers). `numpy` and `random` are allowed. Run:
  ```bash
  python -c "
  import re, pathlib
  pat = re.compile(r'^\s*(?:import|from)\s+faker\b')
  bad = []
  for p in ('generators/tier5_location.py','generators/tier6_links.py'):
      for i, line in enumerate(pathlib.Path(p).read_text().splitlines(), 1):
          if pat.match(line): bad.append(f'{p}:{i}: {line}')
  assert not bad, bad
  print('no faker import in tier5/6')
  "
  ```
- [ ] Neither module reads `AddressRecord.city_id`/`.county_id`/`.territory_id`/`.postal_code_id`/`.country_id`. Run:
  ```bash
  python -c "
  import re, pathlib
  pat = re.compile(r'\.(?:city_id|county_id|territory_id|postal_code_id|country_id)\b')
  bad = []
  for p in ('generators/tier5_location.py','generators/tier6_links.py'):
      for i, line in enumerate(pathlib.Path(p).read_text().splitlines(), 1):
          if 'ar.' in line and pat.search(line):
              bad.append(f'{p}:{i}: {line.rstrip()}')
  assert not bad, bad
  print('no AddressRecord placeholder FK reads')
  "
  ```
- [ ] Importing the modules does not construct DataFrames. Run:
  ```bash
  python -c "
  import importlib, sys, pandas as pd
  calls = {'n': 0}
  _orig = pd.DataFrame
  def _wrap(*a, **k):
      calls['n'] += 1; return _orig(*a, **k)
  pd.DataFrame = _wrap
  for name in ('generators.tier5_location','generators.tier6_links'):
      sys.modules.pop(name, None)
      importlib.import_module(name)
  pd.DataFrame = _orig
  assert calls['n'] == 0, f'{calls[\"n\"]} DataFrames built at import time'
  print('no import-time DataFrames')
  "
  ```

### config/settings.py modification

- [ ] `ID_RANGES` contains the three new sub-type categories. Run:
  ```bash
  python -c "
  from config.settings import ID_RANGES
  needed = {'street_address','parcel_address','post_office_box'}
  assert needed <= set(ID_RANGES), needed - set(ID_RANGES)
  vals = list(ID_RANGES.values())
  assert len(vals) == len(set(vals)), 'duplicate ID_RANGES starts'
  print('ID_RANGES updated')
  "
  ```

### Universal checks

- [ ] `git status --porcelain` shows only: `config/settings.py` (modified), `generators/tier5_location.py` (new), `generators/tier6_links.py` (new), plus this spec file at `.claude/specs/step-15-tier5-6-location-links.md` (already on branch). No stray files (no `__pycache__` in stage, no output CSVs, no edits under `utils/`, `registry/`, `output/`, `references/`, other `seed_data/*.py`, other `generators/*.py`). Run:
  ```bash
  git status --porcelain
  ```
- [ ] All new files pass `python -c "import <module>"` — covered by the first Module-import check.
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — covered by BIGINT dtype check above. **n/a for the CSV-on-disk variant**: this step produces no CSVs; writer is not invoked.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: not touched in this step (Step 22 Tier 14 CDM_DB emits that table).
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSV output; writer not invoked. The equivalent in-memory check (`'Core_DB.GEOSPATIAL' not in ctx.tables`) is covered by the GEOSPATIAL-skip check above.

## Handoff notes

_Leave empty — filled by the implementation session per `implementation-steps.md` Handoff Protocol._

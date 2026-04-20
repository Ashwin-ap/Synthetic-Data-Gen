# Spec: Step 09 — Tier 1 Geography

## Overview

This step builds **Tier 1 — Geography**, the ten Core_DB tables that form the shared geography backbone every downstream tier FKs into: country → region → territory → county → city → postal code, plus the two ISO 3166 standard tables, plus the `GEOGRAPHICAL_AREA` / `GEOGRAPHICAL_AREA_CURRENCY` pair that carries currency-role assignments per geographic area. Unlike Tier 0 (pure hand-coded lookups consumed as-is), Tier 1 tables carry BIGINT surrogate `*_Id` primary keys that the `ADDRESS` / `STREET_ADDRESS` / `PARCEL_ADDRESS` / `POST_OFFICE_BOX_ADDRESS` / `PARTY_LOCATOR` chain in Step 15 (Tier 5 + Tier 6) references by ID. The data itself — country names, US state codes, ISO numeric/alpha codes, time zones, a representative set of cities and postal codes — is still fully hand-authored and deterministic, but **ID assignment is done by the generator using `ctx.ids` (`IdFactory`)**, not hard-coded in the seed module. This keeps BIGINT ID management centralised (PRD §7.1, design §8) and means the seed module is pure reference data that can be audited independent of ID allocation. This step also enforces the **territory chain literal-match requirement** from `references/02_data-mapping-reference.md` Step 3 #19: every US state row in `ISO_3166_COUNTRY_SUBDIVISION_STANDARD` must carry `Territory_Standard_Type_Cd = 'ISO 3166-2 Country Subdivision Standard'` — that exact string drives a WP3 Layer 2 join that otherwise fails silently. See `mvp-tool-design.md` §9 Tier 1 for the authoritative scope and `PRD.md` §4.2 "Address & Location" for the enumerated table list.

## Depends on

- **Step 1** — consumes from `config/settings.py`:
  - `ID_RANGES` — this step adds seven new category entries (`country`, `region`, `territory`, `county`, `city`, `postal_code`, `geographical_area`). See ## Files to modify.
  - `HIGH_TS` — stamped as `di_end_ts` default on every active Tier 1 row via `BaseGenerator.stamp_di()`.
  - `HIGH_DATE` — n/a: Tier 1 tables are all Core_DB; no `Valid_To_Dt`.
- **Step 2** — consumes `generators/base.BaseGenerator` (`stamp_di()` method) and `utils/id_factory.IdFactory` (`next(category)` / `next_many(category, n)` methods). The new `Tier1Geography` class inherits from `BaseGenerator`.
- **Step 3** — consumes `registry/context.GenerationContext`. `Tier1Geography.generate(ctx)` reads `ctx.ids` to mint BIGINT IDs. It does NOT mutate `ctx.tables` (the orchestrator does the `ctx.tables.update()` after every tier, per `mvp-tool-design.md` §15).
- **Step 8** — consumes four already-stamped Tier 0 tables that Tier 1 FK-references by code (not by surrogate key):
  - `Core_DB.CURRENCY` — `GEOGRAPHICAL_AREA_CURRENCY.Currency_Cd` must resolve to a seeded currency row. `USD`, `EUR`, `GBP`, `CAD`, `AUD`, `JPY` are all present after Step 8.
  - `Core_DB.CALENDAR_TYPE` — `COUNTRY.Calendar_Type_Cd` is NOT NULL. Every country uses `'GREGORIAN'` (present in Tier 0).
  - `Core_DB.CITY_TYPE` — `CITY.City_Type_Cd` is nullable but populated. Use `'CITY'`/`'TOWN'`/`'MUNICIPALITY'` (all present in Tier 0).
  - `Core_DB.TERRITORY_TYPE` — `TERRITORY.Territory_Type_Cd` is nullable but populated. Use `'STATE'` for US states, `'PROVINCE'` for Canadian provinces, `'COUNTRY_SUBDIVISION'` otherwise (all present in Tier 0).

No code from Step 4 (UniverseBuilder) or Step 5 (Writer) is imported by this step — Tier 1 is pure reference generation and does not depend on the customer/agreement universe. Step 5's writer parses DDL column order from `references/07_mvp-schema-reference.md` at Step 25 orchestration time; this step only needs to emit DataFrames with columns in DDL order.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 9):
- `PRD.md` §4.2 "Address & Location" (enumerated table list), §7.1 (BIGINT rule), §7.3 (DI column rules; active-record sentinels), §7.9 (GEOSPATIAL skip — n/a for this step but the principle applies: do not invent tables)
- `mvp-tool-design.md` §7 (`BaseGenerator` + DI column rules), §8 (ID Factory — new geography categories must match the documented range pattern), §9 Tier 1 Geography (authoritative scope + territory-chain requirement), §15 (orchestrator signature — `Tier1Geography()` is the second item in the `tiers` list after `Tier0Lookups`)
- `implementation-steps.md` Step 9 entry (exit criteria); Handoff Protocol (post-session notes rules)

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the ten Tier 1 tables. Open only these blocks (line numbers current as of 2026-04-20):
  - `COUNTRY` (§2287) — `Country_Id` PK, `Calendar_Type_Cd` NOT NULL, `Country_Group_Id` nullable (set to `None`; Country_Group is not in MVP scope)
  - `REGION` (§2395) — `Region_Id` PK, `Country_Id` nullable
  - `TERRITORY` (§2405) — `Territory_Id` PK, `Territory_Type_Cd` nullable, `Country_Id` **NOT NULL**, `Region_Id` nullable
  - `COUNTY` (§2330) — `County_Id` PK, `Territory_Id` **NOT NULL**, `MSA_Id` nullable
  - `CITY` (§2215) — `City_Id` PK, `City_Type_Cd` nullable, `Territory_Id` nullable
  - `POSTAL_CODE` (§2202) — `Postal_Code_Id` PK, `County_Id` nullable, `Country_Id` **NOT NULL**, `Postal_Code_Num` nullable (but always populated here), `Time_Zone_Cd` nullable
  - `ISO_3166_COUNTRY_STANDARD` (§2313) — `ISO_3166_Country_3_Num` CHAR(3) PK, `Country_Id` NOT NULL, `Country_Code_Standard_Type_Cd` NOT NULL
  - `ISO_3166_COUNTRY_SUBDIVISION_STANDARD` (§2190) — `Territory_Id` PK, `Territory_Standard_Type_Cd` **NOT NULL** (must equal `'ISO 3166-2 Country Subdivision Standard'` per item #19), `ISO_3166_Country_Alpha_2_Cd` nullable, `ISO_3166_Country_Subdivision_Cd` nullable
  - `GEOGRAPHICAL_AREA` (§2226) — `Geographical_Area_Id` PK, `Geographical_Area_Subtype_Cd` **NOT NULL**, name/desc/start/end fields. The block shows columns listed twice (lines 2230 and 2240) — this is the schema-reference's Core_DB + CDM_DB duplication; use the first occurrence (10 columns including the 3 DI columns). Do NOT emit duplicate columns.
  - `GEOGRAPHICAL_AREA_CURRENCY` (§2251) — `Geographical_Area_Id` + `Currency_Cd` composite PK, `Geographical_Area_Currency_Start_Dt` NOT NULL, `Geographical_Area_Currency_Role_Cd` NOT NULL, `Geographical_Area_Currency_End_Dt` nullable
  - Footnotes in `07` §§3121–3125 ("INTEGER FK candidate") explicitly flag `POSTAL_CODE.Country_Id`, `ISO_3166_COUNTRY_STANDARD.Country_Id`, `COUNTY.Territory_Id`, and `TERRITORY.Country_Id` as INTEGER NOT NULL that "may need BIGINT for CDM_DB cross-schema joins". The BIGINT rule from PRD §7.1 is universal — **always emit these columns as BIGINT (pandas `Int64`) regardless of the DDL saying INTEGER.**
- `references/02_data-mapping-reference.md` Step 3 item #19 — "Territory chain for addresses: STREET ADDRESS BB → TERRITORY BB → REGION BB requires `Territory Standard Type = 'ISO 3166-2 Country Subdivision Standard'`". This is the sole literal-match constraint on Tier 1 and is enforced in ## Definition of done.

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is the MVP-filtered authoritative DDL set per PRD §10.
- `references/05_architect-qa.md` — no Q touches the geography domain.
- `references/06_supporting-enrichments.md` — geography is deterministic reference data, not a distribution.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `resources/iDM_MDM_tables_DDLs.xlsx` — already distilled into `07`.

## Produces

All paths relative to the project root.

**New files:**

- `seed_data/geography_ref.py` — hand-authored static geography reference data. Exposes a single public function `get_geography_seed_data() -> Dict[str, List[Dict]]`. Unlike Tier 0 seed modules (which return DataFrames keyed by `'Core_DB.<TABLE>'`), this module returns **lists of plain dicts without IDs** — surrogate `*_Id` columns are minted later by `Tier1Geography.generate()` via `ctx.ids`. Keys returned:
  - `'countries'` — list of ~20 countries. Each entry: `{name, iso_alpha_2, iso_alpha_3, iso_numeric_3, calendar_type_cd}`. Must include at least: `United States` (USA/840), `Canada` (CAN/124), `United Kingdom` (GBR/826), `Germany` (DEU/276), `France` (FRA/250), `Japan` (JPN/392), `Australia` (AUS/036), `Mexico` (MEX/484), `Brazil` (BRA/076), `China` (CHN/156), `India` (IND/356), `Spain` (ESP/724), `Italy` (ITA/380), `Netherlands` (NLD/528), `Switzerland` (CHE/756), `Sweden` (SWE/752), `Ireland` (IRL/372), `Singapore` (SGP/702), `South Africa` (ZAF/710), `Norway` (NOR/578). `calendar_type_cd` is `'GREGORIAN'` for every country. ISO numeric codes must match the official ISO 3166-1 numeric standard — do not invent.
  - `'us_states'` — list of all 50 US states + DC. Each entry: `{name, usps_2, iso_subdivision_3}` where `usps_2` is the 2-letter USPS code (`CA`, `NY`, `TX`, …) and `iso_subdivision_3` is the 3-char ISO 3166-2:US subdivision code (`US-CA`, `US-NY` format truncated to the post-hyphen 2–3 chars — the DDL column `ISO_3166_Country_Subdivision_Cd` is CHAR(3), so store just the subdivision letters e.g. `'CA '`, `'NY '`, padded if needed, or the 2-letter USPS code — the implementation session picks one deterministic convention and applies it uniformly across all 51 rows. Recommend using the USPS 2-letter code right-padded to 3 chars, which matches common US banking practice).
  - `'foreign_territories'` — list of ~10 subdivisions in non-US countries chosen for demographic plausibility in the customer universe (e.g. Canada: `Ontario`/`Quebec`/`British Columbia`; UK: `England`/`Scotland`; Germany: `Bavaria`/`Berlin`; France: `Île-de-France`). Each entry: `{name, country_iso_alpha_3, territory_type_cd}`. `territory_type_cd` is `'PROVINCE'` for Canada, `'COUNTRY_SUBDIVISION'` for UK/DE/FR. These appear in `TERRITORY` but are NOT required to populate `ISO_3166_COUNTRY_SUBDIVISION_STANDARD` (that table's literal-match constraint only binds on US states).
  - `'cities'` — list of ~100 cities. Each entry: `{name, state_usps_2, country_iso_alpha_3, city_type_cd, postal_codes, time_zone_cd}`. `postal_codes` is a list of 1–3 realistic postal-code strings for that city (e.g. `New York, NY` → `['10001', '10016', '10025']`). `city_type_cd` is `'CITY'` / `'TOWN'` / `'MUNICIPALITY'` (all seeded in Tier 0). Coverage: at least 60 US cities across at least 25 states plus ~10 international cities. The international cities' `state_usps_2` is `None` — their parent territory is looked up from `foreign_territories` by country.
  - `'counties'` — list of ~20 US counties. Each entry: `{name, state_usps_2}`. Counties are sparse (most `POSTAL_CODE.County_Id` rows will be `None`); seed enough to let Step 15 pick one for representative addresses.
  - `'geographical_areas'` — list of ~10 rows for `GEOGRAPHICAL_AREA`. Each entry: `{name, subtype_cd, short_name, desc, currency_cd, start_dt}`. `subtype_cd` distinguishes continents, economic zones, and country groups (e.g. `'CONTINENT'`, `'ECONOMIC_ZONE'`, `'TRADE_BLOC'`). Must include: `North America` / USD, `Europe` / EUR, `United Kingdom Region` / GBP, `Asia Pacific` / USD (generic), `Latin America` / USD, `Eurozone` / EUR. Each area gets a `GEOGRAPHICAL_AREA_CURRENCY` row with role `'preferred'`.

- `generators/tier1_geography.py` — `class Tier1Geography(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]` method. Implementation contract:
  1. Import `get_geography_seed_data` from `seed_data.geography_ref`; import `BaseGenerator`; import `GenerationContext` under `TYPE_CHECKING` only.
  2. Guard: verify `ctx.ids` is non-None and that the four Tier 0 prerequisite tables are present in `ctx.tables` (`Core_DB.CURRENCY`, `Core_DB.CALENDAR_TYPE`, `Core_DB.CITY_TYPE`, `Core_DB.TERRITORY_TYPE`). If any are missing, raise `RuntimeError(f'Tier1Geography requires Tier 0 table {key} to be loaded first')`. This guards against orchestration drift.
  3. Load the seed dicts (one call to `get_geography_seed_data()`).
  4. Mint IDs via `ctx.ids.next('country')` / `'region'` / `'territory'` / `'county'` / `'city'` / `'postal_code'` / `'geographical_area'`. Build **in-memory index dicts** (`country_id_by_iso3`, `territory_id_by_usps`, `city_id_by_key`, …) so FK wiring is O(1).
  5. Build ten DataFrames in FK-dependency order:
     - `COUNTRY` — one row per country. `Country_Group_Id` = `None`.
     - `ISO_3166_COUNTRY_STANDARD` — one row per country with `Country_Code_Standard_Type_Cd = 'ISO 3166-1 numeric'` and `ISO_3166_Country_3_Num = <iso_numeric_3>`.
     - `REGION` — one row per country acting as its own geographic region. `Country_Id` FK.
     - `TERRITORY` — one row per US state (`Territory_Type_Cd = 'STATE'`) + one row per foreign territory. `Country_Id` NOT NULL resolves via ISO alpha-3. `Region_Id` resolves to the country's own region.
     - `ISO_3166_COUNTRY_SUBDIVISION_STANDARD` — one row per US state. `Territory_Id` FK. `Territory_Standard_Type_Cd = 'ISO 3166-2 Country Subdivision Standard'` **verbatim** (this is the literal-match constraint from item #19).
     - `COUNTY` — one row per seeded US county. `Territory_Id` NOT NULL; `MSA_Id` = `None`.
     - `CITY` — one row per seeded city. `Territory_Id` resolves via USPS or foreign-territory name.
     - `POSTAL_CODE` — one row per distinct postal code across all cities (flatten the `postal_codes` lists). `Country_Id` NOT NULL; `County_Id` mostly `None`; a handful wired to seeded counties for coverage.
     - `GEOGRAPHICAL_AREA` — one row per seeded area.
     - `GEOGRAPHICAL_AREA_CURRENCY` — one row per area with `Geographical_Area_Currency_Role_Cd = 'preferred'`, `Geographical_Area_Currency_Start_Dt = HISTORY_START - some margin` (use `date(2000, 1, 1)` as a safe constant), `Geographical_Area_Currency_End_Dt = None`. `Currency_Cd` resolves to the Tier 0 CURRENCY row.
  6. For every DataFrame, stamp via `self.stamp_di(df)`. Do NOT call `stamp_valid()` — Tier 1 tables are all Core_DB.
  7. Return `Dict[str, pd.DataFrame]` keyed `Core_DB.<TABLE>` for all ten tables. Do not mutate `ctx.tables` — the orchestrator does that.

**Do NOT produce** in this step:
- CSVs — writer is not invoked. `output/` must remain empty.
- Wiring into `main.py` — orchestrator changes are Step 25's responsibility.
- New Tier 0 lookup rows — `CURRENCY`/`CALENDAR_TYPE`/`CITY_TYPE`/`TERRITORY_TYPE` are already seeded. If Tier 1 needs a code that is not seeded, escalate per Handoff Protocol §2 rather than monkey-patching Tier 0.
- `GEOSPATIAL` rows — `GEOSPATIAL_POINT` is generated in Step 15, not here; `GEOSPATIAL` (with `ST_Geometry`) is in `SKIPPED_TABLES`.
- `MSA` rows — no `MSA` table is in MVP scope; `COUNTY.MSA_Id` stays `None`.

## Tables generated (if applicable)

After `Tier1Geography.generate(ctx)` runs, `ctx.tables` gains these ten Core_DB keys (row counts are minima — actual counts may be slightly higher depending on how many foreign territories / cities the session decides to seed within the stated bounds):

| Table | Min rows | FK dependencies | Literal-match / constraint requirements |
|-------|---------:|------------------|------------------------------------------|
| `Core_DB.COUNTRY` | 20 | `CALENDAR_TYPE.Calendar_Type_Cd` | All rows use `Calendar_Type_Cd = 'GREGORIAN'` |
| `Core_DB.ISO_3166_COUNTRY_STANDARD` | 20 | `COUNTRY.Country_Id` | `Country_Code_Standard_Type_Cd = 'ISO 3166-1 numeric'`; `ISO_3166_Country_3_Num` matches official standard |
| `Core_DB.REGION` | 20 | `COUNTRY.Country_Id` | One region per country |
| `Core_DB.TERRITORY` | 60 | `COUNTRY.Country_Id` (NOT NULL), `TERRITORY_TYPE.Territory_Type_Cd`, `REGION.Region_Id` | 50 US states + DC + ≥9 foreign; `Territory_Type_Cd = 'STATE'` for US, `'PROVINCE'` for CA |
| `Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD` | 50 | `TERRITORY.Territory_Id` | **`Territory_Standard_Type_Cd = 'ISO 3166-2 Country Subdivision Standard'` on every row (Step 3 #19 literal-match)** |
| `Core_DB.COUNTY` | 20 | `TERRITORY.Territory_Id` (NOT NULL) | `MSA_Id = None` on every row |
| `Core_DB.CITY` | 100 | `CITY_TYPE.City_Type_Cd`, `TERRITORY.Territory_Id` | ≥60 US cities spanning ≥25 states; ≥10 international |
| `Core_DB.POSTAL_CODE` | 100 | `COUNTY.County_Id` (nullable), `COUNTRY.Country_Id` (NOT NULL) | Every postal code FK-resolves to a COUNTRY row |
| `Core_DB.GEOGRAPHICAL_AREA` | 6 | — | Includes North America, Europe, Eurozone, UK Region, Asia Pacific, Latin America |
| `Core_DB.GEOGRAPHICAL_AREA_CURRENCY` | 6 | `GEOGRAPHICAL_AREA.Geographical_Area_Id`, `CURRENCY.Currency_Cd` | Every row has `Geographical_Area_Currency_Role_Cd = 'preferred'` |

All ten DataFrames have the full 5-column DI tail in `DI_COLUMN_ORDER` after `stamp_di()`, with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`.

## Files to modify

- `config/settings.py` — add exactly seven new entries to `ID_RANGES`. Choose starting offsets that do not overlap any existing category. Recommended values (match the "small-universe" offset pattern of `channel: 50` / `campaign: 100` / `market_seg: 500`):
  ```python
  ID_RANGES = {
      ...  # existing entries unchanged
      'country':            700,
      'region':             800,
      'territory':          900,
      'county':           1_100,
      'city':             1_400,
      'postal_code':      1_600,
      'geographical_area': 1_900,
  }
  ```
  These offsets accommodate the min-row counts above with plenty of headroom. Do not reorder or renumber existing categories — that would break `utils/id_factory.py` reproducibility for any entity already minted in prior steps' dev environments.

- No other files modified. `config/code_values.py`, `config/distributions.py`, `utils/`, `registry/`, `output/`, `main.py`, `CLAUDE.md`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/`, existing `seed_data/*.py`, existing `generators/*.py` are NOT touched.

- `seed_data/__init__.py` and `generators/__init__.py` already exist and are empty — do NOT modify.

If the implementation session finds that `references/07_mvp-schema-reference.md` disagrees with this spec on a column name, type, or nullability, escalate per Handoff Protocol §2 — update the upstream reference or add a `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new dependencies. `pandas`, `numpy`, `python-dateutil` are already in `requirements.txt` (Step 1). This step imports only the standard library + pandas + existing project modules.

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — every `*_Id` column in every Tier 1 DataFrame is emitted as `pd.Int64Dtype()` (nullable BIGINT) or `int64` (when all non-null). The DDL in `07` declares `INTEGER` for these columns and `07` §§3121–3125 flag them explicitly as "INTEGER FK candidate → BIGINT". The BIGINT rule wins.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — n/a: no party IDs in Tier 1.
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on all ten DataFrames returned by `Tier1Geography.generate()`. No seed-module-level DI placeholders this time: because the generator builds DataFrames from scratch (rather than merging pre-built dict DataFrames), it constructs each DataFrame with only the business columns and applies `stamp_di()` once at the end. This differs from Tier 0's pattern (placeholder DI → drop → stamp), but the post-stamp state is identical.
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts` stamped to `HIGH_TS` via `stamp_di()` default. `Valid_To_Dt` n/a: Tier 1 is all Core_DB.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — n/a: Tier 1 is all Core_DB. Do NOT call `stamp_valid()`.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** — enforced at construction time. Every DataFrame is built via `pd.DataFrame(rows, columns=_COLS)` where `_COLS` is the authoritative DDL column list including the three DI columns as the last three placeholders (matching the Tier 0 pattern so `stamp_di()` can drop-and-replace uniformly). Alternatively, the generator may build with business columns only and rely on `stamp_di()` to append the 5 DI columns at the end — in that case, the DataFrame before stamping has DDL business columns only, and after stamping the 5 DI columns appear in positions matching the DDL's 3 DI columns (the two extras, `di_data_src_cd` and `di_proc_name`, are injected to meet PRD §7.3 but absent from `07` DDL — this is by design and matches Tier 0's final state). The Definition-of-done check against `_load_ddl_column_order()` allows for this stamped-form difference.
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — n/a: not touched here.
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — n/a: no GEOSPATIAL row authored. `GEOSPATIAL_POINT` (DECIMAL lat/lon) is Step 15's responsibility, not this step's.
- **No ORMs, no database connections — pure pandas → CSV** — writer is not invoked. Generator returns DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — **no randomness in this step**. Every row is hand-coded; every ID is drawn from `ctx.ids` which is deterministic. The generator does not read or use `ctx.rng`.

Step-specific rules (Tier 1 Geography):

- **Seed data has no IDs.** `seed_data/geography_ref.py` returns plain `List[Dict]` entries. Surrogate `*_Id` values are minted only inside `Tier1Geography.generate()`. This separation keeps the seed module auditable against real-world reference data (ISO codes, USPS codes, city names) without coupling to ID allocation.
- **FK wiring via in-memory index dicts.** Build `country_id_by_iso3: Dict[str, int]`, `territory_id_by_usps: Dict[str, int]`, `region_id_by_country_iso3: Dict[str, int]`, etc. during COUNTRY/REGION/TERRITORY construction. Resolve FKs at CITY/POSTAL_CODE/COUNTY construction time via these dicts. Do NOT scan DataFrames linearly to find FKs — O(n²) for no reason.
- **Tier 0 prerequisite guard.** `Tier1Geography.generate()` starts with an explicit check that all four Tier 0 prerequisite tables are in `ctx.tables`. Fail fast with `RuntimeError` if any is missing. This protects against orchestration drift (Step 25 may be edited in a future PR that reorders tiers).
- **Territory chain literal-match (item #19).** Every row in `ISO_3166_COUNTRY_SUBDIVISION_STANDARD` must carry the exact string `'ISO 3166-2 Country Subdivision Standard'` (note exact capitalisation and spacing — `Territory` with capital T, `Subdivision` with capital S, etc.) in `Territory_Standard_Type_Cd`. A helper module-level constant `_ISO_3166_2_SUBDIVISION_STD = 'ISO 3166-2 Country Subdivision Standard'` makes this unambiguous.
- **ISO numeric codes are authoritative.** The `iso_numeric_3` values in the `'countries'` seed list must match the official ISO 3166-1 numeric codes. The implementation session verifies at least the six most-used entries (USA=840, CAN=124, GBR=826, DEU=276, FRA=250, JPN=392) against public knowledge; wrong codes would break any downstream reporting that joins on the numeric standard.
- **Postal code breadth.** Minimum 100 distinct `Postal_Code_Num` values across at least 25 US states plus a handful of international samples (Canadian postal codes use the `A1A 1A1` format; UK uses `SW1A 1AA`-style; international breadth is symbolic only). Time_Zone_Cd populated where known (`ET`/`CT`/`MT`/`PT` for US; `None` OK elsewhere).
- **Deterministic iteration order.** Python dicts preserve insertion order (3.7+) and `IdFactory` increments monotonically. If the seed module returns lists in a deterministic order (they must — hand-authored lists are deterministic), the generated IDs are reproducible across runs. A seed list reshuffle between sessions will change IDs — this is acceptable (no persisted state yet) but should be flagged in handoff notes if it happens.
- **No side effects on import.** `import seed_data.geography_ref` must not construct any DataFrames or perform any network/file I/O. `get_geography_seed_data()` returns plain dicts/lists built at call time. `import generators.tier1_geography` must not instantiate the class or call `generate()`. Enforced by the "no import-time DataFrames" check in Definition of done.
- **`Tier1Geography.generate()` must accept `ctx`** — the `BaseGenerator.generate(self, ctx)` signature is fixed by Step 2. Runtime-import `GenerationContext` via `TYPE_CHECKING` only.
- **No changes to existing files beyond `config/settings.py`.** If implementation discovers that a Tier 0 table in `ctx.tables` is missing a row needed for Tier 1 (e.g., `TERRITORY_TYPE.STATE` is absent), fix it in the Tier 0 seed module in a dedicated follow-up commit rather than stuffing the row into Tier 1. This spec assumes the Step 8 handoff ("79 stamped Core_DB lookup tables") is accurate.
- **Escalation over improvisation.** If `07` has an ambiguity (column name differs from this spec, nullability unclear), stop and leave a `⚠️ Conflict` block in this spec. Do NOT invent columns.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current directory and `python` resolves to the project's Python 3.12 environment.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

**Module-import and API contract:**

- [ ] `python -c "import seed_data.geography_ref, generators.tier1_geography"` exits 0.
- [ ] `seed_data.geography_ref.get_geography_seed_data()` returns a dict with the six expected keys and non-empty lists. Run:
  ```bash
  python -c "
  from seed_data.geography_ref import get_geography_seed_data
  d = get_geography_seed_data()
  expected = {'countries','us_states','foreign_territories','cities','counties','geographical_areas'}
  assert set(d.keys()) == expected, set(d.keys()) ^ expected
  for k, v in d.items():
      assert isinstance(v, list) and len(v) > 0, f'{k} empty or wrong type'
  print('geography_ref keys OK')
  "
  ```
- [ ] `generators.tier1_geography.Tier1Geography` inherits from `BaseGenerator` and `generate(ctx)` is defined. Run:
  ```bash
  python -c "
  from generators.tier1_geography import Tier1Geography
  from generators.base import BaseGenerator
  import inspect
  assert issubclass(Tier1Geography, BaseGenerator)
  sig = inspect.signature(Tier1Geography.generate)
  assert 'ctx' in sig.parameters
  print('Tier1Geography contract OK')
  "
  ```

**`Tier1Geography.generate()` produces the ten expected tables:**

- [ ] `Tier1Geography.generate()` returns exactly these 10 `Core_DB.<TABLE>` keys. Run (builds a minimal ctx with Tier 0 prerequisites loaded):
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42)
          self.tables = {}
  ctx = Ctx()
  ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  expected = {
      'Core_DB.COUNTRY','Core_DB.ISO_3166_COUNTRY_STANDARD','Core_DB.REGION',
      'Core_DB.TERRITORY','Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD',
      'Core_DB.COUNTY','Core_DB.CITY','Core_DB.POSTAL_CODE',
      'Core_DB.GEOGRAPHICAL_AREA','Core_DB.GEOGRAPHICAL_AREA_CURRENCY',
  }
  assert set(out.keys()) == expected, expected ^ set(out.keys())
  print(f'Tier1Geography produced {len(out)} tables')
  "
  ```
- [ ] Row-count minima met across the ten tables. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42)
          self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  mins = {
      'Core_DB.COUNTRY': 20, 'Core_DB.ISO_3166_COUNTRY_STANDARD': 20,
      'Core_DB.REGION': 20, 'Core_DB.TERRITORY': 60,
      'Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD': 50,
      'Core_DB.COUNTY': 20, 'Core_DB.CITY': 100, 'Core_DB.POSTAL_CODE': 100,
      'Core_DB.GEOGRAPHICAL_AREA': 6, 'Core_DB.GEOGRAPHICAL_AREA_CURRENCY': 6,
  }
  bad = [(k, len(out[k]), mins[k]) for k in mins if len(out[k]) < mins[k]]
  assert not bad, bad
  print('row counts OK', {k: len(out[k]) for k in mins})
  "
  ```

**FK-chain resolution (implementation-steps.md Step 9 exit criterion):**

- [ ] Every `CITY.Territory_Id` resolves to a `TERRITORY.Territory_Id`. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  territory_ids = set(out['Core_DB.TERRITORY'].Territory_Id.dropna())
  city_tids = set(out['Core_DB.CITY'].Territory_Id.dropna())
  orphan = city_tids - territory_ids
  assert not orphan, f'CITY orphan Territory_Ids: {orphan}'
  print('CITY->TERRITORY FK OK')
  "
  ```
- [ ] Every `REGION.Country_Id` resolves to a `COUNTRY.Country_Id` (column is nullable in DDL but the generator populates every row — any NULL would mean a region was built without a country and must fail the check). Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  country_ids = set(out['Core_DB.COUNTRY'].Country_Id)
  r = out['Core_DB.REGION']
  assert r.Country_Id.notna().all(), 'REGION.Country_Id must be populated on every row (one region per country)'
  orphan = set(r.Country_Id) - country_ids
  assert not orphan, f'REGION orphan Country_Ids: {orphan}'
  print('REGION->COUNTRY FK OK')
  "
  ```
- [ ] Every populated `TERRITORY.Region_Id` resolves to a `REGION.Region_Id` (column is nullable; check uses `dropna()` like the CITY.Territory_Id check). A corrupted REGION table would silently break Tier 5 address wiring, so this must be enforced at generation time. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  region_ids = set(out['Core_DB.REGION'].Region_Id.dropna())
  t = out['Core_DB.TERRITORY']
  terr_rids = set(t.Region_Id.dropna())
  orphan = terr_rids - region_ids
  assert not orphan, f'TERRITORY orphan Region_Ids: {orphan}'
  print('TERRITORY->REGION FK OK')
  "
  ```
- [ ] Every `TERRITORY.Country_Id` (NOT NULL) resolves to a `COUNTRY.Country_Id`. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  country_ids = set(out['Core_DB.COUNTRY'].Country_Id)
  t = out['Core_DB.TERRITORY']
  assert t.Country_Id.notna().all(), 'TERRITORY.Country_Id must be NOT NULL'
  orphan = set(t.Country_Id) - country_ids
  assert not orphan, f'TERRITORY orphan Country_Ids: {orphan}'
  print('TERRITORY->COUNTRY FK OK')
  "
  ```
- [ ] Every `POSTAL_CODE.Country_Id` (NOT NULL) resolves to a `COUNTRY.Country_Id`. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  cids = set(out['Core_DB.COUNTRY'].Country_Id)
  pc = out['Core_DB.POSTAL_CODE']
  assert pc.Country_Id.notna().all(), 'POSTAL_CODE.Country_Id must be NOT NULL'
  orphan = set(pc.Country_Id) - cids
  assert not orphan, f'POSTAL_CODE orphan Country_Ids: {orphan}'
  print('POSTAL_CODE->COUNTRY FK OK')
  "
  ```
- [ ] Every `COUNTY.Territory_Id` (NOT NULL) resolves. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  tids = set(out['Core_DB.TERRITORY'].Territory_Id)
  co = out['Core_DB.COUNTY']
  assert co.Territory_Id.notna().all()
  orphan = set(co.Territory_Id) - tids
  assert not orphan, f'COUNTY orphan Territory_Ids: {orphan}'
  print('COUNTY->TERRITORY FK OK')
  "
  ```
- [ ] Every `ISO_3166_COUNTRY_SUBDIVISION_STANDARD.Territory_Id` resolves to a US-state `TERRITORY.Territory_Id` (`Territory_Type_Cd = 'STATE'`). Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  t = out['Core_DB.TERRITORY']
  us_state_ids = set(t[t.Territory_Type_Cd == 'STATE'].Territory_Id)
  iso_ids = set(out['Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD'].Territory_Id)
  orphan = iso_ids - us_state_ids
  assert not orphan, f'ISO_3166 subdivision orphan Territory_Ids: {orphan}'
  assert iso_ids <= us_state_ids, 'ISO subdivision should only cover US states'
  print('ISO_3166_COUNTRY_SUBDIVISION_STANDARD->TERRITORY FK OK')
  "
  ```
- [ ] Every `ISO_3166_COUNTRY_STANDARD.Country_Id` resolves. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  cids = set(out['Core_DB.COUNTRY'].Country_Id)
  iso_cids = set(out['Core_DB.ISO_3166_COUNTRY_STANDARD'].Country_Id)
  assert iso_cids <= cids, iso_cids - cids
  print('ISO_3166_COUNTRY_STANDARD->COUNTRY FK OK')
  "
  ```
- [ ] Every `GEOGRAPHICAL_AREA_CURRENCY.Currency_Cd` resolves to a Tier 0 `CURRENCY.Currency_Cd`. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  currency_cds = set(ctx.tables['Core_DB.CURRENCY'].Currency_Cd)
  gac_cds = set(out['Core_DB.GEOGRAPHICAL_AREA_CURRENCY'].Currency_Cd)
  orphan = gac_cds - currency_cds
  assert not orphan, f'GEOGRAPHICAL_AREA_CURRENCY orphan Currency_Cds: {orphan}'
  print('GEOGRAPHICAL_AREA_CURRENCY->CURRENCY FK OK')
  "
  ```

**Composite PK uniqueness (hand-authored risk):**

- [ ] `GEOGRAPHICAL_AREA_CURRENCY` has no duplicate `(Geographical_Area_Id, Currency_Cd)` composite-PK rows. Low-risk today (one row per area per the spec) but a seed-data edit that adds a second currency per area would silently violate the composite PK. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  df = out['Core_DB.GEOGRAPHICAL_AREA_CURRENCY']
  dups = df.duplicated(subset=['Geographical_Area_Id','Currency_Cd'])
  assert not dups.any(), df[dups]
  print('GEOGRAPHICAL_AREA_CURRENCY composite PK unique')
  "
  ```

**ISO 3166 literal-match constraint (item #19):**

- [ ] Every `ISO_3166_COUNTRY_SUBDIVISION_STANDARD.Territory_Standard_Type_Cd` row equals the exact string `'ISO 3166-2 Country Subdivision Standard'`. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  df = out['Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD']
  expected = 'ISO 3166-2 Country Subdivision Standard'
  assert (df.Territory_Standard_Type_Cd == expected).all(), \
      df.Territory_Standard_Type_Cd.value_counts()
  print('item #19 literal-match OK')
  "
  ```
- [ ] Fixed-width ISO 3166 CHAR columns are exactly DDL length — catches silent padding bugs like `'36'` instead of `'036'` for Australia. `ISO_3166_Country_3_Num` is CHAR(3); `ISO_3166_Country_Alpha_2_Cd` is CHAR(2); `ISO_3166_Country_Subdivision_Cd` is CHAR(3). Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  specs = [
      ('Core_DB.ISO_3166_COUNTRY_STANDARD', 'ISO_3166_Country_3_Num', 3),
      ('Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD', 'ISO_3166_Country_Alpha_2_Cd', 2),
      ('Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD', 'ISO_3166_Country_Subdivision_Cd', 3),
  ]
  bad = []
  for key, col, n in specs:
      vals = out[key][col].dropna()
      wrong = vals[vals.str.len() != n]
      if len(wrong): bad.append(f'{key}.{col}: expected CHAR({n}), got lengths {sorted(set(wrong.str.len()))}; samples {wrong.head(5).tolist()}')
  assert not bad, bad
  print('ISO 3166 CHAR lengths OK')
  "
  ```

**BIGINT ID column enforcement (PRD §7.1):**

- [ ] Every `*_Id` column in every Tier 1 DataFrame is a pandas `Int64`/`int64` dtype (not `object`, not plain Python int mixed with NaN). Run:
  ```bash
  python -c "
  import numpy as np, pandas as pd
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  bad = []
  for k, df in out.items():
      for col in df.columns:
          if col.endswith('_Id'):
              dtype = str(df[col].dtype)
              if dtype not in ('Int64','int64'):
                  bad.append(f'{k}.{col}: dtype={dtype}')
  assert not bad, bad
  print('all *_Id columns BIGINT')
  "
  ```

**DI stamping + DDL column order:**

- [ ] Every DataFrame has the full 5-column DI tail with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES, HIGH_TS
  from utils.id_factory import IdFactory
  from utils.di_columns import DI_COLUMN_ORDER
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  di = list(DI_COLUMN_ORDER)
  bad = []
  for k, df in out.items():
      tail = list(df.columns[-5:])
      if tail != di: bad.append(f'{k}: DI tail {tail} != {di}'); continue
      if not (df.di_end_ts == HIGH_TS).all(): bad.append(f'{k}: di_end_ts mismatch'); continue
      if not (df.di_rec_deleted_Ind == 'N').all(): bad.append(f'{k}: di_rec_deleted_Ind mismatch')
  assert not bad, bad
  print(f'{len(out)} Tier 1 tables pass DI stamping')
  "
  ```
- [ ] After stamping, every table passes `output.writer._reorder_to_ddl()`. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from output.writer import _reorder_to_ddl
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  ctx = Ctx(); ctx.tables.update(Tier0Lookups().generate(ctx))
  out = Tier1Geography().generate(ctx)
  for k, df in out.items():
      try: _reorder_to_ddl(df, k)
      except (ValueError, KeyError) as e: raise SystemExit(f'{k}: {e}')
  print(f'{len(out)} tables pass _reorder_to_ddl')
  "
  ```

**Tier 0 prerequisite guard:**

- [ ] `Tier1Geography.generate()` raises `RuntimeError` when a Tier 0 prerequisite is missing. Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier1_geography import Tier1Geography
  class Ctx:
      def __init__(self):
          self.ids = IdFactory(ID_RANGES)
          self.rng = np.random.default_rng(42); self.tables = {}
  try:
      Tier1Geography().generate(Ctx())
      raise AssertionError('should have raised RuntimeError for missing Tier 0')
  except RuntimeError as e:
      assert 'Tier 0' in str(e) or 'CURRENCY' in str(e) or 'CALENDAR' in str(e), str(e)
  print('prerequisite guard OK')
  "
  ```

**Reproducibility:**

- [ ] Two back-to-back runs with the same fresh context produce byte-identical DataFrames (same IDs, same row order). Run:
  ```bash
  python -c "
  import numpy as np
  from config.settings import ID_RANGES
  from utils.id_factory import IdFactory
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  def fresh():
      class C:
          def __init__(self):
              self.ids = IdFactory(ID_RANGES)
              self.rng = np.random.default_rng(42); self.tables = {}
      ctx = C(); ctx.tables.update(Tier0Lookups().generate(ctx))
      return Tier1Geography().generate(ctx)
  a = fresh(); b = fresh()
  assert set(a) == set(b)
  for k in a:
      assert a[k].equals(b[k]), f'{k} differs between runs'
  print('reproducibility OK')
  "
  ```

**No randomness, no import-time side effects:**

- [ ] `seed_data/geography_ref.py` does not import `numpy`, `faker`, `scipy`, `random`, or `secrets`. Run:
  ```bash
  python -c "
  import re, pathlib
  pat = re.compile(r'^\s*(?:import|from)\s+(numpy|faker|scipy|random|secrets)\b')
  bad = []
  for p in ('seed_data/geography_ref.py', 'generators/tier1_geography.py'):
      for i, line in enumerate(pathlib.Path(p).read_text().splitlines(), 1):
          if pat.match(line): bad.append(f'{p}:{i}: {line}')
  assert not bad, bad
  print('no randomness imports')
  "
  ```
- [ ] Importing `seed_data.geography_ref` or `generators.tier1_geography` does not build any DataFrames. Run:
  ```bash
  python -c "
  import importlib, sys, pandas as pd
  calls = {'n': 0}
  _orig = pd.DataFrame
  def _wrap(*a, **k):
      calls['n'] += 1
      return _orig(*a, **k)
  pd.DataFrame = _wrap
  for name in ('seed_data.geography_ref','generators.tier1_geography'):
      sys.modules.pop(name, None)
      importlib.import_module(name)
  pd.DataFrame = _orig
  assert calls['n'] == 0, f'{calls[\"n\"]} DataFrame(s) built at import time'
  print('no import-time DataFrames')
  "
  ```

**`config/settings.py` modification:**

- [ ] `ID_RANGES` contains the seven new geography categories with non-overlapping starts. Run:
  ```bash
  python -c "
  from config.settings import ID_RANGES
  needed = {'country','region','territory','county','city','postal_code','geographical_area'}
  assert needed <= set(ID_RANGES), needed - set(ID_RANGES)
  vals = list(ID_RANGES.values())
  assert len(vals) == len(set(vals)), 'duplicate ID_RANGES starts'
  print('ID_RANGES OK')
  "
  ```

### Universal checks

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else. Run:
  ```bash
  git status --porcelain
  ```
  Every line must map to one of: `config/settings.py` (modified), `seed_data/geography_ref.py` (new), `generators/tier1_geography.py` (new), plus this spec file at `.claude/specs/step-09-tier1-geography.md` (already present on the branch before the session). No stray files (no `__pycache__`, no output CSVs, no changes under `utils/`, `registry/`, `output/`, `references/`, other `seed_data/*.py`, other `generators/*.py`).
- [ ] All new files pass `python -c "import <module>"` — covered by the first check above.
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — covered by the BIGINT dtype check above. **n/a for the CSV-on-disk variant**: this step produces no CSVs; the writer is not invoked.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: not touched in this step.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSV output; writer not invoked.

## Handoff notes

### What shipped
- `seed_data/geography_ref.py` — 20 countries, 51 US states+DC, 11 foreign territories, 101 cities (50 US states covered), 22 counties, 6 geographical areas. All hand-authored, no IDs.
- `generators/tier1_geography.py` — `Tier1Geography(BaseGenerator)` producing all 10 Core_DB tables. Uses `_GEO_DI_START_TS = '2000-01-01 00:00:00.000000'` as a fixed `stamp_di()` start_ts to ensure reproducibility across runs.
- `config/settings.py` — 7 new ID_RANGES entries (country=700, region=800, territory=900, county=1_100, city=1_400, postal_code=1_600, geographical_area=1_900). Pre-existing duplicate (`address` and `claim` both at `1_000_000`) corrected: `claim` moved to `9_000_000`. No claim IDs had been minted, so no reproducibility impact.

### All 17 DoD checks pass
All exit criteria from the spec's Definition of done section executed and confirmed passing.

### Deferred items
None.

### Pre-existing bug fixed (not in spec scope)
`mvp-tool-design.md §8` lists both `address` and `claim` at `1_000_000`. This is a design doc transcription error — both categories using the same start would produce colliding IDs. Fixed by setting `claim: 9_000_000`. The design doc itself should be updated to reflect this.

### Next session hint
Step 10 (Tier 2 Core Entities) can start now. It depends on Step 4 (UniverseBuilder), Step 8 (Tier 0), and Step 9 (Tier 1 — now complete). The Tier1Geography tables are accessed via FK in Step 15 (Tier 5 Location) via `City_Id`, `Territory_Id`, `Postal_Code_Id`, and `Country_Id` — no changes to Tier 1 are expected before then.

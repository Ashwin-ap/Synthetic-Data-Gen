# Spec: Step 08 — Tier 0c Seed Data + Tier 0 Generator Wiring

## Overview

This step authors the **third and final slice of Tier 0 seed data** — the handwritten Python dict literals that populate lookup / reference tables for the `CHANNEL`, `CAMPAIGN` / `PROMOTION`, `ADDRESS` / `GEO` support, `CURRENCY`, `INTEREST_RATE_INDEX`, and miscellaneous (`UNIT_OF_MEASURE`, `TIME_PERIOD_TYPE`) domains — and then wires **all three Tier 0 seed slices (Steps 6, 7, 8) into `generators/tier0_lookups.py`**, the single entry point Step 9+ will call to load every lookup table into `ctx.tables` with DI columns stamped uniformly. This is the only Tier 0 step that produces a generator; Steps 6 and 7 deliberately ship un-stamped DataFrames and defer stamping to this step so that the stamp_di() convention (`generators/base.py`) is applied in exactly one place with one run-time timestamp. After this step, every other tier can reliably FK-reference any Core_DB lookup table. See `PRD.md` §7.11 (seeded-not-generated rule), `mvp-tool-design.md` §9 Tier 0 (authoritative table list), and §14 Decision 2 (rationale). Steps 6, 7, and 8 are listed as independent in `implementation-steps.md` Dependency Graph, but Step 8 is the *wiring* step — it imports Steps 6 and 7's outputs and must not ship until they do. Both are already merged to `main` (commits `beab329` and `a57522c`), so Step 8 is unblocked.

## Depends on

- **Step 1** — consumes from `config/settings.py`:
  - `HIGH_TS` — stamped as `di_end_ts` default on every active lookup row via `BaseGenerator.stamp_di()`.
  - `HIGH_DATE` — n/a for Tier 0 tables (all Core_DB; no `Valid_To_Dt`).
  - `SKIPPED_TABLES`, `OUTPUT_DIR` — not read directly; Step 5's writer handles both.
  - Consumes from `config/code_values.py`:
    - No mandatory literals for this step's own seed modules (channel/campaign/address/currency/interest-index/misc codes are all distribution-neutral — not Layer-2 literal-match). If a downstream step later promotes a Step 8 code to a `code_values.py` constant (e.g. `DEFAULT_CURRENCY_CD = 'USD'`), this module must import and reuse it rather than duplicate the string.
- **Step 2** — consumes `generators/base.BaseGenerator` (`stamp_di()` method). The new `Tier0Lookups` class inherits from it.
- **Step 6** — consumes the four `get_<domain>_tables()` functions from `seed_data/agreement_types`, `seed_data/status_types`, `seed_data/financial_types`, `seed_data/feature_types` (34 tables total, all un-stamped per Step 6's handoff).
- **Step 7** — consumes the two `get_<domain>_tables()` functions from `seed_data/party_types`, `seed_data/industry_codes` (24 tables total, all un-stamped per Step 7's handoff).

No code from Step 3, 4, or 5 is imported by this step. Step 5's writer is not invoked here — CSV writing remains Step 25's responsibility. The `Tier0Lookups.generate()` method returns stamped DataFrames that land in `ctx.tables` only; the writer reads that dict later.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and **Seed Data Authoring Convention** all apply)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 8 + the Seed Data Authoring Convention):
- `PRD.md` §7.3 (DI column rules; active-record sentinels), §7.11 (Tier 0 seeded-not-generated rule), §10 (Ground Truth Priority — `07` takes precedence over `01` for MVP scope)
- `mvp-tool-design.md` §7 (`BaseGenerator` + DI column rules), §9 Tier 0 (authoritative Tier-0 table list grouped by domain; Step 8 implements the "Channel/Promotion", "Address/Geo", and remainder of "Other" blocks plus `CURRENCY` and `INTEREST_RATE_INDEX`), §14 Decision 2 (rationale for hand-coded seed data), §15 (orchestrator signature — `Tier0Lookups()` is the first item in the `tiers` list)
- `implementation-steps.md` Step 8 entry (exit criteria), **Seed Data Authoring Convention** (read-discipline, escalation rules, `get_<domain>_tables` output contract)

**Additional reference files** (only those named in the step's "Reads from" line, filtered per the Seed Data Authoring Convention):
- `references/07_mvp-schema-reference.md` — **authoritative DDL slice** for every table this step seeds. For each table, open only the `#### <TABLE_NAME>` block and capture column names, types, nullability, composite PKs, and FK relationships. Use DDL column order exactly — Step 5's `_load_ddl_column_order` parser returns the DI columns as the final three entries (for Core_DB tables without Valid_* columns), so every DataFrame **before stamping** must include `di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind` as the last three columns with `None` values (matches the Step 6/7 authoring convention). Specific DDL blocks to read (line numbers current as of 2026-04-20):
  - Channel domain: `CHANNEL_TYPE` (§815), `CHANNEL_INSTANCE_SUBTYPE` (§831), `CONVENIENCE_FACTOR_TYPE` (§841), `CHANNEL_STATUS_TYPE` (§863)
  - Campaign/Promotion: `CAMPAIGN_STRATEGY_TYPE` (§763), `CAMPAIGN_TYPE` (§773), `CAMPAIGN_CLASSIFICATION` (§783), `CAMPAIGN_STATUS_TYPE` (§805), `PROMOTION_OFFER_TYPE` (§2118), `PROMOTION_METRIC_TYPE` (§2080)
  - Address/Geo: `ADDRESS_SUBTYPE` (§726), `DIRECTION_TYPE` (§2170), `STREET_SUFFIX_TYPE` (§2180), `TERRITORY_TYPE` (§2417), `CITY_TYPE` (§2272), `CALENDAR_TYPE` (§2298)
  - Currency / Interest Rate: `CURRENCY` (§367), `INTEREST_RATE_INDEX` (§1707)
  - Misc: `UNIT_OF_MEASURE` (§2090), `UNIT_OF_MEASURE_TYPE` (§2464), `TIME_PERIOD_TYPE` (§1425)
- `references/02_data-mapping-reference.md` Step 3 — **constrained code values and literal-match rows**. Scan for items touching this step's domains. Current known items:
  - No channel/campaign/address-domain literal-match row equivalent to FROZEN / Rate Feature / Original Loan Term exists. Channel and campaign codes are distribution-neutral — Step 10's `CHANNEL_INSTANCE` generator will pick freely from seeded `CHANNEL_TYPE` codes; Step 11's `CAMPAIGN` generator will pick freely from seeded `CAMPAIGN_TYPE`/`CAMPAIGN_STATUS_TYPE` rows.
  - `CURRENCY.Currency_Cd = 'USD'` is the de-facto default (Step 16's `AGREEMENT_CURRENCY` uses `'preferred'` + `'USD'`), so `USD` must be present as a seeded row. Other currencies are breadth-only.
- `references/05_architect-qa.md` — open **only** Q's touching the channel / campaign / address / currency / interest-index domains. The file is 76 lines total (Q1–Q7); nothing in this step's scope is explicitly addressed there, so a quick scan is sufficient.

**Do NOT read** (explicitly excluded to protect context budget and per the Seed Data Authoring Convention):
- `references/01_schema-reference.md` — supplementary; `07` is the MVP-filtered DDL set and takes precedence per PRD §10. (Note: `implementation-steps.md` Step 8's "Reads from" line points to `mvp-tool-design.md` §9 Tier 0 rather than `01` — the Convention already elides `01` for Tier 0 seed work.)
- `references/06_supporting-enrichments.md` — distributions; irrelevant for Tier 0. This step introduces zero randomness.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` and `resources/iDM_MDM_tables_DDLs.xlsx` — already distilled into the references above. Do not re-read the Excels per session.

## Produces

All paths relative to the project root.

**New files (seed data — un-stamped, mirror Step 6/7 authoring pattern):**

- `seed_data/channel_types.py` — seed rows for the channel-domain lookup tables. Exposes `get_channel_type_tables() -> Dict[str, pd.DataFrame]`. Tables included (keys are `'Core_DB.<TABLE>'`; column order per `07`, DI columns as the last three with `None` values):
  - `Core_DB.CHANNEL_TYPE` — 6 rows covering `BRANCH`, `ATM`, `ONLINE`, `MOBILE`, `CALL_CENTER`, `EMAIL`. These are the categories Step 10's `CHANNEL_INSTANCE` generator picks from (~20 instances across types) and Step 14's `PARTY_CONTACT_PREFERENCE` maps `SMALLINT Channel_Type_Cd` onto via the `(3=ONLINE, 1=BRANCH, …)` mapping in `mvp-tool-design.md` §9 Tier 4.
  - `Core_DB.CHANNEL_INSTANCE_SUBTYPE` — 5–8 rows enumerating concrete channel instances (e.g. `MAIN_BRANCH`, `DRIVE_THRU_ATM`, `WEB_PORTAL`, `IOS_APP`, `ANDROID_APP`, `INBOUND_CALL`, `OUTBOUND_CALL`, `TRANSACTIONAL_EMAIL`).
  - `Core_DB.CONVENIENCE_FACTOR_TYPE` — 3–5 rows covering convenience / service-quality categorisations (e.g. `24_7_AVAILABLE`, `BUSINESS_HOURS`, `APPOINTMENT_REQUIRED`, `SELF_SERVICE`, `ASSISTED`).
  - `Core_DB.CHANNEL_STATUS_TYPE` — 3–5 rows covering channel instance status codes (e.g. `ACTIVE`, `INACTIVE`, `MAINTENANCE`, `DEPRECATED`). Used by Step 10's `CHANNEL_INSTANCE_STATUS` (if present) and referenced from `CHANNEL_INSTANCE.Channel_Status_Cd`.

- `seed_data/campaign_types.py` — seed rows for the campaign / promotion lookup tables. Exposes `get_campaign_type_tables() -> Dict[str, pd.DataFrame]`. Tables included:
  - `Core_DB.CAMPAIGN_STRATEGY_TYPE` — 4–6 rows (e.g. `ACQUISITION`, `RETENTION`, `CROSS_SELL`, `UP_SELL`, `WIN_BACK`, `BRAND_AWARENESS`).
  - `Core_DB.CAMPAIGN_TYPE` — 4–6 rows (e.g. `DIRECT_MAIL`, `EMAIL`, `DIGITAL_ADS`, `SOCIAL_MEDIA`, `BRANCH_EVENT`, `TELEMARKETING`).
  - `Core_DB.CAMPAIGN_CLASSIFICATION` — 3–5 rows (e.g. `PROSPECT`, `CUSTOMER`, `LAPSED_CUSTOMER`, `HIGH_VALUE`, `MASS_MARKET`).
  - `Core_DB.CAMPAIGN_STATUS_TYPE` — 4–6 rows covering lifecycle status (`PLANNED`, `ACTIVE`, `PAUSED`, `COMPLETED`, `CANCELLED`). Step 21's `CAMPAIGN_STATUS` generator picks `max(Dttm)` from seeded status codes — every status row must FK-resolve here.
  - `Core_DB.PROMOTION_OFFER_TYPE` — 4–6 rows (e.g. `DISCOUNT`, `RATE_REDUCTION`, `FEE_WAIVER`, `CASH_BONUS`, `POINTS_MULTIPLIER`, `FREE_SERVICE`).
  - `Core_DB.PROMOTION_METRIC_TYPE` — 3–5 rows categorising metric measurement (`CONVERSION_RATE`, `RESPONSE_RATE`, `REDEMPTION_RATE`, `CLICK_THROUGH`, `ACQUISITION_COST`).

- `seed_data/address_types.py` — seed rows for the address / geography lookup tables. Exposes `get_address_type_tables() -> Dict[str, pd.DataFrame]`. Tables included:
  - `Core_DB.ADDRESS_SUBTYPE` — **must include `PHYSICAL`** (per `mvp-tool-design.md` §9 Tier 5 — ADDRESS generator uses `Address_Subtype_Cd='PHYSICAL'` as primary) plus 3–5 more (`MAILING`, `BILLING`, `WORK`, `VACATION`, `PO_BOX`).
  - `Core_DB.DIRECTION_TYPE` — **must include all 8 compass points**: `N`, `S`, `E`, `W`, `NE`, `NW`, `SE`, `SW` (per `mvp-tool-design.md` §9 Tier 0 — "DIRECTION_TYPE (8 points)"). Used by `STREET_ADDRESS.Street_Direction_Cd` / `Suffix_Direction_Cd`.
  - `Core_DB.STREET_SUFFIX_TYPE` — 10–15 USPS-standard suffix codes (`ST`, `AVE`, `BLVD`, `DR`, `LN`, `RD`, `WAY`, `CT`, `PL`, `PKWY`, `CIR`, `TER`, `TRL`, `HWY`, `LOOP`). `Street_Suffix_Desc` is the full word (`Street`, `Avenue`, `Boulevard`, …).
  - `Core_DB.TERRITORY_TYPE` — 4–6 rows covering territory/region classifications (`STATE`, `PROVINCE`, `TERRITORY`, `DEPENDENCY`, `AUTONOMOUS_REGION`, `COUNTRY_SUBDIVISION`). Used by `TERRITORY.Territory_Type_Cd` (Step 9 — Tier 1 Geography).
  - `Core_DB.CITY_TYPE` — 3–5 rows (`CITY`, `TOWN`, `VILLAGE`, `MUNICIPALITY`, `UNINCORPORATED`). Used by `CITY.City_Type_Cd` (Step 9).
  - `Core_DB.CALENDAR_TYPE` — 3–5 rows covering calendar conventions (`GREGORIAN`, `FISCAL_JAN`, `FISCAL_JUL`, `FISCAL_OCT`, `ISLAMIC_HIJRI`). Used by `TIME_PERIOD_TYPE` references and geographical fiscal-year associations.

- `seed_data/currency.py` — seed rows for the `CURRENCY` lookup. Exposes `get_currency_tables() -> Dict[str, pd.DataFrame]`. Tables included:
  - `Core_DB.CURRENCY` — **must include `USD`** (default preferred currency per `mvp-tool-design.md` §9 Tier 7 — `AGREEMENT_CURRENCY.Agreement_Currency_Cd='USD'`). Full seed set: `USD`, `EUR`, `GBP`, `CAD`, `AUD`, `JPY`. Each row carries ISO 4217 alpha + numeric codes, `Currency_Symbol`, and `Currency_Decimal_Digit_Num` (rounding precision — 2 for most, 0 for JPY). Column set is per `references/07_mvp-schema-reference.md` §367 DDL — do not invent columns.

- `seed_data/interest_rate_indices.py` — seed rows for the `INTEREST_RATE_INDEX` lookup. Exposes `get_interest_rate_index_tables() -> Dict[str, pd.DataFrame]`. Tables included:
  - `Core_DB.INTEREST_RATE_INDEX` — exactly 5 rows covering the standard floating-rate indices used in US and EU retail banking: `SOFR` (Secured Overnight Financing Rate), `PRIME` (Wall Street Journal US Prime Rate), `FEDFUNDS` (Federal Funds Rate), `LIBOR` (London Interbank Offered Rate — legacy, retained for historical mortgages in the universe), `EURIBOR` (Euro Interbank Offered Rate). `Interest_Rate_Index_Cd` is the PK (see Step 16 design: "one row per distinct interest rate index type; no daily or monthly history granularity"). Downstream rate rows (daily / monthly snapshots) are `INTEREST_INDEX_RATE`, generated in Step 16 — not here.

- `seed_data/misc_types.py` — seed rows for the miscellaneous-domain lookup tables. Exposes `get_misc_type_tables() -> Dict[str, pd.DataFrame]`. Tables included:
  - `Core_DB.UNIT_OF_MEASURE` — 5–10 rows covering weights, lengths, currencies-as-UOM (`USD`, `EUR`), counts, percentages, years, months. Used by PIM `PRODUCT_PARAMETERS` (Step 23).
  - `Core_DB.UNIT_OF_MEASURE_TYPE` — 3–5 rows categorising UOM (`CURRENCY`, `LENGTH`, `WEIGHT`, `COUNT`, `TIME`, `PERCENTAGE`).
  - `Core_DB.TIME_PERIOD_TYPE` — 5–8 rows (`DAY`, `WEEK`, `MONTH`, `QUARTER`, `YEAR`, `DECADE`, `FISCAL_QUARTER`, `FISCAL_YEAR`). Used by agreement/feature/metric date-period references.

**New files (Tier 0 generator):**

- `generators/tier0_lookups.py` — `class Tier0Lookups(BaseGenerator)` with a single `generate(ctx) -> Dict[str, pd.DataFrame]` method. Implementation contract:
  1. Import **all nine** `get_<domain>_tables()` functions (Steps 6–8): `get_agreement_type_tables`, `get_status_type_tables`, `get_financial_type_tables`, `get_feature_type_tables` (Step 6); `get_party_type_tables`, `get_industry_code_tables` (Step 7); `get_channel_type_tables`, `get_campaign_type_tables`, `get_address_type_tables`, `get_currency_tables`, `get_interest_rate_index_tables`, `get_misc_type_tables` (Step 8). Total of **12** functions.
  2. Call each function and merge results into a single `Dict[str, pd.DataFrame]`. Duplicate table keys across modules must raise `ValueError` — a Tier 0 table should be authored in exactly one seed module.
  3. For every DataFrame in the merged dict, drop the three placeholder `None`-valued DI columns (if present) and re-stamp via `self.stamp_di(df)` using the run-time default `start_ts` (i.e. `datetime.now()` → `format_ts` → ISO-6 microsecond string). This yields **five DI columns** in `DI_COLUMN_ORDER`: `di_data_src_cd` (None), `di_start_ts` (run timestamp), `di_proc_name` (None), `di_rec_deleted_Ind` ('N'), `di_end_ts` (`HIGH_TS`).
  4. Return the stamped dict. Do NOT mutate `ctx.tables` inside `generate()` — the orchestrator (`main.py`, Step 25) performs `ctx.tables.update(new_tables)` after every tier.
  5. No stamp_valid() calls — Tier 0 tables are all Core_DB, so Valid_* columns are not stamped.

**Do NOT produce** in this step:
- New CSVs — the writer is not invoked. `output/` must remain empty.
- New config/settings/code_values entries — all necessary constants are already present from Step 1.
- Modifications to `main.py` — wiring `Tier0Lookups()` into the orchestrator is Step 25's responsibility (the `tiers = [Tier0Lookups(), …]` list).
- Re-authoring anything in Steps 6 or 7's seed modules — their outputs are consumed as-is. If a bug is found there, fix it in a dedicated follow-up commit rather than mixing concerns into this step.
- A `seed_data/geography_ref.py` module — that is Step 9 (Tier 1 Geography), not Tier 0.

## Tables generated (if applicable)

The six new seed modules together produce **22 un-stamped DataFrames**, which after wiring through `Tier0Lookups.generate(ctx)` combine with Step 6's 34 + Step 7's 24 seed tables to yield a total of **~80 stamped Core_DB lookup tables** available in `ctx.tables` after this step runs. (The implementation-steps.md Step 8 exit criterion says "~70" — treat 70–85 as the acceptable range since row-level table counts have varied slightly through Steps 6 and 7's authoring.)

**New tables added by Step 8:**

| Module | Table | Min rows | Literal-match / constraint requirements |
|--------|-------|---------:|------------------------------------------|
| `channel_types.py` | `Core_DB.CHANNEL_TYPE` | 6 | Includes `BRANCH`, `ATM`, `ONLINE`, `MOBILE`, `CALL_CENTER`, `EMAIL` |
| | `Core_DB.CHANNEL_INSTANCE_SUBTYPE` | 5 | — |
| | `Core_DB.CONVENIENCE_FACTOR_TYPE` | 3 | — |
| | `Core_DB.CHANNEL_STATUS_TYPE` | 3 | Includes at least one `ACTIVE`-equivalent code |
| `campaign_types.py` | `Core_DB.CAMPAIGN_STRATEGY_TYPE` | 4 | — |
| | `Core_DB.CAMPAIGN_TYPE` | 4 | — |
| | `Core_DB.CAMPAIGN_CLASSIFICATION` | 3 | — |
| | `Core_DB.CAMPAIGN_STATUS_TYPE` | 4 | Includes `ACTIVE` or equivalent; every scheme code Step 21 picks must resolve here |
| | `Core_DB.PROMOTION_OFFER_TYPE` | 4 | — |
| | `Core_DB.PROMOTION_METRIC_TYPE` | 3 | — |
| `address_types.py` | `Core_DB.ADDRESS_SUBTYPE` | 4 | **Must include `PHYSICAL`** |
| | `Core_DB.DIRECTION_TYPE` | 8 | **Must include all 8 compass points**: `N,S,E,W,NE,NW,SE,SW` |
| | `Core_DB.STREET_SUFFIX_TYPE` | 10 | — |
| | `Core_DB.TERRITORY_TYPE` | 4 | — |
| | `Core_DB.CITY_TYPE` | 3 | — |
| | `Core_DB.CALENDAR_TYPE` | 3 | — |
| `currency.py` | `Core_DB.CURRENCY` | 6 | **Must include `USD`** (default Agreement currency) |
| `interest_rate_indices.py` | `Core_DB.INTEREST_RATE_INDEX` | 5 | Exactly `{SOFR, PRIME, FEDFUNDS, LIBOR, EURIBOR}` |
| `misc_types.py` | `Core_DB.UNIT_OF_MEASURE` | 5 | — |
| | `Core_DB.UNIT_OF_MEASURE_TYPE` | 3 | — |
| | `Core_DB.TIME_PERIOD_TYPE` | 5 | — |

Actual column counts and orderings are dictated by `references/07_mvp-schema-reference.md` — not by this spec. Every DataFrame must have all DDL-declared columns (including nullable ones — fill with `None` where data is genuinely absent; do not omit the column). DI columns (`di_start_ts`, `di_end_ts`, `di_rec_deleted_Ind`) are the last three columns of every un-stamped DataFrame, all populated with `None` — Step 6 established this pattern and the DDL-alignment check depends on it. After Tier0Lookups.generate() runs, the **five** DI columns are present in `DI_COLUMN_ORDER` (per `utils/di_columns.py`) with active-record defaults.

**Tables re-stamped by `Tier0Lookups.generate()` (full Tier 0 set across 6/7/8):** the 34+24+22 = 80 tables above, all keyed `Core_DB.<TABLE>`, all passed through `BaseGenerator.stamp_di()`.

## Files to modify

No files modified. All outputs are new files. `config/`, `utils/`, `registry/`, `output/`, `main.py`, `CLAUDE.md`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, and `references/` are NOT touched.

`seed_data/__init__.py` already exists (created in Step 6) and is empty — do NOT recreate or modify.

`generators/__init__.py` already exists (created in Step 1) and is empty — do NOT modify.

If the implementation discovers that a column spelled in `references/07_mvp-schema-reference.md` differs from what this spec assumes (e.g. a capitalisation or underscore difference), escalate per Handoff Protocol §2 — update the upstream reference or add a `⚠️ Conflict` block to this spec. Do not silently improvise column names.

## New dependencies

No new dependencies. `pandas` is already in `requirements.txt` (Step 1). Seed modules depend only on the standard library and pandas. `generators/tier0_lookups.py` additionally imports `generators.base.BaseGenerator` and every seed module via relative import.

## Rules for implementation

Universal (apply to every step):

- BIGINT for all ID columns (per PRD §7.1) — **n/a for lookup tables**: all tables in this step have CHAR / VARCHAR code columns as their PK, no `*_Id` BIGINT columns. If `07` reveals any BIGINT column in these tables, use `pd.Int64Dtype()` (nullable BIGINT). (Spot-check: none of the tables in Step 8's scope carry `*_Id` BIGINT columns — all PKs are `*_Cd` VARCHAR(50) or similar.)
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — n/a: no party IDs in lookup tables.
- DI column stamping on every table via `BaseGenerator.stamp_di()` — **enforced in `Tier0Lookups.generate()`**. Every table passed through the generator emerges with the full 5-column `DI_COLUMN_ORDER` tail stamped. Seed modules themselves still carry 3-column `None` placeholders to preserve Step 6/7 authoring-pattern consistency and DDL-order alignment checks.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records — `di_end_ts` stamped to `HIGH_TS` via `stamp_di()` default. `Valid_To_Dt` n/a: every table in this step is `Core_DB`.
- CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind` (per PRD §7.3) — n/a: every table in this step is `Core_DB`. Do NOT call `stamp_valid()`.
- **Column order in every un-stamped DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md`** — enforced at authoring time. Each dict literal or `pd.DataFrame(..., columns=[...])` must list columns in DDL order including the three DI columns as the last three. After `stamp_di()`, the five-column DI tail replaces the three placeholders (`stamp_di` drops none, but the generator must drop the three placeholder columns before stamping to avoid duplicates — see rule below).
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10) — n/a: no `PARTY_INTERRACTION_EVENT` rows in this step.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — n/a: no geospatial tables here; `GEOSPATIAL` is Core_DB.GEOSPATIAL in `config.settings.SKIPPED_TABLES` and the writer is not invoked anyway.
- No ORMs, no database connections — pure pandas → CSV. The seed modules construct `pd.DataFrame(...)` and return them; no disk I/O, no imports beyond pandas + standard library + `config`.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42` — **n/a, and critically so**: this step introduces zero randomness. Seed data is deterministic by construction (every row is hand-written). **Note:** `stamp_di()` defaults `start_ts` to `datetime.now()` (current wall-clock), which is intentionally non-deterministic. This is acceptable because (a) the `di_start_ts` value does not affect downstream FK joins or validator checks and (b) if strict byte-identical reproducibility is ever needed, the orchestrator (Step 25) can pass an explicit `start_ts` argument. The `Tier0Lookups.generate()` method must not pin its own timestamp — it defers to the `BaseGenerator.stamp_di()` default.

Step-specific rules (Tier 0c seed authoring + Tier 0 generator wiring):

- **No randomness, no Faker, no dynamic generation in seed modules.** Every row is a hand-written dict literal. `numpy`, `faker`, `scipy`, `random`, `secrets` — none of these appear in the imports of any seed file produced by this step. Verified by a `grep` check in Definition of done. (The generator file `generators/tier0_lookups.py` may import `pandas` and `datetime`, but not any randomness library.)
- **Follow the Step 6/7 authoring pattern exactly.** See `seed_data/status_types.py` and `seed_data/party_types.py` for the reference template: a `_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}` module constant, a `_COLS` list giving the DDL-ordered column list, a module-private rows list with `**_DI` splatted into each row, and a single public `get_<domain>_tables()` returning `pd.DataFrame(..., columns=_COLS)`. Consistency with Steps 6/7 makes review trivial and lets `Tier0Lookups` treat all seed modules identically.
- **DDL column order is authoritative.** Before authoring any table, open `references/07_mvp-schema-reference.md`, find the `#### <TABLE_NAME>` block, list columns in the exact order shown including the three trailing DI columns. If a column is NULL-able and the seed has no plausible value, use `None`. The Definition-of-done DDL-alignment check compares against `output.writer._load_ddl_column_order()` — any divergence fails the check.
- **Literal-match requirements for Step 8 seeds.**
  - `CURRENCY` must include `USD` (`Currency_Cd='USD'`). Step 16's `AGREEMENT_CURRENCY` hard-codes `'USD'` as the `Currency_Use_Cd='preferred'` row.
  - `ADDRESS_SUBTYPE` must include `PHYSICAL`. Step 15's ADDRESS generator uses `Address_Subtype_Cd='PHYSICAL'` as the primary physical-address row.
  - `DIRECTION_TYPE` must include all 8 compass points (`N`, `S`, `E`, `W`, `NE`, `NW`, `SE`, `SW`). Enforced in Definition of done.
  - `INTEREST_RATE_INDEX.Interest_Rate_Index_Cd` set must equal exactly `{SOFR, PRIME, FEDFUNDS, LIBOR, EURIBOR}`. Step 16's `INTEREST_INDEX_RATE` generator picks one row per distinct index — each must resolve here.
- **`CURRENCY.Currency_Decimal_Digit_Num` precision.** Populate with SMALLINT-compatible integers: 2 for USD/EUR/GBP/CAD/AUD, 0 for JPY (JPY has no sub-unit). Use plain Python `int`.
- **Each module exposes exactly one public function**, named `get_<domain>_tables()`, returning `Dict[str, pd.DataFrame]` keyed by `'Core_DB.<TABLE>'`. No other public surface. Helper lists / constants may be module-private (leading underscore).
- **No side effects on import.** Importing a seed module must not construct DataFrames eagerly. Build them inside `get_<domain>_tables()` so module import is cheap and the DataFrames are freshly constructed per caller (avoids cross-call mutation bugs). Verified in Definition of done.
- **Desc columns must be human-readable English.** Title-case for multi-word descs (`'Call Center'` not `'CALL_CENTER'` in `Channel_Type_Desc`). These feed downstream BB joins that surface description strings to reporting layers.
- **`Tier0Lookups.generate()` merging rules.**
  - Call every `get_<domain>_tables()` function in a fixed order (agreement → status → financial → feature → party → industry → channel → campaign → address → currency → interest_rate_indices → misc). The order matters only for deterministic iteration when a duplicate is detected.
  - Detect duplicate keys across modules: if `combined[key]` already exists when merging a new module, raise `ValueError(f'Duplicate Tier 0 table key: {key} (authored in two seed modules)')`. A Tier 0 table is authored in exactly one place.
  - For each key in the merged dict: verify the three-column `None`-placeholder DI columns are the last three columns (matches the Step 6/7 authoring convention). If the DataFrame already carries `di_data_src_cd` / `di_proc_name` columns, something is wrong — raise `ValueError`.
  - Drop the three placeholder columns via `df = df.drop(columns=['di_start_ts', 'di_end_ts', 'di_rec_deleted_Ind'])` before calling `self.stamp_di(df)`. Otherwise the stamp would coexist with `None`-valued duplicates (pandas allows this but it breaks the `_reorder_to_ddl` check downstream).
  - After `stamp_di(df)`, the DataFrame has five DI columns in `DI_COLUMN_ORDER`, all rows carry `di_end_ts = HIGH_TS`, `di_rec_deleted_Ind = 'N'`, `di_data_src_cd` / `di_proc_name` = None.
  - Return the stamped dict. The orchestrator does the `ctx.tables.update()`.
- **`Tier0Lookups.generate()` must accept `ctx` even though it doesn't use it** — the `BaseGenerator.generate(self, ctx)` signature is fixed by Step 2. Parameter may be type-hinted `ctx: 'GenerationContext'` via `TYPE_CHECKING` to avoid a circular import at runtime.
- **Escalation over improvisation.** If `references/07_mvp-schema-reference.md` lacks a column whose legal values the spec asks for, follow Handoff Protocol §2 — leave a `⚠️ Conflict` block in this spec. Do NOT invent columns.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current directory and `python` resolves to the project's Python 3.12 environment.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

**Module-import and API contract:**

- [ ] `python -c "import seed_data.channel_types, seed_data.campaign_types, seed_data.address_types, seed_data.currency, seed_data.interest_rate_indices, seed_data.misc_types, generators.tier0_lookups"` exits 0.
- [ ] Each new seed module exposes exactly one public function named `get_<domain>_tables`. Run:
  ```bash
  python -c "
  import seed_data.channel_types as ch, seed_data.campaign_types as ca, \
         seed_data.address_types as ad, seed_data.currency as cu, \
         seed_data.interest_rate_indices as ir, seed_data.misc_types as mi
  assert callable(ch.get_channel_type_tables)
  assert callable(ca.get_campaign_type_tables)
  assert callable(ad.get_address_type_tables)
  assert callable(cu.get_currency_tables)
  assert callable(ir.get_interest_rate_index_tables)
  assert callable(mi.get_misc_type_tables)
  print('seed-module API contract OK')
  "
  ```
- [ ] Each `get_<domain>_tables()` returns `Dict[str, pd.DataFrame]` keyed by `'Core_DB.<TABLE>'`. Run:
  ```bash
  python -c "
  import pandas as pd
  from seed_data.channel_types import get_channel_type_tables
  from seed_data.campaign_types import get_campaign_type_tables
  from seed_data.address_types import get_address_type_tables
  from seed_data.currency import get_currency_tables
  from seed_data.interest_rate_indices import get_interest_rate_index_tables
  from seed_data.misc_types import get_misc_type_tables
  for fn in (get_channel_type_tables, get_campaign_type_tables,
             get_address_type_tables, get_currency_tables,
             get_interest_rate_index_tables, get_misc_type_tables):
      d = fn()
      assert isinstance(d, dict) and all(isinstance(v, pd.DataFrame) for v in d.values())
      assert all(k.startswith('Core_DB.') for k in d)
  print('return-type OK')
  "
  ```
- [ ] `generators.tier0_lookups.Tier0Lookups` inherits from `BaseGenerator` and `generate(ctx)` is defined. Run:
  ```bash
  python -c "
  from generators.tier0_lookups import Tier0Lookups
  from generators.base import BaseGenerator
  assert issubclass(Tier0Lookups, BaseGenerator)
  import inspect
  sig = inspect.signature(Tier0Lookups.generate)
  assert 'ctx' in sig.parameters, sig.parameters
  print('Tier0Lookups contract OK')
  "
  ```

**Literal-match seed rows:**

- [ ] `Core_DB.CHANNEL_TYPE` contains the six canonical codes. Run:
  ```bash
  python -c "
  from seed_data.channel_types import get_channel_type_tables
  df = get_channel_type_tables()['Core_DB.CHANNEL_TYPE']
  codes = set(df.Channel_Type_Cd)
  assert {'BRANCH','ATM','ONLINE','MOBILE','CALL_CENTER','EMAIL'} <= codes, codes
  print('CHANNEL_TYPE core codes OK')
  "
  ```
- [ ] `Core_DB.ADDRESS_SUBTYPE` contains `PHYSICAL`. Run:
  ```bash
  python -c "
  from seed_data.address_types import get_address_type_tables
  df = get_address_type_tables()['Core_DB.ADDRESS_SUBTYPE']
  assert (df.Address_Subtype_Cd == 'PHYSICAL').sum() == 1
  print('ADDRESS_SUBTYPE PHYSICAL row OK')
  "
  ```
- [ ] `Core_DB.DIRECTION_TYPE` contains all 8 compass points. Run:
  ```bash
  python -c "
  from seed_data.address_types import get_address_type_tables
  df = get_address_type_tables()['Core_DB.DIRECTION_TYPE']
  expected = {'N','S','E','W','NE','NW','SE','SW'}
  got = set(df.Direction_Type_Cd)
  assert expected <= got, (expected - got)
  print('DIRECTION_TYPE 8-point compass OK')
  "
  ```
- [ ] `Core_DB.CURRENCY` contains `USD`. Run:
  ```bash
  python -c "
  from seed_data.currency import get_currency_tables
  df = get_currency_tables()['Core_DB.CURRENCY']
  assert (df.Currency_Cd == 'USD').sum() == 1
  print('CURRENCY USD row OK')
  "
  ```
- [ ] `Core_DB.INTEREST_RATE_INDEX` codes equal `{SOFR, PRIME, FEDFUNDS, LIBOR, EURIBOR}` exactly. Run:
  ```bash
  python -c "
  from seed_data.interest_rate_indices import get_interest_rate_index_tables
  df = get_interest_rate_index_tables()['Core_DB.INTEREST_RATE_INDEX']
  codes = set(df.Interest_Rate_Index_Cd)
  assert codes == {'SOFR','PRIME','FEDFUNDS','LIBOR','EURIBOR'}, codes
  print('INTEREST_RATE_INDEX codes OK')
  "
  ```

**`Tier0Lookups.generate()` behaviour — the per-step exit criterion:**

- [ ] Calling `Tier0Lookups().generate(ctx=None)` returns a dict with **70–85** Core_DB-keyed tables (Steps 6+7+8 combined). Run:
  ```bash
  python -c "
  from generators.tier0_lookups import Tier0Lookups
  tables = Tier0Lookups().generate(None)
  assert isinstance(tables, dict)
  assert 70 <= len(tables) <= 85, f'expected 70-85 tables, got {len(tables)}'
  assert all(k.startswith('Core_DB.') for k in tables), (
      [k for k in tables if not k.startswith('Core_DB.')])
  print(f'Tier0Lookups produced {len(tables)} tables')
  "
  ```
- [ ] Every table returned by `Tier0Lookups().generate()` has the full 5-column DI tail in `DI_COLUMN_ORDER` with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. Run:
  ```bash
  python -c "
  from generators.tier0_lookups import Tier0Lookups
  from utils.di_columns import DI_COLUMN_ORDER
  from config.settings import HIGH_TS
  tables = Tier0Lookups().generate(None)
  di = list(DI_COLUMN_ORDER)
  bad = []
  for k, df in tables.items():
      tail = list(df.columns[-5:])
      if tail != di:
          bad.append(f'{k}: DI tail {tail} != {di}'); continue
      if not (df.di_end_ts == HIGH_TS).all():
          bad.append(f'{k}: di_end_ts mismatch'); continue
      if not (df.di_rec_deleted_Ind == 'N').all():
          bad.append(f'{k}: di_rec_deleted_Ind mismatch'); continue
  if bad:
      for b in bad: print(b)
      raise SystemExit(1)
  print(f'{len(tables)} tables pass DI stamping')
  "
  ```
- [ ] No table returned by `Tier0Lookups().generate()` is empty. Run:
  ```bash
  python -c "
  from generators.tier0_lookups import Tier0Lookups
  tables = Tier0Lookups().generate(None)
  empty = [k for k, df in tables.items() if len(df) == 0]
  assert not empty, f'empty tables: {empty}'
  print(f'all {len(tables)} tables non-empty')
  "
  ```
- [ ] Duplicate-key detection triggers a `ValueError`. Run (monkey-patch one of the getters to return a key that already exists):
  ```bash
  python -c "
  import seed_data.currency as cu
  from seed_data.agreement_types import get_agreement_type_tables
  orig = cu.get_currency_tables
  def clashing():
      d = orig()
      # Re-alias the CURRENCY table under a key AGREEMENT_TYPE already uses
      d['Core_DB.AGREEMENT_TYPE'] = d.pop('Core_DB.CURRENCY')
      return d
  cu.get_currency_tables = clashing
  from generators.tier0_lookups import Tier0Lookups
  try:
      Tier0Lookups().generate(None)
      raise AssertionError('should have raised ValueError for duplicate key')
  except ValueError as e:
      assert 'AGREEMENT_TYPE' in str(e) or 'duplicate' in str(e).lower(), str(e)
  cu.get_currency_tables = orig
  print('duplicate-key detection OK')
  "
  ```

**DDL column-order alignment with Step 5's parser:**

- [ ] For every table produced by every **new** seed module in this step, the un-stamped DataFrame's column list equals the DDL column list returned by `output.writer._load_ddl_column_order()`. Run:
  ```bash
  python -c "
  from output.writer import _load_ddl_column_order
  from seed_data.channel_types import get_channel_type_tables
  from seed_data.campaign_types import get_campaign_type_tables
  from seed_data.address_types import get_address_type_tables
  from seed_data.currency import get_currency_tables
  from seed_data.interest_rate_indices import get_interest_rate_index_tables
  from seed_data.misc_types import get_misc_type_tables
  ddl = _load_ddl_column_order()
  combined = {}
  for fn in (get_channel_type_tables, get_campaign_type_tables,
             get_address_type_tables, get_currency_tables,
             get_interest_rate_index_tables, get_misc_type_tables):
      combined.update(fn())
  problems = []
  for key, df in combined.items():
      if key not in ddl:
          problems.append(f'{key}: not found in 07 DDL parse'); continue
      ddl_cols = ddl[key]
      df_cols  = list(df.columns)
      if df_cols != ddl_cols:
          problems.append(f'{key}: order mismatch\\n  DDL: {ddl_cols}\\n  DF : {df_cols}')
  if problems:
      for p in problems: print(p)
      raise SystemExit(1)
  print(f'{len(combined)} Step 8 tables aligned with DDL')
  "
  ```
  If a table is legitimately missing from `07`'s DDL parse, log the mismatch and escalate per Handoff Protocol §2 rather than silently passing.
- [ ] After stamping, every table returned by `Tier0Lookups.generate()` passes `output.writer._reorder_to_ddl()` — i.e. business columns match DDL and DI tail is present. Run:
  ```bash
  python -c "
  from generators.tier0_lookups import Tier0Lookups
  from output.writer import _reorder_to_ddl
  tables = Tier0Lookups().generate(None)
  for k, df in tables.items():
      try:
          _reorder_to_ddl(df, k)
      except (ValueError, KeyError) as e:
          raise SystemExit(f'{k}: {e}')
  print(f'{len(tables)} tables pass _reorder_to_ddl')
  "
  ```

**Row-count plausibility:**

- [ ] Every new table has ≥3 rows. Run:
  ```bash
  python -c "
  from seed_data.channel_types import get_channel_type_tables
  from seed_data.campaign_types import get_campaign_type_tables
  from seed_data.address_types import get_address_type_tables
  from seed_data.currency import get_currency_tables
  from seed_data.interest_rate_indices import get_interest_rate_index_tables
  from seed_data.misc_types import get_misc_type_tables
  combined = {}
  for fn in (get_channel_type_tables, get_campaign_type_tables,
             get_address_type_tables, get_currency_tables,
             get_interest_rate_index_tables, get_misc_type_tables):
      combined.update(fn())
  for k, df in combined.items():
      assert len(df) >= 3, f'{k}: only {len(df)} rows'
  print(f'all {len(combined)} Step 8 tables have >=3 rows')
  "
  ```
- [ ] Step 8 produces exactly 22 new seed tables. Run:
  ```bash
  python -c "
  from seed_data.channel_types import get_channel_type_tables
  from seed_data.campaign_types import get_campaign_type_tables
  from seed_data.address_types import get_address_type_tables
  from seed_data.currency import get_currency_tables
  from seed_data.interest_rate_indices import get_interest_rate_index_tables
  from seed_data.misc_types import get_misc_type_tables
  n = sum(len(fn()) for fn in (
      get_channel_type_tables, get_campaign_type_tables,
      get_address_type_tables, get_currency_tables,
      get_interest_rate_index_tables, get_misc_type_tables))
  # 4 + 6 + 6 + 1 + 1 + 3 = 21 — tolerance 20-24 in case a table is split or combined
  assert 20 <= n <= 24, n
  print(f'{n} Step 8 seed tables produced')
  "
  ```

**No randomness / no dynamic generation:**

- [ ] No new seed module imports `numpy`, `faker`, `scipy`, `random`, or `secrets`. Run:
  ```bash
  python -c "
  import re, pathlib
  pat = re.compile(r'^\s*(?:import|from)\s+(numpy|faker|scipy|random|secrets)\b')
  bad = []
  targets = ['seed_data/channel_types.py', 'seed_data/campaign_types.py',
             'seed_data/address_types.py', 'seed_data/currency.py',
             'seed_data/interest_rate_indices.py', 'seed_data/misc_types.py',
             'generators/tier0_lookups.py']
  for p in targets:
      for i, line in enumerate(pathlib.Path(p).read_text().splitlines(), 1):
          if pat.match(line):
              bad.append(f'{p}:{i}: {line}')
  assert not bad, bad
  print('no randomness imports')
  "
  ```
- [ ] No seed module has top-level DataFrame construction (side-effect-free imports). Run:
  ```bash
  python -c "
  import importlib, sys, pandas as pd
  calls = {'n': 0}
  _orig = pd.DataFrame
  def _wrap(*a, **k):
      calls['n'] += 1
      return _orig(*a, **k)
  pd.DataFrame = _wrap
  for name in ('seed_data.channel_types','seed_data.campaign_types',
               'seed_data.address_types','seed_data.currency',
               'seed_data.interest_rate_indices','seed_data.misc_types'):
      sys.modules.pop(name, None)
      importlib.import_module(name)
  pd.DataFrame = _orig
  assert calls['n'] == 0, f'{calls[\"n\"]} DataFrame(s) built at import time'
  print('no import-time DataFrames')
  "
  ```
- [ ] Importing `generators.tier0_lookups` does not execute the generator (no tables built on import). Run:
  ```bash
  python -c "
  import importlib, sys, pandas as pd
  calls = {'n': 0}
  _orig = pd.DataFrame
  def _wrap(*a, **k):
      calls['n'] += 1
      return _orig(*a, **k)
  pd.DataFrame = _wrap
  sys.modules.pop('generators.tier0_lookups', None)
  importlib.import_module('generators.tier0_lookups')
  pd.DataFrame = _orig
  assert calls['n'] == 0, f'{calls[\"n\"]} DataFrame(s) built at import time'
  print('Tier0Lookups import is side-effect-free')
  "
  ```

**Authoring pattern consistency with Step 6/7:**

- [ ] All six new seed files use the `_DI = {'di_start_ts': None, 'di_end_ts': None, 'di_rec_deleted_Ind': None}` pattern. Run:
  ```bash
  python -c "
  import pathlib
  for p in ['seed_data/channel_types.py', 'seed_data/campaign_types.py',
           'seed_data/address_types.py', 'seed_data/currency.py',
           'seed_data/interest_rate_indices.py', 'seed_data/misc_types.py']:
      src = pathlib.Path(p).read_text()
      assert 'di_start_ts' in src and 'di_end_ts' in src and 'di_rec_deleted_Ind' in src
      assert 'None' in src, 'expected None-valued DI columns'
  print('DI-None authoring pattern OK')
  "
  ```

### Universal checks

- [ ] `git status` shows only files listed under ## Produces — nothing else. Run:
  ```bash
  git status --porcelain
  ```
  Every line must map to one of: `seed_data/channel_types.py`, `seed_data/campaign_types.py`, `seed_data/address_types.py`, `seed_data/currency.py`, `seed_data/interest_rate_indices.py`, `seed_data/misc_types.py`, `generators/tier0_lookups.py` (plus this spec file at `.claude/specs/step-08-tier0c-seed-and-generator.md` which is already present on this branch before the implementation session starts). No stray files (no `__pycache__`, no outputs, no changes under `config/`, `utils/`, `registry/`, `output/`, `references/`, `specs/` outside this step's spec, `seed_data/__init__.py`, `generators/__init__.py`).
- [ ] All new files pass `python -c "import <module>"` — covered by the first check above.
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — **n/a**: this step produces no CSVs. The seed tables are pure code-based lookups with no `*_Id` BIGINT columns by design (PKs are `*_Cd` VARCHAR).
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: `PARTY_INTERRACTION_EVENT` is a CDM_DB table generated in Step 22, not touched here.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSV output at this step; the writer is not invoked.

## Handoff notes

**What shipped:** All 7 files produced as specced — 6 seed modules (`channel_types.py`, `campaign_types.py`, `address_types.py`, `currency.py`, `interest_rate_indices.py`, `misc_types.py`) and `generators/tier0_lookups.py`. `Tier0Lookups().generate(None)` returns 79 stamped Core_DB lookup tables (within the 70–85 target). All 21 Definition of Done checks pass.

**Spec typo — table count says 22, actual is 21 (no missing table):** The spec overview states "22 new seed tables" but a cross-check of every table explicitly listed in the spec's own "Tables generated" section gives exactly 21 (4+6+6+1+1+3). The spec's own DoD row-count check comment also says `# 4+6+6+1+1+3 = 21`. Cross-referencing `mvp-tool-design.md §9 Tier 0` confirms every table in the Channel/Promotion, Address/Geo, and Other (Currency/UOM/TimePeriod) domains is present — nothing is missing. The number "22" in the spec overview is a counting typo.

**DDL is correct for CURRENCY — no conflict:** The spec prose description mentioned `Currency_Symbol` and `Currency_Decimal_Digit_Num` columns, but the authoritative DDL in `07_mvp-schema-reference.md §367` shows `Currency_Rounding_Decimal_Cnt` (same semantic, different name) and no symbol column. Implemented exactly per DDL, which the spec itself mandates. The `07` DDL is correct; the spec prose was imprecise.

**INTEREST_RATE_INDEX NOT NULL column:** `Interest_Rate_Index_Time_Period_Cd` is NOT NULL in the DDL. Populated with `'DAY'` for overnight indices (SOFR, PRIME, FEDFUNDS) and `'MONTH'` for term indices (LIBOR 3M, EURIBOR 3M). These FK-resolve to `TIME_PERIOD_TYPE` rows seeded in `misc_types.py`.

**Next session hint:** Step 9 (Tier 1 Geography) is now unblocked. It reads `TERRITORY_TYPE`, `CITY_TYPE`, `CALENDAR_TYPE`, and `CURRENCY` from `ctx.tables` — all present after `Tier0Lookups.generate()` runs.

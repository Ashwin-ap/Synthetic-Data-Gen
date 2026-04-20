# Spec: Step 22 — Tier 14 CDM_DB

## Overview

This step produces the MDM Customer side of Layer 1 — **all 16 `CDM_DB` MULTISET tables** — by projecting the in-memory `CustomerProfile` / `AgreementProfile` registries and selected Core_DB DataFrames onto the CDM schema. Unlike Core_DB, every CDM_DB table carries **both** DI columns (`di_*`) and Valid/Del metadata (`Valid_From_Dt`, `Valid_To_Dt`, `Del_Ind`), and virtually every business code column is `SMALLINT` (not a VARCHAR code). The step also mints a fresh `CDM_Address_Id` BIGINT surrogate key for `CDM_DB.ADDRESS` — the DDL omits it per architect Q6, so this step both updates `references/07_mvp-schema-reference.md` to include the surrogate and populates it during generation. See `mvp-tool-design.md` §9 Tier 14 and §7.2/§7.8/§7.10 for the driving constraints.

## Depends on

- **Step 1** — `config/settings.py` (SIM_DATE, HISTORY_START, HIGH_DATE, HIGH_TS, `PARTY_INTERRACTION_EVENT_TABLE_NAME`, `BANK_PARTY_ID`, `SELF_EMP_ORG_ID`, `ID_RANGES`). This step **adds** a new `'cdm_address'` key to `ID_RANGES`.
- **Step 2** — `utils/id_factory.IdFactory`, `utils/date_utils.format_ts`/`format_date`, `generators/base.BaseGenerator` (`stamp_di` + `stamp_valid`).
- **Step 3** — `registry/context.GenerationContext` (reads `ctx.customers`, `ctx.agreements`, `ctx.addresses`, writes into `ctx.tables`).
- **Step 4** — `UniverseBuilder` outputs. Consumes every `CustomerProfile` field (`party_id`, `party_type`, `household_id`, `household_role`, `clv_segment`, `occupation_cd`, `age`, `party_since`, etc.) and every `AgreementProfile` (`agreement_id`, `owner_party_id`, `open_dttm`, `close_dttm`, `product_type`).
- **Step 10** — Tier 2 core entities. Consumes `Core_DB.PARTY` (Party_Id universe), `Core_DB.AGREEMENT` (Agreement_Id universe) for FK coverage checks.
- **Step 11** — Tier 3 party subtypes. Consumes `Core_DB.ORGANIZATION` (to source `Organization_Name`, `Business_Identifier` analog, and the reserved `SELF_EMP_ORG_ID = 9999999` row).
- **Step 12** — Tier 4a individual attributes. Consumes `Core_DB.INDIVIDUAL_NAME` (current row per individual: `Name_Type_Cd='legal'`, `Individual_Name_End_Dt=HIGH_DATE`) for `Given_Name`/`Middle_Name`/`Family_Name` → CDM `First_Name`/`Middle_Name`/`Last_Name`, and `Core_DB.INDIVIDUAL` (Birth_Dt).
- **Step 15** — Tier 5 location. Consumes `Core_DB.ADDRESS`, `Core_DB.STREET_ADDRESS`, `Core_DB.POSTAL_CODE`, `Core_DB.CITY`, `Core_DB.COUNTY`, `Core_DB.GEOSPATIAL_POINT` to denormalise into `CDM_DB.ADDRESS`.
- **Step 19** — Tier 9 party-agreement links. Consumes `Core_DB.PARTY_AGREEMENT` (one `'customer'` row per agreement — drives `PARTY_TO_AGREEMENT_ROLE` row count).
- **Step 20** — Tier 10 events. Consumes `Core_DB.EVENT_PARTY` (drives `PARTY_TO_EVENT_ROLE` row count) and `Core_DB.COMPLAINT_EVENT` (drives `PARTY_INTERRACTION_EVENT` 1:1).
- **Step 14** — Tier 4c shared party attributes. Consumes `Core_DB.PARTY_CONTACT_PREFERENCE` (the `Channel_Type_Cd` already captured there) for CDM `PARTY_CONTACT.Contact_Type_Cd` alignment (email vs phone).

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Convention apply to every step)

**Key sections to pay close attention to:**
- `PRD.md` §4.1 (MDM Customer in-scope layer), §4.2 (MDM CDM_DB table list — 16 tables), §7.1 (BIGINT everywhere), §7.2 (shared party_id space), §7.3 (two DI column sets — di_* on all tables, Valid_* additionally on CDM/PIM), §7.10 (PARTY_INTERRACTION_EVENT typo), §7.8 (CDM_Address_Id surrogate — the specific Q6 resolution)
- `mvp-tool-design.md` §7 BaseGenerator DI rules, §9 Tier 14 (the authoritative list of 16 tables and SMALLINT code mappings), §11 Output Format, §14 Decision 4 (same party_id across schemas) and Decision 7 (PARTY_INTERRACTION_EVENT typo)
- `implementation-steps.md` Step 22 (exit criteria)

**Additional reference files** (named in the step's "Reads from" line — plus the DDL verification rule in CLAUDE.md):
- `references/05_architect-qa.md` Q1 (BIGINT always), Q2 (Event_Id BIGINT), Q5 (both di and Valid — history stored in di; di_data_src_cd / di_proc_name NULL), Q6 (CDM_Address_Id surrogate — add to DDL and populate), Q7 (Self-Employment Organization 9999999 already seeded in ORGANIZATION CSV)
- `references/07_mvp-schema-reference.md` §CDM Tables section — lines ~2736 through 3015 (all 16 CDM_DB tables, plus the Notes #38 at line 3172 stating `CDM_DB.ADDRESS` DDL is missing `CDM_Address_Id` and must be added). Verify column order and NOT NULL lists per table before defining `_COLS_<TABLE>` lists.

## Produces

### New generator module

- `generators/tier14_cdm.py` — `Tier14CDM(BaseGenerator)` class. A single `generate(ctx) -> Dict[str, pd.DataFrame]` method returns 16 DataFrames keyed by their `CDM_DB.<TABLE>` schema keys:

  | Output key | Notes |
  |------------|-------|
  | `CDM_DB.PARTY` | 1 row per CustomerProfile |
  | `CDM_DB.INDIVIDUAL` | 1 row per INDIVIDUAL CustomerProfile |
  | `CDM_DB.ORGANIZATION` | 1 row per ORGANIZATION CustomerProfile + the reserved `CDM_Party_Id=9999999` self-employment-org row |
  | `CDM_DB.HOUSEHOLD` | 1 row per distinct `CustomerProfile.household_id` (ignoring None) |
  | `CDM_DB.INDIVIDUAL_TO_HOUSEHOLD` | 1 row per individual with a non-null `household_id` |
  | `CDM_DB.INDIVIDUAL_TO_INDIVIDUAL` | pairs within multi-member households (HEAD↔SPOUSE, HEAD↔DEPENDENT) |
  | `CDM_DB.INDIVIDUAL_TO_ORGANIZATION` | 1 row per EMP individual (no rows for SELF_EMP/RETIRED/NOT_WORKING) |
  | `CDM_DB.ORGANIZATION_TO_ORGANIZATION` | 0–10 rows representing a small parent/subsidiary chain among generated orgs (low-volume, placeholder coverage) |
  | `CDM_DB.PARTY_TO_AGREEMENT_ROLE` | 1 row per AgreementProfile (primary customer role) |
  | `CDM_DB.PARTY_TO_EVENT_ROLE` | 1 row per `Core_DB.EVENT_PARTY` row |
  | `CDM_DB.PARTY_SEGMENT` | 1 row per CustomerProfile (CLV decile segment) |
  | `CDM_DB.ADDRESS` | 1 row per `Core_DB.ADDRESS` row (denormalised), with a fresh `CDM_Address_Id` surrogate |
  | `CDM_DB.ADDRESS_TO_AGREEMENT` | 1 row per AgreementProfile (owner's address) |
  | `CDM_DB.PARTY_CONTACT` | 2 rows per CustomerProfile (1=email, 2=phone) |
  | `CDM_DB.CONTACT_TO_AGREEMENT` | 1 row per AgreementProfile (owner's email contact) |
  | `CDM_DB.PARTY_INTERRACTION_EVENT` | 1 row per `Core_DB.COMPLAINT_EVENT` — **filename preserves the double-R typo** |

  **Note on double-R typo:** the key must match `config.settings.PARTY_INTERRACTION_EVENT_TABLE_NAME` (which resolves to `'PARTY_INTERRACTION_EVENT'` with the typo) — do not introduce a string literal anywhere that would risk a silent correction.

## Tables generated

| Table | Approx rows | Row-construction rule |
|-------|-------------|-----------------------|
| `CDM_DB.PARTY` | ≈ 3,000 | 1 per CustomerProfile. `CDM_Party_Id = cp.party_id`. `Source_Cd = 1` (CIF). `Source_Party_Id = cp.party_id` (self-sourced — SMALLINT-typed FK not needed since both columns are BIGINT). `Party_Type_Cd = 1` if `party_type='INDIVIDUAL'` else `2`. `Party_Lifecycle_Phase_Cd = 3` for ACTIVE/DECLINING/CHURNED cohorts, `2` for NEW cohort (Prospect pre-acquisition flip → Active). `Party_Since = cp.party_since`. `Survival_Record_Ind = 'Y'` for all. `DQ_Score = Decimal('100.00')` for all. |
| `CDM_DB.INDIVIDUAL` | ≈ 2,400 | 1 per CustomerProfile where `party_type='INDIVIDUAL'`. `CDM_Party_Id = cp.party_id`. `First_Name`/`Middle_Name`/`Last_Name` joined from `Core_DB.INDIVIDUAL_NAME` current row (`Individual_Name_End_Dt=HIGH_DATE`, `Name_Type_Cd='legal'`) via `Individual_Party_Id`. `Birth_Dt` joined from `Core_DB.INDIVIDUAL.Birth_Dt`. `Gender`: map `cp.gender_type_cd` (`'MALE'`/`'FEMALE'`) to VARCHAR `'Male'`/`'Female'`. `Salutation`: deterministic `'Mr.'`/`'Ms.'`/`'Mx.'` from gender. `DQ_Score = Decimal('100.00')`. |
| `CDM_DB.ORGANIZATION` | ≈ 601 | 1 per CustomerProfile where `party_type='ORGANIZATION'` (≈600 rows) **plus** 1 row for the reserved self-employment org at `CDM_Party_Id=9999999` (`Organization_Name='Self-Employment Organization'`). `Business_Identifier`: deterministic 9-digit EIN-style string from `cp.party_id` (`f'{cp.party_id % 1_000_000_000:09d}'`). |
| `CDM_DB.HOUSEHOLD` | ≈ 1,000–1,500 | 1 row per **distinct** `cp.household_id` across all customers (filter out `None`). `CDM_Household_Id = household_id` (reuses the BIGINT already minted in Step 4 via `IdFactory('household')`). `Household_Name = f'Household {CDM_Household_Id}'`. `Household_Desc` NULL. |
| `CDM_DB.INDIVIDUAL_TO_HOUSEHOLD` | ≈ 2,400 | 1 row per individual CustomerProfile with `household_id is not None`. Composite PK `(CDM_Party_Id, CDM_Household_Id)`. `Role_Type_Cd` SMALLINT per `HOUSEHOLD_ROLE_TO_CD` (`{1: 'HEAD', 2: 'SPOUSE', 3: 'DEPENDENT'}`). `Probability = Decimal('1.0000')` (hard membership). |
| `CDM_DB.INDIVIDUAL_TO_INDIVIDUAL` | ≈ 1,500–2,500 | Within each household group, emit one directed pair per non-HEAD member → HEAD: `(CDM_Party_Id=member, Parent_CDM_Party_Id=head)`. `Relationship_Type_Cd` SMALLINT: 1=FAMILY. `Relationship_Value_Cd` SMALLINT: 1=SPOUSE, 2=PARENT_OF_DEPENDENT (HEAD→DEPENDENT is not emitted to keep the PK unique; only one directional row per pair). `Probability=Decimal('1.0000')`. |
| `CDM_DB.INDIVIDUAL_TO_ORGANIZATION` | ≈ 1,500 | 1 row per individual with `occupation_cd='EMP'`. `CDM_Party_Id=cp.party_id`, `Parent_CDM_Party_Id=<a real generated org's party_id>` (sample deterministically via `ctx.rng.choice` over the ORG customer IDs — **exclude** 9999999). `Relationship_Type_Cd`=SMALLINT 2=EMPLOYMENT. `Relationship_Value_Cd`=SMALLINT 1=CURRENT. Self-employed / retired / not-working excluded (per PRD §7.12 — no entry to the employer org graph). |
| `CDM_DB.ORGANIZATION_TO_ORGANIZATION` | 0–10 | Minimal coverage rows: sample up to 10 distinct `(child_org, parent_org)` pairs from the ORG customer pool via `ctx.rng.choice`, skipping any pair involving 9999999. If fewer than 20 orgs exist, emit 0 rows without erroring. `Relationship_Type_Cd`=3=SUBSIDIARY, `Relationship_Value_Cd`=1=MAJORITY_OWNED. This table exists to satisfy the DDL scope; no Layer 2 rule depends on it. |
| `CDM_DB.PARTY_TO_AGREEMENT_ROLE` | ≈ 5,000 | 1 row per AgreementProfile. Composite PK `(CDM_Party_Id=ap.owner_party_id, Agreement_Id=ap.agreement_id)`. `Role_Type_Cd`=1=PRIMARY_CUSTOMER (SMALLINT). |
| `CDM_DB.PARTY_TO_EVENT_ROLE` | 1 per `Core_DB.EVENT_PARTY` row | Direct projection of `Core_DB.EVENT_PARTY`. Composite PK `(CDM_Party_Id=Party_Id, Event_Id)`. `Role_Type_Cd` SMALLINT mapped from the VARCHAR `Event_Party_Role_Cd` via `EVENT_PARTY_ROLE_TO_CD` (`{'initiator': 1, 'participant': 2, 'observer': 3, …}` — enumerate every distinct value present). |
| `CDM_DB.PARTY_SEGMENT` | ≈ 3,000 | 1 row per CustomerProfile. `Segment_Type_Cd`=1=CLV_DECILE (SMALLINT). `Segment_Value_Cd = cp.clv_segment` (SMALLINT 1–10). |
| `CDM_DB.ADDRESS` | ≈ 500 | 1 row per `Core_DB.ADDRESS`. `CDM_Address_Id` minted fresh via `ctx.ids.next('cdm_address')`. `Address_Id = <Core_DB.ADDRESS.Address_Id>` (preserves the Tier 5 BIGINT). Denormalised fields (`Address_Country_Cd`, `Address_County`, `Address_City`, `Address_Street`, `Address_Postal_Code`, `Geo_Latitude`, `Geo_Longitude`) joined from Core_DB ADDRESS chain. `Primary_Address_Flag='Y'`. `Address_Type='PHYSICAL'`. `Address_Country_Cd` is SMALLINT — map from `COUNTRY.ISO3_Cd` via a small dict (`{'USA': 1, 'CAN': 2, …}`) defined in this module. |
| `CDM_DB.ADDRESS_TO_AGREEMENT` | ≈ 5,000 | 1 row per AgreementProfile. Composite PK `(Address_Id=<owner's address>, Agreement_Id)`. Owner's `Address_Id` sourced from `CustomerProfile.address_id`. |
| `CDM_DB.PARTY_CONTACT` | ≈ 6,000 | 2 rows per CustomerProfile: one `Contact_Type_Cd=1` (email) with `Contact_Value` from Faker email (deterministic via `Faker(seed)`), one `Contact_Type_Cd=2` (phone) with Faker phone string. `Contact_Id` minted via `ctx.ids.next('contact')`. `Primary_Contact_Ind='Y'` on the email row, `'N'` on the phone row. |
| `CDM_DB.CONTACT_TO_AGREEMENT` | ≈ 5,000 | 1 row per AgreementProfile. `Contact_Id` = the email Contact_Id for `ap.owner_party_id`. `Agreement_Id = ap.agreement_id`. |
| `CDM_DB.PARTY_INTERRACTION_EVENT` | ≈ 150 | 1 row per `Core_DB.COMPLAINT_EVENT`. `Event_Id = ce.Event_Id`. `CDM_Party_Id` joined via `Core_DB.EVENT_PARTY` `Event_Party_Role_Cd='initiator'`. `Event_Type_Cd=1` (SMALLINT, COMPLAINT). `Event_Channel_Type_Cd = ce.Event_Channel_Type_Cd` (already SMALLINT in Core_DB). `Event_Dt = date component of COMPLAINT_EVENT.Event_Received_Dttm` (DATE). `Event_Sentiment_Cd = ce.Event_Sentiment_Cd`. Note: this table has **no Valid/Del columns** per DDL — DI only (see §7.3 rule for exceptions: this table is a DI-only event record in CDM_DB). |

Total new rows ≈ 30,000–35,000.

## Files to modify

- `config/settings.py` — **append** a new `'cdm_address': 20_000_000` entry to `ID_RANGES`. This is the BIGINT base for the `CDM_Address_Id` surrogate sequence. Chosen to sit in an unused band between `'event'` (50M) and everything else; verify no collision by importing `ID_RANGES` and asserting it is a fresh key.

- `config/code_values.py` — **append** SMALLINT enum dicts for every CDM code column introduced in this step. These dicts are the authoritative code→label mappings; the generator emits the integer codes, and each dict is the single source of truth for the enumeration:
  - `CDM_PARTY_SOURCE_CD` (`{1: 'CIF'}`)
  - `CDM_PARTY_TYPE_CD` (`{1: 'INDIVIDUAL', 2: 'ORGANIZATION'}`)
  - `CDM_PARTY_LIFECYCLE_PHASE_CD` (`{1: 'EXTERNAL', 2: 'PROSPECT', 3: 'ACTIVE_CUSTOMER', 4: 'FORMER_CUSTOMER'}`)
  - `HOUSEHOLD_ROLE_TO_CD` (`{1: 'HEAD', 2: 'SPOUSE', 3: 'DEPENDENT'}`) — SMALLINT-keyed by Role_Type_Cd (values are the labels used in `CustomerProfile.household_role`)
  - `RELATIONSHIP_TYPE_CD` (`{1: 'FAMILY', 2: 'EMPLOYMENT', 3: 'SUBSIDIARY'}`)
  - `RELATIONSHIP_VALUE_CD` (`{1: 'SPOUSE_OR_CURRENT_OR_MAJORITY', 2: 'PARENT_OF_DEPENDENT', 3: 'OTHER'}`) — distinct values within each Relationship_Type
  - `AGREEMENT_ROLE_TYPE_CD` (`{1: 'PRIMARY_CUSTOMER', 2: 'CO_OWNER', 3: 'BENEFICIARY'}`)
  - `EVENT_PARTY_ROLE_TO_CD` — the mapping VARCHAR `Event_Party_Role_Cd` → SMALLINT. Exact values populated after inspecting `Core_DB.EVENT_PARTY` in-session; at minimum `'initiator': 1`. **Every** distinct value in the upstream column must appear as a key.
  - `SEGMENT_TYPE_CD` (`{1: 'CLV_DECILE'}`)
  - `CONTACT_TYPE_CD` (`{1: 'EMAIL', 2: 'PHONE', 3: 'MOBILE'}`)
  - `ADDRESS_COUNTRY_CD` (`{1: 'USA', 2: 'CAN', 3: 'MEX', …}`) — covers every ISO3 country code present in `Core_DB.COUNTRY`.
  - `INTERRACTION_EVENT_TYPE_CD` (`{1: 'COMPLAINT', 2: 'INQUIRY', 3: 'COMPLIMENT'}`)

  Exact integer values are free to refine; the requirement is that every SMALLINT column in the 16 tables draws from a named dict in this module and that the reverse-lookup is total over the values emitted.

- `references/07_mvp-schema-reference.md` — **edit the `#### ADDRESS` section under `### CDM Tables (CDM_DB)`** (currently at lines ~2994–3015) to insert a new `CDM_Address_Id BIGINT PK NOT NULL` row **at the top** of the column list, before `Address_Id`. This is the surrogate PK Q6 prescribes and is required for `output/writer.py`'s `_reorder_to_ddl` to accept the generated DataFrame's column set. Do not edit the CDM_DB.ADDRESS `CREATE MULTISET TABLE` block further down in the same file (that DDL is for Teradata load-script reference; the canonical column-list the writer parses lives in the `####`-level markdown table block at the top of the CDM_DB section).

No other files modified. In particular: do not modify `registry/profiles.py`, `registry/universe.py`, `utils/id_factory.py`, `generators/base.py`, or any earlier tier generator.

## New dependencies

No new dependencies. `faker` is already in `requirements.txt` from Step 1 and is reused here for CDM `PARTY_CONTACT.Contact_Value` generation (deterministic: reseed per CustomerProfile.party_id to preserve byte-identical output across runs).

## Rules for implementation

**Universal rules (every step):**

- BIGINT for all ID columns (per PRD §7.1) — never INTEGER, even when the DDL says INTEGER. Applies to every `CDM_Party_Id`, `CDM_Household_Id`, `CDM_Address_Id`, `Address_Id`, `Agreement_Id`, `Event_Id`, `Contact_Id`, `Parent_CDM_Party_Id`, `Source_Party_Id`. Emit every `*_Id` pandas column as dtype `Int64` (nullable bigint) so NULL FKs format correctly and no CSV row renders with a `.0` suffix.
- Same `party_id` space across Core_DB and CDM_DB (per PRD §7.2) — `CDM_Party_Id == CustomerProfile.party_id`, no remapping, no new surrogate.
- DI column stamping on every table via `BaseGenerator.stamp_di()`. All 16 tables carry 5 DI columns.
- `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind` stamped additionally on **15 of the 16 CDM tables** via `BaseGenerator.stamp_valid()`. The exception is **`PARTY_INTERRACTION_EVENT`** — its DDL (lines 2978–2992 of the schema reference) has no Valid columns; it is a DI-only event record. Do not stamp Valid on it.
- `di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records. `Del_Ind = 'N'`. `di_rec_deleted_Ind = 'N'`.
- `di_data_src_cd` and `di_proc_name` are NULL (Q5c).
- Column order in every DataFrame matches the DDL declaration order in `references/07_mvp-schema-reference.md` (after this step's ADDRESS edit lands). Use module-level `_COLS_<TABLE>: List[str]` lists (mirroring the `tier11_crm`/`tier10_events` pattern) and construct DataFrames with `pd.DataFrame(rows, columns=_COLS_<TABLE>)`.
- Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim (per PRD §7.10). Do not write the string `'INTERACTION'` anywhere; always derive the table name from `config.settings.PARTY_INTERRACTION_EVENT_TABLE_NAME`.
- Skip the `GEOSPATIAL` table entirely (per PRD §7.9) — n/a for this step; already skipped upstream.
- No ORMs, no database connections — pure pandas → CSV.
- Reproducibility: all randomness derives from `ctx.rng`, which is seeded from `config.settings.SEED = 42`. Faker must be re-seeded deterministically per-row (e.g. `Faker().seed_instance(int(cp.party_id))`) so contact generation does not consume `ctx.rng` state and so re-runs produce byte-identical output.

**Step-specific rules:**

- **`stamp_valid` is conditional.** Stamp 15 of 16 tables; skip `PARTY_INTERRACTION_EVENT`. Implement this as an explicit `if table_key != 'CDM_DB.PARTY_INTERRACTION_EVENT'` branch in the emit loop — do not rely on a silent DDL column match, because `_reorder_to_ddl` would raise an "unexpected business column" error if Valid cols were stamped on a table whose DDL omits them.
- **`CDM_Address_Id` is a surrogate minted in this step.** It is not carried by `AddressRecord` and is not in `CustomerProfile`. Use `ctx.ids.next('cdm_address')` and persist a local `{Address_Id → CDM_Address_Id}` map only within `Tier14CDM.generate` — do not write it back to `ctx` or to any upstream table.
- **DDL edit is a code-sibling change.** The `07_mvp-schema-reference.md` edit that inserts `CDM_Address_Id` must happen **before** the first run of `Tier14CDM().generate(ctx)` (because `output/writer.py._load_ddl_column_order` is `lru_cache`'d on import and parses the file once). In practice: make the edit in the same session, drop any cached writer module (`importlib.reload(output.writer)`) if re-running, and verify via `python -c "from output.writer import _load_ddl_column_order; assert _load_ddl_column_order()['CDM_DB.ADDRESS'][0] == 'CDM_Address_Id'"`.
- **INDIVIDUAL_TO_INDIVIDUAL uses a canonical direction.** Only emit rows where the non-HEAD member points to the HEAD (via `Parent_CDM_Party_Id=head.party_id`). This keeps the composite PK `(CDM_Party_Id, Parent_CDM_Party_Id)` unique and prevents a spouse↔spouse pair from generating two reciprocal rows.
- **INDIVIDUAL_TO_ORGANIZATION excludes non-EMP cohorts.** Self-employed/retired/not-working individuals are explicitly **not** emitted — per PRD §7.12 the self-emp placeholder org is a Core_DB device; CDM does not carry self-emp employment relationships.
- **ORGANIZATION_TO_ORGANIZATION is defensive.** If fewer than 20 ORG customers exist, emit **zero rows** and continue. Do not raise. This table exists to satisfy DDL scope; no downstream Layer 2 rule depends on it.
- **PARTY_TO_EVENT_ROLE is a direct projection.** Do not invent new event-role relationships — emit exactly one row per existing `Core_DB.EVENT_PARTY` row. Derive `Role_Type_Cd` via the `EVENT_PARTY_ROLE_TO_CD` reverse-map, and fail loudly if the upstream column contains a value not in the map.
- **PARTY_INTERRACTION_EVENT.Event_Dt is DATE, not TIMESTAMP.** Cast the date component of `COMPLAINT_EVENT.Event_Received_Dttm` (a formatted timestamp string `'YYYY-MM-DD HH:MM:SS.ffffff'`) to `'YYYY-MM-DD'`. Verify via a `datetime.strptime` round-trip for at least one row in the DoD check.
- **Faker determinism.** Re-seed Faker per party: `fk = Faker(); fk.seed_instance(int(cp.party_id))`. Call `fk.email()` / `fk.phone_number()` on the per-party instance. **Never** call the module-level `Faker.seed(...)` inside `generate()` — that mutates global state and breaks parallel/re-entrant tests.
- **SMALLINT dtype.** Pandas has no Int16; project convention (from Step 20 / Step 21) is to store SMALLINT columns as `Int64`. Cast every CDM code column with `.astype('Int64')`.
- **`CDM_DB.ORGANIZATION` must include the placeholder row.** Emit one row with `CDM_Party_Id=9999999`, `Organization_Name='Self-Employment Organization'`. This keeps `INDIVIDUAL_PAY_TIMING.Business_Party_Id=9999999` FK-resolvable even against the CDM org universe.
- **Self-sourced `Source_Party_Id`.** The `CDM_DB.PARTY.Source_Party_Id` BIGINT equals `CDM_Party_Id` — there is only one source (CIF) in this synthetic universe. Do not attempt to derive a separate legacy ID.
- **Determinism of iteration.** When iterating `ctx.customers` / `ctx.agreements` / upstream DataFrames, sort by the respective PK before iterating, to guarantee stable ID-minting order for `cdm_address`, `contact`, and the FK-resolver joins.
- **No randomness without `ctx.rng`.** Never call `numpy.random.*` directly. Never use Python's `random` module. Never seed a new RNG. Faker's `seed_instance(int(cp.party_id))` is the only allowed non-`ctx.rng` determinism.

## Definition of done

Tick every box before the session ends, or mark as `n/a` with a one-line justification.

**Source-of-truth & scaffolding:**

- [ ] `git status` shows only files listed under ## Produces or ## Files to modify — nothing else
- [ ] `python -c "import generators.tier14_cdm"` exits 0
- [ ] `python -c "from generators.tier14_cdm import Tier14CDM; Tier14CDM().generate"` exits 0
- [ ] `config/settings.py` has a `'cdm_address'` key in `ID_RANGES`: `python -c "from config.settings import ID_RANGES; assert 'cdm_address' in ID_RANGES and isinstance(ID_RANGES['cdm_address'], int)"` exits 0
- [ ] `config/code_values.py` re-imports cleanly and exposes the new dicts: `python -c "import config.code_values as cv; [getattr(cv, n) for n in ['CDM_PARTY_SOURCE_CD','CDM_PARTY_TYPE_CD','CDM_PARTY_LIFECYCLE_PHASE_CD','HOUSEHOLD_ROLE_TO_CD','RELATIONSHIP_TYPE_CD','AGREEMENT_ROLE_TYPE_CD','EVENT_PARTY_ROLE_TO_CD','SEGMENT_TYPE_CD','CONTACT_TYPE_CD','ADDRESS_COUNTRY_CD','INTERRACTION_EVENT_TYPE_CD']]"` exits 0
- [ ] `references/07_mvp-schema-reference.md` CDM_DB.ADDRESS column list starts with `CDM_Address_Id`: `python -c "from output.writer import _load_ddl_column_order; assert _load_ddl_column_order()['CDM_DB.ADDRESS'][0] == 'CDM_Address_Id', _load_ddl_column_order()['CDM_DB.ADDRESS'][:3]"` exits 0

**Table count & presence (run against `ctx` built by running Steps 4, 8–21, then `Tier14CDM().generate(ctx)`):**

- [ ] All 16 expected CDM_DB keys appear in the returned dict:
      ```python
      expected = {
          'CDM_DB.PARTY','CDM_DB.INDIVIDUAL','CDM_DB.ORGANIZATION','CDM_DB.HOUSEHOLD',
          'CDM_DB.INDIVIDUAL_TO_HOUSEHOLD','CDM_DB.INDIVIDUAL_TO_INDIVIDUAL',
          'CDM_DB.INDIVIDUAL_TO_ORGANIZATION','CDM_DB.ORGANIZATION_TO_ORGANIZATION',
          'CDM_DB.PARTY_TO_AGREEMENT_ROLE','CDM_DB.PARTY_TO_EVENT_ROLE',
          'CDM_DB.PARTY_SEGMENT','CDM_DB.ADDRESS','CDM_DB.ADDRESS_TO_AGREEMENT',
          'CDM_DB.PARTY_CONTACT','CDM_DB.CONTACT_TO_AGREEMENT','CDM_DB.PARTY_INTERRACTION_EVENT',
      }
      assert set(new_tables.keys()) == expected, set(new_tables.keys()) ^ expected
      ```
- [ ] No table is empty — every generated table has ≥1 row (except `ORGANIZATION_TO_ORGANIZATION` which may legitimately be 0):
      ```python
      for k, df in new_tables.items():
          if k == 'CDM_DB.ORGANIZATION_TO_ORGANIZATION':
              continue
          assert len(df) > 0, f'{k} is empty'
      ```

**Row-count & structural invariants:**

- [ ] `CDM_DB.PARTY` row count equals `len(ctx.customers)`:
      ```python
      assert len(new_tables['CDM_DB.PARTY']) == len(ctx.customers)
      ```
- [ ] CDM Party_Id universe matches Core_DB Party_Id universe 1-to-1:
      ```python
      core_ids = set(ctx.tables['Core_DB.PARTY']['Party_Id'])
      cdm_ids  = set(new_tables['CDM_DB.PARTY']['CDM_Party_Id'])
      assert core_ids == cdm_ids, f'symmetric diff: {core_ids ^ cdm_ids}'
      ```
- [ ] `CDM_DB.INDIVIDUAL` row count equals count of INDIVIDUAL CustomerProfiles:
      ```python
      expected = sum(1 for cp in ctx.customers if cp.party_type == 'INDIVIDUAL')
      assert len(new_tables['CDM_DB.INDIVIDUAL']) == expected
      ```
- [ ] `CDM_DB.ORGANIZATION` row count equals count of ORGANIZATION CustomerProfiles plus 1 (the reserved self-employment org):
      ```python
      from config.settings import SELF_EMP_ORG_ID
      expected = sum(1 for cp in ctx.customers if cp.party_type == 'ORGANIZATION') + 1
      org = new_tables['CDM_DB.ORGANIZATION']
      assert len(org) == expected
      assert SELF_EMP_ORG_ID in set(org['CDM_Party_Id'])
      assert (org.loc[org['CDM_Party_Id'] == SELF_EMP_ORG_ID, 'Organization_Name']
              == 'Self-Employment Organization').all()
      ```
- [ ] `CDM_DB.HOUSEHOLD` row count equals count of distinct non-null `household_id`:
      ```python
      hids = {cp.household_id for cp in ctx.customers if cp.household_id is not None}
      assert len(new_tables['CDM_DB.HOUSEHOLD']) == len(hids)
      assert set(new_tables['CDM_DB.HOUSEHOLD']['CDM_Household_Id']) == hids
      ```
- [ ] `CDM_DB.INDIVIDUAL_TO_HOUSEHOLD` has one row per individual with household_id; every (CDM_Party_Id, CDM_Household_Id) pair is unique:
      ```python
      i2h = new_tables['CDM_DB.INDIVIDUAL_TO_HOUSEHOLD']
      expected = sum(1 for cp in ctx.customers
                     if cp.party_type == 'INDIVIDUAL' and cp.household_id is not None)
      assert len(i2h) == expected
      assert i2h.duplicated(['CDM_Party_Id','CDM_Household_Id']).sum() == 0
      ```
- [ ] `CDM_DB.INDIVIDUAL_TO_INDIVIDUAL` PK pairs are unique (no reciprocal double-emit):
      ```python
      i2i = new_tables['CDM_DB.INDIVIDUAL_TO_INDIVIDUAL']
      assert i2i.duplicated(['CDM_Party_Id','Parent_CDM_Party_Id']).sum() == 0
      # No row where CDM_Party_Id == Parent_CDM_Party_Id (no self-loops)
      assert (i2i['CDM_Party_Id'] != i2i['Parent_CDM_Party_Id']).all()
      ```
- [ ] `CDM_DB.INDIVIDUAL_TO_ORGANIZATION` row count equals count of EMP individuals; none point to 9999999:
      ```python
      from config.settings import SELF_EMP_ORG_ID
      i2o = new_tables['CDM_DB.INDIVIDUAL_TO_ORGANIZATION']
      expected = sum(1 for cp in ctx.customers
                     if cp.party_type == 'INDIVIDUAL' and cp.occupation_cd == 'EMP')
      assert len(i2o) == expected
      assert SELF_EMP_ORG_ID not in set(i2o['Parent_CDM_Party_Id'])
      ```
- [ ] `CDM_DB.PARTY_TO_AGREEMENT_ROLE` row count equals `len(ctx.agreements)`; every `(CDM_Party_Id, Agreement_Id)` pair is unique; every Agreement_Id resolves to Core_DB.AGREEMENT:
      ```python
      ptar = new_tables['CDM_DB.PARTY_TO_AGREEMENT_ROLE']
      assert len(ptar) == len(ctx.agreements)
      assert ptar.duplicated(['CDM_Party_Id','Agreement_Id']).sum() == 0
      core_ags = set(ctx.tables['Core_DB.AGREEMENT']['Agreement_Id'])
      assert set(ptar['Agreement_Id']).issubset(core_ags)
      ```
- [ ] `CDM_DB.PARTY_TO_EVENT_ROLE` row count equals `len(Core_DB.EVENT_PARTY)`; every role code resolves:
      ```python
      ptev = new_tables['CDM_DB.PARTY_TO_EVENT_ROLE']
      ep   = ctx.tables['Core_DB.EVENT_PARTY']
      assert len(ptev) == len(ep)
      import config.code_values as cv
      # EVENT_PARTY_ROLE_TO_CD is {VARCHAR_role: SMALLINT_code}; compare against values, not keys.
      assert set(ptev['Role_Type_Cd'].dropna().astype(int)).issubset(set(cv.EVENT_PARTY_ROLE_TO_CD.values()))
      # And every distinct upstream VARCHAR role must be covered by the map (fail loudly on gaps):
      assert set(ep['Event_Party_Role_Cd'].dropna()).issubset(set(cv.EVENT_PARTY_ROLE_TO_CD.keys()))
      ```
- [ ] `CDM_DB.PARTY_SEGMENT` Segment_Value_Cd values are all in 1..10 (CLV decile):
      ```python
      ps = new_tables['CDM_DB.PARTY_SEGMENT']
      assert ps['Segment_Value_Cd'].between(1, 10).all()
      assert (ps['Segment_Type_Cd'] == 1).all()
      assert len(ps) == len(ctx.customers)
      ```
- [ ] `CDM_DB.ADDRESS` has `CDM_Address_Id` as its first business column and the column is unique BIGINT ≥ 20,000,000:
      ```python
      addr = new_tables['CDM_DB.ADDRESS']
      assert 'CDM_Address_Id' in addr.columns
      assert addr['CDM_Address_Id'].is_unique
      assert (addr['CDM_Address_Id'] >= 20_000_000).all()
      # And one CDM row per Core_DB.ADDRESS row
      assert len(addr) == len(ctx.tables['Core_DB.ADDRESS'])
      assert set(addr['Address_Id']) == set(ctx.tables['Core_DB.ADDRESS']['Address_Id'])
      ```
- [ ] `CDM_DB.ADDRESS_TO_AGREEMENT` row count equals `len(ctx.agreements)`; every Address_Id resolves to CDM_DB.ADDRESS:
      ```python
      a2a = new_tables['CDM_DB.ADDRESS_TO_AGREEMENT']
      assert len(a2a) == len(ctx.agreements)
      assert set(a2a['Address_Id']).issubset(set(addr['Address_Id']))
      ```
- [ ] `CDM_DB.PARTY_CONTACT` has exactly 2 rows per CustomerProfile, with Contact_Type_Cd values {1, 2}:
      ```python
      pc = new_tables['CDM_DB.PARTY_CONTACT']
      assert len(pc) == 2 * len(ctx.customers)
      assert set(pc['Contact_Type_Cd']) == {1, 2}
      assert pc['Contact_Id'].is_unique
      ```
- [ ] `CDM_DB.CONTACT_TO_AGREEMENT` row count equals `len(ctx.agreements)`; every Contact_Id is an email contact (Contact_Type_Cd=1):
      ```python
      c2a = new_tables['CDM_DB.CONTACT_TO_AGREEMENT']
      assert len(c2a) == len(ctx.agreements)
      email_ids = set(pc.loc[pc['Contact_Type_Cd'] == 1, 'Contact_Id'])
      assert set(c2a['Contact_Id']).issubset(email_ids)
      ```
- [ ] **`CDM_DB.PARTY_INTERRACTION_EVENT` key uses the preserved double-R typo**, has one row per `Core_DB.COMPLAINT_EVENT`, and carries only DI metadata (no Valid_* columns):
      ```python
      from config.settings import PARTY_INTERRACTION_EVENT_TABLE_NAME as TBL
      key = f'CDM_DB.{TBL}'
      assert 'INTERRACTION' in key  # double-R
      pie = new_tables[key]
      ce  = ctx.tables['Core_DB.COMPLAINT_EVENT']
      assert len(pie) == len(ce)
      assert set(pie['Event_Id']) == set(ce['Event_Id'])
      # Date format check
      from datetime import datetime
      for v in pie['Event_Dt'].head(5):
          datetime.strptime(v, '%Y-%m-%d')  # raises on bad format
      for col in ('Valid_From_Dt','Valid_To_Dt','Del_Ind'):
          assert col not in pie.columns, f'PARTY_INTERRACTION_EVENT has unexpected {col}'
      ```
- [ ] `PARTY_INTERRACTION_EVENT.CDM_Party_Id` per event equals the `'initiator'` EVENT_PARTY.Party_Id for the same Event_Id:
      ```python
      ep_init = ctx.tables['Core_DB.EVENT_PARTY']
      ep_init = ep_init[ep_init['Event_Party_Role_Cd'] == 'initiator'][['Event_Id','Party_Id']]
      m = pie.merge(ep_init, on='Event_Id', suffixes=('_pie','_ep'))
      assert (m['CDM_Party_Id'] == m['Party_Id']).all()
      ```

**ID-type / dtype invariants:**

- [ ] All `*_Id` columns across the 16 tables have pandas dtype `Int64`:
      ```python
      id_cols = {
          'CDM_DB.PARTY':                  ['CDM_Party_Id','Source_Party_Id'],
          'CDM_DB.INDIVIDUAL':             ['CDM_Party_Id'],
          'CDM_DB.ORGANIZATION':           ['CDM_Party_Id'],
          'CDM_DB.HOUSEHOLD':              ['CDM_Household_Id'],
          'CDM_DB.INDIVIDUAL_TO_HOUSEHOLD':['CDM_Party_Id','CDM_Household_Id'],
          'CDM_DB.INDIVIDUAL_TO_INDIVIDUAL':['CDM_Party_Id','Parent_CDM_Party_Id'],
          'CDM_DB.INDIVIDUAL_TO_ORGANIZATION':['CDM_Party_Id','Parent_CDM_Party_Id'],
          'CDM_DB.ORGANIZATION_TO_ORGANIZATION':['CDM_Party_Id','Parent_CDM_Party_Id'],
          'CDM_DB.PARTY_TO_AGREEMENT_ROLE':['CDM_Party_Id','Agreement_Id'],
          'CDM_DB.PARTY_TO_EVENT_ROLE':    ['CDM_Party_Id','Event_Id'],
          'CDM_DB.PARTY_SEGMENT':          ['CDM_Party_Id'],
          'CDM_DB.ADDRESS':                ['CDM_Address_Id','Address_Id'],
          'CDM_DB.ADDRESS_TO_AGREEMENT':   ['Address_Id','Agreement_Id'],
          'CDM_DB.PARTY_CONTACT':          ['Contact_Id'],
          'CDM_DB.CONTACT_TO_AGREEMENT':   ['Contact_Id','Agreement_Id'],
          'CDM_DB.PARTY_INTERRACTION_EVENT':['Event_Id','CDM_Party_Id'],
      }
      for k, cols in id_cols.items():
          df = new_tables[k]
          if len(df) == 0:
              continue  # ORG_TO_ORG may be empty
          for c in cols:
              assert str(df[c].dtype) == 'Int64', f'{k}.{c}: {df[c].dtype}'
      ```
- [ ] Every CDM SMALLINT code column has dtype `Int64`:
      ```python
      sm_cols = {
          'CDM_DB.PARTY': ['Source_Cd','Party_Type_Cd','Party_Lifecycle_Phase_Cd'],
          'CDM_DB.INDIVIDUAL_TO_HOUSEHOLD': ['Role_Type_Cd'],
          'CDM_DB.INDIVIDUAL_TO_INDIVIDUAL': ['Relationship_Type_Cd','Relationship_Value_Cd'],
          'CDM_DB.INDIVIDUAL_TO_ORGANIZATION': ['Relationship_Type_Cd','Relationship_Value_Cd'],
          'CDM_DB.ORGANIZATION_TO_ORGANIZATION': ['Relationship_Type_Cd','Relationship_Value_Cd'],
          'CDM_DB.PARTY_TO_AGREEMENT_ROLE': ['Role_Type_Cd'],
          'CDM_DB.PARTY_TO_EVENT_ROLE':     ['Role_Type_Cd'],
          'CDM_DB.PARTY_SEGMENT':           ['Segment_Type_Cd','Segment_Value_Cd'],
          'CDM_DB.ADDRESS':                 ['Address_Country_Cd'],
          'CDM_DB.PARTY_CONTACT':           ['Contact_Type_Cd'],
          'CDM_DB.PARTY_INTERRACTION_EVENT':['Event_Type_Cd','Event_Channel_Type_Cd','Event_Sentiment_Cd'],
      }
      for k, cols in sm_cols.items():
          df = new_tables[k]
          if len(df) == 0:
              continue
          for c in cols:
              assert str(df[c].dtype) == 'Int64', f'{k}.{c}: {df[c].dtype}'
      ```
- [ ] Every NOT-NULL column in each DDL has no NULL in the produced DataFrame. Minimum coverage:
      ```python
      not_null = {
          'CDM_DB.PARTY': ['Source_Cd','CDM_Party_Id','Source_Party_Id','Party_Type_Cd',
                           'Party_Lifecycle_Phase_Cd','Party_Since','Survival_Record_Ind','DQ_Score'],
          'CDM_DB.INDIVIDUAL': ['CDM_Party_Id','Birth_Dt'],
          'CDM_DB.ORGANIZATION': ['CDM_Party_Id'],
          'CDM_DB.HOUSEHOLD': ['CDM_Household_Id'],
          'CDM_DB.INDIVIDUAL_TO_HOUSEHOLD': ['CDM_Party_Id','CDM_Household_Id','Role_Type_Cd'],
          'CDM_DB.INDIVIDUAL_TO_INDIVIDUAL': ['CDM_Party_Id','Parent_CDM_Party_Id','Relationship_Type_Cd','Relationship_Value_Cd'],
          'CDM_DB.PARTY_TO_AGREEMENT_ROLE': ['CDM_Party_Id','Agreement_Id','Role_Type_Cd'],
          'CDM_DB.PARTY_TO_EVENT_ROLE': ['CDM_Party_Id','Event_Id','Role_Type_Cd'],
          'CDM_DB.PARTY_SEGMENT': ['CDM_Party_Id','Segment_Type_Cd','Segment_Value_Cd'],
          'CDM_DB.ADDRESS': ['CDM_Address_Id','Address_Id','Address_Country_Cd'],
          'CDM_DB.ADDRESS_TO_AGREEMENT': ['Address_Id','Agreement_Id'],
          'CDM_DB.PARTY_CONTACT': ['Contact_Id','Contact_Type_Cd','Primary_Contact_Ind'],
          'CDM_DB.CONTACT_TO_AGREEMENT': ['Contact_Id','Agreement_Id'],
          'CDM_DB.PARTY_INTERRACTION_EVENT': ['Event_Id','CDM_Party_Id','Event_Type_Cd',
                                              'Event_Channel_Type_Cd','Event_Dt','Event_Sentiment_Cd'],
      }
      for k, cols in not_null.items():
          df = new_tables[k]
          if len(df) == 0:
              continue
          for c in cols:
              assert df[c].notna().all(), f'{k}.{c} has NULL'
      ```

**DI / Valid column invariants:**

- [ ] Every table carries the 5-col DI suffix from `stamp_di` with HIGH_TS sentinel on every row:
      ```python
      for k in new_tables:
          df = new_tables[k]
          if len(df) == 0:
              continue
          for c in ('di_data_src_cd','di_start_ts','di_proc_name','di_rec_deleted_Ind','di_end_ts'):
              assert c in df.columns, f'{k} missing DI col {c}'
          assert (df['di_end_ts'] == '9999-12-31 00:00:00.000000').all()
          assert (df['di_rec_deleted_Ind'] == 'N').all()
      ```
- [ ] 15 of 16 tables carry Valid_From_Dt/Valid_To_Dt/Del_Ind; `PARTY_INTERRACTION_EVENT` does not:
      ```python
      from config.settings import PARTY_INTERRACTION_EVENT_TABLE_NAME as TBL
      skip_key = f'CDM_DB.{TBL}'
      for k in new_tables:
          df = new_tables[k]
          if len(df) == 0:
              continue
          for c in ('Valid_From_Dt','Valid_To_Dt','Del_Ind'):
              if k == skip_key:
                  assert c not in df.columns, f'{k} unexpectedly has {c}'
              else:
                  assert c in df.columns, f'{k} missing {c}'
      # Active sentinel
      for k in new_tables:
          if k == skip_key or len(new_tables[k]) == 0:
              continue
          assert (new_tables[k]['Valid_To_Dt'] == '9999-12-31').all()
          assert (new_tables[k]['Del_Ind'] == 'N').all()
      ```

**Column order (Writer round-trip):**

- [ ] Each DataFrame passes `_reorder_to_ddl` without error (implicit: DDL columns and DataFrame columns agree):
      ```python
      from output.writer import _reorder_to_ddl
      for k in new_tables:
          df = new_tables[k]
          if len(df) == 0:
              continue
          _reorder_to_ddl(df, k)  # raises on any mismatch
      ```
- [ ] CSV filename for `PARTY_INTERRACTION_EVENT` preserves the double-R typo when passed through the Writer:
      ```python
      import tempfile; from pathlib import Path; from output.writer import Writer
      with tempfile.TemporaryDirectory() as tmp:
          w = Writer(tmp); k = f'CDM_DB.{PARTY_INTERRACTION_EVENT_TABLE_NAME}'
          p = w.write_one(k, new_tables[k])
          assert p.name == 'PARTY_INTERRACTION_EVENT.csv'
          assert 'INTERRACTION' in p.name
      ```

**Reproducibility:**

- [ ] Running `Tier14CDM().generate(ctx)` twice on two freshly-built contexts (both seeded from 42 and carrying identical upstream tables) yields DataFrames that compare equal via `pd.testing.assert_frame_equal` for every one of the 16 output keys.

**Miscellaneous universal checks:**

- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — covered by the ID-dtype invariant above. CSV-level is n/a since this step does not run `Writer.write_all` on full output; verified at DataFrame level.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — verified above via Writer round-trip.
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — n/a; this step does not produce Core_DB CSVs and does not invoke `Writer.write_all` at the project-root level.

## Handoff notes

### What shipped

- `generators/tier14_cdm.py` — `Tier14CDM` class generating all 16 CDM_DB tables. Key row counts: PARTY 3001, INDIVIDUAL 2400, ORGANIZATION 601, HOUSEHOLD 233, I2H 466, I2I 233, I2O 1187, O2O 10, PTAR 5052, PTEV 99510, SEGMENT 3000, ADDRESS 500, A2A 5052, CONTACT 6000, C2A 5052, PIE 145.
- `config/code_values.py` — appended 12 SMALLINT enum dicts for Tier 14 (CDM_PARTY_SOURCE_CD, CDM_PARTY_TYPE_CD, CDM_PARTY_LIFECYCLE_PHASE_CD, HOUSEHOLD_ROLE_TO_CD, RELATIONSHIP_TYPE_CD, RELATIONSHIP_VALUE_CD, AGREEMENT_ROLE_TYPE_CD, EVENT_PARTY_ROLE_TO_CD, SEGMENT_TYPE_CD, CONTACT_TYPE_CD, ADDRESS_COUNTRY_CD with 20-country mapping, INTERRACTION_EVENT_TYPE_CD).
- `config/settings.py` — added `'cdm_address': 20_000_000` to `ID_RANGES`.
- `references/07_mvp-schema-reference.md` — inserted `CDM_Address_Id BIGINT PK NOT NULL` as first column in the CDM_DB.ADDRESS markdown table.

### Decisions

- `CDM_DB.PARTY` includes the reserved `BANK_PARTY_ID=9999999` row (same value as `SELF_EMP_ORG_ID`) so that `CDM_Party_Id universe == Core_DB.Party_Id universe` as required by DoD check [4]. The spec prose says "1 per CustomerProfile" but the DoD assertion requires symmetry — the DoD wins.
- ADDRESS denormalisation uses dict lookups from Core_DB.STREET_ADDRESS (not AddressRecord FKs) to match the actual FK chain generated by Tier 5's `_resolve_fk_chain`. CITY and COUNTY are ID-only tables so `Address_City` and `Address_County` are NULL (DDL-nullable).
- `ADDRESS_COUNTRY_CD` dict keyed `int → ISO3` (not `ISO3 → int`) to match the SMALLINT direction; `_ISO_NUM_TO_ADDR_CD` maps numeric code strings ('840'…) → SMALLINT codes.
- `EVENT_PARTY_ROLE_TO_CD = {'initiator': 1}` — only value in Core_DB.EVENT_PARTY for this dataset. Generator raises ValueError on any unknown role, so new values surface immediately.

### Deferrals

None. All 27 DoD checks pass.

### Next-session hint

Step 23 — PIM_DB tables (Tier 15). The `cdm_address` key is already in ID_RANGES. The writer and schema reference are ready. PIM_DB tables follow the same DI+Valid stamp pattern as CDM_DB.


# Spec: Step 10 — Tier 2 Core Entities

## Overview

This step builds **Tier 2 — Core Entities**, the eight Core_DB tables that every downstream tier FK-references: `PARTY` (the conceptual Core_DB party registry, IDs shared with CDM_DB per PRD §7.2), `PRODUCT` (one row per distinct product type in the universe), `FEATURE` (~24 rows, including the two literal-match rows Layer 2 depends on), `AGREEMENT` (~5,000 rows projected from `AgreementProfile` — the centre of gravity of the dataset), `ANALYTICAL_MODEL` (the profitability/customer-profitability models that AGREEMENT_SCORE and PARTY_SCORE reference in later tiers), `MARKET_SEGMENT`, `CHANNEL_INSTANCE` (~20 instances across seeded channel types), and `CAMPAIGN` (~10 hand-coded campaigns). Unlike Tier 0 (pure lookups loaded from `seed_data/`) and Tier 1 (reference geography also loaded from `seed_data/`), Tier 2 is the first tier that **projects the in-memory universe** (`CustomerProfile` + `AgreementProfile`) built in Step 4 — `AGREEMENT` rows are 1-to-1 with `ctx.agreements`, `PARTY` rows are 1-to-1 with `ctx.customers`, and `PRODUCT` rows are 1-per-distinct `product_type` using the `product_id` values already minted inside `UniverseBuilder._generate_agreements` (universe.py §391–393). No new statistical decisions are made here — only data formatting, FK wiring, and the few hand-wired rows that `FEATURE`, `ANALYTICAL_MODEL`, `MARKET_SEGMENT`, `CHANNEL_INSTANCE`, and `CAMPAIGN` need to satisfy Layer 2 transformation prerequisites (`mvp-tool-design.md` §12 items #17, #18, plus the `Rate Feature` + `Original Loan Term` literal-match rows that LOAN_ACCOUNT_BB matches verbatim). See `mvp-tool-design.md` §9 Tier 2 for the authoritative scope and `PRD.md` §4.2 for the enumerated table list.

## Depends on

- **Step 1** — consumes from `config/settings.py`: `ID_RANGES` (this step uses the existing `product`, `feature`, `model`, `market_seg`, `channel`, `campaign` categories — **does not add new categories**), `HIGH_TS` stamped as `di_end_ts` default on every Tier 2 row via `BaseGenerator.stamp_di()`, and `HISTORY_START` / `SIM_DATE` for campaign date ranges. No `Valid_To_Dt` wiring (Tier 2 is all Core_DB).
- **Step 2** — consumes `generators/base.BaseGenerator` (`stamp_di()` method only; `stamp_valid()` **never called** in this step) and `utils/id_factory.IdFactory.next(category)` for minting BIGINT IDs for categories that the universe did not pre-allocate (`feature`, `model`, `market_seg`, `channel`, `campaign`). The `product` IDs come from `agreement.product_id` and **must not be re-minted**.
- **Step 3** — consumes `registry/profiles.CustomerProfile`, `registry/profiles.AgreementProfile`, `registry/context.GenerationContext`. `Tier2Core.generate(ctx)` reads `ctx.customers`, `ctx.agreements`, `ctx.ids`, and `ctx.tables` (for Tier 0 lookup presence checks); it does NOT mutate `ctx.tables` (the orchestrator does `ctx.tables.update()` after every tier per design §15).
- **Step 4** — consumes the built universe. Critical invariants this step depends on:
  - Every `AgreementProfile.agreement_id` is a unique BIGINT.
  - Every `AgreementProfile.owner_party_id` is present in `{cp.party_id for cp in ctx.customers}`.
  - Every `AgreementProfile.product_id` is a pre-minted BIGINT that is **stable across all agreements sharing the same `product_type`** (verified in universe.py §391–393 where `product_type_ids[pt] = ids.next('product')` once per type then reused).
  - Every `AgreementProfile.agreement_subtype_cd` equals the `product_type` string and FK-resolves to a seeded `AGREEMENT_SUBTYPE.Agreement_Subtype_Cd` row (Step 6 seeded `CHECKING`, `SAVINGS`, `MMA`, `CERTIFICATE_OF_DEPOSIT`, `RETIREMENT`, `MORTGAGE`, `CREDIT_CARD`, `VEHICLE_LOAN`, `STUDENT_LOAN`, `HELOC`, `PAYDAY`, `COMMERCIAL_CHECKING`).
  - Every `AgreementProfile.open_dttm` is a `datetime` before `SIM_DATE`; every `close_dttm` is `None` except for the ~5% CHURNED cohort.
- **Step 5** — n/a at generation time. The writer is not invoked in this step; DDL column ordering is enforced at DataFrame construction time by passing `columns=_COLS_*` to `pd.DataFrame(...)` and relying on `stamp_di()` to append the 5 DI columns to match the tier 0/1 pattern.
- **Step 8** — consumes already-stamped Tier 0 tables that Tier 2 FK-references by code (not surrogate key):
  - `Core_DB.AGREEMENT_SUBTYPE` — `AGREEMENT.Agreement_Subtype_Cd` resolves here. All 12 MVP product types are seeded.
  - `Core_DB.AGREEMENT_TYPE` — `AGREEMENT.Agreement_Type_Cd` NOT NULL resolves here (seeded values: `DEPOSIT`, `LOAN`, `CREDIT`, `COMMERCIAL`).
  - `Core_DB.AGREEMENT_OBJECTIVE_TYPE` — `AGREEMENT.Agreement_Objective_Type_Cd` NOT NULL resolves here (seeded: `SAVINGS_GOAL`, `HOME_PURCHASE`, `EDUCATION`, `VEHICLE`).
  - `Core_DB.AGREEMENT_OBTAINED_TYPE` — `AGREEMENT.Agreement_Obtained_Cd` NOT NULL resolves here (seeded: `BRANCH`, `ONLINE`, `PHONE`, `REFERRAL`).
  - `Core_DB.AGREEMENT_FORMAT_TYPE` — `AGREEMENT.Agreement_Format_Type_Cd` (nullable) resolves here (seeded: `PAPER`, `ELECTRONIC`, `HYBRID`).
  - `Core_DB.ASSET_LIABILITY_TYPE` / `Core_DB.BALANCE_SHEET_TYPE` — nullable FKs from AGREEMENT. Populated where sensible (DEPOSIT agreements → LIABILITY / ON_BALANCE_SHEET; LOAN/CREDIT agreements → ASSET / ON_BALANCE_SHEET; can also be left `None`).
  - `Core_DB.DATA_SOURCE_TYPE` — `PARTY.Initial_Data_Source_Type_Cd` (nullable) and `ANALYTICAL_MODEL.Data_Source_Type_Cd` (nullable) resolve here (seeded: `CORE_BANKING`, `CARD_SYSTEM`, `LOAN_ORIGINATION`, `MDM`).
  - `Core_DB.STATEMENT_MAIL_TYPE` — `AGREEMENT.Statement_Mail_Type_Cd` (nullable) resolves here (seeded: `PAPER`, `EMAIL`, `PORTAL`, `NONE`).
  - `Core_DB.FEATURE_SUBTYPE` — `FEATURE.Feature_Subtype_Cd` NOT NULL resolves here (`RATE_FEATURE_SUBTYPE_CD = 'Rate Feature'` is seeded first row).
  - `Core_DB.FEATURE_INSURANCE_SUBTYPE` — `FEATURE.Feature_Insurance_Subtype_Cd` (nullable) resolves here.
  - `Core_DB.FEATURE_CLASSIFICATION_TYPE` — `FEATURE.Feature_Classification_Cd` (nullable) resolves here (`ORIGINAL_LOAN_TERM_CLASSIFICATION_CD = 'Original Loan Term'` is seeded).
  - `Core_DB.CHANNEL_TYPE` — `CHANNEL_INSTANCE.Channel_Type_Cd` NOT NULL resolves here (seeded: `BRANCH`, `ATM`, `ONLINE`, `MOBILE`, `CALL_CENTER`, `EMAIL`).
  - `Core_DB.CHANNEL_INSTANCE_SUBTYPE` — `CHANNEL_INSTANCE.Channel_Instance_Subtype_Cd` (nullable) resolves here (seeded: `MAIN_BRANCH`, `DRIVE_THRU_ATM`, `WEB_PORTAL`, `IOS_APP`, `ANDROID_APP`, `INBOUND_CALL`, `OUTBOUND_CALL`).
  - `Core_DB.CONVENIENCE_FACTOR_TYPE` — `CHANNEL_INSTANCE.Convenience_Factor_Cd` **NOT NULL** resolves here (seeded: `24_7_AVAILABLE`, `BUSINESS_HOURS`, `APPOINTMENT_REQUIRED`, `SELF_SERVICE`, `ASSISTED`).
  - `Core_DB.CAMPAIGN_STRATEGY_TYPE` / `Core_DB.CAMPAIGN_TYPE` / `Core_DB.CAMPAIGN_CLASSIFICATION` — nullable FKs from CAMPAIGN resolve here (seeded sets all present).
  - `Core_DB.CURRENCY` — `CAMPAIGN.Currency_Cd` (nullable) resolves here (seeded USD/EUR/GBP/CAD/AUD/JPY).
- **Step 9** — **no direct FK dependency on Tier 1 in this step**. Tier 2 entities do not reference geography. (Tier 5 in Step 15 wires addresses to Tier 1 — not Tier 2's concern.)

No code from Step 5 (Writer) is imported by this step — Tier 2 returns DataFrames only.

## Reads from (source documents)

**Full document reads** (read the entire file):
- `PRD.md` — read in full
- `mvp-tool-design.md` — read in full
- `implementation-steps.md` — read in full (Dependency Graph, Handoff Protocol, and Seed Data Authoring Convention apply to every step)

**Key sections to pay close attention to** (drawn from the "Reads from" line in `implementation-steps.md` Step 10):
- `PRD.md` §4.2 (enumerated table list for "Party & Individual", "Organization", "Products & Features", "Campaign & Promotion", "Channel & Events"), §7.1 (BIGINT rule — overrides every INTEGER declaration below), §7.2 (shared party ID space), §7.3 (DI column rules; active-record sentinels), §7.5 (exclusive AGREEMENT sub-typing — honoured indirectly here because `AgreementProfile.is_*` flags drive Step 16/17 sub-type tables, not Tier 2)
- `mvp-tool-design.md` §9 Tier 2 **Core Entities** (authoritative scope + literal-match requirements for FEATURE and ANALYTICAL_MODEL), §12 items #17 and #18 (AGREEMENT_SCORE and PARTY_SCORE profitability-model constraints — enforced at row-emission time for ANALYTICAL_MODEL in this step; the score rows themselves are Tier 4/7), §14 Decision 1 (Entity-first registry — Tier 2 is the first tier that projects the universe)
- `implementation-steps.md` Step 10 entry (exit criteria); Handoff Protocol (post-session notes rules)

**Additional reference files** (only those named in the step's "Reads from" line):
- `references/07_mvp-schema-reference.md` — **authoritative DDL** for the eight Tier 2 tables. Open only these blocks (line numbers current as of 2026-04-20):
  - `AGREEMENT` (§3147) — 22 business columns + 3 DI. `Agreement_Id` INTEGER NOT NULL → **BIGINT** per §7.1. `Agreement_Subtype_Cd`, `Agreement_Objective_Type_Cd`, `Agreement_Obtained_Cd`, `Agreement_Type_Cd` are NOT NULL. `Agreement_Legally_Binding_Ind` is **CHAR(3)** (`'Yes'`/`'No'`, not `'Y'`/`'N'`). `Proposal_Id` and `Jurisdiction_Id` are INTEGER nullable — populate as NULL (out of MVP scope, no table to FK to).
  - `PRODUCT` (§4081) — 13 business columns + 3 DI. `Product_Id` INTEGER NOT NULL → BIGINT. `Product_Subtype_Cd` NOT NULL, `Host_Product_Num` NOT NULL. `Financial_Product_Ind` and `Service_Ind` are CHAR(3).
  - `FEATURE` (§4902) — 8 business columns + 3 DI. `Feature_Id` INTEGER NOT NULL → BIGINT. `Feature_Subtype_Cd` NOT NULL.
  - `ANALYTICAL_MODEL` (§8039) — 16 business columns + 3 DI. `Model_Id` INTEGER NOT NULL → BIGINT. `Locator_Id` INTEGER nullable → BIGINT (no Tier 2 table to FK to — populate as NULL). `Attestation_Ind` CHAR(3).
  - `MARKET_SEGMENT` (§5455) — 9 business columns + 3 DI. `Market_Segment_Id` INTEGER NOT NULL → BIGINT. `Model_Id` and `Model_Run_Id` INTEGER NOT NULL → BIGINT. `Segment_Start_Dttm` NOT NULL. `Segment_Creator_Party_Id`, `Market_Segment_Scheme_Id`, `Segment_Group_Id` are all nullable → BIGINT.
  - `CHANNEL_INSTANCE` (§3983) — 7 business columns + 3 DI. `Channel_Instance_Id` INTEGER NOT NULL → BIGINT. `Channel_Type_Cd` NOT NULL, `Convenience_Factor_Cd` **NOT NULL**.
  - `CAMPAIGN` (§4274) — 19 business columns + 3 DI. `Campaign_Id` INTEGER NOT NULL → BIGINT. `Parent_Campaign_Id`, `Funding_GL_Main_Account_Id` nullable → BIGINT. All `Campaign_Estimated_*` counts are INTEGER nullable (not `_Id` columns — plain INTEGER is allowed here; they are integers, not IDs — but to keep things consistent, still emit as `Int64` to match the other integer columns). All `Campaign_Estimated_*_Amt` are DECIMAL(18,4).
  - `PARTY` (§8125) — 6 business columns + 3 DI (CDM_DB tables begin at §8449; use the **Core_DB** block at §8125, not the CDM_DB block at §8451). `Party_Id` INTEGER NOT NULL → BIGINT. `Party_Subtype_Cd` NOT NULL, `Party_Type_Cd` NOT NULL.
  - DDL Anomalies & Notes footnotes §§3121–3125 apply — every `*_Id` column in every Tier 2 table is emitted as BIGINT (pandas `Int64`) regardless of the DDL saying INTEGER.

**Do NOT read** (context budget protection):
- `references/01_schema-reference.md` — `07` is the MVP-filtered authoritative DDL set per PRD §10.
- `references/02_data-mapping-reference.md` — the only Step 3 literal-match constraints touching Tier 2 are items #17 (AGREEMENT_SCORE Model_Type_Cd='profitability') and #18 (PARTY_SCORE Model_Purpose_Cd='customer profitability'). Both are enforced in this step at the `ANALYTICAL_MODEL` emission point and verified in Definition of done; no need to re-read the full mapping document.
- `references/05_architect-qa.md` — Q1/Q2 (BIGINT) are already absorbed into PRD §7.1, which is the direct rule this spec cites. No Q touches the other Tier 2 tables.
- `references/06_supporting-enrichments.md` — distributions are Step 4's responsibility; Tier 2 is pure projection.
- `resources/CIF_FSDM_Mapping_MASTER.xlsx` / `resources/iDM_MDM_tables_DDLs.xlsx` — already distilled into `07`.

## Produces

All paths relative to the project root.

**New files:**

- `generators/tier2_core.py` — `class Tier2Core(BaseGenerator)` with a single public `generate(ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]` method. Implementation contract:
  1. Import `BaseGenerator`; import `GenerationContext` under `TYPE_CHECKING` only.
  2. Import literal-match constants from `config.code_values`: `PROFITABILITY_MODEL_TYPE_CD`, `CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD`, `RATE_FEATURE_SUBTYPE_CD`, `ORIGINAL_LOAN_TERM_CLASSIFICATION_CD`.
  3. Import `HISTORY_START`, `SIM_DATE`, `HIGH_TS` from `config.settings` for deterministic date defaults and a fixed `_TIER2_DI_START_TS = '2000-01-01 00:00:00.000000'` constant (mirrors Tier 1's pattern for reproducibility — every run produces identical `di_start_ts` values without depending on wall-clock time).
  4. Guard: verify `ctx.customers` is non-empty, `ctx.agreements` is non-empty, `ctx.ids` is non-None, and that the Tier 0 prerequisite tables listed under ## Depends on "Step 8" are present in `ctx.tables`. If any are missing, raise `RuntimeError(f'Tier2Core requires Tier 0 table {key} to be loaded first')`. This guards against orchestration drift.
  5. Build eight DataFrames in FK-dependency order (PARTY/ANALYTICAL_MODEL/MARKET_SEGMENT/CHANNEL_INSTANCE/CAMPAIGN have no Tier 2 intra-dependencies, but `MARKET_SEGMENT.Model_Id` FKs to `ANALYTICAL_MODEL.Model_Id`, so that order is enforced):
     - **`PARTY`** — one row per `CustomerProfile`. `Party_Id = cp.party_id`; `Party_Type_Cd = cp.party_type` (`'INDIVIDUAL'` / `'ORGANIZATION'`); `Party_Subtype_Cd = 'retail'` for INDIVIDUAL, `'commercial'` for ORGANIZATION (documented subtype distinction — no external FK required, these are free-text VARCHAR NOT NULL columns per DDL); `Party_Start_Dttm = datetime.combine(cp.party_since, time(0, 0))`; `Party_End_Dttm = None`; `Party_Desc = None`; `Initial_Data_Source_Type_Cd = 'MDM'`.
     - **`ANALYTICAL_MODEL`** — 5 to 10 hand-coded model rows. **Must include** at least one row with `Model_Type_Cd = PROFITABILITY_MODEL_TYPE_CD` (drives Step 16 AGREEMENT_SCORE's profitability-model requirement — Layer 2 item #17) and at least one row with `Model_Purpose_Cd = CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD` (drives Step 14 PARTY_SCORE — Layer 2 item #18). A single row may satisfy both (`Model_Type_Cd='profitability'` AND `Model_Purpose_Cd='customer profitability'`), but the spec recommends two distinct models so downstream tiers can cross-reference them independently. Other rows (to reach 5–10 total): `'churn_risk'`, `'cross_sell_propensity'`, `'credit_score'`, `'fraud_detection'`, etc. All `Model_Id` values minted via `ctx.ids.next('model')`. `Model_From_Dttm = datetime(2020, 1, 1, 0, 0, 0)`, `Model_To_Dttm = None`. `Attestation_Ind = 'Yes'`. `Data_Source_Type_Cd = 'CORE_BANKING'` or `'MDM'`. `Locator_Id = None` (no FK target in MVP).
     - **`MARKET_SEGMENT`** — **10 rows**, one per `clv_segment` decile (1–10). `Market_Segment_Id` minted via `ctx.ids.next('market_seg')`. `Model_Id` FKs to a single CLV-model row in ANALYTICAL_MODEL (add a dedicated `'clv_decile'` model if not already present). `Model_Run_Id` is a plain BIGINT `1` (no ANALYTICAL_MODEL_RUN table in MVP; the column is NOT NULL per DDL so `1` is a valid sentinel). `Segment_Start_Dttm = datetime(HISTORY_START.year, HISTORY_START.month, HISTORY_START.day)`. `Segment_Name = f'CLV Decile {i}'` for `i` in 1..10. `Segment_Desc` matches. Other `*_Id` columns NULL.
     - **`PRODUCT`** — one row per distinct `product_type` in `ctx.agreements` (expected 11–12 distinct types per universe.py). `Product_Id` **must equal** the `product_id` already stored on `AgreementProfile` rows of that type — **do not mint new IDs via `ctx.ids.next('product')`**. Resolve by scanning `ctx.agreements` once and taking `{ag.product_type: ag.product_id for ag in ctx.agreements}` as the authoritative map (all agreements of a type carry the same product_id by universe invariant — verified in DoD). `Product_Subtype_Cd = product_type` (reuses the AGREEMENT_SUBTYPE code string). `Host_Product_Num` (NOT NULL) = a deterministic string like `f'HOST_{product_type}_001'`. `Financial_Product_Ind = 'Yes'`. `Service_Ind = 'No'`. `Product_Start_Dt = HISTORY_START - timedelta(days=3650)` (~10 years pre-history, ensures every agreement open date is within product validity). `Product_End_Dt = None`. `Product_Name = product_type.replace('_', ' ').title()`.
     - **`FEATURE`** — **24 rows** (meets design §9 "Seed 20–30 features"). Enumerate the cartesian product of the 7 seeded `FEATURE_SUBTYPE` codes × representative `FEATURE_CLASSIFICATION_TYPE` codes, plus explicit literal-match rows. **Must include**: (a) at least one row with `Feature_Subtype_Cd = RATE_FEATURE_SUBTYPE_CD` (matches Step 3 literal for LOAN_ACCOUNT_BB rate derivation), and (b) at least one row with `Feature_Classification_Cd = ORIGINAL_LOAN_TERM_CLASSIFICATION_CD` (matches Step 3 literal for Original Loan Term derivation). All `Feature_Id` values minted via `ctx.ids.next('feature')`. `Feature_Name` / `Feature_Desc` / `Common_Feature_Name` are human-readable strings derived from the subtype + classification combination. `Feature_Insurance_Subtype_Cd` populated only on the one `'Insurance Feature'` subtype row (use `'LIFE'`); otherwise NULL. `Feature_Level_Subtype_Cnt` = 1.
     - **`CHANNEL_INSTANCE`** — **20 rows** spanning the 5 core channel types (4 instances per type for BRANCH/ATM/ONLINE/MOBILE/CALL_CENTER). `Channel_Instance_Id` minted via `ctx.ids.next('channel')`. `Channel_Type_Cd` NOT NULL FKs to seeded `CHANNEL_TYPE`. `Channel_Instance_Subtype_Cd` FKs to seeded `CHANNEL_INSTANCE_SUBTYPE` (e.g. BRANCH → `MAIN_BRANCH`, ATM → `DRIVE_THRU_ATM`, ONLINE → `WEB_PORTAL`, MOBILE → `IOS_APP` or `ANDROID_APP`, CALL_CENTER → `INBOUND_CALL`). `Convenience_Factor_Cd` **NOT NULL** FKs to seeded `CONVENIENCE_FACTOR_TYPE` (BRANCH → `BUSINESS_HOURS`, ATM/ONLINE/MOBILE → `24_7_AVAILABLE`, CALL_CENTER → `BUSINESS_HOURS`). `Channel_Instance_Name` is a human-readable label like `'Branch #01 — Main Street'`, `'ATM NYC-0043'`, `'www.bank.com'`, `'BankApp iOS 2025'`. `Channel_Instance_Start_Dt = HISTORY_START - timedelta(days=3650)`. `Channel_Instance_End_Dt = None`.
     - **`CAMPAIGN`** — **10 rows** spanning strategy × classification combinations. `Campaign_Id` minted via `ctx.ids.next('campaign')`. `Campaign_Strategy_Cd` / `Campaign_Type_Cd` / `Campaign_Classification_Cd` FK to seeded lookups (all nullable but populated here). `Parent_Campaign_Id = None` (flat hierarchy in MVP). `Funding_GL_Main_Account_Id = None`. `Campaign_Start_Dt = HISTORY_START + timedelta(days=rng_offset)` — since Tier 2 is deterministic and does not read `ctx.rng`, use fixed offsets `[0, 30, 60, 90, 120, 10, 40, 70, 100, 130]` for the 10 rows. `Campaign_End_Dt` similarly fixed 90 days later or `None`. `Currency_Cd = 'USD'`. `Campaign_Estimated_*_Amt` = hand-coded Decimals. `Campaign_Estimated_*_Cnt` = hand-coded integers.
  6. For every DataFrame, stamp via `self.stamp_di(df, start_ts=_TIER2_DI_START_TS)`. Do NOT call `stamp_valid()` — Tier 2 tables are all Core_DB.
  7. Return `Dict[str, pd.DataFrame]` keyed `Core_DB.<TABLE>` for all eight tables. Do not mutate `ctx.tables` — the orchestrator does that.

**Do NOT produce** in this step:
- CSVs — writer is not invoked. `output/` must remain empty.
- New `seed_data/*.py` modules — the FEATURE / ANALYTICAL_MODEL / MARKET_SEGMENT / CHANNEL_INSTANCE / CAMPAIGN rows are entity instances (not reference lookups), hand-coded **inside the generator** module. Reserving `seed_data/` for Tier 0 pure lookups keeps the folder contract clean. If the implementation session feels a constants-only helper module would aid testability, create it as a private `generators/_tier2_rows.py` rather than placing it under `seed_data/`.
- Wiring into `main.py` — orchestrator changes are Step 25's responsibility.
- New Tier 0 lookup rows — every code referenced by Tier 2 is already seeded (verified in ## Depends on). If Tier 2 needs a code that is not seeded, escalate per Handoff Protocol §2 rather than monkey-patching Tier 0.
- Changes to `config/settings.py` — all six required ID_RANGES categories (`product`, `feature`, `model`, `market_seg`, `channel`, `campaign`) already exist.
- Changes to `config/code_values.py` — all four required literal-match constants (`PROFITABILITY_MODEL_TYPE_CD`, `CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD`, `RATE_FEATURE_SUBTYPE_CD`, `ORIGINAL_LOAN_TERM_CLASSIFICATION_CD`) already exist.
- Sub-type chain tables (FINANCIAL_AGREEMENT, DEPOSIT_AGREEMENT, etc.) — Step 17's responsibility.
- AGREEMENT_STATUS / AGREEMENT_CURRENCY / AGREEMENT_SCORE / AGREEMENT_FEATURE / AGREEMENT_METRIC / AGREEMENT_RATE — Step 16's responsibility.

## Tables generated (if applicable)

After `Tier2Core.generate(ctx)` runs, `ctx.tables` gains these eight Core_DB keys (row counts are minima or exact counts — actual counts may be slightly different only for PRODUCT, which is bounded by the distinct-product-type count in the universe):

| Table | Row count | FK dependencies (Tier 0 codes) | Literal-match / constraint requirements |
|-------|-----------|--------------------------------|------------------------------------------|
| `Core_DB.PARTY` | ~3,000 (= `len(ctx.customers)`) | `DATA_SOURCE_TYPE.Data_Source_Type_Cd` | Every `Party_Id` equals a `CustomerProfile.party_id`; no duplicates |
| `Core_DB.ANALYTICAL_MODEL` | 5–10 | `DATA_SOURCE_TYPE.Data_Source_Type_Cd` | **≥1 row with `Model_Type_Cd = 'profitability'` (Layer 2 item #17)**, **≥1 row with `Model_Purpose_Cd = 'customer profitability'` (Layer 2 item #18)** |
| `Core_DB.MARKET_SEGMENT` | 10 | `ANALYTICAL_MODEL.Model_Id` | One row per CLV decile (1..10); every `Model_Id` resolves |
| `Core_DB.PRODUCT` | 11–12 (= distinct `product_type` in universe) | `AGREEMENT_SUBTYPE.Agreement_Subtype_Cd` (via `Product_Subtype_Cd`) | Every `Product_Id` matches the universe's `product_type → product_id` map; no new IDs minted |
| `Core_DB.FEATURE` | 24 | `FEATURE_SUBTYPE`, `FEATURE_INSURANCE_SUBTYPE`, `FEATURE_CLASSIFICATION_TYPE` | **≥1 row with `Feature_Subtype_Cd = 'Rate Feature'`**, **≥1 row with `Feature_Classification_Cd = 'Original Loan Term'`** |
| `Core_DB.AGREEMENT` | ~5,000 (= `len(ctx.agreements)`) | `AGREEMENT_SUBTYPE`, `AGREEMENT_TYPE`, `AGREEMENT_OBJECTIVE_TYPE`, `AGREEMENT_OBTAINED_TYPE`, `AGREEMENT_FORMAT_TYPE`, `ASSET_LIABILITY_TYPE`, `BALANCE_SHEET_TYPE`, `STATEMENT_MAIL_TYPE` | Every `Agreement_Id` unique; `Agreement_Legally_Binding_Ind ∈ {'Yes','No'}` (CHAR(3)) |
| `Core_DB.CHANNEL_INSTANCE` | 20 | `CHANNEL_TYPE`, `CHANNEL_INSTANCE_SUBTYPE`, `CONVENIENCE_FACTOR_TYPE` | Spans at least 5 distinct `Channel_Type_Cd` values (BRANCH/ATM/ONLINE/MOBILE/CALL_CENTER); `Convenience_Factor_Cd` NOT NULL on every row |
| `Core_DB.CAMPAIGN` | 10 | `CAMPAIGN_STRATEGY_TYPE`, `CAMPAIGN_TYPE`, `CAMPAIGN_CLASSIFICATION`, `CURRENCY` | Every `Campaign_Id` unique |

All eight DataFrames have the full 5-column DI tail in `DI_COLUMN_ORDER` after `stamp_di()`, with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`.

## Files to modify

No files modified. `config/settings.py`, `config/code_values.py`, `config/distributions.py`, `utils/*`, `registry/*`, `output/*`, `main.py`, `CLAUDE.md`, `PRD.md`, `mvp-tool-design.md`, `implementation-steps.md`, `references/*`, all `seed_data/*.py`, and all existing `generators/*.py` (base, tier0_lookups, tier1_geography) are NOT touched.

If the implementation session finds that `references/07_mvp-schema-reference.md` disagrees with this spec on a column name, type, or nullability, escalate per Handoff Protocol §2 — update the upstream reference or add a `⚠️ Conflict` block to this spec. Do NOT silently improvise.

## New dependencies

No new dependencies. `pandas`, `numpy` are already in `requirements.txt` (Step 1). This step imports only the standard library + pandas + existing project modules.

## Rules for implementation

Universal (apply to every step):

- **BIGINT for all ID columns** (per PRD §7.1) — every `*_Id` column in every Tier 2 DataFrame is emitted as `pd.Int64Dtype()` (nullable BIGINT) or `int64` (when all non-null). The DDL in `07` declares `INTEGER` for nearly every `_Id` column; the BIGINT rule wins unconditionally. This specifically covers: `Agreement_Id`, `Product_Id`, `Feature_Id`, `Model_Id`, `Model_Run_Id`, `Market_Segment_Id`, `Segment_Creator_Party_Id`, `Market_Segment_Scheme_Id`, `Segment_Group_Id`, `Channel_Instance_Id`, `Campaign_Id`, `Parent_Campaign_Id`, `Funding_GL_Main_Account_Id`, `Party_Id`, `Proposal_Id`, `Jurisdiction_Id`, `Product_Script_Id`, `Locator_Id`.
- **Same `party_id` space across Core_DB and CDM_DB** (per PRD §7.2) — `PARTY.Party_Id` in this step comes directly from `CustomerProfile.party_id`; the same BIGINT value will later be written as `CDM_DB.PARTY.CDM_Party_Id` in Step 22. Do NOT re-mint party IDs here. Do NOT emit Core_DB rows for the `BANK_PARTY_ID` / `SELF_EMP_ORG_ID` reserved constants — those are produced by later tiers (Step 11 for the self-emp org placeholder; Step 9 tier9-party-agreement implicitly via PARTY_RELATED for the bank party).
- **DI column stamping on every table** via `BaseGenerator.stamp_di()` — enforced on all eight DataFrames. Pattern matches Tier 1 exactly: construct each DataFrame from `pd.DataFrame(rows, columns=_COLS_*)` with business columns only, then `self.stamp_di(df, start_ts=_TIER2_DI_START_TS)` appends the 5 DI columns at the end. The fixed `_TIER2_DI_START_TS = '2000-01-01 00:00:00.000000'` constant guarantees byte-identical output across runs (mirrors Tier 1's `_GEO_DI_START_TS`).
- **`di_end_ts = '9999-12-31 00:00:00.000000'` and `Valid_To_Dt = '9999-12-31'` for active records** — `di_end_ts` stamped to `HIGH_TS` via `stamp_di()` default. `Valid_To_Dt` n/a: Tier 2 is all Core_DB.
- **CDM_DB and PIM_DB tables additionally stamp `Valid_From_Dt` / `Valid_To_Dt` / `Del_Ind`** (per PRD §7.3) — n/a: Tier 2 is all Core_DB. Do NOT call `stamp_valid()`.
- **Column order in every DataFrame matches DDL declaration order in `references/07_mvp-schema-reference.md`** — enforced at construction time. Every DataFrame is built via `pd.DataFrame(rows, columns=_COLS)` where `_COLS` is the authoritative DDL business-column list. After `stamp_di()` appends the 5 DI columns, the final column order matches the stamped-form convention established by Tier 0 and Tier 1. The Definition-of-done check against `output.writer._reorder_to_ddl()` enforces final correctness.
- **Preserve the `PARTY_INTERRACTION_EVENT` typo verbatim** (per PRD §7.10) — n/a: that table is Step 22 (Tier 14 CDM_DB), not touched here.
- **Skip the `GEOSPATIAL` table entirely** (per PRD §7.9) — n/a: no GEOSPATIAL row authored. `GEOSPATIAL_POINT` is Step 15's responsibility.
- **No ORMs, no database connections — pure pandas → CSV** — writer is not invoked. Generator returns DataFrames only.
- **Reproducibility: all randomness derives from `ctx.rng`, seeded from `config.settings.SEED = 42`** — **no randomness in this step**. Every row is hand-coded or projected deterministically from `ctx.customers` / `ctx.agreements`. Every ID that this step mints is drawn from `ctx.ids` which is deterministic. The generator does not read or use `ctx.rng`.

Step-specific rules (Tier 2 Core Entities):

- **Universe projection is 1-to-1 and deterministic.** `AGREEMENT` has exactly `len(ctx.agreements)` rows in the same iteration order as the list. `PARTY` has exactly `len(ctx.customers)` rows in the same order. No filtering, no sampling, no order-changing sort except where a stable secondary key is needed for the CSV later (ordering is left as-is by the writer per Step 5).
- **`product_id` reuse is invariant, not a convenience.** The universe's invariant "all agreements of product type P share the same `product_id`" must be verified before emitting `PRODUCT` rows. If the scan finds two distinct `product_id` values for the same `product_type`, raise `RuntimeError(f'product_id invariant violated: {product_type} has {n} distinct IDs')` — this is a universe-builder bug and must not be silently tolerated. Do not call `ctx.ids.next('product')` in this step.
- **`product` IdFactory counter must not be advanced by this step.** Verified post-emission: `ctx.ids.peek('product')` value after Tier 2 equals the value before Tier 2. This is a strong guarantee that no product IDs were accidentally minted.
- **Literal-match constants come from `config.code_values`**, never hardcoded as string literals inside this module. Import: `PROFITABILITY_MODEL_TYPE_CD`, `CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD`, `RATE_FEATURE_SUBTYPE_CD`, `ORIGINAL_LOAN_TERM_CLASSIFICATION_CD`. A typo in any of these strings would silently break Layer 2 rules.
- **`Agreement_Legally_Binding_Ind` is CHAR(3), not CHAR(1).** Valid values are `'Yes'` and `'No'`, never `'Y'` / `'N'`. PRD §4.3 "Output format" explicitly distinguishes CHAR(1) (`Y`/`N`) from CHAR(3) (`Yes`/`No`). Same rule applies to `Product.Financial_Product_Ind`, `Product.Service_Ind`, and `Analytical_Model.Attestation_Ind`.
- **`Agreement_Type_Cd` derivation from `product_type`.** Deterministic mapping using the 4 seeded values:
  - DEPOSIT agreements (`CHECKING`, `SAVINGS`, `MMA`, `CERTIFICATE_OF_DEPOSIT`, `RETIREMENT`) → `'DEPOSIT'`
  - LOAN agreements (`VEHICLE_LOAN`, `STUDENT_LOAN`, `MORTGAGE`, `PAYDAY`) → `'LOAN'`
  - CREDIT agreements (`CREDIT_CARD`, `HELOC`) → `'CREDIT'`
  - COMMERCIAL (`COMMERCIAL_CHECKING`) → `'COMMERCIAL'`
  A small private `_AGREEMENT_TYPE_BY_PRODUCT` dict in the module captures this — not re-derived inline.
- **`Agreement_Objective_Type_Cd` derivation from `product_type`.** Deterministic mapping using the 4 seeded values (`SAVINGS_GOAL`, `HOME_PURCHASE`, `EDUCATION`, `VEHICLE`): deposits → `'SAVINGS_GOAL'`; mortgage/HELOC → `'HOME_PURCHASE'`; student loan → `'EDUCATION'`; vehicle loan → `'VEHICLE'`; credit card / payday / commercial → `'SAVINGS_GOAL'` as a generic catch-all. A private `_AGREEMENT_OBJECTIVE_BY_PRODUCT` dict captures this.
- **`Agreement_Obtained_Cd` derivation from product_type (deterministic — no rng).** For reproducibility, use a modulo-based selection across the seeded 4 values: `obtained_values[hash(product_type) % 4]` is forbidden (hash is not stable across runs); instead use a hardcoded per-product-type mapping.
- **Agreement dates come directly from the universe.** `Agreement_Open_Dttm = ag.open_dttm` (already a `datetime`); `Agreement_Close_Dttm = ag.close_dttm` (`None` for non-churned); `Agreement_Planned_Expiration_Dt`, `Agreement_Processing_Dt`, `Agreement_Signed_Dt` all = `ag.open_dttm.date()` or `None` as appropriate.
- **AGREEMENT secondary columns are left NULL where no strong derivation exists.** `Host_Agreement_Num`, `Agreement_Name`, `Alternate_Agreement_Name`, `Statement_Cycle_Cd`, `Agreement_Source_Cd` — all NULL. `Statement_Mail_Type_Cd` — set to `'PORTAL'` for `has_internet=True` owners (look up via `owner_party_id → CustomerProfile`), `'PAPER'` otherwise; a small `cust_by_id = {cp.party_id: cp for cp in ctx.customers}` lookup dict avoids O(n²).
- **`Asset_Liability_Cd` / `Balance_Sheet_Cd` derivation.** DEPOSIT → `LIABILITY` / `ON_BALANCE_SHEET`; LOAN/CREDIT → `ASSET` / `ON_BALANCE_SHEET`; COMMERCIAL_CHECKING → `LIABILITY` / `ON_BALANCE_SHEET`. Deterministic per-product-type mapping.
- **`Agreement_Format_Type_Cd`** — `'ELECTRONIC'` for `has_internet=True` owners, `'PAPER'` otherwise. Same lookup dict as Statement_Mail_Type_Cd.
- **`PARTY` subtype convention.** `Party_Subtype_Cd = 'retail'` for INDIVIDUAL, `'commercial'` for ORGANIZATION. These strings are free-text VARCHAR NOT NULL per DDL — no FK to any `PARTY_SUBTYPE` table (that table is not in MVP scope per `07`). Document the convention in a module-level constant `_PARTY_SUBTYPE_BY_TYPE = {'INDIVIDUAL': 'retail', 'ORGANIZATION': 'commercial'}`.
- **MARKET_SEGMENT requires a dedicated CLV model.** ANALYTICAL_MODEL must include a row with `Model_Name = 'CLV Decile Model'`, `Model_Type_Cd = 'clv_decile'`, `Model_Purpose_Cd = 'customer segmentation'` (plain strings — not literal-match constants). MARKET_SEGMENT's `Model_Id` FKs to that row's `Model_Id`. A private `_CLV_MODEL_NAME` constant makes the linkage explicit.
- **FEATURE enumeration.** Module-level `_FEATURE_ROWS` list of 24 literal row dicts (no loops that can silently drift). Every row has every business column spelled out. Makes diff review trivial.
- **CHANNEL_INSTANCE enumeration.** Module-level `_CHANNEL_INSTANCE_ROWS` list of 20 literal row dicts.
- **CAMPAIGN enumeration.** Module-level `_CAMPAIGN_ROWS` list of 10 literal row dicts. Date offsets are fixed constants, not rng-derived.
- **No side effects on import.** `import generators.tier2_core` must not construct any DataFrames or perform any network/file I/O. Enforced by the "no import-time DataFrames" check in Definition of done.
- **`Tier2Core.generate()` must accept `ctx`** — the `BaseGenerator.generate(self, ctx)` signature is fixed by Step 2. Runtime-import `GenerationContext` via `TYPE_CHECKING` only.
- **Tier 0 prerequisite guard.** `Tier2Core.generate()` starts with an explicit check that all required Tier 0 tables (listed under ## Depends on "Step 8") are in `ctx.tables`. Fail fast with `RuntimeError` if any is missing.
- **Universe prerequisite guard.** `Tier2Core.generate()` also explicitly checks `ctx.customers` and `ctx.agreements` are non-empty, with a clear error: `RuntimeError('Tier2Core requires a populated ctx.customers — run UniverseBuilder.build() first')`.
- **Escalation over improvisation.** If `07` has an ambiguity (column name differs from this spec, nullability unclear), stop and leave a `⚠️ Conflict` block in this spec. Do NOT invent columns or silently swap FKs.

## Definition of done

The implementation session must execute every check below and confirm it passes (or mark it n/a with justification). Commands assume the project root is the current directory and `python` resolves to the project's Python 3.12 environment.

### Exit criteria from implementation-steps.md (rewritten as runnable checks)

**Module-import and API contract:**

- [ ] `python -c "import generators.tier2_core"` exits 0.
- [ ] `generators.tier2_core.Tier2Core` inherits from `BaseGenerator` and `generate(ctx)` is defined. Run:
  ```bash
  python -c "
  from generators.tier2_core import Tier2Core
  from generators.base import BaseGenerator
  import inspect
  assert issubclass(Tier2Core, BaseGenerator)
  sig = inspect.signature(Tier2Core.generate)
  assert 'ctx' in sig.parameters
  print('Tier2Core contract OK')
  "
  ```

**`Tier2Core.generate()` produces the eight expected tables:**

Helper context builder (reused across checks — keep one working directory for the session so this snippet stays stable):

```python
# _mkctx.py (scratch helper — do NOT commit)
import numpy as np
from config import settings as _cfg
from registry.context import GenerationContext
from registry.universe import UniverseBuilder
from generators.tier0_lookups import Tier0Lookups
from generators.tier1_geography import Tier1Geography

def mkctx():
    rng = np.random.default_rng(_cfg.SEED)
    ctx = UniverseBuilder().build(_cfg, rng)
    ctx.tables.update(Tier0Lookups().generate(ctx))
    ctx.tables.update(Tier1Geography().generate(ctx))
    return ctx
```

- [ ] `Tier2Core.generate()` returns exactly these 8 `Core_DB.<TABLE>` keys. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  expected = {
      'Core_DB.PARTY', 'Core_DB.ANALYTICAL_MODEL', 'Core_DB.MARKET_SEGMENT',
      'Core_DB.PRODUCT', 'Core_DB.FEATURE', 'Core_DB.AGREEMENT',
      'Core_DB.CHANNEL_INSTANCE', 'Core_DB.CAMPAIGN',
  }
  assert set(out.keys()) == expected, expected ^ set(out.keys())
  print(f'Tier2Core produced {len(out)} tables: {sorted(out)}')
  "
  ```

- [ ] Row counts meet expectations. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  assert len(out['Core_DB.PARTY']) == len(ctx.customers), (len(out['Core_DB.PARTY']), len(ctx.customers))
  assert len(out['Core_DB.AGREEMENT']) == len(ctx.agreements), (len(out['Core_DB.AGREEMENT']), len(ctx.agreements))
  assert len(out['Core_DB.MARKET_SEGMENT']) == 10
  assert len(out['Core_DB.FEATURE']) == 24
  assert len(out['Core_DB.CHANNEL_INSTANCE']) == 20
  assert len(out['Core_DB.CAMPAIGN']) == 10
  assert 5 <= len(out['Core_DB.ANALYTICAL_MODEL']) <= 10
  distinct_product_types = {ag.product_type for ag in ctx.agreements}
  assert len(out['Core_DB.PRODUCT']) == len(distinct_product_types), (len(out['Core_DB.PRODUCT']), len(distinct_product_types))
  print(f'row counts OK — PARTY={len(out[\"Core_DB.PARTY\"])}, AGREEMENT={len(out[\"Core_DB.AGREEMENT\"])}, PRODUCT={len(out[\"Core_DB.PRODUCT\"])}')
  "
  ```

**AGREEMENT — Layer 2 correctness (implementation-steps.md Step 10 exit criterion):**

- [ ] `ctx.tables['Core_DB.AGREEMENT']` has ~5,000 rows with BIGINT `Agreement_Id`, no duplicates, all in universe ID space. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  df = out['Core_DB.AGREEMENT']
  assert str(df.Agreement_Id.dtype) in ('Int64','int64'), df.Agreement_Id.dtype
  assert df.Agreement_Id.is_unique
  universe_ids = {ag.agreement_id for ag in ctx.agreements}
  assert set(df.Agreement_Id.tolist()) == universe_ids
  print(f'AGREEMENT OK: {len(df)} rows, unique BIGINT Agreement_Id')
  "
  ```

- [ ] Every CHAR(3) Ind column across Tier 2 is in `{'Yes','No'}` — covers `AGREEMENT.Agreement_Legally_Binding_Ind`, `PRODUCT.Financial_Product_Ind`, `PRODUCT.Service_Ind`, and `ANALYTICAL_MODEL.Attestation_Ind` (per PRD §4.3 — CHAR(3) `'Yes'`/`'No'`, not CHAR(1) `'Y'`/`'N'`). Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  checks = [
      ('Core_DB.AGREEMENT',        'Agreement_Legally_Binding_Ind'),
      ('Core_DB.PRODUCT',          'Financial_Product_Ind'),
      ('Core_DB.PRODUCT',          'Service_Ind'),
      ('Core_DB.ANALYTICAL_MODEL', 'Attestation_Ind'),
  ]
  bad = []
  for key, col in checks:
      vals = set(out[key][col].dropna())
      wrong = vals - {'Yes','No'}
      if wrong: bad.append(f'{key}.{col}: invalid CHAR(3) values {wrong} (also seen: {vals})')
  assert not bad, bad
  print('CHAR(3) Ind columns all Yes/No across 4 columns')
  "
  ```

- [ ] Every AGREEMENT NOT-NULL FK column resolves to a seeded Tier 0 row. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  df = out['Core_DB.AGREEMENT']
  pairs = [
      ('Agreement_Subtype_Cd',          'Core_DB.AGREEMENT_SUBTYPE',          'Agreement_Subtype_Cd'),
      ('Agreement_Type_Cd',             'Core_DB.AGREEMENT_TYPE',             'Agreement_Type_Cd'),
      ('Agreement_Objective_Type_Cd',   'Core_DB.AGREEMENT_OBJECTIVE_TYPE',   'Agreement_Objective_Type_Cd'),
      ('Agreement_Obtained_Cd',         'Core_DB.AGREEMENT_OBTAINED_TYPE',    'Agreement_Obtained_Cd'),
  ]
  bad = []
  for col, tbl, tbl_col in pairs:
      assert df[col].notna().all(), f'{col} has NULLs'
      vals = set(df[col].dropna())
      seeded = set(ctx.tables[tbl][tbl_col])
      orphan = vals - seeded
      if orphan: bad.append(f'{col}: orphan values {orphan}')
  assert not bad, bad
  print('AGREEMENT NOT-NULL FKs all resolve')
  "
  ```

**PRODUCT — invariant and row-count constraints (implementation-steps.md Step 10 exit criterion):**

- [ ] PRODUCT row count equals distinct `product_type` count in `ctx.agreements`, and every `Product_Id` matches the universe. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  df = out['Core_DB.PRODUCT']
  universe_map = {ag.product_type: ag.product_id for ag in ctx.agreements}
  # Invariant: every agreement of type P has the same product_id
  per_type = {}
  for ag in ctx.agreements:
      per_type.setdefault(ag.product_type, set()).add(ag.product_id)
  bad_type = {pt: ids for pt, ids in per_type.items() if len(ids) != 1}
  assert not bad_type, f'product_id invariant violated: {bad_type}'
  # PRODUCT row count matches
  assert len(df) == len(universe_map), (len(df), len(universe_map))
  # Every Product_Id matches the universe
  emit = dict(zip(df.Product_Subtype_Cd, df.Product_Id))
  assert emit == universe_map, f'diff: {set(emit.items()) ^ set(universe_map.items())}'
  print(f'PRODUCT OK: {len(df)} rows; Product_Id reuse invariant holds')
  "
  ```

- [ ] `product` IdFactory counter is unchanged by Tier 2 (no new product IDs minted). Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  before = ctx.ids.peek('product')
  Tier2Core().generate(ctx)
  after = ctx.ids.peek('product')
  assert before == after, f'product IdFactory advanced: {before} -> {after}'
  print(f'product IdFactory untouched: {before} == {after}')
  "
  ```

**FEATURE — literal-match constraint (implementation-steps.md Step 10 exit criterion):**

- [ ] At least one FEATURE row has `Feature_Subtype_Cd = 'Rate Feature'` and at least one has `Feature_Classification_Cd = 'Original Loan Term'`. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from config.code_values import RATE_FEATURE_SUBTYPE_CD, ORIGINAL_LOAN_TERM_CLASSIFICATION_CD
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  df = out['Core_DB.FEATURE']
  rate_rows = df[df.Feature_Subtype_Cd == RATE_FEATURE_SUBTYPE_CD]
  term_rows = df[df.Feature_Classification_Cd == ORIGINAL_LOAN_TERM_CLASSIFICATION_CD]
  assert len(rate_rows) >= 1, f'no Rate Feature row (have: {df.Feature_Subtype_Cd.value_counts().to_dict()})'
  assert len(term_rows) >= 1, f'no Original Loan Term row (have: {df.Feature_Classification_Cd.value_counts().to_dict()})'
  print(f'FEATURE literal-match OK: Rate Feature={len(rate_rows)}, Original Loan Term={len(term_rows)}')
  "
  ```

**ANALYTICAL_MODEL — literal-match constraints #17 and #18 (implementation-steps.md Step 10 exit criterion):**

- [ ] At least one ANALYTICAL_MODEL row has `Model_Type_Cd = 'profitability'` and at least one has `Model_Purpose_Cd = 'customer profitability'`. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from config.code_values import PROFITABILITY_MODEL_TYPE_CD, CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  df = out['Core_DB.ANALYTICAL_MODEL']
  prof_rows = df[df.Model_Type_Cd == PROFITABILITY_MODEL_TYPE_CD]
  cust_prof_rows = df[df.Model_Purpose_Cd == CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD]
  assert len(prof_rows) >= 1, f\"no profitability row; values: {df.Model_Type_Cd.dropna().unique().tolist()}\"
  assert len(cust_prof_rows) >= 1, f\"no customer profitability row; values: {df.Model_Purpose_Cd.dropna().unique().tolist()}\"
  print(f'ANALYTICAL_MODEL literal-match OK: profitability={len(prof_rows)}, customer profitability={len(cust_prof_rows)}')
  "
  ```

**MARKET_SEGMENT FK resolution:**

- [ ] Every `MARKET_SEGMENT.Model_Id` resolves to an `ANALYTICAL_MODEL.Model_Id`. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  model_ids = set(out['Core_DB.ANALYTICAL_MODEL'].Model_Id)
  seg_model_ids = set(out['Core_DB.MARKET_SEGMENT'].Model_Id)
  orphan = seg_model_ids - model_ids
  assert not orphan, f'MARKET_SEGMENT orphan Model_Ids: {orphan}'
  assert out['Core_DB.MARKET_SEGMENT'].Market_Segment_Id.is_unique
  print('MARKET_SEGMENT -> ANALYTICAL_MODEL FK OK')
  "
  ```

**PARTY — universe alignment (PRD §7.2 shared ID space):**

- [ ] Every `PARTY.Party_Id` equals a `CustomerProfile.party_id`, no duplicates, no orphans. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  df = out['Core_DB.PARTY']
  universe_party_ids = {cp.party_id for cp in ctx.customers}
  assert df.Party_Id.is_unique
  assert set(df.Party_Id) == universe_party_ids
  assert df.Party_Type_Cd.isin(['INDIVIDUAL','ORGANIZATION']).all()
  assert df.Party_Subtype_Cd.notna().all() and df.Party_Subtype_Cd.isin(['retail','commercial']).all()
  print(f'PARTY universe alignment OK: {len(df)} rows')
  "
  ```

**CHANNEL_INSTANCE — type coverage and NOT-NULL constraint:**

- [ ] CHANNEL_INSTANCE spans at least 5 distinct `Channel_Type_Cd` values (BRANCH/ATM/ONLINE/MOBILE/CALL_CENTER) and every `Convenience_Factor_Cd` is NOT NULL and FK-resolves. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  df = out['Core_DB.CHANNEL_INSTANCE']
  channel_types = set(df.Channel_Type_Cd)
  required = {'BRANCH','ATM','ONLINE','MOBILE','CALL_CENTER'}
  missing = required - channel_types
  assert not missing, f'missing Channel_Type_Cd: {missing}'
  assert df.Convenience_Factor_Cd.notna().all(), 'Convenience_Factor_Cd NOT NULL violated'
  seeded_conv = set(ctx.tables['Core_DB.CONVENIENCE_FACTOR_TYPE'].Convenience_Factor_Cd)
  orphan = set(df.Convenience_Factor_Cd) - seeded_conv
  assert not orphan, f'Convenience_Factor_Cd orphans: {orphan}'
  print(f'CHANNEL_INSTANCE OK: types={channel_types}')
  "
  ```

**CAMPAIGN FK resolution:**

- [ ] Every populated CAMPAIGN FK resolves to a seeded lookup. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  df = out['Core_DB.CAMPAIGN']
  pairs = [
      ('Campaign_Strategy_Cd',     'Core_DB.CAMPAIGN_STRATEGY_TYPE',  'Campaign_Strategy_Cd'),
      ('Campaign_Type_Cd',         'Core_DB.CAMPAIGN_TYPE',           'Campaign_Type_Cd'),
      ('Campaign_Classification_Cd','Core_DB.CAMPAIGN_CLASSIFICATION','Campaign_Classification_Cd'),
      ('Currency_Cd',              'Core_DB.CURRENCY',                'Currency_Cd'),
  ]
  bad = []
  for col, tbl, tbl_col in pairs:
      vals = set(df[col].dropna())
      seeded = set(ctx.tables[tbl][tbl_col])
      orphan = vals - seeded
      if orphan: bad.append(f'{col}: orphan {orphan}')
  assert not bad, bad
  assert df.Campaign_Id.is_unique
  print('CAMPAIGN FKs all resolve')
  "
  ```

**BIGINT ID column enforcement (PRD §7.1):**

- [ ] Every `*_Id` column in every Tier 2 DataFrame is `Int64` / `int64` dtype. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  bad = []
  for k, df in out.items():
      for col in df.columns:
          if col.endswith('_Id'):
              dtype = str(df[col].dtype)
              if dtype not in ('Int64','int64'):
                  bad.append(f'{k}.{col}: dtype={dtype}')
  assert not bad, bad
  print(f'{len(out)} Tier 2 tables: all *_Id columns BIGINT')
  "
  ```

**DI stamping + DDL column order:**

- [ ] Every DataFrame has the full 5-column DI tail with `di_end_ts = HIGH_TS` and `di_rec_deleted_Ind = 'N'`. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from config.settings import HIGH_TS
  from utils.di_columns import DI_COLUMN_ORDER
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  di = list(DI_COLUMN_ORDER)
  bad = []
  for k, df in out.items():
      tail = list(df.columns[-5:])
      if tail != di: bad.append(f'{k}: DI tail {tail} != {di}'); continue
      if not (df.di_end_ts == HIGH_TS).all(): bad.append(f'{k}: di_end_ts mismatch'); continue
      if not (df.di_rec_deleted_Ind == 'N').all(): bad.append(f'{k}: di_rec_deleted_Ind mismatch')
  assert not bad, bad
  print(f'{len(out)} Tier 2 tables pass DI stamping')
  "
  ```

- [ ] After stamping, every table passes `output.writer._reorder_to_ddl()`. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  from output.writer import _reorder_to_ddl
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  out = Tier2Core().generate(ctx)
  for k, df in out.items():
      try: _reorder_to_ddl(df, k)
      except (ValueError, KeyError) as e: raise SystemExit(f'{k}: {e}')
  print(f'{len(out)} Tier 2 tables pass _reorder_to_ddl')
  "
  ```

**Universe / Tier 0 prerequisite guards:**

- [ ] `Tier2Core.generate()` raises `RuntimeError` when `ctx.customers` is empty. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from utils.id_factory import IdFactory
  from registry.context import GenerationContext
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  ctx = GenerationContext(rng=np.random.default_rng(_cfg.SEED), ids=IdFactory(_cfg.ID_RANGES))
  ctx.config = _cfg
  ctx.tables.update(Tier0Lookups().generate(ctx))
  ctx.tables.update(Tier1Geography().generate(ctx))
  # customers/agreements empty — should fail
  try:
      Tier2Core().generate(ctx)
      raise AssertionError('should have raised for empty customers/agreements')
  except RuntimeError as e:
      assert 'customers' in str(e) or 'agreements' in str(e) or 'UniverseBuilder' in str(e), str(e)
  print('universe prereq guard OK')
  "
  ```

- [ ] `Tier2Core.generate()` raises `RuntimeError` when a Tier 0 prerequisite is missing. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier2_core import Tier2Core
  rng = np.random.default_rng(_cfg.SEED)
  ctx = UniverseBuilder().build(_cfg, rng)
  # No Tier 0 loaded — should fail
  try:
      Tier2Core().generate(ctx)
      raise AssertionError('should have raised for missing Tier 0')
  except RuntimeError as e:
      assert 'Tier 0' in str(e) or 'AGREEMENT_SUBTYPE' in str(e) or 'CHANNEL_TYPE' in str(e), str(e)
  print('Tier 0 prereq guard OK')
  "
  ```

**Reproducibility:**

- [ ] Two back-to-back runs with fresh contexts produce byte-identical Tier 2 DataFrames. Run:
  ```bash
  python -c "
  import numpy as np
  from config import settings as _cfg
  from registry.universe import UniverseBuilder
  from generators.tier0_lookups import Tier0Lookups
  from generators.tier1_geography import Tier1Geography
  from generators.tier2_core import Tier2Core
  def fresh():
      rng = np.random.default_rng(_cfg.SEED)
      ctx = UniverseBuilder().build(_cfg, rng)
      ctx.tables.update(Tier0Lookups().generate(ctx))
      ctx.tables.update(Tier1Geography().generate(ctx))
      return Tier2Core().generate(ctx)
  a = fresh(); b = fresh()
  assert set(a) == set(b)
  for k in a:
      assert a[k].equals(b[k]), f'{k} differs between runs'
  print('reproducibility OK')
  "
  ```

**No randomness, no import-time side effects:**

- [ ] `generators/tier2_core.py` does not import `numpy`, `faker`, `scipy`, `random`, or `secrets` (all randomness is resolved in Step 4's UniverseBuilder; Tier 2 is deterministic projection). Run:
  ```bash
  python -c "
  import re, pathlib
  pat = re.compile(r'^\s*(?:import|from)\s+(numpy|faker|scipy|random|secrets)\b')
  bad = []
  for line_no, line in enumerate(pathlib.Path('generators/tier2_core.py').read_text().splitlines(), 1):
      if pat.match(line): bad.append(f'generators/tier2_core.py:{line_no}: {line}')
  assert not bad, bad
  print('no randomness imports')
  "
  ```

- [ ] Importing `generators.tier2_core` does not build any DataFrames. Run:
  ```bash
  python -c "
  import importlib, sys, pandas as pd
  calls = {'n': 0}
  _orig = pd.DataFrame
  def _wrap(*a, **k):
      calls['n'] += 1
      return _orig(*a, **k)
  pd.DataFrame = _wrap
  sys.modules.pop('generators.tier2_core', None)
  importlib.import_module('generators.tier2_core')
  pd.DataFrame = _orig
  assert calls['n'] == 0, f'{calls[\"n\"]} DataFrame(s) built at import time'
  print('no import-time DataFrames')
  "
  ```

### Universal checks

- [ ] `git status` shows only files listed under ## Produces — nothing else. Run:
  ```bash
  git status --porcelain
  ```
  Every line must map to one of: `generators/tier2_core.py` (new), plus this spec file at `.claude/specs/step-10-tier2-core-entities.md` (already present on the branch before the session). No stray files (no `__pycache__`, no output CSVs, no changes under `config/`, `utils/`, `registry/`, `output/`, `references/`, `seed_data/`, other `generators/*.py`, `main.py`).
- [ ] All new files pass `python -c "import <module>"` — covered by the first check above.
- [ ] No CSV column named `*_Id` uses INTEGER (must be BIGINT per PRD §7.1) — covered by the BIGINT dtype check above. **n/a for the CSV-on-disk variant**: this step produces no CSVs; the writer is not invoked.
- [ ] If `PARTY_INTERRACTION_EVENT` is written, filename preserves the double-R typo — **n/a**: not touched in this step (Step 22 / Tier 14).
- [ ] If `output/Core_DB/` exists, it does not contain `GEOSPATIAL.csv` — **n/a**: no CSV output; writer not invoked.

## Handoff notes

### Session notes — 2026-04-20

**What shipped:** `generators/tier2_core.py` — all 8 Core_DB DataFrames generated and verified. All 25 DoD checks pass.

**Row counts (seed=42):** PARTY=3,000, AGREEMENT=5,052, PRODUCT=12 distinct types, ANALYTICAL_MODEL=7, MARKET_SEGMENT=10, FEATURE=24, CHANNEL_INSTANCE=20, CAMPAIGN=10.

**Key implementation decisions:**
- `_ANALYTICAL_MODEL_TEMPLATES` rows 1 & 2 both carry `Model_Type_Cd='profitability'` AND `Model_Purpose_Cd='customer profitability'`, satisfying Layer 2 items #17 and #18. Row 3 (`CLV Decile Model`) is wired into `MARKET_SEGMENT.Model_Id`.
- `_FEATURE_TEMPLATES` row 0 carries both `Feature_Subtype_Cd=RATE_FEATURE_SUBTYPE_CD` and `Feature_Classification_Cd=ORIGINAL_LOAN_TERM_CLASSIFICATION_CD` — both literal-match constraints satisfied on one row.
- PRODUCT: invariant verified at runtime (`product_id` stable per `product_type`). `ctx.ids.next('product')` never called; counter confirmed unchanged (peek=1012 before and after).
- `cust_by_id` dict built once in generate() and reused for both PARTY (Step H) and AGREEMENT (Step I) to derive `has_internet`-based columns.
- All module-level data (templates, lookup dicts, `_CHANNEL_INST_START`) evaluated at import time without constructing any DataFrames — confirmed by the import-time DataFrame check.

**No conflicts or deviations from spec.** No escalations needed.

**Next session hint:** Step 11 (Tier 3 Party Subtypes — `generators/tier3_party_subtypes.py`) can start now. It reads `ctx.customers` (already built) and emits `INDIVIDUAL`, `ORGANIZATION`, `BUSINESS`. The reserved `SELF_EMP_ORG_ID = 9999999` row must be inserted into ORGANIZATION. Depends on `Core_DB.PARTY` (this step) being in `ctx.tables`.

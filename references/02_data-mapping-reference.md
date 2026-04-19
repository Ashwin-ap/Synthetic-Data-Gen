# CIF FSDM Mapping Reference
## Source: `resources/CIF_FSDM_Mapping_MASTER.xlsx`

---

## Step 1 — Sheet Inventory

| Sheet | Contents |
|---|---|
| **Summary** | Empty — no data |
| **Requirements** | CIF universal dimensions (Identity, Profile, Service, Channel, Transaction, Context + derived dimensions) with data-source types (structured / semi-structured / unstructured) and notes |
| **Sheet1** | Pivot table listing FSDM subject-area labels (used as a filter/grouping reference) |
| **WP2 FSDM CRM FV** | Master CIF→FSDM mapping: 445 data rows. Columns: CIF Universal Dimension, CIF Key Dimension, CIF Entity, CIF Element → FSDM Entity, FSDM Element, Mapping Logic, FSDM Data Type, Min/Max, FSAS Entity, FSAS Attribute. Core deliverable of WP2. |
| **Metadata** | Custom tables for AI/ML structuralization lineage: SOURCE, SOURCE TO TARGET, MODEL |
| **WP2 FSDM Customizations** | Custom/extended FSDM tables: PARTY CONTACT PREFERENCE, MULTIMEDIA OBJECT LOCATOR, COMPLAINT EVENT, PARTY TASK, PARTY TASK STATUS, TASK ACTIVITY, TASK ACTIVITY STATUS |
| **WP3 FSAS FSDM Mapping** | 2,193 rows of Layer 1→Layer 2 transformation rules. Columns (11): Target Entity, Target Attribute, Target Type, Source Entity, Source Attribute, Source Type, Rule, Comment, Status, Reason, Last Change Date. Status split: USED ≈ 1,200 rows / EXCLUDED ≈ 805 rows. Target Types: `iDM`, `APBB`, `DIM`, `MDM`, `FACT`, `CIF End DP`, `EFS`. Source Types: `iDM`, `APBB`, `DIM`, `MDM`, `CJF`, `ML`, `MDM, APBB`, `EFS`, `CIF End DP`. |
| **GRAPH Entities** | Full entity catalogue: 184 entities labelled by schema (iDM, APBB, DIM) |
| **GRAPH Elements** | Empty — no data populated |
| **GRAPH Links** | 1,314 rows. Same column structure as WP3 FSAS FSDM Mapping but **without the Status/Reason/Last Change Date columns**. Approximately matches the USED-status rows from WP3. |
| **WP3 FSAS Cust 360** | FSAS fact-table catalogue (~100 fact tables by area) + selected dimension column definitions (ACCOUNT DIMENSION, ACCOUNT STATUS DIMENSION, ADDRESS DIMENSION, PROMOTION DIMENSION, CAMPAIGN DIMENSION, DATE DIMENSION, CUSTOMER DIMENSION, ACTIVITY TYPE DIMENSION) and custom fact-table definitions (GL ACCOUNT MONTHLY SNAPSHOT FACT, CUSTOMER PRODUCT FACTLESS FACT, CUSTOMER ACTIVITY FACTLESS FACT, ALERT EVENT CLIENT FACTLESS FACT, etc.) |
| **WP4 MDM** | MDM layer definitions: PIM (Product) model and CDM (Customer/Party) model with PARTY, INDIVIDUAL, ORGANIZATION, HOUSEHOLD and relationship tables |
| **WP5 Feature Store** | Feature store design: feature groups (BANK, CUSTOMER, CUSTOMER PRODUCT, CUSTOMER CHANNEL) with feature names, mapping types, and **explicit numeric distributions for synthetic data generation** |
| **WP6 Vector Store** | Empty — no data populated |
| **WP7-9 End Data Products** | Entity definitions for end data products: CUSTOMER CLV, CUSTOMER ATTRITION, CUSTOMER PROFILE, CUSTOMER INTERACTIONS, JOURNEY SIGNALS, JOURNEY SIGNAL PATTERNS, CUSTOMER JOURNEY SIGNAL PATTERNS, CUSTOMER JOURNEY EVENTS, CUSTOMER COMPLAINTS, COMPLAINTS RESOLUTIONS, COMPLAINTS RESOLUTION EVENTS |
| **Calculations** | Brief note: CLV = discounted cashflow of customer profitability forecast over expected future life, discounted at bank's target return on equity |
| **Open Questions** | 4 flagged items (see Step 5) |
| **FSDM CRM FV** | Near-empty; one cell: "Household + split to Commercial and Private Party" — appears to be a scratchpad/earlier draft |

---

## MVP Scope — Layer 1 Tables

Derived from **WP3 FSAS FSDM Mapping** (2,193 rows, unfiltered, all Status values included).

Selection criteria:
- **Target Entities**: rows where `Target Type` ∈ `{iDM, MDM}` → 201 unique entities
- **Source Entities**: rows where `Source Type` ∈ `{MDM, APBB, iDM}` → 207 unique entities

> **Data-quality note:** The spreadsheet contains minor inconsistencies — underscore vs space variants (e.g. `ANALYTICAL_MODEL` / `ANALYTICAL MODEL`, `CITY_TYPE` / `CITY TYPE`), and typos (`AGREEMEN FEATURE`, `PARTY INTERRACTION EVENT`). Canonical names are used below.

---

### Target Entities — `Target Type = iDM` (Layer 1 FSDM Tables)

These are the FSDM iDM tables that WP3 transformation rules write into.

**Agreement & Financial Instruments**

AGREEMENT, AGREEMENT CURRENCY, AGREEMENT FEATURE, AGREEMENT FEATURE ROLE TYPE, AGREEMENT FORMAT TYPE, AGREEMENT METRIC, AGREEMENT OBJECTIVE TYPE, AGREEMENT OBTAINED TYPE, AGREEMENT PRODUCT, AGREEMENT RATE, AGREEMENT SCORE, AGREEMENT STATUS, AGREEMENT STATUS REASON TYPE, AGREEMENT STATUS SCHEME TYPE, AGREEMENT STATUS TYPE, AGREEMENT SUBTYPE, AGREEMENT TYPE, AMORTIZATION METHOD TYPE, CARD, CREDIT AGREEMENT, CREDIT CARD AGREEMENT, CREDIT CARD AGREEMENT SUBTYPE, DAY COUNT BASIS TYPE, DEPOSIT AGREEMENT, DEPOSIT MATURITY SUBTYPE, DEPOSIT TERM AGREEMENT, FINANCIAL AGREEMENT, FINANCIAL AGREEMENT TYPE, FINANCIAL EVENT, INTEREST DISBURSEMENT TYPE, INTEREST INDEX RATE, INTEREST RATE INDEX, LOAN AGREEMENT, LOAN MATURITY SUBTYPE, LOAN TERM AGREEMENT, LOAN TERM SUBTYPE, LOAN TRANSACTION AGREEMENT, LOAN TRANSACTION SUBTYPE, MARKET RISK TYPE, MORTGAGE AGREEMENT, MORTGAGE TYPE, TERM FEATURE, TRADING BOOK TYPE, VARIABLE INTEREST RATE FEATURE

**Party & Individual**

ASSOCIATE EMPLOYMENT, HOUSEHOLD, INDIVIDUAL, INDIVIDUAL BONUS TIMING, INDIVIDUAL GENDER PRONOUN, INDIVIDUAL MARITAL STATUS, INDIVIDUAL MEDICAL, INDIVIDUAL MILITARY STATUS, INDIVIDUAL NAME, INDIVIDUAL OCCUPATION, INDIVIDUAL PAY TIMING, INDIVIDUAL SKILL, INDIVIDUAL SPECIAL NEED, INDIVIDUAL VIP STATUS, PARTY, PARTY AGREEMENT, PARTY CLAIM, PARTY CONTACT, PARTY CREDIT REPORT SCORE, PARTY DEMOGRAPHICS, PARTY IDENTIFICATION, PARTY LANGUAGE USAGE, PARTY LOCATOR, PARTY RELATED, PARTY SCORE, PARTY SEGMENT, PARTY SPECIALTY, PARTY TASK, TASK ACTIVITY

Party lookup / type tables: ETHNICITY TYPE, GENDER PRONOUN, GENDER TYPE, GENERAL MEDICAL STATUS TYPE, LANGUAGE TYPE, MARITAL STATUS TYPE, MILITARY STATUS TYPE, NATIONALITY TYPE, OCCUPATION TYPE, PARTY RELATED STATUS TYPE, SKILL TYPE, SPECIAL NEED TYPE, SPECIALTY TYPE, TAX BRACKET TYPE, VERY IMPORTANT PERSON TYPE

**Organization**

BUSINESS, BUSINESS CATEGORY, GICS INDUSTRY GROUP TYPE, GICS INDUSTRY TYPE, GICS SECTOR TYPE, GICS SUBINDUSTRY TYPE, LEGAL CLASSIFICATION, NACE CLASS, NAICS INDUSTRY *GEO, ORGANIZATION, ORGANIZATION GICS, ORGANIZATION NACE *GEO, ORGANIZATION NAICS *GEO, ORGANIZATION NAME, ORGANIZATION SIC *GEO, SIC

**Product & Feature**

ASSET LIABILITY TYPE, BALANCE SHEET TYPE, DATA SOURCE TYPE, DOCUMENT PRODUCTION CYCLE TYPE, FEATURE, FEATURE CLASSIFICATION TYPE, FEATURE INSURANCE SUBTYPE, FEATURE SUBTYPE, PAYMENT TIMING TYPE, PRICING METHOD SUBTYPE, PRODUCT, PRODUCT FEATURE, PURCHASE INTENT TYPE, RISK EXPOSURE MITIGANT SUBTYPE, SECURITY TYPE, STATEMENT MAIL TYPE, TIME PERIOD TYPE, UNIT OF MEASURE

**Campaign & Promotion**

CAMPAIGN, CAMPAIGN CLASSIFICATION, CAMPAIGN STATUS, CAMPAIGN STATUS TYPE, CAMPAIGN STRATEGY TYPE, CAMPAIGN TYPE, COMPLAINT EVENT, PROMOTION, PROMOTION METRIC TYPE, PROMOTION OFFER, PROMOTION OFFER TYPE

**Address & Geography**

ADDRESS, ADDRESS SUBTYPE, ADDRESS TO AGREEMENT, CALENDAR TYPE, CITY, CITY TYPE, COUNTRY, COUNTY, DIRECTION TYPE, ELECTRONIC ADDRESS, ELECTRONIC ADDRESS SUBTYPE, GEOGRAPHICAL AREA, GEOGRAPHICAL AREA CURRENCY, GEOSPATIAL, GEOSPATIAL POINT, INTERNET PROTOCOL ADDRESS, ISO 3166 COUNTRY STANDARD, ISO 3166 COUNTRY SUBDIVISION STANDARD, LOCATOR RELATED, PARCEL ADDRESS, POST OFFICE BOX ADDRESS, POSTAL CODE, REGION, STREET ADDRESS, STREET ADDRESS DETAIL, STREET SUFFIX TYPE, TELEPHONE NUMBER, TERRITORY, TERRITORY TYPE

**Channel, Events & Other**

ANALYTICAL MODEL, CHANNEL INSTANCE, CHANNEL INSTANCE STATUS, CHANNEL INSTANCE SUBTYPE, CHANNEL STATUS TYPE, CHANNEL TYPE, CONVENIENCE FACTOR TYPE, DEMOGRAPHICS VALUE, EVENT, EVENT PARTY, MARKET SEGMENT

---

### Target Entities — `Target Type = MDM` (Layer 1 MDM Tables)

MDM PIM and CDM tables that WP3 populates. These correspond to the WP4 model.

| MDM Sub-layer | Entities |
|---|---|
| **PIM** (Product) | PRODUCT, PRODUCT GROUP, PRODUCT GROUP TYPE, PRODUCT PARAMETER TYPE, PRODUCT PARAMETERS, PRODUCT TO GROUP |
| **CDM** (Party) | ADDRESS TO AGREEMENT, CONTACT TO AGREEMENT, HOUSEHOLD, INDIVIDUAL TO HOUSEHOLD, INDIVIDUAL TO INDIVIDUAL, INDIVIDUAL TO ORGANIZATION, ORGANIZATION TO ORGANIZATION, PARTY, PARTY ADDRESS, PARTY CONTACT, PARTY INTERRACTION EVENT, PARTY SEGMENT, PARTY TO AGREEMENT ROLE, PARTY TO EVENT ROLE |

---

### Source Entities — `Source Type = APBB` (Building Block Layer)

APBB tables used as Layer 2a intermediate sources in WP3 rules:

ACCOUNT BB, ACCOUNT METRIC BB, ACCOUNT STATUS BB, ACCOUNT STATUS PIVOT BB, ADDRESS BB, CAMPAIGN BB, CHANNEL INSTANCE BB, CITY BB, COUNTRY BB, COUNTY BB, ELECTRONIC ADDRESS BB, EVENT BB, FEATURE BB, FINANCIAL EVENT BB, GEOSPATIAL POINT BB, INDIVIDUAL BB, INDIVIDUAL IDENTIFICATION PIVOT BB, LOAN ACCOUNT BB, ORGANIZATION BB, ORGANIZATION IDENTIFICATION PIVOT BB, ORGANIZATION NAME PIVOT BB, PARCEL ADDRESS BB, PARTY IDENTIFICATION PIVOT BB, PARTY PRIMARY LANGUAGE BB, POST OFFICE BOX ADDRESS BB, PROMOTION BB, PROMOTION OFFER BB, PROMOTION OFFER PIVOT BB, REGION BB, SERVICE BB, STREET ADDRESS BB, TELEPHONE NUMBER BB, TERRITORY BB

> `Source Type = iDM` and `Source Type = MDM` draw from the same entity sets as the iDM and MDM Target Entities listed above.

---

## Step 2 — Full Extraction

### Architecture Overview

Three-layer pipeline:

```
Layer 1 (iDM / FSDM)      →  Layer 2a (APBB Building Blocks)  →  Layer 2b (DIM / FSAS Facts)
AGREEMENT                      ACCOUNT BB                            ACCOUNT DIMENSION
PARTY / INDIVIDUAL             INDIVIDUAL BB                         CUSTOMER DIMENSION
AGREEMENT STATUS               ACCOUNT STATUS BB                     ACCOUNT STATUS DIMENSION
                               ACCOUNT STATUS PIVOT BB
STREET ADDRESS / ADDRESS       ADDRESS BB / STREET ADDRESS BB        ADDRESS DIMENSION
CHANNEL INSTANCE               CHANNEL INSTANCE BB                   CHANNEL DIMENSION
CAMPAIGN                       CAMPAIGN BB                           CAMPAIGN DIMENSION
PROMOTION / PROMOTION OFFER    PROMOTION BB / OFFER BB               PROMOTION DIMENSION
ORGANIZATION                   ORGANIZATION BB                       (no separate DIM)
                                                                      GL ACCOUNT MONTHLY SNAPSHOT FACT
                                                                      CIF CUSTOMER PRODUCT FACTLESS FACT
                                                                      (100+ other facts)
```

**Schema codes used throughout:**
- `iDM` = FSDM source (Layer 1)
- `MDM` = Master Data Management layer (CDM + PIM) — Layer 1 alongside iDM
- `APBB` = building block / pivot (Layer 2a)
- `DIM` = final dimension (Layer 2b)
- `FACT` = fact table (Layer 2b)
- `CIF End DP` = CIF End Data Product (WP7–9 layer)
- `EFS` = External/Feature Store layer
- `CJF` = CIF JSON Feed (source system feed, used in WP3 Source Type)
- `ML` = Machine Learning derived (WP3 Source Type only)

---

### WP2 — CIF → FSDM Element Mapping

The sheet maps each CIF concept to the FSDM table(s) and element(s) that carry it.
Column layout (0-indexed, col 1 = first data col):

| Col | Heading |
|---|---|
| 1 | CIF Universal Dimension |
| 2 | CIF Key Dimension |
| 3 | CIF Entity |
| 5 | CIF Element Name |
| 11–14 | FSDM Subject Area / Area / Entity Type / Entity Name |
| 15 | FSDM Element Name |
| 17 | Mapping Logic |
| 18 | FSDM Data Type |
| 27–28 | Min Value / Max Value |
| 21–23 | FSAS Entity / FSAS Attribute / FSAS Mapping Logic |
| 30–32 | CJF Label / Entity Name / Element Name |

#### CIF Dimension → FSDM Entity Mapping (key rows)

**IDENTITY / Customer**

| CIF Element | FSDM Entity | FSDM Element | Mapping Logic |
|---|---|---|---|
| Customer Identifier | PARTY, INDIVIDUAL / ORGANIZATION | Party Id | PARTY with INDIVIDUAL (private) or ORGANIZATION (commercial) subtypes |
| Account ID | AGREEMENT, PARTY_ASSET, FINANCIAL_AGREEMENT | Agreement Id | From Party to Party (subtype HOUSEHOLD) via PARTY RELATED |
| Household ID | PARTY, HOUSEHOLD, PARTY RELATED | Related Party Id, Party Id | Party Subtype Cd of Related Party = Household |
| Relationship Type | PARTY RELATED | Party Related Role Cd | Flexible role codes |
| Party Agreement Role | PARTY AGREEMENT | Party Agreement Role Cd | PARTY → PARTY AGREEMENT → AGREEMENT |

**PROFILE**

| CIF Element | FSDM Entity | FSDM Element | Mapping Logic |
|---|---|---|---|
| Name | INDIVIDUAL NAME | Given Name, Middle Name, Family Name | INDIVIDUAL → INDIVIDUAL NAME via Individual Party Id WHERE current_date BETWEEN Individual Name Start Dt AND Individual Name End Dt |
| Address | LOCATOR, ADDRESS, STREET ADDRESS | Multiple | PARTY → PARTY LOCATOR → LOCATOR → ADDRESS → STREET ADDRESS; Locator Usage Type Cd |
| Address Type | LOCATOR | Locator Usage Type Cd | — |
| Gender | INDIVIDUAL | Gender Type Cd | — |
| Date of Birth | INDIVIDUAL | Birth Dt | — |
| Taxpayer Identifier | PARTY IDENTIFICATION | Party Identification Num | — |
| Account Tenure Type | PARTY AGREEMENT | Party Agreement Role Cd | — |
| Language Preference | PARTY LANGUAGE USAGE | Language Type Cd | WHERE Party Language Usage Type = 'primary spoken language' |
| Prospect Identification | PARTY STATUS | Party Status Cd | WHERE Party Status Dt = max(Party Status Dt) |
| Customer Identifier | PARTY | Party Id | — |

**BEHAVIORAL / Profitability**

| CIF Element | FSDM Entity | FSDM Element | Mapping Logic |
|---|---|---|---|
| Demographics | PARTY DEMOGRAPHIC, DEMOGRAPHIC VALUE | Demographic Cd/Desc, Range/Start/End Val | PARTY → PARTY DEMOGRAPHIC → DEMOGRAPHICS → DEMOGRAPHIC VALUE for particular Demographic Group Cd |
| Marketing Restriction | DEMOGRAPHIC | Marketing Restriction Ind | — |
| Lifestage Segment | PARTY SEGMENT, MARKET SEGMENT | Market Segment Name | — |
| Account Holdings | AGREEMENT PRODUCT | Product Id | PARTY AGREEMENT → AGREEMENT → AGREEMENT PRODUCT |
| Tenure Types | PARTY AGREEMENT | Party Agreement Role Cd | — |
| Product Category | PRODUCT | Product Subtype Cd, Name, Start/End Dt | Full product hierarchy: PRODUCT → PRODUCT FEATURE → FEATURE, PRODUCT GROUP |
| Product Cost | PRODUCT COST | Product Cost Amt | Per Cost Cd WHERE current_date BETWEEN Product Cost Start Dttm AND End Dttm |
| Agreement Metrics (PD Reserve) | AGREEMENT METRIC | Agreement Metric Amt/Cnt/Rate/Qty | Per Metric Type Cd WHERE current_date BETWEEN Start/End Dttm AND selected Time Period Cd |
| Channel Usage | EVENT CHANNEL INSTANCE, CHANNEL INSTANCE, EVENT, EVENT PARTY | Multiple | — |
| Interest Paid / Earned | FINANCIAL EVENT, FINANCIAL EVENT AMOUNT | Event Transaction Amt | Per Financial Event Type Cd, In Out Direction Type Cd |

**PROPENSITY / Attrition**

| CIF Element | FSDM Entity | FSDM Element |
|---|---|---|
| Customer Age | INDIVIDUAL | Birth Dt |
| Customer Since | PARTY AGREEMENT, AGREEMENT | Agreement Open Dttm |
| Number of Dependents | PARTY DEMOGRAPHIC, PARTY DEMOGRAPHIC VALUE | Demographic Cd/Value Cd |
| Primary Wage Earner Ind | PARTY DEMOGRAPHIC | Demographic Cd/Value |
| Customer Occupation | INDIVIDUAL OCCUPATION | — |
| Customers Financial Plan | OPPORTUNITY, OPPORTUNITY STATUS, OPPORTUNITY PARTY | Lead Type Cd, Opportunity Status Cd |
| Sales Channel Preference | PARTY CONTACT PREFERENCE | Channel Type Cd, Contact Preference Type Cd (Sales vs Service) |
| Service Channel Preference | PARTY CONTACT PREFERENCE | (same table, Contact Preference Type Cd = Service) |
| Reported Income | PARTY DEMOGRAPHIC VALUE | Demographic Val |
| Current Customer Profitability | PARTY AGREEMENT, AGREEMENT, AGREEMENT METRIC | Allocation Pct, Agreement Metric Amt |

**CLV**

| CIF Element | FSDM Entity | FSDM Element |
|---|---|---|
| Current Profitability | AGREEMENT METRIC | Agreement Metric Amt (per Metric Type Cd, Time Period Cd) |
| Future CLV | Not in FSDM — predicted from model | — |

**COMPLIANCE / AML**

| CIF Element | FSDM Entity | FSDM Element |
|---|---|---|
| Channel Risk Grade | PARTY AGREEMENT | Risk Grade Id |
| Geographical Area Risk | GEOGRAPHICAL AREA, GEOGRAPHY RISK GRADE | Risk Grade Id |
| Party Risk Grade | PARTY RISK GRADE, PARTY GROUP RISK GRADE | Risk Grade Id |
| Sanction List Screening | WATCH LIST MEMBER, WATCH LIST SOURCE | Subject/Agreement/Party Id |
| KYC Documents | PARTY IDENTIFICATION, PARTY IDENTIFICATION TYPE, STATUS | Multiple |
| Customer Complaints | DIRECT CONTACT EVENT | Contact Event Subtype Cd |
| Complaint Sentiment | DIRECT CONTACT EVENT | Customer Tone Cd |
| Fair Credit Score | PARTY CREDIT REPORT, SCORE | Credit Report Score Num |

**SERVICE / Products**

Product types covered: Deposits (Checking, Savings, Time), Consumer Lending (Card, Installment, Mortgage), Commercial Lending (Unsecured, Real Estate Secured), Wealth Management (Advisory, Brokerage), Portfolio Investments (Treasuries, GSEs, Equity).

All map to: `AGREEMENT, PARTY_ASSET, FINANCIAL_AGREEMENT → <Multiple>` with account-to-product mapping via `AGREEMENT_PRODUCT`.

**STATUS / Origination & Onboarding**

| CIF Element | FSDM Entity | FSDM Element | Logic |
|---|---|---|---|
| Party ID | PARTY | Party Id | — |
| Customer Onboarding Tstmp | PARTY AGREEMENT, AGREEMENT | Agreement Open Dttm | — |
| Customer Status | PARTY, PARTY STATUS | Party Status Cd | WHERE max Party Status Dt |
| Outbound Marketing Eligibility | PARTY SOLICITATION PREFERENCE | Protocol Type | PARTY + CHANNEL TYPE → PARTY SOLICITATION PREFERENCE WHERE current_date BETWEEN Start/End Dt |
| Lead Product / Lead Type | OPPORTUNITY, PROPOSAL | Lead Type Cd, Proposal Id | — |
| Campaign Id | CAMPAIGN | Campaign Id | — |
| Promotion Id | PROMOTION | Promotion Id | — |
| Application Id / Status | APPLICATION, APPLICATION STATUS | Application Status Type Cd | — |
| Agreement Status | AGREEMENT, AGREEMENT STATUS | Agreement Status Type Cd | — |

**TRANSACTION / Payments**

| CIF Element | FSDM Entity | FSDM Element |
|---|---|---|
| Bank Instruments, Debit/Credit Card, P2P | FUNDS TRANSFER EVENT, ACCESS DEVICE EVENT | Funds Transfer Method Type Cd, Channel Type Cd |
| Payment Instrument→Account | FUNDS TRANSFER EVENT | Originating/Destination Agreement Id, Originating/Destination Account Num |
| Account→Transactions | FUNDS TRANSFER EVENT | Originating Agreement Id |
| Transaction→Channel | FUNDS TRANSFER EVENT, ACCESS DEVICE EVENT | Funds Transfer Method Type Cd + Channel Type Cd |

---

### WP3 — Layer 1 (iDM/MDM) → Layer 2 (APBB/DIM) Transformation Rules

2,193 mapping rows (Status: USED ≈ 1,200 / EXCLUDED ≈ 805). **Target Entity types:** `iDM` (FSDM source), `APBB` (building block), `DIM` (dimension), `MDM` (master data), `FACT`, `CIF End DP`, `EFS`. **Source types:** `iDM`, `APBB`, `DIM`, `MDM`, `CJF` (CIF JSON Feed), `ML`, `MDM, APBB`, `EFS`, `CIF End DP`.

#### Key Entity Transformations

**ACCOUNT BB (APBB) ← AGREEMENT (iDM)**
Primary source: `AGREEMENT`. Straight-move for almost all attributes.
Notable non-straight-moves:
- `Agreement Subtype Desc` ← AGREEMENT SUBTYPE (lookup)
- `Statement Cycle Desc` ← DOCUMENT PRODUCTION CYCLE TYPE (lookup on Statement Cycle Cd)
- `Preferred Currency Cd` ← AGREEMENT CURRENCY WHERE Currency Use = "preferred"
- `Preferred Currency Desc` ← CURRENCY (lookup)
- `Account Profitability Score Val` ← AGREEMENT SCORE WHERE most recent model run with Model Type Cd = 'profitability'
- `Agreement Current Status Cd/Desc/Reason` ← ACCOUNT STATUS PIVOT BB (pre-pivoted from ACCOUNT STATUS BB)

**ACCOUNT STATUS PIVOT BB (APBB) ← ACCOUNT STATUS BB**
Pivots AGREEMENT STATUS rows by scheme type into columns:
- `Agreement Current Status Cd` ← WHERE Agreement Status Scheme = `Account Status`
- `Agreement Accrual Status Cd` ← WHERE Agreement Status Scheme = `Accrual Status`
- `Agreement Default Status Cd` ← WHERE Agreement Status Scheme = `Default Status`
- `Agreement Drawn Undrawn Status Cd` ← WHERE Agreement Status Scheme = `Drawn Undrawn Status`
- `Agreement Frozen Status Cd` ← WHERE Agreement Status Scheme = `Frozen Status`
- `Agreement Past Due Status Cd` ← WHERE Agreement Status Scheme = `Past Due Status`

**ACCOUNT STATUS BB (APBB) ← AGREEMENT STATUS (iDM)**
Straight move of all status fields; desc lookup from AGREEMENT STATUS TYPE, REASON TYPE, SCHEME TYPE.

**ACCOUNT DIMENSION (DIM) ← ACCOUNT BB (APBB)**
Mostly straight-move. Key derived fields:
- `Customer Account Ind` ← PARTY AGREEMENT.Party Agreement Role Cd = "Customer" or similar → set to "1"
- `Product Cd` ← PRODUCT.Host Product Num WHERE AGREEMENT PRODUCT.Agreement Product Role Cd = "primary"
- `Product Desc` ← PRODUCT.Product Name (same condition)

**ACCOUNT STATUS DIMENSION (DIM) ← ACCOUNT STATUS PIVOT BB (APBB)**
Straight-move. One derived field:
- `Frozen Ind` ← set to "1" if frozen status code description = frozen, else "0"

**INDIVIDUAL BB (APBB) ← INDIVIDUAL (iDM)**
Straight-move for core fields. Key lookups:
- `Gender Cd/Desc` ← GENDER TYPE (lookup on Gender Type Cd)
- `Gender Pronoun Cd/Desc` ← GENDER PRONOUN (lookup)
- `Marital Status Cd/Desc` ← MARITAL STATUS TYPE
- `Nationality Cd/Name` ← NATIONALITY TYPE
- `Language Cd/Desc` ← LANGUAGE TYPE (WHERE party Language Usage Type = 'primary spoken language')
- `Language Written Cd/Desc` ← (WHERE party Language Usage Type = 'primary written language')
- `Customer Ind` ← PARTY RELATED WHERE Party Related Role = 'customer of enterprise'
- `Prospect Ind` ← PARTY RELATED WHERE Party Related Role = 'prospect of enterprise'
- `Associate Ind` ← PARTY RELATED WHERE Party Related Role = 'employee of enterprise'
- `Retail Banking Customer Ind` ← PARTY AGREEMENT WHERE role = 'customer' for retail banking product
- `Borrower Ind` ← PARTY AGREEMENT WHERE role = 'borrower'
- `High Net Worth Ind` ← INDIVIDUAL VIP STATUS WHERE VIP Type = high-net-worth
- `VIP Type Cd/Desc` ← INDIVIDUAL VIP STATUS (lookup on VIP Type)
- `Occupation Type Cd/Desc` ← INDIVIDUAL OCCUPATION → OCCUPATION TYPE (lookup)
- Identification pivots: SSN, Passport, Driver's License, Federal Tax Id, etc. ← PARTY IDENTIFICATION WHERE Party Identification Type = specific type
- `FICO Score Val` ← PARTY CREDIT REPORT SCORE
- `Customer Profitability Score Val` ← PARTY SCORE WHERE Model Purpose = 'customer profitability'

**CUSTOMER DIMENSION (DIM) ← INDIVIDUAL BB / ORGANIZATION BB (APBB)**
Straight-move. Note: "unmapped in doc" flag. All 80+ attributes from INDIVIDUAL BB flow through.

**ADDRESS BB (APBB) ← STREET ADDRESS BB / PARCEL ADDRESS BB / POST OFFICE BOX ADDRESS BB**
Street address fields straight-moved; parcel and PO Box fields added.

**STREET ADDRESS BB (APBB) ← STREET ADDRESS (iDM)**
Multiple lookups: CITY (city name for city cd), COUNTRY BB (for territory chain), TERRITORY BB, COUNTY BB, POSTAL CODE.
Notable: `Territory Group Cd/Name` ← `TERRITORY BB WHERE Territory Standard Type = 'ISO 3166-2'` via `REGION BB`.

**ADDRESS DIMENSION (DIM) ← ADDRESS BB**
Straight-move of all address fields.

**PARTY PRIMARY LANGUAGE BB (APBB) ← INDIVIDUAL (iDM)**
Language fields from PARTY LANGUAGE USAGE filtered by Usage Type.

**ORGANIZATION BB (APBB) ← ORGANIZATION (iDM)**
Includes business name lookups (brand name, business name, legal name, registered name from ORGANIZATION NAME WHERE Name Type = specific value).
Industry code pivot: NAICS WHERE Primary NAICS Ind = 'Y', SIC WHERE Primary SIC Ind = 'Y', GICS WHERE Primary GICS Ind = 'Y'.
Legal classification, business category.

**CAMPAIGN BB (APBB) ← CAMPAIGN (iDM)**
Campaign status → SELECT most recent Campaign Status Dttm.

**PROMOTION BB (APBB) ← PROMOTION (iDM)**
Up to 5 Promotion Offer Ids: "For the 1st/2nd/3rd/4th/5th Promotion Offer Id associated with the Promotion Id".

**CHANNEL INSTANCE BB (APBB) ← CHANNEL INSTANCE (iDM)**
Lookups: CHANNEL TYPE (for Channel Type Desc), CHANNEL INSTANCE SUBTYPE, CONVENIENCE FACTOR TYPE.

**LOAN ACCOUNT BB (APBB) ← LOAN AGREEMENT (iDM)**
Interest Rate Index Cd ← AGREEMENT FEATURE WHERE Feature Subtype = "Rate Feature".
Original Loan Term ← AGREEMENT FEATURE WHERE Feature Classification = "Original Loan Term".

**INDIVIDUAL IDENTIFICATION PIVOT BB (APBB) ← PARTY IDENTIFICATION**
One column per identification type (SSN, Passport, Driver License, Federal Tax Id, Employment Auth, Student Number, National Id, DUNS, Legal Entity Identifier).

---

### WP2 FSDM Customizations — Extended/New Tables

Tables added to standard FSDM:

#### PARTY CONTACT PREFERENCE
Replaces PARTY SOLICITATION PREFERENCE; distinguishes Sales vs Service preferences.

| Element | Description |
|---|---|
| Party Id (PK) | Party FK |
| Channel Type Cd | Channel type |
| Contact Preference Type Cd | **'Sales' or 'Service'** — custom extension |
| Party Contact Preference Start Dt | Validity from |
| Party Contact Preference End Dt | Validity to |
| Party Contact Preference Priority Num | Priority ordering |
| Protocol Type Cd | Contact rule protocol |
| Days Cd | Calendar day constraints |
| Hours Cd | Calendar hour constraints |

#### MULTIMEDIA OBJECT LOCATOR
Adds missing link between MULTIMEDIA OBJECT and ELECTRONIC ADDRESS (URI in object store).

| Element | Description |
|---|---|
| MM Object Id (PK) | FK to MULTIMEDIA OBJECT |
| Locator Id (PK) | FK to LOCATOR |
| MM Locator Reason Cd | Purpose (link to object store URI) |
| MM Locator Start Dt | 2025-09-05 example |
| MM Locator End Dt | 2999-12-31 (open-ended) |

#### COMPLAINT EVENT (subtype of EVENT)
| Element | Description |
|---|---|
| Event Id (FK) | Link to EVENT |
| Event Sentiment | Derived sentiment |
| Event Channel Type Cd | Channel used |
| Event Received Dttm | When received |
| Event Txt | Complaint text |
| Event Multimedia Object Ind | Has multimedia link? |

#### PARTY TASK (one per Complaint)
| Element | Description |
|---|---|
| Task Id (PK) | — |
| Party Id (PK/FK) | — |
| Source Event Id (FK) | Link to Complaint Event |
| Task Activity Type Cd | — |
| Task Subtype Cd | — |
| Task Reason Cd | — |

#### PARTY TASK STATUS
| Element | Description |
|---|---|
| Task Id (FK) | — |
| Task Status Start Dttm | — |
| Task Status End Dttm | — |
| Task Status Type Cd | — |
| Task Status Reason Cd | — |
| Task Status Txt | — |

#### TASK ACTIVITY (splits task into steps)
| Element | Description |
|---|---|
| Activity Id (PK) | — |
| Task Id (FK) | — |
| Activity Type Cd | — |
| Activity Txt | — |
| Activity Channel Id | — |
| Activity Start Dttm | — |
| Activity End Dttm | — |

#### TASK ACTIVITY STATUS
Similar structure to PARTY TASK STATUS with Activity Id FK.

---

### WP3 FSAS Cust 360 — FSAS Customizations & Fact Table Catalogue

**FSAS customizations:**
- Replace Product ID with MDM Product ID (from PIM)
- Replace Party Id with MDM Party ID (CDM)

**Available Standard Fact Tables (100+)** — organized by area:

| Area | Example Fact Tables |
|---|---|
| Application | APPLICATION STATUS ACCUMULATING FACT |
| Case | CUSTOMER SERVICE CASE ACCUMULATING FACT |
| Channel | ATM CHANNEL TRANSACTION FACT, BRANCH CHANNEL TRANSACTION FACT, CALL CENTER CHANNEL TRANSACTION FACT, MOBILE APPLICATION CHANNEL TRANSACTION FACT, MULTICHANNEL TRANSACTION FACT, WEB CHANNEL TRANSACTION FACT |
| Customer | ALERT EVENT CLIENT FACTLESS FACT, CREDIT SCORE EVENT FACT, CUSTOMER ACCOUNT FACTLESS FACT, CUSTOMER INCOME REPORTING EVENT FACT, CUSTOMER PRODUCT FACTLESS FACT, CUSTOMER RELATIONSHIP FACTLESS FACT |
| Deposit Account | DEPOSIT ACCOUNT DAILY SNAPSHOT FACT, DEPOSIT ACCOUNT TRANSACTION FACT |
| General Ledger | GL ACCOUNT DAILY SNAPSHOT FACT, **GL ACCOUNT MONTHLY SNAPSHOT FACT**, GL ACCOUNT TRANSACTION FACT |
| Investment | 20+ investment facts |
| Lending | 20+ lending facts (loan, mortgage, credit card, etc.) |
| Marketing | CAMPAIGN COST EVENT FACT, CONTACT EVENT FACTLESS FACT, PROMOTION OFFER FACTLESS FACT |
| Product | PRODUCT FEATURE FACTLESS FACT |

**Custom Fact Tables (CIF-specific):**

**GL ACCOUNT MONTHLY SNAPSHOT FACT** (extended):

| Element | Type |
|---|---|
| Account Key | dim: ACCOUNT DIMENSION |
| Daily Date Key | dim: DATE DIMENSION |
| Domestic Currency Account Balance Amt | Non-aggregative |
| Reporting Currency Interest Earned | Aggregative |
| Reporting Currency Interest Paid | Aggregative |
| Reporting Currency Fraud Mitigation Cost | Aggregative |
| Reporting Currency Other Product Cost | Aggregative |
| Reporting Currency Probability of Default Reserve | Non-aggregative |
| Reporting Currency Fees For Product Holding | Aggregative |
| Reporting Currency Service-related Fees | Aggregative |
| CDM Party Key | dim: CUSTOMER DIMENSION |
| Average Deposit Balance | Non-aggregative |
| Credit Card Balance | Non-aggregative |
| Total Investments | Aggregative |

**CIF CUSTOMER PRODUCT FACTLESS FACT** (custom):

| Element | Dimension / Type |
|---|---|
| CDM Party Key | CUSTOMER DIMENSION |
| Daily Date Key | DATE DIMENSION |
| Product Checking Flag | flag |
| Product Savings Flag | flag |
| Product Credit Card Flag | flag |
| Product Vehicle Loan Flag | flag |
| Product Mortgage Loan Flag | flag |
| Product Home Equity Loan Flag | flag |
| Product Investments Flag | flag |
| Service Online Bill Pay Flag | conditional on Checking |
| Service Debit Card Flag | conditional on Checking |
| Service FICO Score Flag | conditional on Checking |
| Service Safebox Flag | conditional on Checking |
| Payment Cash/Paper Check/Credit Card/ACH/P2P/MoneyTransfer/PayPal/Venmo/Zelle/ApplePay/GooglePay Flag | payment instrument flags |
| Channel ATM/Teller/Banker/IVRU/Phone Agent/Digital/Chatbot/Secure Messages/Email Flag | channel flags |
| Imputed Monthly Income | numeric |
| Customer Tenure | numeric (duration) |

Note: `CUSTOMER PRODUCT FACTLESS FACT.Customer Address Key` → ADDRESS DIMENSION is the **only link between Customer and Address in FSAS** — should be sourced from MDM.

**CIF CUSTOMER ACTIVITY FACTLESS FACT**:

| Element | Dimension |
|---|---|
| CDM Party Key | CUSTOMER DIMENSION |
| Daily Date Key | DATE DIMENSION |
| Channel Key | CHANNEL DIMENSION |
| Activity Type Cd | ACTIVITY DIMENSION |
| Number of Activities | Aggregative |
| Channel Activity Cost | Aggregative |

**Selected FSAS Dimensions (defined in this sheet):**

**ACCOUNT DIMENSION:**
Account Key, Account Num, Account Name, Account Open/Close Dttm, Account Planned Expiration Dt, Account Signed Dt, Account Legally Binding Ind, Account Obtained Cd/Desc, Account Processing Dt, Asset Liability Cd/Desc, Account Type Cd/Desc, Balance Sheet Cd/Desc, Statement Cycle Cd/Desc, Statement Mail Type Cd/Desc, Account Profitability Score Val, Account Status Cd/Desc, Preferred Currency Cd/Desc, **Customer Account Ind**, Product Cd, Product Desc, **Product CLV Type** (MDM PIM CLV product grouping — 8–16 groups).

**ACCOUNT STATUS DIMENSION:** Account Status Key, Account Status Cd/Desc, Account Status Reason Cd/Desc, Accrual Status Cd/Desc, Past Due Status Cd/Desc, Account Default Status Cd/Desc, Drawn Undrawn Status Cd/Desc, **Frozen Ind**.

**ADDRESS DIMENSION:** Address Key, Address Line 1–3, Postal Cd, City Cd/Name, County Cd/Name, Territory Cd/Name/Group Cd/Name, Country Cd/Name, Lat/Long, Geospatial, Elevation, Post Office Box Num, Address Num, Street Direction, Street Num/Name/Suffix, Building/Unit/Floor/Workspace Num, Route/Carrier/Mail fields.

**CUSTOMER DIMENSION** (80+ attributes — note: "unmapped in doc"):
CDM Party Id, Customer Key/Num, Given Name, Middle Name, Family Name, Full Name, Birth Dt, Gender Cd/Desc/Pronoun, Marital Status Cd/Desc, Nationality Cd/Desc, Preferred Language Cd/Desc, Occupation Type Cd/Desc, Social Security Num, Federal Tax Identification Num, National Identification Num, Passport Num, Driver License Num, Employment Auth Num, FICO Score Val, Customer Status Cd/Desc, Customer Type Cd/Desc, Customer Segment Cd/Desc, Customer Profitability Score Val, Retail Banking Customer Ind, Borrower Ind, Associate Ind, Customer Ind (via PARTY RELATED role), VIP Type Cd/Desc, Tax Bracket Cd/Desc, Legal Classification Cd/Desc, Business Category Cd/Desc, Business Legal Name/Start Dt, Primary NAICS/SIC Cd/Desc, Accommodation Cd/Desc/Required Ind, Military Status Type Cd/Desc, High Net Worth Ind, Insurance Claim Third-Party Ind, Pay/Bonus timing, Retirement Dt, Skill Cd/Desc, Ethnicity Type Cd/Desc, Party Since, + 30+ more individual/medical/occupation fields.

**PROMOTION DIMENSION:** Promotion Key/Id, Desc, Start/End Dt, Goal Amt, Type Cd/Desc, Objective, Actual Unit Cost/Cnt, Break Even Order Cnt, Internal Name, Currency Cd.

**CAMPAIGN DIMENSION:** Campaign Key/Id, Strategy Cd/Desc, Desc, Start/End Dt, Type Cd/Desc, Name, Estimated Cost Amt, Estimated Base Customer Cnt, Status Dttm/Cd/Desc.

**CHANNEL DIMENSION:** Channel Key, Channel Instance Id, Channel Type Cd/Desc, Channel Instance Name, Start/End Dt, Convenience Factor Cd/Desc, Channel Status Cd/Desc.

**DATE DIMENSION:** Date Key, Day Dt, Day/Week/Month/Quarter/Year numbers, Fiscal variants, Holiday/Weekend indicators.

**ACTIVITY TYPE DIMENSION:** Activity Type Cd, Name, Description, Start/End Dt.

---

### WP4 MDM — Master Data Management Layer

#### PIM (Product Information Management)

| Entity | Element | Description |
|---|---|---|
| PRODUCT | PIM Id (PK) | Surrogate key |
| PRODUCT | Product Id | Reference to FSDM Product Id |
| PRODUCT | PIM Product Name | PIM-managed product name |
| PRODUCT | PIM Product Desc | — |
| PRODUCT | Valid From / Valid To / Del Ind | SCD tracking |
| PRODUCT PARAMETERS | PIM Parameter Id (PK), PIM Id (FK), PIM Parameter Type Cd, PIM Parameter Value | Maps to FSDM PRODUCT FEATURES/FEATURES |
| PRODUCT PARAMETER TYPE | PIM Parameter Type Cd/Desc | Code table |
| PRODUCT TO GROUP | PIM Id, Group Id, Valid From/To/Del Ind | — |
| PRODUCT GROUP | Product Group Id, Parent Group Id, Product Group Type Cd, Valid From/To/Del Ind | — |
| PRODUCT GROUP TYPE | Type Cd/Name/Desc | — |

**Product Taxonomy (L2 → L1 examples):**
- Deposits → Checking / Savings / Time
- Consumer Lending → Card / Installment / Mortgage
- Commercial Lending → Unsecured / Real Estate Secured
- Wealth Management → Advisory / Brokerage
- Portfolio Investments → Treasuries / GSEs / Equity

#### CDM (Customer Data Model — Party-Object-Location-Event)

**Party cluster:**

| Entity | Key Fields |
|---|---|
| PARTY (CDM) | CDM Party Id, Source Cd, Source Party Id, Party Type Cd (Individual/Organization), Party Lifecycle Phase Cd, Party Since, Valid From/To/Del Ind, Survival Record Ind, DQ Score |
| INDIVIDUAL (CDM) | CDM Party Id, First Name, Middle Name, Last Name, Birth Dt, Gender, Salutation, Valid From/To/Del Ind |
| INDIVIDUAL HISTORY (CDM) | _(entity present in workbook; no attribute columns populated)_ |
| ORGANIZATION (CDM) | CDM Party Id, Organization Name, Business Identifier, Valid From/To/Del Ind |
| HOUSEHOLD | CDM Household Id, Household Name/Desc, Valid From/To/Del Ind |
| INDIVIDUAL TO INDIVIDUAL | CDM Party Id, Parent CDM Party Id, Relationship Type/Value Cd, Probability, Valid From/To/Del Ind |
| INDIVIDUAL TO HOUSEHOLD | CDM Party Id, CDM Household Id, Role Type Cd, Probability, Valid From/To/Del Ind |
| INDIVIDUAL TO ORGANIZATION | CDM Party Id, Parent CDM Party Id, Relationship Type/Value Cd, Probability, Valid From/To/Del Ind |
| ORGANIZATION TO ORGANIZATION | CDM Party Id, Parent CDM Party Id, Relationship Type/Value Cd, Probability, Valid From/To/Del Ind |
| PARTY TO AGREEMENT ROLE | CDM Party Id, Agreement Id, Role Type Cd, Valid From/To/Del Ind |
| PARTY TO EVENT ROLE | CDM Party Id, Event Id, Role Type Cd, Valid From/To/Del Ind |
| PARTY SEGMENT (CDM) | CDM Party Id, Segment Type Cd (CLV/Behavioral/Risk), Segment Value Cd, Valid From/To/Del Ind |

**Location:**

| Entity | Key Fields |
|---|---|
| ADDRESS (CDM) | CDM Party ID, Address Id, Address Type, Country/County/City/Street/Postal Code, Primary Address Flag, Geo Lat/Long, Valid From/To/Del Ind |
| ADDRESS TO AGREEMENT | Address Agreement Id (PK), Address Id, Agreement Id, Valid From/To/Del Ind |

**Object:**

| Entity | Key Fields |
|---|---|
| CONTACT | Contact Id, Contact Type Cd, Contact Value, Primary Contact Ind, Valid From/To/Del Ind |
| CONTACT TO AGREEMENT | Contact Agreement Id (PK), Contact Id, Agreement Id, Valid From/To/Del Ind |

**Events:**

| Entity | Key Fields |
|---|---|
| PARTY INTERACTION EVENT | Event Id, CDM Party Id, Event Type Cd, Event Channel Type Cd, Event Dt, Event Sentiment Cd |

---

### WP5 Feature Store

#### Technical columns in every Feature Group:
Feature Group Id, Primary Key(s), Feature Id, Feature Version Id, Feature Value, Feature Population Dttm.

#### Feature Groups:

**BANK (primary key: Constant)**
- Target Return on Equity (constant — discount rate for CLV)
- CLV Planning Horizon (constant)
- Effective Marginal Tax Rate (constant)

**CUSTOMER (primary key: Party ID)**
- Customer Contribution to Profit (FSAS Facts)
- Product Type 1–8 Holding Ind (FSAS Account Dimension)
- Interest Earned / Paid (FSAS Facts)
- Predicted CLV, Pred Net Interest Margin, Pred Non Interest Expense/Income (Calculated)
- Probability of Attrition (Calculated)
- Customer Tenure (calculated from Customer Since)
- Imputed Monthly Income
- Product Checking/Savings/Credit Card/Vehicle Loan/Mortgage/Home Equity/Investments Flag
- Service Online Bill Pay/Debit Card/FICO Score/Safebox Flag (conditional on Checking)
- Payment instrument flags (Cash, Paper Check, Credit Card, ACH, P2P, Money Transfer, PayPal, Venmo, Zelle, ApplePay, GooglePay)
- Channel flags (ATM, Teller, Banker, IVRU, Phone Agent, Digital, Chatbot, Secure Messages, Email)
- Fees Charged Amt, Credit Utilization Pct, Credit Score Val
- Average Deposit Balance Amt, Credit Card Balance Amt, Total Investments AUM Amt
- Customer Profitability Amt, Attrition Flag, Customer Lifetime Value Amt

**CUSTOMER PRODUCT (primary key: Party ID + Product ID)**
- Probability of Default Reserve, Fees For Product Holding, Service-related Fees, Total Product Costs, Fraud Mitigation Costs

**CUSTOMER CHANNEL (primary key: Party ID + Channel Type Cd)**
- Allocation Channel Activity

#### **Numeric Distributions for Synthetic Data** (from WP5):

| Feature | Distribution |
|---|---|
| Average Deposit Balance | Mean $2,000; P10 $10; P90 $30,000; negatives OK |
| Credit Card Balance | Mean $2,500; P10 $100; P90 $20,000; no negatives |
| Total Investments AUM | Mean $75,000; P10 $5,000; P90 $100,000; no negatives |
| Customer Tenure (years) | Mean 3.5; P10 0.5; P90 25; no negatives |
| Imputed Monthly Income | Mean $4,500; P10 $0; P90 $25,000; no negatives |
| Customer Profitability | Mean $125; P10 $0; P90 $2,500; no negatives |
| Customer Lifetime Value | Mean $500; P10 $50; P90 $25,000; no negatives |
| Fees Charged | Needs distribution help |
| Credit History / Utilization | Needs distribution help |

---

### WP7–9 End Data Products

#### CUSTOMER CLV

PK: CDM Party Cluster Id + CLV Hierarchy Type Cd (hierarchy levels: FSDM Party Id / Clustered MDM Customer / Household / Social Group).

CLV hierarchy structure:
```
L0: Total CLV
  L1: Profit Contribution (Current CLV)
    L2: Net Interest Margin
      L3: Interest Earned  ← GL ACCOUNT MONTHLY SNAPSHOT FACT.Reporting Currency Interest Earned
      L3: Interest Paid    ← GL ACCOUNT MONTHLY SNAPSHOT FACT.Reporting Currency Interest Paid
    L2: Non Interest Expense
      L3: Allocation Loan Losses ← GL Reporting Currency Probability of Default Reserve
      L3: Product Cost
        L4: Fraud Mitigation Cost ← GL Reporting Currency Fraud Mitigation Cost
        L4: Other Product Cost    ← GL Reporting Currency Other Product Cost
      L3: Allocation Channel Activity ← CIF CUSTOMER ACTIVITY FACT.Channel Activity Cost
    L2: Non Interest Income
      L3: Fees For Product Holding ← GL Reporting Currency Fees For Product Holding
      L3: Service-related Fees     ← GL Reporting Currency Service-related Fees
  L2: Effective Marginal Tax Rate  ← Feature Store
  L1: Predicted CLV  ← Feature Store
    L2: Pred Net Interest Margin / Non Interest Expense / Non Interest Income ← Feature Store
Probability of Attrition ← Feature Store
Target Return On Equity / Forecast Horizon / Expected Survive Time ← Feature Store
```

Plus all Feature Store flags (product holding, services, payments, channels, financial metrics).

#### CUSTOMER ATTRITION

PK: CDM Party Cluster Id + CLV Hierarchy Type Cd + Calendar Year + Month + Activity Type Cd + Channel Name.
Fields: Number of Activities (from CUSTOMER ACTIVITY FACT).

#### CUSTOMER PROFILE

PK: CDM Party Cluster Id.
Source: FSAS CUSTOMER DIMENSION for most attributes.
Fields: Credit Score Num (FICO Score Val), Customer Geography Name (Nationality Cd), Gender Cd, Type Cd, Date of Birth, Tenure Num, Estimated Salary Amt, Status Cd, Marital Status Cd, Occupation Type Cd, Preferred Language Cd, VIP Type Cd, Valid From/To/Del Ind.
**Note in source:** "FSAS mapping for Preferred Language Cd is not correct — follow the mapping on FSDM sheet."

#### CUSTOMER INTERACTIONS

PK: CDM Party Id + Event Id.
Fields: Channel Type Cd, Channel Name, Event Dttm, Session ID, Event Type Cd. Additional event attributes TBD.

#### JOURNEY SIGNALS / SIGNAL PATTERNS / CUSTOMER JOURNEY SIGNAL PATTERNS

Journey pattern detection tables linking customers to event sequences (association rule mining: Pattern Id, Signal Type Cd, Signal Frequency, Signal Yield).

#### CUSTOMER COMPLAINTS / RESOLUTIONS / RESOLUTION EVENTS

Structured complaint lifecycle tracking with sentiment, channel, resolution steps.

---

### Metadata (AI/ML Structuralization Lineage)

Three tables to track provenance of structured fields derived from unstructured data:

| Entity | Purpose |
|---|---|
| SOURCE | References to unstructured source objects (URI, type) |
| SOURCE TO TARGET | Links source → target entity/element (from Data Catalog) + Model Id |
| MODEL | Model registry (Id, name, URI, accuracy) |

---

### GRAPH Entities — Full Entity Catalogue

**iDM entities (Layer 1 source):** AGREEMENT (and 8 subtypes/type tables), AGREEMENT CURRENCY, AGREEMENT SCORE, PARTY AGREEMENT, PRODUCT (and FEATURE, PRODUCT FEATURE, PRODUCT GROUP hierarchy), AGREEMENT STATUS (and 3 type tables), ADDRESS, CHANNEL INSTANCE (and CHANNEL TYPE, SUBTYPE, CONVENIENCE FACTOR TYPE, STATUS TYPE), CAMPAIGN (and 4 type/status tables), CARD, AGREEMENT FEATURE, FINANCIAL AGREEMENT (and MARKET RISK TYPE, TRADING BOOK TYPE, DAY COUNT BASIS TYPE), DEPOSIT AGREEMENT, DEPOSIT TERM AGREEMENT, FEATURE (and SUBTYPE, INSURANCE SUBTYPE, CLASSIFICATION TYPE), INDIVIDUAL (and NAME, GENDER PRONOUN, MARITAL STATUS, VIP STATUS, MILITARY STATUS, OCCUPATION, PAY/BONUS TIMING, SKILL, SPECIAL NEED, MEDICAL, ASSOCIATE EMPLOYMENT), PARTY RELATED, PARTY CLAIM, PARTY SCORE, MARKET SEGMENT, PARTY CREDIT REPORT SCORE, GENDER TYPE, ETHNICITY TYPE, MARITAL STATUS TYPE, NATIONALITY TYPE, TAX BRACKET TYPE, VERY IMPORTANT PERSON TYPE, MILITARY STATUS TYPE, OCCUPATION TYPE, TIME PERIOD TYPE, PARTY RELATED STATUS TYPE, GENERAL MEDICAL STATUS TYPE, PRICING METHOD SUBTYPE, FINANCIAL AGREEMENT TYPE, CREDIT AGREEMENT, LOAN AGREEMENT (and subtypes), CREDIT CARD AGREEMENT (and subtype), LOAN TERM AGREEMENT, MORTGAGE AGREEMENT, TERM FEATURE, INTEREST RATE INDEX, AGREEMENT RATE, VARIABLE INTEREST RATE FEATURE, INTEREST INDEX RATE, ORGANIZATION (and NAME, BUSINESS, BUSINESS CATEGORY, GICS/NAICS/NACE/SIC hierarchy, SPECIALTY, LEGAL CLASSIFICATION), PARTY IDENTIFICATION, PARTY LANGUAGE USAGE, LANGUAGE TYPE, PROMOTION (and OFFER, TYPE, METRIC TYPE), STREET ADDRESS (and DETAIL, DIRECTION TYPE, STREET SUFFIX TYPE), CITY, COUNTRY, POSTAL CODE, ISO 3166 standards, GEOGRAPHICAL_AREA, GEOSPATIAL_POINT, TERRITORY, REGION, COUNTY, CURRENCY, DATA SOURCE TYPE, RISK EXPOSURE MITIGANT SUBTYPE, + 20 more type/lookup tables.

**APBB entities (Building Blocks):** ACCOUNT STATUS PIVOT BB, ACCOUNT BB, STREET ADDRESS BB, PARCEL ADDRESS BB, POST OFFICE BOX ADDRESS BB, ADDRESS BB, INDIVIDUAL BB, CAMPAIGN BB, CHANNEL INSTANCE BB, LOAN ACCOUNT BB, INDIVIDUAL IDENTIFICATION PIVOT BB, PARTY PRIMARY LANGUAGE BB, PARTY IDENTIFICATION PIVOT BB, ORGANIZATION NAME PIVOT BB, ORGANIZATION IDENTIFICATION PIVOT BB, PROMOTION BB, PROMOTION OFFER PIVOT BB, PROMOTION OFFER BB, ACCOUNT STATUS BB, GEOSPATIAL POINT BB, COUNTRY BB, REGION BB, TERRITORY BB, CITY BB, COUNTY BB, ASSOCIATE BB, FEATURE BB, ORGANIZATION BB.

**DIM entities:** ACCOUNT DIMENSION, ACCOUNT STATUS DIMENSION, ADDRESS DIMENSION, CAMPAIGN DIMENSION, CHANNEL DIMENSION, CREDIT CARD ACCOUNT DIMENSION, DEPOSIT ACCOUNT DIMENSION, INVESTMENT ACCOUNT DIMENSION, LOAN ACCOUNT DIMENSION, LOAN TERM ACCOUNT DIMENSION, MORTGAGE ACCOUNT DIMENSION, PROMOTION DIMENSION, PROMOTION OFFER DIMENSION, RECEIVING ACCOUNT DIMENSION.

---

### FK/PK Relationships

Key relationships (Layer 1 / iDM):

```
PARTY (Party Id PK)
  ├─ INDIVIDUAL (Individual Party Id FK → PARTY.Party Id)
  │    ├─ INDIVIDUAL NAME (Individual Party Id FK)
  │    ├─ INDIVIDUAL VIP STATUS (Individual Party Id FK)
  │    ├─ INDIVIDUAL OCCUPATION (Individual Party Id FK)
  │    └─ INDIVIDUAL MEDICAL / MILITARY STATUS / SKILL / SPECIAL NEED / MARITAL STATUS / GENDER PRONOUN / ASSOCIATE EMPLOYMENT / BONUS/PAY TIMING
  ├─ ORGANIZATION (Organization Party Id FK → PARTY.Party Id)
  │    ├─ ORGANIZATION NAME (Organization Party Id FK)
  │    ├─ ORGANIZATION GICS / NACE / NAICS / SIC
  │    ├─ BUSINESS (Organization Party Id FK)
  │    └─ PARTY SPECIALTY / LEGAL CLASSIFICATION
  ├─ PARTY AGREEMENT (Party Id FK) → AGREEMENT (Agreement Id PK)
  ├─ PARTY LOCATOR (Party Id FK) → LOCATOR → ADDRESS → STREET ADDRESS (or PARCEL, POST OFFICE BOX)
  ├─ PARTY IDENTIFICATION (Party Id FK)
  ├─ PARTY LANGUAGE USAGE (Party Id FK) → LANGUAGE TYPE
  ├─ PARTY STATUS (Party Id FK)
  ├─ PARTY DEMOGRAPHIC (Party Id FK) → DEMOGRAPHIC → DEMOGRAPHIC VALUE
  ├─ PARTY SEGMENT (Party Id FK) → MARKET SEGMENT
  ├─ PARTY RELATED (Party Id FK, Related Party Id FK) — self-referential
  ├─ PARTY CLAIM (Party Id FK)
  ├─ PARTY SCORE (Party Id FK) → ANALYTICAL MODEL
  ├─ PARTY CREDIT REPORT SCORE (Party Id FK)
  ├─ PARTY RISK GRADE (Party Id FK)
  ├─ PARTY SOLICITATION PREFERENCE / PARTY CONTACT PREFERENCE (Party Id FK)
  └─ EVENT PARTY (Party Id FK) → EVENT

AGREEMENT (Agreement Id PK)
  ├─ AGREEMENT PRODUCT (Agreement Id FK) → PRODUCT (Product Id PK)
  ├─ AGREEMENT STATUS (Agreement Id FK) → AGREEMENT STATUS TYPE / REASON TYPE / SCHEME TYPE
  ├─ AGREEMENT CURRENCY (Agreement Id FK) → CURRENCY
  ├─ AGREEMENT SCORE (Agreement Id FK) → ANALYTICAL MODEL
  ├─ AGREEMENT FEATURE (Agreement Id FK) → FEATURE (Feature Id PK)
  ├─ AGREEMENT METRIC (Agreement Id FK)
  ├─ AGREEMENT RATE (Agreement Id FK)
  ├─ FINANCIAL AGREEMENT (Agreement Id FK)
  │    ├─ DEPOSIT AGREEMENT / DEPOSIT TERM AGREEMENT
  │    ├─ CREDIT AGREEMENT → LOAN AGREEMENT / CREDIT CARD AGREEMENT / MORTGAGE AGREEMENT
  │    └─ LOAN TERM AGREEMENT
  └─ PARTY AGREEMENT (Agreement Id FK)

PRODUCT (Product Id PK)
  ├─ PRODUCT FEATURE (Product Id FK, Feature Id FK) → FEATURE
  ├─ PRODUCT COST (Product Id FK)
  └─ PRODUCT TO PRODUCT GROUP (Product Id FK) → PRODUCT GROUP

EVENT (Event Id PK)
  ├─ EVENT PARTY (Event Id FK) → PARTY
  ├─ EVENT CHANNEL INSTANCE (Event Id FK) → CHANNEL INSTANCE
  ├─ EVENT LOCATOR (Event Id FK) → LOCATOR
  ├─ EVENT MULTIMEDIA OBJECT (Event Id FK) → MULTIMEDIA OBJECT → MULTIMEDIA OBJECT LOCATOR → LOCATOR → ELECTRONIC ADDRESS
  ├─ FINANCIAL EVENT (Event Id FK)
  │    └─ FINANCIAL EVENT AMOUNT (Event Id FK)
  ├─ FUNDS TRANSFER EVENT (Event Id FK) — links ORIGINATING AGREEMENT + DESTINATION AGREEMENT
  ├─ ACCESS DEVICE EVENT (Event Id FK) — includes Channel Type Cd
  └─ DIRECT CONTACT EVENT (Event Id FK) — Customer Tone Cd (Sentiment)

CHANNEL INSTANCE (Channel Instance Id PK) → CHANNEL TYPE
```

---

## Step 3 — Generator Notes

### Which Layer 2 rules require specific Layer 1 column structures?

1. **ACCOUNT STATUS PIVOT BB** requires AGREEMENT STATUS to have records for **all six scheme types**:
   - `Account Status`, `Accrual Status`, `Default Status`, `Drawn Undrawn Status`, `Frozen Status`, `Past Due Status`
   - Without these, the pivoted status columns in ACCOUNT STATUS DIMENSION will be null.

2. **Lookup DESC columns** (106 distinct lookup rules) require reference/code tables to be populated. Each `Look up desc for the code value presented in <ENTITY>` rule requires the corresponding type table to have the code as a PK row. Example: `AGREEMENT.Agreement Subtype Cd` must exist as a PK in `AGREEMENT SUBTYPE` for the ACCOUNT BB join to resolve.

3. **INDIVIDUAL NAME date-range filter**: `WHERE current_date BETWEEN Individual Name Start Dt AND Individual Name End Dt` — Name records must have valid date ranges that include the simulation date.

4. **PARTY LANGUAGE USAGE type filter**: Language records must have `Language Usage Type Cd` = 'primary spoken language' and 'primary written language' for the language columns in INDIVIDUAL BB to populate.

5. **PARTY STATUS recency filter**: `WHERE Party Status Dt = max(Party Status Dt)` — requires at least one PARTY STATUS record per party.

6. **AGREEMENT FEATURE Rate Feature filter**: For `LOAN ACCOUNT BB.Interest Rate Index Cd`, AGREEMENT FEATURE must exist with Feature Id where `FEATURE.Feature Subtype Cd = 'Rate Feature'` for the relevant Agreement Id.

7. **AGREEMENT PRODUCT primary role filter**: `ACCOUNT DIMENSION.Product Cd` and `Product Desc` require `AGREEMENT PRODUCT.Agreement Product Role Cd = 'primary'` for the Agreement.

8. **AGREEMENT CURRENCY preferred filter**: `ACCOUNT BB.Preferred Currency Cd` requires `AGREEMENT CURRENCY` with a Use Type Cd = 'preferred' or similar.

9. **Customer Account Indicator**: `ACCOUNT DIMENSION.Customer Account Ind = '1'` requires `PARTY AGREEMENT.Party Agreement Role Cd = 'Customer'`.

10. **INDIVIDUAL BB indicator derivations**: PARTY RELATED must have records with role codes:
    - `'customer of enterprise'` → Customer Ind = 'Y'
    - `'prospect of enterprise'` → Prospect Ind = 'Y'
    - `'employee of enterprise'` → Associate Ind = 'Y'

11. **Borrower Ind**: PARTY AGREEMENT must have `Party Agreement Role Cd = 'borrower'`.

12. **Retail Banking Customer Ind**: PARTY AGREEMENT must have role = 'customer' linked to a retail banking Agreement.

13. **ACCOUNT STATUS DIMENSION.Frozen Ind**: frozen status code description must match literal value 'frozen' (case-insensitive assumed).

14. **Organization industry pivot (ORGANIZATION BB)**: Exactly one record in ORGANIZATION NAICS with `Primary NAICS Ind = 'Y'`, one in ORGANIZATION SIC with `Primary SIC Ind = 'Y'`, and one in ORGANIZATION GICS with `Primary GICS Ind = 'Y'`.

15. **CAMPAIGN BB.Campaign Status**: Requires CAMPAIGN STATUS records; the rule selects `most recent Campaign Status Dttm`.

16. **PROMOTION BB (5 offers)**: If generator creates fewer than 5 PROMOTION OFFER records per Promotion, higher-order offer columns will be null — which is acceptable.

17. **AGREEMENT SCORE → Account Profitability Score Val**: Requires ANALYTICAL MODEL with `Model Type Cd = 'profitability'` and a corresponding AGREEMENT SCORE record.

18. **PARTY SCORE → Customer Profitability Score Val in INDIVIDUAL BB**: Requires ANALYTICAL MODEL with `Model Purpose = 'customer profitability'` and a PARTY SCORE record per party.

19. **Territory chain for addresses**: STREET ADDRESS BB → TERRITORY BB → REGION BB requires `Territory Standard Type = 'ISO 3166-2 Country Subdivision Standard'`.

20. **PRODUCT CLV Type** in ACCOUNT DIMENSION: requires MDM PIM product grouping with `Product Group Type Cd = 'CLV'` — this is an MDM-level extension not natively in FSDM.

21. **Frozen Ind derivation**: Need `AGREEMENT STATUS.Agreement Status Scheme Cd = 'Frozen Status'` AND a valid code/desc = 'frozen'.

22. **INDIVIDUAL IDENTIFICATION PIVOT BB**: Each identification type column requires a PARTY IDENTIFICATION record with the matching Party Identification Type code. Types needed: SSN, Passport, Driver's License, Federal Tax Id, Employment Authorization Number, Student Number, National Identification Number, DUNS Number, Legal Entity Identifier.

### Which columns must not be null?

| Table | Column | Required Because |
|---|---|---|
| PARTY | Party Id | PK — all other tables FK to this |
| INDIVIDUAL | Individual Party Id | FK to PARTY; needed for name/gender/DOB lookups |
| AGREEMENT | Agreement Id | PK — all account transforms pivot on this |
| AGREEMENT | Agreement Open Dttm | Needed for Customer Tenure / Customer Since calculation |
| AGREEMENT STATUS | Agreement Id, Agreement Status Scheme Cd, Agreement Status Cd | Needed for ACCOUNT STATUS PIVOT BB (6-way pivot) |
| AGREEMENT STATUS | Agreement Status Start Dttm | For temporal filtering |
| PARTY AGREEMENT | Party Id, Agreement Id, Party Agreement Role Cd | Needed for Customer Account Ind, Borrower Ind, Customer Ind derivations |
| AGREEMENT PRODUCT | Agreement Id, Product Id, Agreement Product Role Cd | Role Cd must have at least one 'primary' per Agreement for Product Cd in ACCOUNT DIM |
| INDIVIDUAL NAME | Individual Party Id, Name Type Cd, Individual Name Start Dt, Individual Name End Dt | Date-range filter for current name; Name Type Cd must match expected value |
| PARTY LANGUAGE USAGE | Party Id, Language Type Cd, Language Usage Type Cd | Filter: 'primary spoken language' required for Language Cd in DIM |
| PARTY STATUS | Party Id, Party Status Cd, Party Status Dt | Recency filter for Customer/Prospect status |
| PARTY RELATED | Party Id, Related Party Id, Party Related Role Cd | Needed for Customer/Prospect/Associate indicators |
| AGREEMENT CURRENCY | Agreement Id, Agreement Currency Cd, Currency Use Type Cd | Filter: 'preferred' required for Preferred Currency Cd |
| FEATURE | Feature Id, Feature Subtype Cd | Rate Feature subtype needed for loan rate derivation |
| AGREEMENT FEATURE | Agreement Id, Feature Id, Agreement Feature Role Cd | Link for rate and term lookups |
| CHANNEL INSTANCE | Channel Instance Id, Channel Type Cd | Needed for Channel Dimension |
| EVENT | Event Id, Event Start Dttm | Needed for all event-based facts |
| EVENT PARTY | Event Id, Party Id, Event Party Role Cd | Links events to customers |
| FUNDS TRANSFER EVENT | Event Id, Originating Agreement Id | Links payments to accounts |

### Which code/lookup values must exist in Layer 1?

| Code Column | Entity | Required Values |
|---|---|---|
| Agreement Status Scheme Cd | AGREEMENT STATUS | 'Account Status', 'Accrual Status', 'Default Status', 'Drawn Undrawn Status', 'Frozen Status', 'Past Due Status' |
| Party Related Role Cd | PARTY RELATED | `'customer of enterprise'` (→ Customer_Ind='Y'), `'prospect of enterprise'` (→ Prospect_Ind='Y'), `'employee of enterprise'` (→ Associate_Ind='Y') |
| Party Agreement Role Cd | PARTY AGREEMENT | `'customer'` (→ Customer_Account_Ind='1'), `'borrower'` (→ Borrower_Ind), `'guarantor'`, `'co-borrower'`, `'owner'` |
| Agreement Product Role Cd | AGREEMENT PRODUCT | `'primary'` (at least one per Agreement for ACCOUNT DIM.Product Cd) |
| `Currency_Use_Cd` | AGREEMENT CURRENCY | `'preferred'` (→ Preferred Currency Cd in ACCOUNT_BB), `'secondary'`, `'home'`. No FK to lookup table. |
| Language Usage Type Cd | PARTY LANGUAGE USAGE | 'primary spoken language', 'primary written language' |
| Feature Subtype Cd | FEATURE | 'Rate Feature' |
| Feature Classification Cd | FEATURE | 'Original Loan Term' |
| Name Type Cd | INDIVIDUAL NAME / ORGANIZATION NAME | For individuals: current name type; For orgs: 'brand name', 'business name', 'legal name', 'registered name' |
| Contact Preference Type Cd | PARTY CONTACT PREFERENCE | SMALLINT: 1=Sales, 2=Service (see 01_schema-reference.md SMALLINT Code Enumerations) |
| Party Lifecycle Phase Cd | CDM PARTY | 'External', 'Prospect', 'Active Customer' |
| Segment Type Cd | CDM PARTY SEGMENT | 'CLV', 'Behavioral', 'Risk' |
| Model Type Cd | ANALYTICAL MODEL | 'profitability' |
| Model Purpose | ANALYTICAL MODEL | 'customer profitability' |
| Territory Standard Type | ISO 3166 | 'ISO 3166-2 Country Subdivision Standard' |
| Primary [NAICS/SIC/GICS] Ind | ORGANIZATION NAICS/SIC/GICS | 'Y' for exactly one record per org |
| `Agreement_Feature_Role_Cd` | AGREEMENT_FEATURE_ROLE_TYPE | Seed table with: `'primary'`, `'fee'`, `'rate'`, `'term'` |
| `Agreement_Status_Cd` (Frozen scheme) | AGREEMENT_STATUS_TYPE | For `Agreement_Status_Scheme_Cd = 'Frozen Status'`: seed row `Agreement_Status_Cd = 'FROZEN'`, `Agreement_Status_Desc = 'Frozen'` (triggers ACCOUNT_STATUS_DIMENSION.Frozen_Ind='1') |

### FK generation order (dependency sequence)

Generate in this order to satisfy FK constraints:

```
Tier 0 — Reference/lookup tables (no FKs, all code tables):
  AGREEMENT SUBTYPE, AGREEMENT TYPE, AGREEMENT FORMAT TYPE, AGREEMENT OBJECTIVE TYPE,
  AGREEMENT OBTAINED TYPE, ASSET LIABILITY TYPE, BALANCE SHEET TYPE, DOCUMENT PRODUCTION
  CYCLE TYPE, STATEMENT MAIL TYPE, DATA SOURCE TYPE, AGREEMENT STATUS TYPE,
  AGREEMENT STATUS REASON TYPE, AGREEMENT STATUS SCHEME TYPE, GENDER TYPE, GENDER PRONOUN,
  MARITAL STATUS TYPE, NATIONALITY TYPE, LANGUAGE TYPE, ETHNICITY TYPE, TAX BRACKET TYPE,
  VIP TYPE → VERY IMPORTANT PERSON TYPE, MILITARY STATUS TYPE, OCCUPATION TYPE,
  GENERAL MEDICAL STATUS TYPE, SPECIAL NEED TYPE, SKILL TYPE, SPECIALTY TYPE,
  FEATURE SUBTYPE, FEATURE CLASSIFICATION TYPE, FEATURE INSURANCE SUBTYPE,
  CHANNEL TYPE, CHANNEL INSTANCE SUBTYPE, CONVENIENCE FACTOR TYPE, CHANNEL STATUS TYPE,
  CAMPAIGN TYPE, CAMPAIGN STRATEGY TYPE, CAMPAIGN CLASSIFICATION, CAMPAIGN STATUS TYPE,
  STREET SUFFIX TYPE, DIRECTION TYPE, RISK EXPOSURE MITIGANT SUBTYPE,
  PRICING METHOD SUBTYPE, FINANCIAL AGREEMENT TYPE, LOAN MATURITY SUBTYPE,
  LOAN TRANSACTION SUBTYPE, LOAN TERM SUBTYPE, CREDIT CARD AGREEMENT SUBTYPE,
  MORTGAGE TYPE, DEPOSIT MATURITY SUBTYPE, INTEREST DISBURSEMENT TYPE,
  PAYMENT TIMING TYPE, PURCHASE INTENT TYPE, AMORTIZATION METHOD TYPE,
  PARTY RELATED STATUS TYPE, MARKET RISK TYPE, TRADING BOOK TYPE, DAY COUNT BASIS TYPE,
  SECURITY TYPE, UNIT OF MEASURE, CURRENCY, ADDRESS SUBTYPE, PROMOTION OFFER TYPE,
  PROMOTION METRIC TYPE, TIME PERIOD TYPE, BUSINESS CATEGORY

Tier 1 — Geography (no customer FKs):
  COUNTRY, REGION, TERRITORY, COUNTY, CITY, CITY_TYPE, POSTAL CODE,
  ISO_3166_COUNTRY_STANDARD, ISO 3166 COUNTRY SUBDIVISION STANDARD,
  TERRITORY_TYPE, GEOGRAPHICAL_AREA

Tier 2 — Core entities (no parent FKs):
  PARTY (root of customer hierarchy)
  PRODUCT (root of product hierarchy)
  FEATURE (standalone)
  AGREEMENT (before products linked)
  ANALYTICAL MODEL (standalone)
  MARKET SEGMENT (standalone)
  CHANNEL INSTANCE (standalone, FK to CHANNEL TYPE only)
  CAMPAIGN (standalone)

Tier 3 — Party subtypes (FK to PARTY):
  INDIVIDUAL, ORGANIZATION

Tier 4 — Party attributes (FK to INDIVIDUAL/ORGANIZATION/PARTY):
  INDIVIDUAL NAME, INDIVIDUAL VIP STATUS, INDIVIDUAL OCCUPATION,
  INDIVIDUAL MILITARY STATUS, INDIVIDUAL MEDICAL, INDIVIDUAL MARITAL STATUS,
  INDIVIDUAL GENDER PRONOUN, INDIVIDUAL SKILL, INDIVIDUAL SPECIAL NEED,
  INDIVIDUAL BONUS TIMING, INDIVIDUAL PAY TIMING, INDIVIDUAL ASSOCIATE EMPLOYMENT,
  ORGANIZATION NAME, ORGANIZATION GICS, ORGANIZATION NAICS *GEO, ORGANIZATION NACE *GEO,
  ORGANIZATION SIC *GEO, BUSINESS, PARTY SPECIALTY, LEGAL CLASSIFICATION,
  PARTY LANGUAGE USAGE, PARTY STATUS, PARTY SCORE, PARTY CREDIT REPORT SCORE,
  PARTY DEMOGRAPHIC (→ DEMOGRAPHIC → DEMOGRAPHIC VALUE),
  PARTY SEGMENT (→ MARKET SEGMENT),
  PARTY IDENTIFICATION,
  PARTY SOLICITATION PREFERENCE / PARTY CONTACT PREFERENCE (custom),
  PARTY RISK GRADE

Tier 5 — Location (FK to CITY, COUNTRY, POSTAL CODE, etc.):
  LOCATOR, LOCATOR_RELATED, STREET ADDRESS, PARCEL ADDRESS, POST OFFICE BOX ADDRESS,
  ADDRESS, GEOSPATIAL, GEOSPATIAL_POINT

Tier 6 — Link tables (FK to PARTY + LOCATOR):
  PARTY LOCATOR

Tier 7 — Agreement details (FK to AGREEMENT + reference):
  AGREEMENT STATUS, AGREEMENT CURRENCY, AGREEMENT SCORE (→ ANALYTICAL MODEL),
  AGREEMENT FEATURE (→ FEATURE), AGREEMENT METRIC, AGREEMENT RATE,
  FINANCIAL AGREEMENT, DEPOSIT AGREEMENT, DEPOSIT TERM AGREEMENT,
  CREDIT AGREEMENT, LOAN AGREEMENT, LOAN TERM AGREEMENT, LOAN TRANSACTION AGREEMENT,
  CREDIT CARD AGREEMENT, MORTGAGE AGREEMENT, TERM FEATURE, INTEREST RATE INDEX,
  INTEREST INDEX RATE, VARIABLE INTEREST RATE FEATURE, AGREEMENT OBJECTIVE TYPE,
  CARD (→ AGREEMENT)

Tier 8 — Product hierarchy (FK to PRODUCT + FEATURE):
  PRODUCT FEATURE, PRODUCT COST, PRODUCT GROUP, PRODUCT TO PRODUCT GROUP,
  AGREEMENT PRODUCT (FK to AGREEMENT + PRODUCT)

Tier 9 — Party-Agreement links (FK to PARTY + AGREEMENT):
  PARTY AGREEMENT, PARTY RELATED (self-referential on PARTY), PARTY CLAIM

Tier 10 — Events (FK to EVENT):
  EVENT (root)
  → EVENT PARTY (FK to EVENT + PARTY)
  → EVENT CHANNEL INSTANCE (FK to EVENT + CHANNEL INSTANCE)
  → EVENT LOCATOR (FK to EVENT + LOCATOR)
  → EVENT MULTIMEDIA OBJECT (FK to EVENT)
  → MULTIMEDIA OBJECT (FK to EVENT MULTIMEDIA OBJECT)
  → MULTIMEDIA OBJECT LOCATOR / custom (FK to MULTIMEDIA OBJECT + LOCATOR)
  → FINANCIAL EVENT (FK to EVENT)
     → FINANCIAL EVENT AMOUNT (FK to FINANCIAL EVENT)
  → FUNDS TRANSFER EVENT (FK to EVENT + AGREEMENT x2)
  → ACCESS DEVICE EVENT (FK to EVENT + CHANNEL INSTANCE)
  → DIRECT CONTACT EVENT (FK to EVENT) — for complaints/interactions
  → COMPLAINT EVENT (custom, FK to EVENT)

Tier 11 — CRM entities (FK to PARTY + CAMPAIGN):
  CAMPAIGN STATUS, PROMOTION (→ CAMPAIGN), PROMOTION OFFER (→ PROMOTION),
  CAMPAIGN PARTY, OPPORTUNITY, OPPORTUNITY STATUS, OPPORTUNITY PARTY,
  PROPOSAL, APPLICATION, APPLICATION STATUS

Tier 12 — Watch list / AML (standalone then linked):
  WATCH LIST, WATCH LIST SOURCE, EXTERNAL LIST, WATCH LIST MEMBER
  PARTY RISK GRADE, PARTY GROUP RISK GRADE

Tier 13 — Custom task resolution (FK to EVENT + PARTY):
  PARTY TASK, PARTY TASK STATUS, TASK ACTIVITY, TASK ACTIVITY STATUS

Tier 14 — MDM CDM layer (after FSDM PARTY + AGREEMENT):
  CDM PARTY (from FSDM PARTY), CDM INDIVIDUAL, CDM ORGANIZATION, CDM HOUSEHOLD,
  INDIVIDUAL TO INDIVIDUAL, INDIVIDUAL TO HOUSEHOLD, INDIVIDUAL TO ORGANIZATION,
  ORGANIZATION TO ORGANIZATION, PARTY TO AGREEMENT ROLE, PARTY TO EVENT ROLE,
  CDM PARTY SEGMENT, CDM ADDRESS, ADDRESS TO AGREEMENT, CONTACT, CONTACT TO AGREEMENT,
  PARTY INTERACTION EVENT

Tier 15 — MDM PIM layer (after FSDM PRODUCT):
  PIM PRODUCT, PRODUCT PARAMETERS, PRODUCT PARAMETER TYPE, PRODUCT TO GROUP,
  MDM PRODUCT GROUP, PRODUCT GROUP TYPE
```

### Constrained value sets implied by transformation rules

| Column | Entity | Constraint |
|---|---|---|
| Agreement Status Scheme Cd | AGREEMENT STATUS | Must cover all 6 scheme values for PIVOT BB to be complete |
| In Out Direction Type Cd | FINANCIAL EVENT | Determines Interest Earned vs Paid |
| Financial Event Type Cd | FINANCIAL EVENT | Categorizes event (interest, fee, etc.) |
| Agreement Product Role Cd | AGREEMENT PRODUCT | At least one 'primary' per Agreement for ACCOUNT DIM.Product Cd |
| Party Agreement Role Cd | PARTY AGREEMENT | `'customer'` (→ Customer_Account_Ind='1'), `'borrower'` (→ Borrower_Ind), `'guarantor'`, `'co-borrower'`, `'owner'` |
| Party Related Role Cd | PARTY RELATED | `'customer of enterprise'` (→ Customer_Ind='Y'), `'prospect of enterprise'` (→ Prospect_Ind='Y'), `'employee of enterprise'` (→ Associate_Ind='Y') |
| `Currency_Use_Cd` | AGREEMENT CURRENCY | `'preferred'` (triggers Preferred Currency Cd in ACCOUNT_BB), `'secondary'`, `'home'`. Correct column name; no FK to lookup table. |
| Feature Subtype Cd | FEATURE | Must include 'Rate Feature' for LOAN ACCOUNT BB interest rate derivation |
| Feature Classification Cd | FEATURE | Must include 'Original Loan Term' |
| Language Usage Type Cd | PARTY LANGUAGE USAGE | Must include 'primary spoken language', 'primary written language' |
| Contact Preference Type Cd | PARTY CONTACT PREFERENCE | SMALLINT: 1=Sales, 2=Service (see 01_schema-reference.md SMALLINT Code Enumerations) |
| Primary [X] Ind | ORGANIZATION GICS/NAICS/SIC | Exactly one 'Y' per organization |
| Name Type Cd | ORGANIZATION NAME | 'brand name', 'business name', 'legal name', 'registered name' |
| Model Type Cd | ANALYTICAL MODEL | 'profitability' |
| Campaign Status: latest Dttm | CAMPAIGN STATUS | Most recent record wins — needs at least one per campaign |
| Territory Standard Type | ISO 3166 standard | 'ISO 3166-2 Country Subdivision Standard' |
| `Agreement_Feature_Role_Cd` | AGREEMENT_FEATURE_ROLE_TYPE | Seed: `'primary'`, `'fee'`, `'rate'`, `'term'` |
| `Agreement_Status_Cd` (Frozen Status scheme) | AGREEMENT_STATUS_TYPE | Seed row: `Agreement_Status_Scheme_Cd='Frozen Status'`, `Agreement_Status_Cd='FROZEN'`, `Agreement_Status_Desc='Frozen'` (→ Frozen_Ind='1') |

---

## Step 4 — Self Audit: Missed on First Pass

1. **FSDM CRM FV sheet** is effectively empty (only one cell with "Household + split to Commercial and Private Party") — this appears to be an earlier draft that was superseded by WP2 FSDM CRM FV. Nothing actionable was missed.

2. **GRAPH Elements sheet** is empty — no attribute-level graph data was populated. The entity list in GRAPH Entities is comprehensive but no element-level metadata was provided.

3. **WP6 Vector Store** is empty — the vector embedding layer is defined conceptually but not structured in this workbook.

4. **Summary sheet** is empty — no dashboard content to extract.

5. **Sheet1** contains a PivotTable of FSDM subject area labels mapped to the WP2 mapping rows. These are: Banking-ISO20022-Party, Banking-Agreement.Score And Rating, Banking-AnaCredit, Banking-AML (4 variants), Banking-Event.Overview, Banking-Party.Party Type, Foundation variants (CRM, Channel, Event.Case, Party.Individual, Agreement, Campaign, Cross Subject Area variants, Location, Party.Credit Report, Party.Identification, Party.Legal Entity Identifier, FM.GL And Agreement, Event Subject Area). This serves as a filter/search index for the WP2 sheet — no actionable data missed.

6. **WP3 FSAS Cust 360 — ACCOUNT DIMENSION** has a note: `Product Cd` and `Product Desc` columns state "This needs to be re-mapped to MDM PIM Product Tables" — the MDM layer owns the canonical product hierarchy, not FSDM directly.

7. **CUSTOMER PRODUCT FACTLESS FACT note**: "This is the only link between Customer and Address in FSAS, therefore it should be sourced from MDM rather than from Factless tables" — critical for address dimension joins.

8. **WP7-9 — CUSTOMER PROFILE.Customer Preferred Language Cd** annotation: "FSAS mapping is not correct — need to follow the mapping on FSDM sheet" — the FSDM sheet mapping (PARTY LANGUAGE USAGE filtered by Usage Type) should be used, not the straight move from CUSTOMER DIMENSION.

9. **Calculations sheet** only contains a one-line description of CLV. The actual formula is: `CLV = Σ [Customer_Profit_t / (1 + r)^t]` where r = target return on equity, t = expected remaining customer lifetime. The full calculation tree is in WP7-9 CUSTOMER CLV (L0–L4 hierarchy).

10. **BANKING CUSTOMER CHURN ADS** — referenced in WP2 as a target FSAS entity for `Reported Income → Estimated Salary Amt`. This is an Analytical Data Store entity not fully defined in this workbook. Likely maps to CUSTOMER INCOME REPORTING EVENT FACT.`Reporting Currency Annual Net Income Amt`.

11. **CONSUMER COMPLAINT ADS** — referenced in WP2 as a target FSAS entity for multiple complaint fields. The full column list (Complaint Id, Date Received Dttm, Product Name, Subproduct Name, Issue Txt, Subissues Txt, Narrative, Company Response, State Name, ZIP Cd, Tag Desc, Consumer Consent Ind, Submitted Via Ind, Sent to Company Dttm, Company Response To Consumer Ind, Timely Response Ind, Consumer Disputed Ind) appears in WP3 Cust 360 as CONSUMER COMPLAINT ADS — fully captured above.

12. **WP3 FSAS Cust 360** defines `CIF CUSTOMER ACTIVITY FACT` (distinct from CIF CUSTOMER ACTIVITY FACTLESS FACT) — referenced in WP7-9 CUSTOMER CLV for `Allocation Channel Activity`. The column `Chnl Activity Cost` is the aggregative fact value.

---

## Step 5 — Open Questions

From the **Open Questions sheet** (4 entries):

| Layer | Topic | Question | Answer in Workbook |
|---|---|---|---|
| FSDM | General | Indicator is always Y/N? | Unanswered — WP3 rules use '1'/'0' for some (Frozen Ind, Customer Account Ind) and 'Y'/'N' for others (Agreement Legally Binding Ind) |
| FSAS | Architecture | BB tables vs. DIMENSIONS? | **Resolved:** BB tables are process tables (not for end use); DIMENSIONS are the output. BB = "Building Block" — intermediate Layer 2a |
| FSAS | Architecture | Standard dimensions vs. Vx? | **Resolved:** V1 = standard, default |
| FSDM | Semi-structured | Card Loyalty Program Information | Unanswered — referenced in Requirements sheet as semi-structured source but no FSDM mapping defined |

**Additional open questions identified during extraction:**

1. **Exact code values for role codes** — **RESOLVED**: Use exact strings from WP3 transformation rules. `Party_Agreement_Role_Cd`: `'customer'`, `'borrower'`, `'guarantor'`, `'co-borrower'`, `'owner'`. `Party_Related_Role_Cd`: `'customer of enterprise'`, `'prospect of enterprise'`, `'employee of enterprise'`. `Agreement_Feature_Role_Cd` (FK to AGREEMENT_FEATURE_ROLE_TYPE): seed with `'primary'`, `'fee'`, `'rate'`, `'term'`. `Currency_Use_Cd`: `'preferred'`, `'secondary'`, `'home'`. See constrained value sets table. — *Cross-file resolution, session 2026-04-17*

2. **AGREEMENT CURRENCY `Currency_Use_Cd` exact value** — **RESOLVED**: Correct column name is `Currency_Use_Cd` (no FK to lookup). Value triggering preferred currency derivation in ACCOUNT_BB: `'preferred'`. Full set: `'preferred'`, `'secondary'`, `'home'`. — *Cross-file resolution, session 2026-04-17*

3. **Model Type Cd / Model Purpose exact values** — **RESOLVED**: The constraints section of this file already specifies the required values: `Model_Type_Cd = 'profitability'` and `Model_Purpose_Cd = 'customer profitability'`. These are the values AGREEMENT_SCORE and PARTY_SCORE records must use for profitability scoring. No contradicting specification found in any other reference file. — *Source: 02_data-mapping-reference.md Step 3 Constrained value sets*

4. **BANKING CUSTOMER CHURN ADS and CONSUMER COMPLAINT ADS** — **RESOLVED (out of scope)**: File 05 confirms MVP scope = Layer 1 (iDM + MDM) only. Both are Layer 2 / FSAS target entities and are out of scope for this generator build. — *Source: 05_architect-qa.md Project Context*

5. **Frozen status code description** — **RESOLVED**: Seed `AGREEMENT_STATUS_TYPE` with `Agreement_Status_Scheme_Cd = 'Frozen Status'`, `Agreement_Status_Cd = 'FROZEN'`, `Agreement_Status_Desc = 'Frozen'`. The ACCOUNT_STATUS_DIMENSION rule matches 'frozen' case-insensitively — 'Frozen' satisfies this. See constrained value sets table. — *Cross-file resolution, session 2026-04-17*

6. **CIF CUSTOMER ACTIVITY FACT vs CIF CUSTOMER ACTIVITY FACTLESS FACT** — **RESOLVED (out of scope)**: File 05 confirms MVP = Layer 1 only. Both are Layer 2 FSAS fact tables and out of scope for this generator. — *Source: 05_architect-qa.md Project Context*

7. **CLV Hierarchy Type Cd values** — **RESOLVED (out of scope)**: File 05 confirms MVP = Layer 1 only. CUSTOMER CLV is a WP7-9 end data product (Layer 3+) and out of scope for this generator. — *Source: 05_architect-qa.md Project Context*

8. **Product Type 1–8 grouping** — **RESOLVED**: File 04 explicitly defines the 8 regulatory banking product types: (1) Checking, (2) Savings, (3) Retirement, (4) Credit Card, (5) Vehicle Loan, (6) Mortgage, (7) Investments, (8) Insurance. These map to `PIM_DB.PRODUCT_GROUP` rows identified by `Product_Group_Type_Cd = 'CLV'`. — *Source: 04_domain-context.md Section 1*

9. **Min/Max values for CIF elements** — **RESOLVED**: Three files together provide authoritative distributions: File 03 (SCF 2022 survey statistics for customer financial amounts by income quartile and age), File 01 Generator Notes (schema-level column ranges per data type), and File 04 WP5 Feature Store (feature-level distributions including deposit balance, credit card balance, CLV, and tenure). Use these in combination as the calibration source. — *Source: 01_schema-reference.md Generator Notes; 03_source-data-profile.md Generator Notes; 04_domain-context.md WP5 Feature Store*

10. **PARTY CLAIM / AML tables** — **RESOLVED**: `PARTY_CLAIM` structure is fully defined in `01_schema-reference.md` (standalone PK, no parent CLAIM table needed). AML tables (WATCH_LIST, WATCH_LIST_SOURCE, EXTERNAL_LIST, PARTY_RISK_GRADE, PARTY_GROUP_RISK_GRADE, WATCH_LIST_MEMBER) are **out of scope for MVP** — no DDL exists in any source file; generator skips these entirely. — *Cross-file resolution, session 2026-04-17*


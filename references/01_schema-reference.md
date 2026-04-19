# Schema Reference — CIF Banking FSDM

## Database Schemas

| Schema | Role |
|--------|------|
| **Core_DB** | Primary SOR (System of Record) layer. Full FSDM entity model: agreements, parties, products, campaigns, channels, features, rates, organization, individual demographics, industry codes, geo/address. ~140+ tables. Uses INTEGER/BIGINT PKs; Teradata TITLE clauses on every column; DI metadata on all tables. |
| **CDM_DB** | Customer Data Mart / master data layer. Survivored party, household, relationship, segment, address, contact tables. MULTISET tables; BIGINT PKs; `Del_Ind + Valid_From_Dt/Valid_To_Dt` pattern (SCD2). Simpler schemas than Core_DB. ~14 tables. |
| **PIM_DB** | Product Information Management. Product catalog with parameters and group hierarchy. BIGINT PKs; same `Del_Ind + Valid_From_Dt/Valid_To_Dt` pattern. 6 tables. |
| **Core_DB_customized** | Behavioral/interaction extensions to Core_DB. Contact preferences, events (complaints), tasks, activities. BIGINT PKs; no schema prefix on some (same Core_DB namespace). 8 tables. |

---

## Universal Conventions

### DI Metadata Columns (on ALL tables)
Every table ends with these five columns — never generate as meaningful data, use fixed/system values:
```
di_data_src_cd    VARCHAR(50)   NULL  -- source system code
di_start_ts       TIMESTAMP(6)  NULL  -- ETL load start timestamp
di_proc_name      VARCHAR(255)  NULL  -- ETL process/job name
di_rec_deleted_Ind CHAR(1)      NULL  -- soft-delete flag ('Y'/'N'/NULL)
di_end_ts         TIMESTAMP(6)  NULL  -- ETL load end timestamp
```

### Teradata DDL Conventions
- **TITLE clause**: display alias shown in query results; reveals business meaning when column name is ambiguous (e.g., `Address_Subtype_Cd` has TITLE `'Locator Type Cd'`)
- **UNIQUE PRIMARY INDEX (UPI_*)**: functionally equivalent to UNIQUE PRIMARY KEY — generator should enforce uniqueness
- **Non-Unique Primary Index (NUPI_*)**: distribution key only — allows duplicate rows; generator may produce duplicates in some tables
- **MULTISET TABLE**: explicitly allows duplicate rows; CDM_DB tables are all MULTISET

### Column Naming Patterns
| Pattern | Meaning |
|---------|---------|
| `*_Id` (INTEGER/BIGINT) | Surrogate key; FK to another table |
| `*_Cd` (VARCHAR) | Code/enum value; FK to `*_TYPE` lookup table |
| `*_Desc` (VARCHAR) | Human-readable description for a code |
| `*_Ind` (CHAR(1) or CHAR(3)) | Indicator/flag; CHAR(1)='Y'/'N', CHAR(3)='Yes'/'No'/NULL |
| `*_Num` (VARCHAR(50)) | Numeric-looking but stored as VARCHAR (e.g., account numbers, phone) |
| `*_Amt` | DECIMAL(18,4) monetary amount |
| `*_Rate` | DECIMAL(15,12) interest/rate value |
| `*_Pct` | DECIMAL(9,4) percentage |
| `*_Dt` | DATE |
| `*_Dttm` | TIMESTAMP (date+time) |
| `*_Tm` | TIME |
| `*_Txt` | VARCHAR(1000+) free text |
| `*_Start_Dt/*_End_Dt` | SCD2-style validity range (DATE) |
| `*_Start_Dttm/*_End_Dttm` | SCD2-style validity range (TIMESTAMP) |
| `Valid_From_Dt/Valid_To_Dt` | CDM/PIM pattern for SCD2 |

### Decimal Precision Standards
| Precision | Usage |
|-----------|-------|
| DECIMAL(18,4) | Monetary amounts |
| DECIMAL(15,12) | Interest/exchange rates |
| DECIMAL(9,4) | Percentages, allocation pct, discount factors |
| DECIMAL(9,6) | Geo coordinates (lat/lon) |
| DECIMAL(5,4) | Probabilities (0.0000–1.0000) |
| DECIMAL(5,2) | DQ scores |

---

## Core_DB Tables

### Domain: Agreement & Financial Products

#### AGREEMENT
- **Index**: NUPI on `Agreement_Id` (INTEGER NOT NULL)
- **Key columns**: `Agreement_Id`, `Agreement_Subtype_Cd`(→AGREEMENT_SUBTYPE), `Agreement_Objective_Type_Cd`(→AGREEMENT_OBJECTIVE_TYPE, NOT NULL), `Agreement_Obtained_Cd`(→AGREEMENT_OBTAINED_TYPE, NOT NULL), `Agreement_Type_Cd`(→AGREEMENT_TYPE, NOT NULL), `Agreement_Open_Dttm`, `Agreement_Close_Dttm`, `Agreement_Planned_Expiration_Dt`, `Agreement_Processing_Dt`, `Agreement_Signed_Dt`
- **Flags**: `Agreement_Legally_Binding_Ind` CHAR(3)
- **FKs (implicit)**: `Agreement_Format_Type_Cd`→AGREEMENT_FORMAT_TYPE, `Asset_Liability_Cd`→ASSET_LIABILITY_TYPE, `Balance_Sheet_Cd`→BALANCE_SHEET_TYPE, `Statement_Cycle_Cd`→DOCUMENT_PRODUCTION_CYCLE_TYPE, `Statement_Mail_Type_Cd`→STATEMENT_MAIL_TYPE, `Agreement_Source_Cd`→DATA_SOURCE_TYPE
- **Generator note**: Root entity for all product accounts. Generate 1,000–10,000 rows. `Agreement_Id` must be globally unique across all agreement sub-types.

#### AGREEMENT_STATUS
- **Index**: NUPI on `Agreement_Id`
- **Key columns**: `Agreement_Id`, `Agreement_Status_Scheme_Cd`(→AGREEMENT_STATUS_SCHEME_TYPE, NOT NULL), `Agreement_Status_Start_Dttm`(TIMESTAMP NOT NULL), `Agreement_Status_Cd`(→AGREEMENT_STATUS_TYPE), `Agreement_Status_Reason_Cd`(→AGREEMENT_STATUS_REASON_TYPE), `Agreement_Status_End_Dttm`
- **Generator note**: SCD2-style status history. Each agreement should have ≥1 status row. Current record has NULL `Agreement_Status_End_Dttm`.

#### AGREEMENT_CURRENCY
- **Index**: NUPI on `Agreement_Id`
- **Key columns**: `Currency_Use_Cd`(NOT NULL), `Agreement_Id`(NOT NULL), `Agreement_Currency_Start_Dt`(DATE NOT NULL), `Agreement_Currency_Cd`(→CURRENCY, NOT NULL), `Agreement_Currency_End_Dt`

#### AGREEMENT_SCORE
- **Index**: NUPI on `Agreement_Id`
- **Key columns**: `Agreement_Id`, `Model_Id`(→ANALYTICAL_MODEL), `Model_Run_Id`, `Agreement_Score_Val` VARCHAR(100)

#### AGREEMENT_FEATURE
- **Index**: NUPI on `Agreement_Id`
- **Key columns**: `Agreement_Id`, `Feature_Id`(→FEATURE), `Agreement_Feature_Role_Cd`(→AGREEMENT_FEATURE_ROLE_TYPE, NOT NULL), `Agreement_Feature_Start_Dttm`(NOT NULL), `Agreement_Feature_End_Dttm`
- **Amounts**: `Agreement_Feature_Amt` DECIMAL(18,4), `Agreement_Feature_To_Amt`, `Agreement_Feature_Rate` DECIMAL(15,12), `Agreement_Feature_Qty` DECIMAL(18,4)
- **FKs**: `Agreement_Feature_UOM_Cd`(NOT NULL), `Interest_Rate_Index_Cd`→INTEREST_RATE_INDEX, `Currency_Cd`→CURRENCY

#### AGREEMENT_RATE
- **Index**: NUPI on `Agreement_Id`
- **Key columns**: `Agreement_Id`, `Rate_Type_Cd`(NOT NULL), `Balance_Category_Type_Cd`(NOT NULL), `Agreement_Rate_Start_Dttm`(NOT NULL), `Agreement_Rate_End_Dttm`, `Agreement_Rate_Time_Period_Cd`(NOT NULL), `Agreement_Rate` DECIMAL(15,12)

#### FINANCIAL_AGREEMENT
- **Index**: NUPI on `Agreement_Id` (extends AGREEMENT — 1:1)
- **Key columns**: `Agreement_Id`, `Market_Risk_Type_Cd`(→MARKET_RISK_TYPE, NOT NULL), `Original_Maturity_Dt`, `Trading_Book_Cd`(→TRADING_BOOK_TYPE), `Day_Count_Basis_Cd`(→DAY_COUNT_BASIS_TYPE), `Financial_Agreement_Type_Cd`(→FINANCIAL_AGREEMENT_TYPE), `ISO_8583_Account_Type_Cd`
- **FKs**: `Risk_Exposure_Mitigant_Subtype_Cd`→RISK_EXPOSURE_MITIGANT_SUBTYPE, `Pricing_Method_Subtype_Cd`→PRICING_METHOD_SUBTYPE, `Financial_Agreement_Subtype_Cd`

#### DEPOSIT_AGREEMENT
- **Index**: NUPI on `Agreement_Id` (sub-type of FINANCIAL_AGREEMENT)
- **Key columns**: `Agreement_Id`, `Deposit_Maturity_Subtype_Cd`(→DEPOSIT_MATURITY_SUBTYPE), `Interest_Disbursement_Type_Cd`(→INTEREST_DISBURSEMENT_TYPE, NOT NULL), `Deposit_Ownership_Type_Cd`, `Original_Deposit_Amt` DECIMAL(18,4), `Original_Deposit_Dt`, `Agreement_Currency_Original_Deposit_Amt` DECIMAL(18,4)

#### DEPOSIT_TERM_AGREEMENT
- **Index**: NUPI on `Agreement_Id`
- **Key columns**: `Agreement_Id`, `Next_Term_Maturity_Dt`, `Grace_Period_End_Dt`

#### CREDIT_AGREEMENT
- **Index**: NUPI on `Agreement_Id` (sub-type of FINANCIAL_AGREEMENT)
- **Key columns**: `Agreement_Id`, `Obligor_Borrowing_Purpose_Cd`(NOT NULL), `Credit_Agreement_Grace_Period_Cd`(NOT NULL), `Seniority_Level_Cd`, `Credit_Agreement_Reaging_Cnt`, `Credit_Agreement_Settlement_Dt`
- **Amounts**: `Credit_Agreement_Past_Due_Amt`, `Credit_Agreement_Charge_Off_Amt`, `Credit_Agreement_Impairment_Amt`, `Credit_Agreement_Last_Payment_Amt`, `Credit_Agreement_Last_Payment_Dt` (and Agreement_Currency_* variants for each)
- **FKs**: `Credit_Agreement_Subtype_Cd`, `Specialized_Lending_Type_Cd`, `Payment_Frequency_Time_Period_Cd`→TIME_PERIOD_TYPE

#### LOAN_AGREEMENT
- **Index**: NUPI on `Agreement_Id` (sub-type of CREDIT_AGREEMENT)
- **Key columns**: `Agreement_Id`, `Security_Type_Cd`(→SECURITY_TYPE, NOT NULL), `Loan_Maturity_Subtype_Cd`(→LOAN_MATURITY_SUBTYPE), `Due_Day_Num` VARCHAR(50), `Realizable_Collateral_Amt` DECIMAL(18,4), `Loan_Payoff_Amt` DECIMAL(18,4) (and Agreement_Currency_* variants)

#### LOAN_TERM_AGREEMENT
- **Index**: NUPI on `Agreement_Id` (extends LOAN_AGREEMENT)
- **Key columns**: `Agreement_Id`, `Amortization_Method_Cd`(→AMORTIZATION_METHOD_TYPE, NOT NULL), `Loan_Term_Subtype_Cd`(→LOAN_TERM_SUBTYPE, NOT NULL), `Original_Loan_Amt`, `Preapproved_Loan_Amt`, `Maximum_Monthly_Payment_Amt`, `Balloon_Amt`, `Down_Payment_Amt` (all DECIMAL(18,4)), `Loan_Maturity_Dt`, `Loan_Termination_Dt`, `Loan_Renewal_Dt`, `Commit_Start_Dt`, `Commit_End_Dt`, `Payoff_Dt`, `Loan_Asset_Purchase_Dt`
- **Flags**: `Loan_Refinance_Ind` CHAR(3)

#### LOAN_TRANSACTION_AGREEMENT
- **Index**: NUPI on `Agreement_Id`
- **Key columns**: `Agreement_Id`, `Loan_Transaction_Subtype_Cd`(→LOAN_TRANSACTION_SUBTYPE)

#### MORTGAGE_AGREEMENT
- **Index**: NUPI on `Agreement_Id` (extends LOAN_TERM_AGREEMENT)
- **Key columns**: `Agreement_Id`, `Mortgage_Type_Cd`(→MORTGAGE_TYPE), `First_Time_Mortgage_Ind` CHAR(3), `Closing_Cost_Amt`, `Early_Payoff_Penalty_Amt`, `Adjustable_Payment_Cap_Amt`, `Prepayment_Penalty_Dt` (and Agreement_Currency_* variants)

#### CREDIT_CARD_AGREEMENT
- **Index**: NUPI on `Agreement_Id` (sub-type of CREDIT_AGREEMENT)
- **Key columns**: `Agreement_Id`, `Credit_Card_Agreement_Subtype_Cd`(→CREDIT_CARD_AGREEMENT_SUBTYPE, NOT NULL), `Credit_Card_Activation_Dttm`

#### PARTY_AGREEMENT (bridge/role table)
- **Index**: NUPI on `Agreement_Id`
- **Key columns**: `Party_Id`, `Agreement_Id`, `Party_Agreement_Role_Cd`(NOT NULL), `Party_Agreement_Start_Dt`(NOT NULL), `Party_Agreement_End_Dt`
- **Amounts**: `Allocation_Pct` DECIMAL(9,4), `Party_Agreement_Amt` DECIMAL(18,4), `Party_Agreement_Currency_Amt` DECIMAL(18,4), `Party_Agreement_Num` VARCHAR(50)
- **Generator note**: Links CDM_DB/Core_DB Party_Id to Agreement_Id. Required FK bridge — every agreement should have ≥1 party.

#### PRODUCT (Core_DB version — SOR product definition)
- **Index**: NUPI on `Product_Id` (INTEGER NOT NULL)
- **Key columns**: `Product_Id`, `Product_Subtype_Cd`(NOT NULL), `Host_Product_Num`(NOT NULL), `Product_Name`, `Product_Desc`, `Product_Start_Dt`, `Product_End_Dt`, `Product_Package_Type_Cd`, `Product_Script_Id`, `Product_Creation_Dt`
- **Flags**: `Financial_Product_Ind` CHAR(3), `Service_Ind` CHAR(3)

---

### Domain: Party & Individual (Core_DB)

#### INDIVIDUAL (Core_DB)
- **Index**: NUPI on `Individual_Party_Id` (INTEGER NOT NULL)
- **Key columns**: `Individual_Party_Id`, `Birth_Dt`, `Death_Dt`, `Gender_Type_Cd`(→GENDER_TYPE), `Ethnicity_Type_Cd`(→ETHNICITY_TYPE), `Tax_Bracket_Cd`(→TAX_BRACKET_TYPE, NOT NULL), `Nationality_Cd`(→NATIONALITY_TYPE, NOT NULL), `Retirement_Dt`, `Employment_Start_Dt`
- **Flags**: `Name_Only_No_Pronoun_Ind` CHAR(3)
- **Generator note**: `Individual_Party_Id` must match a Party_Id in the party universe.

#### INDIVIDUAL_NAME
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Name_Type_Cd`(NOT NULL), `Individual_Name_Start_Dt`(NOT NULL), `Given_Name`(NOT NULL), `Middle_Name`(NOT NULL), `Family_Name`(NOT NULL), `Birth_Family_Name`, `Name_Prefix_Txt`, `Name_Suffix_Txt`, `Individual_Name_End_Dt`, `Individual_Full_Name`

#### INDIVIDUAL_GENDER_PRONOUN
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Gender_Pronoun_Type_Cd`(NOT NULL), `Gender_Pronoun_Cd`(→GENDER_PRONOUN), `Gender_Pronoun_Start_Dt`(NOT NULL), `Gender_Pronoun_End_Dt`
- **Flags**: `Self_reported_Ind` CHAR(3)

#### INDIVIDUAL_MARITAL_STATUS
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Individual_Marital_Status_Start_Dt`(NOT NULL), `Marital_Status_Cd`(→MARITAL_STATUS_TYPE, NOT NULL), `Individual_Marital_Status_End_Dt`

#### INDIVIDUAL_MEDICAL
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Data_Source_Type_Cd`(NOT NULL), `Individual_Medical_Start_Dt`(NOT NULL), `Individual_Medical_End_Dt`, `General_Medical_Status_Cd`(→GENERAL_MEDICAL_STATUS_TYPE), `Physical_Exam_Dt`, `Estimated_Pregnancy_Due_Dt`
- **Generator note**: Sensitive PII — consider whether to populate or leave sparse.

#### INDIVIDUAL_SPECIAL_NEED
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Special_Need_Cd`(→SPECIAL_NEED_TYPE, NOT NULL)

#### INDIVIDUAL_MILITARY_STATUS
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Military_Status_Type_Cd`(→MILITARY_STATUS_TYPE, NOT NULL), `Individual_Military_Start_Dt`(NOT NULL), `Individual_Military_End_Dt`

#### INDIVIDUAL_VIP_STATUS
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `VIP_Type_Cd`(→VERY_IMPORTANT_PERSON_TYPE, NOT NULL), `Individual_VIP_Status_Start_Dt`(NOT NULL), `Individual_VIP_Status_End_Dt`

#### INDIVIDUAL_OCCUPATION
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Occupation_Type_Cd`(→OCCUPATION_TYPE, NOT NULL), `Individual_Occupation_Start_Dt`(NOT NULL), `Individual_Occupation_End_Dt`, `Individual_Job_Title_Txt` VARCHAR(1000)

#### INDIVIDUAL_PAY_TIMING
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Business_Party_Id`(→ORGANIZATION, NOT NULL), `Pay_Day_Num` VARCHAR(50), `Time_Period_Cd`(→TIME_PERIOD_TYPE, NOT NULL)

#### INDIVIDUAL_BONUS_TIMING
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Business_Party_Id`(NOT NULL), `Bonus_Month_Num`(NOT NULL) VARCHAR(50)

#### INDIVIDUAL_SKILL
- **Index**: NUPI on `Individual_Party_Id`
- **Key columns**: `Individual_Party_Id`, `Skill_Cd`(→SKILL_TYPE, NOT NULL), `Individual_Skill_Dt`

#### ASSOCIATE_EMPLOYMENT
- **Index**: NUPI on `Associate_Party_Id`
- **Key columns**: `Associate_Party_Id`(→INDIVIDUAL, NOT NULL), `Organization_Party_Id`(→ORGANIZATION, NOT NULL), `Associate_Employment_Start_Dt`(NOT NULL), `Associate_Employment_End_Dt`, `Associate_Hire_Dt`, `Associate_Termination_Dttm`, `Associate_HR_Num`

#### ORGANIZATION (Core_DB)
- **Index**: NUPI on `Organization_Party_Id` (INTEGER NOT NULL)
- **Key columns**: `Organization_Party_Id`, `Organization_Type_Cd`(NOT NULL), `Organization_Established_Dttm`, `Parent_Organization_Party_Id`(self-ref), `Organization_Size_Type_Cd`, `Legal_Classification_Cd`(→LEGAL_CLASSIFICATION), `Ownership_Type_Cd`, `Organization_Close_Dt`, `Organization_Operation_Dt`, `Organization_Fiscal_Month_Num`, `Organization_Fiscal_Day_Num`
- **Basel fields**: `Basel_Organization_Type_Cd`, `Basel_Market_Participant_Cd`, `Basel_Eligible_Central_Ind` CHAR(3)
- **Other**: `BIC_Business_Alpha_4_Cd` CHAR(4)

#### BUSINESS (sub-type of ORGANIZATION)
- **Index**: NUPI on `Business_Party_Id`
- **Key columns**: `Business_Party_Id`, `Tax_Bracket_Cd`(→TAX_BRACKET_TYPE, NOT NULL), `Business_Category_Cd`(→BUSINESS_CATEGORY), `Customer_Location_Type_Cd`, `Business_Legal_Start_Dt`, `Business_Legal_End_Dt`
- **Flags**: `Stock_Exchange_Listed_Ind` CHAR(3)

#### ORGANIZATION_NAME
- **Index**: NUPI on `Organization_Party_Id`
- **Key columns**: `Organization_Party_Id`, `Name_Type_Cd`(NOT NULL), `Organization_Name_Start_Dt`(NOT NULL), `Organization_Name`(NOT NULL), `Organization_Name_Desc`, `Organization_Name_End_Dt`

#### ORGANIZATION_NAICS (industry classification — US)
- **Index**: NUPI on `Organization_Party_Id`
- **Key columns**: `Organization_Party_Id`, `NAICS_National_Industry_Cd`(NOT NULL), `NAICS_Sector_Cd`(NOT NULL), `NAICS_Subsector_Cd`(NOT NULL), `NAICS_Industry_Group_Cd`(NOT NULL), `NAICS_Industry_Cd`(NOT NULL), `Organization_NAICS_Start_Dt`(NOT NULL), `Organization_NAICS_End_Dt`
- **Flags**: `Primary_NAICS_Ind` CHAR(3)

#### ORGANIZATION_NACE (industry classification — EU)
- **Index**: NUPI on `Organization_Party_Id`
- **Key columns**: `Organization_Party_Id`, `NACE_Class_Cd`(NOT NULL), `NACE_Group_Cd`(NOT NULL), `NACE_Division_Cd`(NOT NULL), `NACE_Section_Cd`(NOT NULL), `Organization_NACE_Start_Dt`(NOT NULL), `Organization_NACE_End_Dt`, `Importance_Order_NACE_Num`

#### ORGANIZATION_SIC (industry classification)
- **Index**: NUPI on `Organization_Party_Id`
- **Key columns**: `Organization_Party_Id`, `SIC_Cd`(→SIC, NOT NULL), `Organization_SIC_Start_Dt`(NOT NULL), `Organization_SIC_End_Dt`
- **Flags**: `Primary_SIC_Ind` CHAR(3)

#### ORGANIZATION_GICS (industry classification)
- **Index**: NUPI on `Organization_Party_Id`
- **Key columns**: `Organization_Party_Id`, `GICS_Subindustry_Cd`(NOT NULL), `GICS_Industry_Cd`(NOT NULL), `GICS_Industry_Group_Cd`(NOT NULL), `GICS_Sector_Cd`(→GICS_SECTOR_TYPE, NOT NULL), `Organization_GICS_Start_Dt`(NOT NULL), `Organization_GICS_End_Dt`
- **Flags**: `Primary_GICS_Ind` CHAR(3)

#### PARTY_RELATED (party-to-party relationship)
- **Index**: NUPI on `Party_Id`
- **Key columns**: `Party_Id`, `Related_Party_Id`, `Party_Related_Role_Cd`(NOT NULL), `Party_Related_Start_Dttm`(NOT NULL), `Party_Related_End_Dttm`, `Party_Structure_Type_Cd`(NOT NULL), `Party_Related_Status_Reason_Cd`, `Party_Related_Status_Type_Cd`(→PARTY_RELATED_STATUS_TYPE), `Party_Related_Subtype_Cd`

#### PARTY_CLAIM
- **Index**: NUPI on `Claim_Id`
- **Key columns**: `Claim_Id`(INTEGER NOT NULL), `Party_Id`, `Party_Claim_Role_Cd`(NOT NULL), `Party_Claim_Start_Dttm`(NOT NULL), `Party_Claim_End_Dttm`
- **Flags**: `Party_Claim_Contact_Prohibited_Ind` CHAR(3)

#### PARTY_SCORE
- **Index**: NUPI on `Party_Id`
- **Key columns**: `Party_Id`, `Model_Id`(→ANALYTICAL_MODEL), `Model_Run_Id`, `Party_Score_Val` VARCHAR(100)

#### PARTY_CREDIT_REPORT_SCORE
- **Index**: NUPI on `Obligor_Party_Id`
- **Key columns**: `Reporting_Party_Id`, `Obligor_Party_Id`, `Credit_Report_Dttm`(TIMESTAMP NOT NULL), `Score_Type_Cd`(NOT NULL), `Credit_Report_Score_Num` VARCHAR(50)
- **Generator note**: Credit scores typically 300–850; store as VARCHAR.

#### PARTY_IDENTIFICATION
- **Index**: NUPI on `Party_Id`
- **Key columns**: `Party_Id`, `Issuing_Party_Id`(NOT NULL), `Party_Identification_Type_Cd`(NOT NULL), `Party_Identification_Start_Dttm`(NOT NULL), `Party_Identification_End_Dttm`, `Party_Identification_Num` VARCHAR(50), `Party_Identification_Receipt_Dt`
- **Flags**: `Party_Identification_Primary_Ind` CHAR(3)
- **Generator note**: SSN/passport/DL; mask with realistic patterns.

#### PARTY_LANGUAGE_USAGE
- **Index**: NUPI on `Party_Id`
- **Key columns**: `Party_Id`, `Language_Type_Cd`(→LANGUAGE_TYPE, NOT NULL), `Language_Usage_Type_Cd`(NOT NULL), `Party_Language_Start_Dttm`(NOT NULL), `Party_Language_End_Dttm`, `Party_Language_Priority_Num` VARCHAR(50)

#### PARTY_SPECIALTY
- **Index**: NUPI on `Party_Id`
- **Key columns**: `Party_Id`, `Specialty_Type_Cd`(→SPECIALTY_TYPE, NOT NULL), `Party_Specialty_Start_Dt`(NOT NULL), `Party_Specialty_End_Dt`

#### MARKET_SEGMENT
- **Index**: NUPI on `Market_Segment_Id`
- **Key columns**: `Market_Segment_Id`(INTEGER NOT NULL), `Model_Id`, `Model_Run_Id`, `Segment_Desc`, `Segment_Start_Dttm`(NOT NULL), `Segment_End_Dttm`, `Segment_Group_Id`, `Segment_Name`, `Segment_Creator_Party_Id`, `Market_Segment_Scheme_Id`

---

### Domain: Campaign & Marketing

#### CAMPAIGN
- **Index**: NUPI on `Campaign_Id` (INTEGER NOT NULL)
- **Key columns**: `Campaign_Id`, `Campaign_Strategy_Cd`(→CAMPAIGN_STRATEGY_TYPE), `Campaign_Type_Cd`(→CAMPAIGN_TYPE), `Campaign_Classification_Cd`(→CAMPAIGN_CLASSIFICATION), `Parent_Campaign_Id`(self-ref), `Campaign_Level_Num`, `Campaign_Start_Dt`, `Campaign_End_Dt`, `Campaign_Name`, `Campaign_Creation_Dt`, `Currency_Cd`(→CURRENCY)
- **Amounts**: `Campaign_Estimated_Cost_Amt` DECIMAL(18,4), `Campaign_Estimated_Revenue_Gain_Amt`
- **Counts**: `Campaign_Estimated_Base_Customer_Cnt`, `Campaign_Estimated_Customer_Cnt`, `Campaign_Estimated_Positive_Cnt`, `Campaign_Estimated_Contact_Cnt` (all INTEGER)

#### CAMPAIGN_STATUS
- **Index**: NUPI on `Campaign_Id`
- **Key columns**: `Campaign_Id`, `Campaign_Status_Start_Dttm`(TIMESTAMP NOT NULL), `Campaign_Status_Cd`(→CAMPAIGN_STATUS_TYPE), `Campaign_Status_End_Dttm`

#### PROMOTION
- **Index**: NUPI on `Promotion_Id` (INTEGER NOT NULL)
- **Key columns**: `Promotion_Id`, `Promotion_Type_Cd`(NOT NULL), `Campaign_Id`(→CAMPAIGN, NOT NULL), `Promotion_Classification_Cd`, `Channel_Type_Cd`(→CHANNEL_TYPE), `Internal_Promotion_Name`, `Promotion_Start_Dt`, `Promotion_End_Dt`, `Currency_Cd`, `Unit_Of_Measure_Cd`(→UNIT_OF_MEASURE)
- **Amounts**: `Promotion_Actual_Unit_Cost_Amt` DECIMAL(18,4), `Promotion_Goal_Amt`
- **Counts**: `Promotion_Actual_Unit_Cnt`, `Promotion_Break_Even_Order_Cnt` (INTEGER)

#### PROMOTION_OFFER
- **Index**: NUPI on `Promotion_Id`
- **Key columns**: `Promotion_Id`, `Promotion_Offer_Id`(INTEGER NOT NULL), `Promotion_Offer_Type_Cd`(→PROMOTION_OFFER_TYPE), `Ad_Id`, `Distribution_Start_Dt`, `Distribution_End_Dt`, `Redemption_Start_Dt`, `Redemption_End_Dt`

---

### Domain: Channel & Access Device

#### CHANNEL_INSTANCE
- **Index**: NUPI on `Channel_Instance_Id` (INTEGER NOT NULL)
- **Key columns**: `Channel_Instance_Id`, `Channel_Type_Cd`(→CHANNEL_TYPE, NOT NULL), `Channel_Instance_Subtype_Cd`(→CHANNEL_INSTANCE_SUBTYPE, TITLE: 'Alternate Channel Type Cd'), `Channel_Instance_Name`, `Channel_Instance_Start_Dt`, `Channel_Instance_End_Dt`, `Convenience_Factor_Cd`(→CONVENIENCE_FACTOR_TYPE, NOT NULL)

#### CHANNEL_INSTANCE_STATUS
- **Index**: NUPI on `Channel_Instance_Id`
- **Key columns**: `Channel_Instance_Id`, `Channel_Instance_Status_Start_Dttm`(NOT NULL), `Channel_Status_Cd`, `Channel_Instance_Status_End_Dttm`

#### CHANNEL_TYPE
- **Index**: NUPI on `Channel_Type_Cd` (VARCHAR NOT NULL)
- **Key columns**: `Channel_Type_Cd`, `Channel_Processing_Cd`, `Channel_Type_Name`, `Channel_Type_Desc`, `Channel_Type_Start_Dt`, `Channel_Type_End_Dt`, `Parent_Channel_Type_Cd`(self-ref), `Channel_Type_Subtype_Cd`
- **Generator note**: Not a strict lookup — has operational attributes. Values: BRANCH, ATM, ONLINE, MOBILE, CALL_CENTER, etc.

#### CARD
- **Index**: NUPI on `Access_Device_Id` (INTEGER NOT NULL)
- **Key columns**: `Access_Device_Id`, `Card_Association_Type_Cd`(NOT NULL), `Card_Subtype_Cd`, `Technology_Type_Cd`, `Card_Num` VARCHAR(50), `Card_Sequence_Num`, `Card_Expiration_Dt`, `Card_Issue_Dt`, `Card_Activation_Dt`, `Card_Deactivation_Dt`, `Card_Name`, `Card_Encrypted_Num`, `Card_Manufacture_Dt`, `Card_Replacement_Order_Dt`, `Language_Type_Cd`, `Bank_Identification_Num` VARCHAR(6), `Card_Security_Code_Num` VARCHAR(50)
- **Generator note**: `Card_Num` should be Luhn-valid 16-digit; `Bank_Identification_Num` = first 6 digits; `Card_Security_Code_Num` = 3-digit CVV.

---

### Domain: Feature & Rate

#### FEATURE
- **Index**: NUPI on `Feature_Id` (INTEGER NOT NULL)
- **Key columns**: `Feature_Id`, `Feature_Subtype_Cd`(→FEATURE_SUBTYPE, NOT NULL), `Feature_Insurance_Subtype_Cd`(→FEATURE_INSURANCE_SUBTYPE), `Feature_Classification_Cd`(→FEATURE_CLASSIFICATION_TYPE), `Feature_Name`, `Feature_Desc`, `Common_Feature_Name`, `Feature_Level_Subtype_Cnt` INTEGER

#### TERM_FEATURE (extends FEATURE)
- **Index**: NUPI on `Feature_Id`
- **Key columns**: `Feature_Id`, `From_Time_Period_Cd`, `To_Time_Period_Cd`, `Until_Age_Cd`, `From_Time_Period_Num`, `To_Time_Period_Num`, `Until_Age_Num`, `Term_Type_Cd`

#### VARIABLE_INTEREST_RATE_FEATURE (extends FEATURE)
- **Index**: NUPI on `Feature_Id`
- **Key columns**: `Feature_Id`, `Interest_Rate_Index_Cd`(→INTEREST_RATE_INDEX, NOT NULL), `Spread_Rate` DECIMAL(15,12), `Upper_Limit_Rate` DECIMAL(15,12), `Lower_Limit_Rate` DECIMAL(15,12)

#### INTEREST_RATE_INDEX
- **Index**: NUPI on `Interest_Rate_Index_Cd` (VARCHAR NOT NULL)
- **Key columns**: `Interest_Rate_Index_Cd`, `Interest_Rate_Index_Desc`, `Interest_Rate_Index_Short_Name`, `Currency_Cd`, `Yield_Curve_Maturity_Segment_Cd`, `Compound_Frequency_Time_Period_Cd`, `Interest_Rate_Index_Type_Cd`, `Interest_Rate_Index_Time_Period_Cd`(NOT NULL), `Interest_Index_Time_Period_Num`, `Interest_Index_Rate_Reset_Tm` TIME
- **Generator note**: Reference data: LIBOR, SOFR, PRIME, FEDFUNDS, EURIBOR, etc.

#### INTEREST_INDEX_RATE (time-series rate history)
- **Index**: NUPI on `Interest_Rate_Index_Cd`
- **Key columns**: `Interest_Rate_Index_Cd`, `Index_Rate_Effective_Dttm`(DATE NOT NULL), `Interest_Index_Rate` DECIMAL(15,12), `Discount_Factor_Pct` DECIMAL(9,4), `Zero_Coupon_Rate` DECIMAL(15,12)
- **Generator note**: Generate 6-month daily/monthly history per active index.

---

### Domain: Address & Location (Core_DB)

#### ADDRESS (Core_DB — abstract address)
- **Index**: NUPI on `Address_Id` (INTEGER NOT NULL)
- **Key columns**: `Address_Id`, `Address_Subtype_Cd`(→ADDRESS_SUBTYPE, TITLE: 'Locator Type Cd')

#### STREET_ADDRESS (extends ADDRESS)
- **Index**: NUPI on `Street_Address_Id` (INTEGER NOT NULL)
- **Key columns**: `Street_Address_Id`, `Address_Line_1_Txt`, `Address_Line_2_Txt`, `Address_Line_3_Txt`, `Dwelling_Type_Cd`, `City_Id`→CITY, `County_Id`→COUNTY, `Territory_Id`→TERRITORY, `Postal_Code_Id`→POSTAL_CODE, `Country_Id`→COUNTRY, `Census_Block_Id`, `Carrier_Route_Txt`

#### STREET_ADDRESS_DETAIL (extends STREET_ADDRESS)
- **Index**: NUPI on `Street_Address_Id`
- **Key columns**: `Street_Address_Id`, `Street_Address_Num`(NOT NULL, TITLE: 'House Num'), `Street_Name`(NOT NULL), `Street_Direction_Type_Cd`(→DIRECTION_TYPE, NOT NULL), `Street_Suffix_Cd`(→STREET_SUFFIX_TYPE, NOT NULL), `Building_Num`, `Unit_Num`, `Floor_Val`, `Mail_Pickup_Tm`(TIME NOT NULL), `Mail_Delivery_Tm`(TIME NOT NULL), `Mail_Stop_Num`(NOT NULL), `Mail_Box_Num`(NOT NULL)

#### POSTAL_CODE
- **Index**: NUPI on `Postal_Code_Id`
- **Key columns**: `Postal_Code_Id`, `Country_Id`(NOT NULL), `County_Id`, `Postal_Code_Num` VARCHAR(50), `Time_Zone_Cd`

#### PARCEL_ADDRESS, POST_OFFICE_BOX_ADDRESS
- Address sub-types with City/County/Country/PostalCode/Territory FKs.

#### GEOSPATIAL_POINT
- No schema prefix (global namespace). `Geospatial_Point_Id`, `Latitude_Meas` DECIMAL(18,4), `Longitude_Meas` DECIMAL(18,4), `Elevation_Meas` DECIMAL(18,4), `Elevation_UOM_Cd`

#### GEOSPATIAL
- No schema prefix. `Geospatial_Id`, `Geospatial_Roadway_Subtype_Cd`(NOT NULL), `Geospatial_Coordinates_Geosptl` ST_Geometry (skip for CSV output), `Geospatial_Subtype_Cd`

#### TERRITORY, REGION, COUNTRY, CITY, COUNTY (geo hierarchy)
- **TERRITORY**: `Territory_Id`, `Territory_Type_Cd`(→TERRITORY_TYPE), `Country_Id`(NOT NULL), `Region_Id`
- **REGION**: `Region_Id`, `Country_Id`
- **COUNTRY**: `Country_Id`, `Calendar_Type_Cd`(→CALENDAR_TYPE, NOT NULL), `Country_Group_Id`
- **CITY**: `City_Id`, `City_Type_Cd`(→CITY_TYPE), `Territory_Id`
- **COUNTY**: `County_Id`, `Territory_Id`(NOT NULL), `MSA_Id`
- **ISO_3166_COUNTRY_STANDARD**: `Country_Id`, `Country_Code_Standard_Type_Cd`(NOT NULL), `ISO_3166_Country_3_Num` CHAR(3)
- **ISO_3166_COUNTRY_SUBDIVISION_STANDARD**: `Territory_Id`, `Territory_Standard_Type_Cd`(NOT NULL), `ISO_3166_Country_Alpha_2_Cd` CHAR(2), `ISO_3166_Country_Subdivision_Cd` CHAR(3)
- **GEOGRAPHICAL_AREA**: `Geographical_Area_Id`, `Geographical_Area_Subtype_Cd`(NOT NULL), `Name/Desc`, `Start_Dt/End_Dt`
- **GEOGRAPHICAL_AREA_CURRENCY**: `Geographical_Area_Id`, `Currency_Cd`(NOT NULL), `Start_Dt`, `Role_Cd`(NOT NULL)
- **LOCATOR_RELATED**: `Locator_Id`, `Related_Locator_Id`, `Locator_Related_Reason_Cd`(NOT NULL), `Start_Dt/End_Dt`

---

### Domain: Analytical Models

#### ANALYTICAL_MODEL (no schema prefix — global)
- **Index**: NUPI on `Model_Id`
- **Key columns**: `Model_Id`, `Model_Name`, `Model_Desc`, `Model_Version_Num`, `Model_Type_Cd`, `Model_Algorithm_Type_Cd`, `Data_Source_Type_Cd`, `Model_From_Dttm`, `Model_To_Dttm`, `Model_Predict_Time_Period_Cnt`, `Model_Predict_Time_Period_Cd`, `Model_Purpose_Cd`, `Attestation_Ind` CHAR(3), `Model_Target_Run_Dt`, `Locator_Id`, `Criticality_Type_Cd`
- **Generator note**: Referenced by AGREEMENT_SCORE, PARTY_SCORE, MARKET_SEGMENT. Seed 5–20 models.

---

### Domain: Lookup / Reference Tables (Core_DB)

All follow pattern: `*_Cd VARCHAR(50) NOT NULL` (UPI) + `*_Desc VARCHAR(250) NULL` unless noted.

| Table | PK Column | Notes |
|-------|-----------|-------|
| AGREEMENT_SUBTYPE | Agreement_Subtype_Cd | UPI |
| AGREEMENT_FORMAT_TYPE | Agreement_Format_Type_Cd | UPI |
| AGREEMENT_OBJECTIVE_TYPE | Agreement_Objective_Type_Cd | UPI |
| AGREEMENT_OBTAINED_TYPE | Agreement_Obtained_Cd | UPI |
| AGREEMENT_TYPE | Agreement_Type_Cd | UPI |
| AGREEMENT_STATUS_TYPE | Agreement_Status_Scheme_Cd + Agreement_Status_Cd | NUPI on Scheme_Cd; composite |
| AGREEMENT_STATUS_REASON_TYPE | Agreement_Status_Reason_Cd | UPI |
| AGREEMENT_STATUS_SCHEME_TYPE | Agreement_Status_Scheme_Cd | UPI |
| AGREEMENT_FEATURE_ROLE_TYPE | Agreement_Feature_Role_Cd | UPI |
| ASSET_LIABILITY_TYPE | Asset_Liability_Cd | UPI |
| BALANCE_SHEET_TYPE | Balance_Sheet_Cd | UPI |
| DOCUMENT_PRODUCTION_CYCLE_TYPE | Document_Production_Cycle_Cd | NUPI; has Time_Period_Cd, frequency cols |
| STATEMENT_MAIL_TYPE | Statement_Mail_Type_Cd | UPI |
| DATA_SOURCE_TYPE | Data_Source_Type_Cd | UPI |
| CURRENCY | Currency_Cd | NUPI; also ISO_4217_Currency_Alpha_3_Cd CHAR(3) NOT NULL, Exchange_Rate_Unit_Cnt, Currency_Rounding_Decimal_Cnt |
| MARKET_RISK_TYPE | Market_Risk_Type_Cd | UPI |
| TRADING_BOOK_TYPE | Trading_Book_Cd | UPI |
| DAY_COUNT_BASIS_TYPE | Day_Count_Basis_Cd | UPI |
| DEPOSIT_MATURITY_SUBTYPE | Deposit_Maturity_Subtype_Cd | UPI |
| INTEREST_DISBURSEMENT_TYPE | Interest_Disbursement_Type_Cd | UPI |
| FINANCIAL_AGREEMENT_TYPE | Financial_Agreement_Type_Cd | UPI; TITLE has '-7-1' artifact |
| RISK_EXPOSURE_MITIGANT_SUBTYPE | Risk_Exposure_Mitigant_Subtype_Cd | UPI |
| PRICING_METHOD_SUBTYPE | Pricing_Method_Subtype_Cd | UPI |
| PAYMENT_TIMING_TYPE | Payment_Timing_Type_Cd | UPI |
| PURCHASE_INTENT_TYPE | Purchase_Intent_Cd | UPI |
| SECURITY_TYPE | Security_Type_Cd | UPI |
| LOAN_MATURITY_SUBTYPE | Loan_Maturity_Subtype_Cd | UPI |
| LOAN_TRANSACTION_SUBTYPE | Loan_Transaction_Subtype_Cd | UPI |
| LOAN_TERM_SUBTYPE | Loan_Term_Subtype_Cd | UPI |
| AMORTIZATION_METHOD_TYPE | Amortization_Method_Cd | UPI; Desc NOT NULL |
| MORTGAGE_TYPE | Mortgage_Type_Cd | UPI |
| CREDIT_CARD_AGREEMENT_SUBTYPE | Credit_Card_Agreement_Subtype_Cd | UPI |
| FEATURE_SUBTYPE | Feature_Subtype_Cd | UPI |
| FEATURE_INSURANCE_SUBTYPE | Feature_Insurance_Subtype_Cd | UPI |
| FEATURE_CLASSIFICATION_TYPE | Feature_Classification_Cd | UPI |
| GENDER_TYPE | Gender_Type_Cd | UPI; Desc NOT NULL |
| GENDER_PRONOUN | Gender_Pronoun_Cd + Gender_Pronoun_Type_Cd | UPI composite; has Gender_Pronoun_Name |
| ETHNICITY_TYPE | Ethnicity_Type_Cd | UPI |
| MARITAL_STATUS_TYPE | Marital_Status_Cd | UPI |
| NATIONALITY_TYPE | Nationality_Cd | UPI |
| TAX_BRACKET_TYPE | Tax_Bracket_Cd | NUPI; also Tax_Bracket_Rate DECIMAL(15,12) |
| VERY_IMPORTANT_PERSON_TYPE | VIP_Type_Cd | UPI |
| MILITARY_STATUS_TYPE | Military_Status_Type_Cd | UPI |
| OCCUPATION_TYPE | Occupation_Type_Cd | UPI |
| SPECIAL_NEED_TYPE | Special_Need_Cd | UPI |
| GENERAL_MEDICAL_STATUS_TYPE | General_Medical_Status_Cd | UPI |
| PARTY_RELATED_STATUS_TYPE | Party_Related_Status_Type_Cd | UPI |
| SKILL_TYPE | Skill_Cd | UPI |
| TIME_PERIOD_TYPE | Time_Period_Cd | UPI |
| CAMPAIGN_STRATEGY_TYPE | Campaign_Strategy_Cd | UPI |
| CAMPAIGN_TYPE | Campaign_Type_Cd | UPI |
| CAMPAIGN_CLASSIFICATION | Campaign_Classification_Cd | UPI |
| CAMPAIGN_STATUS_TYPE | Campaign_Status_Cd | UPI |
| CHANNEL_INSTANCE_SUBTYPE | Channel_Instance_Subtype_Cd | UPI; TITLE: 'Alternate Channel Type Cd' |
| CONVENIENCE_FACTOR_TYPE | Convenience_Factor_Cd | UPI |
| ADDRESS_SUBTYPE | Address_Subtype_Cd | UPI; TITLE: 'Locator Type Cd' |
| LANGUAGE_TYPE | Language_Type_Cd | NUPI; ISO_Language_Type_Cd NOT NULL, Language_Native_Name |
| LEGAL_CLASSIFICATION | Legal_Classification_Cd | UPI |
| BUSINESS_CATEGORY | Business_Category_Cd | UPI; TITLE: 'Business Legal Class Cd' |
| SPECIALTY_TYPE | Specialty_Type_Cd | UPI |
| NAICS_INDUSTRY | NAICS_Industry_Cd | NUPI composite (Sector + Subsector + IndustryGroup); US industry codes |
| NACE_CLASS | NACE_Class_Cd | NUPI; European industry; composite hierarchy cols |
| SIC | SIC_Cd | NUPI; SIC_Group_Cd NOT NULL |
| GICS_SECTOR_TYPE | GICS_Sector_Cd | UPI |
| GICS_INDUSTRY_GROUP_TYPE | GICS_Industry_Group_Cd | NUPI; + GICS_Sector_Cd |
| GICS_INDUSTRY_TYPE | GICS_Industry_Cd | NUPI; + Group + Sector cols |
| GICS_SUBINDUSTRY_TYPE | GICS_Subindustry_Cd | NUPI; + Industry + Group + Sector cols |
| PROMOTION_METRIC_TYPE | Promotion_Metric_Type_Cd | UPI |
| PROMOTION_OFFER_TYPE | Promotion_Offer_Type_Cd | UPI; Desc NOT NULL |
| UNIT_OF_MEASURE | Unit_Of_Measure_Cd | NUPI; + Unit_Of_Measure_Name, Unit_Of_Measure_Type_Cd |
| DIRECTION_TYPE | Direction_Type_Cd | UPI; N/S/E/W/NE/NW/SE/SW |
| STREET_SUFFIX_TYPE | Street_Suffix_Cd | UPI; ST/AVE/BLVD/DR/etc. |
| TERRITORY_TYPE | Territory_Type_Cd | UPI; no schema prefix |
| CITY_TYPE | City_Type_Cd | UPI; no schema prefix |
| CALENDAR_TYPE | Calendar_Type_Cd | UPI; no schema prefix; no DI metadata |
| CHANNEL_STATUS_TYPE | Channel_Status_Cd | UPI; no schema prefix; no DI metadata |
| UNIT_OF_MEASURE_TYPE | Unit_Of_Measure_Type_Cd | UPI; no schema prefix; no DI metadata |

---

## CDM_DB Tables

All tables are MULTISET. All use `Del_Ind CHAR(1) NOT NULL` + `Valid_From_Dt DATE NOT NULL` + `Valid_To_Dt DATE NOT NULL`. No TITLE clauses.

#### PARTY (master party — survivored)
- **Index**: NUPI on `CDM_Party_Id` (BIGINT NOT NULL)
- **Key columns**: `Source_Cd`(SMALLINT NOT NULL), `CDM_Party_Id`, `Source_Party_Id`(BIGINT NOT NULL), `Party_Type_Cd`(SMALLINT NOT NULL), `Party_Lifecycle_Phase_Cd`(SMALLINT NOT NULL), `Party_Since`(DATE NOT NULL), `Survival_Record_Ind` CHAR(1) NOT NULL, `DQ_Score` DECIMAL(5,2) NOT NULL
- **Generator note**: BIGINT IDs; CDM_Party_Id is the golden party identifier. Use SMALLINT codes (1/2/3...) for type fields.

#### ORGANIZATION (CDM)
- **Index**: NUPI on `CDM_Party_Id`
- **Key columns**: `CDM_Party_Id`, `Organization_Name` VARCHAR(255), `Business_Identifier` VARCHAR(255)

#### INDIVIDUAL (CDM)
- **Index**: NUPI on `CDM_Party_Id`
- **Key columns**: `CDM_Party_Id`, `First_Name`, `Middle_Name`, `Last_Name`, `Birth_Dt`(NOT NULL), `Gender` VARCHAR(50), `Salutation` VARCHAR(50), `DQ_Score` DECIMAL(5,2)
- **Generator note**: No separate Del_Ind in source — check DDL; Birth_Dt is NOT NULL.

#### INDIVIDUAL_TO_INDIVIDUAL (relationship)
- **Index**: NUPI composite on (`CDM_Party_Id`, `Parent_CDM_Party_Id`)
- **Key columns**: `CDM_Party_Id`, `Parent_CDM_Party_Id`, `Relationship_Type_Cd`(SMALLINT NOT NULL), `Relationship_Value_Cd`(SMALLINT NOT NULL), `Probability` DECIMAL(5,4)

#### INDIVIDUAL_TO_ORGANIZATION
- Same structure as INDIVIDUAL_TO_INDIVIDUAL but between individual (CDM_Party_Id) and organization (Parent_CDM_Party_Id)

#### ORGANIZATION_TO_ORGANIZATION
- Same structure; both parties are organizations.

#### HOUSEHOLD
- **Index**: NUPI on `CDM_Household_Id` (BIGINT NOT NULL)
- **Key columns**: `CDM_Household_Id`, `Household_Name`, `Household_Desc`

#### INDIVIDUAL_TO_HOUSEHOLD
- **Index**: NUPI composite on (`CDM_Party_Id`, `CDM_Household_Id`)
- **Key columns**: `CDM_Party_Id`, `CDM_Household_Id`, `Role_Type_Cd`(SMALLINT NOT NULL), `Probability` DECIMAL(5,4)

#### PARTY_TO_AGREEMENT_ROLE
- **Index**: NUPI composite on (`CDM_Party_Id`, `Agreement_Id`)
- **Key columns**: `CDM_Party_Id`, `Agreement_Id`(BIGINT NOT NULL), `Role_Type_Cd`(SMALLINT NOT NULL)
- **Generator note**: Links CDM parties to Core_DB/CDM Agreement_Id values.

#### PARTY_TO_EVENT_ROLE
- **Index**: NUPI composite on (`CDM_Party_Id`, `Event_Id`)
- **Key columns**: `CDM_Party_Id`, `Event_Id`(BIGINT NOT NULL), `Role_Type_Cd`(SMALLINT NOT NULL)

#### PARTY_SEGMENT
- **Index**: NUPI on `CDM_Party_Id`
- **Key columns**: `CDM_Party_Id`, `Segment_Type_Cd`(SMALLINT NOT NULL), `Segment_Value_Cd`(SMALLINT NOT NULL)

#### ADDRESS (CDM — richer than Core_DB ADDRESS)
- **Index**: NUPI on `Address_Id` (BIGINT NOT NULL)
- **Key columns**: `Address_Id`, `Address_Type` VARCHAR(255), `Address_Country_Cd`(SMALLINT NOT NULL), `Address_County`, `Address_City`, `Address_Street`, `Address_Postal_Code` VARCHAR(20), `Primary_Address_Flag` CHAR(1), `Geo_Latitude` DECIMAL(9,6), `Geo_Longitude` DECIMAL(9,6)

#### ADDRESS_TO_AGREEMENT
- **Index**: NUPI composite on (`Address_Id`, `Agreement_Id`)
- **Key columns**: `Address_Id`(BIGINT NOT NULL), `Agreement_Id`(BIGINT NOT NULL)

#### CONTACT
- **Index**: NUPI on `Contact_Id` (BIGINT NOT NULL)
- **Key columns**: `Contact_Id`, `Contact_Type_Cd`(SMALLINT NOT NULL), `Contact_Value` VARCHAR(255), `Primary_Contact_Ind` CHAR(1) NOT NULL
- **Generator note**: email/phone/mobile. `Contact_Value` should contain realistic email/phone based on `Contact_Type_Cd`.

#### CONTACT_TO_AGREEMENT
- **Index**: NUPI composite on (`Contact_Id`, `Agreement_Id`)
- **Key columns**: `Contact_Id`(BIGINT NOT NULL), `Agreement_Id`(BIGINT NOT NULL)

#### PARTY_INTERRACTION_EVENT (note: typo preserved from DDL)
- **Index**: NUPI on `Event_Id`
- **Key columns**: `Event_Id`(BIGINT NOT NULL), `CDM_Party_Id`(NOT NULL), `Event_Type_Cd`(SMALLINT NOT NULL), `Event_Channel_Type_Cd`(SMALLINT NOT NULL), `Event_Dt`(DATE NOT NULL), `Event_Sentiment_Cd`(SMALLINT NOT NULL)
- **Generator note**: Table name typo "INTERRACTION" — must match DDL exactly.

---

## PIM_DB Tables

All use BIGINT PKs; `Del_Ind CHAR(1) NOT NULL` + `Valid_From_Dt/Valid_To_Dt DATE NOT NULL`.

#### PRODUCT (PIM — product information master)
- **Index**: NUPI on `PIM_Id` (BIGINT NOT NULL)
- **Key columns**: `PIM_Id`, `Product_Id`(BIGINT NOT NULL, links to Core_DB.PRODUCT), `PIM_Product_Name` VARCHAR(255), `PIM_Product_Desc` VARCHAR(32000)
- **Generator note**: `Product_Id` should match a Core_DB.PRODUCT.Product_Id.

#### PRODUCT_PARAMETERS
- **Index**: NUPI on `PIM_Parameter_Id` (BIGINT NOT NULL)
- **Key columns**: `PIM_Parameter_Id`, `PIM_Id`(→PRODUCT, NOT NULL), `PIM_Parameter_Type_Cd`(→PRODUCT_PARAMETER_TYPE, SMALLINT NOT NULL), `PIM_Parameter_Value` VARCHAR(1000)
- **Generator note**: Product attributes as key-value pairs.

#### PRODUCT_PARAMETER_TYPE
- **Index**: NUPI on `PIM_Parameter_Type_Cd` (SMALLINT NOT NULL)
- **Key columns**: `PIM_Parameter_Type_Cd`, `PIM_Parameter_Type_Desc` VARCHAR(255)

#### PRODUCT_TO_GROUP
- **Index**: NUPI on `PIM_Id`
- **Key columns**: `PIM_Id`(→PRODUCT), `Group_Id`(→PRODUCT_GROUP)

#### PRODUCT_GROUP
- **Index**: NUPI on `Product_Group_Id` (BIGINT NOT NULL)
- **Key columns**: `Product_Group_Id`, `Parent_Group_Id`(BIGINT NOT NULL, self-ref), `Product_Group_Type_Cd`(→PRODUCT_GROUP_TYPE, SMALLINT NOT NULL)

#### PRODUCT_GROUP_TYPE
- **Index**: NUPI on `Product_Group_Type_Cd` (SMALLINT NOT NULL)
- **Key columns**: `Product_Group_Type_Cd`, `Product_Group_Type_Name` VARCHAR(255), `Product_Group_Type_Desc` VARCHAR(1000)

---

## Core_DB_customized Tables

All in Core_DB schema. Mix of BIGINT and INTEGER PKs. Some use NUPI with explicit name, some just `PRIMARY INDEX (col)`.

#### PARTY_CONTACT_PREFERENCE
- **Index**: NUPI on `Party_Id`
- **Key columns**: `Party_Id`(BIGINT NOT NULL), `Channel_Type_Cd`(SMALLINT NOT NULL), `Contact_Preference_Type_Cd`(SMALLINT NOT NULL), `Party_Contact_Preference_Start_Dt`(NOT NULL), `Party_Contact_Preference_End_Dt`(NOT NULL), `Protocol_Type_Cd`(SMALLINT NOT NULL), `Days_Cd`(SMALLINT NOT NULL), `Hours_Cd`(SMALLINT NOT NULL), `Party_Contact_Preference_Priority_Num` INTEGER

#### MULTIMEDIA_OBJECT_LOCATOR
- **Index**: NUPI on `MM_Object_Id` (BIGINT NOT NULL)
- **Key columns**: `MM_Object_Id`, `Locator_Id`(BIGINT), `MM_Locator_Reason_Cd`(SMALLINT NOT NULL), `MM_Locator_Start_Dt`(NOT NULL), `MM_Locator_End_Dt`(NOT NULL)
- **Generator note**: Comment in DDL notes "gap: LOV for MM_Locator_Reason_Cd" — no lookup table defined.

#### EVENT
- **Index**: NUPI_EVENT on `Event_Id` (INTEGER NOT NULL)
- **Key columns**: `Event_Id`, `Event_Activity_Type_Cd`(VARCHAR NOT NULL), `Event_Start_Dttm`, `Event_End_Dttm`, `Event_GMT_Start_Dttm`, `Event_Reason_Cd`, `Event_Subtype_Cd`, `Initiation_Type_Cd`, `Event_Desc`

#### COMPLAINT_EVENT (MULTISET)
- **Index**: NUPI on `Event_Id` (BIGINT NOT NULL)
- **Key columns**: `Event_Id`, `Event_Sentiment_Cd`(SMALLINT NOT NULL), `Event_Channel_Type_Cd`(SMALLINT NOT NULL), `Event_Received_Dttm`(TIMESTAMP(0) NOT NULL), `Event_Txt` VARCHAR(32000), `Event_Multimedia_Object_Ind`(CHAR(1) NOT NULL)
- **Generator note**: `Event_Id` links to EVENT. Mixed INTEGER/BIGINT between EVENT and COMPLAINT_EVENT — use BIGINT.

#### PARTY_TASK
- **Index**: NUPI on `Task_Id` (BIGINT NOT NULL)
- **Key columns**: `Task_Id`, `Party_Id`(BIGINT), `Source_Event_Id`(BIGINT, →EVENT), `Task_Activity_Type_Cd`(SMALLINT NOT NULL), `Task_Subtype_Cd`(SMALLINT NOT NULL), `Task_Reason_Cd`(SMALLINT NOT NULL)

#### PARTY_TASK_STATUS
- **Index**: NUPI on `Task_Status_Id` (BIGINT NOT NULL)
- **Key columns**: `Task_Status_Id`, `Task_Id`(BIGINT, →PARTY_TASK), `Task_Status_Start_Dttm`(TIMESTAMP NOT NULL), `Task_Status_End_Dttm`(TIMESTAMP NOT NULL), `Task_Status_Type_Cd`(SMALLINT NOT NULL), `Task_Status_Reason_Cd`(SMALLINT NOT NULL), `Task_Status_Txt` VARCHAR(32000)

#### TASK_ACTIVITY
- **Index**: NUPI on `Activity_Id` (BIGINT NOT NULL)
- **Key columns**: `Activity_Id`, `Task_Id`(BIGINT, →PARTY_TASK), `Activity_Type_Cd`(SMALLINT NOT NULL), `Activity_Txt` VARCHAR(32000), `Activity_Channel_Id`(BIGINT), `Activity_Start_Dttm`(NOT NULL), `Activity_End_Dttm`(NOT NULL)

#### TASK_ACTIVITY_STATUS
- **Index**: NUPI on `Activity_Id`
- **Key columns**: `Activity_Id`(BIGINT NOT NULL, →TASK_ACTIVITY), `Activity_Status_Start_Dttm`(NOT NULL), `Activity_Status_End_Dttm`(NOT NULL), `Activity_Status_Type_Cd`(SMALLINT NOT NULL), `Activity_Status_Reason_Cd`(SMALLINT NOT NULL), `Activity_Status_Txt` VARCHAR(32000)

---

## Generator Notes

### Columns Needing Realistic Value Ranges

| Column / Pattern | Realistic Range / Values |
|-----------------|--------------------------|
| `Agreement_Id` (INTEGER) | 100000–9999999 |
| `Party_Id` / `CDM_Party_Id` (BIGINT) | 1000000–99999999 |
| `Birth_Dt` | 1940-01-01 to 2005-12-31 (age 20–85) |
| `Agreement_Open_Dttm` | Last 10 years; before Close |
| `*_Start_Dt` | Within 6-month history window |
| `*_End_Dt` / `*_End_Dttm` | NULL = current record; or Start + duration |
| `Allocation_Pct` DECIMAL(9,4) | 0.0000–1.0000; sum per agreement ≤ 1 |
| `Agreement_Rate` DECIMAL(15,12) | 0.001–0.25 (0.1%–25%) |
| `Spread_Rate` DECIMAL(15,12) | -0.01–0.05 |
| `Interest_Index_Rate` DECIMAL(15,12) | 0.0–0.15 (historical range) |
| `DQ_Score` DECIMAL(5,2) | 0.00–1.00 |
| `Probability` DECIMAL(5,4) | 0.0000–1.0000 |
| `Credit_Report_Score_Num` VARCHAR(50) | "300"–"850" (FICO) |
| `Original_Loan_Amt` / `Original_Deposit_Amt` | 1000.00–2000000.00 |
| `Card_Num` VARCHAR(50) | 16-digit Luhn-valid |
| `Bank_Identification_Num` VARCHAR(6) | 6-digit BIN |
| `Card_Security_Code_Num` VARCHAR(50) | 3-digit CVV |
| `ISO_4217_Currency_Alpha_3_Cd` CHAR(3) | USD, EUR, GBP, CAD, AUD, JPY |
| `Geo_Latitude` DECIMAL(9,6) | -90.000000 to 90.000000 |
| `Geo_Longitude` DECIMAL(9,6) | -180.000000 to 180.000000 |
| `Tax_Bracket_Rate` DECIMAL(15,12) | 0.10, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37 |

### Constrained Value Sets (Codes / Flags / Enums)

| Column | Values |
|--------|--------|
| `di_rec_deleted_Ind` CHAR(1) | 'N' (active), 'Y' (deleted) — default 'N' |
| `Del_Ind` CHAR(1) | 'N' or 'Y' — default 'N' |
| `Survival_Record_Ind` CHAR(1) | 'Y' (survived), 'N' |
| `Primary_*_Ind` CHAR(3) | 'Yes', 'No' |
| `*_Ind` CHAR(3) | 'Yes', 'No', NULL |
| `Event_Multimedia_Object_Ind` CHAR(1) | 'Y', 'N' |
| `Primary_Contact_Ind` CHAR(1) | 'Y', 'N' |
| `Primary_Address_Flag` CHAR(1) | 'Y', 'N' |
| `Party_Type_Cd` SMALLINT (CDM) | 1=Individual, 2=Organization |
| `Gender` VARCHAR(50) (CDM) | Male, Female, Non-binary, Unknown |
| `Agreement_Legally_Binding_Ind` CHAR(3) | 'Yes', 'No' |
| `Financial_Product_Ind` CHAR(3) | 'Yes', 'No' |
| `Service_Ind` CHAR(3) | 'Yes', 'No' |
| `Basel_Eligible_Central_Ind` CHAR(3) | 'Yes', 'No', NULL |
| `Loan_Refinance_Ind` CHAR(3) | 'Yes', 'No', NULL |
| `First_Time_Mortgage_Ind` CHAR(3) | 'Yes', 'No', NULL |
| `Stock_Exchange_Listed_Ind` CHAR(3) | 'Yes', 'No', NULL |

### Critical FK Relationships for Referential Integrity

```
Seeding order (lookup tables first):
  Level 0 (no deps): All *_TYPE / *_SUBTYPE / *_CLASSIFICATION lookup tables
  Level 1: CURRENCY, TIME_PERIOD_TYPE, CHANNEL_TYPE, UNIT_OF_MEASURE
  Level 2: ANALYTICAL_MODEL, INTEREST_RATE_INDEX, COUNTRY, CALENDAR_TYPE
  Level 3: TERRITORY, REGION → COUNTRY; CITY, COUNTY → TERRITORY; POSTAL_CODE → COUNTRY
  Level 4: FEATURE, PRODUCT (Core_DB), CDM_DB.PARTY/INDIVIDUAL/ORGANIZATION
  Level 5: AGREEMENT, CAMPAIGN, CHANNEL_INSTANCE, CARD
  Level 6: FINANCIAL_AGREEMENT, DEPOSIT_AGREEMENT, CREDIT_AGREEMENT, LOAN_AGREEMENT
              → all extend AGREEMENT (Agreement_Id FK)
  Level 7: DEPOSIT_TERM_AGREEMENT, LOAN_TERM_AGREEMENT, MORTGAGE_AGREEMENT,
              CREDIT_CARD_AGREEMENT, LOAN_TRANSACTION_AGREEMENT
  Level 8: PARTY_AGREEMENT (Party_Id + Agreement_Id)
  Level 9: AGREEMENT_STATUS, AGREEMENT_CURRENCY, AGREEMENT_RATE, AGREEMENT_FEATURE,
              AGREEMENT_SCORE
  Level 10: PROMOTION (→CAMPAIGN), PROMOTION_OFFER (→PROMOTION)
  Level 11: EVENT, PARTY_TASK (→EVENT), TASK_ACTIVITY (→PARTY_TASK)
  Level 12: COMPLAINT_EVENT (→EVENT), PARTY_TASK_STATUS (→PARTY_TASK),
              TASK_ACTIVITY_STATUS (→TASK_ACTIVITY)
  PIM level: PRODUCT_GROUP_TYPE → PRODUCT_GROUP → PRODUCT_TO_GROUP ↔ PIM_DB.PRODUCT
              PIM_DB.PRODUCT.Product_Id → Core_DB.PRODUCT.Product_Id
  CDM bridge: CDM_DB.PARTY_TO_AGREEMENT_ROLE.Agreement_Id → Core_DB.AGREEMENT.Agreement_Id
              CDM_DB.PARTY_TO_EVENT_ROLE.Event_Id → Core_DB.EVENT.Event_Id
```

### Key FK Relationships (column-level)

| Child Column | References |
|-------------|-----------|
| `Agreement_Id` (in sub-tables) | AGREEMENT.Agreement_Id |
| `Feature_Id` (in sub-tables) | FEATURE.Feature_Id |
| `Party_Id` | Conceptually → CDM_DB.PARTY.CDM_Party_Id or Core_DB party |
| `Campaign_Id` in PROMOTION | CAMPAIGN.Campaign_Id |
| `Channel_Type_Cd` | CHANNEL_TYPE.Channel_Type_Cd |
| `Currency_Cd` | CURRENCY.Currency_Cd |
| `Model_Id` | ANALYTICAL_MODEL.Model_Id |
| `Interest_Rate_Index_Cd` | INTEREST_RATE_INDEX.Interest_Rate_Index_Cd |
| `PIM_Id` in PRODUCT_PARAMETERS | PIM_DB.PRODUCT.PIM_Id |
| `Product_Id` in PIM_DB.PRODUCT | Core_DB.PRODUCT.Product_Id |
| `CDM_Party_Id` in CDM sub-tables | CDM_DB.PARTY.CDM_Party_Id |
| `CDM_Household_Id` | CDM_DB.HOUSEHOLD.CDM_Household_Id |
| `Agreement_Id` in CDM_DB | Core_DB.AGREEMENT.Agreement_Id (cross-schema) |
| `Task_Id` in PARTY_TASK_STATUS | PARTY_TASK.Task_Id |
| `Activity_Id` in TASK_ACTIVITY_STATUS | TASK_ACTIVITY.Activity_Id |

### Null vs Populated Business Meaning

| Column | NULL meaning | NOT NULL meaning |
|--------|-------------|-----------------|
| `Agreement_Close_Dttm` | Agreement still open | Agreement closed |
| `*_End_Dt` / `*_End_Dttm` | Current/active record | Historical/expired record |
| `Valid_To_Dt` (CDM/PIM) | Active if set to far-future (9999-12-31) | Expired if in past |
| `Death_Dt` | Individual is alive | Individual is deceased |
| `Parent_Campaign_Id` | Top-level campaign | Sub-campaign |
| `Parent_Organization_Party_Id` | Root org | Child org |
| `Overridden_Feature_Id` | Original feature | Replaces another feature |
| `Party_Claim_End_Dttm` | Open claim | Resolved claim |
| `Agreement_Status_End_Dttm` | Current status | Historical status |
| `Proposal_Id` | No proposal origin | Originated from proposal |

### SMALLINT Code Enumerations

All SMALLINT-coded columns in CDM_DB, Core_DB_customized, and related tables that have no DDL-defined lookup table use the following canonical integer mappings:

#### CDM_DB

| Column | Table(s) | Code → Meaning |
|--------|----------|----------------|
| `Party_Lifecycle_Phase_Cd` | PARTY | 1=External, 2=Prospect, 3=Active Customer |
| `Segment_Type_Cd` | PARTY_SEGMENT | 1=CLV, 2=Behavioral, 3=Risk |
| `Segment_Value_Cd` | PARTY_SEGMENT | 1–10 (decile: 1=lowest, 10=highest) |
| `Contact_Type_Cd` | CONTACT | 1=email, 2=phone, 3=mobile |
| `Role_Type_Cd` | INDIVIDUAL_TO_INDIVIDUAL, INDIVIDUAL_TO_HOUSEHOLD, INDIVIDUAL_TO_ORGANIZATION, ORGANIZATION_TO_ORGANIZATION, PARTY_TO_AGREEMENT_ROLE, PARTY_TO_EVENT_ROLE | 1=primary, 2=spouse_partner, 3=dependent, 4=guarantor, 5=employer |
| `Relationship_Type_Cd` | CDM relationship tables | 1=household_member, 2=employer_employee, 3=guarantor_borrower, 4=parent_subsidiary |
| `Relationship_Value_Cd` | CDM relationship tables | 1=active, 2=former, 3=pending |
| `Event_Type_Cd` | PARTY_INTERRACTION_EVENT | 1=branch_visit, 2=ATM_transaction, 3=online_login, 4=mobile_transaction, 5=call_center_contact, 6=complaint |
| `Event_Channel_Type_Cd` | PARTY_INTERRACTION_EVENT | 1=BRANCH, 2=ATM, 3=ONLINE, 4=MOBILE, 5=CALL_CENTER |
| `Event_Sentiment_Cd` | PARTY_INTERRACTION_EVENT | 1=positive, 2=neutral, 3=negative |

#### Core_DB_customized — PARTY_CONTACT_PREFERENCE

| Column | Code → Meaning |
|--------|----------------|
| `Channel_Type_Cd` (SMALLINT) | 1=BRANCH, 2=ATM, 3=ONLINE, 4=MOBILE, 5=CALL_CENTER, 6=EMAIL |
| `Contact_Preference_Type_Cd` | 1=Sales, 2=Service |
| `Protocol_Type_Cd` | 1=any_time, 2=business_hours, 3=restricted |
| `Days_Cd` | 1=any_day, 2=weekdays, 3=weekends |
| `Hours_Cd` | 1=any_hours, 2=morning, 3=afternoon, 4=evening |

#### Core_DB_customized — Task / Activity / Event tables

| Column | Table | Code → Meaning |
|--------|-------|----------------|
| `Event_Sentiment_Cd` | COMPLAINT_EVENT | 1=positive, 2=neutral, 3=negative |
| `Event_Channel_Type_Cd` | COMPLAINT_EVENT | 1=BRANCH, 2=ONLINE, 3=MOBILE, 4=CALL_CENTER, 5=EMAIL |
| `Task_Activity_Type_Cd` | PARTY_TASK | 1=review, 2=contact_customer, 3=escalate |
| `Task_Subtype_Cd` | PARTY_TASK | 1=complaint_resolution, 2=service_request, 3=sales_inquiry |
| `Task_Reason_Cd` | PARTY_TASK | 1=customer_complaint, 2=fraud_alert, 3=service_failure |
| `Task_Status_Type_Cd` | PARTY_TASK_STATUS | 1=open, 2=in_progress, 3=resolved, 4=closed |
| `Task_Status_Reason_Cd` | PARTY_TASK_STATUS | 1=completed, 2=escalated, 3=cancelled |
| `Activity_Type_Cd` | TASK_ACTIVITY | 1=phone_call, 2=email, 3=chat, 4=in_person |
| `Activity_Status_Type_Cd` | TASK_ACTIVITY_STATUS | 1=pending, 2=completed, 3=cancelled |
| `Activity_Status_Reason_Cd` | TASK_ACTIVITY_STATUS | 1=resolved, 2=no_response, 3=reschedule |

#### MULTIMEDIA_OBJECT_LOCATOR

| Column | Code → Meaning |
|--------|----------------|
| `MM_Locator_Reason_Cd` | 1=primary_document, 2=thumbnail_image, 3=attachment |

#### PIM_DB

SMALLINT codes are fully self-defined by generator-created lookup tables:
- `PIM_Parameter_Type_Cd` → defined in PRODUCT_PARAMETER_TYPE (generator populates with product attribute types)
- `Product_Group_Type_Cd` → defined in PRODUCT_GROUP_TYPE (generator populates with hierarchy type labels)

---

## Missed on First Pass

- **GEOSPATIAL_POINT**, **GEOSPATIAL**, **LOCATOR_RELATED** — no schema prefix (possibly Core_DB global namespace); GEOSPATIAL has ST_Geometry column (skip for CSV output).
- **ANALYTICAL_MODEL**, **CALENDAR_TYPE**, **CHANNEL_STATUS_TYPE**, **UNIT_OF_MEASURE_TYPE**, **CITY_TYPE**, **CITY**, **COUNTY**, **COUNTRY**, **TERRITORY**, **TERRITORY_TYPE**, **REGION** — all lack explicit schema prefix in DDL (global namespace, likely Core_DB).
- **GEOGRAPHICAL_AREA**, **GEOGRAPHICAL_AREA_CURRENCY**, **ISO_3166_COUNTRY_STANDARD**, **ISO_3166_COUNTRY_SUBDIVISION_STANDARD**, **PARCEL_ADDRESS**, **POST_OFFICE_BOX_ADDRESS** — also no DI metadata columns; global namespace.
- `LOCATOR_RELATED` and geospatial tables have no DI metadata columns.
- `CARD` PK is `Access_Device_Id` — not `Card_Id`. The card IS the access device.
- `AGREEMENT_STATUS_TYPE` uses NUPI not UPI (composite Scheme+Status PK).
- `TAX_BRACKET_TYPE` uses NUPI not UPI.
- `LANGUAGE_TYPE` uses NUPI not UPI.
- `CHANNEL_TYPE` is NOT a simple lookup — has operational date range and hierarchy.
- CDM_DB.INDIVIDUAL is missing `Del_Ind` in DDL (present in other CDM tables — likely an oversight; treat as optional).
- `PARTY_INTERRACTION_EVENT` — table name has typo "INTERRACTION" (two R's) — must preserve in code generator.
- Core_DB.INDIVIDUAL and CDM_DB.INDIVIDUAL are **different tables** — Core_DB has demographic/compliance fields; CDM_DB has survivored name/DOB.
- Core_DB.ORGANIZATION and CDM_DB.ORGANIZATION are **different tables** — Core_DB has full org details; CDM_DB is survivored master.

---

## Open Questions

1. **Party ID alignment** — **RESOLVED**: Always use BIGINT across all schemas. File 05 (Q1 & Q2) states: "Wherever this problem arises choosing between INTEGER and BIGINT — always choose BIGINT." `Core_DB.Party_Id` (declared INTEGER) and `CDM_DB.CDM_Party_Id` (BIGINT) are the same logical ID space; generate all party IDs as BIGINT throughout. — *Source: 05_architect-qa.md Q1, Q2*

2. **No explicit PARTY table in Core_DB** — **RESOLVED**: `CDM_DB.PARTY` is the authoritative master party table. File 02 (WP3 FSAS Customizations) explicitly states "Replace Party Id with MDM Party ID (CDM)", confirming `CDM_DB.PARTY.CDM_Party_Id` as the canonical identifier. All Core_DB tables referencing `Party_Id` draw IDs from the `CDM_DB.PARTY` universe. — *Source: 02_data-mapping-reference.md WP3 FSAS Cust 360*

3. **SMALLINT codes in CDM/PIM/customized** — **RESOLVED**: `Party_Type_Cd` is resolved in this file's own Generator Notes (1=Individual, 2=Organization). All remaining SMALLINT-coded columns in CDM_DB and Core_DB_customized have canonical integer mappings defined in the "SMALLINT Code Enumerations" sub-section of Generator Notes below. PIM_DB SMALLINT codes are self-defined by generator-created lookup tables (PRODUCT_PARAMETER_TYPE, PRODUCT_GROUP_TYPE). — *Cross-file resolution, session 2026-04-17*

4. **Agreement inheritance model** — **RESOLVED**: 1:1 exclusive sub-typing confirmed. File 02 (WP3 ACCOUNT BB transformation rules) treats each `Agreement_Id` as following exactly one sub-type path down the hierarchy. The ACCOUNT BB and ACCOUNT DIMENSION treat one account = one product type, which is consistent only with exclusive sub-typing. — *Source: 02_data-mapping-reference.md WP3 ACCOUNT BB*

5. **AGREEMENT.Agreement_Id vs CDM_DB.Agreement_Id** — **RESOLVED**: Same as Q1 — always use BIGINT. Same logical ID space; the INTEGER declaration in `Core_DB.AGREEMENT` is overridden by the universal BIGINT rule. — *Source: 05_architect-qa.md Q1*

6. **LOV for `MM_Locator_Reason_Cd`** — **RESOLVED**: No lookup table is defined in any DDL (DDL itself notes "gap"). Generator uses placeholder SMALLINT codes: 1=primary_document, 2=thumbnail_image, 3=attachment. See SMALLINT Code Enumerations in Generator Notes. — *Cross-file resolution, session 2026-04-17*

7. **No explicit CLAIM table** — **RESOLVED**: `PARTY_CLAIM.Claim_Id` is the PK of `PARTY_CLAIM` itself — a standalone surrogate key (BIGINT, sequential, range 1,000,000–9,999,999). No parent CLAIM table exists in the DDL set and none is needed. `Party_Claim_Role_Cd` is a free-text code with no FK to any lookup table. — *Cross-file resolution, session 2026-04-17*

8. **NAICS/NACE/SIC/GICS data** — **RESOLVED**: Populate each classification table with a representative seed set of real published codes (10–20 rows per classification). Using real codes is required because ORGANIZATION_BB pivot rules FK-join to these tables and `Primary_NAICS_Ind`/`Primary_SIC_Ind`/`Primary_GICS_Ind` filters must resolve against valid rows. Seed sets: **NAICS** — sectors 52 (Finance & Insurance), 62 (Health Care), 44-45 (Retail Trade), 51 (Information), 72 (Accommodation & Food), 81 (Other Services), each with full Subsector/IndustryGroup/Industry/NationalIndustry hierarchy rows; **SIC** — Divisions H (Finance), I (Services), F (Retail Trade), 10–15 real 4-digit codes; **GICS** — all 11 standard sectors (10–60) with representative IndustryGroups, Industries, and Sub-industries; **NACE** — sections A (Agriculture), C (Manufacturing), G (Wholesale/Retail), K (Financial Services), N (Administrative Services). — *Cross-file resolution, session 2026-04-17*

9. **`Attestation_Ind` CHAR(3) in ANALYTICAL_MODEL** — **RESOLVED**: Values are 'Yes' / 'No' / NULL. The universal CHAR(3) flag convention defined in this file's Column Naming Patterns section (`*_Ind CHAR(3)` = 'Yes'/'No'/NULL) applies uniformly; no documented exception exists in any reference file. — *Source: 01_schema-reference.md Column Naming Patterns*

10. **`Agreement_Score_Val` and `Party_Score_Val` format** — **RESOLVED**: Generate as numeric probability strings to 4 decimal places (e.g., `"0.7823"`, `"0.1245"`), range 0.0000–1.0000. Consistent with the DECIMAL(5,4) Probability convention used elsewhere in the schema and matches standard ML model output format. FICO scores are stored separately in `PARTY_CREDIT_REPORT_SCORE.Credit_Report_Score_Num`. — *Cross-file resolution, session 2026-04-17*

---


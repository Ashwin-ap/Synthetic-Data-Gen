# CIF Layer 1 Schema Reference
_Generated from `resources/iDM_MDM_tables_DDLs.xlsx` + SQL DDL files. Total tables: 206 (9 DDL-gap tables added 2026-04-18 from WP2/WP3 mapping rules)_

## Summary Table

| Schema | Table Name | Column Count | PK Columns |
|--------|------------|-------------|------------|
| Core_DB | `AGREEMENT` | 25 | Agreement_Id |
| Core_DB | `AGREEMENT_SUBTYPE` | 5 | Agreement_Subtype_Cd |
| Core_DB | `AGREEMENT_FORMAT_TYPE` | 5 | Agreement_Format_Type_Cd |
| Core_DB | `AGREEMENT_OBJECTIVE_TYPE` | 5 | Agreement_Objective_Type_Cd |
| Core_DB | `AGREEMENT_OBTAINED_TYPE` | 5 | Agreement_Obtained_Cd |
| Core_DB | `AGREEMENT_TYPE` | 5 | Agreement_Type_Cd |
| Core_DB | `ASSET_LIABILITY_TYPE` | 5 | Asset_Liability_Cd |
| Core_DB | `BALANCE_SHEET_TYPE` | 5 | Balance_Sheet_Cd |
| Core_DB | `DOCUMENT_PRODUCTION_CYCLE_TYPE` | 8 | Document_Production_Cycle_Cd |
| Core_DB | `STATEMENT_MAIL_TYPE` | 5 | Statement_Mail_Type_Cd |
| Core_DB | `DATA_SOURCE_TYPE` | 5 | Data_Source_Type_Cd |
| Core_DB | `AGREEMENT_CURRENCY` | 8 | Agreement_Id |
| Core_DB | `CURRENCY` | 8 | Currency_Cd |
| Core_DB | `AGREEMENT_SCORE` | 7 | Agreement_Id |
| Core_DB | `PARTY_AGREEMENT` | 12 | Agreement_Id |
| Core_DB | `AGREEMENT_PRODUCT` | 8 | Agreement_Id |
| Core_DB | `PRODUCT_FEATURE` | 14 | Product_Id |
| Core_DB | `EVENT_PARTY` | 9 | Event_Id |
| Core_DB | `EVENT` | 12 | Event_Id |
| Core_DB | `FINANCIAL_EVENT` | 12 | Event_Id |
| Core_DB | `CHANNEL_INSTANCE` | 10 | Channel_Instance_Id |
| Core_DB | `COMPLAINT_EVENT` | 9 | Event_Id |
| Core_DB | `PARTY_CONTACT_PREFERENCE` | 9 | Party_Id |
| Core_DB | `AGREEMENT_METRIC` | 16 | Agreement_Id |
| Core_DB | `PRODUCT` | 16 | Product_Id |
| Core_DB | `AGREEMENT_STATUS` | 9 | Agreement_Id |
| Core_DB | `AGREEMENT_STATUS_TYPE` | 6 | Agreement_Status_Scheme_Cd |
| Core_DB | `AGREEMENT_STATUS_REASON_TYPE` | 5 | Agreement_Status_Reason_Cd |
| Core_DB | `AGREEMENT_STATUS_SCHEME_TYPE` | 5 | Agreement_Status_Scheme_Cd |
| Core_DB | `ADDRESS` | 5 | Address_Id |
| Core_DB | `ADDRESS_SUBTYPE` | 5 | Address_Subtype_Cd |
| Core_DB | `CAMPAIGN` | 22 | Campaign_Id |
| Core_DB | `CAMPAIGN_STRATEGY_TYPE` | 5 | Campaign_Strategy_Cd |
| Core_DB | `CAMPAIGN_TYPE` | 5 | Campaign_Type_Cd |
| Core_DB | `CAMPAIGN_CLASSIFICATION` | 5 | Campaign_Classification_Cd |
| Core_DB | `CAMPAIGN_STATUS` | 7 | Campaign_Id |
| Core_DB | `CAMPAIGN_STATUS_TYPE` | 5 | Campaign_Status_Cd |
| Core_DB | `CHANNEL_TYPE` | 11 | Channel_Type_Cd |
| Core_DB | `CHANNEL_INSTANCE_SUBTYPE` | 5 | Channel_Instance_Subtype_Cd |
| Core_DB | `CONVENIENCE_FACTOR_TYPE` | 5 | Convenience_Factor_Cd |
| Core_DB | `CHANNEL_INSTANCE_STATUS` | 7 | Channel_Instance_Id |
| Core_DB | `CHANNEL_STATUS_TYPE` | 5 | Channel_Status_Cd |
| Core_DB | `CARD` | 20 | Access_Device_Id |
| Core_DB | `AGREEMENT_FEATURE_ROLE_TYPE` | 5 | Agreement_Feature_Role_Cd |
| Core_DB | `AGREEMENT_RATE` | 10 | Agreement_Id |
| Core_DB | `FINANCIAL_AGREEMENT` | 13 | Agreement_Id |
| Core_DB | `MARKET_RISK_TYPE` | 5 | Market_Risk_Type_Cd |
| Core_DB | `TRADING_BOOK_TYPE` | 5 | Trading_Book_Cd |
| Core_DB | `DAY_COUNT_BASIS_TYPE` | 5 | Day_Count_Basis_Cd |
| Core_DB | `DEPOSIT_AGREEMENT` | 10 | Agreement_Id |
| Core_DB | `DEPOSIT_MATURITY_SUBTYPE` | 5 | Deposit_Maturity_Subtype_Cd |
| Core_DB | `INTEREST_DISBURSEMENT_TYPE` | 5 | Interest_Disbursement_Type_Cd |
| Core_DB | `DEPOSIT_TERM_AGREEMENT` | 6 | Agreement_Id |
| Core_DB | `FEATURE` | 11 | Feature_Id |
| Core_DB | `FEATURE_SUBTYPE` | 5 | Feature_Subtype_Cd |
| Core_DB | `FEATURE_INSURANCE_SUBTYPE` | 5 | Feature_Insurance_Subtype_Cd |
| Core_DB | `FEATURE_CLASSIFICATION_TYPE` | 5 | Feature_Classification_Cd |
| Core_DB | `INDIVIDUAL` | 13 | Individual_Party_Id |
| Core_DB | `INDIVIDUAL_NAME` | 14 | Individual_Party_Id |
| Core_DB | `INDIVIDUAL_GENDER_PRONOUN` | 9 | Individual_Party_Id |
| Core_DB | `INDIVIDUAL_MARITAL_STATUS` | 7 | Individual_Party_Id |
| Core_DB | `ASSOCIATE_EMPLOYMENT` | 10 | Associate_Party_Id |
| Core_DB | `INDIVIDUAL_VIP_STATUS` | 7 | Individual_Party_Id |
| Core_DB | `INDIVIDUAL_MILITARY_STATUS` | 7 | Individual_Party_Id |
| Core_DB | `INDIVIDUAL_OCCUPATION` | 8 | Individual_Party_Id |
| Core_DB | `INDIVIDUAL_PAY_TIMING` | 7 | Individual_Party_Id |
| Core_DB | `INDIVIDUAL_BONUS_TIMING` | 6 | Individual_Party_Id |
| Core_DB | `INDIVIDUAL_SKILL` | 6 | Individual_Party_Id |
| Core_DB | `SKILL_TYPE` | 5 | Skill_Cd |
| Core_DB | `PARTY_RELATED` | 12 | Party_Id |
| Core_DB | `PARTY_CLAIM` | 9 | Claim_Id |
| Core_DB | `PARTY_SCORE` | 7 | Party_Id |
| Core_DB | `MARKET_SEGMENT` | 13 | Market_Segment_Id |
| Core_DB | `PARTY_CREDIT_REPORT_SCORE` | 8 | Obligor_Party_Id |
| Core_DB | `INDIVIDUAL_MEDICAL` | 12 | Individual_Party_Id |
| Core_DB | `INDIVIDUAL_SPECIAL_NEED` | 5 | Individual_Party_Id |
| Core_DB | `SPECIAL_NEED_TYPE` | 5 | Special_Need_Cd |
| Core_DB | `GENDER_TYPE` | 5 | Gender_Type_Cd |
| Core_DB | `GENDER_PRONOUN` | 6 | Gender_Pronoun_Cd, Gender_Pronoun_Type_Cd |
| Core_DB | `ETHNICITY_TYPE` | 5 | Ethnicity_Type_Cd |
| Core_DB | `MARITAL_STATUS_TYPE` | 5 | Marital_Status_Cd |
| Core_DB | `NATIONALITY_TYPE` | 5 | Nationality_Cd |
| Core_DB | `TAX_BRACKET_TYPE` | 6 | Tax_Bracket_Cd |
| Core_DB | `VERY_IMPORTANT_PERSON_TYPE` | 5 | VIP_Type_Cd |
| Core_DB | `MILITARY_STATUS_TYPE` | 5 | Military_Status_Type_Cd |
| Core_DB | `OCCUPATION_TYPE` | 5 | Occupation_Type_Cd |
| Core_DB | `TIME_PERIOD_TYPE` | 5 | Time_Period_Cd |
| Core_DB | `PARTY_RELATED_STATUS_TYPE` | 5 | Party_Related_Status_Type_Cd |
| Core_DB | `GENERAL_MEDICAL_STATUS_TYPE` | 5 | General_Medical_Status_Cd |
| Core_DB | `RISK_EXPOSURE_MITIGANT_SUBTYPE` | 5 | Risk_Exposure_Mitigant_Subtype_Cd |
| Core_DB | `PRICING_METHOD_SUBTYPE` | 5 | Pricing_Method_Subtype_Cd |
| Core_DB | `FINANCIAL_AGREEMENT_TYPE` | 5 | Financial_Agreement_Type_Cd |
| Core_DB | `CREDIT_AGREEMENT` | 21 | Agreement_Id |
| Core_DB | `PAYMENT_TIMING_TYPE` | 5 | Payment_Timing_Type_Cd |
| Core_DB | `PURCHASE_INTENT_TYPE` | 5 | Purchase_Intent_Cd |
| Core_DB | `LOAN_AGREEMENT` | 11 | Agreement_Id |
| Core_DB | `SECURITY_TYPE` | 5 | Security_Type_Cd |
| Core_DB | `LOAN_MATURITY_SUBTYPE` | 5 | Loan_Maturity_Subtype_Cd |
| Core_DB | `LOAN_TRANSACTION_AGREEMENT` | 5 | Agreement_Id |
| Core_DB | `LOAN_TRANSACTION_SUBTYPE` | 5 | Loan_Transaction_Subtype_Cd |
| Core_DB | `CREDIT_CARD_AGREEMENT` | 6 | Agreement_Id |
| Core_DB | `CREDIT_CARD_AGREEMENT_SUBTYPE` | 5 | Credit_Card_Agreement_Subtype_Cd |
| Core_DB | `LOAN_TERM_AGREEMENT` | 30 | Agreement_Id |
| Core_DB | `LOAN_TERM_SUBTYPE` | 5 | Loan_Term_Subtype_Cd |
| Core_DB | `AMORTIZATION_METHOD_TYPE` | 5 | Amortization_Method_Cd |
| Core_DB | `MORTGAGE_AGREEMENT` | 13 | Agreement_Id |
| Core_DB | `MORTGAGE_TYPE` | 5 | Mortgage_Type_Cd |
| Core_DB | `TERM_FEATURE` | 11 | Feature_Id |
| Core_DB | `INTEREST_RATE_INDEX` | 12 | Interest_Rate_Index_Cd |
| Core_DB | `AGREEMENT_FEATURE` | 19 | Agreement_Id |
| Core_DB | `INTEREST_INDEX_RATE` | 8 | Interest_Rate_Index_Cd |
| Core_DB | `VARIABLE_INTEREST_RATE_FEATURE` | 8 | Feature_Id |
| Core_DB | `ORGANIZATION` | 18 | Organization_Party_Id |
| Core_DB | `BUSINESS` | 10 | Business_Party_Id |
| Core_DB | `BUSINESS_CATEGORY` | 5 | Business_Category_Cd |
| Core_DB | `ORGANIZATION_NAICS_*` | 12 | Organization_Party_Id |
| Core_DB | `ORGANIZATION_NACE_*` | 11 | Organization_Party_Id |
| Core_DB | `NACE_CLASS` | 8 | NACE_Class_Cd |
| Core_DB | `ORGANIZATION_SIC_*` | 8 | Organization_Party_Id |
| Core_DB | `ORGANIZATION_GICS` | 11 | Organization_Party_Id |
| Core_DB | `PARTY_SPECIALTY` | 7 | Party_Id |
| Core_DB | `LEGAL_CLASSIFICATION` | 5 | Legal_Classification_Cd |
| Core_DB | `NAICS_INDUSTRY_*` | 8 | NAICS_Sector_Cd, NAICS_Subsector_Cd, NAICS_Industry_Group_Cd |
| Core_DB | `SIC` | 6 | SIC_Cd |
| Core_DB | `GICS_INDUSTRY_TYPE` | 7 | GICS_Industry_Cd |
| Core_DB | `GICS_SUBINDUSTRY_TYPE` | 8 | GICS_Subindustry_Cd |
| Core_DB | `GICS_INDUSTRY_GROUP_TYPE` | 6 | GICS_Industry_Group_Cd |
| Core_DB | `GICS_SECTOR_TYPE` | 5 | GICS_Sector_Cd |
| Core_DB | `SPECIALTY_TYPE` | 5 | Specialty_Type_Cd |
| Core_DB | `ORGANIZATION_NAME` | 9 | Organization_Party_Id |
| Core_DB | `PARTY_IDENTIFICATION` | 12 | Party_Id |
| Core_DB | `PARTY_LANGUAGE_USAGE` | 9 | Party_Id |
| Core_DB | `LANGUAGE_TYPE` | 7 | Language_Type_Cd |
| Core_DB | `PROMOTION` | 19 | Promotion_Id |
| Core_DB | `PROMOTION_METRIC_TYPE` | 5 | Promotion_Metric_Type_Cd |
| Core_DB | `UNIT_OF_MEASURE` | 6 | Unit_Of_Measure_Cd |
| Core_DB | `PROMOTION_OFFER` | 12 | Promotion_Id |
| Core_DB | `PROMOTION_OFFER_TYPE` | 5 | Promotion_Offer_Type_Cd |
| Core_DB | `STREET_ADDRESS` | 15 | Street_Address_Id |
| Core_DB | `STREET_ADDRESS_DETAIL` | 19 | Street_Address_Id |
| Core_DB | `DIRECTION_TYPE` | 5 | Direction_Type_Cd |
| Core_DB | `STREET_SUFFIX_TYPE` | 5 | Street_Suffix_Cd |
| Core_DB | `ISO_3166_COUNTRY_SUBDIVISION_STANDARD` | 7 | Territory_Id |
| Core_DB | `POSTAL_CODE` | 8 | Postal_Code_Id |
| Core_DB | `CITY` | 6 | City_Id |
| Core_DB | `GEOGRAPHICAL_AREA` | 20 | Geographical_Area_Id, Geographical_Area_Id |
| Core_DB | `GEOGRAPHICAL_AREA_CURRENCY` | 16 | Geographical_Area_Id, Geographical_Area_Id |
| Core_DB | `CITY_TYPE` | 10 | City_Type_Cd, City_Type_Cd |
| Core_DB | `COUNTRY` | 6 | Country_Id |
| Core_DB | `CALENDAR_TYPE` | 10 | Calendar_Type_Cd, Calendar_Type_Cd |
| Core_DB | `ISO_3166_COUNTRY_STANDARD` | 12 | ISO_3166_Country_3_Num, ISO_3166_Country_3_Num |
| Core_DB | `COUNTY` | 6 | County_Id |
| Core_DB | `PARCEL_ADDRESS` | 24 | Parcel_Address_Id, Parcel_Address_Id |
| Core_DB | `POST_OFFICE_BOX_ADDRESS` | 20 | Post_Office_Box_Id, Post_Office_Box_Id |
| Core_DB | `REGION` | 5 | Region_Id |
| Core_DB | `TERRITORY` | 7 | Territory_Id |
| Core_DB | `TERRITORY_TYPE` | 10 | Territory_Type_Cd, Territory_Type_Cd |
| Core_DB | `GEOSPATIAL_POINT` | 16 | Geospatial_Point_Id, Geospatial_Point_Id |
| Core_DB | `GEOSPATIAL` | 6 | Geospatial_Id |
| Core_DB | `UNIT_OF_MEASURE_TYPE` | 10 | Unit_Of_Measure_Type_Cd, Unit_Of_Measure_Type_Cd |
| Core_DB | `LOCATOR_RELATED` | 16 | Locator_Id, Locator_Id |
| Core_DB | `ANALYTICAL_MODEL` | 19 | Model_Id |
| Core_DB | `PARTY_DEMOGRAPHIC` | 11 | Party_Id |
| Core_DB | `PARTY` | 10 | Party_Id |
| Core_DB | `HOUSEHOLD` | 6 | Household_Party_Id |
| Core_DB | `DEMOGRAPHIC_VALUE` | 9 | Demographic_Cd |
| Core_DB | `PARTY_LOCATOR` | 9 | Party_Id |
| Core_DB | `ELECTRONIC_ADDRESS` | 8 | Electronic_Address_Id |
| Core_DB | `ELECTRONIC_ADDRESS_SUBTYPE` | 5 | Electronic_Address_Subtype_Cd |
| Core_DB | `INTERNET_PROTOCOL_ADDRESS` | 7 | Internet_Protocol_Address_Id |
| Core_DB | `TELEPHONE_NUMBER` | 11 | Telephone_Number_Id |
| Core_DB | `PARTY_TASK` | 9 | Task_Id |
| Core_DB | `TASK_ACTIVITY` | 10 | Activity_Id |
| Core_DB | `PARTY_ADDRESS` | 9 | Party_Id |
| Core_DB | `PRODUCT_TO_GROUP` | 8 | PIM_Id |
| Core_DB | `PARTY_STATUS` | 8 | Party_Id |
| Core_DB | `PARTY_SEGMENT` | 9 | Party_Id |
| Core_DB | `PRODUCT_COST` | 10 | Product_Id |
| Core_DB | `PRODUCT_GROUP` | 10 | Product_Group_Id |
| Core_DB | `EVENT_CHANNEL_INSTANCE` | 9 | Event_Id |
| Core_DB | `FINANCIAL_EVENT_AMOUNT` | 10 | Event_Id |
| Core_DB | `FUNDS_TRANSFER_EVENT` | 11 | Event_Id |
| Core_DB | `ACCESS_DEVICE_EVENT` | 9 | Event_Id |
| Core_DB | `DIRECT_CONTACT_EVENT` | 8 | Event_Id |
| CDM_DB | `PARTY` | 16 | CDM_Party_Id |
| CDM_DB | `ORGANIZATION` | 11 | CDM_Party_Id |
| CDM_DB | `INDIVIDUAL` | 15 | CDM_Party_Id |
| CDM_DB | `INDIVIDUAL_TO_INDIVIDUAL` | 13 | CDM_Party_Id, Parent_CDM_Party_Id |
| CDM_DB | `INDIVIDUAL_TO_HOUSEHOLD` | 12 | CDM_Party_Id, CDM_Household_Id |
| CDM_DB | `HOUSEHOLD` | 11 | CDM_Household_Id |
| CDM_DB | `INDIVIDUAL_TO_ORGANIZATION` | 13 | CDM_Party_Id, Parent_CDM_Party_Id |
| CDM_DB | `ORGANIZATION_TO_ORGANIZATION` | 13 | CDM_Party_Id, Parent_CDM_Party_Id |
| CDM_DB | `PARTY_TO_AGREEMENT_ROLE` | 11 | CDM_Party_Id, Agreement_Id |
| CDM_DB | `PARTY_TO_EVENT_ROLE` | 11 | CDM_Party_Id, Event_Id |
| CDM_DB | `PARTY_SEGMENT` | 11 | CDM_Party_Id |
| CDM_DB | `ADDRESS_TO_AGREEMENT` | 10 | Address_Id, Agreement_Id |
| CDM_DB | `PARTY_CONTACT` | 12 | Contact_Id |
| CDM_DB | `CONTACT_TO_AGREEMENT` | 10 | Contact_Id, Agreement_Id |
| CDM_DB | `PARTY_INTERRACTION_EVENT` | 11 | Event_Id |
| CDM_DB | `ADDRESS` | 18 | Address_Id |
| PIM_DB | `PRODUCT_TO_GROUP` | 10 | PIM_Id |
| PIM_DB | `PRODUCT` | 12 | PIM_Id |
| PIM_DB | `PRODUCT_PARAMETERS` | 12 | PIM_Parameter_Id |
| PIM_DB | `PRODUCT_PARAMETER_TYPE` | 10 | PIM_Parameter_Type_Cd |
| PIM_DB | `PRODUCT_GROUP` | 11 | Product_Group_Id |
| PIM_DB | `PRODUCT_GROUP_TYPE` | 11 | Product_Group_Type_Cd |
| UNKNOWN | `PARTY_ADDRESS` | 9 | Party_Id |

---

## Schemas by Table Type

### iDM Tables (Core_DB)

#### AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Agreement_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Host_Agreement_Num` | `VARCHAR(50)` |  | NULL |
| `Agreement_Name` | `VARCHAR(100)` |  | NULL |
| `Alternate_Agreement_Name` | `VARCHAR(100)` |  | NULL |
| `Agreement_Open_Dttm` | `TIMESTAMP` |  | NULL |
| `Agreement_Close_Dttm` | `TIMESTAMP` |  | NULL |
| `Agreement_Planned_Expiration_Dt` | `DATE` |  | NULL |
| `Agreement_Processing_Dt` | `DATE` |  | NULL |
| `Agreement_Signed_Dt` | `DATE` |  | NULL |
| `Agreement_Legally_Binding_Ind` | `CHAR(3)` |  | NULL |
| `Proposal_Id` | `INTEGER` |  | NULL |
| `Jurisdiction_Id` | `INTEGER` |  | NULL |
| `Agreement_Format_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Agreement_Objective_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Obtained_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Asset_Liability_Cd` | `VARCHAR(50)` |  | NULL |
| `Balance_Sheet_Cd` | `VARCHAR(50)` |  | NULL |
| `Statement_Cycle_Cd` | `VARCHAR(50)` |  | NULL |
| `Statement_Mail_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Agreement_Source_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Agreement_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_FORMAT_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Format_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Agreement_Format_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_OBJECTIVE_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Objective_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Agreement_Objective_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_OBTAINED_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Obtained_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Agreement_Obtained_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Agreement_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ASSET_LIABILITY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Asset_Liability_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Asset_Liability_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### BALANCE_SHEET_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Balance_Sheet_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Balance_Sheet_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### DOCUMENT_PRODUCTION_CYCLE_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Document_Production_Cycle_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Time_Period_Cd` | `VARCHAR(50)` |  | NULL |
| `Document_Cycle_Desc` | `VARCHAR(250)` |  | NULL |
| `Document_Cycle_Frequency_Num` | `VARCHAR(50)` |  | NULL |
| `Document_Cycle_Frequency_Day_Num` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### STATEMENT_MAIL_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Statement_Mail_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Statement_Mail_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### DATA_SOURCE_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Data_Source_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Data_Source_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_CURRENCY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Currency_Use_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Agreement_Currency_Start_Dt` | `DATE` |  | NOT NULL |
| `Agreement_Currency_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Currency_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CURRENCY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Currency_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Currency_Name` | `VARCHAR(100)` |  | NOT NULL |
| `Exchange_Rate_Unit_Cnt` | `INTEGER` |  | NULL |
| `Currency_Rounding_Decimal_Cnt` | `INTEGER` |  | NULL |
| `ISO_4217_Currency_Alpha_3_Cd` | `CHAR(3)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_SCORE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Model_Id` | `INTEGER` |  | NOT NULL |
| `Model_Run_Id` | `INTEGER` |  | NOT NULL |
| `Agreement_Score_Val` | `VARCHAR(100)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` |  | NOT NULL |
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Party_Agreement_Role_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Agreement_Start_Dt` | `DATE` |  | NOT NULL |
| `Party_Agreement_End_Dt` | `DATE` |  | NULL |
| `Allocation_Pct` | `DECIMAL(9,4)` |  | NULL |
| `Party_Agreement_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Party_Agreement_Currency_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Party_Agreement_Num` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_PRODUCT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Product_Id` | `INTEGER` |  | NOT NULL |
| `Agreement_Product_Role_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Product_Start_Dt` | `DATE` |  | NOT NULL |
| `Agreement_Product_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PRODUCT_FEATURE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Product_Id` | `INTEGER` | Y | NOT NULL |
| `Feature_Id` | `INTEGER` |  | NOT NULL |
| `Product_Feature_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Product_Feature_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Product_Feature_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Product_Feature_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Product_Feature_Rate` | `DECIMAL(15,12)` |  | NULL |
| `Product_Feature_Qty` | `DECIMAL(18,4)` |  | NULL |
| `Product_Feature_Num` | `VARCHAR(50)` |  | NULL |
| `Currency_Cd` | `VARCHAR(50)` |  | NULL |
| `Unit_Of_Measure_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### EVENT_PARTY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `INTEGER` | Y | NOT NULL |
| `Party_Id` | `INTEGER` |  | NOT NULL |
| `Event_Party_Role_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Event_Party_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Event_Party_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Party_Identification_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### EVENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `INTEGER` | Y | NOT NULL |
| `Event_Desc` | `VARCHAR(250)` |  | NULL |
| `Event_Start_Dttm` | `TIMESTAMP` |  | NULL |
| `Event_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Event_GMT_Start_Dttm` | `TIMESTAMP` |  | NULL |
| `Event_Activity_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Event_Reason_Cd` | `VARCHAR(50)` |  | NULL |
| `Event_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Initiation_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### FINANCIAL_EVENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `INTEGER` | Y | NOT NULL |
| `Financial_Event_Period_Start_Dt` | `DATE` |  | NULL |
| `Financial_Event_Period_End_Dt` | `DATE` |  | NULL |
| `Financial_Event_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Document_Production_Cycle_Cd` | `VARCHAR(50)` |  | NULL |
| `Event_Medium_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Debit_Credit_Cd` | `VARCHAR(50)` |  | NULL |
| `In_Out_Direction_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Financial_Event_Bill_Cnt` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_STATUS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `BIGINT` | Y | NOT NULL |
| `Party_Status_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Status_Dt` | `DATE` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_SEGMENT (Core_DB)

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `BIGINT` | Y | NOT NULL |
| `Market_Segment_Id` | `INTEGER` |  | NOT NULL |
| `Party_Segment_Start_Dttm` | `TIMESTAMP` |  | NULL |
| `Party_Segment_End_Dttm` | `TIMESTAMP` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PRODUCT_COST

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Product_Id` | `BIGINT` | Y | NOT NULL |
| `Cost_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Product_Cost_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Product_Cost_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Product_Cost_End_Dttm` | `TIMESTAMP` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PRODUCT_GROUP (Core_DB)

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Product_Group_Id` | `INTEGER` | Y | NOT NULL |
| `Parent_Group_Id` | `INTEGER` |  | NOT NULL |
| `Product_Group_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Product_Group_Name` | `VARCHAR(255)` |  | NULL |
| `Product_Group_Desc` | `VARCHAR(1000)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### EVENT_CHANNEL_INSTANCE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `BIGINT` | Y | NOT NULL |
| `Channel_Instance_Id` | `INTEGER` |  | NOT NULL |
| `Event_Channel_Start_Dttm` | `TIMESTAMP` |  | NULL |
| `Event_Channel_End_Dttm` | `TIMESTAMP` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### FINANCIAL_EVENT_AMOUNT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `BIGINT` | Y | NOT NULL |
| `Financial_Event_Amount_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Event_Transaction_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Financial_Event_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `In_Out_Direction_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### FUNDS_TRANSFER_EVENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `BIGINT` | Y | NOT NULL |
| `Funds_Transfer_Method_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Originating_Agreement_Id` | `BIGINT` |  | NOT NULL |
| `Originating_Account_Num` | `VARCHAR(50)` |  | NULL |
| `Destination_Agreement_Id` | `BIGINT` |  | NULL |
| `Destination_Account_Num` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ACCESS_DEVICE_EVENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `BIGINT` | Y | NOT NULL |
| `Channel_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Funds_Transfer_Method_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Access_Device_Id` | `BIGINT` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### DIRECT_CONTACT_EVENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `BIGINT` | Y | NOT NULL |
| `Contact_Event_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Customer_Tone_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CHANNEL_INSTANCE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Channel_Instance_Id` | `INTEGER` | Y | NOT NULL |
| `Channel_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Channel_Instance_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Channel_Instance_Name` | `VARCHAR(100)` |  | NULL |
| `Channel_Instance_Start_Dt` | `DATE` |  | NULL |
| `Channel_Instance_End_Dt` | `DATE` |  | NULL |
| `Convenience_Factor_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### COMPLAINT_EVENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `BIGINT` | Y | NOT NULL |
| `Event_Sentiment_Cd` | `SMALLINT` |  | NOT NULL |
| `Event_Channel_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Event_Received_Dttm` | `TIMESTAMP(0)` |  | NOT NULL |
| `Event_Txt` | `VARCHAR(32000)` |  | NULL |
| `Event_Multimedia_Object_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_CONTACT_PREFERENCE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Channel_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Contact_Preference_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Party_Contact_Preference_Start_Dt` | `DATE` |  | NOT NULL |
| `Party_Contact_Preference_End_Dt` | `DATE` |  | NOT NULL |
| `Party_Contact_Preference_Priority_Num` | `SMALLINT` |  | NOT NULL |
| `Protocol_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Days_Cd` | `SMALLINT` |  | NOT NULL |
| `Hours_Cd` | `SMALLINT` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_METRIC

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Agreement_Metric_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Metric_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Agreement_Metric_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Agreement_Metric_Time_Period_Cd` | `VARCHAR(50)` |  | NULL |
| `Agreement_Metric_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Metric_Cnt` | `INTEGER` |  | NULL |
| `Agreement_Metric_Rate` | `DECIMAL(15,12)` |  | NULL |
| `Agreement_Metric_Qty` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Metric_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Currency_Cd` | `VARCHAR(50)` |  | NULL |
| `Unit_Of_Measure_Cd` | `VARCHAR(50)` |  | NULL |
| `GL_Main_Account_Segment_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PRODUCT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Product_Id` | `INTEGER` | Y | NOT NULL |
| `Product_Script_Id` | `INTEGER` |  | NULL |
| `Product_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Product_Desc` | `VARCHAR(250)` |  | NULL |
| `Product_Name` | `VARCHAR(100)` |  | NULL |
| `Host_Product_Num` | `VARCHAR(50)` |  | NOT NULL |
| `Product_Start_Dt` | `DATE` |  | NULL |
| `Product_End_Dt` | `DATE` |  | NULL |
| `Product_Package_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Financial_Product_Ind` | `CHAR(3)` |  | NULL |
| `Product_Txt` | `VARCHAR(1000)` |  | NULL |
| `Product_Creation_Dt` | `DATE` |  | NULL |
| `Service_Ind` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_STATUS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Agreement_Status_Scheme_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Status_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Agreement_Status_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Status_Reason_Cd` | `VARCHAR(50)` |  | NULL |
| `Agreement_Status_End_Dttm` | `TIMESTAMP` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_STATUS_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Status_Scheme_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Agreement_Status_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Status_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_STATUS_REASON_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Status_Reason_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Agreement_Status_Reason_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_STATUS_SCHEME_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Status_Scheme_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Agreement_Status_Scheme_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ADDRESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Address_Id` | `INTEGER` | Y | NOT NULL |
| `Address_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ADDRESS_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Address_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Address_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CAMPAIGN

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Campaign_Id` | `INTEGER` | Y | NOT NULL |
| `Campaign_Strategy_Cd` | `VARCHAR(50)` |  | NULL |
| `Campaign_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Campaign_Classification_Cd` | `VARCHAR(50)` |  | NULL |
| `Parent_Campaign_Id` | `INTEGER` |  | NULL |
| `Campaign_Level_Num` | `VARCHAR(50)` |  | NULL |
| `Funding_GL_Main_Account_Id` | `INTEGER` |  | NULL |
| `Campaign_Desc` | `VARCHAR(250)` |  | NULL |
| `Campaign_Start_Dt` | `DATE` |  | NULL |
| `Campaign_End_Dt` | `DATE` |  | NULL |
| `Campaign_Name` | `VARCHAR(100)` |  | NULL |
| `Campaign_Estimated_Cost_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Currency_Cd` | `VARCHAR(50)` |  | NULL |
| `Campaign_Estimated_Revenue_Gain_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Campaign_Estimated_Base_Customer_Cnt` | `INTEGER` |  | NULL |
| `Campaign_Estimated_Customer_Cnt` | `INTEGER` |  | NULL |
| `Campaign_Estimated_Positive_Cnt` | `INTEGER` |  | NULL |
| `Campaign_Estimated_Contact_Cnt` | `INTEGER` |  | NULL |
| `Campaign_Creation_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CAMPAIGN_STRATEGY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Campaign_Strategy_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Campaign_Strategy_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CAMPAIGN_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Campaign_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Campaign_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CAMPAIGN_CLASSIFICATION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Campaign_Classification_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Campaign_Classification_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CAMPAIGN_STATUS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Campaign_Id` | `INTEGER` | Y | NOT NULL |
| `Campaign_Status_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Campaign_Status_Cd` | `VARCHAR(50)` |  | NULL |
| `Campaign_Status_End_Dttm` | `TIMESTAMP` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CAMPAIGN_STATUS_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Campaign_Status_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Campaign_Status_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CHANNEL_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Channel_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Channel_Processing_Cd` | `VARCHAR(50)` |  | NULL |
| `Channel_Type_Name` | `VARCHAR(100)` |  | NULL |
| `Channel_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `Channel_Type_Start_Dt` | `DATE` |  | NULL |
| `Channel_Type_End_Dt` | `DATE` |  | NULL |
| `Parent_Channel_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Channel_Type_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CHANNEL_INSTANCE_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Channel_Instance_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Channel_Instance_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CONVENIENCE_FACTOR_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Convenience_Factor_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Convenience_Factor_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CHANNEL_INSTANCE_STATUS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Channel_Instance_Id` | `INTEGER` | Y | NOT NULL |
| `Channel_Instance_Status_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Channel_Status_Cd` | `VARCHAR(50)` |  | NULL |
| `Channel_Instance_Status_End_Dttm` | `TIMESTAMP` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CHANNEL_STATUS_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Channel_Status_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Channel_Status_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CARD

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Access_Device_Id` | `INTEGER` | Y | NOT NULL |
| `Card_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Card_Association_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Technology_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Card_Num` | `VARCHAR(50)` |  | NULL |
| `Card_Sequence_Num` | `VARCHAR(50)` |  | NULL |
| `Card_Expiration_Dt` | `DATE` |  | NULL |
| `Card_Issue_Dt` | `DATE` |  | NULL |
| `Card_Activation_Dt` | `DATE` |  | NULL |
| `Card_Deactivation_Dt` | `DATE` |  | NULL |
| `Card_Name` | `VARCHAR(100)` |  | NULL |
| `Card_Encrypted_Num` | `VARCHAR(50)` |  | NULL |
| `Card_Manufacture_Dt` | `DATE` |  | NULL |
| `Card_Replacement_Order_Dt` | `DATE` |  | NULL |
| `Language_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Bank_Identification_Num` | `VARCHAR(6)` |  | NULL |
| `Card_Security_Code_Num` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_FEATURE_ROLE_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Feature_Role_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Agreement_Feature_Role_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_RATE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Rate_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Balance_Category_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Rate_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Agreement_Rate_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Agreement_Rate_Time_Period_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Rate` | `DECIMAL(15,12)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### FINANCIAL_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Financial_Agreement_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Market_Risk_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Original_Maturity_Dt` | `DATE` |  | NULL |
| `Risk_Exposure_Mitigant_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Trading_Book_Cd` | `VARCHAR(50)` |  | NULL |
| `Pricing_Method_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Financial_Agreement_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Day_Count_Basis_Cd` | `VARCHAR(50)` |  | NULL |
| `ISO_8583_Account_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### MARKET_RISK_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Market_Risk_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Market_Risk_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### TRADING_BOOK_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Trading_Book_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Trading_Book_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### DAY_COUNT_BASIS_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Day_Count_Basis_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Day_Count_Basis_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### DEPOSIT_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Deposit_Maturity_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Interest_Disbursement_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Deposit_Ownership_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Original_Deposit_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Original_Deposit_Dt` | `DATE` |  | NULL |
| `Agreement_Currency_Original_Deposit_Amt` | `DECIMAL(18,4)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### DEPOSIT_MATURITY_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Deposit_Maturity_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Deposit_Maturity_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INTEREST_DISBURSEMENT_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Interest_Disbursement_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Interest_Disbursement_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### DEPOSIT_TERM_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Next_Term_Maturity_Dt` | `DATE` |  | NULL |
| `Grace_Period_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### FEATURE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Feature_Id` | `INTEGER` | Y | NOT NULL |
| `Feature_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Feature_Insurance_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Feature_Classification_Cd` | `VARCHAR(50)` |  | NULL |
| `Feature_Desc` | `VARCHAR(250)` |  | NULL |
| `Feature_Name` | `VARCHAR(100)` |  | NULL |
| `Common_Feature_Name` | `VARCHAR(100)` |  | NULL |
| `Feature_Level_Subtype_Cnt` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### FEATURE_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Feature_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Feature_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### FEATURE_INSURANCE_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Feature_Insurance_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Feature_Insurance_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### FEATURE_CLASSIFICATION_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Feature_Classification_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Feature_Classification_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Birth_Dt` | `DATE` |  | NULL |
| `Death_Dt` | `DATE` |  | NULL |
| `Gender_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Ethnicity_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Tax_Bracket_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Retirement_Dt` | `DATE` |  | NULL |
| `Employment_Start_Dt` | `DATE` |  | NULL |
| `Nationality_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Name_Only_No_Pronoun_Ind` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_NAME

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Name_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Individual_Name_Start_Dt` | `DATE` |  | NOT NULL |
| `Given_Name` | `VARCHAR(100)` |  | NOT NULL |
| `Middle_Name` | `VARCHAR(100)` |  | NOT NULL |
| `Family_Name` | `VARCHAR(100)` |  | NOT NULL |
| `Birth_Family_Name` | `VARCHAR(100)` |  | NULL |
| `Name_Prefix_Txt` | `VARCHAR(1000)` |  | NULL |
| `Name_Suffix_Txt` | `VARCHAR(1000)` |  | NULL |
| `Individual_Name_End_Dt` | `DATE` |  | NULL |
| `Individual_Full_Name` | `VARCHAR(100)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_GENDER_PRONOUN

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Gender_Pronoun_Start_Dt` | `DATE` |  | NOT NULL |
| `Gender_Pronoun_End_Dt` | `DATE` |  | NULL |
| `Self_reported_Ind` | `CHAR(3)` |  | NULL |
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Gender_Pronoun_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Gender_Pronoun_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_MARITAL_STATUS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Individual_Marital_Status_Start_Dt` | `DATE` |  | NOT NULL |
| `Marital_Status_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Individual_Marital_Status_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ASSOCIATE_EMPLOYMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Associate_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Organization_Party_Id` | `INTEGER` |  | NOT NULL |
| `Associate_Employment_Start_Dt` | `DATE` |  | NOT NULL |
| `Associate_Employment_End_Dt` | `DATE` |  | NULL |
| `Associate_Hire_Dt` | `DATE` |  | NULL |
| `Associate_Termination_Dttm` | `TIMESTAMP` |  | NULL |
| `Associate_HR_Num` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_VIP_STATUS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Individual_VIP_Status_Start_Dt` | `DATE` |  | NOT NULL |
| `VIP_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Individual_VIP_Status_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_MILITARY_STATUS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Individual_Military_Start_Dt` | `DATE` |  | NOT NULL |
| `Military_Status_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Individual_Military_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_OCCUPATION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Occupation_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Individual_Occupation_Start_Dt` | `DATE` |  | NOT NULL |
| `Individual_Occupation_End_Dt` | `DATE` |  | NULL |
| `Individual_Job_Title_Txt` | `VARCHAR(1000)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_PAY_TIMING

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Business_Party_Id` | `INTEGER` |  | NOT NULL |
| `Pay_Day_Num` | `VARCHAR(50)` |  | NULL |
| `Time_Period_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_BONUS_TIMING

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Bonus_Month_Num` | `VARCHAR(50)` |  | NOT NULL |
| `Business_Party_Id` | `INTEGER` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_SKILL

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Skill_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Individual_Skill_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### SKILL_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Skill_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Skill_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_RELATED

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Related_Party_Id` | `INTEGER` |  | NOT NULL |
| `Party_Related_Role_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Related_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Party_Related_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Party_Structure_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Related_Status_Reason_Cd` | `VARCHAR(50)` |  | NULL |
| `Party_Related_Status_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Party_Related_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_CLAIM

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Claim_Id` | `INTEGER` | Y | NOT NULL |
| `Party_Id` | `INTEGER` |  | NOT NULL |
| `Party_Claim_Role_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Claim_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Party_Claim_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Party_Claim_Contact_Prohibited_Ind` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_SCORE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Model_Id` | `INTEGER` |  | NOT NULL |
| `Model_Run_Id` | `INTEGER` |  | NOT NULL |
| `Party_Score_Val` | `VARCHAR(100)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### MARKET_SEGMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Market_Segment_Id` | `INTEGER` | Y | NOT NULL |
| `Model_Id` | `INTEGER` |  | NOT NULL |
| `Model_Run_Id` | `INTEGER` |  | NOT NULL |
| `Segment_Desc` | `VARCHAR(250)` |  | NULL |
| `Segment_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Segment_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Segment_Group_Id` | `INTEGER` |  | NULL |
| `Segment_Name` | `VARCHAR(100)` |  | NULL |
| `Segment_Creator_Party_Id` | `INTEGER` |  | NULL |
| `Market_Segment_Scheme_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_CREDIT_REPORT_SCORE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Reporting_Party_Id` | `INTEGER` |  | NOT NULL |
| `Obligor_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Credit_Report_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Score_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Credit_Report_Score_Num` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_MEDICAL

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Data_Source_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Individual_Medical_Start_Dt` | `DATE` |  | NOT NULL |
| `Individual_Medical_End_Dt` | `DATE` |  | NULL |
| `Physical_Exam_Dt` | `DATE` |  | NULL |
| `General_Medical_Status_Cd` | `VARCHAR(50)` |  | NULL |
| `Last_Menstrual_Period_Dt` | `DATE` |  | NULL |
| `Last_X_ray_Dt` | `DATE` |  | NULL |
| `Estimated_Pregnancy_Due_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INDIVIDUAL_SPECIAL_NEED

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Individual_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Special_Need_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### SPECIAL_NEED_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Special_Need_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Special_Need_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GENDER_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Gender_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Gender_Type_Desc` | `VARCHAR(250)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GENDER_PRONOUN

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Gender_Pronoun_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Gender_Pronoun_Name` | `VARCHAR(100)` |  | NULL |
| `Gender_Pronoun_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ETHNICITY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Ethnicity_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Ethnicity_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### MARITAL_STATUS_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Marital_Status_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Marital_Status_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### NATIONALITY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Nationality_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Nationality_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### TAX_BRACKET_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Tax_Bracket_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Tax_Bracket_Desc` | `VARCHAR(250)` |  | NULL |
| `Tax_Bracket_Rate` | `DECIMAL(15,12)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### VERY_IMPORTANT_PERSON_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `VIP_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `VIP_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### MILITARY_STATUS_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Military_Status_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Military_Status_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### OCCUPATION_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Occupation_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Occupation_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### TIME_PERIOD_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Time_Period_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Time_Period_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_RELATED_STATUS_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Related_Status_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Party_Related_Status_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GENERAL_MEDICAL_STATUS_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `General_Medical_Status_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `General_Medical_Status_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### RISK_EXPOSURE_MITIGANT_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Risk_Exposure_Mitigant_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Risk_Exposure_Mitigant_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PRICING_METHOD_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Pricing_Method_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Pricing_Method_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### FINANCIAL_AGREEMENT_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Financial_Agreement_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Financial_Agreement_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CREDIT_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Seniority_Level_Cd` | `VARCHAR(50)` |  | NULL |
| `Credit_Agreement_Reaging_Cnt` | `INTEGER` |  | NULL |
| `Credit_Agreement_Past_Due_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Credit_Agreement_Charge_Off_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Credit_Agreement_Impairment_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Credit_Agreement_Settlement_Dt` | `DATE` |  | NULL |
| `Credit_Agreement_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Obligor_Borrowing_Purpose_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Currency_Past_Due_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Charge_Off_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Last_Payment_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Impairment_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Specialized_Lending_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Credit_Agreement_Grace_Period_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Payment_Frequency_Time_Period_Cd` | `VARCHAR(50)` |  | NULL |
| `Credit_Agreement_Last_Payment_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Credit_Agreement_Last_Payment_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PAYMENT_TIMING_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Payment_Timing_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Payment_Timing_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PURCHASE_INTENT_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Purchase_Intent_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Purchase_Intent_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### LOAN_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Loan_Maturity_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Security_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Due_Day_Num` | `VARCHAR(50)` |  | NULL |
| `Realizable_Collateral_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Loan_Payoff_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Real_Collateral_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Loan_Payoff_Amt` | `DECIMAL(18,4)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### SECURITY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Security_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Security_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### LOAN_MATURITY_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Loan_Maturity_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Loan_Maturity_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### LOAN_TRANSACTION_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Loan_Transaction_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### LOAN_TRANSACTION_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Loan_Transaction_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Loan_Transaction_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CREDIT_CARD_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Credit_Card_Agreement_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Credit_Card_Activation_Dttm` | `TIMESTAMP` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CREDIT_CARD_AGREEMENT_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Credit_Card_Agreement_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Credit_Card_Agreement_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### LOAN_TERM_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Amortization_Method_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Amortization_End_Dt` | `DATE` |  | NULL |
| `Balloon_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Loan_Term_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Original_Loan_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Preapproved_Loan_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Maximum_Monthly_Payment_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Improvement_Allocation_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Debt_Payment_Allocation_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Down_Payment_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Loan_Maturity_Dt` | `DATE` |  | NULL |
| `Loan_Termination_Dt` | `DATE` |  | NULL |
| `Loan_Renewal_Dt` | `DATE` |  | NULL |
| `Commit_Start_Dt` | `DATE` |  | NULL |
| `Commit_End_Dt` | `DATE` |  | NULL |
| `Payoff_Dt` | `DATE` |  | NULL |
| `Loan_Asset_Purchase_Dt` | `DATE` |  | NULL |
| `Agreement_Currency_Balloon_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Original_Loan_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Preapproved_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Maximum_Monthly_Payment_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Improve_Allocation_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Debt_Payment_Allocation_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Loan_Refinance_Ind` | `CHAR(3)` |  | NULL |
| `Agreement_Currency_Down_Payment_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Down_Payment_Borrow_Amt` | `DECIMAL(18,4)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### LOAN_TERM_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Loan_Term_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Loan_Term_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AMORTIZATION_METHOD_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Amortization_Method_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Amortization_Method_Desc` | `VARCHAR(250)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### MORTGAGE_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `First_Time_Mortgage_Ind` | `CHAR(3)` |  | NULL |
| `Closing_Cost_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Adjustable_Payment_Cap_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Prepayment_Penalty_Dt` | `DATE` |  | NULL |
| `Early_Payoff_Penalty_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Closing_Cost_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Adjustable_Cap_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Currency_Early_Penalty_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Mortgage_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### MORTGAGE_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Mortgage_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Mortgage_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### TERM_FEATURE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Feature_Id` | `INTEGER` | Y | NOT NULL |
| `From_Time_Period_Cd` | `VARCHAR(50)` |  | NULL |
| `To_Time_Period_Cd` | `VARCHAR(50)` |  | NULL |
| `Until_Age_Cd` | `VARCHAR(50)` |  | NULL |
| `From_Time_Period_Num` | `VARCHAR(50)` |  | NULL |
| `To_Time_Period_Num` | `VARCHAR(50)` |  | NULL |
| `Until_Age_Num` | `VARCHAR(50)` |  | NULL |
| `Term_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INTEREST_RATE_INDEX

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Interest_Rate_Index_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Interest_Rate_Index_Desc` | `VARCHAR(250)` |  | NULL |
| `Interest_Rate_Index_Short_Name` | `VARCHAR(100)` |  | NULL |
| `Currency_Cd` | `VARCHAR(50)` |  | NULL |
| `Yield_Curve_Maturity_Segment_Cd` | `VARCHAR(50)` |  | NULL |
| `Compound_Frequency_Time_Period_Cd` | `VARCHAR(50)` |  | NULL |
| `Interest_Rate_Index_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Interest_Rate_Index_Time_Period_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Interest_Index_Time_Period_Num` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### AGREEMENT_FEATURE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Agreement_Id` | `INTEGER` | Y | NOT NULL |
| `Feature_Id` | `INTEGER` |  | NOT NULL |
| `Agreement_Feature_Role_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Agreement_Feature_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Agreement_Feature_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Overridden_Feature_Id` | `INTEGER` |  | NULL |
| `Agreement_Feature_Concession_Ind` | `CHAR(3)` |  | NULL |
| `Agreement_Feature_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Feature_To_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Feature_Rate` | `DECIMAL(15,12)` |  | NULL |
| `Agreement_Feature_Qty` | `DECIMAL(18,4)` |  | NULL |
| `Agreement_Feature_Num` | `VARCHAR(50)` |  | NULL |
| `Agreement_Feature_Dt` | `DATE` |  | NULL |
| `Agreement_Feature_UOM_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Interest_Rate_Index_Cd` | `VARCHAR(50)` |  | NULL |
| `Currency_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INTEREST_INDEX_RATE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Interest_Rate_Index_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Index_Rate_Effective_Dttm` | `DATE` |  | NOT NULL |
| `Interest_Index_Rate` | `DECIMAL(15,12)` |  | NULL |
| `Discount_Factor_Pct` | `DECIMAL(9,4)` |  | NULL |
| `Zero_Coupon_Rate` | `DECIMAL(15,12)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### VARIABLE_INTEREST_RATE_FEATURE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Feature_Id` | `INTEGER` | Y | NOT NULL |
| `Spread_Rate` | `DECIMAL(15,12)` |  | NULL |
| `Interest_Rate_Index_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Upper_Limit_Rate` | `DECIMAL(15,12)` |  | NULL |
| `Lower_Limit_Rate` | `DECIMAL(15,12)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ORGANIZATION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Organization_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Organization_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Organization_Established_Dttm` | `TIMESTAMP` |  | NULL |
| `Parent_Organization_Party_Id` | `INTEGER` |  | NULL |
| `Organization_Size_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Legal_Classification_Cd` | `VARCHAR(50)` |  | NULL |
| `Ownership_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Organization_Close_Dt` | `DATE` |  | NULL |
| `Organization_Operation_Dt` | `DATE` |  | NULL |
| `Organization_Fiscal_Month_Num` | `VARCHAR(50)` |  | NULL |
| `Organization_Fiscal_Day_Num` | `VARCHAR(50)` |  | NULL |
| `Basel_Organization_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Basel_Market_Participant_Cd` | `VARCHAR(50)` |  | NULL |
| `Basel_Eligible_Central_Ind` | `CHAR(3)` |  | NULL |
| `BIC_Business_Alpha_4_Cd` | `CHAR(4)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### BUSINESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Business_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Business_Category_Cd` | `VARCHAR(50)` |  | NULL |
| `Business_Legal_Start_Dt` | `DATE` |  | NULL |
| `Business_Legal_End_Dt` | `DATE` |  | NULL |
| `Tax_Bracket_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Customer_Location_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Stock_Exchange_Listed_Ind` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### BUSINESS_CATEGORY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Business_Category_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Business_Category_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ORGANIZATION_NAICS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Organization_Party_Id` | `INTEGER` | Y | NOT NULL |
| `NAICS_National_Industry_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Organization_NAICS_Start_Dt` | `DATE` |  | NOT NULL |
| `NAICS_Sector_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NAICS_Subsector_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NAICS_Industry_Group_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NAICS_Industry_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Organization_NAICS_End_Dt` | `DATE` |  | NULL |
| `Primary_NAICS_Ind` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ORGANIZATION_NACE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Organization_Party_Id` | `INTEGER` | Y | NOT NULL |
| `NACE_Class_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NACE_Group_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NACE_Division_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NACE_Section_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Organization_NACE_Start_Dt` | `DATE` |  | NOT NULL |
| `Organization_NACE_End_Dt` | `DATE` |  | NULL |
| `Importance_Order_NACE_Num` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### NACE_CLASS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `NACE_Class_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `NACE_Group_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NACE_Division_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NACE_Section_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NACE_Class_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ORGANIZATION_SIC

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Organization_Party_Id` | `INTEGER` | Y | NOT NULL |
| `SIC_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Organization_SIC_Start_Dt` | `DATE` |  | NOT NULL |
| `Organization_SIC_End_Dt` | `DATE` |  | NULL |
| `Primary_SIC_Ind` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ORGANIZATION_GICS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Organization_Party_Id` | `INTEGER` | Y | NOT NULL |
| `GICS_Subindustry_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `GICS_Industry_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `GICS_Industry_Group_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `GICS_Sector_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Organization_GICS_Start_Dt` | `DATE` |  | NOT NULL |
| `Organization_GICS_End_Dt` | `DATE` |  | NULL |
| `Primary_GICS_Ind` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_SPECIALTY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Specialty_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Specialty_Start_Dt` | `DATE` |  | NOT NULL |
| `Party_Specialty_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### LEGAL_CLASSIFICATION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Legal_Classification_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Legal_Classification_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### NAICS_INDUSTRY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `NAICS_Industry_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `NAICS_Sector_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `NAICS_Subsector_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `NAICS_Industry_Group_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `NAICS_Industry_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### SIC

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `SIC_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `SIC_Desc` | `VARCHAR(250)` |  | NULL |
| `SIC_Group_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GICS_INDUSTRY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `GICS_Industry_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `GICS_Industry_Group_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `GICS_Sector_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `GICS_Industry_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GICS_SUBINDUSTRY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `GICS_Subindustry_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `GICS_Industry_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `GICS_Industry_Group_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `GICS_Sector_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `GICS_Subindustry_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GICS_INDUSTRY_GROUP_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `GICS_Industry_Group_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `GICS_Sector_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `GICS_Industry_Group_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GICS_SECTOR_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `GICS_Sector_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `GICS_Sector_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### SPECIALTY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Specialty_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Specialty_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ORGANIZATION_NAME

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Organization_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Name_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Organization_Name_Start_Dt` | `DATE` |  | NOT NULL |
| `Organization_Name` | `VARCHAR(100)` |  | NOT NULL |
| `Organization_Name_Desc` | `VARCHAR(250)` |  | NULL |
| `Organization_Name_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_IDENTIFICATION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Issuing_Party_Id` | `INTEGER` |  | NOT NULL |
| `Party_Identification_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Identification_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Party_Identification_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Party_Identification_Num` | `VARCHAR(50)` |  | NULL |
| `Party_Identification_Receipt_Dt` | `DATE` |  | NULL |
| `Party_Identification_Primary_Ind` | `CHAR(3)` |  | NULL |
| `Party_Identification_Name` | `VARCHAR(100)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_LANGUAGE_USAGE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Language_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Language_Usage_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Language_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Party_Language_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Party_Language_Priority_Num` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### LANGUAGE_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Language_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Language_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `Language_Native_Name` | `VARCHAR(100)` |  | NULL |
| `ISO_Language_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PROMOTION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Promotion_Id` | `INTEGER` | Y | NOT NULL |
| `Promotion_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Campaign_Id` | `INTEGER` |  | NOT NULL |
| `Promotion_Classification_Cd` | `VARCHAR(50)` |  | NULL |
| `Channel_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Internal_Promotion_Name` | `VARCHAR(100)` |  | NULL |
| `Promotion_Desc` | `VARCHAR(250)` |  | NULL |
| `Promotion_Objective_Txt` | `VARCHAR(1000)` |  | NULL |
| `Promotion_Start_Dt` | `DATE` |  | NULL |
| `Promotion_End_Dt` | `DATE` |  | NULL |
| `Promotion_Actual_Unit_Cost_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Promotion_Goal_Amt` | `DECIMAL(18,4)` |  | NULL |
| `Currency_Cd` | `VARCHAR(50)` |  | NULL |
| `Promotion_Actual_Unit_Cnt` | `INTEGER` |  | NULL |
| `Promotion_Break_Even_Order_Cnt` | `INTEGER` |  | NULL |
| `Unit_Of_Measure_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PROMOTION_METRIC_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Promotion_Metric_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Promotion_Metric_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### UNIT_OF_MEASURE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Unit_Of_Measure_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Unit_Of_Measure_Name` | `VARCHAR(100)` |  | NULL |
| `Unit_Of_Measure_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PROMOTION_OFFER

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Promotion_Id` | `INTEGER` | Y | NOT NULL |
| `Promotion_Offer_Id` | `INTEGER` |  | NOT NULL |
| `Promotion_Offer_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Promotion_Offer_Desc` | `VARCHAR(250)` |  | NULL |
| `Ad_Id` | `INTEGER` |  | NULL |
| `Distribution_Start_Dt` | `DATE` |  | NULL |
| `Distribution_End_Dt` | `DATE` |  | NULL |
| `Redemption_Start_Dt` | `DATE` |  | NULL |
| `Redemption_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PROMOTION_OFFER_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Promotion_Offer_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Promotion_Offer_Type_Desc` | `VARCHAR(250)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### STREET_ADDRESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Street_Address_Id` | `INTEGER` | Y | NOT NULL |
| `Address_Line_1_Txt` | `VARCHAR(1000)` |  | NULL |
| `Address_Line_2_Txt` | `VARCHAR(1000)` |  | NULL |
| `Address_Line_3_Txt` | `VARCHAR(1000)` |  | NULL |
| `Dwelling_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Census_Block_Id` | `INTEGER` |  | NULL |
| `City_Id` | `INTEGER` |  | NULL |
| `County_Id` | `INTEGER` |  | NULL |
| `Territory_Id` | `INTEGER` |  | NULL |
| `Postal_Code_Id` | `INTEGER` |  | NULL |
| `Country_Id` | `INTEGER` |  | NULL |
| `Carrier_Route_Txt` | `VARCHAR(1000)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### STREET_ADDRESS_DETAIL

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Street_Address_Id` | `INTEGER` | Y | NOT NULL |
| `Street_Address_Num` | `VARCHAR(50)` |  | NOT NULL |
| `Street_Address_Number_Modifier_Val` | `VARCHAR(100)` |  | NULL |
| `Street_Direction_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Street_Num` | `VARCHAR(50)` |  | NULL |
| `Street_Name` | `VARCHAR(100)` |  | NOT NULL |
| `Street_Suffix_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Building_Num` | `VARCHAR(50)` |  | NULL |
| `Unit_Num` | `VARCHAR(50)` |  | NULL |
| `Floor_Val` | `VARCHAR(100)` |  | NULL |
| `Workspace_Num` | `VARCHAR(50)` |  | NULL |
| `Route_Num` | `VARCHAR(50)` |  | NULL |
| `Mail_Pickup_Tm` | `TIME` |  | NOT NULL |
| `Mail_Delivery_Tm` | `TIME` |  | NOT NULL |
| `Mail_Stop_Num` | `VARCHAR(50)` |  | NOT NULL |
| `Mail_Box_Num` | `VARCHAR(50)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### DIRECTION_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Direction_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Direction_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### STREET_SUFFIX_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Street_Suffix_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Street_Suffix_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ISO_3166_COUNTRY_SUBDIVISION_STANDARD

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Territory_Id` | `INTEGER` | Y | NOT NULL |
| `Territory_Standard_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `ISO_3166_Country_Alpha_2_Cd` | `CHAR(2)` |  | NULL |
| `ISO_3166_Country_Subdivision_Cd` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### POSTAL_CODE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Postal_Code_Id` | `INTEGER` | Y | NOT NULL |
| `County_Id` | `INTEGER` |  | NULL |
| `Country_Id` | `INTEGER` |  | NOT NULL |
| `Postal_Code_Num` | `VARCHAR(50)` |  | NULL |
| `Time_Zone_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CITY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `City_Id` | `INTEGER` | Y | NOT NULL |
| `City_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Territory_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GEOGRAPHICAL_AREA

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Geographical_Area_Id` | `INTEGER` | Y | NOT NULL |
| `Geographical_Area_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Geographical_Area_Short_Name` | `VARCHAR(100)` |  | NULL |
| `Geographical_Area_Name` | `VARCHAR(100)` |  | NULL |
| `Geographical_Area_Desc` | `VARCHAR(250)` |  | NULL |
| `Geographical_Area_Start_Dt` | `DATE` |  | NULL |
| `Geographical_Area_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Geographical_Area_Id` | `INTEGER` | Y | NOT NULL |
| `Geographical_Area_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Geographical_Area_Short_Name` | `VARCHAR(100)` |  | NULL |
| `Geographical_Area_Name` | `VARCHAR(100)` |  | NULL |
| `Geographical_Area_Desc` | `VARCHAR(250)` |  | NULL |
| `Geographical_Area_Start_Dt` | `DATE` |  | NULL |
| `Geographical_Area_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GEOGRAPHICAL_AREA_CURRENCY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Geographical_Area_Id` | `INTEGER` | Y | NOT NULL |
| `Currency_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Geographical_Area_Currency_Start_Dt` | `DATE` |  | NOT NULL |
| `Geographical_Area_Currency_Role_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Geographical_Area_Currency_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Geographical_Area_Id` | `INTEGER` | Y | NOT NULL |
| `Currency_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Geographical_Area_Currency_Start_Dt` | `DATE` |  | NOT NULL |
| `Geographical_Area_Currency_Role_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Geographical_Area_Currency_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CITY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `City_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `City_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `City_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `City_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### COUNTRY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Country_Id` | `INTEGER` | Y | NOT NULL |
| `Calendar_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Country_Group_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### CALENDAR_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Calendar_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Calendar_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Calendar_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Calendar_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ISO_3166_COUNTRY_STANDARD

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Country_Id` | `INTEGER` |  | NOT NULL |
| `Country_Code_Standard_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `ISO_3166_Country_3_Num` | `CHAR(3)` | Y | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Country_Id` | `INTEGER` |  | NOT NULL |
| `Country_Code_Standard_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `ISO_3166_Country_3_Num` | `CHAR(3)` | Y | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### COUNTY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `County_Id` | `INTEGER` | Y | NOT NULL |
| `Territory_Id` | `INTEGER` |  | NOT NULL |
| `MSA_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARCEL_ADDRESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Parcel_Address_Id` | `INTEGER` | Y | NOT NULL |
| `Page_Num` | `VARCHAR(50)` |  | NULL |
| `Map_Num` | `VARCHAR(50)` |  | NULL |
| `Parcel_Num` | `VARCHAR(50)` |  | NULL |
| `City_Id` | `INTEGER` |  | NULL |
| `County_Id` | `INTEGER` |  | NULL |
| `Country_Id` | `INTEGER` |  | NULL |
| `Postal_Code_Id` | `INTEGER` |  | NULL |
| `Territory_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Parcel_Address_Id` | `INTEGER` | Y | NOT NULL |
| `Page_Num` | `VARCHAR(50)` |  | NULL |
| `Map_Num` | `VARCHAR(50)` |  | NULL |
| `Parcel_Num` | `VARCHAR(50)` |  | NULL |
| `City_Id` | `INTEGER` |  | NULL |
| `County_Id` | `INTEGER` |  | NULL |
| `Country_Id` | `INTEGER` |  | NULL |
| `Postal_Code_Id` | `INTEGER` |  | NULL |
| `Territory_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### POST_OFFICE_BOX_ADDRESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Post_Office_Box_Id` | `INTEGER` | Y | NOT NULL |
| `Post_Office_Box_Num` | `VARCHAR(50)` |  | NULL |
| `City_Id` | `INTEGER` |  | NULL |
| `County_Id` | `INTEGER` |  | NULL |
| `Country_Id` | `INTEGER` |  | NULL |
| `Postal_Code_Id` | `INTEGER` |  | NULL |
| `Territory_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Post_Office_Box_Id` | `INTEGER` | Y | NOT NULL |
| `Post_Office_Box_Num` | `VARCHAR(50)` |  | NULL |
| `City_Id` | `INTEGER` |  | NULL |
| `County_Id` | `INTEGER` |  | NULL |
| `Country_Id` | `INTEGER` |  | NULL |
| `Postal_Code_Id` | `INTEGER` |  | NULL |
| `Territory_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### REGION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Region_Id` | `INTEGER` | Y | NOT NULL |
| `Country_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### TERRITORY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Territory_Id` | `INTEGER` | Y | NOT NULL |
| `Territory_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Country_Id` | `INTEGER` |  | NOT NULL |
| `Region_Id` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### TERRITORY_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Territory_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Territory_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Territory_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Territory_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GEOSPATIAL_POINT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Geospatial_Point_Id` | `INTEGER` | Y | NOT NULL |
| `Latitude_Meas` | `DECIMAL(18,4)` |  | NULL |
| `Longitude_Meas` | `DECIMAL(18,4)` |  | NULL |
| `Elevation_Meas` | `DECIMAL(18,4)` |  | NULL |
| `Elevation_UOM_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Geospatial_Point_Id` | `INTEGER` | Y | NOT NULL |
| `Latitude_Meas` | `DECIMAL(18,4)` |  | NULL |
| `Longitude_Meas` | `DECIMAL(18,4)` |  | NULL |
| `Elevation_Meas` | `DECIMAL(18,4)` |  | NULL |
| `Elevation_UOM_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### GEOSPATIAL

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Geospatial_Id` | `INTEGER` | Y | NOT NULL |
| `Geospatial_Roadway_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Geospatial_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### UNIT_OF_MEASURE_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Unit_Of_Measure_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Unit_Of_Measure_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Unit_Of_Measure_Type_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Unit_Of_Measure_Type_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### LOCATOR_RELATED

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Locator_Id` | `INTEGER` | Y | NOT NULL |
| `Related_Locator_Id` | `INTEGER` |  | NOT NULL |
| `Locator_Related_Reason_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Locator_Related_Start_Dt` | `DATE` |  | NOT NULL |
| `Locator_Related_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `Locator_Id` | `INTEGER` | Y | NOT NULL |
| `Related_Locator_Id` | `INTEGER` |  | NOT NULL |
| `Locator_Related_Reason_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Locator_Related_Start_Dt` | `DATE` |  | NOT NULL |
| `Locator_Related_End_Dt` | `DATE` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ANALYTICAL_MODEL

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Model_Id` | `INTEGER` | Y | NOT NULL |
| `Model_Name` | `VARCHAR(100)` |  | NULL |
| `Model_Desc` | `VARCHAR(250)` |  | NULL |
| `Model_Version_Num` | `VARCHAR(50)` |  | NULL |
| `Model_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Model_Algorithm_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Data_Source_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `Model_From_Dttm` | `TIMESTAMP` |  | NULL |
| `Model_To_Dttm` | `TIMESTAMP` |  | NULL |
| `Model_Predict_Time_Period_Cnt` | `INTEGER` |  | NULL |
| `Model_Predict_Time_Period_Cd` | `VARCHAR(50)` |  | NULL |
| `Model_Purpose_Cd` | `VARCHAR(50)` |  | NULL |
| `Attestation_Ind` | `CHAR(3)` |  | NULL |
| `Model_Target_Run_Dt` | `DATE` |  | NULL |
| `Locator_Id` | `INTEGER` |  | NULL |
| `Criticality_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_DEMOGRAPHIC

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Demographic_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Data_Source_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Demographic_Start_Dt` | `DATE` |  | NOT NULL |
| `Demographic_Value_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Demographic_End_Dt` | `DATE` |  | NULL |
| `Party_Demographic_Num` | `VARCHAR(50)` |  | NULL |
| `Party_Demographic_Val` | `VARCHAR(100)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Party_Subtype_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Desc` | `VARCHAR(250)` |  | NULL |
| `Party_Start_Dttm` | `TIMESTAMP` |  | NULL |
| `Party_End_Dttm` | `TIMESTAMP` |  | NULL |
| `Party_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Initial_Data_Source_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### HOUSEHOLD

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Household_Party_Id` | `INTEGER` | Y | NOT NULL |
| `Party_Household_Child_Cnt` | `INTEGER` |  | NULL |
| `Party_Household_Cnt` | `INTEGER` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### DEMOGRAPHIC_VALUE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Demographic_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Demographic_Value_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Demographic_Range_Start_Val` | `VARCHAR(100)` |  | NULL |
| `Demographic_Range_End_Val` | `VARCHAR(100)` |  | NULL |
| `Demographic_Value_Desc` | `VARCHAR(250)` |  | NULL |
| `Demographic_Val` | `VARCHAR(100)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_LOCATOR

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Locator_Id` | `INTEGER` |  | NOT NULL |
| `Locator_Usage_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Party_Locator_Start_Dttm` | `DATE` |  | NOT NULL |
| `Party_Locator_End_Dttm` | `DATE` |  | NULL |
| `Data_Quality_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ELECTRONIC_ADDRESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Electronic_Address_Id` | `INTEGER` | Y | NOT NULL |
| `Electronic_Address_Subtype_Cd` | `VARCHAR(50)` |  | NULL |
| `Electronic_Address_Txt` | `VARCHAR(1000)` |  | NULL |
| `Electronic_Address_Domain_Name` | `VARCHAR(100)` |  | NULL |
| `Domain_Root_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### ELECTRONIC_ADDRESS_SUBTYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Electronic_Address_Subtype_Cd` | `VARCHAR(50)` | Y | NOT NULL |
| `Electronic_Address_Subtype_Desc` | `VARCHAR(250)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### INTERNET_PROTOCOL_ADDRESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Internet_Protocol_Address_Id` | `INTEGER` | Y | NOT NULL |
| `Internet_Protocol_Address_Num` | `VARCHAR(50)` |  | NOT NULL |
| `Internet_Protocol_Registered_By_Party_Id` | `INTEGER` |  | NULL |
| `Internet_Protocol_Network_Name` | `VARCHAR(100)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### TELEPHONE_NUMBER

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Telephone_Number_Id` | `INTEGER` | Y | NOT NULL |
| `Telephone_Num` | `VARCHAR(50)` |  | NULL |
| `Telephone_Country_Code_Num` | `VARCHAR(50)` |  | NULL |
| `Telephone_Area_Code_Num` | `VARCHAR(50)` |  | NULL |
| `Telephone_Exchange_Num` | `VARCHAR(50)` |  | NULL |
| `Telephone_Line_Num` | `VARCHAR(50)` |  | NULL |
| `Telephone_Extension_Num` | `VARCHAR(50)` |  | NULL |
| `Telephone_Number_Type_Cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_TASK

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Task_Id` | `BIGINT` | Y | NOT NULL |
| `Party_Id` | `BIGINT` |  | NULL |
| `Source_Event_Id` | `BIGINT` |  | NULL |
| `Task_Activity_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Task_Subtype_Cd` | `SMALLINT` |  | NOT NULL |
| `Task_Reason_Cd` | `SMALLINT` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### TASK_ACTIVITY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Activity_Id` | `BIGINT` | Y | NOT NULL |
| `Task_Id` | `BIGINT` |  | NULL |
| `Activity_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Activity_Txt` | `VARCHAR(32000)` |  | NULL |
| `Activity_Channel_Id` | `BIGINT` |  | NULL |
| `Activity_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Activity_End_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PARTY_TASK_STATUS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Task_Status_Id` | `BIGINT` | Y | NOT NULL |
| `Task_Id` | `BIGINT` |  | NULL |
| `Task_Status_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Task_Status_End_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Task_Status_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Task_Status_Reason_Cd` | `SMALLINT` |  | NOT NULL |
| `Task_Status_Txt` | `VARCHAR(32000)` |  | NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### TASK_ACTIVITY_STATUS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Activity_Id` | `BIGINT` | Y | NOT NULL |
| `Activity_Status_Start_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Activity_Status_End_Dttm` | `TIMESTAMP` |  | NOT NULL |
| `Activity_Status_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Activity_Status_Reason_Cd` | `SMALLINT` |  | NOT NULL |
| `Activity_Status_Txt` | `VARCHAR(32000)` |  | NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PARTY_ADDRESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Address_Usage_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Address_Id` | `INTEGER` |  | NOT NULL |
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Party_Address_Start_Dt` | `DATE` |  | NOT NULL |
| `Party_Address_End_Dt` | `DATE` |  | NULL |
| `Default_Ind` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

#### PRODUCT_TO_GROUP

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `PIM_Id` | `BIGINT` | Y | NOT NULL |
| `Group_Id` | `BIGINT` |  | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

### CDM Tables (CDM_DB)

#### PARTY

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Source_Cd` | `SMALLINT` |  | NOT NULL |
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Source_Party_Id` | `BIGINT` |  | NOT NULL |
| `Party_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Party_Lifecycle_Phase_Cd` | `SMALLINT` |  | NOT NULL |
| `Party_Since` | `DATE` |  | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `Survival_Record_Ind` | `CHAR(1)` |  | NOT NULL |
| `DQ_Score` | `DECIMAL(5,2)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### ORGANIZATION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Organization_Name` | `VARCHAR(255)` |  | NULL |
| `Business_Identifier` | `VARCHAR(255)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### INDIVIDUAL

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `First_Name` | `VARCHAR(255)` |  | NULL |
| `Middle_Name` | `VARCHAR(255)` |  | NULL |
| `Last_Name` | `VARCHAR(255)` |  | NULL |
| `Birth_Dt` | `DATE` |  | NOT NULL |
| `Gender` | `VARCHAR(50)` |  | NULL |
| `Salutation` | `VARCHAR(50)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `DQ_Score` | `DECIMAL(5,2)` |  | NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### INDIVIDUAL_TO_INDIVIDUAL

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Parent_CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Relationship_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Relationship_Value_Cd` | `SMALLINT` |  | NOT NULL |
| `Probability` | `DECIMAL(5,4)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### INDIVIDUAL_TO_HOUSEHOLD

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `CDM_Household_Id` | `BIGINT` | Y | NOT NULL |
| `Role_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Probability` | `DECIMAL(5,4)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### HOUSEHOLD

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Household_Id` | `BIGINT` | Y | NOT NULL |
| `Household_Name` | `VARCHAR(255)` |  | NULL |
| `Household_Desc` | `VARCHAR(255)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### INDIVIDUAL_TO_ORGANIZATION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Parent_CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Relationship_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Relationship_Value_Cd` | `SMALLINT` |  | NOT NULL |
| `Probability` | `DECIMAL(5,4)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### ORGANIZATION_TO_ORGANIZATION

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Parent_CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Relationship_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Relationship_Value_Cd` | `SMALLINT` |  | NOT NULL |
| `Probability` | `DECIMAL(5,4)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PARTY_TO_AGREEMENT_ROLE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Agreement_Id` | `BIGINT` | Y | NOT NULL |
| `Role_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PARTY_TO_EVENT_ROLE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Event_Id` | `BIGINT` | Y | NOT NULL |
| `Role_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PARTY_SEGMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Party_Id` | `BIGINT` | Y | NOT NULL |
| `Segment_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Segment_Value_Cd` | `SMALLINT` |  | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### ADDRESS_TO_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Address_Id` | `BIGINT` | Y | NOT NULL |
| `Agreement_Id` | `BIGINT` | Y | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PARTY_CONTACT
_SQL file table: `CDM_DB.CONTACT`_  

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Contact_Id` | `BIGINT` | Y | NOT NULL |
| `Contact_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Contact_Value` | `VARCHAR(255)` |  | NULL |
| `Primary_Contact_Ind` | `CHAR(1)` |  | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### CONTACT_TO_AGREEMENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Contact_Id` | `BIGINT` | Y | NOT NULL |
| `Agreement_Id` | `BIGINT` | Y | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PARTY_INTERRACTION_EVENT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Event_Id` | `BIGINT` | Y | NOT NULL |
| `CDM_Party_Id` | `BIGINT` |  | NOT NULL |
| `Event_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Event_Channel_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Event_Dt` | `DATE` |  | NOT NULL |
| `Event_Sentiment_Cd` | `SMALLINT` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### ADDRESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `CDM_Address_Id` | `BIGINT` | Y | NOT NULL |
| `Address_Id` | `BIGINT` |  | NOT NULL |
| `Address_Type` | `VARCHAR(255)` |  | NULL |
| `Address_Country_Cd` | `SMALLINT` |  | NOT NULL |
| `Address_County` | `VARCHAR(255)` |  | NULL |
| `Address_City` | `VARCHAR(255)` |  | NULL |
| `Address_Street` | `VARCHAR(255)` |  | NULL |
| `Address_Postal_Code` | `VARCHAR(20)` |  | NULL |
| `Primary_Address_Flag` | `CHAR(1)` |  | NULL |
| `Geo_Latitude` | `DECIMAL(9,6)` |  | NULL |
| `Geo_Longitude` | `DECIMAL(9,6)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

### PIM Tables (PIM_DB)

#### PRODUCT_TO_GROUP

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `PIM_Id` | `BIGINT` | Y | NOT NULL |
| `Group_Id` | `BIGINT` |  | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PRODUCT

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `PIM_Id` | `BIGINT` | Y | NOT NULL |
| `Product_Id` | `BIGINT` |  | NOT NULL |
| `PIM_Product_Name` | `VARCHAR(255)` |  | NULL |
| `PIM_Product_Desc` | `VARCHAR(32000)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PRODUCT_PARAMETERS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `PIM_Parameter_Id` | `BIGINT` | Y | NOT NULL |
| `PIM_Id` | `BIGINT` |  | NOT NULL |
| `PIM_Parameter_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `PIM_Parameter_Value` | `VARCHAR(1000)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PRODUCT_PARAMETER_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `PIM_Parameter_Type_Cd` | `SMALLINT` | Y | NOT NULL |
| `PIM_Parameter_Type_Desc` | `VARCHAR(255)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PRODUCT_GROUP

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Product_Group_Id` | `BIGINT` | Y | NOT NULL |
| `Parent_Group_Id` | `BIGINT` |  | NOT NULL |
| `Product_Group_Type_Cd` | `SMALLINT` |  | NOT NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

#### PRODUCT_GROUP_TYPE

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Product_Group_Type_Cd` | `SMALLINT` | Y | NOT NULL |
| `Product_Group_Type_Name` | `VARCHAR(255)` |  | NULL |
| `Product_Group_Type_Desc` | `VARCHAR(1000)` |  | NULL |
| `Valid_From_Dt` | `DATE` |  | NOT NULL |
| `Valid_To_Dt` | `DATE` |  | NOT NULL |
| `Del_Ind` | `CHAR(1)` |  | NOT NULL |
| `di_data_src_cd` | `VARCHAR(50)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_proc_name` | `VARCHAR(255)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |

### Unresolved MDM Tables

#### PARTY_ADDRESS

| Column Name | Type (from DDL) | PK | Nullable |
|-------------|-----------------|----| ---------|
| `Party_Address_Usage_Type_Cd` | `VARCHAR(50)` |  | NOT NULL |
| `Address_Id` | `INTEGER` |  | NOT NULL |
| `Party_Id` | `INTEGER` | Y | NOT NULL |
| `Party_Address_Start_Dt` | `DATE` |  | NOT NULL |
| `Party_Address_End_Dt` | `DATE` |  | NULL |
| `Default_Ind` | `CHAR(3)` |  | NULL |
| `di_start_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_end_ts` | `TIMESTAMP(6)` |  | NULL |
| `di_rec_deleted_Ind` | `CHAR(1)` |  | NULL |

---

## DDL Anomalies & Notes

1. **Excel table-name typo** — Excel row labelled `AGREEMEN_FEATURE` is a duplicate of `AGREEMENT_FEATURE` (same DDL, different spelling in column B). The typo entry has been removed; only `AGREEMENT_FEATURE` is included in this document.
2. **INTEGER FK candidate** — `AGREEMENT_SCORE.Model_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
3. **INTEGER FK candidate** — `AGREEMENT_SCORE.Model_Run_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
4. **INTEGER FK candidate** — `PARTY_AGREEMENT.Party_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
5. **INTEGER FK candidate** — `AGREEMENT_PRODUCT.Product_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
6. **INTEGER FK candidate** — `PRODUCT_FEATURE.Feature_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
7. **INTEGER FK candidate** — `EVENT_PARTY.Party_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
8. **INTEGER FK candidate** — `ASSOCIATE_EMPLOYMENT.Organization_Party_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
9. **INTEGER FK candidate** — `INDIVIDUAL_PAY_TIMING.Business_Party_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
10. **INTEGER FK candidate** — `INDIVIDUAL_BONUS_TIMING.Business_Party_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
11. **INTEGER FK candidate** — `PARTY_RELATED.Related_Party_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
12. **INTEGER FK candidate** — `PARTY_CLAIM.Party_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
13. **INTEGER FK candidate** — `PARTY_SCORE.Model_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
14. **INTEGER FK candidate** — `PARTY_SCORE.Model_Run_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
15. **INTEGER FK candidate** — `MARKET_SEGMENT.Model_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
16. **INTEGER FK candidate** — `MARKET_SEGMENT.Model_Run_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
17. **INTEGER FK candidate** — `PARTY_CREDIT_REPORT_SCORE.Reporting_Party_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
18. **INTEGER FK candidate** — `AGREEMENT_FEATURE.Feature_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
19. **INTEGER FK candidate** — `PARTY_IDENTIFICATION.Issuing_Party_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
20. **INTEGER FK candidate** — `PROMOTION.Campaign_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
21. **INTEGER FK candidate** — `PROMOTION_OFFER.Promotion_Offer_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
22. **INTEGER FK candidate** — `POSTAL_CODE.Country_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
23. **INTEGER FK candidate** — `ISO_3166_COUNTRY_STANDARD.Country_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
24. **INTEGER FK candidate** — `COUNTY.Territory_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
25. **INTEGER FK candidate** — `TERRITORY.Country_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
26. **INTEGER FK candidate** — `LOCATOR_RELATED.Related_Locator_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
27. **INTEGER FK candidate** — `PARTY_LOCATOR.Locator_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
28. **INTEGER FK candidate** — `PARTY_ADDRESS.Address_Id` is `INTEGER` NOT NULL (non-PK `_Id` column); may need BIGINT for CDM_DB cross-schema joins.
29. **Implicit FK** — `PRODUCT_TO_GROUP.Group_Id` (`BIGINT`) is NOT NULL but not marked PK — likely references a parent table.
30. **Implicit FK** — `PARTY.Source_Party_Id` (`BIGINT`) is NOT NULL but not marked PK — likely references a parent table.
31. **Implicit FK** — `PARTY_INTERRACTION_EVENT.CDM_Party_Id` (`BIGINT`) is NOT NULL but not marked PK — likely references a parent table.
32. **Implicit FK** — `PRODUCT.Product_Id` (`BIGINT`) is NOT NULL but not marked PK — likely references a parent table.
33. **Implicit FK** — `PRODUCT_PARAMETERS.PIM_Id` (`BIGINT`) is NOT NULL but not marked PK — likely references a parent table.
34. **Implicit FK** — `PRODUCT_GROUP.Parent_Group_Id` (`BIGINT`) is NOT NULL but not marked PK — likely references a parent table.
35. **Schema unknown** — Excel MDM table `PARTY_ADDRESS` has no matching table in CDM_DB.sql or PIM_DB.sql. DDL uses CORE_DB placeholder.
36. **Schema prefix mismatch** — All MDM table DDLs in Excel column F use `CORE_DB.` prefix. Authoritative DDLs from `CDM_DB.sql` / `PIM_DB.sql` are used for column schemas above. The CORE_DB-prefixed DDL is preserved verbatim in the raw DDL section (Excel source).
37. **Name alias** — Excel MDM table `PARTY_CONTACT` (no DDL in column F) maps to `CDM_DB.CONTACT` in `CDM_DB.sql`. The CDM_DB.sql DDL is used.
38. **Missing surrogate PK** — `CDM_DB.ADDRESS` DDL does not define `CDM_Address_Id`. Per `05_architect-qa.md` Q6, a BIGINT surrogate key must be added to the generated CSV.

---

## Raw DDL

> For **CDM_DB** and **PIM_DB** tables the DDL shown is from the authoritative `CDM_DB.sql` / `PIM_DB.sql` files (correct schema prefix). For **Core_DB (iDM)** tables the DDL is from Excel column F.

### Core_DB

#### AGREEMENT

```sql
CREATE  TABLE CORE_DB.AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Agreement_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Subtype Cd',
	Host_Agreement_Num   VARCHAR(50) NULL 
		TITLE 'Host Agreement Num',
	Agreement_Name       VARCHAR(100) NULL 
		TITLE 'Agreement Name',
	Alternate_Agreement_Name VARCHAR(100) NULL 
		TITLE 'Alternate Agreement Name',
	Agreement_Open_Dttm  TIMESTAMP NULL 
		TITLE 'Agreement Open Dttm',
	Agreement_Close_Dttm TIMESTAMP NULL 
		TITLE 'Agreement Close Dttm',
	Agreement_Planned_Expiration_Dt DATE NULL 
		TITLE 'Agreement Planned Expiration Dt',
	Agreement_Processing_Dt DATE NULL 
		TITLE 'Agreement Processing Dt',
	Agreement_Signed_Dt  DATE NULL 
		TITLE 'Agreement Signed Dt',
	Agreement_Legally_Binding_Ind CHAR(3) NULL 
		TITLE 'Agreement Legally Binding Ind',
	Proposal_Id          INTEGER NULL 
		TITLE 'Proposal Id',
	Jurisdiction_Id      INTEGER NULL 
		TITLE 'Jurisdiction Id',
	Agreement_Format_Type_Cd VARCHAR(50) NULL 
		TITLE 'Agreement Format Type Cd',
	Agreement_Objective_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Objective Type Cd',
	Agreement_Obtained_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Obtained Cd',
	Agreement_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Agreement Type Cd',
	Asset_Liability_Cd   VARCHAR(50) NULL 
		TITLE 'Asset Liability Cd',
	Balance_Sheet_Cd     VARCHAR(50) NULL 
		TITLE 'Balance Sheet Cd',
	Statement_Cycle_Cd   VARCHAR(50) NULL 
		TITLE 'Statement Cycle Cd',
	Statement_Mail_Type_Cd VARCHAR(50) NULL 
		TITLE 'Statement Mail Type Cd',
	Agreement_Source_Cd  VARCHAR(50) NULL 
		TITLE 'Agreement Source Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### AGREEMENT_SUBTYPE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_SUBTYPE
(

	Agreement_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Subtype Cd',
	Agreement_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_SUBTYPE
	 (
			Agreement_Subtype_Cd
	 );
```

#### AGREEMENT_FORMAT_TYPE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_FORMAT_TYPE
(

	Agreement_Format_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Format Type Cd',
	Agreement_Format_Type_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Format Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_FORMAT_TYPE
	 (
			Agreement_Format_Type_Cd
	 );
```

#### AGREEMENT_OBJECTIVE_TYPE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_OBJECTIVE_TYPE
(

	Agreement_Objective_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Objective Type Cd',
	Agreement_Objective_Type_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Objective Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_OBJECTIVE_TYPE
	 (
			Agreement_Objective_Type_Cd
	 );
```

#### AGREEMENT_OBTAINED_TYPE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_OBTAINED_TYPE
(

	Agreement_Obtained_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Obtained Cd',
	Agreement_Obtained_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Obtained Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_OBTAINED_TYPE
	 (
			Agreement_Obtained_Cd
	 );
```

#### AGREEMENT_TYPE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_TYPE
(

	Agreement_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Agreement Type Cd',
	Agreement_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Agreement Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_TYPE
	 (
			Agreement_Type_Cd
	 );
```

#### ASSET_LIABILITY_TYPE

```sql
CREATE  TABLE CORE_DB.ASSET_LIABILITY_TYPE
(

	Asset_Liability_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Asset Liability Cd',
	Asset_Liability_Desc VARCHAR(250) NULL 
		TITLE 'Asset Liability Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_ASSET_LIABILITY_TYPE
	 (
			Asset_Liability_Cd
	 );
```

#### BALANCE_SHEET_TYPE

```sql
CREATE  TABLE CORE_DB.BALANCE_SHEET_TYPE
(

	Balance_Sheet_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Balance Sheet Cd',
	Balance_Sheet_Desc   VARCHAR(250) NULL 
		TITLE 'Balance Sheet Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_BALANCE_SHEET_TYPE
	 (
			Balance_Sheet_Cd
	 );
```

#### DOCUMENT_PRODUCTION_CYCLE_TYPE

```sql
CREATE  TABLE CORE_DB.DOCUMENT_PRODUCTION_CYCLE_TYPE
(

	Document_Production_Cycle_Cd VARCHAR(50) NOT NULL 
		TITLE 'Document Production Cycle Cd',
	Time_Period_Cd       VARCHAR(50) NULL 
		TITLE 'Time Period Cd',
	Document_Cycle_Desc  VARCHAR(250) NULL 
		TITLE 'Document Cycle Desc',
	Document_Cycle_Frequency_Num VARCHAR(50) NULL 
		TITLE 'Billing Cycle Frequency Num',
	Document_Cycle_Frequency_Day_Num VARCHAR(50) NULL 
		TITLE 'Billing Cycle Frequency Day Num',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_DOCUMENT_PRODUCTION_CYCLE_TYPE
	 (
			Document_Production_Cycle_Cd
	 );
```

#### STATEMENT_MAIL_TYPE

```sql
CREATE  TABLE CORE_DB.STATEMENT_MAIL_TYPE
(

	Statement_Mail_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Statement Mail Type Cd',
	Statement_Mail_Type_Desc VARCHAR(250) NULL 
		TITLE 'Statement Mail Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_STATEMENT_MAIL_TYPE
	 (
			Statement_Mail_Type_Cd
	 );
```

#### DATA_SOURCE_TYPE

```sql
CREATE  TABLE CORE_DB.DATA_SOURCE_TYPE
(

	Data_Source_Type_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Data Source Type Cd',
	Data_Source_Type_Desc VARCHAR(250) NULL 
		TITLE 'Data Source Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_DATA_SOURCE_TYPE
	 (
			Data_Source_Type_Cd
	 );
```

#### AGREEMENT_CURRENCY

```sql
CREATE  TABLE CORE_DB.AGREEMENT_CURRENCY
(

	Currency_Use_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Currency Use Cd',
	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Agreement_Currency_Start_Dt DATE NOT NULL 
		TITLE 'Agreement Currency Start Dt',
	Agreement_Currency_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Currency Cd',
	Agreement_Currency_End_Dt DATE NULL 
		TITLE 'Agreement Currency End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_AGREEMENT_CURRENCY
	 (
			Agreement_Id
	 );
```

#### CURRENCY

```sql
CREATE  TABLE CORE_DB.CURRENCY
(

	Currency_Cd          VARCHAR(50) NOT NULL 
		TITLE 'Currency Cd',
	Currency_Name        VARCHAR(100) NOT NULL 
		TITLE 'Currency Name',
	Exchange_Rate_Unit_Cnt INTEGER NULL 
		TITLE 'Exchange Rate Unit Cnt',
	Currency_Rounding_Decimal_Cnt INTEGER NULL 
		TITLE 'Currency Rounding Decimal Cnt',
	ISO_4217_Currency_Alpha_3_Cd CHAR(3) NOT NULL 
		TITLE 'ISO 4217 Currency Alpha-3 Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CURRENCY
	 (
			Currency_Cd
	 );
```

#### AGREEMENT_SCORE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_SCORE
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Model_Id             INTEGER NOT NULL 
		TITLE 'Model Id',
	Model_Run_Id         INTEGER NOT NULL 
		TITLE 'Model Run Id',
	Agreement_Score_Val  VARCHAR(100) NOT NULL 
		TITLE 'Agreement Score Val',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_AGREEMENT_SCORE
	 (
			Agreement_Id
	 );
```

#### PARTY_AGREEMENT

```sql
CREATE  TABLE CORE_DB.PARTY_AGREEMENT
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Party_Agreement_Role_Cd VARCHAR(50) NOT NULL 
		TITLE 'Party Agreement Role Cd',
	Party_Agreement_Start_Dt DATE NOT NULL 
		TITLE 'Party Agreement Start Dt',
	Party_Agreement_End_Dt DATE NULL 
		TITLE 'Party Agreement End Dt',
	Allocation_Pct       DECIMAL(9,4) NULL 
		TITLE 'Allocation Pct',
	Party_Agreement_Amt  DECIMAL(18,4) NULL 
		TITLE 'Party Agreement Amt',
	Party_Agreement_Currency_Amt DECIMAL(18,4) NULL 
		TITLE 'Party Agreement Currency Amt',
	Party_Agreement_Num  VARCHAR(50) NULL 
		TITLE 'Party Agreement Num',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### AGREEMENT_PRODUCT

```sql
CREATE  TABLE CORE_DB.AGREEMENT_PRODUCT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Product_Id           INTEGER NOT NULL 
		TITLE 'Product Id',
	Agreement_Product_Role_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Product Role Cd-new',
	Agreement_Product_Start_Dt DATE NOT NULL 
		TITLE 'Agreement Product Start Dt',
	Agreement_Product_End_Dt DATE NULL 
		TITLE 'Agreement Product End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_AGREEMENT_PRODUCT
	 (
			Agreement_Id
	 );
```

#### PRODUCT_FEATURE

```sql
CREATE  TABLE CORE_DB.PRODUCT_FEATURE
(

	Product_Id           INTEGER NOT NULL 
		TITLE 'Product Id',
	Feature_Id           INTEGER NOT NULL 
		TITLE 'Feature Id',
	Product_Feature_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Product Feature Type Cd',
	Product_Feature_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Product Feature Start Dttm',
	Product_Feature_End_Dttm TIMESTAMP NULL 
		TITLE 'Product Feature End Dttm',
	Product_Feature_Amt  DECIMAL(18,4) NULL 
		TITLE 'Product Feature Amt',
	Product_Feature_Rate DECIMAL(15,12) NULL 
		TITLE 'Product Feature Rate',
	Product_Feature_Qty  DECIMAL(18,4) NULL 
		TITLE 'Product Feature Qty',
	Product_Feature_Num  VARCHAR(50) NULL 
		TITLE 'Product Feature Num',
	Currency_Cd          VARCHAR(50) NULL 
		TITLE 'Currency Cd',
	Unit_Of_Measure_Cd   VARCHAR(50) NULL 
		TITLE 'Unit Of Measure Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PRODUCT_FEATURE
	 (
			Product_Id
	 );
```

#### EVENT_PARTY

```sql
CREATE  TABLE CORE_DB.EVENT_PARTY
(

	Event_Id             INTEGER NOT NULL 
		TITLE 'Event Id',
	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Event_Party_Role_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Event Party Role Cd',
	Event_Party_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Event Party Start Dttm',
	Event_Party_End_Dttm TIMESTAMP NULL 
		TITLE 'Event Party End Dttm',
	Party_Identification_Type_Cd VARCHAR(50) NULL 
		TITLE 'Party Identification Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_EVENT_PARTY
	 (
			Event_Id
	 );
```

#### EVENT

```sql
CREATE  TABLE CORE_DB.EVENT
(

	Event_Id             INTEGER NOT NULL 
		TITLE 'Event Id',
	Event_Desc           VARCHAR(250) NULL 
		TITLE 'Event Desc',
	Event_Start_Dttm     TIMESTAMP NULL 
		TITLE 'Event Start Dttm',
	Event_End_Dttm       TIMESTAMP NULL 
		TITLE 'Event End Dttm',
	Event_GMT_Start_Dttm TIMESTAMP NULL 
		TITLE 'Event GMT Start Dttm',
	Event_Activity_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Event Activity Type Cd',
	Event_Reason_Cd      VARCHAR(50) NULL 
		TITLE 'Event Reason Cd',
	Event_Subtype_Cd     VARCHAR(50) NULL 
		TITLE 'Event Subtype Cd',
	Initiation_Type_Cd   VARCHAR(50) NULL 
		TITLE 'Initiation Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_EVENT
	 (
			Event_Id
	 );
```

#### FINANCIAL_EVENT

```sql
CREATE  TABLE CORE_DB.FINANCIAL_EVENT
(

	Event_Id             INTEGER NOT NULL 
		TITLE 'Event Id',
	Financial_Event_Period_Start_Dt DATE NULL 
		TITLE 'Financial Event Period Start Dt',
	Financial_Event_Period_End_Dt DATE NULL 
		TITLE 'Financial Event Period End Dt',
	Financial_Event_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Financial Event Type Cd',
	Document_Production_Cycle_Cd VARCHAR(50) NULL 
		TITLE 'Document Production Cycle Cd',
	Event_Medium_Type_Cd VARCHAR(50) NULL 
		TITLE 'Event Medium Type Cd',
	Debit_Credit_Cd      VARCHAR(50) NULL 
		TITLE 'Debit Credit Cd',
	In_Out_Direction_Type_Cd VARCHAR(50) NULL 
		TITLE 'In Out Direction Type Cd',
	Financial_Event_Bill_Cnt INTEGER NULL 
		TITLE 'Financial Event Bill Cnt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_FINANCIAL_EVENT
	 (
			Event_Id
	 );
```

#### PARTY_STATUS

```sql
CREATE TABLE Core_DB.PARTY_STATUS
(
	Party_Id             BIGINT NOT NULL
		TITLE 'Party Id',
	Party_Status_Cd      VARCHAR(50) NOT NULL
		TITLE 'Party Status Cd',
	Party_Status_Dt      DATE NOT NULL
		TITLE 'Party Status Dt',
	di_start_ts          TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_STATUS
	 (
			Party_Id
	 );
```

#### PARTY_SEGMENT (Core_DB)

```sql
CREATE TABLE Core_DB.PARTY_SEGMENT
(
	Party_Id                  BIGINT NOT NULL
		TITLE 'Party Id',
	Market_Segment_Id         INTEGER NOT NULL
		TITLE 'Market Segment Id',
	Party_Segment_Start_Dttm  TIMESTAMP NULL
		TITLE 'Party Segment Start Dttm',
	Party_Segment_End_Dttm    TIMESTAMP NULL
		TITLE 'Party Segment End Dttm',
	di_start_ts               TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_end_ts                 TIMESTAMP(6) NULL
		TITLE 'DI End Ts',
	di_rec_deleted_Ind        CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_SEGMENT
	 (
			Party_Id
	 );
```

#### PRODUCT_COST

```sql
CREATE TABLE Core_DB.PRODUCT_COST
(
	Product_Id               BIGINT NOT NULL
		TITLE 'Product Id',
	Cost_Cd                  VARCHAR(50) NOT NULL
		TITLE 'Cost Cd',
	Product_Cost_Amt         DECIMAL(18,4) NULL
		TITLE 'Product Cost Amt',
	Product_Cost_Start_Dttm  TIMESTAMP NOT NULL
		TITLE 'Product Cost Start Dttm',
	Product_Cost_End_Dttm    TIMESTAMP NULL
		TITLE 'Product Cost End Dttm',
	di_start_ts              TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_end_ts                TIMESTAMP(6) NULL
		TITLE 'DI End Ts',
	di_rec_deleted_Ind       CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PRODUCT_COST
	 (
			Product_Id
	 );
```

#### PRODUCT_GROUP (Core_DB)

```sql
CREATE TABLE Core_DB.PRODUCT_GROUP
(
	Product_Group_Id         INTEGER NOT NULL
		TITLE 'Product Group Id',
	Parent_Group_Id          INTEGER NOT NULL
		TITLE 'Parent Group Id',
	Product_Group_Type_Cd    VARCHAR(50) NOT NULL
		TITLE 'Product Group Type Cd',
	Product_Group_Name       VARCHAR(255) NULL
		TITLE 'Product Group Name',
	Product_Group_Desc       VARCHAR(1000) NULL
		TITLE 'Product Group Desc',
	di_start_ts              TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_end_ts                TIMESTAMP(6) NULL
		TITLE 'DI End Ts',
	di_rec_deleted_Ind       CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PRODUCT_GROUP
	 (
			Product_Group_Id
	 );
```

#### EVENT_CHANNEL_INSTANCE

```sql
CREATE TABLE Core_DB.EVENT_CHANNEL_INSTANCE
(
	Event_Id                  BIGINT NOT NULL
		TITLE 'Event Id',
	Channel_Instance_Id       INTEGER NOT NULL
		TITLE 'Channel Instance Id',
	Event_Channel_Start_Dttm  TIMESTAMP NULL
		TITLE 'Event Channel Start Dttm',
	Event_Channel_End_Dttm    TIMESTAMP NULL
		TITLE 'Event Channel End Dttm',
	di_start_ts               TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_end_ts                 TIMESTAMP(6) NULL
		TITLE 'DI End Ts',
	di_rec_deleted_Ind        CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_EVENT_CHANNEL_INSTANCE
	 (
			Event_Id
	 );
```

#### FINANCIAL_EVENT_AMOUNT

```sql
CREATE TABLE Core_DB.FINANCIAL_EVENT_AMOUNT
(
	Event_Id                     BIGINT NOT NULL
		TITLE 'Event Id',
	Financial_Event_Amount_Cd    VARCHAR(50) NOT NULL
		TITLE 'Financial Event Amount Cd',
	Event_Transaction_Amt        DECIMAL(18,4) NULL
		TITLE 'Event Transaction Amt',
	Financial_Event_Type_Cd      VARCHAR(50) NOT NULL
		TITLE 'Financial Event Type Cd',
	In_Out_Direction_Type_Cd     VARCHAR(50) NOT NULL
		TITLE 'In Out Direction Type Cd',
	di_start_ts                  TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_end_ts                    TIMESTAMP(6) NULL
		TITLE 'DI End Ts',
	di_rec_deleted_Ind           CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_FINANCIAL_EVENT_AMOUNT
	 (
			Event_Id
	 );
```

#### FUNDS_TRANSFER_EVENT

```sql
CREATE TABLE Core_DB.FUNDS_TRANSFER_EVENT
(
	Event_Id                         BIGINT NOT NULL
		TITLE 'Event Id',
	Funds_Transfer_Method_Type_Cd    VARCHAR(50) NOT NULL
		TITLE 'Funds Transfer Method Type Cd',
	Originating_Agreement_Id         BIGINT NOT NULL
		TITLE 'Originating Agreement Id',
	Originating_Account_Num          VARCHAR(50) NULL
		TITLE 'Originating Account Num',
	Destination_Agreement_Id         BIGINT NULL
		TITLE 'Destination Agreement Id',
	Destination_Account_Num          VARCHAR(50) NULL
		TITLE 'Destination Account Num',
	di_start_ts                      TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_end_ts                        TIMESTAMP(6) NULL
		TITLE 'DI End Ts',
	di_rec_deleted_Ind               CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_FUNDS_TRANSFER_EVENT
	 (
			Event_Id
	 );
```

#### ACCESS_DEVICE_EVENT

```sql
CREATE TABLE Core_DB.ACCESS_DEVICE_EVENT
(
	Event_Id                         BIGINT NOT NULL
		TITLE 'Event Id',
	Channel_Type_Cd                  VARCHAR(50) NOT NULL
		TITLE 'Channel Type Cd',
	Funds_Transfer_Method_Type_Cd    VARCHAR(50) NULL
		TITLE 'Funds Transfer Method Type Cd',
	Access_Device_Id                 BIGINT NULL
		TITLE 'Access Device Id',
	di_start_ts                      TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_end_ts                        TIMESTAMP(6) NULL
		TITLE 'DI End Ts',
	di_rec_deleted_Ind               CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ACCESS_DEVICE_EVENT
	 (
			Event_Id
	 );
```

#### DIRECT_CONTACT_EVENT

```sql
CREATE TABLE Core_DB.DIRECT_CONTACT_EVENT
(
	Event_Id                  BIGINT NOT NULL
		TITLE 'Event Id',
	Contact_Event_Subtype_Cd  VARCHAR(50) NOT NULL
		TITLE 'Contact Event Subtype Cd',
	Customer_Tone_Cd          VARCHAR(50) NULL
		TITLE 'Customer Tone Cd',
	di_start_ts               TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_end_ts                 TIMESTAMP(6) NULL
		TITLE 'DI End Ts',
	di_rec_deleted_Ind        CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_DIRECT_CONTACT_EVENT
	 (
			Event_Id
	 );
```

#### CHANNEL_INSTANCE

```sql
CREATE  TABLE CORE_DB.CHANNEL_INSTANCE
(

	Channel_Instance_Id  INTEGER NOT NULL 
		TITLE 'Channel Instance Id',
	Channel_Type_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Channel Type Cd',
	Channel_Instance_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Alternate Channel Type Cd',
	Channel_Instance_Name VARCHAR(100) NULL 
		TITLE 'Channel Instance Name',
	Channel_Instance_Start_Dt DATE NULL 
		TITLE 'Channel Instance Start Dt',
	Channel_Instance_End_Dt DATE NULL 
		TITLE 'Channel Instance End Dt',
	Convenience_Factor_Cd VARCHAR(50) NOT NULL 
		TITLE 'Convenience Factor Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CHANNEL_INSTANCE
	 (
			Channel_Instance_Id
	 );
```

#### COMPLAINT_EVENT

```sql
CREATE MULTISET TABLE CORE_DB.COMPLAINT_EVENT
(
    Event_Id BIGINT NOT NULL,
    Event_Sentiment_Cd SMALLINT NOT NULL,
    Event_Channel_Type_Cd SMALLINT NOT NULL,
    Event_Received_Dttm TIMESTAMP(0) NOT NULL,
    Event_Txt VARCHAR(32000),
    Event_Multimedia_Object_Ind CHAR(1) NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Event_Id);
```

#### AGREEMENT_METRIC

```sql
CREATE  TABLE CORE_DB.AGREEMENT_METRIC
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Agreement_Metric_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Risk Metric Type Cd',
	Agreement_Metric_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Agreement Metric Start Dttm',
	Agreement_Metric_End_Dttm TIMESTAMP NULL 
		TITLE 'Agreement Metric End Dttm',
	Agreement_Metric_Time_Period_Cd VARCHAR(50) NULL 
		TITLE 'Agreement Metric Time Period Cd',
	Agreement_Metric_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Metric Amt',
	Agreement_Metric_Cnt INTEGER NULL 
		TITLE 'Agreement Metric Cnt',
	Agreement_Metric_Rate DECIMAL(15,12) NULL 
		TITLE 'Agreement Metric Rate',
	Agreement_Metric_Qty DECIMAL(18,4) NULL 
		TITLE 'Agreement Metric Qty',
	Agreement_Currency_Metric_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Metric Amt',
	Currency_Cd          VARCHAR(50) NULL 
		TITLE 'Currency Cd',
	Unit_Of_Measure_Cd   VARCHAR(50) NULL 
		TITLE 'Unit Of Measure Cd',
	GL_Main_Account_Segment_Id INTEGER NULL 
		TITLE 'GL Main Account Segment Id',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_AGREEMENT_METRIC
	 (
			Agreement_Id
	 );
```

#### PRODUCT

```sql
CREATE  TABLE CORE_DB.PRODUCT
(

	Product_Id           INTEGER NOT NULL 
		TITLE 'Product Id',
	Product_Script_Id    INTEGER NULL 
		TITLE 'Product Script Id',
	Product_Subtype_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Product Subtype Cd',
	Product_Desc         VARCHAR(250) NULL 
		TITLE 'Product Desc',
	Product_Name         VARCHAR(100) NULL 
		TITLE 'Product Name',
	Host_Product_Num     VARCHAR(50) NOT NULL 
		TITLE 'Host Product Num',
	Product_Start_Dt     DATE NULL 
		TITLE 'Product Start Dt',
	Product_End_Dt       DATE NULL 
		TITLE 'Product End Dt',
	Product_Package_Type_Cd VARCHAR(50) NULL 
		TITLE 'Product Package Type Cd',
	Financial_Product_Ind CHAR(3) NULL 
		TITLE 'Financial Product Ind',
	Product_Txt          VARCHAR(1000) NULL 
		TITLE 'Product Txt',
	Product_Creation_Dt  DATE NULL 
		TITLE 'Product Creation Dt',
	Service_Ind          CHAR(3) NULL 
		TITLE 'Service Ind',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PRODUCT
	 (
			Product_Id
	 );
```

#### AGREEMENT_STATUS

```sql
CREATE  TABLE CORE_DB.AGREEMENT_STATUS
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Agreement_Status_Scheme_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Scheme Cd',
	Agreement_Status_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Agreement Status Start Dttm',
	Agreement_Status_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Cd',
	Agreement_Status_Reason_Cd VARCHAR(50) NULL 
		TITLE 'Agreement Status Reason Cd',
	Agreement_Status_End_Dttm TIMESTAMP NULL 
		TITLE 'Agreement Status End Dttm',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_AGREEMENT_STATUS
	 (
			Agreement_Id
	 );
```

#### AGREEMENT_STATUS_TYPE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_STATUS_TYPE
(

	Agreement_Status_Scheme_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Scheme Cd',
	Agreement_Status_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Cd',
	Agreement_Status_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Status Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_AGREEMENT_STATUS_TYPE
	 (
			Agreement_Status_Scheme_Cd
	 );
```

#### AGREEMENT_STATUS_REASON_TYPE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_STATUS_REASON_TYPE
(

	Agreement_Status_Reason_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Reason Cd',
	Agreement_Status_Reason_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Status Reason Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_STATUS_REASON_TYPE
	 (
			Agreement_Status_Reason_Cd
	 );
```

#### AGREEMENT_STATUS_SCHEME_TYPE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_STATUS_SCHEME_TYPE
(

	Agreement_Status_Scheme_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Scheme Cd',
	Agreement_Status_Scheme_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Status Scheme Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_STATUS_SCHEME_TYPE
	 (
			Agreement_Status_Scheme_Cd
	 );
```

#### ADDRESS

```sql
CREATE  TABLE CORE_DB.ADDRESS
(

	Address_Id           INTEGER NOT NULL 
		TITLE 'Address Id',
	Address_Subtype_Cd   VARCHAR(50) NULL 
		TITLE 'Locator Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ADDRESS
	 (
			Address_Id
	 );
```

#### ADDRESS_SUBTYPE

```sql
CREATE  TABLE CORE_DB.ADDRESS_SUBTYPE
(

	Address_Subtype_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Locator Type Cd',
	Address_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Locator Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_ADDRESS_SUBTYPE
	 (
			Address_Subtype_Cd
	 );
```

#### CAMPAIGN

```sql
CREATE  TABLE CORE_DB.CAMPAIGN
(

	Campaign_Id          INTEGER NOT NULL 
		TITLE 'Campaign Id',
	Campaign_Strategy_Cd VARCHAR(50) NULL 
		TITLE 'Campaign Strategy Cd',
	Campaign_Type_Cd     VARCHAR(50) NULL 
		TITLE 'Campaign Type Cd',
	Campaign_Classification_Cd VARCHAR(50) NULL 
		TITLE 'Campaign Classification Cd',
	Parent_Campaign_Id   INTEGER NULL 
		TITLE 'Parent Campaign Id',
	Campaign_Level_Num   VARCHAR(50) NULL 
		TITLE 'Campaign Level Num',
	Funding_GL_Main_Account_Id INTEGER NULL 
		TITLE 'Funding GL Main Account Id',
	Campaign_Desc        VARCHAR(250) NULL 
		TITLE 'Campaign Desc',
	Campaign_Start_Dt    DATE NULL 
		TITLE 'Campaign Start Dt',
	Campaign_End_Dt      DATE NULL 
		TITLE 'Campaign End Dt',
	Campaign_Name        VARCHAR(100) NULL 
		TITLE 'Campaign Name',
	Campaign_Estimated_Cost_Amt DECIMAL(18,4) NULL 
		TITLE 'Campaign Estimated Cost Amt',
	Currency_Cd          VARCHAR(50) NULL 
		TITLE 'Currency Cd',
	Campaign_Estimated_Revenue_Gain_Amt DECIMAL(18,4) NULL 
		TITLE 'Campaign Estimated Revenue Gain Amt',
	Campaign_Estimated_Base_Customer_Cnt INTEGER NULL 
		TITLE 'Campaign Estimated Base Customer Cnt',
	Campaign_Estimated_Customer_Cnt INTEGER NULL 
		TITLE 'Campaign Estimated Customer Cnt',
	Campaign_Estimated_Positive_Cnt INTEGER NULL 
		TITLE 'Campaign Estimated Positive Cnt',
	Campaign_Estimated_Contact_Cnt INTEGER NULL 
		TITLE 'Campaign Estimated Contact Cnt',
	Campaign_Creation_Dt DATE NULL 
		TITLE 'Campaign Creation Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CAMPAIGN
	 (
			Campaign_Id
	 );
```

#### CAMPAIGN_STRATEGY_TYPE

```sql
CREATE  TABLE CORE_DB.CAMPAIGN_STRATEGY_TYPE
(

	Campaign_Strategy_Cd VARCHAR(50) NOT NULL 
		TITLE 'Campaign Strategy Cd',
	Campaign_Strategy_Desc VARCHAR(250) NULL 
		TITLE 'Campaign Strategy Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CAMPAIGN_STRATEGY_TYPE
	 (
			Campaign_Strategy_Cd
	 );
```

#### CAMPAIGN_TYPE

```sql
CREATE  TABLE CORE_DB.CAMPAIGN_TYPE
(

	Campaign_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Campaign Type Cd',
	Campaign_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Campaign Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CAMPAIGN_TYPE
	 (
			Campaign_Type_Cd
	 );
```

#### CAMPAIGN_CLASSIFICATION

```sql
CREATE  TABLE CORE_DB.CAMPAIGN_CLASSIFICATION
(

	Campaign_Classification_Cd VARCHAR(50) NOT NULL 
		TITLE 'Campaign Classification Cd',
	Campaign_Classification_Desc VARCHAR(250) NULL 
		TITLE 'Campaign Classification Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CAMPAIGN_CLASSIFICATION
	 (
			Campaign_Classification_Cd
	 );
```

#### CAMPAIGN_STATUS

```sql
CREATE  TABLE CORE_DB.CAMPAIGN_STATUS
(

	Campaign_Id          INTEGER NOT NULL 
		TITLE 'Campaign Id',
	Campaign_Status_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Campaign Status Start Dttm',
	Campaign_Status_Cd   VARCHAR(50) NULL 
		TITLE 'Campaign Status Cd',
	Campaign_Status_End_Dttm TIMESTAMP NULL 
		TITLE 'Campaign Status End Dttm',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CAMPAIGN_STATUS
	 (
			Campaign_Id
	 );
```

#### CAMPAIGN_STATUS_TYPE

```sql
CREATE  TABLE CORE_DB.CAMPAIGN_STATUS_TYPE
(

	Campaign_Status_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Campaign Status Cd',
	Campaign_Status_Desc VARCHAR(250) NULL 
		TITLE 'Campaign Status Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CAMPAIGN_STATUS_TYPE
	 (
			Campaign_Status_Cd
	 );
```

#### CHANNEL_TYPE

```sql
CREATE  TABLE CORE_DB.CHANNEL_TYPE
(

	Channel_Type_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Channel Type Cd',
	Channel_Processing_Cd VARCHAR(50) NULL 
		TITLE 'Channel Processing Cd',
	Channel_Type_Name    VARCHAR(100) NULL 
		TITLE 'Channel Type Name',
	Channel_Type_Desc    VARCHAR(250) NULL 
		TITLE 'Channel Type Desc',
	Channel_Type_Start_Dt DATE NULL 
		TITLE 'Channel Type Start Dt',
	Channel_Type_End_Dt  DATE NULL 
		TITLE 'Channel Type End Dt',
	Parent_Channel_Type_Cd VARCHAR(50) NULL 
		TITLE 'Parent Channel Type Cd',
	Channel_Type_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Channel Type Subtype Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CHANNEL_TYPE
	 (
			Channel_Type_Cd
	 );
```

#### CHANNEL_INSTANCE_SUBTYPE

```sql
CREATE  TABLE CORE_DB.CHANNEL_INSTANCE_SUBTYPE
(

	Channel_Instance_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Alternate Channel Type Cd',
	Channel_Instance_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Alternate Channel Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CHANNEL_INSTANCE_SUBTYPE
	 (
			Channel_Instance_Subtype_Cd
	 );
```

#### CONVENIENCE_FACTOR_TYPE

```sql
CREATE  TABLE CORE_DB.CONVENIENCE_FACTOR_TYPE
(

	Convenience_Factor_Cd VARCHAR(50) NOT NULL 
		TITLE 'Convenience Factor Cd',
	Convenience_Factor_Desc VARCHAR(250) NULL 
		TITLE 'Convenience Factor Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CONVENIENCE_FACTOR_TYPE
	 (
			Convenience_Factor_Cd
	 );
```

#### CHANNEL_INSTANCE_STATUS

```sql
CREATE  TABLE CORE_DB.CHANNEL_INSTANCE_STATUS
(

	Channel_Instance_Id  INTEGER NOT NULL 
		TITLE 'Channel Instance Id',
	Channel_Instance_Status_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Channel Instance Status Start Dttm',
	Channel_Status_Cd    VARCHAR(50) NULL 
		TITLE 'Channel Status Cd',
	Channel_Instance_Status_End_Dttm TIMESTAMP NULL 
		TITLE 'Channel Instance Status End Dttm',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CHANNEL_INSTANCE_STATUS
	 (
			Channel_Instance_Id
	 );
```

#### CHANNEL_STATUS_TYPE

```sql
CREATE  TABLE CORE_DB.CHANNEL_STATUS_TYPE
(

	Channel_Status_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Channel Status Cd',
	Channel_Status_Desc  VARCHAR(250) NULL 
		TITLE 'Channel Status Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CHANNEL_STATUS_TYPE
	 (
			Channel_Status_Cd
	 );
```

#### CARD

```sql
CREATE  TABLE CORE_DB.CARD
(

	Access_Device_Id     INTEGER NOT NULL 
		TITLE 'Access Device Id',
	Card_Subtype_Cd      VARCHAR(50) NULL 
		TITLE 'Card Subtype Cd',
	Card_Association_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Card Association Type Cd',
	Technology_Type_Cd   VARCHAR(50) NULL 
		TITLE 'Technology Type Cd',
	Card_Num             VARCHAR(50) NULL 
		TITLE 'Card Num',
	Card_Sequence_Num    VARCHAR(50) NULL 
		TITLE 'Card Sequence Num',
	Card_Expiration_Dt   DATE NULL 
		TITLE 'Card Expiration Dt',
	Card_Issue_Dt        DATE NULL 
		TITLE 'Card Issue Dt',
	Card_Activation_Dt   DATE NULL 
		TITLE 'Card Activation Dt',
	Card_Deactivation_Dt DATE NULL 
		TITLE 'Card Deactivation Dt',
	Card_Name            VARCHAR(100) NULL 
		TITLE 'Card Name',
	Card_Encrypted_Num   VARCHAR(50) NULL 
		TITLE 'Card Encrypted Num',
	Card_Manufacture_Dt  DATE NULL 
		TITLE 'Card Manufacture Dt',
	Card_Replacement_Order_Dt DATE NULL 
		TITLE 'Card Replacement Order Dt',
	Language_Type_Cd     VARCHAR(50) NULL 
		TITLE 'Language Type Cd',
	Bank_Identification_Num VARCHAR(6) NULL 
		TITLE 'Bank Identification Num',
	Card_Security_Code_Num VARCHAR(50) NULL 
		TITLE 'Card Security Code Num',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CARD
	 (
			Access_Device_Id
	 );
```

#### AGREEMENT_FEATURE_ROLE_TYPE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_FEATURE_ROLE_TYPE
(

	Agreement_Feature_Role_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Feature Role Cd',
	Agreement_Feature_Role_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Feature Role Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_FEATURE_ROLE_TYPE
	 (
			Agreement_Feature_Role_Cd
	 );
```

#### AGREEMENT_RATE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_RATE
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Rate_Type_Cd         VARCHAR(50) NOT NULL 
		TITLE 'Rate Type Cd',
	Balance_Category_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Balance Category Type Cd',
	Agreement_Rate_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Agreement Rate Start Dttm',
	Agreement_Rate_End_Dttm TIMESTAMP NULL 
		TITLE 'Agreement Rate End Dttm',
	Agreement_Rate_Time_Period_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Rate Time Period Cd',
	Agreement_Rate       DECIMAL(15,12) NULL 
		TITLE 'Agreement Rate',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_AGREEMENT_RATE
	 (
			Agreement_Id
	 );
```

#### FINANCIAL_AGREEMENT

```sql
CREATE  TABLE CORE_DB.FINANCIAL_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Financial_Agreement_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Financial Agreement Subtype Cd',
	Market_Risk_Type_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Market Risk Type Cd',
	Original_Maturity_Dt DATE NULL 
		TITLE 'Original Maturity Dt',
	Risk_Exposure_Mitigant_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Risk Exposure Mitigant Subtype Cd',
	Trading_Book_Cd      VARCHAR(50) NULL 
		TITLE 'Trading Book Cd',
	Pricing_Method_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Pricing Method Subtype Cd',
	Financial_Agreement_Type_Cd VARCHAR(50) NULL 
		TITLE 'Financial Agreement Type Cd-7-1',
	Day_Count_Basis_Cd   VARCHAR(50) NULL 
		TITLE 'Day Count Basis Cd',
	ISO_8583_Account_Type_Cd VARCHAR(50) NULL 
		TITLE 'ISO 8583 Account Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_FINANCIAL_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### MARKET_RISK_TYPE

```sql
CREATE  TABLE CORE_DB.MARKET_RISK_TYPE
(

	Market_Risk_Type_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Market Risk Type Cd',
	Market_Risk_Type_Desc VARCHAR(250) NULL 
		TITLE 'Market Risk Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_MARKET_RISK_TYPE
	 (
			Market_Risk_Type_Cd
	 );
```

#### TRADING_BOOK_TYPE

```sql
CREATE  TABLE CORE_DB.TRADING_BOOK_TYPE
(

	Trading_Book_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Trading Book Cd',
	Trading_Book_Desc    VARCHAR(250) NULL 
		TITLE 'Trading Book Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_TRADING_BOOK_TYPE
	 (
			Trading_Book_Cd
	 );
```

#### DAY_COUNT_BASIS_TYPE

```sql
CREATE  TABLE CORE_DB.DAY_COUNT_BASIS_TYPE
(

	Day_Count_Basis_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Day Count Basis Cd',
	Day_Count_Basis_Desc VARCHAR(250) NULL 
		TITLE 'Day Count Basis Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_DAY_COUNT_BASIS_TYPE
	 (
			Day_Count_Basis_Cd
	 );
```

#### DEPOSIT_AGREEMENT

```sql
CREATE  TABLE CORE_DB.DEPOSIT_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Deposit_Maturity_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Deposit Maturity Subtype Cd',
	Interest_Disbursement_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Interest Disbursement Type Cd',
	Deposit_Ownership_Type_Cd VARCHAR(50) NULL 
		TITLE 'Deposit Ownership Type Cd',
	Original_Deposit_Amt DECIMAL(18,4) NULL 
		TITLE 'Original Deposit Amt',
	Original_Deposit_Dt  DATE NULL 
		TITLE 'Original Deposit Dt',
	Agreement_Currency_Original_Deposit_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Original Deposit Amt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_DEPOSIT_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### DEPOSIT_MATURITY_SUBTYPE

```sql
CREATE  TABLE CORE_DB.DEPOSIT_MATURITY_SUBTYPE
(

	Deposit_Maturity_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Deposit Maturity Subtype Cd',
	Deposit_Maturity_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Deposit Maturity Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_DEPOSIT_MATURITY_SUBTYPE
	 (
			Deposit_Maturity_Subtype_Cd
	 );
```

#### INTEREST_DISBURSEMENT_TYPE

```sql
CREATE  TABLE CORE_DB.INTEREST_DISBURSEMENT_TYPE
(

	Interest_Disbursement_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Interest Disbursement Type Cd',
	Interest_Disbursement_Type_Desc VARCHAR(250) NULL 
		TITLE 'Interest Disbursement Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_INTEREST_DISBURSEMENT_TYPE
	 (
			Interest_Disbursement_Type_Cd
	 );
```

#### DEPOSIT_TERM_AGREEMENT

```sql
CREATE  TABLE CORE_DB.DEPOSIT_TERM_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Next_Term_Maturity_Dt DATE NULL 
		TITLE 'Next Term Maturity Dt',
	Grace_Period_End_Dt  DATE NULL 
		TITLE 'Grace Period End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_DEPOSIT_TERM_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### FEATURE

```sql
CREATE  TABLE CORE_DB.FEATURE
(

	Feature_Id           INTEGER NOT NULL 
		TITLE 'Feature Id',
	Feature_Subtype_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Feature Subtype Cd',
	Feature_Insurance_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Feature Insurance Subtype Cd',
	Feature_Classification_Cd VARCHAR(50) NULL 
		TITLE 'Feature Classification Cd',
	Feature_Desc         VARCHAR(250) NULL 
		TITLE 'Feature Desc',
	Feature_Name         VARCHAR(100) NULL 
		TITLE 'Feature Name',
	Common_Feature_Name  VARCHAR(100) NULL 
		TITLE 'Common Feature Name',
	Feature_Level_Subtype_Cnt INTEGER NULL 
		TITLE 'Feature Level Subtype Cnt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_FEATURE
	 (
			Feature_Id
	 );
```

#### FEATURE_SUBTYPE

```sql
CREATE  TABLE CORE_DB.FEATURE_SUBTYPE
(

	Feature_Subtype_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Feature Subtype Cd',
	Feature_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Feature Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_FEATURE_SUBTYPE
	 (
			Feature_Subtype_Cd
	 );
```

#### FEATURE_INSURANCE_SUBTYPE

```sql
CREATE  TABLE CORE_DB.FEATURE_INSURANCE_SUBTYPE
(

	Feature_Insurance_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Feature Insurance Subtype Cd',
	Feature_Insurance_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Feature Insurance Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_FEATURE_INSURANCE_SUBTYPE
	 (
			Feature_Insurance_Subtype_Cd
	 );
```

#### FEATURE_CLASSIFICATION_TYPE

```sql
CREATE  TABLE CORE_DB.FEATURE_CLASSIFICATION_TYPE
(

	Feature_Classification_Cd VARCHAR(50) NOT NULL 
		TITLE 'Feature Classification Cd',
	Feature_Classification_Desc VARCHAR(250) NULL 
		TITLE 'Feature Classification Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_FEATURE_CLASSIFICATION_TYPE
	 (
			Feature_Classification_Cd
	 );
```

#### INDIVIDUAL

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Birth_Dt             DATE NULL 
		TITLE 'Birth Dt',
	Death_Dt             DATE NULL 
		TITLE 'Death Dt',
	Gender_Type_Cd       VARCHAR(50) NULL 
		TITLE 'Gender Type Cd',
	Ethnicity_Type_Cd    VARCHAR(50) NULL 
		TITLE 'Ethnicity Type Cd',
	Tax_Bracket_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Tax Bracket Cd',
	Retirement_Dt        DATE NULL 
		TITLE 'Retirement Dt',
	Employment_Start_Dt  DATE NULL 
		TITLE 'Employment Start Dt',
	Nationality_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Nationality Cd',
	Name_Only_No_Pronoun_Ind CHAR(3) NULL 
		TITLE 'Name Only No Pronoun Ind',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL
	 (
			Individual_Party_Id
	 );
```

#### INDIVIDUAL_NAME

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_NAME
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Name_Type_Cd         VARCHAR(50) NOT NULL 
		TITLE 'Name Type Cd',
	Individual_Name_Start_Dt DATE NOT NULL 
		TITLE 'Individual Name Start Dt',
	Given_Name           VARCHAR(100) NOT NULL 
		TITLE 'Given Name',
	Middle_Name          VARCHAR(100) NOT NULL 
		TITLE 'Middle Name',
	Family_Name          VARCHAR(100) NOT NULL 
		TITLE 'Family Name',
	Birth_Family_Name    VARCHAR(100) NULL 
		TITLE 'Birth Family Name',
	Name_Prefix_Txt      VARCHAR(1000) NULL 
		TITLE 'Name Prefix Txt',
	Name_Suffix_Txt      VARCHAR(1000) NULL 
		TITLE 'Name Suffix Txt',
	Individual_Name_End_Dt DATE NULL 
		TITLE 'Individual Name End Dt',
	Individual_Full_Name VARCHAR(100) NULL 
		TITLE 'Individual Full Name',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_NAME
	 (
			Individual_Party_Id
	 );
```

#### INDIVIDUAL_GENDER_PRONOUN

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_GENDER_PRONOUN
(

	Gender_Pronoun_Start_Dt DATE NOT NULL 
		TITLE 'Gender Pronoun Start Dt',
	Gender_Pronoun_End_Dt DATE NULL 
		TITLE 'Gender Pronoun End Dt',
	Self_reported_Ind    CHAR(3) NULL 
		TITLE 'Self-reported Ind',
	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Gender_Pronoun_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Gender Pronoun Type Cd',
	Gender_Pronoun_Cd    VARCHAR(50) NULL 
		TITLE 'Gender Pronoun Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_GENDER_PRONOUN
	 (
			Individual_Party_Id
	 );
```

#### INDIVIDUAL_MARITAL_STATUS

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_MARITAL_STATUS
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Individual_Marital_Status_Start_Dt DATE NOT NULL 
		TITLE 'Individual Marital Status Start Dt',
	Marital_Status_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Marital Status Cd',
	Individual_Marital_Status_End_Dt DATE NULL 
		TITLE 'Individual Marital Status End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_MARITAL_STATUS
	 (
			Individual_Party_Id
	 );
```

#### ASSOCIATE_EMPLOYMENT

```sql
CREATE  TABLE CORE_DB.ASSOCIATE_EMPLOYMENT
(

	Associate_Party_Id   INTEGER NOT NULL 
		TITLE 'Associate Party Id',
	Organization_Party_Id INTEGER NOT NULL 
		TITLE 'Organization Party Id',
	Associate_Employment_Start_Dt DATE NOT NULL 
		TITLE 'Associate Employment Start Dt',
	Associate_Employment_End_Dt DATE NULL 
		TITLE 'Associate Employment End Dt',
	Associate_Hire_Dt    DATE NULL 
		TITLE 'Associate Hire Dt',
	Associate_Termination_Dttm TIMESTAMP NULL 
		TITLE 'Associate Termination Dttm',
	Associate_HR_Num     VARCHAR(50) NULL 
		TITLE 'Associate HR Num',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ASSOCIATE_EMPLOYMENT
	 (
			Associate_Party_Id
	 );
```

#### INDIVIDUAL_VIP_STATUS

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_VIP_STATUS
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Individual_VIP_Status_Start_Dt DATE NOT NULL 
		TITLE 'Individual VIP Status Start Dt',
	VIP_Type_Cd          VARCHAR(50) NOT NULL 
		TITLE 'VIP Type Cd',
	Individual_VIP_Status_End_Dt DATE NULL 
		TITLE 'Individual VIP Status End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_VIP_STATUS
	 (
			Individual_Party_Id
	 );
```

#### INDIVIDUAL_MILITARY_STATUS

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_MILITARY_STATUS
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Individual_Military_Start_Dt DATE NOT NULL 
		TITLE 'Individual Military Start Dt',
	Military_Status_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Military Status Type Cd',
	Individual_Military_End_Dt DATE NULL 
		TITLE 'Individual Military End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_MILITARY_STATUS
	 (
			Individual_Party_Id
	 );
```

#### INDIVIDUAL_OCCUPATION

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_OCCUPATION
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Occupation_Type_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Occupation Type Cd',
	Individual_Occupation_Start_Dt DATE NOT NULL 
		TITLE 'Individual Occupation Start Dt',
	Individual_Occupation_End_Dt DATE NULL 
		TITLE 'Individual Occupation End Dt',
	Individual_Job_Title_Txt VARCHAR(1000) NULL 
		TITLE 'Individual Job Title Txt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_OCCUPATION
	 (
			Individual_Party_Id
	 );
```

#### INDIVIDUAL_PAY_TIMING

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_PAY_TIMING
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Business_Party_Id    INTEGER NOT NULL 
		TITLE 'Business Party Id',
	Pay_Day_Num          VARCHAR(50) NULL 
		TITLE 'Pay Day Num',
	Time_Period_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Time Period Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_PAY_TIMING
	 (
			Individual_Party_Id
	 );
```

#### INDIVIDUAL_BONUS_TIMING

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_BONUS_TIMING
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Bonus_Month_Num      VARCHAR(50) NOT NULL 
		TITLE 'Bonus Month Num',
	Business_Party_Id    INTEGER NOT NULL 
		TITLE 'Business Party Id',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_BONUS_TIMING
	 (
			Individual_Party_Id
	 );
```

#### INDIVIDUAL_SKILL

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_SKILL
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Skill_Cd             VARCHAR(50) NOT NULL 
		TITLE 'Skill Cd',
	Individual_Skill_Dt  DATE NULL 
		TITLE 'Individual Skill Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_SKILL
	 (
			Individual_Party_Id
	 );
```

#### SKILL_TYPE

```sql
CREATE  TABLE CORE_DB.SKILL_TYPE
(

	Skill_Cd             VARCHAR(50) NOT NULL 
		TITLE 'Skill Cd',
	Skill_Desc           VARCHAR(250) NULL 
		TITLE 'Skill Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_SKILL_TYPE
	 (
			Skill_Cd
	 );
```

#### PARTY_RELATED

```sql
CREATE  TABLE CORE_DB.PARTY_RELATED
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Related_Party_Id     INTEGER NOT NULL 
		TITLE 'Related Party Id',
	Party_Related_Role_Cd VARCHAR(50) NOT NULL 
		TITLE 'Party Related Role Cd',
	Party_Related_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Party Related Start Dttm',
	Party_Related_End_Dttm TIMESTAMP NULL 
		TITLE 'Party Related End Dttm',
	Party_Structure_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Party Structure Type Cd',
	Party_Related_Status_Reason_Cd VARCHAR(50) NULL 
		TITLE 'Party Related Status Reason Cd',
	Party_Related_Status_Type_Cd VARCHAR(50) NULL 
		TITLE 'Party Related Status Type Cd',
	Party_Related_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Party Related Subtype Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_RELATED
	 (
			Party_Id
	 );
```

#### PARTY_CLAIM

```sql
CREATE  TABLE CORE_DB.PARTY_CLAIM
(

	Claim_Id             INTEGER NOT NULL 
		TITLE 'Claim Id',
	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Party_Claim_Role_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Party Claim Role Cd',
	Party_Claim_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Party Claim Start Dttm',
	Party_Claim_End_Dttm TIMESTAMP NULL 
		TITLE 'Party Claim End Dttm',
	Party_Claim_Contact_Prohibited_Ind CHAR(3) NULL 
		TITLE 'Party Claim Contact Prohibited Ind',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_CLAIM
	 (
			Claim_Id
	 );
```

#### PARTY_SCORE

```sql
CREATE  TABLE CORE_DB.PARTY_SCORE
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Model_Id             INTEGER NOT NULL 
		TITLE 'Model Id',
	Model_Run_Id         INTEGER NOT NULL 
		TITLE 'Model Run Id',
	Party_Score_Val      VARCHAR(100) NULL 
		TITLE 'Party Score Val',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_SCORE
	 (
			Party_Id
	 );
```

#### MARKET_SEGMENT

```sql
CREATE  TABLE CORE_DB.MARKET_SEGMENT
(

	Market_Segment_Id    INTEGER NOT NULL 
		TITLE 'Market Segment Id',
	Model_Id             INTEGER NOT NULL 
		TITLE 'Model Id',
	Model_Run_Id         INTEGER NOT NULL 
		TITLE 'Model Run Id',
	Segment_Desc         VARCHAR(250) NULL 
		TITLE 'Segment Desc',
	Segment_Start_Dttm   TIMESTAMP NOT NULL 
		TITLE 'Segment Start Dttm',
	Segment_End_Dttm     TIMESTAMP NULL 
		TITLE 'Segment End Dttm',
	Segment_Group_Id     INTEGER NULL 
		TITLE 'Segment Group Id',
	Segment_Name         VARCHAR(100) NULL 
		TITLE 'Segment Name',
	Segment_Creator_Party_Id INTEGER NULL 
		TITLE 'Segment Creator Party Id',
	Market_Segment_Scheme_Id INTEGER NULL 
		TITLE 'Market Segment Scheme Id',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_MARKET_SEGMENT
	 (
			Market_Segment_Id
	 );
```

#### PARTY_CREDIT_REPORT_SCORE

```sql
CREATE  TABLE CORE_DB.PARTY_CREDIT_REPORT_SCORE
(

	Reporting_Party_Id   INTEGER NOT NULL 
		TITLE 'Reporting Party Id',
	Obligor_Party_Id     INTEGER NOT NULL 
		TITLE 'Obligor Party Id',
	Credit_Report_Dttm   TIMESTAMP NOT NULL 
		TITLE 'Credit Report Dttm',
	Score_Type_Cd        VARCHAR(50) NOT NULL 
		TITLE 'Score Type Cd',
	Credit_Report_Score_Num VARCHAR(50) NULL 
		TITLE 'Credit Report Score Num',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_CREDIT_REPORT_SCORE
	 (
			Obligor_Party_Id
	 );
```

#### INDIVIDUAL_MEDICAL

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_MEDICAL
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Data_Source_Type_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Data Source Type Cd',
	Individual_Medical_Start_Dt DATE NOT NULL 
		TITLE 'Individual Medical Start Dt',
	Individual_Medical_End_Dt DATE NULL 
		TITLE 'Individual Medical End Dt',
	Physical_Exam_Dt     DATE NULL 
		TITLE 'Physical Exam Dt',
	General_Medical_Status_Cd VARCHAR(50) NULL 
		TITLE 'General Medical Status Cd',
	Last_Menstrual_Period_Dt DATE NULL 
		TITLE 'Last Menstrual Period Dt',
	Last_X_ray_Dt        DATE NULL 
		TITLE 'Last X-ray Dt',
	Estimated_Pregnancy_Due_Dt DATE NULL 
		TITLE 'Estimated Pregnancy Due Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_MEDICAL
	 (
			Individual_Party_Id
	 );
```

#### INDIVIDUAL_SPECIAL_NEED

```sql
CREATE  TABLE CORE_DB.INDIVIDUAL_SPECIAL_NEED
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Special_Need_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Special Need Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_SPECIAL_NEED
	 (
			Individual_Party_Id
	 );
```

#### SPECIAL_NEED_TYPE

```sql
CREATE  TABLE CORE_DB.SPECIAL_NEED_TYPE
(

	Special_Need_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Special Need Cd',
	Special_Need_Desc    VARCHAR(250) NULL 
		TITLE 'Special Need Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_SPECIAL_NEED_TYPE
	 (
			Special_Need_Cd
	 );
```

#### GENDER_TYPE

```sql
CREATE  TABLE CORE_DB.GENDER_TYPE
(

	Gender_Type_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Gender Type Cd',
	Gender_Type_Desc     VARCHAR(250) NOT NULL 
		TITLE 'Gender Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_GENDER_TYPE
	 (
			Gender_Type_Cd
	 );
```

#### GENDER_PRONOUN

```sql
CREATE  TABLE CORE_DB.GENDER_PRONOUN
(

	Gender_Pronoun_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Gender Pronoun Cd',
	Gender_Pronoun_Name  VARCHAR(100) NULL 
		TITLE 'Gender Pronoun Name',
	Gender_Pronoun_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Gender Pronoun Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_GENDER_PRONOUN
	 (
			Gender_Pronoun_Cd,
			Gender_Pronoun_Type_Cd
	 );
```

#### ETHNICITY_TYPE

```sql
CREATE  TABLE CORE_DB.ETHNICITY_TYPE
(

	Ethnicity_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Ethnicity Type Cd',
	Ethnicity_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Ethnicity Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_ETHNICITY_TYPE
	 (
			Ethnicity_Type_Cd
	 );
```

#### MARITAL_STATUS_TYPE

```sql
CREATE  TABLE CORE_DB.MARITAL_STATUS_TYPE
(

	Marital_Status_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Marital Status Cd',
	Marital_Status_Desc  VARCHAR(250) NULL 
		TITLE 'Marital Status Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_MARITAL_STATUS_TYPE
	 (
			Marital_Status_Cd
	 );
```

#### NATIONALITY_TYPE

```sql
CREATE  TABLE CORE_DB.NATIONALITY_TYPE
(

	Nationality_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Nationality Cd',
	Nationality_Desc     VARCHAR(250) NULL 
		TITLE 'Nationality Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_NATIONALITY_TYPE
	 (
			Nationality_Cd
	 );
```

#### TAX_BRACKET_TYPE

```sql
CREATE  TABLE CORE_DB.TAX_BRACKET_TYPE
(

	Tax_Bracket_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Tax Bracket Cd',
	Tax_Bracket_Desc     VARCHAR(250) NULL 
		TITLE 'Tax Bracket Desc',
	Tax_Bracket_Rate     DECIMAL(15,12) NULL 
		TITLE 'Tax Bracket Rate',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_TAX_BRACKET_TYPE
	 (
			Tax_Bracket_Cd
	 );
```

#### VERY_IMPORTANT_PERSON_TYPE

```sql
CREATE  TABLE CORE_DB.VERY_IMPORTANT_PERSON_TYPE
(

	VIP_Type_Cd          VARCHAR(50) NOT NULL 
		TITLE 'VIP Type Cd',
	VIP_Type_Desc        VARCHAR(250) NULL 
		TITLE 'VIP Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_VERY_IMPORTANT_PERSON_TYPE
	 (
			VIP_Type_Cd
	 );
```

#### MILITARY_STATUS_TYPE

```sql
CREATE  TABLE CORE_DB.MILITARY_STATUS_TYPE
(

	Military_Status_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Military Status Type Cd',
	Military_Status_Desc VARCHAR(250) NULL 
		TITLE 'Military Status Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_MILITARY_STATUS_TYPE
	 (
			Military_Status_Type_Cd
	 );
```

#### OCCUPATION_TYPE

```sql
CREATE  TABLE CORE_DB.OCCUPATION_TYPE
(

	Occupation_Type_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Occupation Type Cd',
	Occupation_Type_Desc VARCHAR(250) NULL 
		TITLE 'Occupation Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_OCCUPATION_TYPE
	 (
			Occupation_Type_Cd
	 );
```

#### TIME_PERIOD_TYPE

```sql
CREATE  TABLE CORE_DB.TIME_PERIOD_TYPE
(

	Time_Period_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Time Period Cd',
	Time_Period_Desc     VARCHAR(250) NULL 
		TITLE 'Time Period Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_TIME_PERIOD_TYPE
	 (
			Time_Period_Cd
	 );
```

#### PARTY_RELATED_STATUS_TYPE

```sql
CREATE  TABLE CORE_DB.PARTY_RELATED_STATUS_TYPE
(

	Party_Related_Status_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Party Related Status Type Cd',
	Party_Related_Status_Type_Desc VARCHAR(250) NULL 
		TITLE 'Party Related Status Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_PARTY_RELATED_STATUS_TYPE
	 (
			Party_Related_Status_Type_Cd
	 );
```

#### GENERAL_MEDICAL_STATUS_TYPE

```sql
CREATE  TABLE CORE_DB.GENERAL_MEDICAL_STATUS_TYPE
(

	General_Medical_Status_Cd VARCHAR(50) NOT NULL 
		TITLE 'General Medical Status Cd',
	General_Medical_Status_Desc VARCHAR(250) NULL 
		TITLE 'General Medical Status Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_GENERAL_MEDICAL_STATUS_TYPE
	 (
			General_Medical_Status_Cd
	 );
```

#### RISK_EXPOSURE_MITIGANT_SUBTYPE

```sql
CREATE  TABLE CORE_DB.RISK_EXPOSURE_MITIGANT_SUBTYPE
(

	Risk_Exposure_Mitigant_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Risk Exposure Mitigant Subtype Cd',
	Risk_Exposure_Mitigant_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Risk Exposure Mitigant Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_RISK_EXPOSURE_MITIGANT_SUBTYPE
	 (
			Risk_Exposure_Mitigant_Subtype_Cd
	 );
```

#### PRICING_METHOD_SUBTYPE

```sql
CREATE  TABLE CORE_DB.PRICING_METHOD_SUBTYPE
(

	Pricing_Method_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Pricing Method Subtype Cd',
	Pricing_Method_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Pricing Method Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_PRICING_METHOD_SUBTYPE
	 (
			Pricing_Method_Subtype_Cd
	 );
```

#### FINANCIAL_AGREEMENT_TYPE

```sql
CREATE  TABLE CORE_DB.FINANCIAL_AGREEMENT_TYPE
(

	Financial_Agreement_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Financial Agreement Type Cd-7-1',
	Financial_Agreement_Type_Desc VARCHAR(250) NULL 
		TITLE 'Financial Agreement Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_FINANCIAL_AGREEMENT_TYPE
	 (
			Financial_Agreement_Type_Cd
	 );
```

#### CREDIT_AGREEMENT

```sql
CREATE  TABLE CORE_DB.CREDIT_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Seniority_Level_Cd   VARCHAR(50) NULL 
		TITLE 'Seniority Level Cd',
	Credit_Agreement_Reaging_Cnt INTEGER NULL 
		TITLE 'Reaging Cnt',
	Credit_Agreement_Past_Due_Amt DECIMAL(18,4) NULL 
		TITLE 'Financing Agreement Past Due Amt',
	Credit_Agreement_Charge_Off_Amt DECIMAL(18,4) NULL 
		TITLE 'Financing Agreement Charge Off Amt',
	Credit_Agreement_Impairment_Amt DECIMAL(18,4) NULL 
		TITLE 'Credit Agreement Impairment Amt',
	Credit_Agreement_Settlement_Dt DATE NULL 
		TITLE 'Credit Agreement Settlement Dt',
	Credit_Agreement_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Credit Agreement Subtype Cd',
	Obligor_Borrowing_Purpose_Cd VARCHAR(50) NOT NULL 
		TITLE 'Obligor Borrowing Purpose Cd',
	Agreement_Currency_Past_Due_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Financing Agreement Past Due Amt',
	Agreement_Currency_Charge_Off_Amt DECIMAL(18,4) NULL 
		TITLE 'Acct Currency Financing Agreement Charge Off Amt',
	Agreement_Currency_Last_Payment_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Financing Agreement Last Payment Amt',
	Agreement_Currency_Impairment_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Impairment Amt',
	Specialized_Lending_Type_Cd VARCHAR(50) NULL 
		TITLE 'Specialized Lending Type Cd',
	Credit_Agreement_Grace_Period_Cd VARCHAR(50) NOT NULL 
		TITLE 'Credit Agreement Grace Period Cd',
	Payment_Frequency_Time_Period_Cd VARCHAR(50) NULL 
		TITLE 'Payment Frequency Time Period Cd',
	Credit_Agreement_Last_Payment_Amt DECIMAL(18,4) NULL 
		TITLE 'Financing Agreement Last Payment Amt',
	Credit_Agreement_Last_Payment_Dt DATE NULL 
		TITLE 'Financing Agreement Last Payment Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CREDIT_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### PAYMENT_TIMING_TYPE

```sql
CREATE  TABLE CORE_DB.PAYMENT_TIMING_TYPE
(

	Payment_Timing_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Payment Timing Type Cd',
	Payment_Timing_Type_Desc VARCHAR(250) NULL 
		TITLE 'Payment Timing Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_PAYMENT_TIMING_TYPE
	 (
			Payment_Timing_Type_Cd
	 );
```

#### PURCHASE_INTENT_TYPE

```sql
CREATE  TABLE CORE_DB.PURCHASE_INTENT_TYPE
(

	Purchase_Intent_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Purchase Intent Cd',
	Purchase_Intent_Desc VARCHAR(250) NULL 
		TITLE 'Purchase Intent Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_PURCHASE_INTENT_TYPE
	 (
			Purchase_Intent_Cd
	 );
```

#### LOAN_AGREEMENT

```sql
CREATE  TABLE CORE_DB.LOAN_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Loan_Maturity_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Loan Maturity Subtype Cd',
	Security_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Security Type Cd',
	Due_Day_Num          VARCHAR(50) NULL 
		TITLE 'Due Day Num',
	Realizable_Collateral_Amt DECIMAL(18,4) NULL 
		TITLE 'Realizable Collateral Amt',
	Loan_Payoff_Amt      DECIMAL(18,4) NULL 
		TITLE 'Loan Payoff Amt',
	Agreement_Currency_Real_Collateral_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Real Collateral Amt',
	Agreement_Currency_Loan_Payoff_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Loan Payoff Amt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_LOAN_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### SECURITY_TYPE

```sql
CREATE  TABLE CORE_DB.SECURITY_TYPE
(

	Security_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Security Type Cd',
	Security_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Security Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_SECURITY_TYPE
	 (
			Security_Type_Cd
	 );
```

#### LOAN_MATURITY_SUBTYPE

```sql
CREATE  TABLE CORE_DB.LOAN_MATURITY_SUBTYPE
(

	Loan_Maturity_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Loan Maturity Subtype Cd',
	Loan_Maturity_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Loan Maturity Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_LOAN_MATURITY_SUBTYPE
	 (
			Loan_Maturity_Subtype_Cd
	 );
```

#### LOAN_TRANSACTION_AGREEMENT

```sql
CREATE  TABLE CORE_DB.LOAN_TRANSACTION_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Loan_Transaction_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Loan Transaction Subtype Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_LOAN_TRANSACTION_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### LOAN_TRANSACTION_SUBTYPE

```sql
CREATE  TABLE CORE_DB.LOAN_TRANSACTION_SUBTYPE
(

	Loan_Transaction_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Loan Transaction Subtype Cd',
	Loan_Transaction_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Loan Transaction Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_LOAN_TRANSACTION_SUBTYPE
	 (
			Loan_Transaction_Subtype_Cd
	 );
```

#### CREDIT_CARD_AGREEMENT

```sql
CREATE  TABLE CORE_DB.CREDIT_CARD_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Credit_Card_Agreement_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Credit Card Agreement Subtype Cd',
	Credit_Card_Activation_Dttm TIMESTAMP NULL 
		TITLE 'Credit Card Activation Dttm',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CREDIT_CARD_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### CREDIT_CARD_AGREEMENT_SUBTYPE

```sql
CREATE  TABLE CORE_DB.CREDIT_CARD_AGREEMENT_SUBTYPE
(

	Credit_Card_Agreement_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Credit Card Agreement Subtype Cd',
	Credit_Card_Agreement_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Credit Card Agreement Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CREDIT_CARD_AGREEMENT_SUBTYPE
	 (
			Credit_Card_Agreement_Subtype_Cd
	 );
```

#### LOAN_TERM_AGREEMENT

```sql
CREATE  TABLE CORE_DB.LOAN_TERM_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Amortization_Method_Cd VARCHAR(50) NOT NULL 
		TITLE 'Amortization Method Cd',
	Amortization_End_Dt  DATE NULL 
		TITLE 'Amortization End Dt',
	Balloon_Amt          DECIMAL(18,4) NULL 
		TITLE 'Balloon Amt',
	Loan_Term_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Loan Term Subtype Cd',
	Original_Loan_Amt    DECIMAL(18,4) NULL 
		TITLE 'Original Loan Amt',
	Preapproved_Loan_Amt DECIMAL(18,4) NULL 
		TITLE 'Preapproved Loan Amt',
	Maximum_Monthly_Payment_Amt DECIMAL(18,4) NULL 
		TITLE 'Maximum Monthly Payment Amt',
	Improvement_Allocation_Amt DECIMAL(18,4) NULL 
		TITLE 'Improvement Allocation Amt',
	Debt_Payment_Allocation_Amt DECIMAL(18,4) NULL 
		TITLE 'Debt Payment Allocation Amt',
	Down_Payment_Amt     DECIMAL(18,4) NULL 
		TITLE 'Down Payment Amt',
	Loan_Maturity_Dt     DATE NULL 
		TITLE 'Loan Maturity Dt',
	Loan_Termination_Dt  DATE NULL 
		TITLE 'Loan Termination Dt',
	Loan_Renewal_Dt      DATE NULL 
		TITLE 'Loan Renewal Dt',
	Commit_Start_Dt      DATE NULL 
		TITLE 'Commit Start Dt',
	Commit_End_Dt        DATE NULL 
		TITLE 'Commit End Dt',
	Payoff_Dt            DATE NULL 
		TITLE 'Payoff Dt',
	Loan_Asset_Purchase_Dt DATE NULL 
		TITLE 'Loan Asset Purchase Dt',
	Agreement_Currency_Balloon_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Balloon Amt',
	Agreement_Currency_Original_Loan_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Original Loan Amt',
	Agreement_Currency_Preapproved_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Preapproved Amt',
	Agreement_Currency_Maximum_Monthly_Payment_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Maximum Monthly Payment Amt',
	Agreement_Currency_Improve_Allocation_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Improve Allocation Amt',
	Agreement_Currency_Debt_Payment_Allocation_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Debt Payment Allocation Amt',
	Loan_Refinance_Ind   CHAR(3) NULL 
		TITLE 'Loan Refinance Ind',
	Agreement_Currency_Down_Payment_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Down Payment Amt',
	Agreement_Currency_Down_Payment_Borrow_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Down Payment Borrow Amt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_LOAN_TERM_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### LOAN_TERM_SUBTYPE

```sql
CREATE  TABLE CORE_DB.LOAN_TERM_SUBTYPE
(

	Loan_Term_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Loan Term Subtype Cd',
	Loan_Term_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Loan Term Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_LOAN_TERM_SUBTYPE
	 (
			Loan_Term_Subtype_Cd
	 );
```

#### AMORTIZATION_METHOD_TYPE

```sql
CREATE  TABLE CORE_DB.AMORTIZATION_METHOD_TYPE
(

	Amortization_Method_Cd VARCHAR(50) NOT NULL 
		TITLE 'Amortization Method Cd',
	Amortization_Method_Desc VARCHAR(250) NOT NULL 
		TITLE 'Amortization Method Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_AMORTIZATION_METHOD_TYPE
	 (
			Amortization_Method_Cd
	 );
```

#### MORTGAGE_AGREEMENT

```sql
CREATE  TABLE CORE_DB.MORTGAGE_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	First_Time_Mortgage_Ind CHAR(3) NULL 
		TITLE 'First Time Mortgage Ind',
	Closing_Cost_Amt     DECIMAL(18,4) NULL 
		TITLE 'Closing Cost Amt',
	Adjustable_Payment_Cap_Amt DECIMAL(18,4) NULL 
		TITLE 'Adjustable Payment Cap Amt',
	Prepayment_Penalty_Dt DATE NULL 
		TITLE 'Prepayment Penalty Dt',
	Early_Payoff_Penalty_Amt DECIMAL(18,4) NULL 
		TITLE 'Early Payoff Penalty Amt',
	Agreement_Currency_Closing_Cost_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Closing Cost Amt',
	Agreement_Currency_Adjustable_Cap_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Adjustable Cap Amt',
	Agreement_Currency_Early_Penalty_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Currency Early Penalty Amt',
	Mortgage_Type_Cd     VARCHAR(50) NULL 
		TITLE 'Mortgage Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_MORTGAGE_AGREEMENT
	 (
			Agreement_Id
	 );
```

#### MORTGAGE_TYPE

```sql
CREATE  TABLE CORE_DB.MORTGAGE_TYPE
(

	Mortgage_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Mortgage Type Cd',
	Mortgage_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Mortgage Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_MORTGAGE_TYPE
	 (
			Mortgage_Type_Cd
	 );
```

#### TERM_FEATURE

```sql
CREATE  TABLE CORE_DB.TERM_FEATURE
(

	Feature_Id           INTEGER NOT NULL 
		TITLE 'Feature Id',
	From_Time_Period_Cd  VARCHAR(50) NULL 
		TITLE 'From Time Period Cd',
	To_Time_Period_Cd    VARCHAR(50) NULL 
		TITLE 'To Time Period Cd',
	Until_Age_Cd         VARCHAR(50) NULL 
		TITLE 'Until Age Cd',
	From_Time_Period_Num VARCHAR(50) NULL 
		TITLE 'From Time Period Num',
	To_Time_Period_Num   VARCHAR(50) NULL 
		TITLE 'To Time Period Num',
	Until_Age_Num        VARCHAR(50) NULL 
		TITLE 'Until Age Num',
	Term_Type_Cd         VARCHAR(50) NULL 
		TITLE 'Term Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_TERM_FEATURE
	 (
			Feature_Id
	 );
```

#### INTEREST_RATE_INDEX

```sql
CREATE  TABLE CORE_DB.INTEREST_RATE_INDEX
(

	Interest_Rate_Index_Cd VARCHAR(50) NOT NULL 
		TITLE 'Interest Rate Index Cd',
	Interest_Rate_Index_Desc VARCHAR(250) NULL 
		TITLE 'Interest Rate Index Desc',
	Interest_Rate_Index_Short_Name VARCHAR(100) NULL 
		TITLE 'Interest Rate Index Short Name',
	Currency_Cd          VARCHAR(50) NULL 
		TITLE 'Currency Cd',
	Yield_Curve_Maturity_Segment_Cd VARCHAR(50) NULL 
		TITLE 'Yield Curve Maturity Segment Id',
	Compound_Frequency_Time_Period_Cd VARCHAR(50) NULL 
		TITLE 'Compound Frequency Time Period Cd',
	Interest_Rate_Index_Type_Cd VARCHAR(50) NULL 
		TITLE 'Interest Rate Index Type Cd',
	Interest_Rate_Index_Time_Period_Cd VARCHAR(50) NOT NULL 
		TITLE 'Interest Rate Index Time Period Cd',
	Interest_Index_Time_Period_Num VARCHAR(50) NULL 
		TITLE 'Interest Index Time Period Num',
	Interest_Index_Rate_Reset_Tm TIME NULL 
		TITLE 'Interest Index Rate Reset Tm',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INTEREST_RATE_INDEX
	 (
			Interest_Rate_Index_Cd
	 );
```

#### AGREEMENT_FEATURE

```sql
CREATE  TABLE CORE_DB.AGREEMENT_FEATURE
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Feature_Id           INTEGER NOT NULL 
		TITLE 'Feature Id',
	Agreement_Feature_Role_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Feature Role Cd',
	Agreement_Feature_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Agreement Feature Start Dttm',
	Agreement_Feature_End_Dttm TIMESTAMP NULL 
		TITLE 'Agreement Feature End Dttm',
	Overridden_Feature_Id INTEGER NULL 
		TITLE 'Overridden Feature Id',
	Agreement_Feature_Concession_Ind CHAR(3) NULL 
		TITLE 'Agreement Feature Concession Ind',
	Agreement_Feature_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Feature Amt',
	Agreement_Feature_To_Amt DECIMAL(18,4) NULL 
		TITLE 'Agreement Feature To Amt',
	Agreement_Feature_Rate DECIMAL(15,12) NULL 
		TITLE 'Agreement Feature Rate',
	Agreement_Feature_Qty DECIMAL(18,4) NULL 
		TITLE 'Agreement Feature Qty',
	Agreement_Feature_Num VARCHAR(50) NULL 
		TITLE 'Agreement Feature Num',
	Agreement_Feature_Dt DATE NULL 
		TITLE 'Agreement Feature Dt',
	Agreement_Feature_UOM_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Feature UOM Cd',
	Interest_Rate_Index_Cd VARCHAR(50) NULL 
		TITLE 'Interest Rate Index Cd',
	Currency_Cd          VARCHAR(50) NULL 
		TITLE 'Currency Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_AGREEMENT_FEATURE
	 (
			Agreement_Id
	 );
```

#### INTEREST_INDEX_RATE

```sql
CREATE  TABLE CORE_DB.INTEREST_INDEX_RATE
(

	Interest_Rate_Index_Cd VARCHAR(50) NOT NULL 
		TITLE 'Interest Rate Index Cd',
	Index_Rate_Effective_Dttm DATE NOT NULL 
		TITLE 'Index Rate Effective Dttm',
	Interest_Index_Rate  DECIMAL(15,12) NULL 
		TITLE 'Interest Index Rate',
	Discount_Factor_Pct  DECIMAL(9,4) NULL 
		TITLE 'Discount Factor Pct',
	Zero_Coupon_Rate     DECIMAL(15,12) NULL 
		TITLE 'Zero Coupon Rate',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INTEREST_INDEX_RATE
	 (
			Interest_Rate_Index_Cd
	 );
```

#### VARIABLE_INTEREST_RATE_FEATURE

```sql
CREATE  TABLE CORE_DB.VARIABLE_INTEREST_RATE_FEATURE
(

	Feature_Id           INTEGER NOT NULL 
		TITLE 'Feature Id',
	Spread_Rate          DECIMAL(15,12) NULL 
		TITLE 'Spread Rate',
	Interest_Rate_Index_Cd VARCHAR(50) NOT NULL 
		TITLE 'Interest Rate Index Cd',
	Upper_Limit_Rate     DECIMAL(15,12) NULL 
		TITLE 'Upper Limit Rate',
	Lower_Limit_Rate     DECIMAL(15,12) NULL 
		TITLE 'Lower Limit Rate',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_VARIABLE_INTEREST_RATE_FEATURE
	 (
			Feature_Id
	 );
```

#### ORGANIZATION

```sql
CREATE  TABLE CORE_DB.ORGANIZATION
(

	Organization_Party_Id INTEGER NOT NULL 
		TITLE 'Organization Party Id',
	Organization_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Organization Type Cd',
	Organization_Established_Dttm TIMESTAMP NULL 
		TITLE 'Organization Established Dttm',
	Parent_Organization_Party_Id INTEGER NULL 
		TITLE 'Parent Organization Party Id',
	Organization_Size_Type_Cd VARCHAR(50) NULL 
		TITLE 'Organization Size Type Cd',
	Legal_Classification_Cd VARCHAR(50) NULL 
		TITLE 'Legal Classification Cd',
	Ownership_Type_Cd    VARCHAR(50) NULL 
		TITLE 'Ownership Type Cd',
	Organization_Close_Dt DATE NULL 
		TITLE 'Organization Close Dt',
	Organization_Operation_Dt DATE NULL 
		TITLE 'Organization Operation Dt',
	Organization_Fiscal_Month_Num VARCHAR(50) NULL 
		TITLE 'Organization Fiscal Month Num',
	Organization_Fiscal_Day_Num VARCHAR(50) NULL 
		TITLE 'Organization Fiscal Day Num',
	Basel_Organization_Type_Cd VARCHAR(50) NULL 
		TITLE 'Basel Organization Type Cd',
	Basel_Market_Participant_Cd VARCHAR(50) NULL 
		TITLE 'Basel Market Participant Cd',
	Basel_Eligible_Central_Ind CHAR(3) NULL 
		TITLE 'Basel Eligible Central Ind',
	BIC_Business_Alpha_4_Cd CHAR(4) NULL 
		TITLE 'BIC Business Alpha-4 Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ORGANIZATION
	 (
			Organization_Party_Id
	 );
```

#### BUSINESS

```sql
CREATE  TABLE CORE_DB.BUSINESS
(

	Business_Party_Id    INTEGER NOT NULL 
		TITLE 'Business Party Id',
	Business_Category_Cd VARCHAR(50) NULL 
		TITLE 'Business Legal Class Cd',
	Business_Legal_Start_Dt DATE NULL 
		TITLE 'Business Legal Start Dt',
	Business_Legal_End_Dt DATE NULL 
		TITLE 'Business Legal End Dt',
	Tax_Bracket_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Tax Bracket Cd',
	Customer_Location_Type_Cd VARCHAR(50) NULL 
		TITLE 'Customer Location Type Cd',
	Stock_Exchange_Listed_Ind CHAR(3) NULL 
		TITLE 'Stock Exchange Listed Ind',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_BUSINESS
	 (
			Business_Party_Id
	 );
```

#### BUSINESS_CATEGORY

```sql
CREATE  TABLE CORE_DB.BUSINESS_CATEGORY
(

	Business_Category_Cd VARCHAR(50) NOT NULL 
		TITLE 'Business Legal Class Cd',
	Business_Category_Desc VARCHAR(250) NULL 
		TITLE 'Business Legal Class Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_BUSINESS_CATEGORY
	 (
			Business_Category_Cd
	 );
```

#### ORGANIZATION_NAICS

```sql
CREATE  TABLE CORE_DB.ORGANIZATION_NAICS
(

	Organization_Party_Id INTEGER NOT NULL 
		TITLE 'Organization Party Id',
	NAICS_National_Industry_Cd VARCHAR(50) NOT NULL 
		TITLE 'NAICS National Industry Cd *Geo',
	Organization_NAICS_Start_Dt DATE NOT NULL 
		TITLE 'Organization NAICS Start Dt',
	NAICS_Sector_Cd      VARCHAR(50) NOT NULL 
		TITLE 'NAICS Sector Cd *Geo',
	NAICS_Subsector_Cd   VARCHAR(50) NOT NULL 
		TITLE 'NAICS Subsector Cd *Geo',
	NAICS_Industry_Group_Cd VARCHAR(50) NOT NULL 
		TITLE 'NAICS Industry Group Cd *Geo',
	NAICS_Industry_Cd    VARCHAR(50) NOT NULL 
		TITLE 'NAICS Industry Cd *Geo',
	Organization_NAICS_End_Dt DATE NULL 
		TITLE 'Organization NAICS End Dt',
	Primary_NAICS_Ind    CHAR(3) NULL 
		TITLE 'Primary NAICS Ind',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ORGANIZATION_NAICS
	 (
			Organization_Party_Id
	 );
```

#### ORGANIZATION_NACE

```sql
CREATE  TABLE CORE_DB.ORGANIZATION_NACE
(

	Organization_Party_Id INTEGER NOT NULL 
		TITLE 'Organization Party Id',
	NACE_Class_Cd        VARCHAR(50) NOT NULL 
		TITLE 'NACE Class Cd *Geo',
	NACE_Group_Cd        VARCHAR(50) NOT NULL 
		TITLE 'NACE Group Cd *Geo',
	NACE_Division_Cd     VARCHAR(50) NOT NULL 
		TITLE 'NACE Division Cd *GEO',
	NACE_Section_Cd      VARCHAR(50) NOT NULL 
		TITLE 'NACE Section Cd *Geo',
	Organization_NACE_Start_Dt DATE NOT NULL 
		TITLE 'Organization NACE Start Dt',
	Organization_NACE_End_Dt DATE NULL 
		TITLE 'Organization NACE End Dt',
	Importance_Order_NACE_Num VARCHAR(50) NULL 
		TITLE 'Importance Order NACE Num',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ORGANIZATION_NACE
	 (
			Organization_Party_Id
	 );
```

#### NACE_CLASS

```sql
CREATE  TABLE CORE_DB.NACE_CLASS
(

	NACE_Class_Cd        VARCHAR(50) NOT NULL 
		TITLE 'NACE Class Cd *Geo',
	NACE_Group_Cd        VARCHAR(50) NOT NULL 
		TITLE 'NACE Group Cd *Geo',
	NACE_Division_Cd     VARCHAR(50) NOT NULL 
		TITLE 'NACE Division Cd *GEO',
	NACE_Section_Cd      VARCHAR(50) NOT NULL 
		TITLE 'NACE Section Cd *Geo',
	NACE_Class_Desc      VARCHAR(250) NULL 
		TITLE 'NACE Class Desc *Geo',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_NACE_CLASS
	 (
			NACE_Class_Cd
	 );
```

#### ORGANIZATION_SIC

```sql
CREATE  TABLE CORE_DB.ORGANIZATION_SIC
(

	Organization_Party_Id INTEGER NOT NULL 
		TITLE 'Organization Party Id',
	SIC_Cd               VARCHAR(50) NOT NULL 
		TITLE 'SIC Cd',
	Organization_SIC_Start_Dt DATE NOT NULL 
		TITLE 'Organization SIC Start Dt',
	Organization_SIC_End_Dt DATE NULL 
		TITLE 'Organization SIC End Dt',
	Primary_SIC_Ind      CHAR(3) NULL 
		TITLE 'Primary SIC Ind',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ORGANIZATION_SIC
	 (
			Organization_Party_Id
	 );
```

#### ORGANIZATION_GICS

```sql
CREATE  TABLE CORE_DB.ORGANIZATION_GICS
(

	Organization_Party_Id INTEGER NOT NULL 
		TITLE 'Organization Party Id',
	GICS_Subindustry_Cd  VARCHAR(50) NOT NULL 
		TITLE 'GICS Subindustry Cd',
	GICS_Industry_Cd     VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Cd',
	GICS_Industry_Group_Cd VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Group Cd',
	GICS_Sector_Cd       VARCHAR(50) NOT NULL 
		TITLE 'GICS Sector Cd',
	Organization_GICS_Start_Dt DATE NOT NULL 
		TITLE 'Organization GICS Start Dt',
	Organization_GICS_End_Dt DATE NULL 
		TITLE 'Organization GICS End Dt',
	Primary_GICS_Ind     CHAR(3) NULL 
		TITLE 'Primary GICS Ind',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ORGANIZATION_GICS
	 (
			Organization_Party_Id
	 );
```

#### PARTY_SPECIALTY

```sql
CREATE  TABLE CORE_DB.PARTY_SPECIALTY
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Specialty_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Specialty Type Cd',
	Party_Specialty_Start_Dt DATE NOT NULL 
		TITLE 'Party Specialty Start Dt',
	Party_Specialty_End_Dt DATE NULL 
		TITLE 'Party Specialty End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_SPECIALTY
	 (
			Party_Id
	 );
```

#### LEGAL_CLASSIFICATION

```sql
CREATE  TABLE CORE_DB.LEGAL_CLASSIFICATION
(

	Legal_Classification_Cd VARCHAR(50) NOT NULL 
		TITLE 'Legal Classification Cd',
	Legal_Classification_Desc VARCHAR(250) NULL 
		TITLE 'Legal Classification Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_LEGAL_CLASSIFICATION
	 (
			Legal_Classification_Cd
	 );
```

#### NAICS_INDUSTRY

```sql
CREATE  TABLE CORE_DB.NAICS_INDUSTRY
(

	NAICS_Industry_Cd    VARCHAR(50) NOT NULL 
		TITLE 'NAICS Industry Cd *Geo',
	NAICS_Sector_Cd      VARCHAR(50) NOT NULL 
		TITLE 'NAICS Sector Cd *Geo',
	NAICS_Subsector_Cd   VARCHAR(50) NOT NULL 
		TITLE 'NAICS Subsector Cd *Geo',
	NAICS_Industry_Group_Cd VARCHAR(50) NOT NULL 
		TITLE 'NAICS Industry Group Cd *Geo',
	NAICS_Industry_Desc  VARCHAR(250) NULL 
		TITLE 'NAICS Industry Desc *Geo',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_NAICS_INDUSTRY
	 (
			NAICS_Sector_Cd,
			NAICS_Subsector_Cd,
			NAICS_Industry_Group_Cd
	 );
```

#### SIC

```sql
CREATE  TABLE CORE_DB.SIC
(

	SIC_Cd               VARCHAR(50) NOT NULL 
		TITLE 'SIC Cd',
	SIC_Desc             VARCHAR(250) NULL 
		TITLE 'SIC Desc',
	SIC_Group_Cd         VARCHAR(50) NOT NULL 
		TITLE 'SIC Group Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_SIC
	 (
			SIC_Cd
	 );
```

#### GICS_INDUSTRY_TYPE

```sql
CREATE  TABLE CORE_DB.GICS_INDUSTRY_TYPE
(

	GICS_Industry_Cd     VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Cd',
	GICS_Industry_Group_Cd VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Group Cd',
	GICS_Sector_Cd       VARCHAR(50) NOT NULL 
		TITLE 'GICS Sector Cd',
	GICS_Industry_Desc   VARCHAR(250) NULL 
		TITLE 'GICS Industry Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_GICS_INDUSTRY_TYPE
	 (
			GICS_Industry_Cd
	 );
```

#### GICS_SUBINDUSTRY_TYPE

```sql
CREATE  TABLE CORE_DB.GICS_SUBINDUSTRY_TYPE
(

	GICS_Subindustry_Cd  VARCHAR(50) NOT NULL 
		TITLE 'GICS Subindustry Cd',
	GICS_Industry_Cd     VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Cd',
	GICS_Industry_Group_Cd VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Group Cd',
	GICS_Sector_Cd       VARCHAR(50) NOT NULL 
		TITLE 'GICS Sector Cd',
	GICS_Subindustry_Desc VARCHAR(250) NULL 
		TITLE 'GICS Subindustry Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_GICS_SUBINDUSTRY_TYPE
	 (
			GICS_Subindustry_Cd
	 );
```

#### GICS_INDUSTRY_GROUP_TYPE

```sql
CREATE  TABLE CORE_DB.GICS_INDUSTRY_GROUP_TYPE
(

	GICS_Industry_Group_Cd VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Group Cd',
	GICS_Sector_Cd       VARCHAR(50) NOT NULL 
		TITLE 'GICS Sector Cd',
	GICS_Industry_Group_Desc VARCHAR(250) NULL 
		TITLE 'GICS Industry Group Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_GICS_INDUSTRY_GROUP_TYPE
	 (
			GICS_Industry_Group_Cd
	 );
```

#### GICS_SECTOR_TYPE

```sql
CREATE  TABLE CORE_DB.GICS_SECTOR_TYPE
(

	GICS_Sector_Cd       VARCHAR(50) NOT NULL 
		TITLE 'GICS Sector Cd',
	GICS_Sector_Desc     VARCHAR(250) NULL 
		TITLE 'GICS Sector Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_GICS_SECTOR_TYPE
	 (
			GICS_Sector_Cd
	 );
```

#### SPECIALTY_TYPE

```sql
CREATE  TABLE CORE_DB.SPECIALTY_TYPE
(

	Specialty_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Specialty Type Cd',
	Specialty_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Specialty Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_SPECIALTY_TYPE
	 (
			Specialty_Type_Cd
	 );
```

#### ORGANIZATION_NAME

```sql
CREATE  TABLE CORE_DB.ORGANIZATION_NAME
(

	Organization_Party_Id INTEGER NOT NULL 
		TITLE 'Organization Party Id',
	Name_Type_Cd         VARCHAR(50) NOT NULL 
		TITLE 'Name Type Cd',
	Organization_Name_Start_Dt DATE NOT NULL 
		TITLE 'Organization Name Start Dt',
	Organization_Name    VARCHAR(100) NOT NULL 
		TITLE 'Organization Name',
	Organization_Name_Desc VARCHAR(250) NULL 
		TITLE 'Organization Name Desc',
	Organization_Name_End_Dt DATE NULL 
		TITLE 'Organization Name End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ORGANIZATION_NAME
	 (
			Organization_Party_Id
	 );
```

#### PARTY_IDENTIFICATION

```sql
CREATE  TABLE CORE_DB.PARTY_IDENTIFICATION
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Issuing_Party_Id     INTEGER NOT NULL 
		TITLE 'Issuing Party Id',
	Party_Identification_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Party Identification Type Cd',
	Party_Identification_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Party Identification Start Dttm',
	Party_Identification_End_Dttm TIMESTAMP NULL 
		TITLE 'Party Identification End Dttm',
	Party_Identification_Num VARCHAR(50) NULL 
		TITLE 'Party Identification Num',
	Party_Identification_Receipt_Dt DATE NULL 
		TITLE 'Party Identification Receipt Dt',
	Party_Identification_Primary_Ind CHAR(3) NULL 
		TITLE 'Party Identification Primary Ind',
	Party_Identification_Name VARCHAR(100) NULL 
		TITLE 'Party Identification Name',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_IDENTIFICATION
	 (
			Party_Id
	 );
```

#### PARTY_LANGUAGE_USAGE

```sql
CREATE  TABLE CORE_DB.PARTY_LANGUAGE_USAGE
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Language_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Language Type Cd',
	Language_Usage_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Language Usage Type Cd',
	Party_Language_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Party Language Start Dttm',
	Party_Language_End_Dttm TIMESTAMP NULL 
		TITLE 'Party Language End Dttm',
	Party_Language_Priority_Num VARCHAR(50) NULL 
		TITLE 'Party Language Priority Num',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_LANGUAGE_USAGE
	 (
			Party_Id
	 );
```

#### LANGUAGE_TYPE

```sql
CREATE  TABLE CORE_DB.LANGUAGE_TYPE
(

	Language_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Language Type Cd',
	Language_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Language Type Desc',
	Language_Native_Name VARCHAR(100) NULL 
		TITLE 'Language Native Name',
	ISO_Language_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'ISO Language Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_LANGUAGE_TYPE
	 (
			Language_Type_Cd
	 );
```

#### PROMOTION

```sql
CREATE  TABLE CORE_DB.PROMOTION
(

	Promotion_Id         INTEGER NOT NULL 
		TITLE 'Promotion Id',
	Promotion_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Promotion Type Cd',
	Campaign_Id          INTEGER NOT NULL 
		TITLE 'Campaign Id',
	Promotion_Classification_Cd VARCHAR(50) NULL 
		TITLE 'Promotion Classification Cd',
	Channel_Type_Cd      VARCHAR(50) NULL 
		TITLE 'Channel Type Cd',
	Internal_Promotion_Name VARCHAR(100) NULL 
		TITLE 'Internal Promotion Name',
	Promotion_Desc       VARCHAR(250) NULL 
		TITLE 'Promotion Desc',
	Promotion_Objective_Txt VARCHAR(1000) NULL 
		TITLE 'Promotion Objective Txt',
	Promotion_Start_Dt   DATE NULL 
		TITLE 'Promotion Start Dt',
	Promotion_End_Dt     DATE NULL 
		TITLE 'Promotion End Dt',
	Promotion_Actual_Unit_Cost_Amt DECIMAL(18,4) NULL 
		TITLE 'Promotion Actual Unit Cost Amt',
	Promotion_Goal_Amt   DECIMAL(18,4) NULL 
		TITLE 'Promotion Goal Amt',
	Currency_Cd          VARCHAR(50) NULL 
		TITLE 'Currency Cd',
	Promotion_Actual_Unit_Cnt INTEGER NULL 
		TITLE 'Promotion Actual Unit Cnt',
	Promotion_Break_Even_Order_Cnt INTEGER NULL 
		TITLE 'Promotion Break Even Order Cnt',
	Unit_Of_Measure_Cd   VARCHAR(50) NULL 
		TITLE 'Unit Of Measure Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PROMOTION
	 (
			Promotion_Id
	 );
```

#### PROMOTION_METRIC_TYPE

```sql
CREATE  TABLE CORE_DB.PROMOTION_METRIC_TYPE
(

	Promotion_Metric_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Promotion Metric Type Cd',
	Promotion_Metric_Type_Desc VARCHAR(250) NULL 
		TITLE 'Promotion Metric Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_PROMOTION_METRIC_TYPE
	 (
			Promotion_Metric_Type_Cd
	 );
```

#### UNIT_OF_MEASURE

```sql
CREATE  TABLE CORE_DB.UNIT_OF_MEASURE
(

	Unit_Of_Measure_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Unit Of Measure Cd',
	Unit_Of_Measure_Name VARCHAR(100) NULL 
		TITLE 'Unit Of Measure Name',
	Unit_Of_Measure_Type_Cd VARCHAR(50) NULL 
		TITLE 'Unit Of Measure Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_UNIT_OF_MEASURE
	 (
			Unit_Of_Measure_Cd
	 );
```

#### PROMOTION_OFFER

```sql
CREATE  TABLE CORE_DB.PROMOTION_OFFER
(

	Promotion_Id         INTEGER NOT NULL 
		TITLE 'Promotion Id',
	Promotion_Offer_Id   INTEGER NOT NULL 
		TITLE 'Promotion Offer Id',
	Promotion_Offer_Type_Cd VARCHAR(50) NULL 
		TITLE 'Promotion Offer Type Cd',
	Promotion_Offer_Desc VARCHAR(250) NULL 
		TITLE 'Promotion Offer Desc',
	Ad_Id                INTEGER NULL 
		TITLE 'Ad Id',
	Distribution_Start_Dt DATE NULL 
		TITLE 'Distribution Start Dt',
	Distribution_End_Dt  DATE NULL 
		TITLE 'Distribution End Dt',
	Redemption_Start_Dt  DATE NULL 
		TITLE 'Redemption Start Dt',
	Redemption_End_Dt    DATE NULL 
		TITLE 'Redemption End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PROMOTION_OFFER
	 (
			Promotion_Id
	 );
```

#### PROMOTION_OFFER_TYPE

```sql
CREATE  TABLE CORE_DB.PROMOTION_OFFER_TYPE
(

	Promotion_Offer_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Promotion Offer Type Cd',
	Promotion_Offer_Type_Desc VARCHAR(250) NOT NULL 
		TITLE 'Promotion Offer Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_PROMOTION_OFFER_TYPE
	 (
			Promotion_Offer_Type_Cd
	 );
```

#### STREET_ADDRESS

```sql
CREATE  TABLE CORE_DB.STREET_ADDRESS
(

	Street_Address_Id    INTEGER NOT NULL 
		TITLE 'Street Address Id',
	Address_Line_1_Txt   VARCHAR(1000) NULL 
		TITLE 'Address Line 1 Txt',
	Address_Line_2_Txt   VARCHAR(1000) NULL 
		TITLE 'Address Line 2 Txt',
	Address_Line_3_Txt   VARCHAR(1000) NULL 
		TITLE 'Address Line 3 Txt',
	Dwelling_Type_Cd     VARCHAR(50) NULL 
		TITLE 'Dwelling Type Cd',
	Census_Block_Id      INTEGER NULL 
		TITLE 'Census Block Id *Geo',
	City_Id              INTEGER NULL 
		TITLE 'City Id',
	County_Id            INTEGER NULL 
		TITLE 'County Id',
	Territory_Id         INTEGER NULL 
		TITLE 'Territory Id',
	Postal_Code_Id       INTEGER NULL 
		TITLE 'Postal Code Id',
	Country_Id           INTEGER NULL 
		TITLE 'Country Id',
	Carrier_Route_Txt    VARCHAR(1000) NULL 
		TITLE 'Carrier Route Txt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_STREET_ADDRESS
	 (
			Street_Address_Id
	 );
```

#### STREET_ADDRESS_DETAIL

```sql
CREATE  TABLE CORE_DB.STREET_ADDRESS_DETAIL
(

	Street_Address_Id    INTEGER NOT NULL 
		TITLE 'Street Address Id',
	Street_Address_Num   VARCHAR(50) NOT NULL 
		TITLE 'House Num',
	Street_Address_Number_Modifier_Val VARCHAR(100) NULL 
		TITLE 'House Num Modifier Val',
	Street_Direction_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Street Direction Type Cd',
	Street_Num           VARCHAR(50) NULL 
		TITLE 'Street Num',
	Street_Name          VARCHAR(100) NOT NULL 
		TITLE 'Street Name',
	Street_Suffix_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Street Suffix Cd',
	Building_Num         VARCHAR(50) NULL 
		TITLE 'Building Num',
	Unit_Num             VARCHAR(50) NULL 
		TITLE 'Unit Num',
	Floor_Val            VARCHAR(100) NULL 
		TITLE 'Floor Num',
	Workspace_Num        VARCHAR(50) NULL 
		TITLE 'Workspace Num',
	Route_Num            VARCHAR(50) NULL 
		TITLE 'Route Num',
	Mail_Pickup_Tm       TIME NOT NULL 
		TITLE 'Mail Pickup Tm',
	Mail_Delivery_Tm     TIME NOT NULL 
		TITLE 'Mail Delivery Tm',
	Mail_Stop_Num        VARCHAR(50) NOT NULL 
		TITLE 'Mail Stop Num',
	Mail_Box_Num         VARCHAR(50) NOT NULL 
		TITLE 'Mail Box Num',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_STREET_ADDRESS_DETAIL
	 (
			Street_Address_Id
	 );
```

#### DIRECTION_TYPE

```sql
CREATE  TABLE CORE_DB.DIRECTION_TYPE
(

	Direction_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Direction Type Cd',
	Direction_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Direction Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_DIRECTION_TYPE
	 (
			Direction_Type_Cd
	 );
```

#### STREET_SUFFIX_TYPE

```sql
CREATE  TABLE CORE_DB.STREET_SUFFIX_TYPE
(

	Street_Suffix_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Street Suffix Cd',
	Street_Suffix_Desc   VARCHAR(250) NULL 
		TITLE 'Street Suffix Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_STREET_SUFFIX_TYPE
	 (
			Street_Suffix_Cd
	 );
```

#### ISO_3166_COUNTRY_SUBDIVISION_STANDARD

```sql
CREATE  TABLE CORE_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD
(

	Territory_Id         INTEGER NOT NULL 
		TITLE 'Territory Id',
	Territory_Standard_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Territory Standard Type Cd',
	ISO_3166_Country_Alpha_2_Cd CHAR(2) NULL 
		TITLE 'ISO 3166 Country Alpha-2 Cd',
	ISO_3166_Country_Subdivision_Cd CHAR(3) NULL 
		TITLE 'ISO 3166 Country Subdivision Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ISO_3166_COUNTRY_SUBDIVISION_STANDARD
	 (
			Territory_Id
	 );
```

#### POSTAL_CODE

```sql
CREATE  TABLE CORE_DB.POSTAL_CODE
(

	Postal_Code_Id       INTEGER NOT NULL 
		TITLE 'Postal Code Id',
	County_Id            INTEGER NULL 
		TITLE 'County Id',
	Country_Id           INTEGER NOT NULL 
		TITLE 'Country Id',
	Postal_Code_Num      VARCHAR(50) NULL 
		TITLE 'Postal Code Num',
	Time_Zone_Cd         VARCHAR(50) NULL 
		TITLE 'Time Zone Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_POSTAL_CODE
	 (
			Postal_Code_Id
	 );
```

#### CITY

```sql
CREATE  TABLE CORE_DB.CITY
(

	City_Id              INTEGER NOT NULL 
		TITLE 'City Id',
	City_Type_Cd         VARCHAR(50) NULL 
		TITLE 'City Type Cd',
	Territory_Id         INTEGER NULL 
		TITLE 'Territory Id',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_CITY
	 (
			City_Id
	 );
```

#### GEOGRAPHICAL_AREA

```sql
CREATE  TABLE CORE_DB.GEOGRAPHICAL_AREA
(

	Geographical_Area_Id INTEGER NOT NULL 
		TITLE 'Geographical Area Id',
	Geographical_Area_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Geographical Area Subtype Cd',
	Geographical_Area_Short_Name VARCHAR(100) NULL 
		TITLE 'Geographical Area Short Name',
	Geographical_Area_Name VARCHAR(100) NULL 
		TITLE 'Geographical Area Name',
	Geographical_Area_Desc VARCHAR(250) NULL 
		TITLE 'Geographical Area Desc',
	Geographical_Area_Start_Dt DATE NULL 
		TITLE 'Geographical Area Start Dt',
	Geographical_Area_End_Dt DATE NULL 
		TITLE 'Geographical Area End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_GEOGRAPHICAL_AREA
	 (
			Geographical_Area_Id
	 );
```

#### GEOGRAPHICAL_AREA_CURRENCY

```sql
CREATE  TABLE CORE_DB.GEOGRAPHICAL_AREA_CURRENCY
(

	Geographical_Area_Id INTEGER NOT NULL 
		TITLE 'Geographical Area Id',
	Currency_Cd          VARCHAR(50) NOT NULL 
		TITLE 'Currency Cd',
	Geographical_Area_Currency_Start_Dt DATE NOT NULL 
		TITLE 'Geographical Area Currency Start Dt',
	Geographical_Area_Currency_Role_Cd VARCHAR(50) NOT NULL 
		TITLE 'Geographical Area Currency Role Cd',
	Geographical_Area_Currency_End_Dt DATE NULL 
		TITLE 'Geographical Area Currency End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_GEOGRAPHICAL_AREA_CURRENCY
	 (
			Geographical_Area_Id
	 );
```

#### CITY_TYPE

```sql
CREATE  TABLE CORE_DB.CITY_TYPE
(

	City_Type_Cd         VARCHAR(50) NOT NULL 
		TITLE 'City Type Cd',
	City_Type_Desc       VARCHAR(250) NULL 
		TITLE 'City Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CITY_TYPE
	 (
			City_Type_Cd
	 );
```

#### COUNTRY

```sql
CREATE  TABLE CORE_DB.COUNTRY
(

	Country_Id           INTEGER NOT NULL 
		TITLE 'Country Id',
	Calendar_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Calendar Type Cd',
	Country_Group_Id     INTEGER NULL 
		TITLE 'Country Group Id',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_COUNTRY
	 (
			Country_Id
	 );
```

#### CALENDAR_TYPE

```sql
CREATE  TABLE CORE_DB.CALENDAR_TYPE
(

	Calendar_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Calendar Type Cd',
	Calendar_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Calendar Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_CALENDAR_TYPE
	 (
			Calendar_Type_Cd
	 );
```

#### ISO_3166_COUNTRY_STANDARD

```sql
CREATE  TABLE CORE_DB.ISO_3166_COUNTRY_STANDARD
(

	Country_Id           INTEGER NOT NULL 
		TITLE 'Country Id',
	Country_Code_Standard_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Country Code Standard Type Cd',
	ISO_3166_Country_3_Num CHAR(3) NOT NULL 
		TITLE 'ISO 3166 Country-3 Num',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ISO_3166_COUNTRY_STANDARD
	 (
			ISO_3166_Country_3_Num
	 );
```

#### COUNTY

```sql
CREATE  TABLE CORE_DB.COUNTY
(

	County_Id            INTEGER NOT NULL 
		TITLE 'County Id',
	Territory_Id         INTEGER NOT NULL 
		TITLE 'Territory Id',
	MSA_Id               INTEGER NULL 
		TITLE 'MSA Id *Geo',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_COUNTY
	 (
			County_Id
	 );
```

#### PARCEL_ADDRESS

```sql
CREATE  TABLE CORE_DB.PARCEL_ADDRESS
(

	Parcel_Address_Id    INTEGER NOT NULL 
		TITLE 'Parcel Address Id',
	Page_Num             VARCHAR(50) NULL 
		TITLE 'Page Num',
	Map_Num              VARCHAR(50) NULL 
		TITLE 'Map Num',
	Parcel_Num           VARCHAR(50) NULL 
		TITLE 'Parcel Num',
	City_Id              INTEGER NULL 
		TITLE 'City Id',
	County_Id            INTEGER NULL 
		TITLE 'County Id',
	Country_Id           INTEGER NULL 
		TITLE 'Country Id',
	Postal_Code_Id       INTEGER NULL 
		TITLE 'Postal Code Id',
	Territory_Id         INTEGER NULL 
		TITLE 'Territory Id',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARCEL_ADDRESS
	 (
			Parcel_Address_Id
	 );
```

#### POST_OFFICE_BOX_ADDRESS

```sql
CREATE  TABLE CORE_DB.POST_OFFICE_BOX_ADDRESS
(

	Post_Office_Box_Id   INTEGER NOT NULL 
		TITLE 'Post Office Box Id',
	Post_Office_Box_Num  VARCHAR(50) NULL 
		TITLE 'Post Office Box Num',
	City_Id              INTEGER NULL 
		TITLE 'City Id',
	County_Id            INTEGER NULL 
		TITLE 'County Id',
	Country_Id           INTEGER NULL 
		TITLE 'Country Id',
	Postal_Code_Id       INTEGER NULL 
		TITLE 'Postal Code Id',
	Territory_Id         INTEGER NULL 
		TITLE 'Territory Id',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_POST_OFFICE_BOX_ADDRESS
	 (
			Post_Office_Box_Id
	 );
```

#### REGION

```sql
CREATE  TABLE CORE_DB.REGION
(

	Region_Id            INTEGER NOT NULL 
		TITLE 'Region Id',
	Country_Id           INTEGER NULL 
		TITLE 'Country Id',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_REGION
	 (
			Region_Id
	 );
```

#### TERRITORY

```sql
CREATE  TABLE CORE_DB.TERRITORY
(

	Territory_Id         INTEGER NOT NULL 
		TITLE 'Territory Id',
	Territory_Type_Cd    VARCHAR(50) NULL 
		TITLE 'Territory Type Cd',
	Country_Id           INTEGER NOT NULL 
		TITLE 'Country Id',
	Region_Id            INTEGER NULL 
		TITLE 'Region Id',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_TERRITORY
	 (
			Territory_Id
	 );
```

#### TERRITORY_TYPE

```sql
CREATE  TABLE CORE_DB.TERRITORY_TYPE
(

	Territory_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Territory Type Cd',
	Territory_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Territory Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_TERRITORY_TYPE
	 (
			Territory_Type_Cd
	 );
```

#### GEOSPATIAL_POINT

```sql
CREATE  TABLE CORE_DB.GEOSPATIAL_POINT
(

	Geospatial_Point_Id  INTEGER NOT NULL 
		TITLE 'Geospatial Point Id',
	Latitude_Meas        DECIMAL(18,4) NULL 
		TITLE 'Latitude Meas',
	Longitude_Meas       DECIMAL(18,4) NULL 
		TITLE 'Longitude Meas',
	Elevation_Meas       DECIMAL(18,4) NULL 
		TITLE 'Altitude Meas',
	Elevation_UOM_Cd     VARCHAR(50) NULL 
		TITLE 'Elevation UOM Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_GEOSPATIAL_POINT
	 (
			Geospatial_Point_Id
	 );
```

#### GEOSPATIAL

```sql
CREATE  TABLE CORE_DB.GEOSPATIAL
(

	Geospatial_Id        INTEGER NOT NULL 
		TITLE 'Geospatial Id',
	Geospatial_Roadway_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Geospatial Roadway Subtype Cd',
	Geospatial_Coordinates_Geosptl ST_Geometry NULL 
		TITLE 'Geospatial Coordinates Geosptl',
	Geospatial_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Geospatial Subtype Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_GEOSPATIAL
	 (
			Geospatial_Id
	 );
```

#### UNIT_OF_MEASURE_TYPE

```sql
CREATE  TABLE CORE_DB.UNIT_OF_MEASURE_TYPE
(

	Unit_Of_Measure_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Unit Of Measure Type Cd',
	Unit_Of_Measure_Type_Desc VARCHAR(250) NULL 
		TITLE 'Unit Of Measure Type Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_UNIT_OF_MEASURE_TYPE
	 (
			Unit_Of_Measure_Type_Cd
	 );
```

#### LOCATOR_RELATED

```sql
CREATE  TABLE CORE_DB.LOCATOR_RELATED
(

	Locator_Id           INTEGER NOT NULL 
		TITLE 'Locator Id',
	Related_Locator_Id   INTEGER NOT NULL 
		TITLE 'Related Locator Id',
	Locator_Related_Reason_Cd VARCHAR(50) NOT NULL 
		TITLE 'Locator Relationship Type Cd',
	Locator_Related_Start_Dt DATE NOT NULL 
		TITLE 'Locator Related Start Dt',
	Locator_Related_End_Dt DATE NULL 
		TITLE 'Locator Related End Dt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_LOCATOR_RELATED
	 (
			Locator_Id
	 );
```

#### ANALYTICAL_MODEL

```sql
CREATE  TABLE CORE_DB.ANALYTICAL_MODEL
(

	Model_Id             INTEGER NOT NULL 
		TITLE 'Model Id',
	Model_Name           VARCHAR(100) NULL 
		TITLE 'Model Name',
	Model_Desc           VARCHAR(250) NULL 
		TITLE 'Model Desc',
	Model_Version_Num    VARCHAR(50) NULL 
		TITLE 'Model Version Num',
	Model_Type_Cd        VARCHAR(50) NULL 
		TITLE 'Model Type Cd',
	Model_Algorithm_Type_Cd VARCHAR(50) NULL 
		TITLE 'Model Algorithm Type Cd',
	Data_Source_Type_Cd  VARCHAR(50) NULL 
		TITLE 'Data Source Type Cd',
	Model_From_Dttm      TIMESTAMP NULL 
		TITLE 'Model From Dttm',
	Model_To_Dttm        TIMESTAMP NULL 
		TITLE 'Model To Dttm',
	Model_Predict_Time_Period_Cnt INTEGER NULL 
		TITLE 'Model Predict Time Period Cnt',
	Model_Predict_Time_Period_Cd VARCHAR(50) NULL 
		TITLE 'Model Predict Time Period Cd',
	Model_Purpose_Cd     VARCHAR(50) NULL 
		TITLE 'Model Purpose Cd',
	Attestation_Ind      CHAR(3) NULL 
		TITLE 'Attestation Ind',
	Model_Target_Run_Dt  DATE NULL 
		TITLE 'Model Target Run Dt',
	Locator_Id           INTEGER NULL 
		TITLE 'Locator Id',
	Criticality_Type_Cd  VARCHAR(50) NULL 
		TITLE 'Criticality Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ANALYTICAL_MODEL
	 (
			Model_Id
	 );
```

#### PARTY_DEMOGRAPHIC

```sql
CREATE  TABLE CORE_DB.PARTY_DEMOGRAPHIC
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Demographic_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Demographic Cd',
	Data_Source_Type_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Data Source Type Cd',
	Party_Demographic_Start_Dt DATE NOT NULL 
		TITLE 'Party Demographic Start Dt',
	Demographic_Value_Cd VARCHAR(50) NOT NULL 
		TITLE 'Demographic Value Cd',
	Party_Demographic_End_Dt DATE NULL 
		TITLE 'Party Demographic End Dt',
	Party_Demographic_Num VARCHAR(50) NULL 
		TITLE 'Party Demographic Num',
	Party_Demographic_Val VARCHAR(100) NULL 
		TITLE 'Party Demographic Val',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_DEMOGRAPHIC
	 (
			Party_Id
	 );
```

#### PARTY

```sql
CREATE  TABLE CORE_DB.PARTY
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Party_Subtype_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Party Subtype Cd',
	Party_Desc           VARCHAR(250) NULL 
		TITLE 'Party Desc',
	Party_Start_Dttm     TIMESTAMP NULL 
		TITLE 'Party Start Dttm',
	Party_End_Dttm       TIMESTAMP NULL 
		TITLE 'Party End Dttm',
	Party_Type_Cd        VARCHAR(50) NOT NULL 
		TITLE 'Party Type Cd',
	Initial_Data_Source_Type_Cd VARCHAR(50) NULL 
		TITLE 'Initial Data Source Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY
	 (
			Party_Id
	 );
```

#### HOUSEHOLD

```sql
CREATE  TABLE CORE_DB.HOUSEHOLD
(

	Household_Party_Id   INTEGER NOT NULL 
		TITLE 'Household Party Id',
	Party_Household_Child_Cnt INTEGER NULL 
		TITLE 'Party Household Child Cnt',
	Party_Household_Cnt  INTEGER NULL 
		TITLE 'Party Household Cnt',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_HOUSEHOLD
	 (
			Household_Party_Id
	 );
```

#### DEMOGRAPHIC_VALUE

```sql
CREATE  TABLE CORE_DB.DEMOGRAPHIC_VALUE
(

	Demographic_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Demographic Cd',
	Demographic_Value_Cd VARCHAR(50) NOT NULL 
		TITLE 'Demographic Value Cd',
	Demographic_Range_Start_Val VARCHAR(100) NULL 
		TITLE 'Demographic Range Start Val',
	Demographic_Range_End_Val VARCHAR(100) NULL 
		TITLE 'Demographic Range End Val',
	Demographic_Value_Desc VARCHAR(250) NULL 
		TITLE 'Demographic Value Desc',
	Demographic_Val      VARCHAR(100) NULL 
		TITLE 'Demographic Val',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_DEMOGRAPHIC_VALUE
	 (
			Demographic_Cd
	 );
```

#### PARTY_LOCATOR

```sql
CREATE  TABLE CORE_DB.PARTY_LOCATOR
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Locator_Id           INTEGER NOT NULL 
		TITLE 'Locator Id',
	Locator_Usage_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Locator Usage Type Cd',
	Party_Locator_Start_Dttm DATE NOT NULL 
		TITLE 'Party Locator Start Dttm',
	Party_Locator_End_Dttm DATE NULL 
		TITLE 'Party Locator End Dttm',
	Data_Quality_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Data Quality Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_LOCATOR
	 (
			Party_Id
	 );
```

#### ELECTRONIC_ADDRESS

```sql
CREATE  TABLE CORE_DB.ELECTRONIC_ADDRESS
(

	Electronic_Address_Id INTEGER NOT NULL 
		TITLE 'Electronic Address Id',
	Electronic_Address_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Electronic Address Subtype Cd',
	Electronic_Address_Txt VARCHAR(1000) NULL 
		TITLE 'Electronic Address Txt',
	Electronic_Address_Domain_Name VARCHAR(100) NULL 
		TITLE 'Electronic Address Domain Name',
	Domain_Root_Cd       VARCHAR(50) NULL 
		TITLE 'Domain Root Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_ELECTRONIC_ADDRESS
	 (
			Electronic_Address_Id
	 );
```

#### ELECTRONIC_ADDRESS_SUBTYPE

```sql
CREATE  TABLE CORE_DB.ELECTRONIC_ADDRESS_SUBTYPE
(

	Electronic_Address_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Electronic Address Subtype Cd',
	Electronic_Address_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Electronic Address Subtype Desc',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	 UNIQUE PRIMARY INDEX UPI_ELECTRONIC_ADDRESS_SUBTYPE
	 (
			Electronic_Address_Subtype_Cd
	 );
```

#### INTERNET_PROTOCOL_ADDRESS

```sql
CREATE  TABLE CORE_DB.INTERNET_PROTOCOL_ADDRESS
(

	Internet_Protocol_Address_Id INTEGER NOT NULL 
		TITLE 'Internet Protocol Address Id',
	Internet_Protocol_Address_Num VARCHAR(50) NOT NULL 
		TITLE 'Internet Protocol Address Num',
	Internet_Protocol_Registered_By_Party_Id INTEGER NULL 
		TITLE 'Internet Protocol Registered By Party Id',
	Internet_Protocol_Network_Name VARCHAR(100) NULL 
		TITLE 'Internet Protocol Network Name',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_INTERNET_PROTOCOL_ADDRESS
	 (
			Internet_Protocol_Address_Id
	 );
```

#### TELEPHONE_NUMBER

```sql
CREATE  TABLE CORE_DB.TELEPHONE_NUMBER
(

	Telephone_Number_Id  INTEGER NOT NULL 
		TITLE 'Telephone Number Id',
	Telephone_Num        VARCHAR(50) NULL 
		TITLE 'Telephone Num DD',
	Telephone_Country_Code_Num VARCHAR(50) NULL 
		TITLE 'Telephone Country Cd',
	Telephone_Area_Code_Num VARCHAR(50) NULL 
		TITLE 'Telephone Area Cd',
	Telephone_Exchange_Num VARCHAR(50) NULL 
		TITLE 'Telephone Exchange Num',
	Telephone_Line_Num   VARCHAR(50) NULL 
		TITLE 'Telephone Line Num',
	Telephone_Extension_Num VARCHAR(50) NULL 
		TITLE 'Telephone Extension Num',
	Telephone_Number_Type_Cd VARCHAR(50) NULL 
		TITLE 'Telephone Number Type Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_TELEPHONE_NUMBER
	 (
			Telephone_Number_Id
	 );
```

#### PARTY_TASK

```sql
CREATE TABLE CORE_DB.PARTY_TASK
(
    Task_Id                  BIGINT       NOT NULL,
    Party_Id                 BIGINT,
    Source_Event_Id          BIGINT,
    Task_Activity_Type_Cd    SMALLINT     NOT NULL,
    Task_Subtype_Cd          SMALLINT     NOT NULL,
    Task_Reason_Cd           SMALLINT     NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Task_Id);
```

#### TASK_ACTIVITY

```sql
CREATE TABLE CORE_DB.TASK_ACTIVITY
(
    Activity_Id              BIGINT          NOT NULL,
    Task_Id                  BIGINT,
    Activity_Type_Cd         SMALLINT        NOT NULL,
    Activity_Txt             VARCHAR(32000),
    Activity_Channel_Id      BIGINT,
    Activity_Start_Dttm      TIMESTAMP       NOT NULL,
    Activity_End_Dttm        TIMESTAMP       NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Activity_Id);
```

#### PARTY_ADDRESS

```sql
CREATE  TABLE CORE_DB.PARTY_ADDRESS
(

	Party_Address_Usage_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Party Address Usage Type Cd',
	Address_Id           INTEGER NOT NULL 
		TITLE 'Address Id',
	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Party_Address_Start_Dt DATE NOT NULL 
		TITLE 'Party Address Start Dt',
	Party_Address_End_Dt DATE NULL 
		TITLE 'Party Address End Dt',
	Default_Ind          CHAR(3) NULL 
		TITLE 'Default Ind',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_ADDRESS
	 (
			Party_Id
	 );
```

#### PRODUCT_TO_GROUP

```sql
CREATE TABLE CORE_DB.PRODUCT_TO_GROUP (
    PIM_Id BIGINT NOT NULL,
    Group_Id BIGINT NOT NULL,
    Valid_From_Dt DATE NOT NULL,
    Valid_To_Dt DATE NOT NULL,
    Del_Ind CHAR(1) NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (PIM_Id);
```

### CDM_DB

#### PARTY

```sql
CREATE MULTISET TABLE CDM_DB.PARTY
(
     Source_Cd                 SMALLINT        NOT NULL
    ,CDM_Party_Id              BIGINT          NOT NULL
    ,Source_Party_Id           BIGINT          NOT NULL
    ,Party_Type_Cd             SMALLINT        NOT NULL
    ,Party_Lifecycle_Phase_Cd  SMALLINT        NOT NULL
    ,Party_Since               DATE            NOT NULL
    ,Valid_From_Dt             DATE            NOT NULL
    ,Valid_To_Dt               DATE            NOT NULL
    ,Del_Ind                   CHAR(1)         NOT NULL
    ,Survival_Record_Ind       CHAR(1)         NOT NULL
    ,DQ_Score                  DECIMAL(5,2) NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id);
```

#### ORGANIZATION

```sql
CREATE MULTISET TABLE CDM_DB.ORGANIZATION
(
     CDM_Party_Id          BIGINT          NOT NULL
    ,Organization_Name     VARCHAR(255)
    ,Business_Identifier   VARCHAR(255)
    ,Valid_From_Dt         DATE            NOT NULL
    ,Valid_To_Dt           DATE            NOT NULL
    ,Del_Ind               CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id);
```

#### INDIVIDUAL

```sql
CREATE MULTISET TABLE CDM_DB.INDIVIDUAL
(
     CDM_Party_Id      BIGINT          NOT NULL
    ,First_Name        VARCHAR(255)
    ,Middle_Name       VARCHAR(255)
    ,Last_Name         VARCHAR(255)
    ,Birth_Dt          DATE            NOT NULL
    ,Gender            VARCHAR(50)
    ,Salutation        VARCHAR(50)
    ,Valid_From_Dt     DATE            NOT NULL
    ,Valid_To_Dt       DATE            NOT NULL
    ,DQ_Score                  DECIMAL(5,2)
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id);
```

#### INDIVIDUAL_TO_INDIVIDUAL

```sql
CREATE MULTISET TABLE CDM_DB.INDIVIDUAL_TO_INDIVIDUAL
(
     CDM_Party_Id              BIGINT          NOT NULL
    ,Parent_CDM_Party_Id       BIGINT          NOT NULL
    ,Relationship_Type_Cd      SMALLINT        NOT NULL
    ,Relationship_Value_Cd     SMALLINT        NOT NULL
    ,Probability               DECIMAL(5,4)
    ,Valid_From_Dt             DATE            NOT NULL
    ,Valid_To_Dt               DATE            NOT NULL
    ,Del_Ind                   CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id, Parent_CDM_Party_Id);
```

#### INDIVIDUAL_TO_HOUSEHOLD

```sql
CREATE MULTISET TABLE CDM_DB.INDIVIDUAL_TO_HOUSEHOLD
(
     CDM_Party_Id          BIGINT          NOT NULL
    ,CDM_Household_Id      BIGINT          NOT NULL
    ,Role_Type_Cd          SMALLINT        NOT NULL
    ,Probability           DECIMAL(5,4)
    ,Valid_From_Dt         DATE            NOT NULL
    ,Valid_To_Dt           DATE            NOT NULL
    ,Del_Ind               CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id, CDM_Household_Id);
```

#### HOUSEHOLD

```sql
CREATE MULTISET TABLE CDM_DB.HOUSEHOLD
(
     CDM_Household_Id      BIGINT          NOT NULL
    ,Household_Name        VARCHAR(255)
    ,Household_Desc        VARCHAR(255)
    ,Valid_From_Dt         DATE            NOT NULL
    ,Valid_To_Dt           DATE            NOT NULL
    ,Del_Ind               CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Household_Id);
```

#### INDIVIDUAL_TO_ORGANIZATION

```sql
CREATE MULTISET TABLE CDM_DB.INDIVIDUAL_TO_ORGANIZATION
(
     CDM_Party_Id              BIGINT          NOT NULL
    ,Parent_CDM_Party_Id       BIGINT          NOT NULL
    ,Relationship_Type_Cd      SMALLINT        NOT NULL
    ,Relationship_Value_Cd     SMALLINT        NOT NULL
    ,Probability               DECIMAL(5,4)
    ,Valid_From_Dt             DATE            NOT NULL
    ,Valid_To_Dt               DATE            NOT NULL
    ,Del_Ind                   CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id, Parent_CDM_Party_Id);
```

#### ORGANIZATION_TO_ORGANIZATION

```sql
CREATE MULTISET TABLE CDM_DB.ORGANIZATION_TO_ORGANIZATION
(
     CDM_Party_Id              BIGINT          NOT NULL
    ,Parent_CDM_Party_Id       BIGINT          NOT NULL
    ,Relationship_Type_Cd      SMALLINT        NOT NULL
    ,Relationship_Value_Cd     SMALLINT        NOT NULL
    ,Probability               DECIMAL(5,4)
    ,Valid_From_Dt             DATE            NOT NULL
    ,Valid_To_Dt               DATE            NOT NULL
    ,Del_Ind                   CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id, Parent_CDM_Party_Id);
```

#### PARTY_TO_AGREEMENT_ROLE

```sql
CREATE MULTISET TABLE CDM_DB.PARTY_TO_AGREEMENT_ROLE
(
     CDM_Party_Id      BIGINT          NOT NULL
    ,Agreement_Id      BIGINT          NOT NULL
    ,Role_Type_Cd      SMALLINT        NOT NULL
    ,Valid_From_Dt     DATE            NOT NULL
    ,Valid_To_Dt       DATE            NOT NULL
    ,Del_Ind           CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id, Agreement_Id);
```

#### PARTY_TO_EVENT_ROLE

```sql
CREATE MULTISET TABLE CDM_DB.PARTY_TO_EVENT_ROLE
(
     CDM_Party_Id      BIGINT          NOT NULL
    ,Event_Id          BIGINT          NOT NULL
    ,Role_Type_Cd      SMALLINT        NOT NULL
    ,Valid_From_Dt     DATE            NOT NULL
    ,Valid_To_Dt       DATE            NOT NULL
    ,Del_Ind           CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id, Event_Id);
```

#### PARTY_SEGMENT

```sql
CREATE MULTISET TABLE CDM_DB.PARTY_SEGMENT
(
     CDM_Party_Id          BIGINT          NOT NULL
    ,Segment_Type_Cd       SMALLINT        NOT NULL
    ,Segment_Value_Cd      SMALLINT        NOT NULL
    ,Valid_From_Dt         DATE            NOT NULL
    ,Valid_To_Dt           DATE            NOT NULL
    ,Del_Ind               CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (CDM_Party_Id);
```

#### ADDRESS_TO_AGREEMENT

```sql
CREATE MULTISET TABLE CDM_DB.ADDRESS_TO_AGREEMENT
(
    Address_Id                BIGINT          NOT NULL
    ,Agreement_Id              BIGINT          NOT NULL
    ,Valid_From_Dt             DATE            NOT NULL
    ,Valid_To_Dt               DATE            NOT NULL
    ,Del_Ind                   CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Address_Id, Agreement_Id);
```

#### PARTY_CONTACT

```sql
CREATE MULTISET TABLE CDM_DB.CONTACT
(
     Contact_Id             BIGINT          NOT NULL
    ,Contact_Type_Cd        SMALLINT        NOT NULL
    ,Contact_Value          VARCHAR(255)
    ,Primary_Contact_Ind    CHAR(1)         NOT NULL
    ,Valid_From_Dt          DATE            NOT NULL
    ,Valid_To_Dt            DATE            NOT NULL
    ,Del_Ind                CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Contact_Id);
```

#### CONTACT_TO_AGREEMENT

```sql
CREATE MULTISET TABLE CDM_DB.CONTACT_TO_AGREEMENT
(
     Contact_Id        BIGINT          NOT NULL
    ,Agreement_Id      BIGINT          NOT NULL
    ,Valid_From_Dt     DATE            NOT NULL
    ,Valid_To_Dt       DATE            NOT NULL
    ,Del_Ind           CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Contact_Id, Agreement_Id);
```

#### PARTY_INTERRACTION_EVENT

```sql
CREATE MULTISET TABLE CDM_DB.PARTY_INTERRACTION_EVENT
(
     Event_Id                  BIGINT          NOT NULL
    ,CDM_Party_Id              BIGINT          NOT NULL
    ,Event_Type_Cd             SMALLINT        NOT NULL
    ,Event_Channel_Type_Cd     SMALLINT        NOT NULL
    ,Event_Dt                  DATE            NOT NULL
    ,Event_Sentiment_Cd        SMALLINT        NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Event_Id);
```

#### ADDRESS

```sql
CREATE MULTISET TABLE CDM_DB.ADDRESS
(
     Address_Id                BIGINT          NOT NULL
    ,Address_Type              VARCHAR(255)
    ,Address_Country_Cd        SMALLINT        NOT NULL
    ,Address_County            VARCHAR(255)
    ,Address_City              VARCHAR(255)
    ,Address_Street            VARCHAR(255)
    ,Address_Postal_Code       VARCHAR(20)
    ,Primary_Address_Flag      CHAR(1)
    ,Geo_Latitude              DECIMAL(9,6)
    ,Geo_Longitude             DECIMAL(9,6)
    ,Valid_From_Dt             DATE            NOT NULL
    ,Valid_To_Dt               DATE            NOT NULL
    ,Del_Ind                   CHAR(1)         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Address_Id);
```

### PIM_DB

#### PRODUCT_TO_GROUP

```sql
CREATE TABLE PIM_DB.PRODUCT_TO_GROUP (
    PIM_Id BIGINT NOT NULL,
    Group_Id BIGINT NOT NULL,
    Valid_From_Dt DATE NOT NULL,
    Valid_To_Dt DATE NOT NULL,
    Del_Ind CHAR(1) NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (PIM_Id);
```

#### PRODUCT

```sql
CREATE TABLE PIM_DB.PRODUCT (
    PIM_Id BIGINT NOT NULL,
    Product_Id BIGINT NOT NULL,
    PIM_Product_Name VARCHAR(255),
    PIM_Product_Desc VARCHAR(32000),
    Valid_From_Dt DATE NOT NULL,
    Valid_To_Dt DATE NOT NULL,
    Del_Ind CHAR(1) NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (PIM_Id);
```

#### PRODUCT_PARAMETERS

```sql
CREATE TABLE PIM_DB.PRODUCT_PARAMETERS (
    PIM_Parameter_Id BIGINT NOT NULL,
    PIM_Id BIGINT NOT NULL,
    PIM_Parameter_Type_Cd SMALLINT NOT NULL,
    PIM_Parameter_Value VARCHAR(1000),
    Valid_From_Dt DATE NOT NULL,
    Valid_To_Dt DATE NOT NULL,
    Del_Ind CHAR(1) NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (PIM_Parameter_Id);
```

#### PRODUCT_PARAMETER_TYPE

```sql
CREATE TABLE PIM_DB.PRODUCT_PARAMETER_TYPE (
    PIM_Parameter_Type_Cd SMALLINT NOT NULL,
    PIM_Parameter_Type_Desc VARCHAR(255),
    Valid_From_Dt DATE NOT NULL,
    Valid_To_Dt DATE NOT NULL,
    Del_Ind CHAR(1) NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (PIM_Parameter_Type_Cd);
```

#### PRODUCT_GROUP

```sql
CREATE TABLE PIM_DB.PRODUCT_GROUP (
    Product_Group_Id BIGINT NOT NULL,
    Parent_Group_Id BIGINT NOT NULL,
    Product_Group_Type_Cd SMALLINT NOT NULL,
    Valid_From_Dt DATE NOT NULL,
    Valid_To_Dt DATE NOT NULL,
    Del_Ind CHAR(1) NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Product_Group_Id);
```

#### PRODUCT_GROUP_TYPE

```sql
CREATE TABLE PIM_DB.PRODUCT_GROUP_TYPE (
    Product_Group_Type_Cd SMALLINT NOT NULL,
    Product_Group_Type_Name VARCHAR(255),
    Product_Group_Type_Desc VARCHAR(1000),
    Valid_From_Dt DATE NOT NULL,
    Valid_To_Dt DATE NOT NULL,
    Del_Ind CHAR(1) NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Product_Group_Type_Cd);
```

### UNKNOWN

#### PARTY_ADDRESS

```sql
CREATE  TABLE CORE_DB.PARTY_ADDRESS
(

	Party_Address_Usage_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Party Address Usage Type Cd',
	Address_Id           INTEGER NOT NULL 
		TITLE 'Address Id',
	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Party_Address_Start_Dt DATE NOT NULL 
		TITLE 'Party Address Start Dt',
	Party_Address_End_Dt DATE NULL 
		TITLE 'Party Address End Dt',
	Default_Ind          CHAR(3) NULL 
		TITLE 'Default Ind',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind'
)
	PRIMARY INDEX NUPI_PARTY_ADDRESS
	 (
			Party_Id
	 );
```

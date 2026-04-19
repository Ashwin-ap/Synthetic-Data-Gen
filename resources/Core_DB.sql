CREATE  TABLE  Core_DB.AGREEMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_AGREEMENT
	 (
			Agreement_Id
	 );


CREATE  TABLE  Core_DB.AGREEMENT_SUBTYPE
(

	Agreement_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Subtype Cd',
	Agreement_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_SUBTYPE
	 (
			Agreement_Subtype_Cd
	 );
	 

CREATE  TABLE  Core_DB.AGREEMENT_FORMAT_TYPE
(

	Agreement_Format_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Format Type Cd',
	Agreement_Format_Type_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Format Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_FORMAT_TYPE
	 (
			Agreement_Format_Type_Cd
	 );
	 

CREATE  TABLE  Core_DB.AGREEMENT_OBJECTIVE_TYPE
(

	Agreement_Objective_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Objective Type Cd',
	Agreement_Objective_Type_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Objective Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_OBJECTIVE_TYPE
	 (
			Agreement_Objective_Type_Cd
	 );
	 

CREATE  TABLE  Core_DB.AGREEMENT_OBTAINED_TYPE
(

	Agreement_Obtained_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Obtained Cd',
	Agreement_Obtained_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Obtained Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_OBTAINED_TYPE
	 (
			Agreement_Obtained_Cd
	 );
	 

CREATE  TABLE  Core_DB.AGREEMENT_TYPE
(

	Agreement_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Agreement Type Cd',
	Agreement_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Agreement Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_TYPE
	 (
			Agreement_Type_Cd
	 );


	 
CREATE  TABLE  Core_DB.ASSET_LIABILITY_TYPE
(

	Asset_Liability_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Asset Liability Cd',
	Asset_Liability_Desc VARCHAR(250) NULL 
		TITLE 'Asset Liability Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_ASSET_LIABILITY_TYPE
	 (
			Asset_Liability_Cd
	 );


	 
CREATE  TABLE  Core_DB.BALANCE_SHEET_TYPE
(

	Balance_Sheet_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Balance Sheet Cd',
	Balance_Sheet_Desc   VARCHAR(250) NULL 
		TITLE 'Balance Sheet Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_BALANCE_SHEET_TYPE
	 (
			Balance_Sheet_Cd
	 );
	 


CREATE  TABLE  Core_DB.DOCUMENT_PRODUCTION_CYCLE_TYPE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_DOCUMENT_PRODUCTION_CYCLE_TYPE
	 (
			Document_Production_Cycle_Cd
	 );
	 

	 
CREATE  TABLE  Core_DB.STATEMENT_MAIL_TYPE
(

	Statement_Mail_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Statement Mail Type Cd',
	Statement_Mail_Type_Desc VARCHAR(250) NULL 
		TITLE 'Statement Mail Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_STATEMENT_MAIL_TYPE
	 (
			Statement_Mail_Type_Cd
	 );
	 

CREATE  TABLE  Core_DB.DATA_SOURCE_TYPE
(

	Data_Source_Type_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Data Source Type Cd',
	Data_Source_Type_Desc VARCHAR(250) NULL 
		TITLE 'Data Source Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_DATA_SOURCE_TYPE
	 (
			Data_Source_Type_Cd
	 );
	 


CREATE  TABLE  Core_DB.AGREEMENT_CURRENCY
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_AGREEMENT_CURRENCY
	 (
			Agreement_Id
	 );
	 


CREATE  TABLE  Core_DB.CURRENCY
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_CURRENCY
	 (
			Currency_Cd
	 );
	 


CREATE  TABLE  Core_DB.AGREEMENT_SCORE
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Model_Id             INTEGER NOT NULL 
		TITLE 'Model Id',
	Model_Run_Id         INTEGER NOT NULL 
		TITLE 'Model Run Id',
	Agreement_Score_Val  VARCHAR(100) NOT NULL 
		TITLE 'Agreement Score Val',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_AGREEMENT_SCORE
	 (
			Agreement_Id
	 );
	 


CREATE  TABLE  Core_DB.PARTY_AGREEMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_AGREEMENT
	 (
			Agreement_Id
	 );



CREATE  TABLE  Core_DB.PRODUCT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PRODUCT
	 (
			Product_Id
	 );

	 

CREATE  TABLE  Core_DB.AGREEMENT_STATUS
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_AGREEMENT_STATUS
	 (
			Agreement_Id
	 );
	 


CREATE  TABLE  Core_DB.AGREEMENT_STATUS_TYPE
(

	Agreement_Status_Scheme_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Scheme Cd',
	Agreement_Status_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Cd',
	Agreement_Status_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Status Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_AGREEMENT_STATUS_TYPE
	 (
			Agreement_Status_Scheme_Cd
	 );

	 

CREATE  TABLE  Core_DB.AGREEMENT_STATUS_REASON_TYPE
(

	Agreement_Status_Reason_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Reason Cd',
	Agreement_Status_Reason_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Status Reason Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_STATUS_REASON_TYPE
	 (
			Agreement_Status_Reason_Cd
	 );
	 


CREATE  TABLE  Core_DB.AGREEMENT_STATUS_SCHEME_TYPE
(

	Agreement_Status_Scheme_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Status Scheme Cd',
	Agreement_Status_Scheme_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Status Scheme Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_STATUS_SCHEME_TYPE
	 (
			Agreement_Status_Scheme_Cd
	 );
	 


CREATE  TABLE  Core_DB.ADDRESS
(

	Address_Id           INTEGER NOT NULL 
		TITLE 'Address Id',
	Address_Subtype_Cd   VARCHAR(50) NULL 
		TITLE 'Locator Type Cd',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ADDRESS
	 (
			Address_Id
	 );
	 


CREATE  TABLE  Core_DB.ADDRESS_SUBTYPE
(

	Address_Subtype_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Locator Type Cd',
	Address_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Locator Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_ADDRESS_SUBTYPE
	 (
			Address_Subtype_Cd
	 );


	 
CREATE  TABLE  Core_DB.CAMPAIGN
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_CAMPAIGN
	 (
			Campaign_Id
	 );
	 

CREATE  TABLE  Core_DB.CAMPAIGN_STRATEGY_TYPE
(

	Campaign_Strategy_Cd VARCHAR(50) NOT NULL 
		TITLE 'Campaign Strategy Cd',
	Campaign_Strategy_Desc VARCHAR(250) NULL 
		TITLE 'Campaign Strategy Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_CAMPAIGN_STRATEGY_TYPE
	 (
			Campaign_Strategy_Cd
	 );
	 

CREATE  TABLE  Core_DB.CAMPAIGN_TYPE
(

	Campaign_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Campaign Type Cd',
	Campaign_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Campaign Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_CAMPAIGN_TYPE
	 (
			Campaign_Type_Cd
	 );
	 

CREATE  TABLE  Core_DB.CAMPAIGN_CLASSIFICATION
(

	Campaign_Classification_Cd VARCHAR(50) NOT NULL 
		TITLE 'Campaign Classification Cd',
	Campaign_Classification_Desc VARCHAR(250) NULL 
		TITLE 'Campaign Classification Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_CAMPAIGN_CLASSIFICATION
	 (
			Campaign_Classification_Cd
	 );

	 

CREATE  TABLE  Core_DB.CAMPAIGN_STATUS
(

	Campaign_Id          INTEGER NOT NULL 
		TITLE 'Campaign Id',
	Campaign_Status_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Campaign Status Start Dttm',
	Campaign_Status_Cd   VARCHAR(50) NULL 
		TITLE 'Campaign Status Cd',
	Campaign_Status_End_Dttm TIMESTAMP NULL 
		TITLE 'Campaign Status End Dttm',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_CAMPAIGN_STATUS
	 (
			Campaign_Id
	 );



CREATE  TABLE  Core_DB.CAMPAIGN_STATUS_TYPE
(

	Campaign_Status_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Campaign Status Cd',
	Campaign_Status_Desc VARCHAR(250) NULL 
		TITLE 'Campaign Status Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_CAMPAIGN_STATUS_TYPE
	 (
			Campaign_Status_Cd
	 );
	 
	 
	 
CREATE  TABLE  Core_DB.CHANNEL_INSTANCE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_CHANNEL_INSTANCE
	 (
			Channel_Instance_Id
	 );
	 


CREATE  TABLE  Core_DB.CHANNEL_TYPE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_CHANNEL_TYPE
	 (
			Channel_Type_Cd
	 );
	 
	 
CREATE  TABLE  Core_DB.CHANNEL_INSTANCE_SUBTYPE
(

	Channel_Instance_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Alternate Channel Type Cd',
	Channel_Instance_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Alternate Channel Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_CHANNEL_INSTANCE_SUBTYPE
	 (
			Channel_Instance_Subtype_Cd
	 );
	 


CREATE  TABLE  Core_DB.CONVENIENCE_FACTOR_TYPE
(

	Convenience_Factor_Cd VARCHAR(50) NOT NULL 
		TITLE 'Convenience Factor Cd',
	Convenience_Factor_Desc VARCHAR(250) NULL 
		TITLE 'Convenience Factor Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_CONVENIENCE_FACTOR_TYPE
	 (
			Convenience_Factor_Cd
	 );
	 


CREATE  TABLE  Core_DB.CHANNEL_INSTANCE_STATUS
(

	Channel_Instance_Id  INTEGER NOT NULL 
		TITLE 'Channel Instance Id',
	Channel_Instance_Status_Start_Dttm TIMESTAMP NOT NULL 
		TITLE 'Channel Instance Status Start Dttm',
	Channel_Status_Cd    VARCHAR(50) NULL 
		TITLE 'Channel Status Cd',
	Channel_Instance_Status_End_Dttm TIMESTAMP NULL 
		TITLE 'Channel Instance Status End Dttm',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_CHANNEL_INSTANCE_STATUS
	 (
			Channel_Instance_Id
	 );
	 


CREATE  TABLE  Core_DB.CARD
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_CARD
	 (
			Access_Device_Id
	 );
	 
	 

CREATE  TABLE  Core_DB.AGREEMENT_FEATURE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_AGREEMENT_FEATURE
	 (
			Agreement_Id
	 );
	 
	 


CREATE  TABLE  Core_DB.AGREEMENT_FEATURE_ROLE_TYPE
(

	Agreement_Feature_Role_Cd VARCHAR(50) NOT NULL 
		TITLE 'Agreement Feature Role Cd',
	Agreement_Feature_Role_Desc VARCHAR(250) NULL 
		TITLE 'Agreement Feature Role Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_AGREEMENT_FEATURE_ROLE_TYPE
	 (
			Agreement_Feature_Role_Cd
	 );
	 


CREATE  TABLE  Core_DB.AGREEMENT_RATE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_AGREEMENT_RATE
	 (
			Agreement_Id
	 );



CREATE  TABLE  Core_DB.FINANCIAL_AGREEMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_FINANCIAL_AGREEMENT
	 (
			Agreement_Id
	 );



CREATE  TABLE  Core_DB.MARKET_RISK_TYPE
(

	Market_Risk_Type_Cd  VARCHAR(50) NOT NULL 
		TITLE 'Market Risk Type Cd',
	Market_Risk_Type_Desc VARCHAR(250) NULL 
		TITLE 'Market Risk Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_MARKET_RISK_TYPE
	 (
			Market_Risk_Type_Cd
	 );
	 

CREATE  TABLE  Core_DB.TRADING_BOOK_TYPE
(

	Trading_Book_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Trading Book Cd',
	Trading_Book_Desc    VARCHAR(250) NULL 
		TITLE 'Trading Book Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_TRADING_BOOK_TYPE
	 (
			Trading_Book_Cd
	 );
	 

CREATE  TABLE  Core_DB.DAY_COUNT_BASIS_TYPE
(

	Day_Count_Basis_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Day Count Basis Cd',
	Day_Count_Basis_Desc VARCHAR(250) NULL 
		TITLE 'Day Count Basis Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_DAY_COUNT_BASIS_TYPE
	 (
			Day_Count_Basis_Cd
	 );
	 
	 

CREATE  TABLE  Core_DB.DEPOSIT_AGREEMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_DEPOSIT_AGREEMENT
	 (
			Agreement_Id
	 );
	 

CREATE  TABLE  Core_DB.DEPOSIT_MATURITY_SUBTYPE
(

	Deposit_Maturity_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Deposit Maturity Subtype Cd',
	Deposit_Maturity_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Deposit Maturity Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_DEPOSIT_MATURITY_SUBTYPE
	 (
			Deposit_Maturity_Subtype_Cd
	 );
	 
	 

CREATE  TABLE  Core_DB.INTEREST_DISBURSEMENT_TYPE
(

	Interest_Disbursement_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Interest Disbursement Type Cd',
	Interest_Disbursement_Type_Desc VARCHAR(250) NULL 
		TITLE 'Interest Disbursement Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_INTEREST_DISBURSEMENT_TYPE
	 (
			Interest_Disbursement_Type_Cd
	 );
	 
	 


CREATE  TABLE  Core_DB.DEPOSIT_TERM_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Next_Term_Maturity_Dt DATE NULL 
		TITLE 'Next Term Maturity Dt',
	Grace_Period_End_Dt  DATE NULL 
		TITLE 'Grace Period End Dt',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_DEPOSIT_TERM_AGREEMENT
	 (
			Agreement_Id
	 );
	 



CREATE  TABLE  Core_DB.FEATURE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_FEATURE
	 (
			Feature_Id
	 );
	 


CREATE  TABLE  Core_DB.FEATURE_SUBTYPE
(

	Feature_Subtype_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Feature Subtype Cd',
	Feature_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Feature Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_FEATURE_SUBTYPE
	 (
			Feature_Subtype_Cd
	 );
	 


CREATE  TABLE  Core_DB.FEATURE_INSURANCE_SUBTYPE
(

	Feature_Insurance_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Feature Insurance Subtype Cd',
	Feature_Insurance_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Feature Insurance Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_FEATURE_INSURANCE_SUBTYPE
	 (
			Feature_Insurance_Subtype_Cd
	 );
	 


CREATE  TABLE  Core_DB.FEATURE_CLASSIFICATION_TYPE
(

	Feature_Classification_Cd VARCHAR(50) NOT NULL 
		TITLE 'Feature Classification Cd',
	Feature_Classification_Desc VARCHAR(250) NULL 
		TITLE 'Feature Classification Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_FEATURE_CLASSIFICATION_TYPE
	 (
			Feature_Classification_Cd
	 );
	 


CREATE  TABLE  Core_DB.INDIVIDUAL
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL
	 (
			Individual_Party_Id
	 );
	 
	 

CREATE  TABLE  Core_DB.INDIVIDUAL_NAME
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_NAME
	 (
			Individual_Party_Id
	 );




CREATE  TABLE  Core_DB.INDIVIDUAL_GENDER_PRONOUN
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_GENDER_PRONOUN
	 (
			Individual_Party_Id
	 );
	 


CREATE  TABLE  Core_DB.INDIVIDUAL_MARITAL_STATUS
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Individual_Marital_Status_Start_Dt DATE NOT NULL 
		TITLE 'Individual Marital Status Start Dt',
	Marital_Status_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Marital Status Cd',
	Individual_Marital_Status_End_Dt DATE NULL 
		TITLE 'Individual Marital Status End Dt',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_MARITAL_STATUS
	 (
			Individual_Party_Id
	 );
	 
	 


CREATE  TABLE  Core_DB.ASSOCIATE_EMPLOYMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ASSOCIATE_EMPLOYMENT
	 (
			Associate_Party_Id
	 );
	 


CREATE  TABLE  Core_DB.INDIVIDUAL_VIP_STATUS
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Individual_VIP_Status_Start_Dt DATE NOT NULL 
		TITLE 'Individual VIP Status Start Dt',
	VIP_Type_Cd          VARCHAR(50) NOT NULL 
		TITLE 'VIP Type Cd',
	Individual_VIP_Status_End_Dt DATE NULL 
		TITLE 'Individual VIP Status End Dt',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_VIP_STATUS
	 (
			Individual_Party_Id
	 );
	 


CREATE  TABLE  Core_DB.INDIVIDUAL_MILITARY_STATUS
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Individual_Military_Start_Dt DATE NOT NULL 
		TITLE 'Individual Military Start Dt',
	Military_Status_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Military Status Type Cd',
	Individual_Military_End_Dt DATE NULL 
		TITLE 'Individual Military End Dt',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_MILITARY_STATUS
	 (
			Individual_Party_Id
	 );




CREATE  TABLE  Core_DB.INDIVIDUAL_OCCUPATION
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_OCCUPATION
	 (
			Individual_Party_Id
	 );




CREATE  TABLE  Core_DB.INDIVIDUAL_PAY_TIMING
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Business_Party_Id    INTEGER NOT NULL 
		TITLE 'Business Party Id',
	Pay_Day_Num          VARCHAR(50) NULL 
		TITLE 'Pay Day Num',
	Time_Period_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Time Period Cd',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_PAY_TIMING
	 (
			Individual_Party_Id
	 );
	 


CREATE  TABLE  Core_DB.INDIVIDUAL_BONUS_TIMING
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Bonus_Month_Num      VARCHAR(50) NOT NULL 
		TITLE 'Bonus Month Num',
	Business_Party_Id    INTEGER NOT NULL 
		TITLE 'Business Party Id',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_BONUS_TIMING
	 (
			Individual_Party_Id
	 );
	 


CREATE  TABLE  Core_DB.INDIVIDUAL_SKILL
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Skill_Cd             VARCHAR(50) NOT NULL 
		TITLE 'Skill Cd',
	Individual_Skill_Dt  DATE NULL 
		TITLE 'Individual Skill Dt',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_SKILL
	 (
			Individual_Party_Id
	 );
	 
	 


CREATE  TABLE  Core_DB.SKILL_TYPE
(

	Skill_Cd             VARCHAR(50) NOT NULL 
		TITLE 'Skill Cd',
	Skill_Desc           VARCHAR(250) NULL 
		TITLE 'Skill Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_SKILL_TYPE
	 (
			Skill_Cd
	 );
	 


CREATE  TABLE  Core_DB.PARTY_RELATED
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_RELATED
	 (
			Party_Id
	 );
	 
	 

CREATE  TABLE  Core_DB.PARTY_CLAIM
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_CLAIM
	 (
			Claim_Id
	 );
	 



CREATE  TABLE  Core_DB.PARTY_SCORE
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Model_Id             INTEGER NOT NULL 
		TITLE 'Model Id',
	Model_Run_Id         INTEGER NOT NULL 
		TITLE 'Model Run Id',
	Party_Score_Val      VARCHAR(100) NULL 
		TITLE 'Party Score Val',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_SCORE
	 (
			Party_Id
	 );
	 
	 



CREATE  TABLE  Core_DB.MARKET_SEGMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_MARKET_SEGMENT
	 (
			Market_Segment_Id
	 );
	 
	 


CREATE  TABLE  Core_DB.PARTY_CREDIT_REPORT_SCORE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_CREDIT_REPORT_SCORE
	 (
			Obligor_Party_Id
	 );
	 
	 

CREATE  TABLE  Core_DB.INDIVIDUAL_MEDICAL
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_MEDICAL
	 (
			Individual_Party_Id
	 );
	 
	 

CREATE  TABLE  Core_DB.INDIVIDUAL_SPECIAL_NEED
(

	Individual_Party_Id  INTEGER NOT NULL 
		TITLE 'Individual Party Id',
	Special_Need_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Special Need Cd',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INDIVIDUAL_SPECIAL_NEED
	 (
			Individual_Party_Id
	 );
	 
	 

CREATE  TABLE  Core_DB.SPECIAL_NEED_TYPE
(

	Special_Need_Cd      VARCHAR(50) NOT NULL 
		TITLE 'Special Need Cd',
	Special_Need_Desc    VARCHAR(250) NULL 
		TITLE 'Special Need Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_SPECIAL_NEED_TYPE
	 (
			Special_Need_Cd
	 );
	 


CREATE  TABLE  Core_DB.GENDER_TYPE
(

	Gender_Type_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Gender Type Cd',
	Gender_Type_Desc     VARCHAR(250) NOT NULL 
		TITLE 'Gender Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_GENDER_TYPE
	 (
			Gender_Type_Cd
	 );
	 
	 


CREATE  TABLE  Core_DB.GENDER_PRONOUN
(

	Gender_Pronoun_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Gender Pronoun Cd',
	Gender_Pronoun_Name  VARCHAR(100) NULL 
		TITLE 'Gender Pronoun Name',
	Gender_Pronoun_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Gender Pronoun Type Cd',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_GENDER_PRONOUN
	 (
			Gender_Pronoun_Cd,
			Gender_Pronoun_Type_Cd
	 );
	 


CREATE  TABLE  Core_DB.ETHNICITY_TYPE
(

	Ethnicity_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Ethnicity Type Cd',
	Ethnicity_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Ethnicity Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_ETHNICITY_TYPE
	 (
			Ethnicity_Type_Cd
	 );
	 
	 

CREATE  TABLE  Core_DB.MARITAL_STATUS_TYPE
(

	Marital_Status_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Marital Status Cd',
	Marital_Status_Desc  VARCHAR(250) NULL 
		TITLE 'Marital Status Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_MARITAL_STATUS_TYPE
	 (
			Marital_Status_Cd
	 );
	 
	 


CREATE  TABLE  Core_DB.NATIONALITY_TYPE
(

	Nationality_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Nationality Cd',
	Nationality_Desc     VARCHAR(250) NULL 
		TITLE 'Nationality Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_NATIONALITY_TYPE
	 (
			Nationality_Cd
	 );
	 



CREATE  TABLE  Core_DB.TAX_BRACKET_TYPE
(

	Tax_Bracket_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Tax Bracket Cd',
	Tax_Bracket_Desc     VARCHAR(250) NULL 
		TITLE 'Tax Bracket Desc',
	Tax_Bracket_Rate     DECIMAL(15,12) NULL 
		TITLE 'Tax Bracket Rate',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_TAX_BRACKET_TYPE
	 (
			Tax_Bracket_Cd
	 );
	 



CREATE  TABLE  Core_DB.VERY_IMPORTANT_PERSON_TYPE
(

	VIP_Type_Cd          VARCHAR(50) NOT NULL 
		TITLE 'VIP Type Cd',
	VIP_Type_Desc        VARCHAR(250) NULL 
		TITLE 'VIP Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_VERY_IMPORTANT_PERSON_TYPE
	 (
			VIP_Type_Cd
	 );
	 



CREATE  TABLE  Core_DB.MILITARY_STATUS_TYPE
(

	Military_Status_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Military Status Type Cd',
	Military_Status_Desc VARCHAR(250) NULL 
		TITLE 'Military Status Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_MILITARY_STATUS_TYPE
	 (
			Military_Status_Type_Cd
	 );
	 



CREATE  TABLE  Core_DB.OCCUPATION_TYPE
(

	Occupation_Type_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Occupation Type Cd',
	Occupation_Type_Desc VARCHAR(250) NULL 
		TITLE 'Occupation Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_OCCUPATION_TYPE
	 (
			Occupation_Type_Cd
	 );
	 



CREATE  TABLE  Core_DB.TIME_PERIOD_TYPE
(

	Time_Period_Cd       VARCHAR(50) NOT NULL 
		TITLE 'Time Period Cd',
	Time_Period_Desc     VARCHAR(250) NULL 
		TITLE 'Time Period Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_TIME_PERIOD_TYPE
	 (
			Time_Period_Cd
	 );
	 
	 



CREATE  TABLE  Core_DB.PARTY_RELATED_STATUS_TYPE
(

	Party_Related_Status_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Party Related Status Type Cd',
	Party_Related_Status_Type_Desc VARCHAR(250) NULL 
		TITLE 'Party Related Status Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_PARTY_RELATED_STATUS_TYPE
	 (
			Party_Related_Status_Type_Cd
	 );
	 



CREATE  TABLE  Core_DB.GENERAL_MEDICAL_STATUS_TYPE
(

	General_Medical_Status_Cd VARCHAR(50) NOT NULL 
		TITLE 'General Medical Status Cd',
	General_Medical_Status_Desc VARCHAR(250) NULL 
		TITLE 'General Medical Status Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_GENERAL_MEDICAL_STATUS_TYPE
	 (
			General_Medical_Status_Cd
	 );
	 



CREATE  TABLE  Core_DB.RISK_EXPOSURE_MITIGANT_SUBTYPE
(

	Risk_Exposure_Mitigant_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Risk Exposure Mitigant Subtype Cd',
	Risk_Exposure_Mitigant_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Risk Exposure Mitigant Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_RISK_EXPOSURE_MITIGANT_SUBTYPE
	 (
			Risk_Exposure_Mitigant_Subtype_Cd
	 );
	 



CREATE  TABLE  Core_DB.PRICING_METHOD_SUBTYPE
(

	Pricing_Method_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Pricing Method Subtype Cd',
	Pricing_Method_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Pricing Method Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_PRICING_METHOD_SUBTYPE
	 (
			Pricing_Method_Subtype_Cd
	 );
	 



CREATE  TABLE  Core_DB.FINANCIAL_AGREEMENT_TYPE
(

	Financial_Agreement_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Financial Agreement Type Cd-7-1',
	Financial_Agreement_Type_Desc VARCHAR(250) NULL 
		TITLE 'Financial Agreement Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_FINANCIAL_AGREEMENT_TYPE
	 (
			Financial_Agreement_Type_Cd
	 );
	 



CREATE  TABLE  Core_DB.CREDIT_AGREEMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_CREDIT_AGREEMENT
	 (
			Agreement_Id
	 );
	 




CREATE  TABLE  Core_DB.PAYMENT_TIMING_TYPE
(

	Payment_Timing_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Payment Timing Type Cd',
	Payment_Timing_Type_Desc VARCHAR(250) NULL 
		TITLE 'Payment Timing Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_PAYMENT_TIMING_TYPE
	 (
			Payment_Timing_Type_Cd
	 );
	 


CREATE  TABLE  Core_DB.PURCHASE_INTENT_TYPE
(

	Purchase_Intent_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Purchase Intent Cd',
	Purchase_Intent_Desc VARCHAR(250) NULL 
		TITLE 'Purchase Intent Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_PURCHASE_INTENT_TYPE
	 (
			Purchase_Intent_Cd
	 );
	 



CREATE  TABLE  Core_DB.LOAN_AGREEMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_LOAN_AGREEMENT
	 (
			Agreement_Id
	 );
	 



CREATE  TABLE  Core_DB.SECURITY_TYPE
(

	Security_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Security Type Cd',
	Security_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Security Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_SECURITY_TYPE
	 (
			Security_Type_Cd
	 );
	 
	 



CREATE  TABLE  Core_DB.LOAN_MATURITY_SUBTYPE
(

	Loan_Maturity_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Loan Maturity Subtype Cd',
	Loan_Maturity_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Loan Maturity Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_LOAN_MATURITY_SUBTYPE
	 (
			Loan_Maturity_Subtype_Cd
	 );
	 



CREATE  TABLE  Core_DB.LOAN_TRANSACTION_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Loan_Transaction_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Loan Transaction Subtype Cd',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_LOAN_TRANSACTION_AGREEMENT
	 (
			Agreement_Id
	 );
	 
	 



CREATE  TABLE  Core_DB.LOAN_TRANSACTION_SUBTYPE
(

	Loan_Transaction_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Loan Transaction Subtype Cd',
	Loan_Transaction_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Loan Transaction Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_LOAN_TRANSACTION_SUBTYPE
	 (
			Loan_Transaction_Subtype_Cd
	 );
	 



CREATE  TABLE  Core_DB.CREDIT_CARD_AGREEMENT
(

	Agreement_Id         INTEGER NOT NULL 
		TITLE 'Agreement Id',
	Credit_Card_Agreement_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Credit Card Agreement Subtype Cd',
	Credit_Card_Activation_Dttm TIMESTAMP NULL 
		TITLE 'Credit Card Activation Dttm',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_CREDIT_CARD_AGREEMENT
	 (
			Agreement_Id
	 );
	 


CREATE  TABLE  Core_DB.CREDIT_CARD_AGREEMENT_SUBTYPE
(

	Credit_Card_Agreement_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Credit Card Agreement Subtype Cd',
	Credit_Card_Agreement_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Credit Card Agreement Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_CREDIT_CARD_AGREEMENT_SUBTYPE
	 (
			Credit_Card_Agreement_Subtype_Cd
	 );
	 
	 


CREATE  TABLE  Core_DB.LOAN_TERM_AGREEMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_LOAN_TERM_AGREEMENT
	 (
			Agreement_Id
	 );
	 



CREATE  TABLE  Core_DB.LOAN_TERM_SUBTYPE
(

	Loan_Term_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Loan Term Subtype Cd',
	Loan_Term_Subtype_Desc VARCHAR(250) NULL 
		TITLE 'Loan Term Subtype Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_LOAN_TERM_SUBTYPE
	 (
			Loan_Term_Subtype_Cd
	 );
	 



CREATE  TABLE  Core_DB.AMORTIZATION_METHOD_TYPE
(

	Amortization_Method_Cd VARCHAR(50) NOT NULL 
		TITLE 'Amortization Method Cd',
	Amortization_Method_Desc VARCHAR(250) NOT NULL 
		TITLE 'Amortization Method Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_AMORTIZATION_METHOD_TYPE
	 (
			Amortization_Method_Cd
	 );
	 



CREATE  TABLE  Core_DB.MORTGAGE_AGREEMENT
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_MORTGAGE_AGREEMENT
	 (
			Agreement_Id
	 );
	 


CREATE  TABLE  Core_DB.MORTGAGE_TYPE
(

	Mortgage_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Mortgage Type Cd',
	Mortgage_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Mortgage Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_MORTGAGE_TYPE
	 (
			Mortgage_Type_Cd
	 );
	 



CREATE  TABLE  Core_DB.TERM_FEATURE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_TERM_FEATURE
	 (
			Feature_Id
	 );
	 
	 



CREATE  TABLE  Core_DB.INTEREST_RATE_INDEX
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INTEREST_RATE_INDEX
	 (
			Interest_Rate_Index_Cd
	 );
	 


CREATE  TABLE  Core_DB.INTEREST_INDEX_RATE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_INTEREST_INDEX_RATE
	 (
			Interest_Rate_Index_Cd
	 );
	 
	 


CREATE  TABLE  Core_DB.VARIABLE_INTEREST_RATE_FEATURE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_VARIABLE_INTEREST_RATE_FEATURE
	 (
			Feature_Id
	 );
	 



CREATE  TABLE  Core_DB.ORGANIZATION
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ORGANIZATION
	 (
			Organization_Party_Id
	 );
	 



CREATE  TABLE  Core_DB.BUSINESS
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_BUSINESS
	 (
			Business_Party_Id
	 );
	 



CREATE  TABLE  Core_DB.BUSINESS_CATEGORY
(

	Business_Category_Cd VARCHAR(50) NOT NULL 
		TITLE 'Business Legal Class Cd',
	Business_Category_Desc VARCHAR(250) NULL 
		TITLE 'Business Legal Class Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_BUSINESS_CATEGORY
	 (
			Business_Category_Cd
	 );
	 



CREATE  TABLE  Core_DB.ORGANIZATION_NAICS
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ORGANIZATION_NAICS
	 (
			Organization_Party_Id
	 );
	 





CREATE  TABLE  Core_DB.ORGANIZATION_NACE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ORGANIZATION_NACE
	 (
			Organization_Party_Id
	 );
	 



CREATE  TABLE  Core_DB.NACE_CLASS
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_NACE_CLASS
	 (
			NACE_Class_Cd
	 );
	 



CREATE  TABLE  Core_DB.ORGANIZATION_SIC
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ORGANIZATION_SIC
	 (
			Organization_Party_Id
	 );
	 



CREATE  TABLE  Core_DB.ORGANIZATION_GICS
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ORGANIZATION_GICS
	 (
			Organization_Party_Id
	 );



CREATE  TABLE  Core_DB.PARTY_SPECIALTY
(

	Party_Id             INTEGER NOT NULL 
		TITLE 'Party Id',
	Specialty_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Specialty Type Cd',
	Party_Specialty_Start_Dt DATE NOT NULL 
		TITLE 'Party Specialty Start Dt',
	Party_Specialty_End_Dt DATE NULL 
		TITLE 'Party Specialty End Dt',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_SPECIALTY
	 (
			Party_Id
	 );
	 



CREATE  TABLE  Core_DB.LEGAL_CLASSIFICATION
(

	Legal_Classification_Cd VARCHAR(50) NOT NULL 
		TITLE 'Legal Classification Cd',
	Legal_Classification_Desc VARCHAR(250) NULL 
		TITLE 'Legal Classification Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_LEGAL_CLASSIFICATION
	 (
			Legal_Classification_Cd
	 );
	 
	 


CREATE  TABLE  Core_DB.NAICS_INDUSTRY
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_NAICS_INDUSTRY
	 (
			NAICS_Sector_Cd,
			NAICS_Subsector_Cd,
			NAICS_Industry_Group_Cd
	 );
	 
 


CREATE  TABLE  Core_DB.SIC
(

	SIC_Cd               VARCHAR(50) NOT NULL 
		TITLE 'SIC Cd',
	SIC_Desc             VARCHAR(250) NULL 
		TITLE 'SIC Desc',
	SIC_Group_Cd         VARCHAR(50) NOT NULL 
		TITLE 'SIC Group Cd',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_SIC
	 (
			SIC_Cd
	 );
	 


CREATE  TABLE  Core_DB.GICS_INDUSTRY_TYPE
(

	GICS_Industry_Cd     VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Cd',
	GICS_Industry_Group_Cd VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Group Cd',
	GICS_Sector_Cd       VARCHAR(50) NOT NULL 
		TITLE 'GICS Sector Cd',
	GICS_Industry_Desc   VARCHAR(250) NULL 
		TITLE 'GICS Industry Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_GICS_INDUSTRY_TYPE
	 (
			GICS_Industry_Cd
	 );
	 



CREATE  TABLE  Core_DB.GICS_SUBINDUSTRY_TYPE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_GICS_SUBINDUSTRY_TYPE
	 (
			GICS_Subindustry_Cd
	 );
	 


CREATE  TABLE  Core_DB.GICS_INDUSTRY_GROUP_TYPE
(

	GICS_Industry_Group_Cd VARCHAR(50) NOT NULL 
		TITLE 'GICS Industry Group Cd',
	GICS_Sector_Cd       VARCHAR(50) NOT NULL 
		TITLE 'GICS Sector Cd',
	GICS_Industry_Group_Desc VARCHAR(250) NULL 
		TITLE 'GICS Industry Group Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_GICS_INDUSTRY_GROUP_TYPE
	 (
			GICS_Industry_Group_Cd
	 );
	 



CREATE  TABLE  Core_DB.GICS_SECTOR_TYPE
(

	GICS_Sector_Cd       VARCHAR(50) NOT NULL 
		TITLE 'GICS Sector Cd',
	GICS_Sector_Desc     VARCHAR(250) NULL 
		TITLE 'GICS Sector Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_GICS_SECTOR_TYPE
	 (
			GICS_Sector_Cd
	 );
	 



CREATE  TABLE  Core_DB.SPECIALTY_TYPE
(

	Specialty_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Specialty Type Cd',
	Specialty_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Specialty Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_SPECIALTY_TYPE
	 (
			Specialty_Type_Cd
	 );
	 


CREATE  TABLE  Core_DB.ORGANIZATION_NAME
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ORGANIZATION_NAME
	 (
			Organization_Party_Id
	 );
	 


CREATE  TABLE  Core_DB.PARTY_IDENTIFICATION
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_IDENTIFICATION
	 (
			Party_Id
	 );
	 


CREATE  TABLE  Core_DB.PARTY_LANGUAGE_USAGE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_LANGUAGE_USAGE
	 (
			Party_Id
	 );
	 


CREATE  TABLE  Core_DB.LANGUAGE_TYPE
(

	Language_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Language Type Cd',
	Language_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Language Type Desc',
	Language_Native_Name VARCHAR(100) NULL 
		TITLE 'Language Native Name',
	ISO_Language_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'ISO Language Type Cd',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_LANGUAGE_TYPE
	 (
			Language_Type_Cd
	 );
	 



CREATE  TABLE  Core_DB.PROMOTION
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PROMOTION
	 (
			Promotion_Id
	 );
	 



CREATE  TABLE  Core_DB.PROMOTION_METRIC_TYPE
(

	Promotion_Metric_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Promotion Metric Type Cd',
	Promotion_Metric_Type_Desc VARCHAR(250) NULL 
		TITLE 'Promotion Metric Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_PROMOTION_METRIC_TYPE
	 (
			Promotion_Metric_Type_Cd
	 );
	 


CREATE  TABLE  Core_DB.UNIT_OF_MEASURE
(

	Unit_Of_Measure_Cd   VARCHAR(50) NOT NULL 
		TITLE 'Unit Of Measure Cd',
	Unit_Of_Measure_Name VARCHAR(100) NULL 
		TITLE 'Unit Of Measure Name',
	Unit_Of_Measure_Type_Cd VARCHAR(50) NULL 
		TITLE 'Unit Of Measure Type Cd',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_UNIT_OF_MEASURE
	 (
			Unit_Of_Measure_Cd
	 );
	 



CREATE  TABLE  Core_DB.PROMOTION_OFFER
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PROMOTION_OFFER
	 (
			Promotion_Id
	 );
	 


CREATE  TABLE  Core_DB.PROMOTION_OFFER_TYPE
(

	Promotion_Offer_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Promotion Offer Type Cd',
	Promotion_Offer_Type_Desc VARCHAR(250) NOT NULL 
		TITLE 'Promotion Offer Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_PROMOTION_OFFER_TYPE
	 (
			Promotion_Offer_Type_Cd
	 );
	 


CREATE  TABLE  Core_DB.STREET_ADDRESS
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_STREET_ADDRESS
	 (
			Street_Address_Id
	 );
	 


CREATE  TABLE  Core_DB.STREET_ADDRESS_DETAIL
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_STREET_ADDRESS_DETAIL
	 (
			Street_Address_Id
	 );


CREATE  TABLE  Core_DB.DIRECTION_TYPE
(

	Direction_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Direction Type Cd',
	Direction_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Direction Type Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_DIRECTION_TYPE
	 (
			Direction_Type_Cd
	 );
	 


CREATE  TABLE  Core_DB.STREET_SUFFIX_TYPE
(

	Street_Suffix_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Street Suffix Cd',
	Street_Suffix_Desc   VARCHAR(250) NULL 
		TITLE 'Street Suffix Desc',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	 UNIQUE PRIMARY INDEX UPI_STREET_SUFFIX_TYPE
	 (
			Street_Suffix_Cd
	 );
	 


CREATE  TABLE  Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD
(

	Territory_Id         INTEGER NOT NULL 
		TITLE 'Territory Id',
	Territory_Standard_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Territory Standard Type Cd',
	ISO_3166_Country_Alpha_2_Cd CHAR(2) NULL 
		TITLE 'ISO 3166 Country Alpha-2 Cd',
	ISO_3166_Country_Subdivision_Cd CHAR(3) NULL 
		TITLE 'ISO 3166 Country Subdivision Cd',
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ISO_3166_COUNTRY_SUBDIVISION_STANDARD
	 (
			Territory_Id
	 );
	 
	 


CREATE  TABLE  Core_DB.POSTAL_CODE
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
	di_data_src_cd       VARCHAR(50) NULL 
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL 
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL 
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL 
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL 
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_POSTAL_CODE
	 (
			Postal_Code_Id
	 );
	 

CREATE  TABLE GEOSPATIAL_POINT
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
		TITLE 'Elevation UOM Cd'
)
	PRIMARY INDEX NUPI_GEOSPATIAL_POINT
	 (
			Geospatial_Point_Id
	 );
	 

CREATE  TABLE GEOSPATIAL
(

	Geospatial_Id        INTEGER NOT NULL 
		TITLE 'Geospatial Id',
	Geospatial_Roadway_Subtype_Cd VARCHAR(50) NOT NULL 
		TITLE 'Geospatial Roadway Subtype Cd',
	Geospatial_Coordinates_Geosptl ST_Geometry NULL 
		TITLE 'Geospatial Coordinates Geosptl',
	Geospatial_Subtype_Cd VARCHAR(50) NULL 
		TITLE 'Geospatial Subtype Cd'
)
	PRIMARY INDEX NUPI_GEOSPATIAL
	 (
			Geospatial_Id
	 );


CREATE  TABLE LOCATOR_RELATED
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
		TITLE 'Locator Related End Dt'
)
	PRIMARY INDEX NUPI_LOCATOR_RELATED
	 (
			Locator_Id
	 );
	 

CREATE  TABLE UNIT_OF_MEASURE_TYPE
(

	Unit_Of_Measure_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Unit Of Measure Type Cd',
	Unit_Of_Measure_Type_Desc VARCHAR(250) NULL 
		TITLE 'Unit Of Measure Type Desc'
)
	 UNIQUE PRIMARY INDEX UPI_UNIT_OF_MEASURE_TYPE
	 (
			Unit_Of_Measure_Type_Cd
	 );
	 

CREATE  TABLE ANALYTICAL_MODEL
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
		TITLE 'Criticality Type Cd'
)
	PRIMARY INDEX NUPI_ANALYTICAL_MODEL
	 (
			Model_Id
	 );


CREATE  TABLE CALENDAR_TYPE
(

	Calendar_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Calendar Type Cd',
	Calendar_Type_Desc   VARCHAR(250) NULL 
		TITLE 'Calendar Type Desc'
)
	 UNIQUE PRIMARY INDEX UPI_CALENDAR_TYPE
	 (
			Calendar_Type_Cd
	 );
	 
	 
CREATE  TABLE CHANNEL_STATUS_TYPE
(

	Channel_Status_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Channel Status Cd',
	Channel_Status_Desc  VARCHAR(250) NULL 
		TITLE 'Channel Status Desc'
)
	 UNIQUE PRIMARY INDEX UPI_CHANNEL_STATUS_TYPE
	 (
			Channel_Status_Cd
	 );
	 

CREATE  TABLE CITY
(

	City_Id              INTEGER NOT NULL 
		TITLE 'City Id',
	City_Type_Cd         VARCHAR(50) NULL 
		TITLE 'City Type Cd',
	Territory_Id         INTEGER NULL 
		TITLE 'Territory Id'
)
	PRIMARY INDEX NUPI_CITY
	 (
			City_Id
	 );
	 
	 

CREATE  TABLE CITY_TYPE
(

	City_Type_Cd         VARCHAR(50) NOT NULL 
		TITLE 'City Type Cd',
	City_Type_Desc       VARCHAR(250) NULL 
		TITLE 'City Type Desc'
)
	 UNIQUE PRIMARY INDEX UPI_CITY_TYPE
	 (
			City_Type_Cd
	 );
	 


CREATE  TABLE COUNTY
(

	County_Id            INTEGER NOT NULL 
		TITLE 'County Id',
	Territory_Id         INTEGER NOT NULL 
		TITLE 'Territory Id',
	MSA_Id               INTEGER NULL 
		TITLE 'MSA Id *Geo'
)
	PRIMARY INDEX NUPI_COUNTY
	 (
			County_Id
	 );
	 
	 

CREATE  TABLE COUNTRY
(

	Country_Id           INTEGER NOT NULL 
		TITLE 'Country Id',
	Calendar_Type_Cd     VARCHAR(50) NOT NULL 
		TITLE 'Calendar Type Cd',
	Country_Group_Id     INTEGER NULL 
		TITLE 'Country Group Id'
)
	PRIMARY INDEX NUPI_COUNTRY
	 (
			Country_Id
	 );
	 


CREATE  TABLE GEOGRAPHICAL_AREA
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
		TITLE 'Geographical Area End Dt'
)
	PRIMARY INDEX NUPI_GEOGRAPHICAL_AREA
	 (
			Geographical_Area_Id
	 );
	 


CREATE  TABLE GEOGRAPHICAL_AREA_CURRENCY
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
		TITLE 'Geographical Area Currency End Dt'
)
	PRIMARY INDEX NUPI_GEOGRAPHICAL_AREA_CURRENCY
	 (
			Geographical_Area_Id
	 );
	 

CREATE  TABLE ISO_3166_COUNTRY_STANDARD
(

	Country_Id           INTEGER NOT NULL 
		TITLE 'Country Id',
	Country_Code_Standard_Type_Cd VARCHAR(50) NOT NULL 
		TITLE 'Country Code Standard Type Cd',
	ISO_3166_Country_3_Num CHAR(3) NOT NULL 
		TITLE 'ISO 3166 Country-3 Num'
)
	PRIMARY INDEX NUPI_ISO_3166_COUNTRY_STANDARD
	 (
			ISO_3166_Country_3_Num
	 );
	 


CREATE  TABLE PARCEL_ADDRESS
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
		TITLE 'Territory Id'
)
	PRIMARY INDEX NUPI_PARCEL_ADDRESS
	 (
			Parcel_Address_Id
	 );
	 

CREATE  TABLE POST_OFFICE_BOX_ADDRESS
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
		TITLE 'Territory Id'
)
	PRIMARY INDEX NUPI_POST_OFFICE_BOX_ADDRESS
	 (
			Post_Office_Box_Id
	 );
	 


CREATE  TABLE REGION
(

	Region_Id            INTEGER NOT NULL 
		TITLE 'Region Id',
	Country_Id           INTEGER NULL 
		TITLE 'Country Id'
)
	PRIMARY INDEX NUPI_REGION
	 (
			Region_Id
	 );
	 

CREATE  TABLE TERRITORY
(

	Territory_Id         INTEGER NOT NULL 
		TITLE 'Territory Id',
	Territory_Type_Cd    VARCHAR(50) NULL 
		TITLE 'Territory Type Cd',
	Country_Id           INTEGER NOT NULL 
		TITLE 'Country Id',
	Region_Id            INTEGER NULL 
		TITLE 'Region Id'
)
	PRIMARY INDEX NUPI_TERRITORY
	 (
			Territory_Id
	 );
	 

CREATE  TABLE TERRITORY_TYPE
(

	Territory_Type_Cd    VARCHAR(50) NOT NULL 
		TITLE 'Territory Type Cd',
	Territory_Type_Desc  VARCHAR(250) NULL 
		TITLE 'Territory Type Desc'
)
	 UNIQUE PRIMARY INDEX UPI_TERRITORY_TYPE
	 (
			Territory_Type_Cd
	 );


/* ============================================================
   DDL-GAP TABLES
   These 9 tables were in-scope per 02_data-mapping-reference.md
   but had no DDL in the original SQL files.
   Column definitions derived from WP2/WP3 mapping rules.
   Added: 2026-04-18
   ============================================================ */


CREATE TABLE Core_DB.PARTY_STATUS
(
	Party_Id             BIGINT NOT NULL
		TITLE 'Party Id',
	Party_Status_Cd      VARCHAR(50) NOT NULL
		TITLE 'Party Status Cd',
	Party_Status_Dt      DATE NOT NULL
		TITLE 'Party Status Dt',
	di_data_src_cd       VARCHAR(50) NULL
		TITLE 'DI Data Src Cd',
	di_start_ts          TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_proc_name         VARCHAR(255) NULL
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind   CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind',
	di_end_ts            TIMESTAMP(6) NULL
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_STATUS
	 (
			Party_Id
	 );


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
	di_data_src_cd            VARCHAR(50) NULL
		TITLE 'DI Data Src Cd',
	di_start_ts               TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_proc_name              VARCHAR(255) NULL
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind        CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind',
	di_end_ts                 TIMESTAMP(6) NULL
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PARTY_SEGMENT
	 (
			Party_Id
	 );


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
	di_data_src_cd           VARCHAR(50) NULL
		TITLE 'DI Data Src Cd',
	di_start_ts              TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_proc_name             VARCHAR(255) NULL
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind       CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind',
	di_end_ts                TIMESTAMP(6) NULL
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PRODUCT_COST
	 (
			Product_Id
	 );


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
	di_data_src_cd           VARCHAR(50) NULL
		TITLE 'DI Data Src Cd',
	di_start_ts              TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_proc_name             VARCHAR(255) NULL
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind       CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind',
	di_end_ts                TIMESTAMP(6) NULL
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_PRODUCT_GROUP
	 (
			Product_Group_Id
	 );


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
	di_data_src_cd            VARCHAR(50) NULL
		TITLE 'DI Data Src Cd',
	di_start_ts               TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_proc_name              VARCHAR(255) NULL
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind        CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind',
	di_end_ts                 TIMESTAMP(6) NULL
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_EVENT_CHANNEL_INSTANCE
	 (
			Event_Id
	 );


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
	di_data_src_cd               VARCHAR(50) NULL
		TITLE 'DI Data Src Cd',
	di_start_ts                  TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_proc_name                 VARCHAR(255) NULL
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind           CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind',
	di_end_ts                    TIMESTAMP(6) NULL
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_FINANCIAL_EVENT_AMOUNT
	 (
			Event_Id
	 );


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
	di_data_src_cd                   VARCHAR(50) NULL
		TITLE 'DI Data Src Cd',
	di_start_ts                      TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_proc_name                     VARCHAR(255) NULL
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind               CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind',
	di_end_ts                        TIMESTAMP(6) NULL
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_FUNDS_TRANSFER_EVENT
	 (
			Event_Id
	 );


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
	di_data_src_cd                   VARCHAR(50) NULL
		TITLE 'DI Data Src Cd',
	di_start_ts                      TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_proc_name                     VARCHAR(255) NULL
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind               CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind',
	di_end_ts                        TIMESTAMP(6) NULL
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_ACCESS_DEVICE_EVENT
	 (
			Event_Id
	 );


CREATE TABLE Core_DB.DIRECT_CONTACT_EVENT
(
	Event_Id                  BIGINT NOT NULL
		TITLE 'Event Id',
	Contact_Event_Subtype_Cd  VARCHAR(50) NOT NULL
		TITLE 'Contact Event Subtype Cd',
	Customer_Tone_Cd          VARCHAR(50) NULL
		TITLE 'Customer Tone Cd',
	di_data_src_cd            VARCHAR(50) NULL
		TITLE 'DI Data Src Cd',
	di_start_ts               TIMESTAMP(6) NULL
		TITLE 'DI Start Ts',
	di_proc_name              VARCHAR(255) NULL
		TITLE 'DI Proc Name',
	di_rec_deleted_Ind        CHAR(1) NULL
		TITLE 'DI Rec Deleted Ind',
	di_end_ts                 TIMESTAMP(6) NULL
		TITLE 'DI End Ts'
)
	PRIMARY INDEX NUPI_DIRECT_CONTACT_EVENT
	 (
			Event_Id
	 );
	 
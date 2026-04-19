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






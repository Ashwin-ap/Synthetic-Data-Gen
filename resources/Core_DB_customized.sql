-- PARTY CONTACT PREFERENCE

CREATE TABLE Core_DB.PARTY_CONTACT_PREFERENCE
(
    Party_Id                            BIGINT       NOT NULL,
    Channel_Type_Cd                     SMALLINT     NOT NULL,
    Contact_Preference_Type_Cd          SMALLINT     NOT NULL,
    Party_Contact_Preference_Start_Dt   DATE         NOT NULL,
    Party_Contact_Preference_End_Dt     DATE         NOT NULL,
    Party_Contact_Preference_Priority_Num  INTEGER,
    Protocol_Type_Cd                    SMALLINT     NOT NULL,
    Days_Cd                             SMALLINT     NOT NULL,
    Hours_Cd                            SMALLINT     NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Party_Id);

--


-- MULTIMEDIA OBJECT LOCATOR

CREATE TABLE Core_DB.MULTIMEDIA_OBJECT_LOCATOR
(
    MM_Object_Id           BIGINT       NOT NULL,
    Locator_Id             BIGINT,
    MM_Locator_Reason_Cd   SMALLINT     NOT NULL,
    MM_Locator_Start_Dt    DATE         NOT NULL,
    MM_Locator_End_Dt      DATE         NOT NULL
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (MM_Object_Id);

-- gap: LOV for MM_Locator_Reason_Cd



-- EVENT
CREATE  TABLE Core_DB.EVENT
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
		TITLE 'Initiation Type Cd'
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
	PRIMARY INDEX NUPI_EVENT
	 (
			Event_Id
	 );

-- COMPLAINTS EVENT

CREATE MULTISET TABLE Core_DB.COMPLAINT_EVENT
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

-- PARTY TASK

CREATE TABLE Core_DB.PARTY_TASK
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


-- PARTY TASK STATUS
CREATE TABLE Core_DB.PARTY_TASK_STATUS
(
    Task_Status_Id           BIGINT          NOT NULL,
    Task_Id                  BIGINT,
    Task_Status_Start_Dttm   TIMESTAMP       NOT NULL,
    Task_Status_End_Dttm     TIMESTAMP       NOT NULL,
    Task_Status_Type_Cd      SMALLINT        NOT NULL,
    Task_Status_Reason_Cd    SMALLINT        NOT NULL,
    Task_Status_Txt          VARCHAR(32000)
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Task_Status_Id);

-- 

-- TASK ACTIVITY

CREATE TABLE Core_DB.TASK_ACTIVITY
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

--

-- TASK ACTIVITY STATUS

CREATE TABLE Core_DB.TASK_ACTIVITY_STATUS
(
    Activity_Id                  BIGINT          NOT NULL,
    Activity_Status_Start_Dttm   TIMESTAMP       NOT NULL,
    Activity_Status_End_Dttm     TIMESTAMP       NOT NULL,
    Activity_Status_Type_Cd      SMALLINT        NOT NULL,
    Activity_Status_Reason_Cd    SMALLINT        NOT NULL,
    Activity_Status_Txt          VARCHAR(32000)
    ,di_data_src_cd              VARCHAR(50)     NULL
    ,di_start_ts                 TIMESTAMP(6)    NULL
    ,di_proc_name                VARCHAR(255)    NULL
    ,di_rec_deleted_Ind          CHAR(1)         NULL
    ,di_end_ts                   TIMESTAMP(6)    NULL
)
PRIMARY INDEX (Activity_Id);

--




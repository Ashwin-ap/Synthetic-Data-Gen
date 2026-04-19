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


from __future__ import annotations

from datetime import datetime, time, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, Dict, List

import pandas as pd

from config.settings import HISTORY_START
from config.code_values import (
    PROFITABILITY_MODEL_TYPE_CD,
    CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD,
    RATE_FEATURE_SUBTYPE_CD,
    ORIGINAL_LOAN_TERM_CLASSIFICATION_CD,
)
from generators.base import BaseGenerator

if TYPE_CHECKING:
    from registry.context import GenerationContext

# ── Constants ────────────────────────────────────────────────────────────────

_TIER2_DI_START_TS = '2000-01-01 00:00:00.000000'
_CLV_MODEL_NAME = 'CLV Decile Model'

_PARTY_SUBTYPE_BY_TYPE = {'INDIVIDUAL': 'retail', 'ORGANIZATION': 'commercial'}

_AGREEMENT_TYPE_BY_PRODUCT = {
    'CHECKING': 'DEPOSIT', 'SAVINGS': 'DEPOSIT', 'MMA': 'DEPOSIT',
    'CERTIFICATE_OF_DEPOSIT': 'DEPOSIT', 'RETIREMENT': 'DEPOSIT',
    'MORTGAGE': 'LOAN', 'VEHICLE_LOAN': 'LOAN', 'STUDENT_LOAN': 'LOAN', 'PAYDAY': 'LOAN',
    'CREDIT_CARD': 'CREDIT', 'HELOC': 'CREDIT',
    'COMMERCIAL_CHECKING': 'COMMERCIAL',
}

_AGREEMENT_OBJECTIVE_BY_PRODUCT = {
    'CHECKING': 'SAVINGS_GOAL', 'SAVINGS': 'SAVINGS_GOAL', 'MMA': 'SAVINGS_GOAL',
    'CERTIFICATE_OF_DEPOSIT': 'SAVINGS_GOAL', 'RETIREMENT': 'SAVINGS_GOAL',
    'MORTGAGE': 'HOME_PURCHASE', 'HELOC': 'HOME_PURCHASE',
    'STUDENT_LOAN': 'EDUCATION', 'VEHICLE_LOAN': 'VEHICLE',
    'CREDIT_CARD': 'SAVINGS_GOAL', 'PAYDAY': 'SAVINGS_GOAL',
    'COMMERCIAL_CHECKING': 'SAVINGS_GOAL',
}

_AGREEMENT_OBTAINED_BY_PRODUCT = {
    'CHECKING': 'BRANCH', 'SAVINGS': 'BRANCH', 'CERTIFICATE_OF_DEPOSIT': 'BRANCH',
    'VEHICLE_LOAN': 'BRANCH', 'PAYDAY': 'BRANCH',
    'MMA': 'ONLINE', 'CREDIT_CARD': 'ONLINE', 'STUDENT_LOAN': 'ONLINE',
    'RETIREMENT': 'PHONE', 'COMMERCIAL_CHECKING': 'PHONE',
    'MORTGAGE': 'REFERRAL', 'HELOC': 'REFERRAL',
}

_ASSET_LIABILITY_BY_TYPE = {
    'DEPOSIT': 'LIABILITY', 'LOAN': 'ASSET', 'CREDIT': 'ASSET', 'COMMERCIAL': 'LIABILITY',
}

_BALANCE_SHEET_BY_TYPE = {
    'DEPOSIT': 'ON_BALANCE_SHEET', 'LOAN': 'ON_BALANCE_SHEET',
    'CREDIT': 'ON_BALANCE_SHEET', 'COMMERCIAL': 'ON_BALANCE_SHEET',
}

_REQUIRED_TIER0_TABLES = (
    'Core_DB.AGREEMENT_SUBTYPE', 'Core_DB.AGREEMENT_TYPE',
    'Core_DB.AGREEMENT_OBJECTIVE_TYPE', 'Core_DB.AGREEMENT_OBTAINED_TYPE',
    'Core_DB.AGREEMENT_FORMAT_TYPE', 'Core_DB.ASSET_LIABILITY_TYPE',
    'Core_DB.BALANCE_SHEET_TYPE', 'Core_DB.DATA_SOURCE_TYPE',
    'Core_DB.STATEMENT_MAIL_TYPE', 'Core_DB.FEATURE_SUBTYPE',
    'Core_DB.FEATURE_INSURANCE_SUBTYPE', 'Core_DB.FEATURE_CLASSIFICATION_TYPE',
    'Core_DB.CHANNEL_TYPE', 'Core_DB.CHANNEL_INSTANCE_SUBTYPE',
    'Core_DB.CONVENIENCE_FACTOR_TYPE', 'Core_DB.CAMPAIGN_STRATEGY_TYPE',
    'Core_DB.CAMPAIGN_TYPE', 'Core_DB.CAMPAIGN_CLASSIFICATION', 'Core_DB.CURRENCY',
)

# ── DDL column lists (business columns; DI appended by stamp_di) ──────────────

_COLS_PARTY = [
    'Party_Id', 'Party_Subtype_Cd', 'Party_Desc', 'Party_Start_Dttm',
    'Party_End_Dttm', 'Party_Type_Cd', 'Initial_Data_Source_Type_Cd',
]

_COLS_AGREEMENT = [
    'Agreement_Id', 'Agreement_Subtype_Cd', 'Host_Agreement_Num', 'Agreement_Name',
    'Alternate_Agreement_Name', 'Agreement_Open_Dttm', 'Agreement_Close_Dttm',
    'Agreement_Planned_Expiration_Dt', 'Agreement_Processing_Dt', 'Agreement_Signed_Dt',
    'Agreement_Legally_Binding_Ind', 'Proposal_Id', 'Jurisdiction_Id',
    'Agreement_Format_Type_Cd', 'Agreement_Objective_Type_Cd', 'Agreement_Obtained_Cd',
    'Agreement_Type_Cd', 'Asset_Liability_Cd', 'Balance_Sheet_Cd',
    'Statement_Cycle_Cd', 'Statement_Mail_Type_Cd', 'Agreement_Source_Cd',
]

_COLS_PRODUCT = [
    'Product_Id', 'Product_Script_Id', 'Product_Subtype_Cd', 'Product_Desc',
    'Product_Name', 'Host_Product_Num', 'Product_Start_Dt', 'Product_End_Dt',
    'Product_Package_Type_Cd', 'Financial_Product_Ind', 'Product_Txt',
    'Product_Creation_Dt', 'Service_Ind',
]

_COLS_FEATURE = [
    'Feature_Id', 'Feature_Subtype_Cd', 'Feature_Insurance_Subtype_Cd',
    'Feature_Classification_Cd', 'Feature_Desc', 'Feature_Name',
    'Common_Feature_Name', 'Feature_Level_Subtype_Cnt',
]

_COLS_ANALYTICAL_MODEL = [
    'Model_Id', 'Model_Name', 'Model_Desc', 'Model_Version_Num', 'Model_Type_Cd',
    'Model_Algorithm_Type_Cd', 'Data_Source_Type_Cd', 'Model_From_Dttm', 'Model_To_Dttm',
    'Model_Predict_Time_Period_Cnt', 'Model_Predict_Time_Period_Cd', 'Model_Purpose_Cd',
    'Attestation_Ind', 'Model_Target_Run_Dt', 'Locator_Id', 'Criticality_Type_Cd',
]

_COLS_MARKET_SEGMENT = [
    'Market_Segment_Id', 'Model_Id', 'Model_Run_Id', 'Segment_Desc',
    'Segment_Start_Dttm', 'Segment_End_Dttm', 'Segment_Group_Id', 'Segment_Name',
    'Segment_Creator_Party_Id', 'Market_Segment_Scheme_Id',
]

_COLS_CHANNEL_INSTANCE = [
    'Channel_Instance_Id', 'Channel_Type_Cd', 'Channel_Instance_Subtype_Cd',
    'Channel_Instance_Name', 'Channel_Instance_Start_Dt', 'Channel_Instance_End_Dt',
    'Convenience_Factor_Cd',
]

_COLS_CAMPAIGN = [
    'Campaign_Id', 'Campaign_Strategy_Cd', 'Campaign_Type_Cd',
    'Campaign_Classification_Cd', 'Parent_Campaign_Id', 'Campaign_Level_Num',
    'Funding_GL_Main_Account_Id', 'Campaign_Desc', 'Campaign_Start_Dt',
    'Campaign_End_Dt', 'Campaign_Name', 'Campaign_Estimated_Cost_Amt', 'Currency_Cd',
    'Campaign_Estimated_Revenue_Gain_Amt', 'Campaign_Estimated_Base_Customer_Cnt',
    'Campaign_Estimated_Customer_Cnt', 'Campaign_Estimated_Positive_Cnt',
    'Campaign_Estimated_Contact_Cnt', 'Campaign_Creation_Dt',
]

# ── Hand-coded data templates ─────────────────────────────────────────────────

_MODEL_FROM_DTTM = datetime(2020, 1, 1, 0, 0, 0)

_ANALYTICAL_MODEL_TEMPLATES: List[Dict] = [
    # Row 1 & 2 both satisfy item #17 (profitability) and item #18 (customer profitability)
    {
        'Model_Name': 'Profitability Scoring Model',
        'Model_Desc': 'Scores agreements based on profitability metrics',
        'Model_Version_Num': '1.0',
        'Model_Type_Cd': PROFITABILITY_MODEL_TYPE_CD,
        'Model_Algorithm_Type_Cd': None,
        'Data_Source_Type_Cd': 'CORE_BANKING',
        'Model_From_Dttm': _MODEL_FROM_DTTM,
        'Model_To_Dttm': None,
        'Model_Predict_Time_Period_Cnt': None,
        'Model_Predict_Time_Period_Cd': None,
        'Model_Purpose_Cd': CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD,
        'Attestation_Ind': 'Yes',
        'Model_Target_Run_Dt': None,
        'Locator_Id': pd.NA,
        'Criticality_Type_Cd': None,
    },
    {
        'Model_Name': 'Customer Profitability Model',
        'Model_Desc': 'Estimates customer lifetime profitability for party scoring',
        'Model_Version_Num': '1.0',
        'Model_Type_Cd': PROFITABILITY_MODEL_TYPE_CD,
        'Model_Algorithm_Type_Cd': None,
        'Data_Source_Type_Cd': 'MDM',
        'Model_From_Dttm': _MODEL_FROM_DTTM,
        'Model_To_Dttm': None,
        'Model_Predict_Time_Period_Cnt': None,
        'Model_Predict_Time_Period_Cd': None,
        'Model_Purpose_Cd': CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD,
        'Attestation_Ind': 'Yes',
        'Model_Target_Run_Dt': None,
        'Locator_Id': pd.NA,
        'Criticality_Type_Cd': None,
    },
    # Row 3: CLV model — wired into MARKET_SEGMENT.Model_Id
    {
        'Model_Name': _CLV_MODEL_NAME,
        'Model_Desc': 'Segments customers into 10 CLV deciles based on lifetime value',
        'Model_Version_Num': '1.0',
        'Model_Type_Cd': 'clv_decile',
        'Model_Algorithm_Type_Cd': None,
        'Data_Source_Type_Cd': 'CORE_BANKING',
        'Model_From_Dttm': _MODEL_FROM_DTTM,
        'Model_To_Dttm': None,
        'Model_Predict_Time_Period_Cnt': None,
        'Model_Predict_Time_Period_Cd': None,
        'Model_Purpose_Cd': 'customer segmentation',
        'Attestation_Ind': 'Yes',
        'Model_Target_Run_Dt': None,
        'Locator_Id': pd.NA,
        'Criticality_Type_Cd': None,
    },
    {
        'Model_Name': 'Churn Risk Model',
        'Model_Desc': 'Predicts probability of customer churn within 90 days',
        'Model_Version_Num': '2.1',
        'Model_Type_Cd': 'churn_risk',
        'Model_Algorithm_Type_Cd': None,
        'Data_Source_Type_Cd': 'CORE_BANKING',
        'Model_From_Dttm': _MODEL_FROM_DTTM,
        'Model_To_Dttm': None,
        'Model_Predict_Time_Period_Cnt': None,
        'Model_Predict_Time_Period_Cd': None,
        'Model_Purpose_Cd': 'churn prediction',
        'Attestation_Ind': 'Yes',
        'Model_Target_Run_Dt': None,
        'Locator_Id': pd.NA,
        'Criticality_Type_Cd': None,
    },
    {
        'Model_Name': 'Cross-Sell Propensity Model',
        'Model_Desc': 'Scores likelihood of customer acquiring additional products',
        'Model_Version_Num': '1.3',
        'Model_Type_Cd': 'cross_sell_propensity',
        'Model_Algorithm_Type_Cd': None,
        'Data_Source_Type_Cd': 'CORE_BANKING',
        'Model_From_Dttm': _MODEL_FROM_DTTM,
        'Model_To_Dttm': None,
        'Model_Predict_Time_Period_Cnt': None,
        'Model_Predict_Time_Period_Cd': None,
        'Model_Purpose_Cd': 'product recommendation',
        'Attestation_Ind': 'Yes',
        'Model_Target_Run_Dt': None,
        'Locator_Id': pd.NA,
        'Criticality_Type_Cd': None,
    },
    {
        'Model_Name': 'Credit Score Model',
        'Model_Desc': 'Internal credit risk scoring based on payment history and balances',
        'Model_Version_Num': '3.0',
        'Model_Type_Cd': 'credit_score',
        'Model_Algorithm_Type_Cd': None,
        'Data_Source_Type_Cd': 'LOAN_ORIGINATION',
        'Model_From_Dttm': _MODEL_FROM_DTTM,
        'Model_To_Dttm': None,
        'Model_Predict_Time_Period_Cnt': None,
        'Model_Predict_Time_Period_Cd': None,
        'Model_Purpose_Cd': 'credit risk',
        'Attestation_Ind': 'Yes',
        'Model_Target_Run_Dt': None,
        'Locator_Id': pd.NA,
        'Criticality_Type_Cd': None,
    },
    {
        'Model_Name': 'Fraud Detection Model',
        'Model_Desc': 'Real-time fraud scoring for card and digital transactions',
        'Model_Version_Num': '4.2',
        'Model_Type_Cd': 'fraud_detection',
        'Model_Algorithm_Type_Cd': None,
        'Data_Source_Type_Cd': 'CARD_SYSTEM',
        'Model_From_Dttm': _MODEL_FROM_DTTM,
        'Model_To_Dttm': None,
        'Model_Predict_Time_Period_Cnt': None,
        'Model_Predict_Time_Period_Cd': None,
        'Model_Purpose_Cd': 'fraud prevention',
        'Attestation_Ind': 'Yes',
        'Model_Target_Run_Dt': None,
        'Locator_Id': pd.NA,
        'Criticality_Type_Cd': None,
    },
]

# 24 literal feature rows. Row 0: Feature_Subtype_Cd=RATE_FEATURE_SUBTYPE_CD AND
# Feature_Classification_Cd=ORIGINAL_LOAN_TERM_CLASSIFICATION_CD — satisfies both literal-match
# constraints simultaneously. Feature_Insurance_Subtype_Cd non-null only on Insurance Feature rows.
_FEATURE_TEMPLATES: List[Dict] = [
    # Rate Feature (4 rows)
    {'Feature_Subtype_Cd': RATE_FEATURE_SUBTYPE_CD, 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': ORIGINAL_LOAN_TERM_CLASSIFICATION_CD,
     'Feature_Desc': 'Interest rate applied over the original agreed loan term',
     'Feature_Name': 'Rate Feature - Original Loan Term',
     'Common_Feature_Name': 'Rate Loan Term', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': RATE_FEATURE_SUBTYPE_CD, 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Current Rate',
     'Feature_Desc': 'Current applicable interest rate on the agreement',
     'Feature_Name': 'Rate Feature - Current Rate',
     'Common_Feature_Name': 'Current Rate', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': RATE_FEATURE_SUBTYPE_CD, 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Origination Rate',
     'Feature_Desc': 'Interest rate at origination of the agreement',
     'Feature_Name': 'Rate Feature - Origination Rate',
     'Common_Feature_Name': 'Origination Rate', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': RATE_FEATURE_SUBTYPE_CD, 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Minimum Payment',
     'Feature_Desc': 'Minimum required payment rate for the period',
     'Feature_Name': 'Rate Feature - Minimum Payment',
     'Common_Feature_Name': 'Min Payment Rate', 'Feature_Level_Subtype_Cnt': 1},
    # Fee Feature (4 rows)
    {'Feature_Subtype_Cd': 'Fee Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Current Rate',
     'Feature_Desc': 'Current fee rate assessed on the agreement',
     'Feature_Name': 'Fee Feature - Current Rate',
     'Common_Feature_Name': 'Current Fee Rate', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Fee Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Minimum Balance',
     'Feature_Desc': 'Fee charged when balance falls below minimum threshold',
     'Feature_Name': 'Fee Feature - Minimum Balance',
     'Common_Feature_Name': 'Min Balance Fee', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Fee Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Maximum Balance',
     'Feature_Desc': 'Fee assessed when balance exceeds maximum threshold',
     'Feature_Name': 'Fee Feature - Maximum Balance',
     'Common_Feature_Name': 'Max Balance Fee', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Fee Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Maturity Date',
     'Feature_Desc': 'Early termination fee applied before maturity date',
     'Feature_Name': 'Fee Feature - Maturity Date',
     'Common_Feature_Name': 'Early Termination Fee', 'Feature_Level_Subtype_Cnt': 1},
    # Term Feature (4 rows)
    {'Feature_Subtype_Cd': 'Term Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': ORIGINAL_LOAN_TERM_CLASSIFICATION_CD,
     'Feature_Desc': 'Duration of the original agreed loan term in months',
     'Feature_Name': 'Term Feature - Original Loan Term',
     'Common_Feature_Name': 'Original Term', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Term Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Maturity Date',
     'Feature_Desc': 'Final maturity date for the term agreement',
     'Feature_Name': 'Term Feature - Maturity Date',
     'Common_Feature_Name': 'Maturity Date', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Term Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Minimum Payment',
     'Feature_Desc': 'Minimum scheduled payment amount for the term',
     'Feature_Name': 'Term Feature - Minimum Payment',
     'Common_Feature_Name': 'Min Payment', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Term Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Current Rate',
     'Feature_Desc': 'Current rate applicable during the term',
     'Feature_Name': 'Term Feature - Current Rate',
     'Common_Feature_Name': 'Term Current Rate', 'Feature_Level_Subtype_Cnt': 1},
    # Balance Feature (4 rows)
    {'Feature_Subtype_Cd': 'Balance Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Minimum Balance',
     'Feature_Desc': 'Minimum required balance to maintain the agreement',
     'Feature_Name': 'Balance Feature - Minimum Balance',
     'Common_Feature_Name': 'Min Balance', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Balance Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Maximum Balance',
     'Feature_Desc': 'Maximum allowable balance on the agreement',
     'Feature_Name': 'Balance Feature - Maximum Balance',
     'Common_Feature_Name': 'Max Balance', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Balance Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Current Rate',
     'Feature_Desc': 'Current balance rate applied to the agreement',
     'Feature_Name': 'Balance Feature - Current Rate',
     'Common_Feature_Name': 'Balance Rate', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Balance Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': ORIGINAL_LOAN_TERM_CLASSIFICATION_CD,
     'Feature_Desc': 'Balance carried forward from original loan term',
     'Feature_Name': 'Balance Feature - Original Loan Term',
     'Common_Feature_Name': 'Original Term Balance', 'Feature_Level_Subtype_Cnt': 1},
    # Reward Feature (4 rows)
    {'Feature_Subtype_Cd': 'Reward Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Minimum Balance',
     'Feature_Desc': 'Minimum balance required to qualify for rewards',
     'Feature_Name': 'Reward Feature - Minimum Balance',
     'Common_Feature_Name': 'Reward Min Balance', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Reward Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Maturity Date',
     'Feature_Desc': 'Expiry date for accumulated reward points',
     'Feature_Name': 'Reward Feature - Maturity Date',
     'Common_Feature_Name': 'Reward Expiry', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Reward Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Current Rate',
     'Feature_Desc': 'Current reward accrual rate per dollar spent',
     'Feature_Name': 'Reward Feature - Current Rate',
     'Common_Feature_Name': 'Reward Rate', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Reward Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Maximum Balance',
     'Feature_Desc': 'Maximum reward points that can be accumulated',
     'Feature_Name': 'Reward Feature - Maximum Balance',
     'Common_Feature_Name': 'Max Reward Points', 'Feature_Level_Subtype_Cnt': 1},
    # Insurance Feature (2 rows) — Feature_Insurance_Subtype_Cd='LIFE'
    {'Feature_Subtype_Cd': 'Insurance Feature', 'Feature_Insurance_Subtype_Cd': 'LIFE',
     'Feature_Classification_Cd': ORIGINAL_LOAN_TERM_CLASSIFICATION_CD,
     'Feature_Desc': 'Life insurance coverage over the original loan term',
     'Feature_Name': 'Insurance Feature - Original Loan Term',
     'Common_Feature_Name': 'Life Insurance Term', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Insurance Feature', 'Feature_Insurance_Subtype_Cd': 'LIFE',
     'Feature_Classification_Cd': 'Current Rate',
     'Feature_Desc': 'Current life insurance premium rate on the agreement',
     'Feature_Name': 'Insurance Feature - Current Rate',
     'Common_Feature_Name': 'Life Insurance Rate', 'Feature_Level_Subtype_Cnt': 1},
    # Payment Feature (2 rows)
    {'Feature_Subtype_Cd': 'Payment Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': 'Minimum Payment',
     'Feature_Desc': 'Minimum scheduled payment feature for the agreement',
     'Feature_Name': 'Payment Feature - Minimum Payment',
     'Common_Feature_Name': 'Min Payment Feature', 'Feature_Level_Subtype_Cnt': 1},
    {'Feature_Subtype_Cd': 'Payment Feature', 'Feature_Insurance_Subtype_Cd': None,
     'Feature_Classification_Cd': ORIGINAL_LOAN_TERM_CLASSIFICATION_CD,
     'Feature_Desc': 'Payment schedule over the original agreed loan term',
     'Feature_Name': 'Payment Feature - Original Loan Term',
     'Common_Feature_Name': 'Term Payment Schedule', 'Feature_Level_Subtype_Cnt': 1},
]

_CHANNEL_INST_START = HISTORY_START - timedelta(days=3650)

# 20 literal channel instance rows: 4 per type × 5 types.
_CHANNEL_INSTANCE_TEMPLATES: List[Dict] = [
    # BRANCH (4)
    {'Channel_Type_Cd': 'BRANCH', 'Channel_Instance_Subtype_Cd': 'MAIN_BRANCH',
     'Channel_Instance_Name': 'Branch #01 - Main Street',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': 'BUSINESS_HOURS'},
    {'Channel_Type_Cd': 'BRANCH', 'Channel_Instance_Subtype_Cd': 'MAIN_BRANCH',
     'Channel_Instance_Name': 'Branch #02 - Downtown',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': 'BUSINESS_HOURS'},
    {'Channel_Type_Cd': 'BRANCH', 'Channel_Instance_Subtype_Cd': 'MAIN_BRANCH',
     'Channel_Instance_Name': 'Branch #03 - Westside',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': 'BUSINESS_HOURS'},
    {'Channel_Type_Cd': 'BRANCH', 'Channel_Instance_Subtype_Cd': 'MAIN_BRANCH',
     'Channel_Instance_Name': 'Branch #04 - Airport',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': 'APPOINTMENT_REQUIRED'},
    # ATM (4)
    {'Channel_Type_Cd': 'ATM', 'Channel_Instance_Subtype_Cd': 'DRIVE_THRU_ATM',
     'Channel_Instance_Name': 'ATM NYC-0001',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    {'Channel_Type_Cd': 'ATM', 'Channel_Instance_Subtype_Cd': 'DRIVE_THRU_ATM',
     'Channel_Instance_Name': 'ATM NYC-0002',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    {'Channel_Type_Cd': 'ATM', 'Channel_Instance_Subtype_Cd': 'DRIVE_THRU_ATM',
     'Channel_Instance_Name': 'ATM LA-0001',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    {'Channel_Type_Cd': 'ATM', 'Channel_Instance_Subtype_Cd': 'DRIVE_THRU_ATM',
     'Channel_Instance_Name': 'ATM CHI-0001',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    # ONLINE (4)
    {'Channel_Type_Cd': 'ONLINE', 'Channel_Instance_Subtype_Cd': 'WEB_PORTAL',
     'Channel_Instance_Name': 'www.bank.com',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    {'Channel_Type_Cd': 'ONLINE', 'Channel_Instance_Subtype_Cd': 'WEB_PORTAL',
     'Channel_Instance_Name': 'Online Portal v2',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    {'Channel_Type_Cd': 'ONLINE', 'Channel_Instance_Subtype_Cd': 'WEB_PORTAL',
     'Channel_Instance_Name': 'Business Banking Portal',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    {'Channel_Type_Cd': 'ONLINE', 'Channel_Instance_Subtype_Cd': 'WEB_PORTAL',
     'Channel_Instance_Name': 'Secure Banking Hub',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': 'SELF_SERVICE'},
    # MOBILE (4)
    {'Channel_Type_Cd': 'MOBILE', 'Channel_Instance_Subtype_Cd': 'IOS_APP',
     'Channel_Instance_Name': 'BankApp iOS 2024',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    {'Channel_Type_Cd': 'MOBILE', 'Channel_Instance_Subtype_Cd': 'IOS_APP',
     'Channel_Instance_Name': 'BankApp iOS 2025',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    {'Channel_Type_Cd': 'MOBILE', 'Channel_Instance_Subtype_Cd': 'ANDROID_APP',
     'Channel_Instance_Name': 'BankApp Android 2024',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    {'Channel_Type_Cd': 'MOBILE', 'Channel_Instance_Subtype_Cd': 'ANDROID_APP',
     'Channel_Instance_Name': 'BankApp Android 2025',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': '24_7_AVAILABLE'},
    # CALL_CENTER (4)
    {'Channel_Type_Cd': 'CALL_CENTER', 'Channel_Instance_Subtype_Cd': 'INBOUND_CALL',
     'Channel_Instance_Name': 'Inbound Support Line #1',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': 'BUSINESS_HOURS'},
    {'Channel_Type_Cd': 'CALL_CENTER', 'Channel_Instance_Subtype_Cd': 'INBOUND_CALL',
     'Channel_Instance_Name': 'Inbound Support Line #2',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': 'BUSINESS_HOURS'},
    {'Channel_Type_Cd': 'CALL_CENTER', 'Channel_Instance_Subtype_Cd': 'OUTBOUND_CALL',
     'Channel_Instance_Name': 'Outbound Sales Line #1',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': 'BUSINESS_HOURS'},
    {'Channel_Type_Cd': 'CALL_CENTER', 'Channel_Instance_Subtype_Cd': 'INBOUND_CALL',
     'Channel_Instance_Name': 'Customer Retention Line',
     'Channel_Instance_Start_Dt': _CHANNEL_INST_START, 'Channel_Instance_End_Dt': None,
     'Convenience_Factor_Cd': 'BUSINESS_HOURS'},
]

# 10 literal campaign rows. '_offset' drives Campaign_Start_Dt (days from HISTORY_START);
# stripped before DataFrame construction.
_CAMPAIGN_TEMPLATES: List[Dict] = [
    {'_offset': 0,   'Campaign_Strategy_Cd': 'ACQUISITION',     'Campaign_Type_Cd': 'EMAIL',
     'Campaign_Classification_Cd': 'PROSPECT',       'Campaign_Name': 'New Customer Email 2025-Q4',
     'Campaign_Desc': 'Email acquisition campaign targeting new prospects',
     'Campaign_Estimated_Cost_Amt': Decimal('25000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('150000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 50000, 'Campaign_Estimated_Customer_Cnt': 2500,
     'Campaign_Estimated_Positive_Cnt': 500, 'Campaign_Estimated_Contact_Cnt': 50000},
    {'_offset': 30,  'Campaign_Strategy_Cd': 'RETENTION',       'Campaign_Type_Cd': 'DIRECT_MAIL',
     'Campaign_Classification_Cd': 'CUSTOMER',        'Campaign_Name': 'Retention Direct Mail Nov',
     'Campaign_Desc': 'Direct mail retention campaign for at-risk customers',
     'Campaign_Estimated_Cost_Amt': Decimal('18000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('90000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 10000, 'Campaign_Estimated_Customer_Cnt': 1000,
     'Campaign_Estimated_Positive_Cnt': 300, 'Campaign_Estimated_Contact_Cnt': 10000},
    {'_offset': 60,  'Campaign_Strategy_Cd': 'CROSS_SELL',      'Campaign_Type_Cd': 'DIGITAL_ADS',
     'Campaign_Classification_Cd': 'HIGH_VALUE',      'Campaign_Name': 'High Value Digital Cross-Sell',
     'Campaign_Desc': 'Digital ads targeting high-value customers for cross-sell',
     'Campaign_Estimated_Cost_Amt': Decimal('35000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('280000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 5000,  'Campaign_Estimated_Customer_Cnt': 800,
     'Campaign_Estimated_Positive_Cnt': 200, 'Campaign_Estimated_Contact_Cnt': 5000},
    {'_offset': 90,  'Campaign_Strategy_Cd': 'UP_SELL',         'Campaign_Type_Cd': 'EMAIL',
     'Campaign_Classification_Cd': 'HIGH_VALUE',      'Campaign_Name': 'Premium Upgrade Email Jan',
     'Campaign_Desc': 'Email campaign to upsell premium banking products',
     'Campaign_Estimated_Cost_Amt': Decimal('12000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('120000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 8000,  'Campaign_Estimated_Customer_Cnt': 1200,
     'Campaign_Estimated_Positive_Cnt': 240, 'Campaign_Estimated_Contact_Cnt': 8000},
    {'_offset': 120, 'Campaign_Strategy_Cd': 'WIN_BACK',        'Campaign_Type_Cd': 'DIRECT_MAIL',
     'Campaign_Classification_Cd': 'LAPSED_CUSTOMER', 'Campaign_Name': 'Win-Back Lapsed Customers Feb',
     'Campaign_Desc': 'Direct mail to re-engage lapsed banking customers',
     'Campaign_Estimated_Cost_Amt': Decimal('22000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('110000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 15000, 'Campaign_Estimated_Customer_Cnt': 900,
     'Campaign_Estimated_Positive_Cnt': 180, 'Campaign_Estimated_Contact_Cnt': 15000},
    {'_offset': 10,  'Campaign_Strategy_Cd': 'ACQUISITION',     'Campaign_Type_Cd': 'SOCIAL_MEDIA',
     'Campaign_Classification_Cd': 'PROSPECT',        'Campaign_Name': 'Social Media Acquisition Oct',
     'Campaign_Desc': 'Social media campaign to attract new digital-savvy prospects',
     'Campaign_Estimated_Cost_Amt': Decimal('30000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('200000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 80000, 'Campaign_Estimated_Customer_Cnt': 3000,
     'Campaign_Estimated_Positive_Cnt': 600, 'Campaign_Estimated_Contact_Cnt': 80000},
    {'_offset': 40,  'Campaign_Strategy_Cd': 'RETENTION',       'Campaign_Type_Cd': 'TELEMARKETING',
     'Campaign_Classification_Cd': 'CUSTOMER',        'Campaign_Name': 'Retention Telemarketing Nov',
     'Campaign_Desc': 'Outbound calls for retention of declining-balance customers',
     'Campaign_Estimated_Cost_Amt': Decimal('15000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('75000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 3000,  'Campaign_Estimated_Customer_Cnt': 600,
     'Campaign_Estimated_Positive_Cnt': 150, 'Campaign_Estimated_Contact_Cnt': 3000},
    {'_offset': 70,  'Campaign_Strategy_Cd': 'CROSS_SELL',      'Campaign_Type_Cd': 'BRANCH_EVENT',
     'Campaign_Classification_Cd': 'CUSTOMER',        'Campaign_Name': 'Branch Cross-Sell Event Dec',
     'Campaign_Desc': 'In-branch event showcasing complementary banking products',
     'Campaign_Estimated_Cost_Amt': Decimal('8000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('60000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 2000,  'Campaign_Estimated_Customer_Cnt': 400,
     'Campaign_Estimated_Positive_Cnt': 100, 'Campaign_Estimated_Contact_Cnt': 2000},
    {'_offset': 100, 'Campaign_Strategy_Cd': 'UP_SELL',         'Campaign_Type_Cd': 'DIGITAL_ADS',
     'Campaign_Classification_Cd': 'MASS_MARKET',     'Campaign_Name': 'Digital Upsell Mass Market Jan',
     'Campaign_Desc': 'Digital advertising to upsell mass-market checking customers',
     'Campaign_Estimated_Cost_Amt': Decimal('20000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('100000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 30000, 'Campaign_Estimated_Customer_Cnt': 2000,
     'Campaign_Estimated_Positive_Cnt': 400, 'Campaign_Estimated_Contact_Cnt': 30000},
    {'_offset': 130, 'Campaign_Strategy_Cd': 'BRAND_AWARENESS',  'Campaign_Type_Cd': 'EMAIL',
     'Campaign_Classification_Cd': 'MASS_MARKET',     'Campaign_Name': 'Brand Awareness Email Feb',
     'Campaign_Desc': 'Email newsletter for broad brand awareness and engagement',
     'Campaign_Estimated_Cost_Amt': Decimal('10000.0000'),
     'Campaign_Estimated_Revenue_Gain_Amt': Decimal('50000.0000'),
     'Campaign_Estimated_Base_Customer_Cnt': 100000, 'Campaign_Estimated_Customer_Cnt': 5000,
     'Campaign_Estimated_Positive_Cnt': 1000, 'Campaign_Estimated_Contact_Cnt': 100000},
]


# ── Generator ─────────────────────────────────────────────────────────────────

class Tier2Core(BaseGenerator):

    def generate(self, ctx: 'GenerationContext') -> Dict[str, pd.DataFrame]:
        # ── Step A: Guards ────────────────────────────────────────────────────
        if not ctx.customers:
            raise RuntimeError(
                'Tier2Core requires a populated ctx.customers — run UniverseBuilder.build() first'
            )
        if not ctx.agreements:
            raise RuntimeError(
                'Tier2Core requires a populated ctx.agreements — run UniverseBuilder.build() first'
            )
        for key in _REQUIRED_TIER0_TABLES:
            if key not in ctx.tables:
                raise RuntimeError(f'Tier2Core requires Tier 0 table {key} to be loaded first')

        # ── Step B: ANALYTICAL_MODEL ──────────────────────────────────────────
        model_rows: List[Dict] = []
        clv_model_id: int = -1
        for tpl in _ANALYTICAL_MODEL_TEMPLATES:
            mid = ctx.ids.next('model')
            model_rows.append({'Model_Id': mid, **tpl})
            if tpl['Model_Name'] == _CLV_MODEL_NAME:
                clv_model_id = mid

        df_model = pd.DataFrame(model_rows, columns=_COLS_ANALYTICAL_MODEL)
        df_model = df_model.astype({'Model_Id': 'Int64', 'Locator_Id': 'Int64'})

        # ── Step C: MARKET_SEGMENT ────────────────────────────────────────────
        seg_start = datetime(HISTORY_START.year, HISTORY_START.month, HISTORY_START.day)
        seg_rows: List[Dict] = []
        for i in range(1, 11):
            seg_rows.append({
                'Market_Segment_Id':       ctx.ids.next('market_seg'),
                'Model_Id':                clv_model_id,
                'Model_Run_Id':            1,
                'Segment_Desc':            f'Customer Lifetime Value decile {i} segment',
                'Segment_Start_Dttm':      seg_start,
                'Segment_End_Dttm':        None,
                'Segment_Group_Id':        pd.NA,
                'Segment_Name':            f'CLV Decile {i}',
                'Segment_Creator_Party_Id': pd.NA,
                'Market_Segment_Scheme_Id': pd.NA,
            })
        df_seg = pd.DataFrame(seg_rows, columns=_COLS_MARKET_SEGMENT)
        df_seg = df_seg.astype({
            'Market_Segment_Id': 'Int64', 'Model_Id': 'Int64', 'Model_Run_Id': 'Int64',
            'Segment_Group_Id': 'Int64', 'Segment_Creator_Party_Id': 'Int64',
            'Market_Segment_Scheme_Id': 'Int64',
        })

        # ── Step D: PRODUCT (reuse universe product_ids; never mint new ones) ─
        per_type: Dict[str, set] = {}
        for ag in ctx.agreements:
            per_type.setdefault(ag.product_type, set()).add(ag.product_id)
        for pt, id_set in per_type.items():
            if len(id_set) != 1:
                raise RuntimeError(
                    f'product_id invariant violated: {pt} has {len(id_set)} distinct IDs'
                )
        product_map = {ag.product_type: ag.product_id for ag in ctx.agreements}
        product_start = HISTORY_START - timedelta(days=3650)
        product_rows: List[Dict] = []
        for pt, pid in product_map.items():
            product_rows.append({
                'Product_Id':           pid,
                'Product_Script_Id':    pd.NA,
                'Product_Subtype_Cd':   pt,
                'Product_Desc':         None,
                'Product_Name':         pt.replace('_', ' ').title(),
                'Host_Product_Num':     f'HOST_{pt}_001',
                'Product_Start_Dt':     product_start,
                'Product_End_Dt':       None,
                'Product_Package_Type_Cd': None,
                'Financial_Product_Ind': 'Yes',
                'Product_Txt':          None,
                'Product_Creation_Dt':  None,
                'Service_Ind':          'No',
            })
        df_product = pd.DataFrame(product_rows, columns=_COLS_PRODUCT)
        df_product = df_product.astype({'Product_Id': 'Int64', 'Product_Script_Id': 'Int64'})

        # ── Step E: FEATURE ───────────────────────────────────────────────────
        feature_rows: List[Dict] = []
        for tpl in _FEATURE_TEMPLATES:
            feature_rows.append({'Feature_Id': ctx.ids.next('feature'), **tpl})
        df_feature = pd.DataFrame(feature_rows, columns=_COLS_FEATURE)
        df_feature = df_feature.astype({'Feature_Id': 'Int64'})

        # ── Step F: CHANNEL_INSTANCE ──────────────────────────────────────────
        channel_rows: List[Dict] = []
        for tpl in _CHANNEL_INSTANCE_TEMPLATES:
            channel_rows.append({'Channel_Instance_Id': ctx.ids.next('channel'), **tpl})
        df_channel = pd.DataFrame(channel_rows, columns=_COLS_CHANNEL_INSTANCE)
        df_channel = df_channel.astype({'Channel_Instance_Id': 'Int64'})

        # ── Step G: CAMPAIGN ──────────────────────────────────────────────────
        campaign_rows: List[Dict] = []
        for tpl in _CAMPAIGN_TEMPLATES:
            offset = tpl['_offset']
            start_dt = HISTORY_START + timedelta(days=offset)
            end_dt = start_dt + timedelta(days=90)
            row = {k: v for k, v in tpl.items() if k != '_offset'}
            row['Campaign_Id'] = ctx.ids.next('campaign')
            row['Parent_Campaign_Id'] = pd.NA
            row['Campaign_Level_Num'] = 1
            row['Funding_GL_Main_Account_Id'] = pd.NA
            row['Campaign_Start_Dt'] = start_dt
            row['Campaign_End_Dt'] = end_dt
            row['Currency_Cd'] = 'USD'
            row['Campaign_Creation_Dt'] = HISTORY_START
            campaign_rows.append(row)
        df_campaign = pd.DataFrame(campaign_rows, columns=_COLS_CAMPAIGN)
        df_campaign = df_campaign.astype({
            'Campaign_Id': 'Int64', 'Parent_Campaign_Id': 'Int64',
            'Funding_GL_Main_Account_Id': 'Int64',
            'Campaign_Estimated_Base_Customer_Cnt': 'Int64',
            'Campaign_Estimated_Customer_Cnt': 'Int64',
            'Campaign_Estimated_Positive_Cnt': 'Int64',
            'Campaign_Estimated_Contact_Cnt': 'Int64',
        })

        # ── Step H: PARTY ─────────────────────────────────────────────────────
        cust_by_id = {cp.party_id: cp for cp in ctx.customers}
        party_rows: List[Dict] = []
        for cp in ctx.customers:
            party_rows.append({
                'Party_Id':                    cp.party_id,
                'Party_Subtype_Cd':            _PARTY_SUBTYPE_BY_TYPE[cp.party_type],
                'Party_Desc':                  None,
                'Party_Start_Dttm':            datetime.combine(cp.party_since, time(0, 0)),
                'Party_End_Dttm':              None,
                'Party_Type_Cd':               cp.party_type,
                'Initial_Data_Source_Type_Cd': 'MDM',
            })
        df_party = pd.DataFrame(party_rows, columns=_COLS_PARTY)
        df_party = df_party.astype({'Party_Id': 'Int64'})

        # ── Step I: AGREEMENT ─────────────────────────────────────────────────
        agr_rows: List[Dict] = []
        for ag in ctx.agreements:
            agr_type = _AGREEMENT_TYPE_BY_PRODUCT[ag.product_type]
            cp = cust_by_id[ag.owner_party_id]
            agr_rows.append({
                'Agreement_Id':                  ag.agreement_id,
                'Agreement_Subtype_Cd':          ag.agreement_subtype_cd,
                'Host_Agreement_Num':            None,
                'Agreement_Name':                None,
                'Alternate_Agreement_Name':      None,
                'Agreement_Open_Dttm':           ag.open_dttm,
                'Agreement_Close_Dttm':          ag.close_dttm,
                'Agreement_Planned_Expiration_Dt': None,
                'Agreement_Processing_Dt':       ag.open_dttm.date(),
                'Agreement_Signed_Dt':           ag.open_dttm.date(),
                'Agreement_Legally_Binding_Ind': 'Yes',
                'Proposal_Id':                   pd.NA,
                'Jurisdiction_Id':               pd.NA,
                'Agreement_Format_Type_Cd':      'ELECTRONIC' if cp.has_internet else 'PAPER',
                'Agreement_Objective_Type_Cd':   _AGREEMENT_OBJECTIVE_BY_PRODUCT[ag.product_type],
                'Agreement_Obtained_Cd':         _AGREEMENT_OBTAINED_BY_PRODUCT[ag.product_type],
                'Agreement_Type_Cd':             agr_type,
                'Asset_Liability_Cd':            _ASSET_LIABILITY_BY_TYPE[agr_type],
                'Balance_Sheet_Cd':              _BALANCE_SHEET_BY_TYPE[agr_type],
                'Statement_Cycle_Cd':            None,
                'Statement_Mail_Type_Cd':        'PORTAL' if cp.has_internet else 'PAPER',
                'Agreement_Source_Cd':           None,
            })
        df_agr = pd.DataFrame(agr_rows, columns=_COLS_AGREEMENT)
        df_agr = df_agr.astype({
            'Agreement_Id': 'Int64', 'Proposal_Id': 'Int64', 'Jurisdiction_Id': 'Int64',
        })

        # ── Step J: stamp DI on all 8 DataFrames ─────────────────────────────
        df_party    = self.stamp_di(df_party,    start_ts=_TIER2_DI_START_TS)
        df_model    = self.stamp_di(df_model,    start_ts=_TIER2_DI_START_TS)
        df_seg      = self.stamp_di(df_seg,      start_ts=_TIER2_DI_START_TS)
        df_product  = self.stamp_di(df_product,  start_ts=_TIER2_DI_START_TS)
        df_feature  = self.stamp_di(df_feature,  start_ts=_TIER2_DI_START_TS)
        df_channel  = self.stamp_di(df_channel,  start_ts=_TIER2_DI_START_TS)
        df_campaign = self.stamp_di(df_campaign, start_ts=_TIER2_DI_START_TS)
        df_agr      = self.stamp_di(df_agr,      start_ts=_TIER2_DI_START_TS)

        # ── Step K: Return ────────────────────────────────────────────────────
        return {
            'Core_DB.PARTY':            df_party,
            'Core_DB.ANALYTICAL_MODEL': df_model,
            'Core_DB.MARKET_SEGMENT':   df_seg,
            'Core_DB.PRODUCT':          df_product,
            'Core_DB.FEATURE':          df_feature,
            'Core_DB.CHANNEL_INSTANCE': df_channel,
            'Core_DB.CAMPAIGN':         df_campaign,
            'Core_DB.AGREEMENT':        df_agr,
        }

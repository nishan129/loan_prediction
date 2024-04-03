import os

TRAIN_FILE_PATH = "D:\Machine Learning project\Loan\Loan Project\loan_prediction\artifact\data_ingestion\data_ingestion\train.parquet"
TEST_FILE_PATH = "D:\Machine Learning project\Loan\Loan Project\loan_prediction\artifact\data_ingestion\data_ingestion\test.parquet"
TARGET_COLUMN = "Risk_Flag"
PIPELINE_NAME:str = "loanpipe"
ARTIFACT_DIR: str = "artifact"
FILE_NAME:str = "loan.parquet"

TRAIN_FILE_NAME: str = "train.parquet"
TEST_FILE_NAME: str = "test.parquet"

PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "Data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.1

"""
Data Validation related constant  with DATA_VALIDATION VAR Name
"""
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR: str  = "validated"
DATA_VALIDATION_INVALID_DIR : str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"


"""
Data Transformation related constant with Data Transformation var name
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
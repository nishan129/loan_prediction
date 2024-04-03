import os

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
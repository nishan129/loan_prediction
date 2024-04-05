import os
from pathlib import Path

TARGET_COLUMN = "Risk_Flag"
PIPELINE_NAME:str = "loanpipe"
ARTIFACT_DIR: str = "artifact"
FILE_NAME:str = "loan.parquet"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

TRANS_TRAIN_FILE_NAME: str = "train.npy"
TRANS_TEST_FILE_NAME: str = "test.npy"

PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.h5"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
PARAMS_FILE_PATH = Path("params.yaml")



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

"""
Model Trainer related constant with Model Trainer var name
"""
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.h5"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6


"""
Model Evaluation related constant with Model Evaluation var name
"""

MODEL_EVALUATION_DIR_NAME: str = "model_evaluation"
MLFLOW_URI:str = "https://dagshub.com/nishan129/loan_prediction.mlflow"
MODEL_EVALUATION_REPORT_NAME: str = "report.yaml"
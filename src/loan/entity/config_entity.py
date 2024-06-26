from src.loan.constant.trainingpipeline import PIPELINE_NAME, ARTIFACT_DIR, DATA_INGESTION_DIR_NAME,DATA_INGESTION_COLLECTION_NAME,TRAIN_FILE_NAME,FILE_NAME,TEST_FILE_NAME, DATA_INGESTION_FEATURE_STORE_DIR,DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
from src.loan.constant import trainingpipeline
import os
from datetime import datetime
from src.loan.utils.main_utils import read_yaml_file

class TrainingPipelineConfig:
    def __init__(self, timestamp= datetime.now()):
        #timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR)
        self.timestamp: str = timestamp
        self.config = read_yaml_file(trainingpipeline.SCHEMA_FILE_PATH)
        self.all_params = read_yaml_file(trainingpipeline.PARAMS_FILE_PATH)
        
class DataIngestionConfig:
    def __init__(self, traning_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            traning_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME
        )
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,DATA_INGESTION_DIR_NAME, TRAIN_FILE_NAME
        )
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_DIR_NAME, TEST_FILE_NAME
        )
        
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME
        
class DataValidationConfig:
    def __init__(self,traning_pipeline_config:TrainingPipelineConfig):
        # Data Validation direcotry
        self.data_validation_dir:str = os.path.join(traning_pipeline_config.artifact_dir,
                                               trainingpipeline.DATA_VALIDATION_DIR_NAME)
        # Data Validation directory for valid train data and test data
        self.valid_data_dir:str = os.path.join(self.data_validation_dir,
                                                      trainingpipeline.DATA_VALIDATION_VALID_DIR)
        self.valid_train_file_path:str = os.path.join(self.valid_data_dir,
                                                      trainingpipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str = os.path.join(self.valid_data_dir,
                                                     trainingpipeline.TEST_FILE_NAME)
        # Data validation directory for invalid train data and test data
        self.invalid_data_dir:str = os.path.join(self.data_validation_dir,
                                                            trainingpipeline.DATA_VALIDATION_INVALID_DIR)
        self.invalid_train_file_path:str = os.path.join(self.invalid_data_dir,
                                                        trainingpipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str = os.path.join(self.invalid_data_dir,
                                                       trainingpipeline.TEST_FILE_NAME)
        # Data validation dircotory for data validation drift report 
        self.drift_report_file_path:str = os.path.join(self.data_validation_dir,
                                                                 trainingpipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                                 trainingpipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str = os.path.join(training_pipeline_config.artifact_dir,
                                                    trainingpipeline.DATA_TRANSFORMATION_DIR_NAME)
        
        self.transformed_train_file_path:str = os.path.join(self.data_transformation_dir,
                                                            trainingpipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                            trainingpipeline.TRANS_TRAIN_FILE_NAME) 
        
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,
                                                            trainingpipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                            trainingpipeline.TRANS_TEST_FILE_NAME)
        
        self.transformed_object_filepath: str = os.path.join(self.data_transformation_dir,
                                                                     trainingpipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                                     trainingpipeline.PREPROCSSING_OBJECT_FILE_NAME)
        
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir,
                                                   trainingpipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str = os.path.join(self.model_trainer_dir,
                                                                trainingpipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                                trainingpipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.excepted_accuracy: float = trainingpipeline.MODEL_TRAINER_EXPECTED_SCORE
        
class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(training_pipeline_config.artifact_dir,
                                                      trainingpipeline.MODEL_EVALUATION_DIR_NAME)
        self.report_file_name: str = os.path.join(self.model_evaluation_dir,
                                                  trainingpipeline.MODEL_EVALUATION_REPORT_NAME)
        self.mlflow_uri: str = trainingpipeline.MLFLOW_URI
        self.all_params = training_pipeline_config.all_params
        
        
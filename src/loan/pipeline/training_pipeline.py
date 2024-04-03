from src.loan.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from src.loan.exception import ModelException
from src.loan.logger import logging
from src.loan.components.data_ingention import DataIngestion
from src.loan.entity.artifact_entity import DataIngestionArtifact
import sys

class TrainPipeline:
    def __init__(self):
        self.trainig_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(traning_pipeline_config=self.trainig_pipeline_config)
        
        
        #self.trainig_pipeline_config= trainig_pipeline_config
        
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Start data ingestion")
            data_ingestion = DataIngestion(data_ingenstion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion completed successfully and artifact is {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise ModelException(e,sys)
            
    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)
        
    def start_data_preparation(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)
        
    def start_model_training(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)
        
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)
        
    def start_model_validation(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingenstion_artifact:DataIngestionArtifact = self.start_data_ingestion()
        except Exception as e: 
            raise ModelException(e,sys)
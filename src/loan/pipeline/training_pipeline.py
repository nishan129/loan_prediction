from src.loan.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig
from src.loan.exception import ModelException
from src.loan.logger import logging
from src.loan.components.data_ingention import DataIngestion
from src.loan.components.data_validation import DataValidation
from src.loan.components.data_transformation import DataTransform
from src.loan.components.model_trainer import ModelTrainer
from src.loan.components.model_evaluation import ModelEvaluation
from src.loan.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
import sys

class TrainPipeline:
    def __init__(self):
        self.trainig_pipeline_config = TrainingPipelineConfig()
        
        
        
        #self.trainig_pipeline_config= trainig_pipeline_config
        
        
    def start_data_ingestion(self) ->DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(traning_pipeline_config=self.trainig_pipeline_config)
            logging.info("Start data ingestion")
            data_ingestion = DataIngestion(data_ingenstion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion completed successfully and artifact is {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise ModelException(e,sys)
            
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)-> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(traning_pipeline_config=self.trainig_pipeline_config)
            logging.info("Start data validation")
            data_validation = DataValidation(data_ingenstion_artifact=data_ingestion_artifact,
                                             data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            
            logging.info(f"data validation completed successfully and artifact is {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise ModelException(e,sys)
        
    def start_data_preprocessing(self,data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(self.trainig_pipeline_config)
            logging.info(f'Start Data Transformation')
            data_transformation = DataTransform(data_validation_artifact=data_validation_artifact,
                                                data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiat_data_transform()
            logging.info(f"Data Transformation is complete {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise ModelException(e,sys)
        
    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(self.trainig_pipeline_config) 
            logging.info("Start model training")
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                         data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifacts = model_trainer.initiat_model_trainer()
            logging.info(f"Model training is complete {model_trainer_artifacts}")
            return model_trainer_artifacts
        except Exception as e:
            raise ModelException(e,sys)
        
    def start_model_evaluation(self,model_trainer_artifacts:ModelTrainerArtifact,
                               data_transformation_artifact:DataTransformationArtifact,
                               data_validation_artifact:DataValidationArtifact) -> ModelEvaluationArtifact:
        try:
            model_evaluation_config = ModelEvaluationConfig(self.trainig_pipeline_config)
            logging.info("Start Model evaluation")
            model_evaluation = ModelEvaluation(model_evaluation_config=model_evaluation_config,
                                               model_trainer_artifact=model_trainer_artifacts,
                                               data_transformation_artifact=data_transformation_artifact,
                                               data_validation_artifact=data_validation_artifact)
            model_evaluation_artifacts = model_evaluation.initiat_model_evaluation()
            model_evaluation.log_into_mlflow()
            logging.info("Model Evaluation is complete")
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
            data_validation_artifact: DataValidationArtifact = self.start_data_validation(data_ingestion_artifact=data_ingenstion_artifact)
            data_transformation_artifact: DataTransformationArtifact = self.start_data_preprocessing(data_validation_artifact)
            model_trainer_artifact: ModelTrainerArtifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact: ModelEvaluationArtifact = self.start_model_evaluation(model_trainer_artifacts=model_trainer_artifact,
                                                                                             data_transformation_artifact=data_transformation_artifact,
                                                                data_validation_artifact=data_validation_artifact)
        except Exception as e: 
            raise ModelException(e,sys)
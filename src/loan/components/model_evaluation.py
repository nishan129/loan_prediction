from src.loan.exception import ModelException
from src.loan.logger import logging
from src.loan.entity.config_entity import ModelEvaluationConfig
from src.loan.entity.artifact_entity import ModelEvaluationArtifact, ModelTrainerArtifact, DataValidationArtifact, DataTransformationArtifact
import os, sys
from src.loan.utils.main_utils import load_object, write_yaml_file, save_json
from urllib.parse import urlparse
from src.loan.constant.trainingpipeline import TARGET_COLUMN
from src.loan.ml.model.metrics import get_classification_score
import mlflow
import mlflow.keras
import tensorflow as tf
from pathlib import Path
import pandas as pd


class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                 model_trainer_artifact:ModelTrainerArtifact,
                 data_transformation_artifact:DataTransformationArtifact,
                 data_validation_artifact:DataValidationArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.data_validation_artifact = data_validation_artifact
            self.all_params = self.model_evaluation_config.all_params
        except Exception as e:
            raise ModelException(e,sys)
        
    @staticmethod
    def load_model(file_path:str) -> tf.keras.Model:
        try:
            return tf.keras.models.load_model(file_path)
        except Exception as e:
            raise ModelException(e,sys)
    
        
    def initiat_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            # loading preprocessor
            preprocesor = load_object(file_path=self.data_transformation_artifact.transformed_object_filepath)
            
            # loading train model
            self.model = self.load_model(file_path=self.model_trainer_artifact.trained_model_file_path)
            
            # loading test data
            train_data_path = self.data_validation_artifact.valid_train_file_path
            test_data_path = self.data_validation_artifact.valid_test_file_path
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)
            
            data = pd.concat([train_data,test_data])
            X_data = data.drop(columns=[TARGET_COLUMN], axis=1)
            y_data = data[TARGET_COLUMN]
            
            X_data_preproces = preprocesor.transform(X_data)
            predict = self.model.predict(X_data_preproces)
            #self.score = self.model.evaluate(X_data, y_data)
            self.train_metric = get_classification_score(y_true=y_data,y_pred=predict)
            #write_yaml_file(filename=self.model_evaluation_config.report_file_name,data=self.train_metric)
            model_evaluation_artifact = ModelEvaluationArtifact(model_evaluation_dir=self.model_evaluation_config.model_evaluation_dir,
                                                                report_file_name=self.model_evaluation_config.report_file_name,
                                                                train_model_metric_artifact=self.train_metric,
                                                                all_params=self.all_params)
            
            logging.info(f"Model Evaluation Complete and artifact is {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise ModelException(e,sys)
        
    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)
        
    def log_into_mlflow(self):
        try:
            
            mlflow.set_registry_uri(self.model_evaluation_config.mlflow_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        
            with mlflow.start_run():
                mlflow.log_params(self.all_params)
                mlflow.log_metrics(
                {"accuracy":self.train_metric.accuracy_score,"f1_score": self.train_metric.f1_score, "precision": self.train_metric.precision_score,
                 "recall":self.train_metric.recall_score}
                )
            # Model registry does not work with file store
                if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
    
                    mlflow.keras.log_model(self.model, "model", registered_model_name="ANNModel")
                else:
                    mlflow.keras.log_model(self.model, "model")
        except Exception as e:
            raise(ModelException(e,sys))


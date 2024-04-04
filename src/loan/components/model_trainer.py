from src.loan.logger import logging
from src.loan.exception import ModelException
from src.loan.entity.config_entity import ModelTrainerConfig
from src.loan.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from src.loan.utils.main_utils import  load_numpy_array_data, load_object, save_object
from src.loan.ml.model.model import ANNClassifier
from src.loan.constant.trainingpipeline import BATCH_SIZE,EPOCHS
from src.loan.ml.model.metrics import get_classification_score
from src.loan.ml.model.estimator import LoanModel
from tensorflow.keras.callbacks import EarlyStopping
import sys,os

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise ModelException(e, sys)
        
    # def train_model(self,X_train,y_train,epochs=100,batch_size=32,validation_data=None):
    #     try:
    #         logging.info("Model building start")
    #         ann_classifier = ANNClassifier(X_train,y_train)
    #         Model = ann_classifier.build_model()
    #         logging.info("Model Building end")
    #         logging.info("Model Training is start")
    #         history = Model.fit(X_train,y_train,epochs=EPOCHS)
    #         logging.info("Model training is done")
    #         return history
    #     except Exception as e:
    #         raise ModelException(e, sys)
        
    def initiat_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_filepath
            test_file_path = self.data_transformation_artifact.transformed_test_filepath
            
            # loading trainig data
            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)
            
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            
            logging.info("Model building start")
            ann_classifier = ANNClassifier(X_train,y_train)
            Model = ann_classifier.build_model()
            logging.info("Model Building end")
            logging.info("Model Training is start")
            early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1)
            history = Model.fit(X_train,y_train,epochs=EPOCHS,batch_size=BATCH_SIZE,callbacks=[early_stopping],validation_data=(X_test,y_test))
            logging.info("Model Training is done")
            logging.info(f"Model Accuracy is {history.history['accuracy'][-1]}. And Model loss is {history.history['loss'][-1]}. And Val Accuracy is {history.history['val_accuracy'][-1]}. And Validation loss is {history.history['val_loss'][-1]}")
            # Classification metrics for Train set
            train_pred = Model.predict(X_train)
            classification_metrics_train = get_classification_score(y_true=y_train,y_pred=train_pred)
            # if classification_metrics_train.f1_score >= self.model_trainer_config.excepted_accuracy:
            #     raise Exception("Train model is not good to provide accepted accuracy")
            
            # classification metrics for Test set
            predict = Model.predict(X_test)
            classification_metrics_test = get_classification_score(y_true=y_test,y_pred=predict)
            
            # Overfiting and under fiting
            # diff =  abs(classification_metrics_train.f1_score - classification_metrics_test.f1_score)
            # if diff < 0.5:
            #     raise Exception("Model is not good try to more experiment")
            
            
            #preprocesor = load_object(self.data_transformation_artifact.transformed_object_filepath)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            #model  = LoanModel(preprocessor=preprocesor,model=Model)
            #save_object(file_path=self.model_trainer_config.trained_model_file_path,object=model)
            Model.save(self.model_trainer_config.trained_model_file_path)
            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_metrics_train,
                test_metric_artifact=classification_metrics_test)
            logging.info(f"Model Trainig is Completed and artifacts is {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise ModelException(e, sys)

import tensorflow as tf
from src.loan.constant.trainingpipeline import *
import os, sys
from src.loan.utils.main_utils import  load_object
from src.loan.exception import ModelException
from src.loan.logger import logging

class Prediction:
    def __init__(self):
        self.main_dir = ARTIFACT_DIR
        self.model_dir = MODEL_TRAINER_DIR_NAME
        self.model_traind_model = MODEL_TRAINER_TRAINED_MODEL_DIR
        self.model_name = MODEL_TRAINER_TRAINED_MODEL_NAME
        self.data_transform_dir = DATA_TRANSFORMATION_DIR_NAME
        self.transform_object_path = DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR
        self.transform_object_name= PREPROCSSING_OBJECT_FILE_NAME
        
        self.transfrom = os.path.join(self.main_dir,self.data_transform_dir,self.transform_object_path,self.transform_object_name)
        self.file  = os.path.join(self.main_dir,self.model_dir,self.model_traind_model,self.model_name)
        self.model = tf.keras.models.load_model(self.file)
        self.preprocesor = load_object(self.transfrom)
    def predict(self, data):
        preprocesor = self.preprocesor
        model = self.model
        pre_data = preprocesor.transform(data)
        pred = model.predict(pre_data)
        return(pred.argmax())
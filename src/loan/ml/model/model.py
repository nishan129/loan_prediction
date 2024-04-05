import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from src.loan.constant.trainingpipeline import *
from src.loan.exception import ModelException
from src.loan.logger import logging
from src.loan.utils.main_utils import read_yaml_file
from src.loan.constant.trainingpipeline import *
import sys

class ANNClassifier:
    def __init__(self,X_train,y_train):
        try:
            self.X_train = X_train
            self.y_train = y_train
            self.model = self.build_model
            self.config = read_yaml_file(PARAMS_FILE_PATH)
        except Exception as e:
            raise ModelException(e,sys)
        
    def build_model(self):
        try:
            logging.info("ANN Model building Start")
            model = tf.keras.models.Sequential([
                                tf.keras.layers.Dense(64, activation='relu', input_shape=(self.X_train.shape[1],)),  # Input layer with 64 neurons and ReLU activation
                                tf.keras.layers.BatchNormalization(), # Batch normalization layer
                                tf.keras.layers.Dense(128, activation='relu'),  # Hidden layer with 128 neurons and ReLU activation
                                tf.keras.layers.Dropout(0.5), # Hidden Dropout layer with 0.7 persent dropout
                                tf.keras.layers.Dense(64, activation='relu'),   # Hidden layer with 64 neurons and ReLU activation
                                #tf.keras.layers.Dropout(0.3),
                                tf.keras.layers.Dense(32, activation='relu'),   # Hidden layer with 32 neurons and ReLU activation
                                tf.keras.layers.Dense(16, activation='relu'),   # Hidden layer with 16 neurons and ReLU activation
                                tf.keras.layers.Dense(8, activation='relu'),    # Hidden layer with 8 neurons and ReLU activation
                                tf.keras.layers.Dense(1, activation='sigmoid')])
            model.compile(optimizer=self.config["OPTIMIZER"], loss=self.config["LOSS"], metrics=[self.config["METRIC"]])
            logging.info("Model Building is Complete")
            return model
        except Exception as e:
            raise ModelException(e,sys)
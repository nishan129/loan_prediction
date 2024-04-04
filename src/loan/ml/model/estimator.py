from src.loan.exception import ModelException
from src.loan.logger import logging
import sys,os
class LoanModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise ModelException(e,sys)
        
    def predict(self,X):
        try:
            x_transform = self.preprocessor(X)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise ModelException(e,sys)
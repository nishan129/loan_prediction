from src.loan.constant.trainingpipeline import SCHEMA_FILE_PATH
from src.loan.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from src.loan.entity.config_entity import DataValidationConfig
from src.loan.logger import logging
from src.loan.utils.main_utils import read_yaml_file, write_yaml_file
import sys,os
from scipy.stats import ks_2samp
from src.loan.exception import ModelException
import pandas as pd
class DataValidation:
    
    def __init__(self, data_ingenstion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingenstion_artifact = data_ingenstion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise ModelException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame) -> bool:
        try:
            numeber_of_colums = len(self.schema_config['columns'])
            if len(dataframe.columns) == numeber_of_colums:
                return True
        except Exception as e:
            raise ModelException(e,sys)
        
    def is_numerical_column_is_exist(self,dataframe:pd.DataFrame) -> bool:
        try:
            numerical_columns = self.schema_config["numerical_columns"]
            datacolumns = dataframe.columns
            
            numerical_columns_prasent = True
            missing_numerical_columns = []
            
            for num_columns in numerical_columns:
                if num_columns not in datacolumns:
                    numerical_columns_prasent = False
                    missing_numerical_columns.append(num_columns)
            logging.info(f"Missing numerical columns is {missing_numerical_columns}")
            return numerical_columns_prasent
        except Exception as e:
            raise ModelException(e,sys)
        
    def is_categorical_column_is_exist(self, datafram:pd.DataFrame) -> bool:
        try:
            categorical_columns = self.schema_config['categorical_columns']
            data_columns = datafram.columns
            
            categorical_columns_present = True
            missing_categorical_columns = []
            
            for cate_col in categorical_columns:
                if cate_col not in data_columns:
                    categorical_columns_present = False
                    missing_categorical_columns.append(cate_col)
            logging.info(f"Missing categorical columns{missing_categorical_columns}")
            return categorical_columns_present
        except Exception as e:
            raise ModelException(e,sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ModelException(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)-> bool:
        try:
            status = True
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_same_dist = ks_2samp(d1,d2)
                if is_same_dist.pvalue >= threshold:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({col:{"p_value": float(is_same_dist.pvalue),
                                        "drift_status": is_found}})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            write_yaml_file(filename=drift_report_file_path,data=report)
            return status
        except Exception as e:
            raise ModelException(e,sys)
        
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            error_massage = ""
            train_file_path = self.data_ingenstion_artifact.trained_file_path
            test_file_path = self.data_ingenstion_artifact.test_file_path
            
            # Reading data from train and test file path
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            # Validate number of columns
            
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_massage = f"{error_massage}Train dataframe does not contain all columns. "
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_massage = f"{error_massage} Test dataframe does not contain all columns. "
            
            status = self.is_numerical_column_is_exist(dataframe=train_dataframe)
            if not status:
                error_massage = f"{error_massage} Train dataframe does not contain all numerical columns. "
        
            status = self.is_numerical_column_is_exist(dataframe=test_dataframe)
            if not status:
                error_massage = f"{error_massage} Test dataframe does not contain all numerical columns. "
            
            status = self.is_categorical_column_is_exist(datafram=train_dataframe)
            if not status:
                error_massage = f"{error_massage} Train dataframe does not contain all categorical columns. " 
            
            status = self.is_categorical_column_is_exist(datafram=test_dataframe)
            if not status:
                error_massage = f"{error_massage} Test dataframe does not contain all categorical columns. "
            
            if len(error_massage) > 0:
                raise Exception(error_massage)
             
            # Lets check data drift 
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            
            # To get artifcats folder
            data_validation_artifacts = DataValidationArtifact(
                validation_status=status,valid_train_file_path=self.data_ingenstion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingenstion_artifact.test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifacts}")
            return data_validation_artifacts
        except Exception as e:
            raise ModelException(e,sys)
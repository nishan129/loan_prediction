from src.loan.entity.config_entity import DataTransformationConfig
from src.loan.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact, DataTransformationArtifact
import sys
import numpy as np
import pandas as pd
from src.loan.exception import ModelException
from sklearn.compose import ColumnTransformer
from src.loan.logger import logging
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from src.loan.constant.trainingpipeline import TARGET_COLUMN
from src.loan.utils.main_utils import save_numpy_array_data,save_object

class DataTransform:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise ModelException(e,sys)
    
    @staticmethod   
    def read_data(filepath) -> pd.DataFrame:
        try:
            df  = pd.read_parquet(filepath)
            return df 
        except Exception as e:
            raise ModelException(e,sys)
        
    @classmethod
    def get_data_transform_object(cls) -> Pipeline:
        try:
            rodust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy="constant",fill_value=0)
            column_transformer = ColumnTransformer([
                ('Ohe',OneHotEncoder(sparse_output=False, handle_unknown='ignore'),[3, 4, 5, 6, 7, 8])
            ])
            preprocesor = Pipeline(steps=[
                ("imputer",simple_imputer),
                ("transformer",column_transformer),
                ("scaler",rodust_scaler)
            ])
            return preprocesor
        except Exception as e:
            raise ModelException(e,sys)
        
    def initiat_data_transform(self) -> DataTransformationArtifact:
        try:
            train_df = DataTransform.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransform.read_data(self.data_validation_artifact.valid_test_file_path)
            preprocesor =self.get_data_transform_object()
            # Trainig data frame
            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_train_df = train_df[TARGET_COLUMN]
            
            # Testing data frame
            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_test_df = test_df[TARGET_COLUMN]
            
            preprocesor_object = preprocesor.fit(input_features_train_df)
            transformed_input_train_features = preprocesor_object.transform(input_features_train_df)
            transformed_input_test_features = preprocesor_object.transform(input_features_test_df)
            
            smt = SMOTE(random_state = 42)
            
            input_features_train_final, target_features_train_final = smt.fit_resample(
                transformed_input_train_features,target_train_df
            )
            
            input_features_test_final, target_features_test_final = smt.fit_resample(
             transformed_input_test_features,  target_test_df 
            )
            
            train_arr = np.c_[input_features_train_final,np.array(target_features_train_final)]
            test_arr = np.c_[input_features_test_final,np.array(target_features_test_final)]
            
            # save numpy arrays
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            
            save_object(self.data_transformation_config.transformed_object_filepath,object=preprocesor)
            
            data_transformation_artifacts = DataTransformationArtifact(
                transformed_train_filepath=self.data_transformation_config.transformed_train_file_path,
                transformed_test_filepath=self.data_transformation_config.transformed_test_file_path,
                transformed_object_filepath=self.data_transformation_config.transformed_object_filepath)
            logging.info(f"Data transformation is complete artifact: {data_transformation_artifacts}")
            return data_transformation_artifacts
        except Exception as e:
            raise ModelException(e,sys)
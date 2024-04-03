from src.loan.exception import ModelException
from src.loan.logger import logging
from src.loan.entity.config_entity import DataIngestionConfig
from src.loan.entity.artifact_entity import DataIngestionArtifact
from src.loan.data_acess.loan_data import LoanData
import sys,os
from sklearn.model_selection import train_test_split
from pandas import DataFrame


class DataIngestion:
    def __init__(self,data_ingenstion_config:DataIngestionConfig):
        try:
            self.data_ingenstion_config = data_ingenstion_config
        except Exception as e:
            raise ModelException(e,sys)
        
    def export_data_into_feature_store(self)-> DataFrame:
        """Export mongodb collection record as data frame into feature

        Raises:
            ModelException: To get error 

        Returns:
            DataFrame: is a pandas dataframe
        """
        try:
            logging.info("Expoting data from mongodb to feature store")
            data = LoanData()
            df = data.export_collection_as_dataframe(collection_name=self.data_ingenstion_config.collection_name)
            feature_store_file_path = self.data_ingenstion_config.feature_store_file_path
            
            # Creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            df.to_parquet(feature_store_file_path,index=False)
            return df
        except Exception as e:
            raise ModelException(e,sys)
        
    def split_data_as_train_test(self, dataframe:DataFrame) -> None:
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingenstion_config.train_test_split_ratio)
            
            dir_path = os.path.dirname(self.data_ingenstion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dir_path = os.path.dirname(self.data_ingenstion_config.testing_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_set.to_parquet(self.data_ingenstion_config.training_file_path,index=False)
            test_set.to_parquet(self.data_ingenstion_config.testing_file_path,index=False)
        except Exception as e:
            raise ModelException(e,sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_articat=DataIngestionArtifact(trained_file_path=self.data_ingenstion_config.training_file_path
                                  ,test_file_path=self.data_ingenstion_config.testing_file_path)
            return data_ingestion_articat
        except Exception as e:
            raise ModelException(e,sys)
        
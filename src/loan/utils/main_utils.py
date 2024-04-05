from src.loan.exception import ModelException
import sys,os
import yaml
import dill
import numpy as np
import tensorflow as tf
from src.loan.logger import logging
import json
from pathlib import Path

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
            return data
    except Exception as e:
        raise ModelException(e,sys)
    
def write_yaml_file(filename: str, data, replace:bool = False) -> None:
    try:
        if replace:
            if os.path.exists(filename):
                os.remove(filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file:
            return yaml.dump(data,file,default_flow_style=False)
    except Exception as e:
        raise ModelException(e,sys)
    
def save_numpy_array_data(file_path:str,array:np.array):
    """
    save data numpy array
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path, 'wb') as file:
            np.save(file,array)
    except Exception as e:
        raise ModelException(e,sys)
        
def load_numpy_array_data(file_path:str) -> np.array:
    try:
        with open(file_path,'rb') as file:
            return np.load(file)
    except Exception as e:
        raise ModelException(e,sys)
    

def save_object(file_path:str, object:object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file:
            dill.dump(object,file)
    except Exception as e:
        raise ModelException(e,sys)
    
   
    
def load_object(file_path:str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file path{file_path} is not exists")
        with open(file_path,'rb') as file:
            return dill.load(file)
    except Exception as e:
        raise ModelException(e,sys)
    
    
    
    
def save_model(file_path:str, model) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok= True)
        with open(file_path, 'wb') as file:
            tf.saved_model.save(model,file)
    except Exception as e:
        raise ModelException(e,sys) 
    
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"json file saved at: {path}")
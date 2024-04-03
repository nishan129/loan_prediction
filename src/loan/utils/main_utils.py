from src.loan.exception import ModelException
import sys,os
import yaml

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
    
def writ_yaml_file(data, filename):
    with open(filename, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
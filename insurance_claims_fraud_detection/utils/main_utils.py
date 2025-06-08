import os
import sys
import pymysql
import numpy as np
import dill
import yaml

from insurance_claims_fraud_detection.logger import logging
from insurance_claims_fraud_detection.exception import Custom_Exception
from insurance_claims_fraud_detection.constants import DATABASE_NAME, HOST, USER, PASSWORD
import pandas as pd


def read_sql_data():
    logging.info("Reading SQL database started")
    try:
        mydb=pymysql.connect(
            host=HOST,
            port=int(PORT),
            user=USER,
            password=PASSWORD,
            db=DATABASE_NAME
        )
        logging.info("Connection Established")
        df=pd.read_sql_query('Select * from insurancefraud_dataset',mydb)
        print(df.head())

        return df

    except Exception as e:
        raise Custom_Exception(e,sys)
    
    
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise Custom_Exception(e, sys) from e
    


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise Custom_Exception(e, sys) from e
import os
import sys
import pymysql
import numpy as np
import dill
import yaml

from insurance_claims_fraud_detection.logger import logging
from insurance_claims_fraud_detection.exception import Custom_Exception
from insurance_claims_fraud_detection.constants import DATABASE_NAME, TABLE_NAME, HOST, PORT, USER, PASSWORD
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
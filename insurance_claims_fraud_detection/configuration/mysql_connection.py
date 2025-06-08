import sys
import os
import pymysql
import certifi

from insurance_claims_fraud_detection.exception import Custom_Exception
from insurance_claims_fraud_detection.logger import logging
from insurance_claims_fraud_detection.constants import (
    DATABASE_NAME, HOST, USER, PASSWORD
)

ca = certifi.where()

class MySQLClient:
    """
    Class Name :   MySQLClient
    Description :  This class establishes a connection to the MySQL database and can be used to export data 
                   from the MySQL feature store.
    """
    client = None

    def __init__(self) -> None:
        try:
            if MySQLClient.client is None:
                database_name = os.getenv(DATABASE_NAME)
                host = os.getenv(HOST)
                user = os.getenv(USER)
                password = os.getenv(PASSWORD)

                if not all([host, user, password, database_name]):
                    raise ValueError("Missing required environment variables.")

                mydb = pymysql.connect(
                    host=host,
                    user=user,
                    password=password,
                    db=database_name
                )

                MySQLClient.client = mydb

            self.client = MySQLClient.client
            self.database_name = os.getenv(DATABASE_NAME)

            logging.info("MySQL connection successful")

        except Exception as e:
            raise Custom_Exception(e, sys)


# if __name__ == "__main__":
#     try:
#         obj = MySQLClient()  # instantiate the class
#         print("Client object:", obj.client)  # verify connection object
#     except Exception as e:
#         print("Failed to connect:", str(e))

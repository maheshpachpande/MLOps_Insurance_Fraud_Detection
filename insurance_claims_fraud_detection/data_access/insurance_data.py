import sys
import pandas as pd
import numpy as np
from typing import Optional

from insurance_claims_fraud_detection.configuration.mysql_connection import MySQLClient
from insurance_claims_fraud_detection.exception import Custom_Exception


class InsuranceData:
    """
    This class helps export the entire MySQL table (collection) as a pandas DataFrame.
    """

    def __init__(self):
        """
        Initialize MySQLClient to interact with the MySQL database.
        """
        try:
            self.mysql_client = MySQLClient()
        except Exception as e:
            raise Custom_Exception(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Export entire MySQL table as a pandas DataFrame.
        """
        try:
            # Determine the database to use
            db_name = database_name if database_name else self.mysql_client.database_name

            # ✅ FIXED QUERY
            query = f"SELECT * FROM {db_name}.{collection_name};"

            # Execute and load data
            df = pd.read_sql_query(query, self.mysql_client.client)

            # Clean up invalid values
            df.replace({"?": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise Custom_Exception(e, sys)


# if __name__ == "__main__":
#     try:
#         # Example usage
#         insurance_data = InsuranceData()
#         df = insurance_data.export_collection_as_dataframe("insurancefraud_dataset")
#         print(df.head())  # Display the first few rows of the DataFrame
#     except Exception as e:
#         print(f"Error: {str(e)}")
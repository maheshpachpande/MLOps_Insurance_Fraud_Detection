# ------ Module Imports & Initialization ------
import os  # For directory and file path operations
import sys  # For system-specific parameters and exception info
from pandas import DataFrame  # Used for type hinting and handling data
from sklearn.model_selection import train_test_split  # To split data into train/test sets

# Project-specific module imports
from insurance_claims_fraud_detection.data_access.insurance_data import InsuranceData  # MySQL Data Access Layer
from insurance_claims_fraud_detection.entity.config_entity import DataIngestionConfig  # Config for ingestion process
from insurance_claims_fraud_detection.entity.artifact_entity import DataIngestionArtifact  # Output artifacts (train/test paths)
from insurance_claims_fraud_detection.exception import Custom_Exception  # Custom exception handling
from insurance_claims_fraud_detection.logger import logging  # For logging steps and errors

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        Initializes the DataIngestion class using the provided configuration.
        This config contains paths, table name, and split ratio.
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Custom_Exception(e, sys)

    # ------ Data Extraction ------
    def export_data_into_feature_store(self) -> DataFrame:
        """
        This method connects to MySQL via the InsuranceData layer,
        extracts the full table as a DataFrame, and stores it as a CSV file 
        in the 'feature store' directory for reproducibility and traceability.
        """
        try:
            logging.info("Exporting data from MySQL...")

            # Initialize Data Access Layer (DAL)
            insurance_data = InsuranceData()

            # Fetch data from MySQL using table name from config
            dataframe = insurance_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            logging.info(f"Shape: {dataframe.shape}")

            # Ensure the feature store directory exists
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)

            # Save extracted data as raw CSV
            dataframe.to_csv(feature_store_path, index=False)
            return dataframe

        except Exception as e:
            raise Custom_Exception(e, sys)

    # ------ Data Splitting ------
    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Splits the raw DataFrame into training and testing sets
        using the ratio defined in the config, and saves both to disk.
        """
        try:
            # Perform random train/test split
            train_set, test_set = train_test_split(
                dataframe, 
                test_size=self.data_ingestion_config.train_test_split_ratio
            )

            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)

            # Save the train and test sets as CSV files
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False)

        except Exception as e:
            raise Custom_Exception(e, sys)

    # ------ Pipeline Orchestration ------
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Orchestrates the complete data ingestion pipeline:
        1. Extracts data from MySQL and saves to a feature store.
        2. Splits data into train/test sets and saves them.
        3. Returns paths as an artifact to the training pipeline.
        """
        try:
            # Step 1: Extract and save raw data from DB
            dataframe = self.export_data_into_feature_store()

            # Step 2: Split and save train/test datasets
            self.split_data_as_train_test(dataframe)

            # Step 3: Return the file paths as part of the pipeline artifact
            return DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

        except Exception as e:
            raise Custom_Exception(e, sys)


# if __name__ == "__main__":
#     try:
#         # Example usage
#         data_ingestion_config = DataIngestionConfig()
#         data_ingestion = DataIngestion(data_ingestion_config)
#         artifact = data_ingestion.initiate_data_ingestion()
#         print(f"Data Ingestion Artifact: {artifact}")
#     except Exception as e:
#         print(f"Error: {str(e)}")
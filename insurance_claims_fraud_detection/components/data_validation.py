import json
import os
import sys
import pandas as pd

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
#from evidently.presets import DataDriftPreset

# from evidently.model_profile import Profile
# from evidently.model_profile.sections import DataDriftProfileSection
from pandas import DataFrame

from insurance_claims_fraud_detection.exception import Custom_Exception
from insurance_claims_fraud_detection.logger import logging
from insurance_claims_fraud_detection.utils.main_utils import read_yaml_file, write_yaml_file
from insurance_claims_fraud_detection.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from insurance_claims_fraud_detection.entity.config_entity import DataValidationConfig
from insurance_claims_fraud_detection.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise Custom_Exception(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise Custom_Exception(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            if missing_numerical_columns:
                logging.info(f"Missing numerical column(s): {missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            if missing_categorical_columns:
                logging.info(f"Missing categorical column(s): {missing_categorical_columns}")

            return not (missing_categorical_columns or missing_numerical_columns)
        except Exception as e:
            raise Custom_Exception(e, sys)

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Custom_Exception(e, sys)
    def detect_dataset_drift(self, reference_df, current_df):
        try:
            drift_report = Report(metrics=[DataDriftPreset()])
            drift_report.run(reference_data=reference_df, current_data=current_df)
            
            # Ensure directory exists
            report_dir = os.path.dirname(self.data_validation_config.drift_report_file_path)
            os.makedirs(report_dir, exist_ok=True)
            
            # Save HTML report (optional)
            html_path = self.data_validation_config.drift_report_file_path.replace('.yaml', '.html')
            drift_report.save_html(html_path)
            
            # Save YAML report
            report_dict = drift_report.as_dict()
            write_yaml_file(
                file_path=self.data_validation_config.drift_report_file_path,
                content=report_dict
            )
            
            # Extract drift metrics correctly
            drift_metrics = report_dict['metrics'][0]['result']
            n_features = drift_metrics['number_of_columns']
            n_drifted_features = drift_metrics['number_of_drifted_columns']
            drift_status = drift_metrics['dataset_drift']
            
            logging.info(f"{n_drifted_features}/{n_features} features drifted.")
            return drift_status
        except Exception as e:
            raise Custom_Exception(e, sys)


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            validation_error_msg = ""
            logging.info("Starting data validation")

            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)

            if not self.validate_number_of_columns(train_df):
                validation_error_msg += "Missing columns in training dataset. "

            if not self.validate_number_of_columns(test_df):
                validation_error_msg += "Missing columns in test dataset. "

            if not self.is_column_exist(train_df):
                validation_error_msg += "Some expected columns missing in training dataset. "

            if not self.is_column_exist(test_df):
                validation_error_msg += "Some expected columns missing in test dataset. "

            validation_status = len(validation_error_msg.strip()) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info("Data drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "No data drift detected"
            else:
                logging.info(f"Validation failed with message: {validation_error_msg}")

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise Custom_Exception(e, sys)
        
        
# if __name__ == "__main__":
#     # Example usage
#     try:
#         data_ingestion_artifact = DataIngestionArtifact(
#             trained_file_path="path/to/train.csv",
#             test_file_path="path/to/test.csv"
#         )
#         data_validation_config = DataValidationConfig(
#             drift_report_file_path="path/to/drift_report.yaml"
#         )
#         data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
#         data_validation.initiate_data_validation()
#     except Custom_Exception as e:
#         logging.error(f"An error occurred: {e}")

import os
import sys


DATABASE_NAME = "database_name"

HOST = "host"

USER = "user"
PASSWORD = "passwd"

COLLECTION_NAME = "insurancefraud_dataset"

PIPELINE_NAME = "insuranceClaimsFraudDetection"
ARTIFACT_DIR = "artifact"
FILE_NAME = "insurance.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

MODEL_FILE_NAME = "model.pkl"


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "insurancefraud_dataset"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
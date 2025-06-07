import os # for checking file size, existence, and creating folders.
from pathlib import Path # Converts string file paths to Path objects, making them easier to work with across different OSes (Windows, Linux, macOS).

# Define the root project directory name
project_name = "insurance_claims_fraud_detection"

# List of files and directories to create for the MLOps-based insurance fraud detection project
list_of_files = [

    # Python package initialization
    f"{project_name}/__init__.py", #marks a directory as a Python package. Without it, Python won't recognize the folder as a module you can import from.

    # Components for different stages of the ML pipeline
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",       # Handles reading and importing data
    f"{project_name}/components/data_validation.py",      # Validates schema, nulls, etc.
    f"{project_name}/components/data_transformation.py",  # Data cleaning, encoding, scaling, etc.
    f"{project_name}/components/model_trainer.py",        # ML model training logic
    f"{project_name}/components/model_evaluation.py",     # Evaluates model performance
    f"{project_name}/components/model_pusher.py",         # Pushes model to production or registry

    # Configuration folder to manage config settings
    f"{project_name}/configuration/__init__.py",

    # Constants folder to hold constant values used throughout the project
    f"{project_name}/constants/__init__.py",

    # Entity definitions for configs and artifacts (like DTOs)
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",            # Config entities for different pipeline stages
    f"{project_name}/entity/artifact_entity.py",          # Artifact entities representing output from each stage

    # Custom exception handling
    f"{project_name}/exception/__init__.py",

    # Logging functionality
    f"{project_name}/logger/__init__.py",

    # Pipeline orchestration folder
    f"{project_name}/pipline/__init__.py",
    f"{project_name}/pipline/training_pipeline.py",       # Script to run full training pipeline
    f"{project_name}/pipline/prediction_pipeline.py",     # Script for running inference/predictions

    # Utility functions
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",                # Main utility functions like reading config, saving files

    # Application entry point
    "app.py",

    # Required dependencies for the project
    "requirements.txt",

    # Docker configuration files
    "Dockerfile",
    ".dockerignore",

    # Demo script for testing the pipeline
    "demo.py",

    # Package setup script for pip installation
    "setup.py",

    # YAML configuration files for model and data schema
    "config/model.yaml",
    "config/schema.yaml",
]

# Create directories and files from the list
for filepath in list_of_files:
    filepath = Path(filepath)  # Convert string to Path object for OS-independent handling
    filedir, filename = os.path.split(filepath)  # Split path into directory and file

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)  # Create directory if it doesn’t exist

    # Create empty file if it doesn't exist or is empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass  # Create an empty file
    else:
        print(f"file is already present at: {filepath}")

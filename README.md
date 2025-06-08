# MLOps_Insurance_Fraud_Detection
**MLOps_Insurance_Fraud_Detection** is an end-to-end pipeline that automates the development, deployment, monitoring, and retraining of machine learning models to detect fraudulent insurance claims efficiently and reliably.

Workflow:
1. Constant 
    - Returns all the constant values(give user, password, etc.)

2. Entity 
    - (artiact_entity: Returns Output of conponent), 

    - (config_entity: it will use constant to create path and provide in Data Ingestion......)

3. Configuration: for database connection....

4. Data Access: 
    - insurance_data.py : it will from database to dataframe. 
    - returns df.head()

4. Component:
    - data_ingestion.py : it will read data from database and store in local.

5. Pipeline:
    - pipeline.py : it will call all the component and data access.



6. How to **DVC** involved in this project?:

        - git init (Initializes a new Git repository to track code, config files, and DVC metadata.)

        - dvc init (Sets up DVC in the project by creating .dvc/ folder and .dvcignore file. Adds DVC configurations to .git.)

        - dvc add data/ (Tells DVC to track the raw_data.csv file. DVC replaces the actual file with a .dvc file and moves data to DVC cache.)

        - git add data.dvc .gitignore (Adds the .dvc file and .gitignore to Git. The actual data file is excluded from Git using .gitignore.)

        - git commit -m "Add raw_data.csv to DVC tracking" (Saves the tracked .dvc metadata file to Git history for versioning.)

        - dvc remote add -d myremote gdrive://<your-drive-id> 
        (Create a Remote Storage for DVC (e.g., Google Drive, S3, Azure, etc.) 
        Configures a default DVC remote for storing actual data files. Replace gdrive:// with your preferred storage.)

        - dvc push
        (Uploads the actual large data file (not tracked by Git) to the remote DVC storage.)

        - git add .
        - git commit -m "Add initial data processing script"
        (Tracks and versions your code/scripts as usual with Git.)

        - git push -u origin main
        (Pushes all committed code, pipeline files, and DVC metadata to GitHub.)

7. a



- dvc init (creates .dvcignore, .dvc)

- dvc remote add -d myremote s3       
<!-- {Create a Remote Storage for DVC (e.g., Google Drive, S3, Azure, etc.)
dvc remote add -d myremote gdrive://<your-drive-id>} -->
- dvc add artifact//
- git add .gitignore data.dvc
- dvc commit  
- dvc push
- git add .
- git commit -m "Add initial data processing script"
    (Tracks and versions your code/scripts as usual with Git.)

- git push -u origin main
    (Pushes all committed code, pipeline files, and DVC metadata to GitHub.)
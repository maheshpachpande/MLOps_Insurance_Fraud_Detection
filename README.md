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

    - dvc init (creates .dvcignore, .dvc)

    - dvc remote add -d myremote s3       
    <!-- {Create a Remote Storage for DVC (e.g., Google Drive, S3, Azure, etc.)
    dvc remote add -d myremote gdrive://<your-drive-id>} -->

    - /s3 folder added in .gitignore

    - dvc add artifact//
    - git add .gitignore data.dvc
    - dvc commit  
    - dvc push
    - git add .

    - git commit -m "Add initial data processing script"
        (Tracks and versions your code/scripts as usual with Git.)

    - git push -u origin main
        (Pushes all committed code, pipeline files, and DVC metadata to GitHub.)


7. a

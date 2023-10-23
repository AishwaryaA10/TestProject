from snowflake.snowpark.session import Session
import os
import joblib
import pandas as pd
import sys

def load_model(staged_model_f_name: str, stage_name: str):
    # Define model location
    IMPORT_DIR = sys._xoptions["snowflake_import_directory"]
    model_f_path = os.path.join(IMPORT_DIR, staged_model_f_name)
    
    # Load the model and initialize the predictor
    model = joblib.load(model_f_path)
    return model

def main(
    args: list, 
    staged_model_f_name: str,
    stage_name: str
    )-> bool:

    # Load model from stage
    model = load_model(staged_model_f_name, stage_name)

    # transform record
    inputs = [
        'SALARY', 'SENIORITY', 'TENURE_MONTHS', 'MONTHS_AFTER_COLLEGE', 'BIRTH_YEAR', 'OVERTIME_HOURS',
        'MAPPED_ROLE_CLEAN', 'SEX', 'ETHNICITY', 'HOSPITAL_TYPE', 'HOSPITAL_OWNERSHIP', 'COMPANY_NAME', 'CITY_STATE', 'DISTANCE', 'DEGREE_CLEAN'
    ]
    row = pd.DataFrame([args], columns=inputs)
    X_row = row[inputs]
    prediction = model.predict(X_row)[0]
    if prediction == 0:
        return False
    else:
        return True
    #return bool(model.predict(X_row)[0])
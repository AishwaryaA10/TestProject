import os
from joblib import dump
import inspect
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report
from snowflake.snowpark.session import Session
import snowflake.snowpark.types as T
import snowflake.snowpark.functions as F

def stage_data_for_ml(session, table_name, target_col, excluded_cols):
    # Load data
    df_raw = (session
        .table(f'{table_name}')
        .filter(F.col("JOB_ENDDATE").is_not_null())
        .toPandas())

    # Exclude columns
    excluded_cols.append(target_col)
    df_exc = df_raw.loc[:, ~df_raw.columns.isin(excluded_cols)]
    
    # Get numeric and cat features
    numeric_features = df_exc.select_dtypes(include=np.number).columns.tolist()
    categorical_features = df_exc.select_dtypes(include=['object']).columns.tolist()
    
    # Dedupe inputs
    X_raw = df_raw[numeric_features + categorical_features]
    y_raw = df_raw[target_col]
    X     = X_raw.drop_duplicates()
    y     = y_raw[X.index]

    # Train-test splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, random_state=123, stratify=y)

    # Convert data from numpy arrays to pandas dataframes
    X_train_pdf = pd.DataFrame(X_train, columns=X.columns)
    X_test_pdf = pd.DataFrame(X_test, columns=X.columns)
    y_train_pdf =  pd.DataFrame(y_train, columns=[target_col])
    y_test_pdf = pd.DataFrame(y_test, columns=[target_col])

    return X, y, numeric_features, categorical_features, X_train_pdf, X_test_pdf, y_train_pdf, y_test_pdf

def my_train_test_split(X, y):
    # Train-test splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, random_state=123, stratify=y)

    # Convert data from numpy arrays to pandas dataframes
    X_train_pdf = pd.DataFrame(X_train, columns=X.columns)
    X_test_pdf = pd.DataFrame(X_test, columns=X.columns)
    y_train_pdf =  pd.DataFrame(y_train, columns=[y.columns[0]])
    y_test_pdf = pd.DataFrame(y_test, columns=[y.columns[0]])

    return X_train_pdf, X_test_pdf, y_train_pdf, y_test_pdf

def define_ml_pipeline(numeric_features, categorical_features):
    # Add numeric transformer
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    # Add categorical transformer
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
        ])

    # Build data preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    # Build ml pipeline
    pipe = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', RandomForestClassifier(n_estimators=10, 
                                                                class_weight='balanced_subsample',
                                                                random_state=123))])

    # Define parameter search space for grid search
    param_grid = {
        'classifier__n_estimators': [100],
        'classifier__max_depth' : [4],
        'classifier__criterion' :['gini']
        }

    # Define grid search object
    ml_pipeline = GridSearchCV(
        estimator = pipe, 
        param_grid=param_grid,  
        cv=3, 
        scoring='f1_micro'
        )
    
    return ml_pipeline

def evaluate_model_performance(ml_pipeline, X_test, y_test):
    # Generate predictions
    y_pred = ml_pipeline.predict(X_test)

    # Generate classification report 
    clf_report = classification_report(y_test, y_pred, output_dict=True)
    clf_report_pdf = pd.DataFrame(clf_report).transpose()

    # Generate confusion matrix
    labels = np.unique(np.append(y_test,y_pred))
    cnf_matrix =  confusion_matrix(y_test,y_pred,labels=labels)
    cnf_matrix_pdf = pd.DataFrame(cnf_matrix, index=[f'{x}_Predicted' for x in labels], columns=[f'{x}_Actual' for x in labels]).reset_index(drop=False)

    # Extract feature importances
    features_names = ml_pipeline.best_estimator_.named_steps['preprocessor'].get_feature_names_out()
    feature_importances = ml_pipeline.best_estimator_.named_steps["classifier"].feature_importances_

    # Zip coefficients and names together and make a DataFrame
    zipped = zip(features_names, feature_importances)
    feature_importances_pdf = pd.DataFrame(zipped, columns=["feature", "value"])

    return clf_report_pdf, cnf_matrix_pdf, feature_importances_pdf

def save_artifacts_into_stage(session, artifacts, experiment_name, local_path, stage_name):
    # Check local directory
    os.makedirs(f'{local_path}/{experiment_name}/', exist_ok=True)

    # Save pandas dataframes
    pandas_dfs = artifacts['data']['objects']
    pandas_dfs_names = artifacts['data']['names']
    for pdf, f_name in zip(pandas_dfs, pandas_dfs_names):
        f_path = f'{local_path}/{experiment_name}/{f_name}.csv'
        pdf.to_csv(f_path, index=None)
        session.file.put(f_path, f'@{stage_name}/{experiment_name}', auto_compress=False, overwrite=True)

    # Save binaries locally
    binaries = artifacts['binaries']['objects']
    binaries_names = artifacts['binaries']['names']
    for binary, f_name in zip(binaries, binaries_names):
        f_path = f'{local_path}/{experiment_name}/{f_name}.joblib'
        dump(binary, f_path)
        session.file.put(f_path, f'@{stage_name}/{experiment_name}',auto_compress=False, overwrite=True)


def main(session: Session, table_name: str, target_col: str, excluded_cols: list, experiment_name: str, stage:str) -> T.Variant:
    # 1. Clean Data
    X, y, numeric_features, categorical_features, X_train_pdf, X_test_pdf, y_train_pdf, y_test_pdf = stage_data_for_ml(session, table_name, target_col, excluded_cols)

    # 2. Create data preprocessor and pipeline
    ml_pipeline = define_ml_pipeline(numeric_features, categorical_features)
    
    # 3. Fit ML pipeline
    ml_pipeline.fit(X_train_pdf, y_train_pdf)
    best_estimator = ml_pipeline.best_estimator_

    # 4. Evaluate training results
    clf_report_pdf, cnf_matrix_pdf, feature_importances_pdf = evaluate_model_performance(ml_pipeline, X_test_pdf, y_test_pdf)

    # 5. Save artifacts to stage
    artifacts = {
        'data' : 
        {
            'names'  : ['X', 'y', 'X_train', 'X_test', 'y_train', 'y_test', 'clf_report', 'cnf_matrix', 'feature_importances'],
            'objects': [X, y, X_train_pdf, X_test_pdf, y_train_pdf, y_test_pdf, clf_report_pdf, cnf_matrix_pdf, feature_importances_pdf]
        },
        'binaries' : 
        {
            'names'  : ['ml_pipeline'],
            'objects': [ml_pipeline]
        }
    }
    res = save_artifacts_into_stage(session, artifacts, experiment_name, 'tmp', stage)
    
    return clf_report_pdf.to_dict()
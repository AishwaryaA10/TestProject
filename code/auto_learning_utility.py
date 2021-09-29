import numpy as np
import pandas as pd

from typing import Tuple, List
from sklearn.base import BaseEstimator

import configparser
config = configparser.ConfigParser()
config.read('/notebooks/notebooks/code/config.ini')

ci_distance_threshold = int(config.get('Threshold','ci_distance_threshold'))
weighted_proba_threshold =float(config.get('Threshold','weighted_proba_threshold'))
ci_similarity_threshold = float(config.get('Threshold','ci_similarity_threshold'))
time_diff_minutes_threshold = int(config.get('Threshold','time_diff_minutes_threshold'))
time_diff_seconds_threshold = int(config.get('Threshold','time_diff_seconds_threshold'))

class RuleAugmentedEstimator(BaseEstimator):

    def __init__(self, base_model: BaseEstimator, ai: List, **base_params):
        self.ai = ai
        self.base_model = base_model
        self.base_model.set_params(**base_params)

    def rules(self,row,*args,**kwargs):
        if row['ci_distance'] <= 2 and row['kb'] == 1:
            return 1
        if row['ci_distance'] <= 2 and row['kb'] == 0:
            return 1
        if row['ci_distance'] in range(3,5) and row['time_diff'] <= 10 and row['kb'] == 1:
            return 1
        if row['ci_distance'] in range(3,5) and row['time_diff'] <= 10 and row['kb'] == 0:
            return 1
        if row['ci_distance'] in range(5,ci_distance_threshold) and row['time_diff'] <=5 and row['kb'] == 1:
            return 1 #,"ci_distance"
        if row['ci_distance'] in range(5,ci_distance_threshold) and row['time_diff'] <=5 and row['kb'] == 0:
            return 1 #,"ci_distance"
        if row['application_service'] == 1 and row['time_diff'] <=time_diff_minutes_threshold:
            return 1 #,"application_service"
        if row['u_business_service'] == 1 and row['time_diff_s'] <=time_diff_seconds_threshold:
            return 1 #,"business_service"
        if row['cr_comp'] == 1:
            return 1 #,"change_request"
        if row['ci_similarity'] >= ci_similarity_threshold:
            return 1 #,"ci_similarity"
        if row['weighted_proba'] >= weighted_proba_threshold:
            return 1 #,"weighted_proba"
        
    def _get_base_model_data(self, X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
        """Filters the trainig data for data points not affected by the rules."""
        train_X = X
        train_y = y
        return train_X,train_y
    
    def fit(self, X: pd.DataFrame, y: pd.Series, **kwargs):
        train_X, train_y = self._get_base_model_data(X, y)
        self.base_model.fit(train_X, train_y, **kwargs)
        
        
    def predict(self, X: pd.DataFrame) -> np.array:        
        if "base_ai" in self.ai:
            prediction = X.apply(self.rules, axis=1)
            prediction.fillna(0,inplace=True)
            return prediction.values
        if "auto_learning" in self.ai:
            prediction = self.base_model.predict(X)
            return prediction
        if "base_ai_auto_learning" in self.ai:
            p_X = X.copy()
            p_X['prediction'] = np.nan
            p_X['prediction'] = X.apply(self.rules, axis=1)
            if len(p_X.loc[p_X['prediction'].isna()].index != 0):
                base_X = p_X.loc[p_X['prediction'].isna()].copy()
                base_X.drop('prediction', axis=1, inplace=True)
                p_X.loc[p_X['prediction'].isna(), 'prediction'] = self.base_model.predict(base_X)
            return p_X['prediction'].values
    
    def predict_proba(self, X: pd.DataFrame) -> np.array:        
        if "base_ai" in self.ai:
            return 1.0
        if "auto_learning" in self.ai:
            prediction = self.base_model.predict_proba(X)[:,1]
            return prediction
        if "base_ai_auto_learning" in self.ai:
            p_X = X.copy()
            p_X['prediction'] = np.nan
            p_X['prediction'] = X.apply(self.rules, axis=1)
            if len(p_X.loc[p_X['prediction'].isna()].index != 0):
                base_X = p_X.loc[p_X['prediction'].isna()].copy()
                base_X.drop('prediction', axis=1, inplace=True)
                p_X.loc[p_X['prediction'].isna(), 'prediction'] = self.base_model.predict_proba(base_X)[:,1]
            return p_X['prediction'].values
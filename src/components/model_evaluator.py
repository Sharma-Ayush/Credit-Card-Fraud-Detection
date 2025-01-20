from src.logger import logging

from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from imblearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from sklearn.metrics import auc, precision_recall_curve

class ModelEvaluator:
    '''
    A class for evaluating our model on given data.
    '''
    def evaluate(self, pre_processor, model, X, Y, scorer_func, name_for_data):
        '''
        Method Description: Model evaluation method.
        Takes in the pre-processor, model, X, Y, scorer function, name or title of the data set and returns evaluation score.
        '''
        logging.info(f'Initiating model evaluation for {name_for_data} data set...')

        X_transformed = pre_processor.transform(X)
        Y_pred = model.predict_proba(X_transformed)

        score = scorer_func(Y, Y_pred[:, 1])

        logging.info(f'Successfully completed model evaluation for {name_for_data} data set with score  = {score}!!!')
        return score 
from src.logger import logging

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

class ModelTrainer:
    '''
    A class for training our model for training pipeline
    '''
    def train_model(self, model, params, X_train, Y_train):
        '''
        Method Description: Model training method
        Set parameters for model and fit it.
        '''
        logging.info('Initiating model training...')

        # Set the parameters for the model
        model.set_params(**params)

        # Fit the model
        model.fit(X_train, Y_train)

        logging.info(f'Successfully completed model training!!!')
from src.logger import logging

from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from imblearn.pipeline import Pipeline

class DataPreProcessor:
    '''
    A class for data pre-processing of raw data so that it can be used for training pipeline or prediction pipeline
    '''

    def transform(self, pre_processor, X):
        '''
        Method Description: Pre-processor transform method.
        Takes in the pre-processor, X_train and returns transformed X_train.
        '''
        logging.info('Initiating data pre-processing for model evaluation or prediction...')

        X_transformed = pre_processor.transform(X)
        
        logging.info('Successfully completed data pre-processing for model evaluation or prediction!!!')
        return X_transformed

    def fit_transform(self, pre_processor, X_train, Y_train):
        '''
        Method Description: Pre-processor fit and transform method.
        Takes in the pre-processor, X_train, Y_train. Fits the pre-processor, transforms X_train and returns it.
        '''
        logging.info('Initiating data pre-processing of train set for training...')

        X_train_transformed = pre_processor.fit_transform(X_train, Y_train)

        logging.info('Successfully completed data pre-processing of train set!!!')
        return X_train_transformed
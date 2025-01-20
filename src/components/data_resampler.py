from src.logger import logging

from imblearn.over_sampling import SMOTE

class DataResampler:
    '''
    A class for data resampling of pre-processed train data so that it can be used for training pipeline
    '''
    def fit_resample(self, resampler, X_train, Y_train):
        '''
        Method Description: Resampler fit and transform method.
        Takes in the resampler, X_train, Y_train. Fits the resampler, transforms X_train and returns it.
        '''
        logging.info('Initiating data resampling of train set for training...')

        X_train_transformed, Y_train_transformed = resampler.fit_resample(X_train, Y_train)

        logging.info('Successfully completed data transformation of train set!!!')
        return (X_train_transformed, Y_train_transformed)
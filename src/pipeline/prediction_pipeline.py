import os
import sys
import pandas as pd
from dataclasses import dataclass

from src.components.data_transformation import DataPreProcessor
from src.utils import load_object

from src.logger import logging
from src.exception import CustomError

@dataclass
class PredictionPipelineConfig:
    '''
    A data class for storing paths related to prediction pipeline
    '''
    preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
    model_file_path = os.path.join('artifacts', 'model.pkl' )

class PredictPipeline:
    '''
    A class for running the prediction pipeline
    '''
    def __init__(self):
        self.prediction_pipeline_config = PredictionPipelineConfig()

    def transform(self, pre_processor, X):
        '''
        Take in the pre-processor, X, Y and pre-process X & Y to return the transformed version of X for prediction
        '''
        data_transformation = DataPreProcessor()
        X_transformed = data_transformation.transform(pre_processor, X)
        
        return X_transformed

    def run_pipeline(self, X, fraud_prob_threshold = 0.5):
        logging.info('Initiating prediction pipeline...')
        try:
            # Loading model and pre-processor
            logging.info('Loading model and pre-processor...')
            model = load_object(self.prediction_pipeline_config.model_file_path)
            preprocessor = load_object(self.prediction_pipeline_config.preprocessor_path)
            logging.info('Successfully completed loading of model and pre-processor!!!')

            # Transforming X by passing it to the pre-processor
            X_transformed = self.transform(preprocessor, X)

            # Predicting the probabilities
            prediction = model.predict_proba(X_transformed)
        except:
            error_obj = CustomError(*sys.exc_info())
            logging.error(error_obj, exc_info = True)
            raise error_obj
        else:
            logging.info('Successfully completed prediction pipeline!!!')

            # Based on given threshold determine whether the transaction is Fraudulent or Genuine
            if prediction[0, 1] > fraud_prob_threshold:
                return "Fraudulent transaction"
            else:
                return "Genuine transaction"
import sys
import os
from dataclasses import dataclass
import numpy as np

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataPreProcessor
from src.components.model_trainer import ModelTrainer
from src.components.data_resampler import DataResampler
from src.components.model_evaluator import ModelEvaluator
from src.utils import load_object, area_under_precision_recall_curve, save_object, double_log_transform, cube_root_transform

from src.exception import CustomError
from src.logger import logging

@dataclass
class TrainingPipelineConfig:
    '''
    A data class for storing paths related to training pipeline
    '''
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")
    model_obj_file_path = os.path.join("artifacts", "model.pkl")

class TrainingPipeline:
    '''A class for running the whole training pipeline'''
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def ingest_data(self, path, target_class, test_size, random_state):
        '''
        Loads data from given file path of csv file, splits it into test-train, saves the data and returns it further for data transformation
        '''
        data_ingestion = DataIngestion()
        data_arr = data_ingestion.ingest_data(path, target_class, test_size, random_state)

        return data_arr

    def transform_data_with_resampling(self, pre_processor, resampler, X_train, Y_train):
        '''
        Take in the pre-processor, resampler, X_train, Y_train and pre-process X_train & Y_train to return the transformed versions for model training
        '''
        # fitting pre-processor and transforming X_train
        data_transformation = DataPreProcessor()
        X_train_transformed = data_transformation.fit_transform(pre_processor, X_train, Y_train)

        # fitting resampler and resampling already transformed X_train
        data_resampler = DataResampler()
        X_train_transformed, Y_train_transformed = data_resampler.fit_resample(resampler, X_train_transformed, Y_train)

        return (X_train_transformed, Y_train_transformed)
        
    def transform_data_without_resampling(self, pre_processor, X, Y):
        '''
        Take in the pre-processor, X, Y and pre-process X & Y to return the transformed version of X for model evaluation or prediction
        '''
        data_transformation = DataPreProcessor()
        X_transformed = data_transformation.transform(pre_processor, X, Y)
        
        return X_transformed
        
    def train_model(self, model, params, X_train, Y_train):
        '''
        Take in the model, parameters, transformed-resampled train set and fit on it
        '''
        model_trainer = ModelTrainer() 

        return model_trainer.train_model(model, params, X_train, Y_train)  
        
    def evaluate_model(self, pre_processor, model, X, Y, scorer_func, name_for_data):
        '''
        Take in the pre-processor, model, X, Y, scorer function, name or title for data set and return the evaluation score
        '''
        model_evaluator = ModelEvaluator() 
        score = model_evaluator.evaluate(pre_processor, model, X, Y, scorer_func, name_for_data)  

        return score      
    
    def find_best_model(self, models_data, greater_is_better = True):
        '''
        Find the best modesl index in models_data which has the best test score
        '''
        if greater_is_better:
            best_model_score = -np.inf
            for index, model in enumerate(models_data):
                if model['test_score'] > best_model_score:
                    best_model_index = index
                    best_model_score = model['test_score']
        else:
            best_model_score = np.inf
            for index, model in enumerate(models_data):
                if model['test_score'] < best_model_score:
                    best_model_index = index
                    best_model_score = model['test_score']  

        return best_model_index

    def run_pipeline(self, score_threshold, ingestion_path = 'notebook/Data/creditcard.csv'):
        logging.info('Started training pipeline...')
        try:
            # Loading the data
            X_train, X_test, Y_train, Y_test = self.ingest_data(ingestion_path, 'Class', 0.33, 42)

            # Loding the pre-processor and model configurations
            models_data = load_object('notebook/models/models_data.pkl')

            for model in models_data:
                logging.info(f'For model - {model['name'].replace("_", " ")}:')

                # Transforming data by pre-processing and resampling
                X_train_transformed, Y_train_transformed = self.transform_data_with_resampling(model['pre-processor'],
                                                                                               model['resampler'],
                                                                                               X_train,
                                                                                               Y_train)

                # Training the model
                self.train_model(model['model'],
                                 model['best_params'],
                                 X_train_transformed,
                                 Y_train_transformed)
                
                # Evaluating model on train set
                model['train_score'] = self.evaluate_model(model['pre-processor'], model['model'], X_train, Y_train, area_under_precision_recall_curve, 'train')

                # Evaluating model on test set
                model['test_score'] = self.evaluate_model(model['pre-processor'], model['model'], X_test, Y_test, area_under_precision_recall_curve, 'test')

            # Finding best model based on test score
            best_model_index = self.find_best_model(models_data)

            if models_data[best_model_index]['test_score'] >= score_threshold:
                # saving the best model
                save_object(self.training_pipeline_config.preprocessor_obj_file_path, models_data[best_model_index]['pre-processor'])
                save_object(self.training_pipeline_config.model_obj_file_path, models_data[best_model_index]['model'])
                print(f"Training pipeline completed.")
                print(f'Best model - {models_data[best_model_index]['name'].replace("_", " ")}')
                print(f'Train Score - {models_data[best_model_index]['train_score']}')
                print(f'Test Score - {models_data[best_model_index]['test_score']}')
                logging.info(f'Best model - {models_data[best_model_index]['name'].replace("_", " ")}. Train Score - {models_data[best_model_index]['train_score']}. Test Score - {models_data[best_model_index]['test_score']}')
            else:
                print(f'No appropriate model found based on scoring threshold of {score_threshold}')
        except:
            error_obj = CustomError(*sys.exc_info())
            logging.error(error_obj, exc_info = True)
            raise error_obj
        else:
            save_object(self.training_pipeline_config.preprocessor_obj_file_path, models_data[best_model_index]['pre-processor'])
            save_object(self.training_pipeline_config.model_obj_file_path, models_data[best_model_index]['model'])
            logging.info('Successfully completed training pipeline!!!')

if __name__ == "__main__":
    training_pipeline_obj = TrainingPipeline()
    training_pipeline_obj.run_pipeline(0.6)

    
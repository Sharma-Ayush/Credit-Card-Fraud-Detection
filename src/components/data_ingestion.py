import os
import sys
from src.exception import CustomError
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    '''A data class for storing paths related to data files storage'''
    raw_data_path = os.path.join("artifacts", "data.csv")
    train_data_path = os.path.join("artifacts", "train.csv")
    test_data_path = os.path.join("artifacts", "test.csv")

class DataIngestion:
    '''To import data, split it into test-train data, and save the files in pre-defined paths'''

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def load_data(self, path):
        return pd.read_csv(path)
    
    def split_data(self, df, target_class, test_size, random_state):
        return train_test_split(df.drop(target_class, axis = 1),
                                df[target_class],
                                stratify = df[target_class],
                                test_size = test_size,
                                random_state = random_state)
    
    def save_data(self, df, path):
        df.to_csv(path, 
                  index = False,
                  header = True)

    def ingest_data(self):
        logging.info("Started data ingestion...")
        try:
            # load data
            df = self.load_data('notebook/Data/creditcard.csv')

            # create required directories, if not exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True)

            # split the dataset
            X_train, X_test, Y_train, Y_test = self.split_data(df, 
                                                               target_class = 'Class',
                                                               test_size = 0.2,
                                                               random_state = 42)

            # save the data to files
            self.save_data(df, self.ingestion_config.raw_data_path)
            self.save_data(pd.concat((X_train, Y_train), axis = 1), self.ingestion_config.train_data_path)
            self.save_data(pd.concat((X_test, Y_test), axis = 1), self.ingestion_config.test_data_path)
        except:
            error_obj = CustomError(*sys.exc_info())
            logging.error(error_obj, exc_info = True)
            raise error_obj
        else:
            logging.info("Successfully completed data ingestion!!!")

            return (self.ingestion_config.train_data_path,
                    self.ingestion_config.test_data_path)
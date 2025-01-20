import os
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    '''
    A data class for storing paths related to data files storage
    '''
    raw_data_path = os.path.join("artifacts", "data.csv")
    train_data_path = os.path.join("artifacts", "train.csv")
    test_data_path = os.path.join("artifacts", "test.csv")

class DataIngestion:
    '''
    A class for ingesting data to be used in training pipeline
    '''
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def save_data(self, df, path):
        '''
        Save dataframe as a csv file in given path without index but with header included
        '''
        df.to_csv(path, 
                  index = False,
                  header = True)

    def ingest_data(self, path, target_class, test_size, random_state):
        '''
        Method Description: Data ingestion method
        Loads the data from given csv file path, splits it into train-test data, saves them into csv files.
        Returns the splitted data as a tuple of format (X_train, X_test, Y_train, Y_test)
        '''
        logging.info('Initiating data ingestion...')

        # load data and drop duplicates
        df = pd.read_csv(path)
        df.drop_duplicates(inplace = True)

        # create required directories, if not exist
        os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True)

        # split the dataset
        X_train, X_test, Y_train, Y_test = train_test_split(df.drop(target_class, axis = 1),
                                                            df[target_class],
                                                            stratify = df[target_class],
                                                            test_size = test_size,
                                                            random_state = random_state)

        # save the data to files
        self.save_data(df, self.ingestion_config.raw_data_path)
        self.save_data(pd.concat((X_train, Y_train), axis = 1), self.ingestion_config.train_data_path)
        self.save_data(pd.concat((X_test, Y_test), axis = 1), self.ingestion_config.test_data_path)

        logging.info("Successfully completed data ingestion!!!")
        return (X_train, X_test, Y_train, Y_test)
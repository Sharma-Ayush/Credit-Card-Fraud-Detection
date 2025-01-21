from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split

class DataIngestion:
    '''
    A class for ingesting data to be used in training pipeline
    '''
    def ingest_data(self, path, target_class, test_size, random_state):
        '''
        Method Description: Data ingestion method
        Loads the data from given csv file path, drops duplicates and splits the data into train-test data.
        Returns the splitted data as a tuple of format (X_train, X_test, Y_train, Y_test)
        '''
        logging.info('Initiating data ingestion...')

        # Load data and drop duplicates
        df = pd.read_csv(path)
        df.drop_duplicates(inplace = True)

        # Split the dataset
        X_train, X_test, Y_train, Y_test = train_test_split(df.drop(target_class, axis = 1),
                                                            df[target_class],
                                                            stratify = df[target_class],
                                                            test_size = test_size,
                                                            random_state = random_state)

        logging.info("Successfully completed data ingestion!!!")
        return (X_train, X_test, Y_train, Y_test)
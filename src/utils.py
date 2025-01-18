import os
import sys

import dill
import pickle

from src.exception import CustomError
from src.logger import logging

class CustomFormatter(logging.Formatter):
    '''
    Custom Formatter which replaces first occurence of full path ane with relative pathname of app.py
    '''
    def format(self, record):
        full_path = record.pathname
        relative_path = os.path.relpath(full_path)
        formatted_string = logging.Formatter.format(self, record)
        return formatted_string.replace(full_path, relative_path, 1)

def save_object(file_path, obj):
    '''
    Save an object in given path as a pickle file
    '''
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok = True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except:
        error_obj = CustomError(*sys.exc_info())
        logging.error(error_obj, exc_info = True)
        raise error_obj
    
def load_object(file_path):
    '''
    Load an object from given path of a pickle file
    '''
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except:
        error_obj = CustomError(*sys.exc_info())
        logging.error(error_obj, exc_info = True)
        raise error_obj


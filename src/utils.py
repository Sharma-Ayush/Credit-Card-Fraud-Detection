import os

import dill
import pickle

import numpy as np

from sklearn.metrics import auc, precision_recall_curve

from src.logger import logging

class CustomFormatter(logging.Formatter):
    '''
    Custom Formatter which replaces first occurence of full path with relative pathname of app.py
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
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok = True)

    with open(file_path, "wb") as file_obj:
        pickle.dump(obj, file_obj)
    
def load_object(file_path):
    '''
    Load an object from given path of a pickle file
    '''
    with open(file_path, "rb") as file_obj:
        return pickle.load(file_obj)
    
def area_under_precision_recall_curve(y_true, y_pred):
    '''
    Function that can compute the area under precision recall curve
    '''
    precision, recall, _ = precision_recall_curve(y_true, y_pred)
    auc_precision_recall = auc(recall, precision)

    return auc_precision_recall

def double_log_transform(x):
    '''Transform x by taking the log of the data after shifting by 1. This operation is done two times iteratively.'''
    return np.log10(np.log10(x + 1) + 1)

def cube_root_transform(x):
    '''Transform x by taking the cube root of the data.'''
    return np.cbrt(x)



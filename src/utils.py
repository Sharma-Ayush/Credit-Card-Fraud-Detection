import logging
import os

# Custom class so that we can print realtive path with respect to app.py
class CustomFormatter(logging.Formatter):
    '''Custom Formatter which replaces first occurence of full path ane with relative pathname of app.py'''
    def format(self, record):
        full_path = record.pathname
        relative_path = os.path.relpath(full_path)
        formatted_string = logging.Formatter.format(self, record)
        return formatted_string.replace(full_path, relative_path, 1)
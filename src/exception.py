import sys
from src.logger import logging

class CustomError(Exception):
    '''Custom Exception class for making the print of exception message more informative'''
    def __init__(self, type_of_error, exception_object, traceback):
        super().__init__(exception_object.args)
        self.type_of_error = type_of_error
        self.exception_object = exception_object
        self.traceback = traceback
    
    def __str__(self):
        return f"{self.type_of_error.__name__}: {self.exception_object}"

from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .' # String for running setup.py within dependency file and generating the distribution package

def get_dependencies(dependency_file:str) -> List[str]:
    '''Read the dependencies from given file path and return as a list of strings'''
    
    dependencies = []
    
    with open(dependency_file, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line != HYPHEN_E_DOT:
                dependencies.append(stripped_line)

    return dependencies

setup(
    name = 'ieee_cis_fraud_detection',
    version = '0.0.1',
    author = 'Ayush Sharma',
    author_email = 'ayushsharma812@gmail.com',
    packages = find_packages(),
    install_requires = get_dependencies('requirements.txt')
    )
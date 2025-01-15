import logging
import logging.config
import os
import json

# make log directory if it does not exist
os.makedirs('logs', exist_ok = True)

cwd = os.getcwd()
config_file_path = os.path.join('', 'src/logging_config.json')

# Load the JSON configuration
with open(config_file_path, 'r') as config_file:
    config_dict = json.load(config_file)

# Setting up the config
logging.config.dictConfig(config_dict)



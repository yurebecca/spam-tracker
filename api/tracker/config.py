import os
import json

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path) as config_file:    
    config = json.load(config_file)
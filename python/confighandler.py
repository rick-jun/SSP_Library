import json
import sys

def parse_json_config(filename):
    try:
        with open(filename, 'r', encoding='UTF-8') as config_file:
            return json.load(config_file)
        
    except Exception as e:
        print(f"Error at parse_json_config(): {e}")
        raise e
            
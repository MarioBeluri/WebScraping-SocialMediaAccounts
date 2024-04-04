"""
	utility scripts
"""
import json
from datetime import datetime

def get_timestamp():
	timestamp = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
	return timestamp

def save_json_output(file_path_name, data):
	with open(file_path_name, 'w+', encoding='utf-8') as fd:
		json.dump(data, fd, ensure_ascii=False, indent=4)

import json
import os

DEFAULT_IP_ADDRESS = '192.168.88.252'
DEFAULT_USERNAME = 'Bosch'
DEFAULT_PASSWORD = 'Robert'
DEFAULT_MODULE_NAME = 'LuxaSim16-01'
DEFAULT_JSON_FILE_PATH = 'C:\\Users\\SHS1MT.DE\\Desktop\\web\\log_files\\modules.json'
DEFAULT_LOG_FILE_PATH = 'C:\\Users\\SHS1MT.DE\\Desktop\\web\\log_files\\ip_address.txt'
MAX_RETRIES = 5  # Number of retries for connection

# Load signals from JSON file
with open(DEFAULT_JSON_FILE_PATH) as f:
    modules_data = json.load(f)
    IN_SIGNALS = [(entry['signal'], entry['port']) for entry in modules_data if entry['direction'] == 'in']
    OUT_SIGNALS = [(entry['signal'], entry['port']) for entry in modules_data if entry['direction'] == 'out']
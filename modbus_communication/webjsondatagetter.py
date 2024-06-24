import argparse
import json
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modbus_communication.settings')
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modbus_app.models import Signal
import time
from datetime import datetime

DEFAULT_IP_ADDRESS = '192.168.88.253'
DEFAULT_USERNAME = 'Bosch'
DEFAULT_PASSWORD = 'Robert'
DEFAULT_MODULE_NAME = 'LuxaSim16-01'
DEFAULT_FILE_PATH = 'C:\\Users\\SHS1MT.DE\\Desktop\\web\\log_files\\modules.json'
DEFAULT_LOG_FILE_PATH = 'C:\\Users\\SHS1MT.DE\\Desktop\\web\\log_files\\ip_address.txt'
MAX_RETRIES = 5  # Number of retries for connection

class CustomError(Exception):
    pass

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server="direct://"')
    chrome_options.add_argument('--proxy-bypass-list=*')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login(driver, url, username, password):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'txtUsername')))
    
    username_field = driver.find_element(By.ID, 'txtUsername')
    password_field = driver.find_element(By.ID, 'txtPassword')
    login_button = driver.find_element(By.ID, 'btnLogin')

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
    
    time.sleep(5)

def fetch_json_data(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'pre')))
    json_content = driver.find_element(By.TAG_NAME, 'pre').text
    return json_content

def filter_json_content(json_content, module_name):
    data = json.loads(json_content)
    filtered_data = [entry for entry in data if entry.get('module') == module_name]
    return json.dumps(filtered_data, indent=4)

def save_json_to_file(json_content, file_path):
    with open(file_path, 'w') as file:
        file.write(json_content)
    print(f"JSON data saved to {file_path}")

def save_ip_address(ip_address, log_file_path):
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open(log_file_path, 'a') as file:
        file.write(f"{current_time} - {ip_address}\n")
    print(f"IP address {ip_address} logged to {log_file_path} with timestamp {current_time}")

def save_signals_to_db(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        Signal.objects.all().delete()  # Clear existing signals
        for entry in data:
            if entry['port'] == 0:
                continue  # Ignore port 0
            Signal.objects.create(
                name=entry['signal'],
                direction=entry['direction'],
                port=entry['port'],
                state=False,
                program_number=0 if 'Prog' in entry['signal'] or 'ProgAck' in entry['signal'] else None
            )
    print(f"Signals from {file_path} saved to database")

def main(ip_address, username, password, module_name, file_path, log_file_path):
    driver = setup_driver()
    retries = 0
    while retries < MAX_RETRIES:
        try:
            login_url = f'https://{ip_address}/login'
            json_url = f'https://{ip_address}/BS350/BMS/modules'
            login(driver, login_url, username, password)
            json_content = fetch_json_data(driver, json_url)
            filtered_content = filter_json_content(json_content, module_name)
            save_json_to_file(filtered_content, file_path)
            save_ip_address(ip_address, log_file_path)
            save_signals_to_db(file_path)
            break
        except CustomError as e:
            print(e)
            retries += 1
            print(f"Retrying... ({retries}/{MAX_RETRIES})")
            time.sleep(5)  # Wait for a while before retrying
        finally:
            driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch and filter JSON data from a website.')
    parser.add_argument('--ip_address', type=str, default=DEFAULT_IP_ADDRESS, help='The IP address of the target website')
    parser.add_argument('--username', type=str, default=DEFAULT_USERNAME, help='The username for login')
    parser.add_argument('--password', type=str, default=DEFAULT_PASSWORD, help='The password for login')
    parser.add_argument('--module_name', type=str, default=DEFAULT_MODULE_NAME, help='The module name to filter the JSON data')
    parser.add_argument('--file_path', type=str, default=DEFAULT_FILE_PATH, help='The path where the JSON data should be saved')
    parser.add_argument('--log_file_path', type=str, default=DEFAULT_LOG_FILE_PATH, help='The path where the IP address should be logged')

    args = parser.parse_args()
    main(args.ip_address, args.username, args.password, args.module_name, args.file_path, args.log_file_path)

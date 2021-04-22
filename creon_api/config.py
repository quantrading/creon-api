import json
import os

config = {}
if os.path.exists("creon_config.json"):
    with open("creon_config.json") as f:
        config = json.load(f)

LOG_PATH = config.get('LOG_PATH', "./cybos_log")
DATA_FOLDER_PATH = config.get('DATA_FOLDER_PATH', "./cybos_data")
CODE_LIST_FOLDER_PATH = config.get('CODE_LIST_FOLDER_PATH', f"{DATA_FOLDER_PATH}/code_list")
PROCESSED_DATA_FOLDER = config.get('PROCESSED_DATA_FOLDER', f"{DATA_FOLDER_PATH}/processed_data")
CODE_FOLDER_PATH = f"{DATA_FOLDER_PATH}/code_list"
ADJ_INFO_PATH = f"{DATA_FOLDER_PATH}/adj_info"
DAILY_DATA_PATH = f"{DATA_FOLDER_PATH}/daily_data"
MINUTE_DATA_PATH = f"{DATA_FOLDER_PATH}/minute_data"
ADJ_DAILY_DATA_PATH = f"{PROCESSED_DATA_FOLDER}/adj_daily_data"

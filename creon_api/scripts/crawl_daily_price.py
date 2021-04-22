from datetime import datetime
import pandas as pd
from creon_api.cybos import Cybos
from .. import utils
from ..logger import logger
from ..config import DAILY_DATA_PATH


def create_new_daily_stock_file(stock_code_list: list, start_date: str, end_date: str,
                                data_folder_path: str = DAILY_DATA_PATH):
    utils.make_dir(data_folder_path)
    cybos_api = Cybos()
    for i, code in enumerate(stock_code_list):
        print(f"{code} {i + 1}/{len(stock_code_list)}")

        if utils.is_exist(f"{data_folder_path}/{code}.csv"):
            print("이미있음.")
            continue
        try:
            res = cybos_api.get_daily_price(code, start_date, end_date)
        except Exception as e:
            logger.error(f"{e} : {start_date} {end_date} {code}")
            continue
        res.to_csv(f"{data_folder_path}/{code}.csv", encoding='utf-8-sig', index=False)


def update_daily_stock_file(stock_code_list: list, date: str = None, data_folder_path: str = DAILY_DATA_PATH):
    utils.make_dir(data_folder_path)
    cybos_api = Cybos()
    if date is None:
        date = datetime.today().strftime("%Y%m%d")

    for i, code in enumerate(stock_code_list):
        print(f"{code} {i + 1}/{len(stock_code_list)}")

        try:
            df = pd.read_csv(f"{data_folder_path}/{code}.csv")
        except Exception as e:
            logger.error(f"{e} : {date} {code} 파일 존재하지 않음. 새로 받고 저장")
            create_new_daily_stock_file([code], "20000101", date, data_folder_path)
            continue

        try:
            res = cybos_api.get_daily_price(code, date, date)
        except Exception as e:
            logger.error(f"{e} : {date} {code}")
            continue
        df = pd.concat([df, res], axis=0)
        df = df.drop_duplicates(subset=['date'], keep='first')
        df.to_csv(f"{data_folder_path}/{code}.csv", encoding='utf-8-sig', index=False)

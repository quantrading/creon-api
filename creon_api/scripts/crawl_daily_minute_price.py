from datetime import datetime
import pandas as pd
from pandas.errors import EmptyDataError
from creon_api.cybos import Cybos
from .. import utils
from ..config import MINUTE_DATA_PATH
from ..logger import logger


def get_not_available_code_list(path: str) -> list:
    try:
        code_df = pd.read_csv(f"{path}.csv", header=None, dtype=object)
        code_list = code_df.iloc[:, 0].astype(str).tolist()
        print(code_list)
    except FileNotFoundError:
        code_list = []
    except EmptyDataError:
        code_list = []
    return code_list


def save_not_available_code_list(code_list: list, path: str) -> None:
    not_found_code_series = pd.Series(code_list)
    not_found_code_series.to_csv(f"{path}.csv", index=False, header=False)


def save_daily_minute_price_file(stock_code_list: list, date: datetime = None, data_folder_path: str = MINUTE_DATA_PATH):
    if date is None:
        date = datetime.today()
    utils.make_dir(data_folder_path)

    cybos_api = Cybos()

    date_for_file_name = date.strftime("%Y-%m-%d")
    not_available_code_list = get_not_available_code_list(f"{data_folder_path}/not_available_{date_for_file_name}")

    for i, code in enumerate(stock_code_list):
        print(f"{date_for_file_name} {code} {i + 1}/{len(stock_code_list)}")
        utils.make_dir(f"{data_folder_path}/{code}")

        if code in not_available_code_list:
            continue

        if utils.is_exist(f"{data_folder_path}/{code}/{date_for_file_name}.csv"):
            print("이미있음.")
            continue
        try:
            res = cybos_api.get_minutely_price(code, date.strftime("%Y%m%d"))
        except Exception as e:
            logger.error(e)
            not_available_code_list.append(code)
            continue

        res.to_csv(f"{data_folder_path}/{code}/{date_for_file_name}.csv", encoding='utf-8-sig')
    save_not_available_code_list(not_available_code_list, f"{data_folder_path}/not_available_{date_for_file_name}")

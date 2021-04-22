import pandas as pd
from creon_api.cybos import Cybos
from ..logger import logger
from .. import utils
from ..config import ADJ_INFO_PATH


def create_new_stock_adj_info_file(stock_code_list: list, data_folder_path: str = ADJ_INFO_PATH):
    cybos_api = Cybos()
    utils.make_dir(data_folder_path)
    for i, code in enumerate(stock_code_list):
        print(f"{code} {i + 1}/{len(stock_code_list)}")

        if utils.is_exist(f"{data_folder_path}/{code}.csv"):
            print("이미있음.")
            continue
        try:
            res = cybos_api.get_stock_adj_info(code)
        except Exception as e:
            logger.error(f"{e} : {code}")
            continue
        res.to_csv(f"{data_folder_path}/{code}.csv", encoding='utf-8-sig', index=False)


def update_stock_adj_info_file(stock_code_list: list, data_folder_path: str = ADJ_INFO_PATH):
    cybos_api = Cybos()
    utils.make_dir(data_folder_path)
    for i, code in enumerate(stock_code_list):
        print(f"{code} {i + 1}/{len(stock_code_list)}")

        try:
            df = pd.read_csv(f"{data_folder_path}/{code}.csv")
        except Exception as e:
            logger.error(f"{e} : {code} 파일 존재하지 않음. 새로 받고 저장")
            create_new_stock_adj_info_file([code], data_folder_path)
            continue

        try:
            res = cybos_api.get_stock_adj_info(code)
        except Exception as e:
            logger.error(f"{e} : {code}")
            continue
        df = pd.concat([df, res], axis=0)
        df = df.drop_duplicates(subset=['권부일'], keep='first')
        df.to_csv(f"{data_folder_path}/{code}.csv", encoding='utf-8-sig', index=False)

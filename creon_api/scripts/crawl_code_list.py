from datetime import datetime
import pandas as pd
from creon_api.cybos import Cybos
from .. import utils
from ..config import CODE_LIST_FOLDER_PATH


def save_recent_stock_code_list_file(date: str = None, data_folder_path: str = CODE_LIST_FOLDER_PATH):
    if date is None:
        date = datetime.today().strftime("%Y%m%d")

    cybos_api = Cybos()

    market_type_list = [
        '0',  # 구분없음
        '1',  # 거래소
        '2',  # 코스닥
        '3',  # K-OTC
        '4',  # KRX
        '5',  # KONEX
    ]
    for market_type in market_type_list:
        code_list = cybos_api.get_stock_list(market_type)

        if market_type == '0':
            market_folder = '구분없음'
        elif market_type == '1':
            market_folder = '거래소'
        elif market_type == '2':
            market_folder = '코스닥'
        elif market_type == '3':
            market_folder = 'K-OTC'
        elif market_type == '4':
            market_folder = 'KRX'
        elif market_type == '5':
            market_folder = 'KONEX'
        else:
            raise ValueError(f"Invalid market_type : {market_type}")

        code_series = pd.Series(code_list, name='code')
        print(date, market_folder)
        print(code_series)

        utils.make_dir(f"{data_folder_path}/{market_folder}")
        code_series.to_csv(f"{data_folder_path}/{market_folder}/{date}.csv", encoding='utf-8-sig', index=False)

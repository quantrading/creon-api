import pandas as pd
from creon_api.config import ADJ_INFO_PATH, ADJ_FLOAT_RATIO_PATH
from .. import utils


def read_adj_info_file(code: str) -> pd.DataFrame:
    """
    :param code: 종목코드   ex) A005930
    """
    path = f"{ADJ_INFO_PATH}/{code}.csv"
    df = pd.read_csv(path, index_col='권부일', parse_dates=True)
    return df


def parse_float_ratio(code: str) -> pd.Series:
    adj_df = read_adj_info_file(code)

    float_ratio_series = adj_df['변경전기준가'] / adj_df['변경후기준가']
    float_ratio_series = float_ratio_series[float_ratio_series != 1]
    float_ratio_series.name = '수정비율'
    return float_ratio_series


def save_float_ratio_series_to_file(series: pd.Series, code: str, data_folder_path: str = ADJ_FLOAT_RATIO_PATH):
    utils.make_dir(data_folder_path)
    series.to_csv(f"{data_folder_path}/{code}.csv", encoding='utf-8-sig')

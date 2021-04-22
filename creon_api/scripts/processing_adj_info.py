import pandas as pd
from creon_api.config import ADJ_INFO_PATH, DAILY_DATA_PATH, ADJ_DAILY_DATA_PATH
from .. import utils


def read_adj_info_file(code: str) -> pd.DataFrame:
    """
    :param code: 종목코드   ex) A005930
    """
    path = f"{ADJ_INFO_PATH}/{code}.csv"
    df = pd.read_csv(path, index_col='권부일', parse_dates=True)
    return df


def read_daily_data_file(code: str) -> pd.DataFrame:
    path = f"{DAILY_DATA_PATH}/{code}.csv"
    df = pd.read_csv(path, index_col='date', parse_dates=True)

    df = df[[
        "open",
        "high",
        "low",
        "close",
        "volume",
        "transaction_value",
        "listed_stock_amount",
        "market_capitalization",
    ]]
    return df


def get_processed_adj_price_df(code: str) -> pd.DataFrame:
    adj_df = read_adj_info_file(code)
    daily_df = read_daily_data_file(code)

    float_ratio_series = adj_df['변경전기준가'] / adj_df['변경후기준가']
    float_ratio_series = float_ratio_series.reindex(daily_df.index)
    float_ratio_series = float_ratio_series.fillna(1)
    float_ratio_series = float_ratio_series.cumprod() / float_ratio_series.cumprod().iloc[-1]
    float_ratio_series = float_ratio_series.bfill().ffill()

    new_df = daily_df.copy()
    new_df[[
        'adj_open',
        'adj_high',
        'adj_low',
        'adj_close',
    ]] = daily_df[['open', 'high', 'low', 'close']].multiply(float_ratio_series, axis=0)
    new_df['adj_volume'] = daily_df['volume'].divide(float_ratio_series)
    new_df['adj_ratio'] = float_ratio_series

    new_df = new_df[[
        "open",
        "high",
        "low",
        "close",
        "volume",
        'adj_open',
        'adj_high',
        'adj_low',
        'adj_close',
        'adj_volume',
        'adj_ratio',
        "transaction_value",
        "listed_stock_amount",
        "market_capitalization",
    ]]
    return new_df


def save_processed_df_to_file(df: pd.DataFrame, code: str, data_folder_path: str = ADJ_DAILY_DATA_PATH):
    utils.make_dir(data_folder_path)
    df.to_csv(f"{data_folder_path}/{code}.csv", encoding='utf-8-sig')

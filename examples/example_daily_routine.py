import creon_api.utils as utils
import creon_api.scripts.crawl_code_list
import creon_api.scripts.crawl_daily_stock_adj_info
import creon_api.scripts.crawl_daily_price
import creon_api.scripts.crawl_daily_minute_price
import creon_api.scripts.processing_adj_info
import creon_api.scripts.parse_adj_ratio

if __name__ == "__main__":
    # 주식시장 종목리스트 다운로드
    creon_api.scripts.crawl_code_list.save_recent_stock_code_list_file()

    code_list = [
        *utils.load_krx_code_list(),
        *utils.index_code_list
    ]

    # 권리락 정보 다운로드
    creon_api.scripts.crawl_daily_stock_adj_info.update_stock_adj_info_file(code_list)

    # 일별데이터 다운로드
    creon_api.scripts.crawl_daily_price.update_daily_stock_file(code_list)

    # 분봉데이터 다운로드
    creon_api.scripts.crawl_daily_minute_price.save_daily_minute_price_file(code_list)

    # 수정주가 계산 및 저장
    code_list = utils.get_adj_file_code_list()
    for i, code in enumerate(code_list):
        print(f"{code} {i + 1}/{len(code_list)}")
        processed_adj_price_df = creon_api.scripts.processing_adj_info.get_processed_adj_price_df(code)
        creon_api.scripts.processing_adj_info.save_processed_df_to_file(processed_adj_price_df, code)

    # 수정비율 계산 및 저장
    code_list = utils.get_adj_file_code_list()
    for i, code in enumerate(code_list):
        print(f"{code} {i + 1}/{len(code_list)}")
        float_ratio_series = creon_api.scripts.parse_adj_ratio.parse_float_ratio(code)
        creon_api.scripts.parse_adj_ratio.save_float_ratio_series_to_file(float_ratio_series, code)

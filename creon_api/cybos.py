import win32com.client
import time
import pandas as pd


class Cybos:
    """
    기본적인 데이터는 2002년 이후 제공한다함.

    1분봉 2년
    5분봉 5년
    틱 20일
    
    """
    MIN_INTERVAL = 0.35
    recent_request = time.time()
    instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")  # 연결상태확인 1:연결 0:연결안됨
    if instCpCybos.IsConnect != 1:
        raise ConnectionError('cybos plus 가 연결되어 있지 않음.')  # 관리자 권한 확인 필요

    @classmethod
    def request_api(cls, func, *args, **kwargs):
        interval = time.time() - cls.recent_request
        if interval < cls.MIN_INTERVAL:
            time.sleep(cls.MIN_INTERVAL - interval)
        res = func(*args, **kwargs)
        cls.recent_request = time.time()
        return res

    @classmethod
    def get_stock_listed_date(cls, code: str):
        cp_code_mgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        date = cls.request_api(cp_code_mgr.GetStockListedDate, code)
        return date

    @classmethod
    def get_stock_list(cls, market_type: str):
        """
        0: 구분없음
        1: 거래소
        2: 코스닥
        3: K-OTC
        4: KRX
        5: KONEX
        """
        cp_code_mgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        data = cls.request_api(cp_code_mgr.GetStockListByMarket, market_type)
        return data

    @classmethod
    def get_minutely_price(cls, stock_code: str, date: str) -> pd.DataFrame:
        """
        :param stock_code: 'A005930', 'U001'
        :param date: 'YYYYMMDD'
        :return: 
        """
        stock_chart_ins = win32com.client.Dispatch("CpSysDib.StockChart")

        stock_chart_ins.SetInputValue(0, stock_code)  # 종목코드
        stock_chart_ins.SetInputValue(1, ord('1'))  # '1':기간 '2':개수     기간 요청시, 주,월,분,틱 불가
        stock_chart_ins.SetInputValue(2, date)  # 요청종료일
        stock_chart_ins.SetInputValue(3, date)  # 요청시작일

        items = [
            0,  # 날짜
            1,  # 시간
            2, 3, 4, 5,  # 시, 고, 저, 종
            8,  # 거래량
            9,  # 거래대금
            10,  # 누적체결매도수량
            11,  # 누적체결매수수량
            25,  # 주식회전율
            26,  # 거래성립률
        ]
        stock_chart_ins.SetInputValue(5, items)
        stock_chart_ins.SetInputValue(6, ord('m'))  # D:일 T:틱 m:분 M:달
        stock_chart_ins.SetInputValue(7, 1)  # 주기
        stock_chart_ins.SetInputValue(9, ord('0'))  # 0:무수정주가 1:수정주가
        stock_chart_ins.SetInputValue(10, ord('3'))  # 3:시간외거래량 제외

        cls.request_api(stock_chart_ins.BlockRequest)

        data_counts = stock_chart_ins.GetHeaderValue(3)  # 3:수신개수

        data_list = []
        for i in range(data_counts):
            row = []
            for j in range(len(items)):
                value = stock_chart_ins.GetDataValue(j, i)
                row.append(value)
            data_list.append(row)
        df = pd.DataFrame(data_list, columns={
            'date': str,
            'time': str,
            'open': float,
            'high': float,
            'low': float,
            'close': float,
            'volume': float,
            'transaction_value': float,
            'cum_buy_conclusion': float,
            'cum_sell_conclusion': float,
            'turnover': float,
            'trade_success_rate': float,
        })
        return df

    @classmethod
    def get_daily_price(cls, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        :param stock_code: 'A005930', 'U001'
        :param start_date: 'YYYYMMDD'
        :param end_date: 'YYYYMMDD'
        :return:
        """
        stock_chart_ins = win32com.client.Dispatch("CpSysDib.StockChart")

        stock_chart_ins.SetInputValue(0, stock_code)  # 종목코드
        stock_chart_ins.SetInputValue(1, ord('1'))  # '1':기간 '2':개수     기간 요청시, 주,월,분,틱 불가
        stock_chart_ins.SetInputValue(2, end_date)  # 요청종료일
        stock_chart_ins.SetInputValue(3, start_date)  # 요청시작일

        items = [
            0,  # 날짜
            2, 3, 4, 5,  # 시, 고, 저, 종
            8,  # 거래량
            9,  # 거래대금
            12,  # 상장주식수
            13,  # 시가총액
            # 18,  # 수정주가일자
            # 19,  # 수정주가비율
        ]
        stock_chart_ins.SetInputValue(5, items)
        stock_chart_ins.SetInputValue(6, ord('D'))  # D:일 T:틱 m:분 M:달
        stock_chart_ins.SetInputValue(7, 1)  # 주기
        stock_chart_ins.SetInputValue(9, ord('0'))  # 0:무수정주가 1:수정주가
        stock_chart_ins.SetInputValue(10, ord('3'))  # 3:시간외거래량 제외

        data_list = []
        while True:
            cls.request_api(stock_chart_ins.BlockRequest)
            data_counts = stock_chart_ins.GetHeaderValue(3)  # 3:수신개수

            for i in range(data_counts):
                row = []
                for j in range(len(items)):
                    value = stock_chart_ins.GetDataValue(j, i)
                    row.append(value)
                data_list.append(row)

            if stock_chart_ins.Continue == 0:
                break

        df = pd.DataFrame(data_list, columns={
            'date': str,
            'open': float,
            'high': float,
            'low': float,
            'close': float,
            'volume': float,
            'transaction_value': float,
            'listed_stock_amount': int,
            'market_capitalization': int,
            # 'adj_date': str,
            # 'adj_ratio': float,
        })
        df = df.sort_values('date', ascending=True)
        return df

    @classmethod
    def get_stock_adj_info(cls, stock_code: str) -> pd.DataFrame:
        """
        :param stock_code: 'A005930', 'U001'
        :return:
        """
        stock_adj_ins = win32com.client.Dispatch("CpSysDib.StockAdj")

        stock_adj_ins.SetInputValue(0, stock_code)  # 종목코드
        stock_adj_ins.SetInputValue(1, 'D')
        items = [
            0,  # 권부일
            3,  # 락구분코드 00:해당사항없음(락이 발생안한 경우), 01:권리락,02:배당락,03:분배락,04:권배락,05:중간(분기)배당락,06:권리중간배당락,07:권리분기배당락,99:기타
            4,  # 액면가변경구분코드 00:해당없음, 01:액면분할, 02:액면병합, 03:주식분할, 04:주식병합, 99:기타
            5,  # 재평가종목사유코드 00:해당없음, 01:회사분할, 02:자본감소, 03:장기간정지, 04:초과분배,05:대규모배당, 06: 회사분할합병, 99:기타
            6,  # 변경전 기준가
            7,  # 변경후 기준가
        ]

        data_list = []
        while True:
            cls.request_api(stock_adj_ins.BlockRequest)
            data_counts = stock_adj_ins.GetHeaderValue(2)  # 2:수신개수

            for i in range(data_counts):
                row = []
                for j in items:
                    value = stock_adj_ins.GetDataValue(j, i)
                    row.append(value)
                data_list.append(row)

            if stock_adj_ins.Continue == 0:
                break

        df = pd.DataFrame(data_list, columns={
            '권부일': str,
            '락구분코드': str,
            '액면가변경구분코드': str,
            '재평가종목사유코드': str,
            '변경전기준가': str,
            '변경후기준가': str,
        })
        df = df.sort_values('권부일', ascending=True).reset_index(drop=True)
        return df

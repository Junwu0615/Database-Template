# -*- coding: utf-8 -*-
import pandas as pd

from developer.utils.normal import *
from developer.utils.telegram import send_message
from developer.modules.logger import Logger
from developer.modules.interface import Interface
from developer.modules.models.WorkStatus import Status
from developer.modules.models.TForexQuotes import TForexQuotesField, TForexQuotesFormat


class Entry(Interface):
    def __init__(self, do_time=None, logger=None):
        do_time = do_time or []
        if logger is None:
            raise Exception('Logger 未設定，請先於 __main__ 中定義')

        self.logger = logger
        super().__init__(do_time, logger)


    def config_once(self):
        """ 定義一次性變數 """
        pass


    def update_once(self):
        """ 主邏輯撰寫 """
        datum = {}
        ret = Status.ERR_UNKNOWN
        # send_message(msg='test', logger=self.logger, bot_token='', chat_id='')
        try:
            # 情境模擬: 讀取本地檔案，並將其塞入資料庫
            file = './sample/xauusd_2024-12-26.json'
            loader = [json.loads(i) for i in open(file, 'r')][0]
            symbol = loader['symbol']

            for i in loader['historical']:
                key = f"{i['date']}_{symbol}_D1"
                datum[key] = {
                    TForexQuotesField.CREATEDATETIME.value: trans_datetime(i['date'], SHORT_FORMAT),
                    TForexQuotesField.SYMBOL.value: symbol,
                    TForexQuotesField.INTERVAL.value: 'D1',
                    TForexQuotesField.OPEN.value: trans_decimal(i['open'], '0.01'),
                    TForexQuotesField.HIGH.value: trans_decimal(i['high'], '0.01'),
                    TForexQuotesField.LOW.value: trans_decimal(i['low'], '0.01'),
                    TForexQuotesField.CLOSE.value: trans_decimal(i['close'], '0.01'),
                    TForexQuotesField.VOLUME.value: trans_decimal(i['volume'], '0.01'),
                }
            self.save_datum(db_name=TForexQuotesField.DB_NAME.value,
                            table_format=TForexQuotesFormat,
                            save_data=datum)

            # 查詢資料
            # fq_data = self.get_datum(db_name=TForexQuotesField.DB_NAME.value,
            #                          table_format=TForexQuotesFormat)

            fq_data = self.get_datum(db_name=TForexQuotesField.DB_NAME.value,
                                     table_format=TForexQuotesFormat,
                                     **{'SQL_WHERE': "Symbol = 'XAUUSD'"})

            df = pd.DataFrame(fq_data)
            self.logger.info(df)

            ret = Status.OK

        except Exception as e:
            self.logger.error()

        finally:
            return ret


if __name__ == '__main__':
    """
    功能說明
        -排程邏輯: 參閱 developer.modules.interface <settings_schedule> 方法
    """
    logger = Logger(console_name=f'.{__name__}_console',
                    file_name=f'.{__name__}')

    logger.info(logger.title_log(f'[{__name__}] 主程式啟動'))

    do_time = ['MTWTFss=06:00:00', 'MTWTFss=18:00:00']
    # entry = Entry(do_time)
    entry = Entry(do_time, logger)
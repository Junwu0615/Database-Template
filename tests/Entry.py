# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-31
"""
import json
import pandas as pd

from developer.package.norm_function import DATE_YMD_ONE
from developer.package.interface import Interface
from developer.definition.state import State
from developer.model.TForexQuotes import TForexQuotesField, TForexQuotesFormat

class Entry(Interface):
    def __init__(self, do_time=None):
        do_time = do_time or []
        super().__init__(do_time)

    def config_once(self):
        """ 定義一次性變數 """
        pass

    def update_once(self):
        """ 主邏輯撰寫 """
        datum = {}
        ret = State.ERR_UNKNOWN
        try:
            # 情境模擬: 讀取本地檔案，並將其塞入資料庫
            file = './sample/xauusd_2024-12-26.json'
            loader = [json.loads(i) for i in open(file, 'r')][0]
            symbol = loader['symbol']

            for i in loader['historical']:
                key = f"{i['date']}_{symbol}_D1"
                datum[key] = {
                    TForexQuotesField.CREATEDATETIME.value: self.trans_datetime(i['date'], DATE_YMD_ONE),
                    TForexQuotesField.SYMBOL.value: symbol,
                    TForexQuotesField.INTERVAL.value: 'D1',
                    TForexQuotesField.OPEN.value: self.trans_decimal(i['open'], '0.01'),
                    TForexQuotesField.HIGH.value: self.trans_decimal(i['high'], '0.01'),
                    TForexQuotesField.LOW.value: self.trans_decimal(i['low'], '0.01'),
                    TForexQuotesField.CLOSE.value: self.trans_decimal(i['close'], '0.01'),
                    TForexQuotesField.VOLUME.value: self.trans_decimal(i['volume'], '0.01'),
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
            self.log_info(df)

            ret = State.OK

        except Exception as e:
            self.log_error(exc_info=True)
        finally:
            return ret

if __name__ == '__main__':
    """
    功能說明
        -排程邏輯: 參閱 developer.package.interface <settings_schedule> 方法
    """
    do_time = ['MTWTFss=06:00:00', 'MTWTFss=18:00:00']
    entry = Entry(do_time)
    # entry = Entry()
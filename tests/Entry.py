# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-28
"""
import json
import pandas as pd

from package.norm_function import DATE_YMD_ONE
from package.interface import Interface
from model.TForexQuotes import TForexQuotesField, TableFormat

class Entry(Interface):
    def __init__(self):
        Interface.__init__(self)

    def update_once(self):
        """
        FIXME 情境模擬: 讀取本地檔案，並將其塞入資料庫
        """
        datum = {}
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
        self.save_datum(db_name=TForexQuotesField.TABLE_DB.value,
                        table_name=TForexQuotesField.TABLE_NAME.value,
                        table_format=TableFormat,
                        save_data=datum)

        """ 查詢資料 """
        fq_data = self.get_datum(db_name=TForexQuotesField.TABLE_DB.value,
                                 table_name=TForexQuotesField.TABLE_NAME.value)
        df = pd.DataFrame(fq_data)
        print(df)

if __name__ == '__main__':
    entry = Entry()
    entry.update_once()
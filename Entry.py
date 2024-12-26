# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-28
"""
import json

from Depend.SqlServer import DatabaseLogic
from Depend.NormFunction import NormLogic, DATE_YMD_ONE
from Model.TForexQuotes import TForexQuotesField, TableFormat

class Entry(NormLogic, DatabaseLogic):
    def __init__(self):
        NormLogic.__init__(self)
        DatabaseLogic.__init__(self)

    def main(self):
        # self.db_logic.create_database('table_test') # 建立資料庫
        # rows = self.db_logic.query_data() # 查詢資料
        # print(rows)

        # 讀取本地檔案，並將其塞入資料庫
        datum = {}
        interval = 'D1'
        file = rf'C:\Users\PC\Code\Python\Publish-To-Git\Forex\Forex-Get-Quotes\Datasets\XAUUSD\{interval}\xauusd_2024-12-26.json'
        loader = [json.loads(i) for i in open(file, 'r')][0]
        symbol = loader['symbol']
        for i in loader['historical']:
            key = f"{i['date']}_{symbol}_{interval}"
            datum[key] = {
                TForexQuotesField.CREATEDATETIME.value: self.trans_datetime(i['date'], DATE_YMD_ONE),
                TForexQuotesField.SYMBOL.value: symbol,
                TForexQuotesField.INTERVAL.value: interval,
                TForexQuotesField.OPEN.value: self.trans_decimal(i['open'], '0.01'),
                TForexQuotesField.HIGH.value: self.trans_decimal(i['high'], '0.01'),
                TForexQuotesField.LOW.value: self.trans_decimal(i['low'], '0.01'),
                TForexQuotesField.CLOSE.value: self.trans_decimal(i['close'], '0.01'),
                TForexQuotesField.VOLUME.value: self.trans_decimal(i['volume'], '0.01'),
            }
        self.save_datum(db_name=TForexQuotesField.TABLE_DB.value,
                        table_format=TableFormat,
                        table_name=TForexQuotesField.TABLE_NAME.value,
                        save_data=datum)


if __name__ == '__main__':
    entry = Entry()
    entry.main()
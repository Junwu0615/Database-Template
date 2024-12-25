# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-26
"""
from Depend.BaseLogic import BaseLogic

class Entry:
    def __init__(self):
        self.base = BaseLogic()

    def main(self):
        # self.base.create_database('table_test') # 建立資料庫
        # self.base.create_table() # 建立表格
        # self.base.insert_data() # 插入資料
        rows = self.base.query_data() # 查詢資料
        print(rows)

if __name__ == '__main__':
    entry = Entry()
    entry.main()


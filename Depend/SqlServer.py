# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-28
"""
import pyodbc, sqlalchemy
from tqdm import tqdm
from sqlalchemy.dialects import mssql
from sqlalchemy.schema import CreateTable

from Depend import Account

class FromSQLProgrammingError(Exception):
    pass

class DatabaseLogic:
    def __init__(self):
        self.db_name = 'DB_NULL'
        self.connection_string = (f'DRIVER={Account.DRIVER};SERVER={Account.SERVER};DATABASE={self.db_name};'
                                  f'UID={Account.USERNAME};PWD={Account.PASSWORD};Trusted_Connection=yes;')

    def update_connection_string(self, db_name: str):
        """
        更新連接字串
        """
        if self.db_name != db_name:
            self.connection_string = self.connection_string.replace(self.db_name, db_name)
            self.db_name = db_name

    def create_database(self, db_name: str):
        """
        建立資料庫
        """
        conn, cursor = None, None
        try:
            sql_cmd = self.connection_string.replace(f'DATABASE={self.db_name};', '')
            conn = pyodbc.connect(sql_cmd, autocommit=True)
            cursor = conn.cursor()

            # 確認是否該資料庫已存在
            sql_cmd = f"SELECT name FROM master.sys.databases WHERE name = '{db_name}'"
            cursor.execute(sql_cmd)
            # 若否則新建立
            if len(cursor.fetchall()) == 0:
                sql_cmd = f'CREATE DATABASE {db_name}'
                cursor.execute(sql_cmd)
                self.log_warning(f'Database -> [{db_name}] Created Successfully')
            else:
                self.log_warning(f'Database -> [{db_name}] Already Exists')

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def create_table(self, table_format: sqlalchemy):
        """
        建立表格
        """
        conn, cursor = None, None
        try:
            conn = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(f'USE {self.db_name}')

            # 確認是否該資料表已存在
            table_name = table_format.__table__.name
            sql_cmd = f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
            cursor.execute(sql_cmd)
            # 若否則新建立
            if len(cursor.fetchall()) == 0:
                sql_cmd = str(CreateTable(table_format.__table__).compile(dialect=mssql.dialect()))
                cursor.execute(sql_cmd)
                self.log_warning(f'Table -> [{table_name}] Created Successfully')
            else:
                self.log_warning(f'Table -> [{table_name}] Already Exists')

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def save_datum(self, db_name: str, table_format: sqlalchemy, table_name: str, save_data: dict, batch_size: int=500):
        """
        插入資料: 批次塞入
        """
        conn, cursor = None, None
        try:
            self.update_connection_string(db_name)
            self.create_database(db_name)
            self.create_table(table_format)

            conn = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(f'USE {self.db_name}')
            cursor.fast_executemany = True # 提高效能

            keys = save_data[list(save_data.keys())[0]].keys()
            keys = [f'[{i}]' for i in keys]
            _value = list(save_data.values())
            # schedule = tqdm(len(_value))
            schedule = 0
            for idx in range(0, len(_value), batch_size):
                feed_value = [tuple(i.values()) for i in _value[idx:idx + batch_size]]

                # 判斷該鍵值是否已在表格: Merge(查詢, 更新, 插入)
                placeholder = ', '.join([f"({', '.join(['?'] * len(keys))})"])
                mapping_cols = ' AND '.join([f'Target.{col} = Source.{col}' for col in keys if col in table_format.__primary_key__])
                update_cols = ', '.join([f'Target.{col} = Source.{col}' for col in keys if col not in table_format.__primary_key__])
                cols = ', '.join(keys)
                src_cols = ', '.join([f'Source.{col}' for col in keys])

                sql_cmd = f"""
                MERGE INTO {table_name} AS Target
                USING (VALUES {placeholder}) AS Source 
                ({cols}) ON {mapping_cols}
                WHEN MATCHED THEN UPDATE SET {update_cols}
                WHEN NOT MATCHED THEN INSERT ({cols}) VALUES ({src_cols});
                """
                try:
                    cursor.executemany(sql_cmd, feed_value)
                    schedule += len(feed_value)
                    self.log_info(f'Store Data In The Database [{schedule} / {len(_value)}]')

                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def query(self):
        """
        # 查詢資料
        """
        conn, cursor = None, None
        try:
            self.update_connection_string(db_name)
            conn = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = conn.cursor()
            # 欲使用資料庫
            cursor.execute(f'USE {self.db_name}')

            # 下查詢語法
            cursor.execute('SELECT * FROM Employees')

            # 回傳結果
            rows = cursor.fetchall()
            return rows

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
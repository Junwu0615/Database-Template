# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-30
"""
import pyodbc, sqlalchemy
from tqdm import tqdm
from datetime import datetime
from sqlalchemy.dialects import mssql
from sqlalchemy.schema import CreateTable
from developer.package import sql_account
from developer.package.norm_function import ERROR_TEXT

class FromSQLProgrammingError(Exception):
    pass

class DatabaseLogic:
    def __init__(self):
        self.db_name = 'DB_NULL'
        self.connection_string = (f'DRIVER={sql_account.DRIVER};SERVER={sql_account.SERVER};DATABASE={self.db_name};'
                                  f'UID={sql_account.USERNAME};PWD={sql_account.PASSWORD};Trusted_Connection=yes;')

    def __update_connection_string(self, db_name: str):
        """ 更新連接字串: 預期只開放內部呼叫 """
        if self.db_name != db_name:
            self.connection_string = self.connection_string.replace(self.db_name, db_name)
            self.db_name = db_name

    def __create_database(self, db_name: str):
        """ 建立資料庫: 預期只開放內部呼叫 """
        conn = cursor = None
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
            # else:
            #     self.log_warning(f'Database -> [{db_name}] Already Exists')

        except:
            self.log_error(ERROR_TEXT, exc_info=True)
        finally:
            cursor.close()
            conn.close()

    def __create_table(self, table_format: sqlalchemy):
        """ 建立表格: 預期只開放內部呼叫 """
        conn = cursor = None
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
            # else:
            #     self.log_warning(f'Table -> [{table_name}] Already Exists')

        except:
            self.log_error(ERROR_TEXT, exc_info=True)
        finally:
            cursor.close()
            conn.close()

    def save_datum(self, db_name: str, table_format: sqlalchemy,
                   save_data: dict, batch_size: int=500):
        """
        複合式功能
            - 查詢資料庫, 有無建立; 若有略過
            - 查詢資料表, 有無建立; 若有略過
            - 插入資料以 Merge 方式進行, 並加入批次塞入邏輯
            * FIXME 預計將此功能拆解，分為子方法(插入/查詢/合併)運行
        """
        conn = cursor = None
        try:
            self.__update_connection_string(db_name)
            self.__create_database(db_name)
            self.__create_table(table_format)

            conn = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(f'USE {self.db_name}')

            table_name = table_format.__table__.name
            # cursor.fast_executemany = True # 提高效能

            keys = save_data[list(save_data.keys())[0]].keys()
            keys = [i for i in keys]
            # keys = [f'[{i}]' for i in keys]
            _value = list(save_data.values())

            s_state = f_state = 0
            for idx in range(0, len(_value), batch_size):
                feed_value = [tuple(i.values()) for i in _value[idx:idx + batch_size]]

                # 判斷該鍵值是否已在表格: Merge(查詢, 更新, 插入)
                primary_key = table_format.__primary_key__
                placeholder = ', '.join([f"({', '.join(['?'] * len(keys))})"])
                mapping_cols = ' AND '.join([f'Target.{col} = Source.{col}' for col in keys if col in primary_key])
                update_cols = ', '.join([f'Target.{col} = Source.{col}' for col in keys if col not in primary_key])
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
                    s_state += len(feed_value)
                    self.log_info(f'Store Data In The Database [M: {s_state}, F: {f_state}, T: {len(_value)}]')

                except:
                    f_state += len(feed_value)
                    self.log_error(f'Store Data In The Database [M: {s_state}, F: {f_state}, T: {len(_value)}]', exc_info=True)

        except:
            self.log_error(ERROR_TEXT, exc_info=True)
        finally:
            cursor.close()
            conn.close()

    def get_datum(self, db_name: str, table_format: sqlalchemy, date: datetime=None, **kwargs):
        """
        查詢資料
            TODO 預計加入功能
                -參數時間範圍
                -WHERE SQL 條件篩選
        """
        conn = cursor = None
        try:
            self.__update_connection_string(db_name)
            conn = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(f'USE {self.db_name}')

            # 確認是否該資料表已存在
            table_name = table_format.__table__.name
            sql_cmd = f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
            cursor.execute(sql_cmd)

            # 若否則回傳空字典
            if len(cursor.fetchall()) == 0:
                return {}
            else:
                if 'WHERE' in kwargs:
                    cursor.execute(f"SELECT * FROM {table_name} WHERE {kwargs['WHERE']}")
                else:
                    cursor.execute(f"SELECT * FROM {table_name}")
                try:
                    # columns = [f'[{i[0]}]' for i in cursor.description]
                    columns = [i[0] for i in cursor.description]
                    primary_key = table_format.__primary_key__
                    datum = {}
                    for content in [dict(zip(columns, i)) for i in cursor.fetchall()]:
                        key = ''
                        for k, v in content.items():
                            if k in primary_key:
                                if isinstance(v, datetime):
                                    key += f'{str(v)[:19]}_'
                                else:
                                    key += f'{v}_'
                        datum[key[:-1]] = content

                    return datum
                except:
                    self.log_error(ERROR_TEXT, exc_info=True)

        except:
            self.log_error(ERROR_TEXT, exc_info=True)
        finally:
            cursor.close()
            conn.close()
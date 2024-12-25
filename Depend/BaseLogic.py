# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-26
"""
import pyodbc
from Depend import Account

class BaseLogic:
    def __init__(self):
        self.server = Account.SERVER
        self.database = Account.DATABASE
        self.username = Account.USERNAME
        self.password = Account.PASSWORD
        self.driver = Account.DRIVER

        # SQL Server 連接字串
        self.connection_string = (f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};'
                                  f'UID=your_username;PWD=your_password;Trusted_Connection=yes;')

    def create_database(self, table_name: str):
        """
        建立資料庫
        """
        conn, cursor = None, None
        try:
            conn = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE {table_name}')
            print(f"資料庫 '{table_name}' 建立成功！")

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def create_table(self):
        """
        建立表格
        """
        conn, cursor = None, None
        try:
            conn = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(f'USE {self.database}')

            cursor.execute("""
            CREATE TABLE Employees (
                ID INT PRIMARY KEY,
                Name NVARCHAR(50),
                Position NVARCHAR(50),
                HireDate DATE
            )
            """)
            print("資料表 'Employees' 建立成功！")

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def insert_data(self):
        """
        插入資料
        """
        conn, cursor = None, None
        try:
            conn = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(f'USE {self.database}')

            cursor.execute("""
            INSERT INTO Employees (ID, Name, Position, HireDate)
            VALUES
                (1, 'Alice', 'Manager', '2022-01-01'),
                (2, 'Bob', 'Engineer', '2023-03-15'),
                (3, 'Charlie', 'Analyst', '2024-06-20')
            """)
            conn.commit()  # 提交更改
            print('資料插入成功！')
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
            conn = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = conn.cursor()
            # 欲使用資料庫
            cursor.execute(f'USE {self.database}')

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
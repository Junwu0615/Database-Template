<a href='https://github.com/Junwu0615/Database-Template'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/Database-Template.svg'> 
<a href='https://github.com/Junwu0615/Database-Template'><img alt='GitHub Clones' src='https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count_total&url=https://gist.githubusercontent.com/Junwu0615/65eaa98eafcee3f625a269fa70451f8a/raw/Database-Template_clone.json&logo=github'> </br>
[![](https://img.shields.io/badge/Project-Database_Template-blue.svg?style=plastic)](https://github.com/Junwu0615/Database-Template) 
[![](https://img.shields.io/badge/Language-SQL_Server-blue.svg?style=plastic)](https://www.microsoft.com/zh-tw/sql-server/sql-server-downloads)
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) </br>
[![](https://img.shields.io/badge/Package-pyodbc_5.2.0-green.svg?style=plastic)](https://pypi.org/project/pyodbc/) 

### A.　更新計畫

| 事件 | 敘述 | 更新時間 |
|:----:|-----|:----:|
| 專案上架 | Database Template | 2024-12-25 |
| 建立常用函示 | NormFunction.py | 2024-12-28 |
| 資料表: 模板定義 | 依 TForexQuotes.py 模板畫葫蘆 | 2024-12-28 |
| 更新常用函示 | 加入log異動 / 字串處理 / 數值處理 / 爬蟲連線 | 2024-12-28 |
| 模組化 | 將 SQL 串接 Database 過程模組化，並用繼承方式使用功能 | 進行中 |
| 套件化 | 將整個功能打包成套件，用安裝方式直接使用該功能 | - |

<br>

### B.　SQL 語法 (查詢頁)
#### 新建資料庫
```sql
CREATE DATABASE <MyDatabase>;
```
#### 刪除資料庫順序 : 一律手動，勿程式化
```sql
-- 檢查資料庫是否存在
SELECT name FROM master.sys.databases WHERE name = '<MyDatabase>';

-- 強制斷開所有連接，將資料庫設為單一使用者模式以便刪除。
-- 因為如果有其他使用者正在使用資料庫，直接用 DROP DATABASE 會失敗。
ALTER DATABASE <MyDatabase> SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

-- 直接刪除資料庫及其所有內容。
DROP DATABASE <MyDatabase>;
```

```sql
-- 查詢該表格是否存在
SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = <MyDatabase>;
```

<br>

### C.　Python 串接語法
#### 顯示系統上可用的所有 ODBC 驅動
```py
pyodbc.drivers()
```

<br>

### D.　模型規格紀錄
#### I.　整數類型
| 類型 | 說明 |
|:----|:----|
| Integer | 對應 SQL 的整數類型，如 INT |
| SmallInteger | 對應 SQL 的小整數類型，如 SMALLINT |
| BigInteger | 用於大整數，對應 SQL 的 BIGINT |

#### II.　字符串類型
| 類型 | 說明 |
|:----|:----|
| String(length) | 可變長度的字符串。length 指定最大長度，對應 SQL 的 VARCHAR |
| Text | 不定長度的大文本，對應 SQL 的 TEXT 或 CLOB |
| Unicode(length) | 支持 Unicode 的字符串，類似 String |
| UnicodeText | 支持 Unicode 的長文本，類似 Text |
| CHAR(length) | 固定長度字符串，對應 SQL 的 CHAR |

#### III.　數值類型
| 類型 | 說明 |
|:----|:----|
| Float | 浮點數，對應 SQL 的 FLOAT 或 REAL |
| Numeric(precision, scale) | 精確數值類型，對應 SQL 的 NUMERIC 或 DECIMAL，用於高精度計算 |
| DECIMAL(precision, scale) | 與 Numeric 相同，是其別名 |

#### IV.　日期和時間類型
| 類型 | 說明 |
|:----|:----|
| Date | 僅日期部分，對應 SQL 的 DATE |
| Time | 僅時間部分，對應 SQL 的 TIME |
| DateTime | 日期和時間，對應 SQL 的 DATETIME 或 TIMESTAMP |
| Interval | 時間間隔，對應 SQL 的 INTERVAL |

#### V.　布林值類型
| 類型 | 說明 |
|:----|:----|
| Boolean  | 布林值，對應 SQL 的 BOOLEAN，存儲 True 或 False |

#### VI.　二進制類型
| 類型 | 說明 |
|:----|:----|
| LargeBinary | 二進制數據，對應 SQL 的 BLOB 或 BYTEA |

#### VII.　UUID 類型
| 類型 | 說明 |
|:----|:----|
| UUID | 用於存儲通用唯一標識符（UUID），對應 SQL 的相關類型（如 UUID）|

#### VII.　JSON 類型
| 類型 | 說明 |
|:----|:----|
| JSON | 用於存儲 JSON 數據，對應 SQL 的 JSON 或類似類型 |

<br>

### E.　其他備註
#### 查看 ODBC 版本(名稱) 
```
win + R : odbcad32 -> 切到驅動程式 -> ex: ODBC Driver 17 for SQL Server
```

<br>

### F.　展示成果
![00.jpg](/Sample/00.jpg)

<br>

### G.　資源連結
- [OpenAI ChatGPT](https://openai.com/chatgpt/overview/)
- [輕量級 SQL IDE: Azure Data Studio](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?view=sql-server-ver16&tabs=win-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall) <br>
- [伺服器建立: SQL Server Express](https://www.microsoft.com/zh-tw/sql-server/sql-server-downloads)
- [SqlAlchemy 文章參考](https://developer.aliyun.com/article/1563092)
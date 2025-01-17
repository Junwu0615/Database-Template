<a href='https://github.com/Junwu0615/Database-Template'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/Database-Template.svg'> 
<a href='https://github.com/Junwu0615/Database-Template'><img alt='GitHub Clones' src='https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count_total&url=https://gist.githubusercontent.com/Junwu0615/65eaa98eafcee3f625a269fa70451f8a/raw/Database-Template_clone.json&logo=github'> <br>
[![](https://img.shields.io/badge/Project-Database_Template-blue.svg?style=plastic)](https://github.com/Junwu0615/Database-Template) 
[![](https://img.shields.io/badge/Language-SQL_Server-blue.svg?style=plastic)](https://www.microsoft.com/zh-tw/sql-server/sql-server-downloads) 
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) <br>
[![](https://img.shields.io/badge/Package-pyodbc_5.2.0-green.svg?style=plastic)](https://pypi.org/project/pyodbc/) 
[![](https://img.shields.io/badge/Package-sqlalchemy_2.0.36-green.svg?style=plastic)](https://pypi.org/project/sqlalchemy/) 
[![](https://img.shields.io/badge/Package-colorlog_6.9.0-green.svg?style=plastic)](https://pypi.org/project/colorlog/) 

<br>

## A.　更新計畫

| 事件 | 敘述 | 更新時間 |
|:----:|----|:----:|
| 專案上架 | Database Template | 2024-12-25 |
| 建立常用函示 | developers.package.norm_function | 2024-12-28 |
| 資料表: 模板定義 | 依 developers.model.TForexQuotes 模板畫葫蘆 | 2024-12-28 |
| 更新常用函示 | 日誌打印 / 字串處理 / 數值處理 / 爬蟲連線 | 2024-12-28 |
| 模組化 | 將 SQL 串接 Database 過程模組化，並用繼承方式使用功能 | 2024-12-28 |
| 套件化 | 將整個功能打包成套件，用安裝方式直接使用該功能 | 2024-12-29 |
| 定義制式規格 | update_once & config_once | 2024-12-30 |
| 定義運行狀態 | 詳見 developers.definition.state | 2024-12-30 |
| 加入排程邏輯 | 可依據參數定時設定，到點啟動專案 | 2024-12-30 |
| 查詢資料: 增加可用參數 | SQL WHERE 條件篩選 | 2025-01-09 |
| 查詢資料: 增加可用參數 | 參數時間 | - |
| 更新底層 | 外圍包大型迴圈，基於回傳狀態判斷是否 Retry | - |
| 優化進入點 | __name__ == '__main__' 移至底層 | - |
| 調整 Merge 邏輯 | 用子方法 ( 插入 / 查詢 / 合併 ) 分別進行，不採用官方 Merge 語法 | - |


<br>

## B.　成果展示
![00.gif](/sample/00.gif)

![00.jpg](/sample/00.jpg)

![01.jpg](/sample/01.jpg)

<br>

## C.　套件化安裝
- 本目錄底下執行下方指令 # 若本專案更新，引用套件則會隨著更新
    ```commandline
    pip install -e .
    ```
  - ![03.jpg](/sample/03.jpg)
- developers.package.`sql_account_.py` -> `sql_account.py` 更改欲使用內容
- 開發其他專案時可以直接引用本套件撰寫物件
- ![02.jpg](/sample/02.jpg)

<br>

## D.　學習紀錄

### I.　SQL 語法
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

### II.　Python 串接語法
#### 顯示系統上可用的所有 ODBC 驅動
```py
pyodbc.drivers()
```

<br>

### III.　模型規格紀錄
#### a.　整數類型
| 類型 | 說明 |
|:----|:----|
| Integer | 對應 SQL 的整數類型，如 INT |
| SmallInteger | 對應 SQL 的小整數類型，如 SMALLINT |
| BigInteger | 用於大整數，對應 SQL 的 BIGINT |

#### b.　字符串類型
| 類型 | 說明 |
|:----|:----|
| String(length) | 可變長度的字符串。length 指定最大長度，對應 SQL 的 VARCHAR |
| Text | 不定長度的大文本，對應 SQL 的 TEXT 或 CLOB |
| Unicode(length) | 支持 Unicode 的字符串，類似 String |
| UnicodeText | 支持 Unicode 的長文本，類似 Text |
| CHAR(length) | 固定長度字符串，對應 SQL 的 CHAR |

#### c.　數值類型
| 類型 | 說明 |
|:----|:----|
| Float | 浮點數，對應 SQL 的 FLOAT 或 REAL |
| Numeric(precision, scale) | 精確數值類型，對應 SQL 的 NUMERIC 或 DECIMAL，用於高精度計算 |
| DECIMAL(precision, scale) | 與 Numeric 相同，是其別名 |

#### d.　日期和時間類型
| 類型 | 說明 |
|:----|:----|
| Date | 僅日期部分，對應 SQL 的 DATE |
| Time | 僅時間部分，對應 SQL 的 TIME |
| DateTime | 日期和時間，對應 SQL 的 DATETIME 或 TIMESTAMP |
| Interval | 時間間隔，對應 SQL 的 INTERVAL |

#### e.　布林值類型
| 類型 | 說明 |
|:----|:----|
| Boolean  | 布林值，對應 SQL 的 BOOLEAN，存儲 True 或 False |

#### f.　二進制類型
| 類型 | 說明 |
|:----|:----|
| LargeBinary | 二進制數據，對應 SQL 的 BLOB 或 BYTEA |

#### g.　UUID 類型
| 類型 | 說明 |
|:----|:----|
| UUID | 用於存儲通用唯一標識符（UUID），對應 SQL 的相關類型（如 UUID）|

#### h.　JSON 類型
| 類型 | 說明 |
|:----|:----|
| JSON | 用於存儲 JSON 數據，對應 SQL 的 JSON 或類似類型 |

<br>

### IV.　其他備註
#### 查看 ODBC 版本(名稱) 
```
win + R : odbcad32 -> 切到驅動程式 -> ex: ODBC Driver 17 for SQL Server
```

<br>


## E.　資源連結
- [特別感謝 DL 前輩](https://github.com/dl-jack-123)
- [OpenAI ChatGPT](https://openai.com/chatgpt/overview/)
- [輕量級 SQL IDE: Azure Data Studio](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?view=sql-server-ver16&tabs=win-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall) <br>
- [伺服器建立: SQL Server Express](https://www.microsoft.com/zh-tw/sql-server/sql-server-downloads)
- [SqlAlchemy 文章參考](https://developer.aliyun.com/article/1563092)
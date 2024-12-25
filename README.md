<a href='https://github.com/Junwu0615/Database-Template'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/Database-Template.svg'> 
<a href='https://github.com/Junwu0615/Database-Template'><img alt='GitHub Clones' src='https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count_total&url=https://gist.githubusercontent.com/Junwu0615/65eaa98eafcee3f625a269fa70451f8a/raw/Database-Template_clone.json&logo=github'> </br>
[![](https://img.shields.io/badge/Project-Database_Template-blue.svg?style=plastic)](https://github.com/Junwu0615/Database-Template) 
[![](https://img.shields.io/badge/Language-SQL_Server-blue.svg?style=plastic)](https://www.microsoft.com/zh-tw/sql-server/sql-server-downloads)
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) </br>
[![](https://img.shields.io/badge/Package-pyodbc_5.2.0-green.svg?style=plastic)](https://pypi.org/project/pyodbc/) 



### A.　SQL 語法 (查詢頁)
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

### B.　Python 串接語法
#### 顯示系統上可用的所有 ODBC 驅動
```py
pyodbc.drivers()
```


### C.　其他備註
#### 查看 ODBC 版本(名稱) 
```
win + R : odbcad32 -> 切到驅動程式 -> ex: ODBC Driver 17 for SQL Server
```

### D.　資源連結
- [輕量級 SQL IDE: Azure Data Studio](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?view=sql-server-ver16&tabs=win-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall) <br>
- [伺服器建立: SQL Server Express](https://www.microsoft.com/zh-tw/sql-server/sql-server-downloads)
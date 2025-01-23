# -*- coding: utf-8 -*-
import os

SERVER = os.environ.get('SQL_SERVICE_BROKER_HOST').split(',')[0]
SERVER = 'localhost\SQLExpress' if SERVER is None else SERVER

SERVER_HOST = os.environ.get('SQL_SERVICE_BROKER_HOST').split(',')[-1]

USERNAME = os.environ.get('SQL_SERVICE_LOGIN_USER')
USERNAME = '' if USERNAME is None else USERNAME

PASSWORD = os.environ.get('SQL_SERVICE_LOGIN_PASSWORD')
PASSWORD = '' if PASSWORD is None else PASSWORD

DRIVER = os.environ.get('SQL_SERVICE_DRIVER')
DRIVER = '{ODBC Driver 17 for SQL Server}' if DRIVER is None else f'ODBC Driver {DRIVER} for SQL Server'
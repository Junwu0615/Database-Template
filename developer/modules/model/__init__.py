# -*- coding: utf-8 -*-

# *** 初始化資料庫變數 ***
from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# *** 常見引用 ***
from typing import Union
from enum import Enum, IntEnum, unique
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, DECIMAL, JSON

# *** 將資料庫列成一個清單 ***
__all__ = [
    'Base',
    'Union',
    'Enum',
    'IntEnum',
    'unique',
    'Mapped',
    'mapped_column',
    'Column',
    'Integer',
    'BigInteger',
    'String',
    'Unicode',
    'DateTime',
    'DECIMAL',
    'JSON',
]
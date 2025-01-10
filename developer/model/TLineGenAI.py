# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2025-01-10
"""
from typing import Union
from enum import Enum, IntEnum, unique
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, BigInteger, DECIMAL, Unicode

@unique
class TLineGenAIField(Enum):
    DB_TYPE          =        'DataCollect',                 '收集庫類型'
    DATA_LEVEL       =        'L1',                          '一階資料'
    DB_NAME          =        DB_TYPE[0] + DATA_LEVEL[0],    '資料庫名稱'

    TABLE_NAME       =        'TLineGenAI',                  'LineBot結合GenAI之收集用戶數據'

    USER_ID          =        'USER_ID',                     '商品代碼'
    TEXT_COUNT       =        'TEXT_COUNT',                  '接收字串次數'
    MEDIA_COUNT      =        'MEDIA_COUNT',                 '接收媒體次數'
    A_SERVE          =        'A_SERVE',                     "creator's github"
    B_SERVE          =        'B_SERVE',                     'identify food and feedback'
    C_SERVE          =        'C_SERVE',                     'gif meme name search'
    D_SERVE          =        'D_SERVE',                     "creator's dashboard"
    E_SERVE          =        'E_SERVE',                     'human companion robot'
    F_SERVE          =        'F_SERVE',                     'generate self-introduction'

    def __new__(cls, value: str, name: str) -> Union['TLineGenAIField', str]:
        callback = object.__new__(cls)
        callback._value_ = value
        callback.name_zh_tw = name
        return callback

Base = declarative_base()
class TLineGenAIFormat(Base):
    __tablename__ = 'TLineGenAI'
    __primary_key__ = [
        TLineGenAIField.USER_ID.value,
    ]
    __primary_key_symbol__ = [f'[{i}]' for i in __primary_key__]

    USER_ID = mapped_column(Unicode(128), primary_key=True)
    TEXT_COUNT = mapped_column(Integer, nullable=True)
    MEDIA_COUNT = mapped_column(Integer, nullable=True)
    A_SERVE = mapped_column(Integer, nullable=True)
    B_SERVE = mapped_column(Integer, nullable=True)
    C_SERVE = mapped_column(Integer, nullable=True)
    D_SERVE = mapped_column(Integer, nullable=True)
    E_SERVE = mapped_column(Integer, nullable=True)
    F_SERVE = mapped_column(Integer, nullable=True)
# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-27
"""
from datetime import datetime

from enum import Enum, IntEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, DECIMAL, Unicode

class TForexQuotesField(Enum):
    DB_TYPE          =        'DataCollect',                 '收集庫類型'
    TABLE_LEVEL      =        'L1',                          '一階資料'
    TABLE_DB         =        DB_TYPE[0] + TABLE_LEVEL[0],   '資料庫名稱'

    TABLE_NAME       =        'TForexQuotes',                '外匯收報價'

    CREATEDATETIME   =        'CreateDateTime',              '數據日期'
    SYMBOL           =        'Symbol',                      '商品代碼'
    INTERVAL         =        'Interval',                    '時間戳記'
    OPEN             =        'Open',                        '開盤價'
    HIGH             =        'High',                        '最高價'
    LOW              =        'Low',                         '最低價'
    CLOSE            =        'Close',                       '收盤價'
    VOLUME           =        'Volume',                      '交易量'

    def __new__(cls, value, name):
        ret_obj = object.__new__(cls)
        ret_obj._value_ = value
        ret_obj.name_zh_tw = name
        return ret_obj

Base = declarative_base()
class TableFormat(Base):
    __tablename__ = 'TForexQuotes'
    __primary_key__ = [
        TForexQuotesField.CREATEDATETIME.value,
        TForexQuotesField.SYMBOL.value,
        TForexQuotesField.INTERVAL.value,
    ]
    __primary_key__ = [f'[{i}]' for i in __primary_key__]

    CreateDateTime = mapped_column(DateTime, primary_key=True)
    Symbol = mapped_column(Unicode(12), primary_key=True)
    Interval = mapped_column(Unicode(6), primary_key=True)

    Open = mapped_column(DECIMAL(19, 2), nullable=True)
    High = mapped_column(DECIMAL(19, 2), nullable=True)
    Low = mapped_column(DECIMAL(19, 2), nullable=True)
    Close = mapped_column(DECIMAL(19, 2), nullable=True)
    Volume = mapped_column(Integer, nullable=True)
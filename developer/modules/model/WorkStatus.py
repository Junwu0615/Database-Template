# -*- coding: utf-8 -*-
from developer.modules.sql.models import (Base, Union, Enum, IntEnum, unique,
                                          Mapped, mapped_column,
                                          Column, DateTime, Integer, BigInteger,
                                          DECIMAL, Unicode, String)

@unique
class Status(IntEnum):
    OK                =        200,    '成功'
    OK_SKIP           =        201,    '成功_略過'
    OK_EMPTY          =        202,    '成功_空資料'

    ERR_UNKNOWN       =        400,    '未知錯誤'
    ERR_NETWORK       =        404,    '網路錯誤'
    ERR_TIMEOUT       =        408,    '請求逾時'


    def __new__(cls, value: int, name: str):
        callback = int.__new__(cls)
        callback._value_ = value
        callback.name_zh_tw = name
        return callback


    def __str__(self) -> str:
        return f'<{self.__class__.__name__}.{self.name}: {self.value}>'
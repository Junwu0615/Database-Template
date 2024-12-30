# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-30
"""
from typing import Union
from enum import IntEnum, unique

@unique
class State(IntEnum):
    OK                =        0,    '成功'
    OK_SKIP           =        1,    '成功_略過'
    OK_EMPTY          =        2,    '成功_空資料'

    ERROR             =        3,    '失敗'
    NETWORK_ERROR     =        4,    '網路錯誤'
    UNKNOWN           =        5,    '未知錯誤'


    def __new__(cls, value: int, name: str) -> Union['State', str]:
        callback = int.__new__(cls)
        callback._value_ = value
        callback.name_zh_tw = name
        return callback

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}.{self.name}: {self.value}>'
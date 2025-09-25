# -*- coding: utf-8 -*-
import os, sys, time, json, copy, logging, urllib3
import re, collections, operator, random, math
import requests, statistics, pathlib

from tqdm import tqdm
from dotenv import load_dotenv
from colorlog import ColoredFormatter
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta, timezone
from typing import Callable, Iterator, Tuple, Any, Dict, List, Optional

MODULE_NAME = __name__.upper()

SHORT_FORMAT = '%Y-%m-%d'
SHORT_FORMAT_2 = '%Y/%m/%d'
LONG_FORMAT = '%Y-%m-%d %H:%M:%S'
LONG_T_FORMAT = '%Y-%m-%dT%H:%M:%S'

TZ_UTC_0 = timezone(timedelta(hours=0))
TZ_UTC_8 = timezone(timedelta(hours=8))


class DecimalEncoder(json.JSONEncoder):
    """
    TODO 於寫入時可將 Decimal 轉為字串
         json_str = json.dumps(item, ensure_ascii=False, cls=DecimalEncoder)
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)


def exit_program(self):
    raise KeyboardInterrupt(f'{__name__}，偵測到 Ctrl+C，正在關閉服務...')


def convert_to_common(data):
    """
    TODO 遞迴地將字典中的所有字串數字轉換為 int 或 float。
    """
    if isinstance(data, dict):
        return {k: convert_to_common(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_common(item) for item in data]
    elif isinstance(data, str):
        # 嘗試將字串轉為數字
        try:
            # 檢查是否為整數
            if data.isdigit():
                return int(data)
            # 檢查是否為浮點數或 Decimal
            elif '.' in data or 'e' in data or 'E' in data:
                return float(data)
        except ValueError:
            # 如果轉換失敗，保持為字串
            pass
    return data


def remove_key_recursively(data, key_to_remove='') -> Any:
    """
    TODO 遞迴地從字典或列表中移除指定的鍵值對
         * Args :
            data : 要處理的字典或列表
            key_to_remove : 要移除的鍵名
         * Returns :
            移除指定鍵後的字典或列表
    """
    if isinstance(data, dict):
        # 創建一個新的字典，過濾掉要移除的鍵，並遞迴處理其值
        return {
            key: remove_key_recursively(value, key_to_remove)
            for key, value in data.items()
            if key != key_to_remove
        }
    elif isinstance(data, list):
        # 遞迴處理列表中的每個元素
        return [remove_key_recursively(item, key_to_remove) for item in data]
    else:
        # 如果是基本型別，直接返回
        return data


def create_folder(path: str):
    """
    TODO 單一函式創建檔案夾
        os.makedirs(str(getattr(pathlib.Path(file_path), 'parent')), exist_ok=True)
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def trans_decimal(target, decimal_num: str) -> Decimal:
    return Decimal(target).quantize(Decimal(decimal_num), rounding=ROUND_HALF_UP)


def trans_replace(target: str, symbol_list: list) -> str:
    for symbol in symbol_list:
        target = target.replace(symbol, '')
    return target


def get_now(hours: int=None, minutes: int=None, seconds: int=None, tzinfo: timezone=None) -> datetime:
    target_time = datetime.utcnow()

    if hours is not None:
        target_time += timedelta(hours=hours)

    if minutes is not None:
        target_time += timedelta(minutes=minutes)

    if seconds is not None:
        target_time += timedelta(seconds=seconds)

    if tzinfo is not None:
        target_time = target_time.replace(tzinfo=tzinfo)

    return target_time


def trans_datetime(target: str, date_format: str, tz: timezone=TZ_UTC_8) -> datetime:
    # 轉台灣時間 UTC +8
    return datetime.strptime(target, date_format).replace(tzinfo=tz)


def trans_timestamp(target, change_num: float=0, tz: timezone=TZ_UTC_8) -> datetime:
    # 轉台灣時間 UTC +8
    return datetime.fromtimestamp(target + change_num).replace(tzinfo=tz)
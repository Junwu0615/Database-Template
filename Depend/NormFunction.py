# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-28
"""
from dateutil import tz
from datetime import datetime
from requests import Session, Response
from decimal import Decimal, ROUND_HALF_UP

DATE_YMD_ONE = '%Y-%m-%d'
DATE_YMD_TWO = '%Y/%m/%d'

class NormLogic:
    def __init__(self):
        self.session = Session()

    def trans_decimal(self, target, decimal_num: str) -> Decimal:
        return Decimal(target).quantize(Decimal(decimal_num), rounding=ROUND_HALF_UP)

    def trans_replace(self, target: str, symbol_list: list) -> str:
        for symbol in symbol_list:
            target = target.replace(symbol, '')
        return target

    def trans_datetime(self, target: str, date_format: str) -> datetime:
        # 轉成台灣時間 UTC +8
        return datetime.strptime(target, date_format).replace(tzinfo=tz.gettz('Asia/Taipei'))

    def trans_timestamp(self, target) -> datetime:
        # 轉成台灣時間 UTC +8
        return datetime.fromtimestamp(target).replace(tzinfo=tz.gettz('Asia/Taipei'))

    def http_get(self, url: str) -> Response:
        headers = None
        return self.session.get(url, headers=headers)

    def http_post(self, url: str, payload: dict=None, data_json: bool=True) -> Response:
        headers = None
        if data_json:
            return self.session.get(url, data=payload, headers=headers)
        else:
            return self.session.get(url, json=payload, headers=headers)

    def log_info(self):
        pass

    def log_warning(self):
        pass

    def log_error(self):
        pass
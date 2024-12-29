# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-29
"""
import os, logging
from dateutil import tz
from datetime import datetime
from colorlog import ColoredFormatter
from requests import Session, Response
from decimal import Decimal, ROUND_HALF_UP

DATE_YMD_ONE = '%Y-%m-%d'
DATE_YMD_TWO = '%Y/%m/%d'
DATE_YMD_3TH = '%Y-%m-%d %H:%M:%S'

class NormLogic:
    def __init__(self):
        self.session = Session()
        self.logger = None
        self.logger_settings()

    def logger_settings(self):
        colors_config = {
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'DEBUG': 'green',
            'CRITICAL': 'bold_red',
        }
        fmt = "%(log_color)s[%(asctime)s] %(levelname)s: %(message)s"
        date_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = ColoredFormatter(fmt=fmt,
                                     datefmt=date_fmt,
                                     log_colors=colors_config,
                                     )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

    def trans_decimal(self, target, decimal_num: str) -> Decimal:
        return Decimal(target).quantize(Decimal(decimal_num), rounding=ROUND_HALF_UP)

    def trans_replace(self, target: str, symbol_list: list) -> str:
        for symbol in symbol_list:
            target = target.replace(symbol, '')
        return target

    def trans_datetime(self, target: str, date_format: str) -> datetime:
        # 轉台灣時間 UTC +8
        return datetime.strptime(target, date_format).replace(tzinfo=tz.gettz('Asia/Taipei'))

    def trans_timestamp(self, target, change_num: float=0) -> datetime:
        # 轉台灣時間 UTC +8
        return datetime.fromtimestamp(target + change_num).replace(tzinfo=tz.gettz('Asia/Taipei'))

    def http_get(self, url: str) -> Response:
        headers = None
        return self.session.get(url, headers=headers)

    def http_post(self, url: str, payload: dict=None, data_json: bool=True) -> Response:
        headers = None
        if data_json:
            return self.session.get(url, data=payload, headers=headers)
        else:
            return self.session.get(url, json=payload, headers=headers)

    def log_info(self, ret_text: str):
        self.logger.info(ret_text)

    def log_warning(self, ret_text: str):
        self.logger.warning(ret_text)

    def log_error(self, ret_text: str, exc_info: bool=False):
        self.logger.error(ret_text, exc_info=exc_info)

    def create_folder(self, path: str):
        # Create folder & Check Path Folder
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
# -*- coding: utf-8 -*-
from requests import Session, Response
from developer.utils.normal import *

class CrawlerLogic:
    def __init__(self, logger: logging.Logger=None):
        self.logger = logger
        self.session = Session()


    def http_get(self, url: str) -> Response:
        headers = None
        return self.session.get(url, headers=headers)


    def http_post(self, url: str, payload: dict=None, data_json: bool=True) -> Response:
        headers = None
        if data_json:
            return self.session.get(url, data=payload, headers=headers)
        else:
            return self.session.get(url, json=payload, headers=headers)
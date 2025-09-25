# -*- coding: utf-8 -*-
"""
send_message 功能 : 發送異常狀態至 telegram
Notice: token 需用個人帳戶申請(免費)
"""
from developer.utils.normal import *

MODULE_NAME = __name__.upper()

def send_message(msg: str='success', logger: logging.Logger=None,
                 bot_token: str=None, chat_id: str=None,
                 timeout: int=2):

    if bot_token is None:
        raise Exception('Telegram: bot_token 未設定')

    if chat_id is None:
        raise Exception('Telegram: chat_id 未設定')

    if logger is None:
        raise Exception('Telegram: logger 未設定')

    replace_list = [':', '&']
    trans_replace(msg, replace_list)

    url = (f'https://api.telegram.org/bot{bot_token}/'
           f'sendMessage?chat_id={chat_id}&'
           f'text={msg}')
    try:
        requests.post(url, timeout=timeout)

    except Exception as e:
        logger.error(f'[{MODULE_NAME}] 發送失敗')
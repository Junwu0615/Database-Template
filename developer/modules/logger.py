# -*- coding: utf-8 -*-
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler
from developer.utils.normal import *

MODULE_NAME = __name__.upper()

TITLE_SYMBOL_NUMBER = 20
COLORS_CONFIG = {
    'INFO': 'white',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'DEBUG': 'green',
    'CRITICAL': 'bold_red',
}
FILE_FMT = '[%(asctime)s] %(levelname)s: %(message)s'
CONSOLE_FMT = '%(log_color)s[%(asctime)s] %(levelname)s: %(message)s'

class Logger:
    def __init__(self, console_name: str=None, file_name: str=None, use_docker=None,
                 file_path: str=None, max_bytes: int=(15 * 1024 * 1024),
                 backup_count: int=100):

        if file_path is None and file_name is not None and use_docker is None:
            file_path = 'log' + file_name.replace('.', '/') + '.txt'

        elif file_path is None and file_name is not None and use_docker is not None:
            file_path = use_docker + file_name.replace('.', '/') + '.txt'

        self.console_log = None
        if console_name is not None:
            self.console_log = self._console_logging_settings(console_name)

        self.file_log = None
        if file_name is not None:
            self.file_log = self._file_logging_settings(file_name, file_path, max_bytes, backup_count)


    def _console_logging_settings(self, console_name: str) -> logging.Logger:
        logger = logging.getLogger(__name__ + console_name)
        logger.setLevel(logging.DEBUG)

        # 關鍵步驟：在新增前，先移除並關閉舊的 handlers
        if logger.hasHandlers():
            for handler in logger.handlers:
                handler.close()
            logger.handlers.clear()

        # 創建一個 StreamHandler 將日誌顯示在主控台
        console_handler = logging.StreamHandler()

        # 日誌風格
        console_handler.setFormatter(
            ColoredFormatter(fmt=CONSOLE_FMT,
                             datefmt=LONG_FORMAT,
                             log_colors=COLORS_CONFIG)
        )

        # 日誌等級
        console_handler.setLevel(logging.DEBUG)

        logger.addHandler(console_handler)
        return logger


    def _file_logging_settings(self, file_name: str, file_path: str,
                               max_bytes: int, backup_count: int) -> logging.Logger:
        # 創建資料夾
        os.makedirs(str(getattr(pathlib.Path(file_path), 'parent')), exist_ok=True)

        logger = logging.getLogger(__name__ + file_name)
        logger.setLevel(logging.DEBUG)

        # 關鍵步驟：在新增前，先移除並關閉舊的 handlers
        if logger.hasHandlers():
            for handler in logger.handlers:
                handler.close()
            logger.handlers.clear()

        # 創建一個 FileHandler 將日誌寫入檔案
        file_handler = RotatingFileHandler(file_path,
                                           maxBytes=max_bytes,
                                           backupCount=backup_count,
                                           encoding='utf-8')

        # 日誌風格
        file_handler.setFormatter(
            logging.Formatter(
                fmt=FILE_FMT,
                datefmt=LONG_FORMAT)
        )

        # 日誌等級
        file_handler.setLevel(logging.DEBUG)

        logger.addHandler(file_handler)
        return logger


    def info(self, msg: str='', console_b: bool=True, file_b: bool=True, **kwargs):
        """
        kwargs ...not defined, but can be used to pass additional parameters
        """
        if console_b and self.console_log is not None:
            getattr(self.console_log, 'info')(msg)

        if file_b and self.file_log is not None:
            getattr(self.file_log, 'info')(msg)


    def warning(self, msg: str='', console_b: bool=True, file_b: bool=True, **kwargs):
        """
        kwargs ...not defined, but can be used to pass additional parameters
        """
        if console_b and self.console_log is not None:
            getattr(self.console_log, 'warning')(msg)

        if file_b and self.file_log is not None:
            getattr(self.file_log, 'warning')(msg)


    def error(self, msg: str='', exc_info: bool=True, console_b: bool=True, file_b: bool=True, **kwargs):
        """
        kwargs ...not defined, but can be used to pass additional parameters
        """
        if console_b and self.console_log is not None:
            if exc_info:
                getattr(self.console_log, 'error')(msg, exc_info=exc_info)
            else:
                getattr(self.console_log, 'error')(msg)

        if file_b and self.file_log is not None:
            if exc_info:
                getattr(self.file_log, 'error')(msg, exc_info=exc_info)
            else:
                getattr(self.file_log, 'error')(msg)


    def title_log(self, title_name: str) -> str:
        return f"\n{'='*TITLE_SYMBOL_NUMBER} {title_name} {'='*TITLE_SYMBOL_NUMBER}\n\n"
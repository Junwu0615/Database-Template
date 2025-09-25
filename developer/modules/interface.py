# -*- coding: utf-8 -*-
import schedule
from schedule import every, run_pending
from developer.utils.normal import *
from developer.modules.crawler import CrawlerLogic
from developer.modules.ms_sql.sql_server import MSDatabase

MODULE_NAME = __name__.upper()

# noinspection PyTypeChecker
class Interface(CrawlerLogic, MSDatabase):
    def __init__(self, do_time: list, logger: logging.Logger):
        CrawlerLogic.__init__(self, logger)
        MSDatabase.__init__(self, logger)
        self.logger = logger
        self.config_once()
        self.originate()
        if do_time:
            self.var_next_run = []
            self.settings_schedule(do_time, self.originate)
            self.schedule_run()


    def settings_schedule(self, do_time, function):
        """
        * 定時排程設定 *
            -不使用 do_time <為空> 或 <註解> 即可
            -[周一至周日]: 英文字首排序 + 空格 + 欲啟動時間(台灣時間)
            -字母大寫意味著 <啟動> ; 反之小寫 <不啟動>
        """
        for event in do_time:
            d = event.split('=')[0]
            t = event.split('=')[-1]
            if d[0] == 'M':
                every().monday.at(t).do(function)
            if d[1] == 'T':
                every().tuesday.at(t).do(function)
            if d[2] == 'W':
                every().wednesday.at(t).do(function)
            if d[3] == 'T':
                every().thursday.at(t).do(function)
            if d[4] == 'F':
                every().friday.at(t).do(function)
            if d[5] == 'S':
                every().saturday.at(t).do(function)
            if d[6] == 'S':
                every().sunday.at(t).do(function)


    def schedule_next_run(self) -> str:
        return sorted([i.next_run for i in schedule.get_jobs()])[0].__str__()


    def schedule_run(self):
        while True:
            get_next_time = self.schedule_next_run()
            if get_next_time not in self.var_next_run:
                self.var_next_run += [get_next_time]
                self.logger.warning(f'[{MODULE_NAME}] Schedule Next Run: {get_next_time}')
            run_pending()
            time.sleep(1)


    def config_once(self):
        pass


    def update_once(self):
        pass


    def originate(self):
        self.var_next_run = []
        ret = self.update_once()
        self.logger.warning(f'[{MODULE_NAME}] {ret}')
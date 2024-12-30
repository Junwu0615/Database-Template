# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-31
"""
import time, schedule
from datetime import datetime
from schedule import every, run_pending

from developer.definition.state import State
from developer.package.norm_function import NormLogic
from developer.package.sql_server import DatabaseLogic

# noinspection PyTypeChecker
class Interface(NormLogic, DatabaseLogic):
    def __init__(self, do_time: list):
        NormLogic.__init__(self)
        DatabaseLogic.__init__(self)
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
            if d[0].upper() == 'M':
                every().monday.at(t).do(function)
            if d[1].upper() == 'T':
                every().tuesday.at(t).do(function)
            if d[2].upper() == 'W':
                every().wednesday.at(t).do(function)
            if d[3].upper() == 'T':
                every().thursday.at(t).do(function)
            if d[4].upper() == 'F':
                every().friday.at(t).do(function)
            if d[5].upper() == 'S':
                every().saturday.at(t).do(function)
            if d[6].upper() == 'S':
                every().sunday.at(t).do(function)

    def schedule_next_run(self) -> str:
        return sorted([i.next_run for i in schedule.get_jobs()])[0].__str__()

    def schedule_run(self):
        while True:
            get_next_time = self.schedule_next_run()
            if get_next_time not in self.var_next_run:
                self.var_next_run += [get_next_time]
                self.log_warning(f'Schedule Next Run: {get_next_time}')
            run_pending()
            time.sleep(1)

    def config_once(self):
        pass

    def update_once(self):
        pass

    def originate(self):
        self.var_next_run = []
        ret = self.update_once()
        self.log_warning(ret)
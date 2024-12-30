# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-30
"""
import time, schedule
from datetime import datetime
from schedule import every, run_pending

from developers.definition.state import State
from developers.package.norm_function import NormLogic
from developers.package.sql_server import DatabaseLogic

class Interface(NormLogic, DatabaseLogic):
    def __init__(self, todo_time: list):
        NormLogic.__init__(self)
        DatabaseLogic.__init__(self)
        self.var_next_run = []
        self.settings_schedule(todo_time, self.originate)
        self.config_once()
        self.originate()
        self.schedule_run()

    def settings_schedule(self, todo_time, function):
        """
        * 定時排程設定 *
            -不使用 todo_time <為空> 或 <註解> 即可
            -[周一至周日]: 英文字首排序 + 空格 + 欲啟動時間(台灣時間)
            -字母大寫意味著 <啟動> ; 反之小寫 <不啟動>
        """
        for event in todo_time:
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
        timestamp = self.get_datetime_now().timestamp() + schedule.idle_seconds()
        return datetime.fromtimestamp(timestamp).__str__()

    def schedule_run(self):
        while True:
            if self.schedule_next_run() not in self.var_next_run:
                self.var_next_run += [self.schedule_next_run()]
                self.log_warning(f'Schedule Next Run: {self.schedule_next_run()}')
            run_pending()
            time.sleep(1)

    def config_once(self):
        pass

    def update_once(self):
        pass

    def originate(self):
        self.var_next_run = []
        ret = self.update_once()
        self.log_warning(f'{repr(ret)}')
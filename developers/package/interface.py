# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-30
"""
from developers.definition.state import State
from developers.package.norm_function import NormLogic
from developers.package.sql_server import DatabaseLogic

class Interface(NormLogic, DatabaseLogic):
    def __init__(self):
        NormLogic.__init__(self)
        DatabaseLogic.__init__(self)
        self.originate()

    def config_onece(self):
        pass

    def update_once(self):
        pass

    def originate(self):
        self.config_onece()
        ret = self.update_once()
        self.log_warning(f'{repr(ret)}')
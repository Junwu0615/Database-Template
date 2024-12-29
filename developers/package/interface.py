# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-29
"""
from developers.package.norm_function import NormLogic
from developers.package.sql_server import DatabaseLogic

class Interface(NormLogic, DatabaseLogic):
    def __init__(self):
        NormLogic.__init__(self)
        DatabaseLogic.__init__(self)

    def update_once(self):
        pass
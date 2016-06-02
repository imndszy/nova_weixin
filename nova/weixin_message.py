# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from get_user_info import Student
from lib.database import mysql


class NovaMessage(Student):
    def __init__(self, openid):
        Student.__init__(openid)
    pass

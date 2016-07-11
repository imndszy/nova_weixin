# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from lib.database import mysql


def get_bind_info(stuid,passwd):
    sql = "select *from biding where stuid = %s" % stuid

    @mysql(sql)
    def get_result(results=''):
        return results
    result = get_result()
    if(result):
        return result[0]
    return 0


def verify_password(stuid,passwd):
    sql = "select certificationcode from password where stuid = %s" % stuid


    @mysql(sql)
    def get_password(results=''):
        return results
    result = str(get_password()[0])
    if(result == passwd):
        return True
    else:
        return False

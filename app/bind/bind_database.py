# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from app.lib.database import mysql


def get_bind_info(stuid,passwd):
    sql = "select *from biding where stuid = %s" % stuid

    @mysql(sql)
    def get_result(results=''):
        return results
    result = get_result()
    print result
    if result :
        return result[0]
    return 0


def verify_password(stuid,passwd):
    sql = "select certificationcode from password where stuid = %s" % stuid


    @mysql(sql)
    def get_password(results=''):
        return results
    results = get_password()
    if results!=-1:
        result = str(results[0])
        if(result == passwd):
            return True
        else:
            return False
    return -1

def save_new_student(stuid):
    sql = "insert into biding values('',0,%s,'','',0,0,0)" % stuid


    @mysql(sql)
    def save(results=''):
        return results
    if save() != -1:
        return 0
    else:
        return -1



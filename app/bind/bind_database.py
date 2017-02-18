# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from nova_weixin.packages.novamysql import select_int, insert
from nova_weixin.packages.novalog import NovaLog

log = NovaLog(path='log/db_operation.log')

def verify_password(stuid, passwd):
    result = str(select_int('select certificationcode from password where stuid =?', stuid))

    if not result:
        log.info("no certificationcode in database for student {stuid}".format(stuid=stuid))
        return -1
    if result == passwd:
        return True
    else:
        return False


def save_new_student(stuid):
    result = insert('biding', openid='', stuid=stuid, subscribe='', tempcode='', latestreq=0, limited_time=0, lastrequest=0)

    if result == 1:
        return 0
    else:
        log.warn("insert into database error -- save_new_student")
        return -1

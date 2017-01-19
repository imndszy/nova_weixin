# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from nova_weixin.packages.novamysql import select_int, insert
# from nova_weixin.app.lib.database import mysql


# def get_bind_info(stuid, passwd):
#     sql = "select *from biding where stuid = %s" % stuid
#
#     @mysql(sql)
#     def get_result(results=''):
#         return results
#     result = get_result()
#     print result
#     if result:
#         return result[0]
#     return 0


def verify_password(stuid, passwd):
    result = select_int('select certificationcode from password where stuid =?',stuid)
    # sql = "select certificationcode from password where stuid = %s" % stuid
    #
    # @mysql(sql)
    # def get_password(results=''):
    #     return results
    # results = get_password()
    # if results != -1:
    #     result = str(results[0])
    #     if(result == passwd):
    #         return True
    #     else:
    #         return False
    if not result:
        return -1
    if(result == passwd):
        return True
    else:
        return False


def save_new_student(stuid):
    result = insert('biding', openid='', stuid=stuid, subscribe='', tempcode='', latestreq=0, limited_time=0, lastrequest=0)
    # sql = "insert into biding values('',%d,'','',0,0,0)" % stuid
    #
    # @mysql(sql)
    # def save(results=''):
    #     return results
    # if save() != -1:
    #     return 0
    # else:
    #     return -1
    if result == 1:
        return 0
    else:
        return -1

# if __name__ == '__main__':
#     print get_bind_info(141270033,'asd')

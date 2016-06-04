# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from nova_weixin.lib.database import mysql


def classes():
    sql = "select *from member"

    @mysql(sql)
    def get_classes(results=''):
        return results

    result = get_classes()
    class_dict = dict()
    for i in result:
        class_dict[i[2]] = i[1]

    return class_dict

def stu(classes):
    if len(classes)<1:
        return -1
    stu_dict = dict()
    for i in classes:
        sql = "select stuid,name from stuinfo where class='" + i + "'"

        @mysql(sql)
        def get_stu(results=''):
            return results
        result = get_stu()
        stu_dict[i] = result
    return stu_dict

def create_html(stu_dict):
    pass





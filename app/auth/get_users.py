# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
# from nova_weixin.app.lib.database import mysql
from nova_weixin.packages.novamysql import select


def classes():
    class_list = select('select * from member')
    class_dict = dict()

    for i in class_list:
        class_dict[i['class']] = i['name']
    return class_dict


def stu(classes_seq):
    """
    :param classes_seq: list of class name
    :return: {class_name:[(stuid,stu_name),()...],class_name2:[(),()]}
    """
    if len(classes_seq) < 1:
        return -1
    stu_dict = dict()

    for i in classes_seq:
        stus = select('select stuid,name from stuinfo where class=?', i)
        result = [(j['stuid'],j['name']) for j in stus]
        stu_dict[i] = result
    return stu_dict

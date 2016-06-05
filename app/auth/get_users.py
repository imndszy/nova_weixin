# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from lib.database import mysql
import os


def classes():
    """
    :return: example return :
    {u'111111': u'\u5c71\u897f', u'131278': u'13\u5de5\u5de5',
    u'131279': u'13\u91d1\u5de5', u'151271': u'15\u81ea\u52a8',
    u'121271': u'12\u4fe1\u5de5', u'121270': u'12\u81ea\u52a8',
    u'131270': u'13\u81ea\u52a8', u'131271': u'13\u4fe1\u5de5',
    u'151278': u'15\u5de5\u5de5', u'121279': u'12\u91d1\u5de5',
    u'121278': u'12\u5de5\u5de5', u'141271': u'14\u4fe1\u5de5',
    u'141270': u'14\u81ea\u52a8', u'141279': u'14\u91d1\u5de5',
    u'141278': u'14\u5de5\u5de5'}
    """
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
    """
    get students in separate class
    :param classes: list of class_id
    :return: students dict whose key is class_id
    """
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

def create_class_html(class_dict):
    pwd = os.path.abspath(os.path.dirname(__file__))
    pwd = pwd[:-4]+'templates/auth/class.html'
    content = u"""{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block title %}Nova {% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>choose classes first</h1>
</div>
<div>
        <h3>全选后再选中某个班级代表排除这个班级</h3>
</div>
<form method="post">
<input type = "checkbox" name = "checked" value ="choose_all"> 全选
"""
    for key,value in class_dict.items():
        temp = u'<input type="checkbox" name="checked" value="%s" > %s <br/>\n' % (key,value)
        content = content+temp+'<br/>'
    content = content+u"""<input type="submit">
</form>
{% endblock %}"""
    content = content.encode('utf-8')
    with open(pwd,'w') as class_file:
        class_file.write(content)

def create_stu_html(stu_dict,class_dict):
    pwd = os.path.abspath(os.path.dirname(__file__))
    pwd = pwd[:-4]+'templates/auth/stu.html'
    content = u"""{% extends "base.html" %}
    {% import "bootstrap/wtf.html" as wtf %}
    {% block title %}Nova {% endblock %}

    {% block page_content %}
    <div class="page-header">
        <h1>choose students</h1>
    </div>
    <div>
        <h3>全选后再选中某个学生代表排除这个学生</h3>
    </div>
    <form method="post">
    <input type = "checkbox" name = "checked" value ="choose_stu_all"> 全选 <br/>
    """
    for key,value in stu_dict.items():
        temp = u'<p>%s</p><br/>\n' % class_dict[key]
        for j in value:
            temp = temp+u'<input type="checkbox" name="checked" value="%s" > %s \n' % (str(j[0]),str(j[0])+' '+j[1])
        content = content+temp+'<br/>'
    content = content + u"""<input type="submit">
    </form>
    {% endblock %}"""
    content = content.encode('utf-8')
    with open(pwd, 'w') as class_file:
        class_file.write(content)

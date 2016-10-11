# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os
from nova_weixin.app.lib.database import mysql


def classes():
    # type: () -> object
    sql = "select *from member"

    @mysql(sql)
    def get_classes(results=''):
        return results

    result = get_classes()
    if result == -1:
        return -1
    class_dict = dict()
    for i in result:
        class_dict[i[2]] = i[1]
    return class_dict


def stu(classes_seq):
    if len(classes_seq) < 1:
        return -1
    stu_dict = dict()
    for i in classes_seq:
        sql = "select stuid,name from stuinfo where class='" + i + "'"

        @mysql(sql)
        def get_stu(results=''):
            return results
        result = get_stu()
        stu_dict[i] = result
    return stu_dict


def create_class_html(class_dict):
    pwd = os.path.abspath(os.path.dirname(__file__))
    pwd = pwd[:-4] + 'templates/auth/class.html'
    content = u"""{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block title %}Nova {% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>choose classes first</h1>
</div>
<form method="post">
<input type = "checkbox" name = "checked" value ="choose_all"> 全选 <br/>
"""
    for key, value in class_dict.items():
        temp = u'<input type="checkbox" name="checked" value="%s" > %s \n' % (key, value)
        content = content+temp+'<br/>'
    content = content+u"""<input type="submit">
</form>
{% endblock %}"""
    content = content.encode('utf-8')
    with open(pwd, 'w') as class_file:
        class_file.write(content)


def create_stu_html(stu_dict, class_dict):
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
        temp = u'<p>%s</p>\n' % class_dict[key]
        for j in value:
            temp = temp+u'<input type="checkbox" name="checked" value="%s" > %s \n' % (str(j[0]),str(j[0])+' '+j[1])
        content = content+temp+'<br/>'
    content = content + u"""<input type="submit">
    </form>
    {% endblock %}"""
    content = content.encode('utf-8')
    with open(pwd, 'w') as class_file:
        class_file.write(content)


if __name__ == '__main__':
    class_dict = classes()
    stu_dict = stu(class_dict.keys())
    create_stu_html(stu_dict,class_dict)
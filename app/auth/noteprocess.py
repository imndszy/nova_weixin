# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from lib.database import mysql
from app.weixin.template import send_common_template_msg
from nova.get_user_info import get_openid


def note_index(article_url,image_url,stu_list,nid):
    stu_text = ''
    for i in stu_list:
        stu_text = stu_text+i
    sql = "insert into noteindex valus(%s,%s,0,'','%s',0)" % (nid,nid,stu_text)

    @mysql(sql)
    def insert(results=''):
        return results
    return 0


def note_content(article_url,image_url,title,nid):
    sql = "insert into notecontent values(%s,'%s','cac','','%s','%s',0)" % (nid,title,image_url,article_url)

    @mysql(sql)
    def insert(results=''):
        return results
    return 0


def note_response(nid):
    sql = "insert into noteresponse values(%s,0,0,'','',0)" % nid

    @mysql(sql)
    def insert(results=''):
        return results
    return 0


def send(_title,article_url,stu_list):
    for i in stu_list:
        openid = get_openid(i)
        result = send_common_template_msg(article_url, title = _title, touser = openid)
        if result.get['errcode'] != 0:
            pass
    return 0

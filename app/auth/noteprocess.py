# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import logging
from urllib import quote

from ..lib.database import mysql
from ..weixin.template import send_common_template_msg
from ..nova.get_user_info import get_openid



def note_index(stu_list, nid):
    stu_text = ''
    for i in stu_list:
        stu_text = stu_text+i
    sql = "insert into noteindex values(%s,%s,0,'','%s',0)" % (nid, nid, stu_text)

    @mysql(sql)
    def insert(results=''):
        return results

    result = insert()
    return 0


def note_content(article_url, image_url, title, nid):
    sql = "insert into notecontent values(%s,'%s','cac','','%s','%s',0)" % (nid, title, image_url, article_url)

    @mysql(sql)
    def insert(results=''):
        return results
    result = insert()
    return 0


def note_response(nid):
    sql = "insert into noteresponse values(%s,0,0,'','',0)" % nid

    @mysql(sql)
    def insert(results=''):
        return results

    result = insert()
    return 0


def send(_title, article_url, stu_list):
    url = quote(article_url)
    post_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
        'appid=wx92a9c338a5d02f38&redirect_uri=http://121.42.216.141/code/' \
        '%s&response_type=code&scope=snsapi_base&state=123#wechat_redirect' % url
    cnt = 0
    for i in stu_list:
        openid = get_openid(i)
        if openid != -1:
            openid = openid.encode('utf8')
        result = send_common_template_msg(post_url, title=_title, touser=openid)
        if result.get('errcode') != 0:
            logging.basicConfig(format='%(asctime)s %(levelname)s%(message)s', \
                                datefmt='%Y/%m/%d %I:%M:%S %p', \
                                filename='./log/sendmsg.log', \
                                level=logging.DEBUG)
            logging.warning("sending template msg error --send() noteprocess.py:"+str(result))
            cnt = cnt+1
    if 0<cnt<len(stu_list):
        return -2
    elif cnt == len(stu_list):
        return -1
    else:
        return 0

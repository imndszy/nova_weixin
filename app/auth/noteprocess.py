# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from nova_weixin.packages.novalog import NovaLog
from nova_weixin.packages.novamysql import insert

# from nova_weixin.app.lib.database import mysql
from nova_weixin.packages.nova_wxsdk import send_common_template_msg
from nova_weixin.app.nova.get_user_info import get_openid
from nova_weixin.app.weixin.weixinconfig import APP_ID
from nova_weixin.app.config import ADDRESS
from nova_weixin.packages.nova_wxsdk import WxApiUrl


log = NovaLog(path='log/db_operation.log')
send_log = NovaLog(path='log/runtime.log')

def note_index(stu_list, nid):
    stu_text = ''
    for i in stu_list:
        stu_text = stu_text + i
    result = insert('noteindex', nid=nid, publishTime=nid, sort=0, topic='', stuids=stu_text, expire=0)
    # sql = "insert into noteindex "\
    #       "values(%s,%s,0,'','%s',0)" % (nid, nid, stu_text)
    #
    # @mysql(sql)
    # def insert(results=''):
    #     return results
    #
    # insert()
    if result == 1:
        return 0
    else:
        log.warn("insert into database error -- note_index")
        return -1


def note_content(arti_url, image_url, title, nid):
    # temp_tuple = (nid, title, image_url, arti_url)
    result = insert('notecontent', nid=nid, title=title, publisher='cac', detail='', picurl=image_url, url=arti_url, tid=0)
    # sql = "insert into notecontent "\
    #       "values(%s,'%s','cac','','%s','%s',0)" % temp_tuple
    #
    # @mysql(sql)
    # def insert(results=''):
    #     return results
    # insert()
    if result == 1:
        return 0
    else:
        log.warn("insert into database error -- note_content")
        return -1


def note_response(nid):
    result = insert('noteresponse',nid=nid, earlistread=0, latestread=0, readlist='', readtime='', readpop=0)
    # sql = "insert into noteresponse values(%s,0,0,'','',0)" % nid
    #
    # @mysql(sql)
    # def insert(results=''):
    #     return results
    #
    # insert()
    if result == 1:
        return 0
    else:
        log.warn("insert into database error -- note_response")
        return -1


def send(_title, nid, stu_list):

    url = ADDRESS + '/code/' + str(nid)
    post_url = WxApiUrl.oauth2_new_page.format(appid=APP_ID, redirect_url=url)
    # post_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
    #     'appid=%s&redirect_uri=%s' \
    #     '&response_type=code&scope=snsapi_base&state=123'\
    #     '#wechat_redirect' % (APP_ID, url)
    cnt = 0
    for i in stu_list:
        openid = get_openid(i)
        if openid:
            openid = openid.encode('utf8')
        result = send_common_template_msg(post_url, title=_title,
                                          touser=openid)
        if result.get('errcode') != 0:
            cnt = cnt + 1
            send_log.warn('send msg error {stuid}, errmsg: {errmsg}'.format(stuid=str(i), errmsg=result.get('errmsg')))
#说明部分人发送成功
    if 0 < cnt < len(stu_list):
        return -2
#说明一个都没发送成功
    elif cnt == len(stu_list):
        return -1
    else:
        return 0

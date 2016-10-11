# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import logging

from nova_weixin.app.lib.database import mysql
from nova_weixin.app.weixin.template import send_common_template_msg
from nova_weixin.app.nova.get_user_info import get_openid
from nova_weixin.app.config import ADDRESS
from nova_weixin.app.weixin.weixinconfig import APP_ID


def note_index(stu_list, nid):
    stu_text = ''
    for i in stu_list:
        stu_text = stu_text + i
    sql = "insert into noteindex "\
          "values(%s,%s,0,'','%s',0)" % (nid, nid, stu_text)

    @mysql(sql)
    def insert(results=''):
        return results

    insert()
    return 0


def note_content(arti_url, image_url, title, nid):
    temp_tuple = (nid, title, image_url, arti_url)
    sql = "insert into notecontent "\
          "values(%s,'%s','cac','','%s','%s',0)" % temp_tuple

    @mysql(sql)
    def insert(results=''):
        return results
    insert()
    return 0


def note_response(nid):
    sql = "insert into noteresponse values(%s,0,0,'','',0)" % nid

    @mysql(sql)
    def insert(results=''):
        return results

    insert()
    return 0


def send(_title, arti_url, stu_list):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d]'
                               '%(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='./log/sendmsg.log',
                        filemode='w')
    arti_url = arti_url.replace('?', '$').replace('#', '@').replace('&', '!')
    url = ADDRESS + '/code/' + arti_url
    post_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
        'appid=%s&redirect_uri=%s' \
        '&response_type=code&scope=snsapi_base&state=123'\
        '#wechat_redirect' % (APP_ID, url)
    cnt = 0
    for i in stu_list:
        openid = get_openid(i)
        if openid != -1:
            openid = openid.encode('utf8')
        result = send_common_template_msg(post_url, title=_title,
                                          touser=openid)
        logging.warning("sending template msg error --send()"
                        "noteprocess.py:" + str(result))
        if result.get('errcode') != 0:
            logging.warning("sending template msg error --send()"
                            " noteprocess.py:" + str(result))
            cnt = cnt + 1
#说明部分人发送成功
    if 0 < cnt < len(stu_list):
        return -2
#说明一个都发送成功
    elif cnt == len(stu_list):
        return -1
    else:
        return 0

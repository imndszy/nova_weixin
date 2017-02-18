# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import sys
import threading
from nova_weixin.packages.novalog import NovaLog
from nova_weixin.packages.nova_wxsdk import WxApiUrl, send_common_template_msg, get_token
from nova_weixin.app.nova.get_user_info import  get_all_users
from nova_weixin.app.weixin.weixinconfig import APP_ID, SECRET, TEMPLATE_ID
from nova_weixin.app.config import ADDRESS

PY2 = sys.version_info[0] == 2
send_log = NovaLog(path='log/runtime.log')


class SendTemplateMsg(threading.Thread):

    error_cnt = 0
    send_lock = threading.Lock()

    def __init__(self, nid, title, stuid, openid, token):
        threading.Thread.__init__(self)
        self.nid = nid
        if PY2:
            self.title = title
        else:
            self.title = title.decode('utf8')
        self.stuid = stuid
        self.openid = openid
        self.token = token

    def run(self):
        result = send_common_template_msg(self.__get_url(), title=self.title, template_id=TEMPLATE_ID,
                                          touser=self.openid ,acc_token=self.token)
        if result.get('errcode') != 0:
            SendTemplateMsg.send_lock.acquire()
            SendTemplateMsg.error_cnt += 1
            send_log.warn('send msg error {stuid}, errmsg: {errmsg}'.format(stuid=str(self.stuid)+str(self.openid), errmsg=result.get('errmsg')))
            SendTemplateMsg.send_lock.release()

    def __get_url(self):
        url = ADDRESS + '/code/' + str(self.nid)
        return WxApiUrl.oauth2_new_page.format(appid=APP_ID, redirect_url=url)


def send(_title, nid, stu_list):
    users = get_all_users()
    acc_token = get_token(appid=APP_ID, appsecret=SECRET)

    if acc_token['status'] == -1:
        return -1

    openids = []
    error_openid = 0
    for i in users:
        if str(i['stuid']) in stu_list:
            if i['openid']:
                if PY2:
                    openids.append({'stuid': i['stuid'], 'openid': i['openid'].encode('utf8')})
                else:
                    openids.append({'stuid': i['stuid'], 'openid': i['openid']})
            else:
                error_openid += 1
                send_log.warn('send msg error {stuid}, errmsg: can not get openid'.format(stuid=i['stuid']))

    threads = []
    for stu in openids:
        post = SendTemplateMsg(nid, _title, stu['stuid'], stu['openid'], acc_token['acc_token'])
        threads.append(post)
        post.start()

    for thread in threads:
        thread.join()

#说明部分人发送成功
    if 0 < SendTemplateMsg.error_cnt + error_openid <= len(stu_list):
        return -1
    else:
        return 0
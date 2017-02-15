# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
import os

from . import WxApiUrl, CommunicateWithApi
from nova_weixin.packages.novalog import NovaLog

log = NovaLog('log/runtime.log')

def get_token(appid=None, appsecret=None):
    data = os.getenv('nova_acc_token', '')

    if data:
        past_time = int(data[0:10])
        acc_token = data[10:]
    else:
        past_time = 1400000000
    now_time = int(time.time())
    if now_time - past_time > 1000:
        url = WxApiUrl.token.format(appid=appid, appsecret=appsecret)

        result = CommunicateWithApi.get_data(url)

        if result.get('errcode'):
            log.warn("get access token error with errmsg:{errmsg}".format(errmsg=result.get('errmsg')))
            return -1
        else:
            acc_token = result.get('access_token')
            env_string = str(int(time.time())) + acc_token
            os.environ['nova_acc_token'] = env_string
            return acc_token

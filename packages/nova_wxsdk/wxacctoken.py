# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
import os

from . import WxApiUrl, CommunicateWithApi

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
            return {'status': -1, 'errmsg': result.get('errmsg'), 'errcode': result.get('errcode')}
        else:
            acc_token = result.get('access_token')
            env_string = str(int(time.time())) + acc_token
            os.environ['nova_acc_token'] = env_string
            return {'status': 1, 'acc_token': acc_token}
    else:
        return {'status': 1, 'acc_token': acc_token}

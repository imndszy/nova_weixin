# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
import requests
import os

from nova_weixin.app.weixin.weixinconfig import APP_ID, SECRET

def get_token():
    data = os.getenv('nova_acc_token', '')
    # with open(basedir + '/acc_token') as f:
    #     data = f.read()
    if data:
        past_time = int(data[0:10])
        acc_token = data[10:]
    else:
        past_time = 1400000000
    now_time = int(time.time())
    if now_time - past_time > 1000:
        app_id = APP_ID
        app_secret = SECRET
        url = 'https://api.weixin.qq.com/cgi-bin/'\
              'token?grant_type=client_credential&appid=%s&secret=%s' % \
              (app_id, app_secret)
        result = requests.get(url).json()

        if result.get('errcode'):
            return -1
        else:
            acc_token = result.get('access_token')
            env_string = str(int(time.time())) + acc_token
            os.environ['nova_acc_token'] = env_string
            # with open(basedir + '/acc_token', 'w') as f:
            #     f.write(string)
            return acc_token

if __name__ == '__main__':
    print(get_token())
    print(os.getenv('nova_acc_token'))
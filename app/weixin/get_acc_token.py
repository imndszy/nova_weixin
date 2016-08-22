# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
import urllib2
import json
import os
import logging
from weixinconfig import APP_ID,SECRET

basedir = os.path.abspath(os.path.dirname(__file__))


def get_token():
    with open(basedir+'/acc_token') as f:
        data = f.read()
    if data:
        past_time = int(data[0:10])
        acc_token = data[10:]
    else:
        past_time = 1400000000
    now_time = int(time.time())
    if now_time-past_time > 1000:
        app_id = APP_ID
        app_secret = SECRET
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % \
              (app_id, app_secret)
        result = urllib2.urlopen(url).read()
        if json.loads(result).get('errcode'):
            logging.basicConfig(format='%(asctime)s %(message)s', \
                                datefmt='%Y/%m/%d %I:%M:%S %p', \
                                filename='./log/acc_token.log', \
                                level=logging.DEBUG)
            logging.debug("fail to get acc_token --get_acc_token.py")
            acc_token = "fail to get acc_token --get_acc_token.py"

        else:
            acc_token = json.loads(result).get('access_token')
            string = str(int(time.time()))+acc_token
            with open(basedir+'/acc_token', 'w') as f:
                f.write(string)
    return acc_token

if __name__ == "__main__":
    #get_token()
    print "test"






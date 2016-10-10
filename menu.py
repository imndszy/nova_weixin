# -*- coding:utf8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json
import requests
import logging

from nova_weixin.app.weixin.get_acc_token import get_token
from nova_weixin.app.weixin.weixinconfig import MENU


def create_menu():
    acc_token = get_token()
    if acc_token:
        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % acc_token
        data = MENU
        request = requests.post(url, json.dumps(data, ensure_ascii=False))
        return request.text
    else:
        return "failed to get access_token!--menu.py"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='./log/menu.log',
                        filemode='w')
    logging.info('执行菜单更新操作'+str(create_menu()))

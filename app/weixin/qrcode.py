# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json
import urllib
import urllib2
import logging
import get_acc_token


def create_ticket(action_name, scene_id, expire_seconds=604800):
    acc_token = get_acc_token.get_token()
    if acc_token:
        url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % acc_token
        if action_name == "QR_SCENE":
            data = {
                "expire_seconds": expire_seconds,
                "action_name": "QR_SCENE",
                "action_info":
                    {
                        "scene": {"scene_id": scene_id}
                    }
            }
        elif action_name == "QR_LIMIT_STR_SCENE":
            data = {
                "action_name": "QR_LIMIT_SCENE",
                "action_info":
                    {
                        "scene": {"scene_id": scene_id}
                    }
            }
        request = urllib2.urlopen(url, json.dumps(data, ensure_ascii=False)).read()
        result = json.loads(request)
        if result.get('errcode'):
            logging.basicConfig(format='%(asctime)s %(message)s', \
                                datefmt='%Y/%m/%d %I:%M:%S %p', \
                                filename='./log/qrcode.log', \
                                level=logging.DEBUG)
            logging.warning("failed to get ticket -- qrcode.py")
            return ''
        else:
            return result.get('ticket')
    else:
        logging.basicConfig(format='%(asctime)s %(message)s', \
                            datefmt='%Y/%m/%d %I:%M:%S %p', \
                            filename='./log/acc_token.log', \
                            level=logging.DEBUG)
        logging.warning("failed to get acc_token -- qrcode.py--create_ticket()")
        return ''


def get_qrcode_url(ticket):
    if ticket:
        tic = 'ticket'
        dic = {tic:ticket}
        parameter = urllib.urlencode(dic)
        url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?%s" % parameter
        return url
    else:
        logging.basicConfig(format='%(asctime)s %(message)s', \
                            datefmt='%Y/%m/%d %I:%M:%S %p', \
                            filename='./log/qrcode.log', \
                            level=logging.DEBUG)
        logging.warning("invalid ticket,--get_qrcode_url() qrcode.py")

if __name__ == "__main__":
    ticket = create_ticket("QR_SCENE")
    get_qrcode_url(ticket)




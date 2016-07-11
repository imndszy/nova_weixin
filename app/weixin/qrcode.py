# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json
import urllib
import urllib2
import get_acc_token


def create_ticket(action_name, expire_seconds=604800):
    acc_token = get_acc_token.get_token()
    if acc_token:
        url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % acc_token
        if action_name == "QR_SCENE":
            data = {
                "expire_seconds": expire_seconds,
                "action_name": "QR_SCENE",
                "action_info":
                    {
                        "scene": {"scene_id": 1}
                    }
            }
        elif action_name == "QR_LIMIT_STR_SCENE":
            data = {
                "action_name": "QR_LIMIT_SCENE",
                "action_info":
                    {
                        "scene": {"scene_id": 123}
                    }
            }
        request = urllib2.urlopen(url, json.dumps(data, ensure_ascii=False)).read()
        result = json.loads(request)
        if result.get('errcode'):
            print 'failed to get ticket -- qrcode.py'    #log here
            return ''
        else:
            return result.get('ticket')
    else:
        print "failed to get acc_token -- qrcode.py--create_ticket()"      #log here
        return ''


def get_qrcode_url(ticket):
    if ticket:
        tic = 'ticket'
        dic = {tic:ticket}
        parameter = urllib.urlencode(dic)
        url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?%s" % parameter
        return url
    else:
        print "invalid ticket,check the log"

if __name__ == "__main__":
    ticket = create_ticket("QR_SCENE")
    get_qrcode_url(ticket)




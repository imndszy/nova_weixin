# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json
import urllib2
import get_acc_token


def send_customer_service_message_txt(touser='o19fSvhseI04YpNJkVYVIBTEjESs', content='你好！'):
    acc_token = get_acc_token.get_token()
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % acc_token
    txt = {
            "touser": "%s" % touser,
            "msgtype": "text",
            "text":
            {
                    "content": "%s" % content
            }
    }
    request = urllib2.urlopen(url, json.dumps(txt, ensure_ascii=False))
    return json.loads(request.read())

if __name__ == "__main__":
    print send_customer_service_message_txt()
    print 'OK!'

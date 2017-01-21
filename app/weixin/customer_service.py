# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json

from nova_weixin.app.weixin.get_acc_token import get_token
from nova_weixin.packages.nova_wxsdk import WxApiUrl, CommunicateWithApi


def send_customer_service_message_txt(touser,
                                      content='你好！'):
    acc_token = get_token()
    url = WxApiUrl.send_msg.format(access_token=acc_token)
    txt = {
            "touser": "%s" % touser,
            "msgtype": "text",
            "text":
            {
                "content": "%s" % content
            }
    }
    return CommunicateWithApi.post_data(url, json.dumps(txt, ensure_ascii=False).encode('utf8'))

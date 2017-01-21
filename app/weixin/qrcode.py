# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json

from nova_weixin.app.weixin.get_acc_token import get_token
from nova_weixin.packages.nova_wxsdk import WxApiUrl, CommunicateWithApi

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

def create_ticket(action_name, scene_id=0, expire_seconds=604800):
    acc_token = get_token()
    if acc_token:
        url = WxApiUrl.create_qrcode.format(access_token=acc_token)
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
        result = CommunicateWithApi.post_data(url, json.dumps(data, ensure_ascii=False).encode('utf8'))
        if result.get('errcode'):
            return ''
        else:
            return result.get('ticket')
    else:
        return ''


def get_qrcode_url(ticket):
    tic = 'ticket'
    dic = {tic: ticket}
    parameter = urlencode(dic)
    return "https://mp.weixin.qq.com/cgi-bin/showqrcode?%s" % parameter


if __name__ == "__main__":
    ticket = create_ticket("QR_SCENE")
    print(ticket)
    print(get_qrcode_url(ticket))

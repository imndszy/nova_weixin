# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json

from . import WxApiUrl, CommunicateWithApi
from nova_weixin.packages.novalog import NovaLog

log = NovaLog('log/runtime.log')

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

def create_ticket(action_name, acc_token, scene_id=0, expire_seconds=604800):
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
            return {'status': -1, 'errcode': result.get('errcode'), 'errmsg': result.get('errmsg')}
        else:
            return {'status': 1, 'ticket': result.get('ticket')}
    else:
        return {'status': -1, 'errcode': 100000, 'errmsg': 'acc_token is none'}


def get_qrcode_url(ticket):
    tic = 'ticket'
    dic = {tic: ticket.get('ticket')}
    parameter = urlencode(dic)
    return "https://mp.weixin.qq.com/cgi-bin/showqrcode?%s" % parameter


if __name__ == "__main__":
    ticket = create_ticket("QR_SCENE", acc_token=-1)
    print(ticket)
    print(get_qrcode_url(ticket))

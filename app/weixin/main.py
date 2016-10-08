# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import hashlib
import xml.etree.ElementTree as ET
from flask import request, make_response, redirect,render_template

from nova_weixin.app.weixin import weixin
from nova_weixin.app.weixin.weixinconfig import TOKEN


@weixin.route('/', methods=['GET'])
def wechat_auth():
    echostr = request.args.get('echostr', '')
    if verification():
        return make_response(echostr)
    return render_template("index.html")


@weixin.route('/', methods=['POST'])
def wechat_msg():
    rec = request.data
    msg = parse(rec)
    # from msg_handler import MsgHandler
    # message = MsgHandler(msg)
    if msg['MsgType'] == 'event':
        from msg_handler import handle_event
        content = handle_event(msg)
        return res_text_msg(msg,content)


@weixin.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@weixin.route('/code/<path:message_url>', methods=['GET', 'POST'])
def oauth(message_url):
    """
    这个函数用于获取微信公众号的文章链接并跳转
    :param message_url:公众号文章链接
    :return:跳转至相应链接
    """
    from urllib import unquote
    post_url = unquote(str(message_url))
    code = request.args.get('code', '')
    if not code:
        return post_url
    else:
        from weixin.oauth_handler import get_openid
        openid = get_openid(code)
        from weixin.oauth_handler import openid_handler
        openid_handler(openid, post_url)
        return redirect(post_url)


def verification():
    """
    verify the weixin token
    """
    token = TOKEN
    data = request.args
    signature = data.get('signature', '')
    timestamp = data.get('timestamp', '')
    nonce = data.get('nonce', '')
    s = [timestamp, nonce, token]
    s.sort()
    s = ''.join(s)
    if hashlib.sha1(s).hexdigest() == signature:
        return 1
    return 0


def parse(rec):
    """
    :param rec: rec is a xml file
    :return: return a dictionary
    """
    root = ET.fromstring(rec)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

text_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"

def res_text_msg(msg, content):
    response = make_response(text_rep % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())), content))
    response.content_type='application/xml'
    return response
# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
import hashlib
import xml.etree.ElementTree as ET
from flask import request, make_response, redirect, render_template, session,jsonify

from nova_weixin.app.weixin import weixin
from nova_weixin.app.weixin.weixinconfig import TOKEN
from nova_weixin.app.weixin.oauth_handler import (jiaowu,get_openid_from_code,
                                                  jiaowu_save,history_articles)
from nova_weixin.app.nova.get_user_info import get_stuid,get_stu_name


@weixin.route('/', methods=['GET'])
def wechat_auth():
    echostr = request.args.get('echostr', '')
    if verification():
        return make_response(echostr)
    return render_template("index.html")


@weixin.route('/', methods=['POST'])
def wechat_msg():
    rec = request.data
    if rec:
        msg = parse(rec)
    # from msg_handler import MsgHandler
    # message = MsgHandler(msg)
        if msg['MsgType'] == 'event':
            if msg['Event'] == 'CLICK' and  msg['EventKey'] == 'not_read_msg':
                from msg_handler import handle_mes_key
                handle_mes_key(msg)
            from msg_handler import handle_event
            content = handle_event(msg)
            return res_text_msg(msg, content)


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
    post_url = str(message_url).replace(':/', '://')
    post_url = post_url.replace('$', '?').replace('@', '#').replace('!', '&')
    code = request.args.get('code', '')
    if not code:
        return redirect(post_url)
    else:
        openid = get_openid_from_code(code)
        try:
            from nova_weixin.app.weixin.oauth_handler import openid_handler
            openid_handler(openid, post_url)
        except:
            pass
        finally:
            return redirect(post_url)

@weixin.route('/history', methods=['GET', 'POST'])
def oauth_history():
    code = request.args.get('code', '')
    if not code:
        return redirect('')
    openid = get_openid_from_code(code)
    session['openid'] = openid
    stuid = get_stuid(openid)
    session['stuid'] = stuid
    session['name'] = get_stu_name(stuid).encode('utf8')
    session['history_checked'] = 'history'
    return render_template('note.html')


@weixin.route('/handle_history')
def handle_history():
    if session.get('history_checked'):
        page = int(request.args.get('page'))
        if not page:
            return redirect('')
        result = history_articles(session['stuid'])
        article_list = []
        for i in result:
            if len(i):
                article_list.append({'title':i[1].encode('utf8'),'url':i[2].encode('utf8')})
        article_list.reverse()
        if len(article_list)-page*8>8:
            result = {'result':article_list[(page-1)*8:8*page],'name':session['name']}
        else:
            result = {'result':article_list[(page-1)*8:],'name':session['name']}
    return jsonify(result)

@weixin.route('/jiaowu')
def oauth_jiaowu():
    code = request.args.get('code', '')
    if not code:
        return redirect('')
    if not session.get('jiaowu', ''):
        openid = get_openid_from_code(code)
        session['openid'] = openid
        result = jiaowu(openid)
        if result == -1:
            return '您尚未绑定学号！'
        if result:
            session['email'] = result[0]
            session['status'] = result[1]
            session['stuid'] = result[2]
            session['jiaowu'] = 'jiaowu'
    return render_template('jiaowu.html')


@weixin.route('/handle_jiaowu',methods=['GET','POST'])
def handle_jiaowu():
    if session['jiaowu'] == 'jiaowu' and request.values.get('num') == '2':
        da = request.values
        session['email'] = da.get('email').encode('utf8')
        session['status'] = int(da.get('status').encode('utf8'))
        jiaowu_save(session['stuid'],session['email'],session['status'])
        return jsonify(result='ok')
    if request.args.get('num') == '1' and session['jiaowu'] == 'jiaowu':
        return jsonify(result='ok',
                       email=session['email'],
                       status=str(session['status']))
    return 'ok'


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
    response = make_response(text_rep % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), content))
    response.content_type = 'application/xml'
    return response

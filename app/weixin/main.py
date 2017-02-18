# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import hashlib
import xml.etree.ElementTree as ET
from flask import request, make_response, redirect, render_template, session,jsonify

from nova_weixin.app.weixin import weixin
from nova_weixin.app.weixin.weixinconfig import TOKEN
from nova_weixin.app.weixin.oauth_handler import (jiaowu,get_openid_from_code,
                                                  get_url,
                                                  jiaowu_save,history_articles)
from nova_weixin.app.nova.get_user_info import get_stu_name
from nova_weixin.app.weixin.msg_handler import handle_msg
from nova_weixin.app.config import PY2


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
        return handle_msg(msg)


@weixin.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@weixin.route('/code/<int:nid>', methods=['GET', 'POST'])
def oauth(nid):
    """
    这个函数用于获取微信公众号的文章编号并跳转
    :param nid:公众号文章编号
    :return:跳转至相应链接
    """
    # post_url = str(message_url).replace(':/', '://')
    # post_url = post_url.replace('$', '?').replace('@', '#').replace('!', '&')
    code = request.args.get('code', '')
    if not code:
        return redirect('/')
    else:
        url = get_url(nid)
        openid = get_openid_from_code(code)
        try:
            from nova_weixin.app.weixin.oauth_handler import openid_handler
            openid_handler(openid, nid)
        except:
            pass
        finally:
            return redirect(url)


@weixin.route('/history', methods=['GET', 'POST'])
def oauth_history():
    code = request.args.get('code', '')
    if not code:
        return redirect('')
    openid = get_openid_from_code(code)
    session['openid'] = openid
    if PY2:
        session['name'] = get_stu_name(openid=openid, first=False).encode('utf8')
    else:
        session['name'] = get_stu_name(openid=openid, first=False)
    session['history_checked'] = 'history'
    return render_template('note.html')


@weixin.route('/handle_history')
def handle_history():
    if session.get('history_checked'): # 确认是否从history路由跳转过来
        page = int(request.args.get('page'))
        if not page:
            return redirect('')
        result = history_articles(session['stuid'])
        article_list = []
        for i in result:
            if len(i):
                if PY2:
                    article_list.append({'title':i[1].encode('utf8'),'url':i[2].encode('utf8')})
                else:
                    article_list.append({'title': i[1], 'url': i[2]})
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
            session['email'] = result['email']
            session['status'] = result['status']
            session['stuid'] = result['stuid']
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
    if hashlib.sha1(s.encode('utf8')).hexdigest() == signature:
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

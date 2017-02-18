# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask import (render_template, redirect, url_for, flash, session)

from nova_weixin.app.bind.forms import BindForm, ReBindForm
from nova_weixin.app.bind import bind
from nova_weixin.app.bind.bind_database import (verify_password,
                                                save_new_student)
from nova_weixin.packages.nova_wxsdk import create_ticket, get_qrcode_url, get_token
from nova_weixin.app.weixin.weixinconfig import APP_ID, SECRET
from nova_weixin.app.nova.get_user_info import get_openid


@bind.route('/register', methods=['GET', 'POST'])
def register():
    form = BindForm()
    if form.validate_on_submit():
        stuid = form.stuid.data.encode('utf8')
        passwd = form.certification.data.encode('utf8')
        session['stuid'] = stuid
        session['passwd'] = passwd
        verify_status = verify_password(stuid, passwd)
        if verify_status and verify_status != -1:
            session['register'] = True
            query_result = get_openid(stuid)
            if query_result:                                      #该学号已经绑定微信号
                openid = query_result.encode('utf8')
                session['openid'] = openid
                return redirect(url_for('bind.rebind'))
            else:
                if save_new_student(stuid) == -1:
                    return "注册失败，请联系管理员！"
                return redirect(url_for('bind.get_qrcode'))
        elif verify_status == -1:
            return render_template('404.html')
        else:
            flash('Invalid Student ID or Password.')
    return render_template('bind/register.html', form=form)


@bind.route('/qrcode', methods=['GET', 'POST'])
def get_qrcode():
    if session.get('register'):
        acc_token = get_token(appid=APP_ID, appsecret=SECRET)
        ticket = create_ticket("QR_SCENE", acc_token=acc_token.get('acc_token'), scene_id=int(session['stuid']))
        url = get_qrcode_url(ticket)
        return redirect(url)
    return render_template('404.html')


@bind.route('/rebind', methods=['GET', 'POST'])
def rebind():
    if session.get('register') and session.get('openid'):
        form = ReBindForm()
        if form.validate_on_submit():
            coverage = form.coverage.data
            if coverage == 'yes':
                acc_token = get_token(appid=APP_ID, appsecret=SECRET)
                ticket = create_ticket("QR_SCENE", acc_token=acc_token.get('acc_token'), scene_id=int(session['stuid']))
                url = get_qrcode_url(ticket['ticket'])
                return redirect(url)
            else:
                return redirect(url_for('main.index'))
        return render_template('bind/rebind.html', form=form)
    return render_template('404.html')

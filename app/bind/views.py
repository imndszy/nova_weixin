# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from . import bind
from flask import (render_template, redirect, request, url_for, flash, session)
from forms import BindForm
from bind_database import get_bind_info,verify_password
from app.weixin.qrcode import create_ticket,get_qrcode_url

@bind.route('/register',methods=['GET','POST'])
def register():
    form = BindForm()
    if form.validate_on_submit():
        stuid = form.stuid.data.encode('utf8')
        print stuid,type(stuid)
        passwd = form.certification.data.encode('utf8')
        print passwd,type(passwd)
        session['stuid'] = stuid
        session['passwd'] = passwd
        if (verify_password(stuid,passwd)):
            query_result = get_bind_info(stuid,passwd)
            if(query_result):                                      #该学号已经绑定微信号
                openid = query_result
                session['openid'] = openid
            else:
                session['register'] = True
                return redirect(url_for('bind.get_qrcode'))
        else:
            flash('Invalid Student ID or Password.')
    return render_template('bind/register.html',form=form)

@bind.route('/qrcode',methods=['GET','POST'])
def get_qrcode():
    if(session['register']):
        ticket = create_ticket("QR_SCENE")
        url = get_qrcode_url(ticket)
        flash("请扫描以下二维码完成关注！")
        return redirect(url)
    return render_template('404.html')

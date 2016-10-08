# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
from flask import (render_template, redirect, request, url_for, flash, session)

from nova_weixin.app.auth import auth
from nova_weixin.app.auth.forms import LoginForm,ArticleForm
from nova_weixin.app.auth.get_users import classes, stu
from nova_weixin.app.auth.noteprocess import note_index, note_content, note_response, send
from nova_weixin.app.config import USER_EMAIL,USER_PASSWD


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == USER_EMAIL and form.password.data == USER_PASSWD:
            session['login'] = True
            return redirect(request.args.get('next') or url_for('auth.article'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/article', methods=['GET', 'POST'])
def article():
    if session.get('login'):
        form = ArticleForm()
        if form.validate_on_submit():
            article_url = form.url.data
            image_url = form.image_url.data
            title = form.title.data
            session['article_url'] = article_url
            session['image_url'] = image_url
            session['title'] = title
            class_dict_all = classes()
            session['class_dict'] = class_dict_all
            if class_dict_all == -1:
                return render_template('auth/fail.html')
            #create_class_html(class_dict_all)
            return redirect(request.args.get('next') or url_for('auth.choose_class'))
        return render_template('auth/article.html', form=form)
    return redirect(url_for('auth.login'))


@auth.route('/choose_class', methods=['GET', 'POST'])
def choose_class():
    if session.get('login'):
        class_dict_all = session['class_dict']
        if request.method == 'POST':
            class_list = request.form.getlist('checked')
            # class_dict_all = classes()
            if 'choose_all' in class_list:
                class_list = [i for i in class_dict_all.keys() if i not in class_list]
            session['classes'] = class_list
            stu_dict_all = stu(class_list)
            session['stu_dict'] = stu_dict_all
            #create_stu_html(stu_dict_all, class_dict_all)
            return redirect(url_for('auth.choose_stu'))
        return render_template('auth/class1.html',class_dict = class_dict_all)
    return redirect(url_for('auth.login'))


@auth.route('/choose_stu', methods=['GET', 'POST'])
def choose_stu():
    if session.get('login'):
        if session.get('classes'):
            article_url = session['article_url'].encode('utf8')
            image_url = session['image_url'].encode('utf8')
            title = session['title'].encode('utf8')
            stu_dict_all = session['stu_dict']
            if request.method == 'POST':
                stu_list = request.form.getlist('checked')
                class_list = session['classes']
                chosen_class_stu = []
                for m in stu(class_list).values():
                    for n in m:
                        chosen_class_stu.append(str(n[0]))
                if 'choose_stu_all' in stu_list:
                    stu_list = [i for i in chosen_class_stu if i not in stu_list]
                nid = int(time.time())
                note_index(stu_list, nid)
                note_content(article_url, image_url, title, nid)
                note_response(nid)
                if send(title, article_url, stu_list) == -1:
                    return render_template('auth/fail.html')
                session['finish'] = 'finished'
                return redirect(url_for('auth.finish'))
            return render_template('auth/stu1.html',stu_dict = stu_dict_all,class_dict = session['class_dict'])
        return redirect(url_for('auth.article'))
    return redirect(url_for('auth.login'))


@auth.route('/finish', methods=['GET', 'POST'])
def finish():
    if session.get('login'):
        if session.get('finish') == 'finished':
            return render_template('auth/finish.html')
        return redirect(url_for('auth.article'))
    return redirect(url_for('login'))


@auth.route('/logout')
def logout():
    if session.get('login'):
        session.pop('login')
        session.pop('classes')
        session.pop('stu_dict')
        flash('You have been logged out.')
        return redirect(url_for('main.index'))
    return redirect(url_for('login'))


# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         if form.username.data == ROOT_USER:
#             user = User(email=form.email.data,
#                         username=form.username.data,
#                         password=form.password.data)
#             db.session.add(user)
#             flash('You can now login.')
#             return redirect(url_for('auth.login'))
#         else:
#             flash('Must be Novaer!')
#             return redirect(url_for('main.wrong'))
#     return render_template('auth/register.html', form=form)

# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import time
from flask import (render_template, redirect, request,
                   url_for, flash, session, jsonify)

from nova_weixin.app.auth import auth
from nova_weixin.app.auth.forms import LoginForm, ArticleForm
from nova_weixin.app.auth.get_users import classes, stu
from nova_weixin.app.auth.noteprocess import (note_index,
                                              note_content,
                                              note_response,
                                              get_read_info,
                                              get_activity_info)
from nova_weixin.packages.nova_admin import send
from nova_weixin.app.config import USER_EMAIL, USER_PASSWD
from nova_weixin.app.weixin.msg_handler import read_info


@auth.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('auth.article'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == USER_EMAIL and form.password.data == USER_PASSWD:
            session['login'] = True
            return redirect(request.args.get('next') or
                            url_for('auth.article'))
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
            return redirect(request.args.get('next') or
                            url_for('auth.choose_class'))
        return render_template('auth/article.html', form=form)
    return redirect(url_for('auth.login'))


@auth.route('/choose_class', methods=['GET', 'POST'])
def choose_class():
    if session.get('login'):
        class_dict_all = session['class_dict']
        if request.method == 'POST':
            class_list = request.form.getlist('checked')
            if 'choose_all' in class_list:
                class_list = [i for i in class_dict_all.keys()
                              if i not in class_list]
            session['classes'] = class_list
            return redirect(url_for('auth.choose_stu'))
        return render_template('auth/class.html', class_dict=class_dict_all)
    return redirect(url_for('auth.login'))


@auth.route('/choose_stu', methods=['GET', 'POST'])
def choose_stu():
    if session.get('login'):
        if session.get('classes'):
            article_url = session['article_url'].encode('utf8')
            image_url = session['image_url'].encode('utf8')
            title = session['title'].encode('utf8')
            stu_dict_all = stu(session['classes'])
            if request.method == 'POST': # 确定被选择的学生
                stu_list = request.form.getlist('checked')

                class_list = session['classes']
                chosen_class_stu = []  # 获取除全选外选中班级的所有学生
                for m in stu(class_list).values():
                    for n in m:
                        chosen_class_stu.append(str(n[0]))
                if 'choose_stu_all' in stu_list:
                    stu_list = [i for i in chosen_class_stu
                                if i not in stu_list]
                stu_list = list(set(stu_list))
                nid = int(time.time())
                note_content(article_url, image_url, title, nid)
                note_response(nid)
                result = send(title, nid, stu_list)
                if result['status'] == -1:
                    return render_template('auth/fail.html')
                note_index(result['success_stus'], nid)  # 将收到消息的学生添加到数据库
                session.pop('classes')
                if result['status'] == -2:
                    return render_template('auth/fail.html')

                session['finish'] = 'finished'
                return redirect(url_for('auth.finish'))
            return render_template('auth/stu.html',
                                   stu_dict=stu_dict_all,
                                   class_dict=session['class_dict'])
        return redirect(url_for('auth.article'))
    return redirect(url_for('auth.login'))


@auth.route('/finish', methods=['GET', 'POST'])
def finish():
    if session.get('login'):
        if session.get('finish') == 'finished':
            return render_template('auth/finish.html')
        return redirect(url_for('auth.article'))
    return redirect(url_for('auth.login'))


@auth.route('/view')
def view_read():
    if session.get('login'):
        return render_template('auth/nova.html')
    return redirect(url_for('auth.login'))


@auth.route('/view/handler')
def view_handle():
    if session.get('login'):
        data = request.args
        if data.get('quest') == 'activity':
            activities = get_activity_info()
            return jsonify({'status':0, 'activities': activities})
    return redirect(url_for('auth.login'))


@auth.route('/view/readinfo')
def view_read_info():
    if session.get('login'):
        data = request.args
        if data.get('quest') == 'stus':
            if data.get('nid', None):
                 stus = get_read_info(data.get('nid'))
                 return jsonify({'status': 0, 'stus': stus})
            else:
                return jsonify({'status': -1, 'errmsg': '未获取到nid'})
    return redirect(url_for('auth.login'))


@auth.route('/test')
def test():
    return jsonify(get_read_info(nid=213))


@auth.route('/view/stus')
def view_stus():
    if session.get('login'):
        data = request.args
        if data.get('quest') == 'grades':
            return jsonify({'status': 0, 'classes': classes()})
        else:
            return redirect(url_for('auth.index'))
    return redirect(url_for('auth.login'))


@auth.route('/view/stus/class_readinfo')
def handle_classes():
    if session.get('login'):
        data = request.args
        if data.get('quest') == 'classes':
            if data.get('classid'):
                return jsonify(stu([data.get('classid')]))
        else:
            return redirect(url_for('auth.index'))
    return redirect(url_for('auth.login'))


@auth.route('/view/stus/personal')
def handle_person():
    if session.get('login'):
        data = request.args
        if data.get('quest') == 'person' and data.get('stuid'):
            return jsonify(read_info(data.get('stuid')))
        return redirect(url_for('auth.index'))
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    if session.get('login'):
        session.pop('login')
        session.pop('classes') if session.get('classes') else 0
        session.pop('stu_dict') if session.get('stu_dict') else 0
        flash('You have been logged out.')
        return redirect(url_for('main.index'))
    return redirect(url_for('login'))

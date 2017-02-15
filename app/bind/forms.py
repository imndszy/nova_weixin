# -*- coding:utf8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class BindForm(Form):
    stuid = StringField('Student ID', validators=[DataRequired()])
    certification = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ReBindForm(Form):
    coverage = SelectField(u'您已经绑定过该学号至ＮＯＶＡ,确定要重新绑定吗？',
                           choices=[('yes', u'是'), ('no', u'否')],
                           validators=[DataRequired()])
    submit = SubmitField(u'提交')

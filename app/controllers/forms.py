# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField, SubmitField, IntegerField, RadioField
from ..extensions import Many2manyField
from .. models.hero import *
from wtforms.validators import *


class HeroForm(FlaskForm):
    name = StringField(u'名称')
    star = IntegerField(u'星级')
    sex = RadioField(u'性别', choices=[('female', u'女性'), ('male', u'男性')])
    tags = Many2manyField('Tag', model=Tag)
    submit = SubmitField(u'提交')

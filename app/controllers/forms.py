# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField, SubmitField, IntegerField, RadioField, BooleanField
from ..extensions import Many2manyField
from .. models.hero import *
from wtforms.validators import *


class HeroForm(FlaskForm):
    name = StringField(u'名称')
    star = IntegerField(u'星级')
    sex = RadioField(u'性别', choices=[('女性干员', u'女性'), ('男性干员', u'男性')])
    position = RadioField('位置', choices=[('近战位', '近战'), ('远程位', '远程')])
    career = SelectField('职业', coerce=int)
    is_public = BooleanField('公开招募限定')
    experience = RadioField('资历', choices=[('新手', '新手'), ('资深干员', '资深干员'), ('高级资深干员', '高级资深干员')])
    tags = Many2manyField('Tag', model=Tag)
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(HeroForm, self).__init__(*args, **kwargs)
        self.career.choices = [(career.id, career.name) for career in Career.query.all()]

# -*- coding: utf-8 -*-
from .. import db
from .mixin import ModelMixin


class Career(db.Model, ModelMixin):
    __tablename__ = 'career'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return u'career(%s): %s' % (self.id, self.name)

    @staticmethod
    def insert_careers():
        careers = ['狙击干员', '术士干员', '先锋干员', '近卫干员', '重装干员', '医疗干员', '辅助干员', '特种干员']
        for name in careers:
            career = Career(name=name)
            db.session.add(career)
        db.session.commit()


class Tag(db.Model, ModelMixin):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return u'tag(%s): %s' % (self.id, self.name)

    def __str__(self):
        return self.name

    @staticmethod
    def insert_tags():
        tags = ['输出', '防护', '生存', '治疗', '费用回复', '群攻', '减速', '支援', '快速复活', '削弱', '位移', '召唤', '控场', '爆发']
        for name in tags:
            tag = Tag(name=name)
            db.session.add(tag)
        db.session.commit()


HeroTagRel = db.Table(
    'hero_tag_rel',
    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
)


class Hero(db.Model, ModelMixin):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    star = db.Column(db.Integer)
    sex = db.Column(db.String(32))
    position = db.Column(db.String(32))
    is_public = db.Column(db.Boolean, default=True)
    experience = db.Column(db.String)
    career_id = db.Column(db.Integer, db.ForeignKey('career.id'))
    tags = db.relationship(
        'Tag',
        secondary=HeroTagRel,
        backref=db.backref('hero', lazy='joined'),
        lazy='dynamic',
        cascade='all',
    )

    def __repr__(self):
        return u'hero(%s): %s' % (self.id, self.name)

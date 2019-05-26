# -*- coding: utf-8 -*-
from .. import db


class Career(db.Model):
    __tablename__ = 'career'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return u'career(%s): %s' % (self.id, self.name)


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return u'tag(%s): %s' % (self.id, self.name)

HeroTagRel = db.Table(
    'hero_tag_rel',
    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
)


class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    star = db.Column(db.Integer)
    sex = db.Column(db.String(32))
    tags = db.relationship(
        'Tag',
        secondary=HeroTagRel,
        backref=db.backref('hero', lazy='joined'),
        lazy='dynamic',
        cascade='all',
    )

    def __repr__(self):
        return u'hero(%s): %s' % (self.id, self.name)

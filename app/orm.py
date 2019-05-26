# -*- coding: utf-8 -*-
import psycopg2


class Orm(object):

    def __init__(self):
        self.db = None
        self.cr = None

    def init_app(self, app):
        self.db = psycopg2.connect(
            host=app.host,
            database=app.db,
            user=app.db_user,
            password=app.db_password,
        )
        self.cr = self.db.cursor()

    def _execute(self, sql):
        res = None
        try:
            res = self.cr.execute(sql)
        except BaseException as e:
            print(e)
        return res


class Field(object):
    def __init__(self, name, **kwargs):
        self.name = name


class MetaModel(type):
    def __new__(cls, name, bases, attrs):
        if not hasattr(cls, 'tables'):
            cls.tables = []
        if not hasattr(cls, 'fields'):
            cls.fields = {}
        if attrs.get('_table_name') and attrs['_table_name'] not in cls.tables:
            cls.tables.append(attrs['_table_name'])
        for k, v in attrs.items():
            if isinstance(k, Field):
                cls.fields[k] = v
        return type.__new__(cls, name, bases, attrs)


class Model(dict):
    __metaclass__ = MetaModel

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError("{} object has no attribute {}".format(self._name, item))

    def __setattr__(self, key, value):
        self[key] = value


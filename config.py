# -*- coding: utf-8 -*-
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'You Shall Not Pass'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

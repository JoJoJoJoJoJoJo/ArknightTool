# -*- coding: utf-8 -*-
from flask import Blueprint

main = Blueprint('main', __name__)

# Stupid design
from . import views

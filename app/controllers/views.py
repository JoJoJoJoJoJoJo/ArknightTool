# -*- coding: utf-8 -*-
from flask import render_template, redirect
from . import main
from . forms import *


@main.route('/')
def index():
    return 'Hello World'


@main.route('/heros', methods=['POST', 'GET'])
def heros():
    heroForm = HeroForm()
    if heroForm.validate_on_submit():
        name = heroForm.name.data
        star = heroForm.star.data
        sex = heroForm.sex.data
        tags = heroForm.tags.data
        hero = Hero(name=name, star=star, sex=sex)
        hero.tags.extend(tags)
        db.session.add(hero)
        db.session.commit()
        return redirect('/')
    return render_template('hero.html', form=heroForm)


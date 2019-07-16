# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for
from . import main
from . forms import *


@main.route('/')
def index():
    return 'Hello World'


@main.route('/heros')
def heros():
    page = request.args.get('page', 1, type=int)
    pagination = Hero.query.paginate(page, per_page=20, error_out=False).items
    careers = {hero.name: Career.browse(hero.career_id).name for hero in pagination}
    return render_template('heros.html', pagination=pagination, careers=careers)


@main.route('/hero/<id>')
def hero(id):
    hero = Hero.query.filter_by(id=id).first()
    tags = ' '.join(tag.name for tag in hero.tags.all())
    info = {
        'name': hero.name,
        'star': hero.star,
        'career': Career.browse(hero.career_id).name,
        'sex': hero.sex,
        'position': hero.position,
        'is_public': hero.is_public,
        'experience': hero.experience or '无',
    }
    return render_template('hero.html', hero=info, tags=tags)


@main.route('/create', methods=['POST', 'GET'])
def create():
    form = HeroForm()
    if form.validate_on_submit():
        hero = Hero(
            name=form.name.data,
            star=form.star.data,
            sex=form.sex.data,
            position=form.position.data,
            career_id=form.career.data,
            is_public=form.is_public.data,
            experience=form.experience.data,
            tags=form.tags.data,
        )
        db.session.add(hero)
        db.session.commit()
        return redirect(url_for('.hero', id=hero.id))
    return render_template('edit_hero.html', form=form, hero=None)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = HeroForm()
    hero = Hero.query.filter_by(id=id).first()
    if form.validate_on_submit():
        hero.name = form.name.data
        hero.star = form.star.data
        hero.sex = form.sex.data
        hero.position = form.position.data
        hero.is_public = form.is_public.data
        hero.experience = form.experience.data
        hero.career_id = form.career.data
        hero.tags = form.tags.data
        db.session.add(hero)
        db.session.commit()
        return redirect(url_for('.hero', id=id))
    form.name.data = hero.name
    form.star.data = hero.star
    form.sex.data = hero.sex
    # FIXME: career id and tag id not right
    form.career.data = hero.career_id
    form.position.data = hero.position
    form.is_public.data = hero.is_public
    form.experience.data = hero.experience
    form.tags.data = hero.tags.all()
    return render_template('edit_hero.html', form=form, hero=hero)

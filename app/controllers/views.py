# -*- coding: utf-8 -*-
import json
from flask import render_template, redirect, request, url_for, current_app
from itertools import combinations, groupby
from . import main
from . forms import *
from .fetch_data import FetchHero


@main.route('/')
def index():
    return 'Hello World'


@main.route('/heros')
def heros():
    page = request.args.get('page', 1, type=int)
    pagination = Hero.query.paginate(page, per_page=20, error_out=False)
    heros = pagination.items
    careers = {hero.name: Career.browse(hero.career_id).name for hero in heros}
    return render_template('heros.html', pagination=pagination, careers=careers, heros=heros)


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
    form.career.data = hero.career_id
    form.position.data = hero.position
    form.is_public.data = hero.is_public
    form.experience.data = hero.experience
    form.tags.data = hero.tags.all()
    return render_template('edit_hero.html', form=form, hero=hero)


@main.route('/fetch')
def fetch():
    fetch_tool = FetchHero(current_app.config['FETCH_URL'])
    fetch_tool.fetch_url()
    return redirect(url_for('.heros'))


@main.route('/query')
def query():
    careers = Career.query.all()
    tags = Tag.query.all()
    heros = Hero.query.filter_by(is_public=True).order_by(Hero.star.desc()).all()
    return render_template('query.html', careers=careers, tags=tags, heros= heros)


@main.route('/query-data', methods=['POST'])
def query_data():
    data = json.loads(request.get_data())
    # {'a': ['a1', 'a2'], 'b': ['b1', 'b2']} --> {'a1': 'a', 'a2': 'a', 'b1': 'b', 'b2': 'b'}
    _field_mapping = {i: k for k, v in data.items() for i in v}
    _all_combinations = sum([list(combinations(_field_mapping.keys(), i + 1)) for i in range(len(_field_mapping.keys()))], [])
    _all_combinations = list(filter(lambda co: len(co) <= 3, _all_combinations))
    res = []
    for combine in _all_combinations:
        clause = {k: list(v) for k, v in groupby(combine, key=lambda c: _field_mapping[c])}
        if any(len(group) > 1 for key, group in clause.items() if key != 'tags'):
            continue
        query = Hero.query
        for key, group in clause.items():
            if key == 'career_id':
                query = query.filter_by(**{key: Career.name_get(group[0]).id})
            elif key == 'tags':
                for tag in group:
                    query = query.intersect(Hero.query.join(Hero.tags).filter(Tag.name==tag))
            else:
                query = query.filter_by(**{key: group[0]})
        heros = query.filter_by(is_public=True).order_by(Hero.star.desc()).all()
        if heros:
            res.append({'combine': combine, 'hero_ids': [hero.id for hero in heros], 'stars': [hero.star for hero in heros]})
            res.sort(key=lambda d: min(d['stars']) > 3, reverse=True)
    return json.dumps(res)

import requests
from bs4 import BeautifulSoup
from .. models.hero import *


class FetchHero:
    def __init__(self, url):
        self.url = url

    def fetch_url(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text)
        trs = soup.find('table', id='CardSelectTr').find_all('tr')
        for tr in trs:
            if not tr.td:
                continue
            name = tr.td.a['title']
            career_id = Career.name_get(tr['data-param1'] + '干员').id
            star = int(tr['data-param2'][0])
            sex = tr['data-param3'] + '性干员'
            position, *tags = sorted(tr['data-param5'].split(','), key=lambda s: '近战位'in s or '远程位' in s, reverse=True)
            tags = [tag.strip() for tag in tags]
            if '新手' in tags:
                tags.remove('新手')
            tag_ids = list(map(Tag.name_get, tags))
            is_public = '公开招募' in tr['data-param6']
            if star == 6:
                experience = '高级资深干员'
            elif star == 5:
                experience = '资深干员'
            elif star < 3:
                experience = '新手'
            else:
                experience = None
            hero = Hero.name_get(name)
            if hero:
                hero.career_id = career_id
                hero.star = star
                hero.sex = sex
                hero.position = position
                hero.tags = tag_ids
                hero.is_public = is_public
                hero.experience = experience
            else:
                hero = Hero(
                    name=name,
                    career_id=career_id,
                    star=star,
                    sex=sex,
                    position=position,
                    tags=tag_ids,
                    is_public=is_public,
                    experience=experience,
                )
            db.session.add(hero)
        db.session.commit()

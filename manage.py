# -*- coding: utf-8 -*-

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models.hero import *
from app import create_app

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return {
        'app': app,
        'db': db,
        'Hero': Hero,
        'Career': Career,
        'Tag': Tag,
    }


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    # from flask_migrate import upgrade
    #
    # upgrade()

    Career.insert_careers()
    Tag.insert_tags()


if __name__ == '__main__':
    manager.run()

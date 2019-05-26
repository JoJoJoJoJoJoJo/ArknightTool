# -*- coding: utf-8 -*-

from flask_script import Manager, Shell
# from flask_migrate import Migrate, MigrateCommand
from app.models.hero import *
from app import create_app

app = create_app()
manager = Manager(app)


def make_shell_context():
    return {
        'app': app,
        'db': db,
        'Hero': Hero,
        'Career': Career,
        'Tag': Tag,
    }


manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()

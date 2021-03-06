# coding=utf-8
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    with open('.env') as f:
        for line in f:
            var = line.strip().split('=')
            if len(var) == 2:
                os.environ[var[0]] = var[1]
from flask.ext.script import Manager

from app import create_app, db
from app.models import User


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def adduser(email, username, admin=False):
    """Register a new user."""
    from getpass import getpass

    password = getpass()
    password_confirm = getpass(prompt='Confirm: ')
    if not password == password_confirm:
        import sys

        sys.exit('Error: passwords do not match.')

    db.create_all()
    user = User(email=email, username=username, password=password,
                is_admin=admin)
    db.session.add(user)
    db.session.commit()
    print 'User {} was registered successfully.'.format(username)


@manager.command
def migrate():
    """Migrate database."""

    db.create_all()
    print 'Database migrated successfully.'


@manager.command
def test():
    from subprocess import call

    call(['nosetests', '-v', '--with-coverage', '--cover-package=app',
          '--cover-branches', '--cover-erase', '--cover-html',
          '--cover-html-dir=cover'])


if __name__ == '__main__':
    manager.run()
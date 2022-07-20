from flask import Blueprint
import click
from flask_api.models import User, db

cli = Blueprint('command', __name__)


@cli.cli.command('create_superuser')
@click.argument('email')
@click.argument('password')
def create(email, password):
    ''' Creates a superuser '''
    if User.find_by_email(email):
        raise ValueError('Email exists.')
    user = User(email=email, password=password, is_superuser=True)
    db.session.add(user)
    db.session.commit()
    print(f'Superuser created {email=}')

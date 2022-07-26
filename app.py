import click

from flask_api import app, db
from flask_api.models import History, Role, User


@app.shell_context_processor
def shell():
    return {
        'db': db,
        'user': User,
        'role': Role,
        'history': History,
    }


@app.cli.command('create-superuser')
@click.argument('email')
@click.password_option(help='Do not set password on the command line!')
def create(email, password):
    ''' Creates a superuser '''
    if User.find_by_email(email):
        error = f'Error: {email} is already registered'
        click.secho(f'{error}\n', fg='red', bold=True)
        return 1
    user = User(email=email, password=password, is_superuser=True)
    db.session.add(user)
    db.session.commit()
    message = f"Successfully added new superuser:\n {user}"
    click.secho(message, fg="blue", bold=True)
    return 0

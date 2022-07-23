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

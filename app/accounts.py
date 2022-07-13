from passlib.hash import argon2 as hasher
from models import User
from app import app
from db import db

user_id = getattr(User, app.config['user_id_field'])


def hash_password(password: str):
    return hasher.hash(password)


def verify_password(password: str, hash):
    return hasher.verify(password, hash)


def get_user(id):
    return User.query.filter(user_id == id).one_or_none()


def create_user(id, password):
    if get_user(id):
        return False
    new_user = User(user_id=id, password=hash_password(password))
    db.session.add(new_user)
    db.session.commit()
    return new_user

import uuid

from passlib.hash import argon2 as hasher
from sqlalchemy.dialects.postgresql import UUID

from flask_api import db

from .utils import utc_now

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.ForeignKey('role.id'), primary_key=True),
)


class IdTimeStampedMixin:
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)


class Role(db.Model, IdTimeStampedMixin):
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model, IdTimeStampedMixin):
    email = db.Column(db.String(255), unique=True, nullable=False)
    _password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    roles = db.relationship(Role, secondary=roles_users, backref='users')
    is_superuser = db.Column(db.Boolean(), default=False)

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password: str):
        self._password_hash = hasher.hash(password)

    def verify_password(self, password: str):
        return hasher.verify(password, self._password_hash)

    def get_jwt(self):
        pass

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).one_or_none()

    def __repr__(self):
        return f'<User {self.email}>'


class History(db.Model):
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    additional_info = db.Column(db.Text)
    user = db.relationship(User, backref='log')

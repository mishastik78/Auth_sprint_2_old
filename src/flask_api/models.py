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

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def find_by_id(cls, id):
        if uuid.UUID(str(id)).version != 4:
            raise ValueError
        return cls.query.filter_by(id=id).one_or_none()

    def __repr__(self):
        return f'<Role {self.name}>'


class OAuthAccount(db.Model):
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    issuer = db.Column(db.String(255), nullable=False, primary_key=True)
    sub = db.Column(db.String(1024), nullable=False)
    user = db.relationship('User', backref='oauth_accs')


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

    def add_history(self, action, info=None):
        row = History(action=action, additional_info=info, user=self)
        db.session.add(row)
        db.session.commit()

    def get_history(self, limit=None):
        return History.query.filter_by(user=self).order_by(History.created_at.desc()).limit(limit).all()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def find_by_id(cls, id):
        if uuid.UUID(str(id)).version != 4:
            raise ValueError
        return cls.query.filter_by(id=id).one_or_none()

    @classmethod
    def find_by_oauth(cls, issuer, sub):
        acc = OAuthAccount.query.filter_by(issuer=issuer, sub=sub).one_or_none()
        return acc.user if acc else None

    def __repr__(self):
        return f'<User {self.email}>'


class History(db.Model):
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now, primary_key=True)
    action = db.Column(db.String(255), nullable=True)
    additional_info = db.Column(db.Text)
    user = db.relationship(User, backref='history')

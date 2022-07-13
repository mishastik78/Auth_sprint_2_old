import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from db import db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.ForeignKey('role.id'), primary_key=True),
)


class IdTimeStampedMixin:
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=datetime.datetime.utcnow)


class Role(db.Model, IdTimeStampedMixin):
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model, IdTimeStampedMixin):
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    roles = db.relationship(Role, secondary=roles_users, backref='users')

    def __repr__(self):
        return f'<User {self.email}>'


class LogHistory(db.Model):
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    additional_info = db.Column(db.Text)
    user = db.relationship(User, backref='log')

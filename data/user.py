import sqlalchemy
from flask import url_for

from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    avatar = sqlalchemy.Column(sqlalchemy.String,
                               default="static/data/avatars/default.png")
    is_premium = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User> {self.nickname} {"Premium" if self.is_premium else ""}'

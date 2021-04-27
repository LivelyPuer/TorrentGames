import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    short_description = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    system_requirements = sqlalchemy.Column(sqlalchemy.String, default="На любом утюге потянет")
    category_id = sqlalchemy.Column(sqlalchemy.Integer)
    description = sqlalchemy.Column(sqlalchemy.String)
    need_premium = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    url = sqlalchemy.Column(sqlalchemy.String)
    version = sqlalchemy.Column(sqlalchemy.String)
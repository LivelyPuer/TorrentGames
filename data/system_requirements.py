import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class SystemRequirements(SqlAlchemyBase):
    __tablename__ = 'system_requirements'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    system = sqlalchemy.Column(sqlalchemy.String)
    cpu = sqlalchemy.Column(sqlalchemy.String)
    ram = sqlalchemy.Column(sqlalchemy.Integer)
    video = sqlalchemy.Column(sqlalchemy.String)
    disk_space = sqlalchemy.Column(sqlalchemy.Integer)

    games = orm.relation("Game", back_populates='system_requirements')
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    nickname = StringField('Ник')
    avatar_url = StringField("URL аватарки")
    avatar = FileField("Аватрака")
    submit = SubmitField('Изменить')

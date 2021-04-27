from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    short_description = TextAreaField("Краткое описание", validators=[DataRequired()])
    version = StringField("Версия игры", validators=[DataRequired()])
    image = FileField("Картинка")
    image_url = StringField("URL картинки")
    description = TextAreaField("Описание", validators=[DataRequired()])
    need_premium = BooleanField("Для скачивания нужен премиум")
    category = SelectField('Категория',
                           choices=[(1, 'Гонки'), (2, 'Хоррор'), (3, 'Шутер'), (4, 'Приключение'),
                                    (5, 'Песочница'), (6, "Экшен"), (7, "Стратегия"),
                                    (8, 'Головоломки'),
                                    (10, 'Ритмичные игры')], validators=[DataRequired()])
    url = FileField("Torrent-файл", validators=[DataRequired()])
    submit = SubmitField('Добавить')
    system_requirements = TextAreaField("Системные требования")

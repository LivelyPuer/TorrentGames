from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash, generate_password_hash


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    nickname = StringField('Ник', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторный пароль', validators=[DataRequired()])
    premium = BooleanField("Купить премиум аккаунт?")
    submit = SubmitField('Войти')
import datetime
import json
import os

from flask import Flask, render_template, redirect
from flask_ngrok import run_with_ngrok
from flask_restful import Api, abort
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired

from data.category import Category
from data.game import Game
from flask import redirect, render_template
from flask_login import logout_user, login_required, login_user, LoginManager, current_user

from data import db_session, games_resources

from data.user import User
from forms.game import GameForm
from forms.login_form import LoginForm
from forms.profile import ProfileForm
from forms.search import SearchForm
from forms.user import RegisterForm


def page_not_found(e):
    return render_template('404.html'), 404


app = Flask(__name__)
run_with_ngrok(app)
app.register_error_handler(404, page_not_found)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
UPLOAD_PATH = 'static/data'
db_session.global_init("database.db")
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(games_resources.GamesListResource, '/api/games')
api.add_resource(games_resources.GamesSearchResource, '/api/games/search/<game_title>')
api.add_resource(games_resources.GameResource, '/api/game/<int:game_id>')
api.add_resource(games_resources.UserEmailPremiumResource, '/api/user/<user_email>')


@app.route('/', methods=["GET", "POST"])
def index():
    db_sess = db_session.create_session()
    games = db_sess.query(Game).all()
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('/search/{}'.format(form.search.data))
    print(current_user if current_user else "Не авторизаван")
    return render_template("main.html", games=games, form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login2.html', message="Wrong login or password", form=form)
    return render_template('login2.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            nickname=form.nickname.data,
            is_premium=form.premium.data

        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addgame', methods=['GET', 'POST'])
@login_required
def add_game():
    form = GameForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Game).filter(Game.title == form.title.data).all():
            return render_template('add_game.html', title='Дбавление Игры',
                                   form=form, message="Игра с таким названием уже существует")
        print(form.image_url.data, ":", form.image.check_validators([DataRequired()]))
        if form.image_url.data == "" and form.image.check_validators([DataRequired()]):
            return render_template('add_game.html', title='Добавление Игры',
                                   form=form, message="Нет картинки")
        game = Game(
            title=form.title.data,
            short_description=form.short_description.data,
            version=form.version.data,
            description=form.description.data,
            need_premium=form.need_premium.data,
            category_id=form.category.data
        )
        if form.image_url.data:
            game.image = form.image_url.data
        else:
            f = form.image.data
            filename = secure_filename(f.filename)
            img_path = os.path.join(
                UPLOAD_PATH, 'img', filename
            )
            f.save(img_path)
            game.image = '\\' + img_path

        f = form.url.data
        filename = secure_filename(f.filename)
        torrent_path = os.path.join(
            UPLOAD_PATH, 'torrent', filename
        )
        f.save(torrent_path)
        game.url = '\\' + torrent_path
        game.user_id = current_user.id
        db_sess = db_session.create_session()
        db_sess.add(game)
        db_sess.commit()
        return redirect('/addgame')
    return render_template('add_game.html', title='Регистрация Работы', form=form)


def n_to_br(string) -> str:
    s = str(string)
    print(list(s))
    s.replace("\n", "<br>")
    print(s)
    return s


@app.route('/aboutgame/<int:game_id>')
def about_game(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).get(game_id)
    category = db_sess.query(Category).get(game.category_id)
    print(category)
    if game is None:
        abort(404)
    return render_template('about_game.html', game=game, category=category.title, n_to_br=n_to_br)


@app.route('/l')
def d():
    return render_template('index.html')


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        if form.nickname.data:
            user.nickname = form.nickname.data
        if form.avatar.data.filename:
            f = form.avatar.data
            filename = secure_filename(f.filename)
            img_path = os.path.join(
                UPLOAD_PATH, 'img', filename
            )
            f.save(img_path)
            user.avatar = '\\' + img_path
        if form.avatar_url.data:
            user.avatar = form.avatar_url.data
        db_sess.commit()

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    user_games = db_sess.query(Game).filter(Game.user_id == current_user.id)
    return render_template('profile.html', user=user, games=user_games, form=form)


@app.route('/search/category/<int:category_id>', methods=['GET', 'POST'])
def find_category(category_id):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('/search/{}'.format(form.search.data))
    db_sess = db_session.create_session()
    games = db_sess.query(Game).filter(Game.category_id == category_id).all()
    return render_template("main.html", games=games, form=form)


@app.route('/search/<game_title>', methods=['GET', 'POST'])
def search(game_title):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('/search/{}'.format(form.search.data))
    else:
        session = db_session.create_session()
        games = session.query(Game).all()
        dct = {}
        for game in games:
            dct[game.id] = 0
            i = 0
            if game_title.lower() in game.title.lower():
                dct[game.id] += len(game_title)
            if len(game_title) == len(game.title):
                dct[game.id] += len(game_title) // 2
            for char in zip(game.title.lower(), game_title.lower()):
                if i > len(game_title):
                    break
                if char[0] == char[1]:
                    dct[game.id] += 1
                i += 1
        lst = []
        for key, value in dct.items():
            lst.append((key, value))
        lst.sort(key=lambda x: x[1], reverse=True)

        game = session.query(Game).filter(Game.id.in_(
            [x[0] for x in
             list(filter(lambda x: lst[0][1] - 2 <= x[1] <= lst[0][1] + 2, lst))])).all()
        return render_template("main.html", games=game, form=form, value=game_title)


if __name__ == "__main__":
    app.run()

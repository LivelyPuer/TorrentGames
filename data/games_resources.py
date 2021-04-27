from . import db_session
from .game import Game
from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource

from .user import User


def abort_if_game_not_found(game_id):
    session = db_session.create_session()
    news = session.query(Game).get(game_id)
    if not news:
        abort(404, message=f"Game {game_id} not found")


def abort_if_user_not_found(user_mail):
    session = db_session.create_session()
    news = session.query(User).filter(User.email == user_mail).first()
    if not news:
        abort(404, message=f"User email {user_mail} not found")


parser = reqparse.RequestParser()
# parser.add_argument("main", type=dict, action="append")
parser.add_argument("id", required=False, type=int)
parser.add_argument("title", required=False)
parser.add_argument("short_description", required=True)
parser.add_argument("image", required=True)
parser.add_argument("user_id", required=True, type=int)
parser.add_argument("category", required=True, type=int)
parser.add_argument("system_requirements", required=True)
parser.add_argument("description", required=True)
parser.add_argument("need_premium", required=True, type=bool)
parser.add_argument("url", required=True)
parser.add_argument("version", required=False)


class GameResource(Resource):
    def get(self, game_id):
        abort_if_game_not_found(game_id)
        session = db_session.create_session()
        game = session.query(Game).get(game_id)
        return jsonify(game.to_dict(
            only=("id",
                  "title",
                  "short_description",
                  "image",
                  "user_id",
                  "system_requirements",
                  "description",
                  "need_premium",
                  "url",
                  "version",
                  )))

    def delete(self, game_id):
        abort_if_game_not_found(game_id)
        session = db_session.create_session()
        game = session.query(Game).get(game_id)
        session.delete(game)
        session.commit()
        return jsonify({'success': 'OK'})


class GamesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(Game).all()
        return jsonify([item.to_dict(
            only=("id",
                  "title",
                  "short_description",
                  "image",
                  "user_id",
                  "system_requirements",
                  "description",
                  "need_premium",
                  "url",
                  "version",
                  )) for item in users])

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        game = Game(
            title=args["title"],
            short_description=args["short_description"],
            version=args["version"],
            image=args["image"],
            description=args["description"],
            need_premium=args["need_premium"],
            category_id=args["category"],
            url=args["url"],
            system_requirements=args["system_requirements"],
            user_id=args["user_id"],
        )
        session.add(game)
        session.commit()
        return jsonify(
            {'success': 'OK'})


class GamesSearchResource(Resource):
    def get(self, game_title):
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
        print(lst)
        max_value = max(lst, key=lambda x: x[1])
        game = session.query(Game).get(max_value[0])
        return jsonify(game.to_dict(
            only=("id",
                  "title",
                  "short_description",
                  "image",
                  "user_id",
                  "system_requirements",
                  "description",
                  "need_premium",
                  "url",
                  "version",
                  )))


class UserEmailPremiumResource(Resource):
    def get(self, user_email):
        abort_if_user_not_found(user_email)
        session = db_session.create_session()
        user = session.query(User).filter(User.email == user_email).first()
        return jsonify(user.to_dict(
            only=('id', 'email',
                  'is_premium',
                  )))

    def put(self, user_email):
        abort_if_user_not_found(user_email)
        session = db_session.create_session()
        user = session.query(User).filter(User.email == user_email).first()
        user.is_premium = True
        session.commit()
        return jsonify(
            {'success': 'OK'})

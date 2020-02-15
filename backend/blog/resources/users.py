from uuid import uuid4
from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (
    create_refresh_token, jwt_refresh_token_required, get_jwt_identity,
    create_access_token, jwt_required,
)

from ..database import db
from ..models import UserModel
from .utils import no_spacing_string


class User(Resource):
    def get(self):
        users = UserModel.query.all()

        return {
            'users': [user.jsonify() for user in users]
        }

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=no_spacing_string(max_length=40, min_length=3),
        required=True,
    )
    parser.add_argument(
        'password',
        type=no_spacing_string(max_length=40, min_length=8),
        required=True,
    )
    parser.add_argument(
        'email',
        type=no_spacing_string(max_length=50, min_length=8),
        required=True,
    )

    def post(self):
        user_data = self.parser.parse_args()

        user = UserModel.query.filter(
            (UserModel.username == user_data['username']) |
            (UserModel.email == user_data['email'])
        ).first()

        if user:
            reason = user.email == user_data['email'] and 'email' or 'username'
            return {
                'msg': f"User with this {reason} already exists",
            }, 400

        new_user = UserModel(
            username=user_data['username'],
            password=sha256.hash(user_data['password']),
            email=user_data['email'],
            identity=str(uuid4()),
        )

        db.session.add(new_user)
        db.session.commit()

        return {
            'id': new_user.id,
        }


class Authorization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'identifier',
        type=no_spacing_string(max_length=40, min_length=3),
        required=True,
    )

    parser.add_argument(
        'password',
        type=no_spacing_string(max_length=40, min_length=8),
        required=True,
    )

    def post(self):
        data = self.parser.parse_args()

        user = UserModel.query.filter(
            (UserModel.username == data['identifier']) |
            (UserModel.email == data['identifier'])
        ).first()

        if not user:
            return {
                'msg': 'User not found',
            }, 404

        if sha256.verify(data['password'], user.password):
            return {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'refresh_token': create_refresh_token(identity=user.identity)
            }
        return {
            'msg': 'wrong password',
        }, 400


class AccessToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = UserModel.query.filter(
            UserModel.identity == get_jwt_identity()
        ).first()

        if not user:
            return {
                'msg': 'Identity is outdated.',
            }, 400

        return {
            'access_token': create_access_token(user.identity),
        }


class AccessedPing(Resource):
    @jwt_required
    def get(self):
        return {
            'on_accessed_ping': 'we_accessed_pong'
        }

from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256

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
        required=True
    )
    parser.add_argument(
        'password',
        type=no_spacing_string(max_length=40, min_length=8),
        required=True
    )
    parser.add_argument(
        'email',
        type=no_spacing_string(max_length=40, min_length=8),
        required=True
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
                'description': f"User with this {reason} already exists",
            }, 400

        new_user = UserModel(
            username=user_data['username'],
            password=sha256.hash(user_data['password']),
            email=user_data['email'],
        )

        db.session.add(new_user)
        db.session.commit()

        return {
            'id': new_user.id,
        }

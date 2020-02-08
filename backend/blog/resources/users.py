from flask_restful import Resource, reqparse

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

    def post(self):
        args = self.parser.parse_args()
        return {
            'username': args['username']
        }

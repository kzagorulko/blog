from flask_restful import Api

from .users import User, Authorization, AccessToken, AccessedPing

api = Api()

api.add_resource(User, '/users')
api.add_resource(AccessedPing, '/access-ping')
api.add_resource(AccessToken, '/access-tokens')
api.add_resource(Authorization, '/refresh-tokens')

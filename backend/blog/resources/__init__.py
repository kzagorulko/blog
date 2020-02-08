from flask_restful import Api

from .users import User

api = Api()

api.add_resource(User, '/users')

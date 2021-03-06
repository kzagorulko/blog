from enum import Enum

from .database import db


class PrivacyType(Enum):
    ALL = 0
    AUTHORIZED = 1
    HIDDEN = 2


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    identity = db.Column(db.String(36), unique=True, nullable=False)
    privacy = db.Column(
        db.Enum(PrivacyType), nullable=False, default=PrivacyType.ALL
    )
    is_active = db.Column(
        db.Boolean(create_constraint=False), default=False, nullable=False
    )

    def jsonify(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
        }

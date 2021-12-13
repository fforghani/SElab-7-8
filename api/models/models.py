from datetime import datetime

from flask import g

from api.conf.auth import auth, jwt
from api.database.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=80))
    password = db.Column(db.String(length=80))
    email = db.Column(db.String(length=80))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_role = db.Column(db.String, default="user")

    def generate_auth_token(self, permission_level):
        if permission_level == 1:
            token = jwt.dumps({"email": self.email, "admin": 1})
            return token

        elif permission_level == 2:
            token = jwt.dumps({"email": self.email, "admin": 2})
            return token

        return jwt.dumps({"email": self.email, "admin": 0})

    # Generates a new access token from refresh token.
    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        g.user = None
        try:
            data = jwt.loads(token)
        except:
            return False

        if "email" and "admin" in data:
            g.user = data["email"]
            g.admin = data["admin"]
            return True
        return False

    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', name='%s', password='%s', email='%s', created='%s')>" % (
            self.id,
            self.username,
            self.password,
            self.email,
            self.created,
        )

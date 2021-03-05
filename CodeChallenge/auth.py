from datetime import datetime
from typing import List

import argon2
from flask import current_app
from flask_jwt_extended import JWTManager
from itsdangerous import URLSafeTimedSerializer

from .models import db, Users

jwt = JWTManager()


def hash_password(plaintext):
    ph = argon2.PasswordHasher()
    return ph.hash(plaintext)


def authenticate(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@jwt.user_lookup_loader
def identity(_, jwt_payload):
    return Users.query.get(jwt_payload["sub"])


def create_user(email, username, password):
    u = Users()
    u.parent_email = email
    u.username = username
    u.password = hash_password(password)
    u.dob = datetime.now().strftime("%Y-%m-%d")

    db.session.add(u)
    db.session.commit()


def reset_user(username, password):
    u = Users.query.filter_by(username=username).first()
    u.password = hash_password(password)

    db.session.commit()


def password_reset_token(user: Users) -> str:
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return ts.dumps(user.username, salt="recovery-key")


def reset_password_from_token(token: str, password: str):
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    username = ts.loads(token, salt="recovery-key", max_age=86400)
    reset_user(username, password)

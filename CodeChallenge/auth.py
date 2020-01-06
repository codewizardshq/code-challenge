import argon2
from flask import current_app
from flask_jwt_extended import JWTManager
from itsdangerous import URLSafeTimedSerializer

from .models import db

jwt = JWTManager()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=True)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<User {self.username!r}>"

    def check_password(self, password):
        ph = argon2.PasswordHasher()
        try:
            return ph.verify(self.password, password)
        except argon2.exceptions.VerifyMismatchError:
            return False


def hash_password(plaintext):
    ph = argon2.PasswordHasher()
    return ph.hash(plaintext)


def authenticate(username, password):
    user = Users.query.filter_by(email=username).first()
    if user and user.check_password(password):
        return user


@jwt.user_loader_callback_loader
def identity(identity):
    return Users.query.get(identity)


def create_user(email, username, password):
    u = Users()
    u.email = email
    u.username = username
    u.password = hash_password(password)

    db.session.add(u)
    db.session.commit()


def reset_user(email, password):
    u = Users.query.filter_by(email=email)
    u.password = hash_password(password)

    db.session.commit()


def password_reset_token(user: Users) -> str:
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return ts.dumps(user.email, salt="recovery-key")


def reset_password_from_token(token: str, password: str):
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    email = ts.loads(token, salt="recovery-key", max_age=86400)
    reset_user(email, password)

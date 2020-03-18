from datetime import datetime

import argon2
from flask import current_app
from flask_jwt_extended import JWTManager
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import func

from .models import db, Vote

jwt = JWTManager()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentfirstname = db.Column(db.String(80), nullable=True)
    studentlastname = db.Column(db.String(80), nullable=True)

    parentfirstname = db.Column(db.String(80), nullable=True)
    parentlastname = db.Column(db.String(80), nullable=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    parent_email = db.Column(db.String(120), unique=False, nullable=False)
    student_email = db.Column(db.String(120), unique=False, nullable=True)
    dob = db.Column(db.String(10), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=True)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    found_us = db.Column(db.String(2000))

    def __repr__(self):
        return f"<User {self.username!r}>"

    def check_password(self, password):
        ph = argon2.PasswordHasher()
        try:
            return ph.verify(self.password, password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def casted_votes(self) -> int:
        q = db.session \
            .query(func.count(Vote.id)) \
            .filter_by(user_id=self.id)

        n = q.scalar()
        return n

    def votes(self):
        v = Vote.query \
            .filter_by(user_id=self.id) \
            .all()
        return v

    def display(self):
        if self.studentfirstname is not None \
                and self.studentlastname is not None \
                and len(self.studentlastname):
            return f"{self.studentfirstname} " \
                   f"{self.studentlastname[0]}."


def hash_password(plaintext):
    ph = argon2.PasswordHasher()
    return ph.hash(plaintext)


def authenticate(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@jwt.user_loader_callback_loader
def identity(ident):
    return Users.query.get(ident)


def create_user(email, username, password):
    u = Users()
    u.parent_email = email
    u.username = username
    u.password = hash_password(password)
    u.dob = datetime.now().strftime("%Y-%m-%d")

    db.session.add(u)
    db.session.commit()


def reset_user(username, password):
    u = Users.query.filter_by(username=username)
    u.password = hash_password(password)

    db.session.commit()


def password_reset_token(user: Users) -> str:
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return ts.dumps(user.username, salt="recovery-key")


def reset_password_from_token(token: str, password: str):
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    username = ts.loads(token, salt="recovery-key", max_age=86400)
    reset_user(username, password)

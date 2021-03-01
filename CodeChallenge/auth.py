from datetime import datetime
from typing import List

import argon2
from flask import current_app
from flask_jwt_extended import JWTManager
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import func
from .mailgun import email_template, mg_list_add

from .models import db, Vote

jwt = JWTManager()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_first_name = db.Column(db.String(80), nullable=True)
    student_last_name = db.Column(db.String(80), nullable=True)

    parent_first_name = db.Column(db.String(80), nullable=True)
    parent_last_name = db.Column(db.String(80), nullable=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    parent_email = db.Column(db.String(120), unique=False, nullable=False)
    student_email = db.Column(db.String(120), unique=False, nullable=True)
    dob = db.Column(db.String(10), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=True)
    password = db.Column(db.String(120), nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    found_us = db.Column(db.String(2000))
    teacher = db.Column(db.String(200))
    school_name = db.Column(db.String(200))
    cwhq_username = db.Column(db.String(100))

    def __repr__(self):
        return f"<User({self.username!r})>"

    def __str__(self):
        return self.username

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
        if self.student_first_name is not None \
                and self.student_last_name is not None \
                and len(self.student_last_name):
            return f"{self.student_first_name} " \
                   f"{self.student_last_name[0]}."

    def _mail_recipients(self) -> List[str]:
        if not self.student_email:
            return [self.parent_email]
        return [self.parent_email, self.student_email]

    def send_welcome_email(self):
        email_template(
            self._mail_recipients(),
            "Mission Confirmed! Welcome to the CodeWizardsHQ Code Challenge",
            "challenge_welcome.html",
            name=self.student_first_name or self.parent_first_name
        )

    def send_confirmation_email(self):
        email_template(
            self._mail_recipients(),
            "Your Code Challenge Account",
            "challenge_account_confirm.html",
            username=self.username,
            name=self.student_first_name or self.parent_first_name
        )

    def _mg_vars(self):
        return dict(
            codeChallengeUsername=self.username,
            studentEmail=self.student_email,
            studentFirstName=self.student_first_name,
            studentLastName=self.student_last_name,
            studentName=f"{self.student_first_name} {self.student_last_name}",
            parentFirstName=self.parent_first_name,
            parentLastName=self.parent_last_name,
            parentName=f"{self.parent_first_name} {self.parent_last_name}",
            userId=self.id,
            studentDOB=self.dob,
            type=""
        )

    def add_to_mailing_list(self, list_name: str):
        for i, addr in enumerate(self._mail_recipients()):
            mg_vars = self._mg_vars()

            if i == 0:
                mg_vars["type"] = "parent"
            else:
                mg_vars["type"] = "student"

            mg_list_add(addr, list_name, mg_vars)


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

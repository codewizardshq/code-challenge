import re
from datetime import datetime
from typing import List, Tuple

import argon2  # noQA
import requests
from flask import current_app
from flask_jwt_extended import JWTManager
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import func, event

from CodeChallenge.mailgun import email_template, mg_list_add, raise_undeliverable
from CodeChallenge.models.connection import db
from CodeChallenge.models.vote import Vote

jwt = JWTManager()


def lookup_username(try_username):
    return User.query.filter_by(username=try_username).first()


def clean_username(try_username):
    return re.sub(r"[^ A-Z_0-9]", "_", try_username, flags=re.IGNORECASE).strip()


class ValidationError(Exception):
    """Thrown when a field fails validation."""

    pass


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_first_name = db.Column(db.String(80), nullable=True)
    student_last_name = db.Column(db.String(80), nullable=True)

    parent_first_name = db.Column(db.String(80), nullable=True)
    parent_last_name = db.Column(db.String(80), nullable=True)

    username = db.Column(db.String(32), unique=True, nullable=False, index=True)
    parent_email = db.Column(db.String(120), unique=False, nullable=False, index=True)
    student_email = db.Column(db.String(120), unique=False, nullable=True)
    dob = db.Column(db.String(10), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=True)
    password = db.Column(db.String(120), nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    found_us = db.Column(db.String(2000))
    school_name = db.Column(db.String(200))
    cwhq_username = db.Column(db.String(100))
    is_teacher = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    teacher = db.relationship("User", lazy=True, uselist=False)

    def __init__(self):
        self.errors = []  # type: List[str]

        # temporary place to store the user's plaintext password for bulk imports
        # this property will otherwise be an empty string
        self.plaintext = ""  # type: str
        self.original_row = []  # type: List[str]

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
        q = db.session.query(func.count(Vote.id)).filter_by(user_id=self.id)

        n = q.scalar()
        return n

    def votes(self):
        v = Vote.query.filter_by(user_id=self.id).all()
        return v

    def display(self):
        if (
            self.student_first_name is not None
            and self.student_last_name is not None
            and len(self.student_last_name)
        ):
            return f"{self.student_first_name} " f"{self.student_last_name[0]}."

    def _mail_recipients(self) -> List[str]:
        if not self.student_email:
            return [self.parent_email]
        return [self.parent_email, self.student_email]

    def send_welcome_email(self):
        email_template(
            self._mail_recipients(),
            "Mission Confirmed! Welcome to the CodeWizardsHQ Code Challenge",
            "challenge_welcome.html",
            name=self.student_first_name or self.parent_first_name,
        )

    def send_confirmation_email(self, password=None):
        email_template(
            self._mail_recipients(),
            "Your Code Challenge Account",
            "challenge_account_confirm.html",
            username=self.username,
            name=self.student_first_name or self.parent_first_name,
            password=password,
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
            type="",
        )

    def add_to_mailing_list(self, list_name: str):
        for i, addr in enumerate(self._mail_recipients()):
            mg_vars = self._mg_vars()

            if i == 0:
                mg_vars["type"] = "parent"
            else:
                mg_vars["type"] = "student"

            mg_list_add(addr, list_name, mg_vars)

    def generate_password(self):
        """Generate a random password. Set's the user's password to the generated_students value,
        then returns the password string in plaintext. Does NOT commit.

        Raises :class:`HTTPError`, if one occurred."""
        if current_app.config["TESTING"]:
            import secrets

            pw = secrets.token_urlsafe()
            self.set_password(pw)
            self.plaintext = pw
            return

        response = requests.get("https://www.dinopass.com/password/strong")
        response.raise_for_status()

        self.set_password(response.text)
        self.plaintext = response.text

    def _initial_username(self) -> str:
        if not self.student_first_name or not self.student_last_name:
            return self.parent_email

        try:
            last = self.student_last_name[0]
        except IndexError:
            last = ""

        try_username = (self.student_first_name + last).casefold()
        try_username = clean_username(try_username)

        return try_username

    def generate_username(self) -> None:
        """Generates an initial username, then increments a discriminator number
        on the initial username until an unused one is generated_students. Sets the generated_students username
        on the object but does not commit changes."""
        try_username = self._initial_username()
        discriminator = 2

        while lookup_username(try_username) is not None:
            try_username += str(discriminator)
            discriminator += 1

        self.username = try_username

    def set_password(self, plaintext):
        self.password = argon2.PasswordHasher().hash(plaintext)

    def set_username(self, username: str):
        if not username:
            raise ValidationError("username cannot be null or empty")

        if len(username) < 3:
            raise ValidationError("username is not long enough")

        self.username = username.strip()

    def set_parent_email(self, email: str):
        if not email or type(email) != str:
            raise ValidationError("parent email cannot be null or empty")

        email = email.strip()
        raise_undeliverable(email)

        self.parent_email = email

    def set_parent_first_name(self, name: str):
        assert type(name) == str
        self.parent_first_name = name.strip().title()

    def set_parent_last_name(self, name: str):
        assert type(name) == str
        self.parent_last_name = name.strip().title()

    def set_student_first_name(self, name: str):
        assert type(name) == str
        self.student_first_name = name.strip().title()

    def set_student_last_name(self, name: str):
        assert type(name) == str
        self.student_last_name = name.strip().title()

    def set_school_name(self, name: str):
        assert type(name) == str
        if not name:
            raise ValidationError("school name may not be None or empty")
        self.school_name = name

    def set_student_email(self, email: str):
        if not email or type(email) != str:
            raise ValidationError(
                "may not set a None or empty student email. use clear_student_email()"
            )
        email = email.strip()
        raise_undeliverable(email)
        self.student_email = email

    def clear_student_email(self):
        self.student_email = None

    def to_csv(self) -> Tuple[str, ...]:
        return (
            str(self.id),
            self.student_first_name,
            self.student_last_name,
            self.parent_first_name,
            self.parent_last_name,
            self.username,
            self.plaintext,
        )

    @classmethod
    def lookup_teacher(cls, email: str):
        return cls.query.filter_by(is_teacher=True, parent_email=email).first()


@event.listens_for(User, "after_insert")
def teacher_send_email(mapper, connection, target: User):
    if target.is_teacher:
        target.send_confirmation_email(password=target.plaintext)
        target.send_welcome_email()


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


def create_user(email, username, password):
    u = User()
    u.parent_email = email
    u.username = username
    u.password = hash_password(password)
    u.dob = datetime.now().strftime("%Y-%m-%d")

    db.session.add(u)
    db.session.commit()


def reset_user(username, password):
    u = User.query.filter_by(username=username).first()
    u.password = hash_password(password)

    db.session.commit()


def password_reset_token(user: User) -> str:
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return ts.dumps(user.username, salt="recovery-key")


def reset_password_from_token(token: str, password: str):
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    username = ts.loads(token, salt="recovery-key", max_age=86400)
    reset_user(username, password)


@jwt.user_lookup_loader
def identity(_, jwt_payload):
    return User.query.get(jwt_payload["sub"])


def hash_password(plaintext):
    ph = argon2.PasswordHasher()
    return ph.hash(plaintext)

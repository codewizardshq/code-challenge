import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from application.helpers.serialize import Serialize
from application import db
from null import Null

def sanitize_user(
                    user,
                    raiseonfail = True
                 ):
    if isinstance(user, User):
        pass
    if isinstance(user, (int, float)):
        user = User.query.get(user)
    if isinstance(user, str):
        user = User.query.get(int(user))
    if not isinstance(user, User):
        if raiseonfail:
            raise Exception('Unknown User', str(user))
        else:
            user = None
    return user

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=True)
    password = db.Column(db.String(120), nullable=False))

    def serialize(self):
        return {
            'id': self.id,
            'name': '{} + {}'.format(self.firstname, self.lastname),
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin
        }

    def __repr__(self):
        return '<User %r>' % self.username

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=True)
    answer = db.Column(db.DateTime, nullable=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'answer': self.answer,
            'created': self.created,
            'updated': self.updated
        }

    def __repr__(self):
        return '<Quiz %r>' % self.id


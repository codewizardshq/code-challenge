# from application import db
# from application import
from flask import request
from flask_restplus import Resource
from application.models import Quiz
from application import db
from flask_sqlalchemy import SQLAlchemy
# from application.helpers.serialize import Serialize

from .security import require_auth
from . import api_rest
import ipdb

# db = SQLAlchemy()

# curl -X "GET" -d "{'user':1}" "http://127.0.0.1:5000/api/users"
# curl -X "POST" -d "{'name':'Ricky Bobby'}" "http://127.0.0.1:5000/api/users"
@api_rest.route('/users', methods=['GET', 'POST', 'PUT'])
class Quizzes(Resource):
    def get(self, user=None):
        quiz = db.session.query(Quiz).get(user)
        if quiz:
            return quiz.serialize()
        else:
            return {}

    def post(self, name=None):
        user = User()
        if name:
            user.name = name
        db.session.add(user)
        db.session.commit()
        return user.serialize()

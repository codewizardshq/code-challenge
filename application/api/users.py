# from application import db
# from application import
from flask import request
from flask_restplus import Resource, reqparse, fields
from application.models import User, sanitize_user
from application import db
from flask_sqlalchemy import SQLAlchemy
from .security import require_auth
from . import api_rest
import ipdb
from null import Null


# curl -X GET -H 'Content-Type: application/json' -d "{'user':1}" "http://127.0.0.1:5000/api/users"
# curl -X POST -H 'Content-Type: application/json' -d '{"firstname":"Ricky", "lastname":"Bobby", "username":"rickybobby","email":"ricky@bobby.com"}' 'http://127.0.0.1:5000/api/users'


@api_rest.route('/users', methods=['GET', 'POST', 'PUT'])
class Users(Resource):
    def get(self):
        if api_rest.payload:
            user = self.user_get(**api_rest.payload)
            if user:
                return user.serialize()
            else:
                api_rest.abort(404, "User {} doesn't exist".format(user))
        else:
            api_rest.abort(404, "User not provided")

    def post(self):
        user = self.user_createupdate(**api_rest.payload)
        return user.serialize()

    def user_get(self, user=None):
        if user:
            user = sanitize_user(user)
            return user


    def user_createupdate(self,
                          user      = Null,
                          firstname = Null,
                          lastname  = Null,
                          username  = Null,
                          email     = Null
                         ):
        if user != Null:
            user = sanitize_user(user)
        else:
            user = User()
        if firstname != Null:
            user.firstname = firstname
        if lastname != Null:
            user.lastname = lastname
        if username != Null:
            user.username = username
        if email != Null:
            user.email = email
        # ipdb.set_trace()
        db.session.add(user)
        db.session.commit()
        return user


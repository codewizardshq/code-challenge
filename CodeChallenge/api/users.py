from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_current_user, get_jwt_identity,
                                jwt_refresh_token_required, jwt_required,
                                set_access_cookies, set_refresh_cookies,
                                unset_jwt_cookies)
from flask_limiter.util import get_remote_address
from flask_mail import Message

from ..auth import (Users, hash_password, password_reset_token,
                    reset_password_from_token)
from ..limiter import limiter
from ..mail import mail
from ..models import db

bp = Blueprint("userapi", __name__, url_prefix="/api/v1/users")


def json_error(reason, status=400):
    return jsonify({"status": "error", "reason": reason}), status


@bp.route("/token/auth", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = Users.query.filter_by(email=username).first()
    if user is None or not user.check_password(password):
        return json_error("invalid username or password")

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    res = jsonify({"status": "success"})
    set_access_cookies(res, access_token)
    set_refresh_cookies(res, refresh_token)

    return res, 200


@bp.route("/token/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    u = get_jwt_identity()
    access_token = create_access_token(identity=u)

    res = jsonify({"status": "success"})
    set_access_cookies(res, access_token)

    return res, 200


@bp.route("/token/remove", methods=["POST"])
def logout():
    res = jsonify({"status": "success"})
    unset_jwt_cookies(res)

    return res, 200


@bp.route("/register", methods=["POST"])
def register():

    user_data = request.get_json()
    new_u = Users()

    email = user_data.get("email", None)
    username = user_data.get("username", None)

    if email is None:
        return json_error("email is required")

    if username is None:
        return json_error("username is required")

    password = user_data.get("password", None)

    if password is None or len(password) < 11 or len(password) > 120:
        return json_error("invalid password length (between 11 and 120)")

    if Users.query.filter_by(email=email).first():
        return json_error("that email is already in use")

    if Users.query.filter_by(username=username).first():
        return json_error("that username has been taken")

    new_u.email = user_data['email']
    new_u.username = user_data['username']
    new_u.password = hash_password(password)
    new_u.firstname = user_data['firstname']
    new_u.lastname = user_data['lastname']
    new_u.active = True

    db.session.add(new_u)
    db.session.commit()

    return jsonify({"status": "success"})


@bp.route("/hello", methods=["GET"])
@jwt_required
def hello_protected():
    identity = get_jwt_identity()
    user = get_current_user()

    return jsonify({"status": "success",
                    "message": f"Hello {user.firstname}! (id {identity})",
                    "your_username": user.username,
                    "your_email": user.email})


@bp.route("/forgot", methods=["POST"])
@limiter.limit("3 per hour", key_func=get_remote_address)
def forgot_password():

    data = request.get_json()
    email = data.get("email")
    if email is None:
        return jsonify(status="error", reason="email missing"), 400

    user = Users.query.filter_by(email=email).first()

    if user is None:
        return jsonify(status="error",
                       reason="no account with that email"), 400

    token = password_reset_token(user)

    msg = Message(subject="Password Reset",
                  body="You are receiving this message because a password "
                  "reset request has been issued for your account. If you "
                  "did not make this request, you can ignore this email. "
                  "To reset your password, use this link within 24 hours. "
                  f"https://www.hackcwhq.com/reset-password?token={token}",
                  recipients=[user.email])

    if current_app.config.get("TESTING", False):
        msg.extra_headers = {"X-Password-Reset-Token": token}

    mail.send(msg)

    return jsonify(status="success", reason="password reset email sent")


@bp.route("/reset-password", methods=["POST"])
@limiter.limit("3 per hour", key_func=get_remote_address)
def reset_password():

    data = request.get_json()
    password = data.get("password")
    token = data.get("token")

    if token is None or password is None:
        return json_error("missing token or password")

    if len(password) < 11 and len(password) > 120:
        return json_error("invalid password length (between 11 and 120)")

    try:
        reset_password_from_token(token, password)
    except Exception:
        return json_error("password reset failed")

    return jsonify(status="success", reason="password reset successfully")

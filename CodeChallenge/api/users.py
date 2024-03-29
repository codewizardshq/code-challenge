from flask import (
    Blueprint,
    jsonify,
    request,
    current_app,
    render_template,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from flask_limiter.util import get_remote_address
from flask_mail import Message
from requests import HTTPError

from .. import core
from ..auth import Users, hash_password, password_reset_token, reset_password_from_token
from ..decorators import cors_allow
from ..limiter import limiter
from ..mail import mail
from ..mailgun import mg_validate
from ..models import db

bp = Blueprint("userapi", __name__, url_prefix="/api/v1/users")


def json_error(reason, status=400):
    return jsonify({"status": "error", "reason": reason}), status


@bp.route("/token/auth", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = Users.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return json_error("invalid username or password")

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    res = jsonify({"status": "success"})
    set_access_cookies(res, access_token)
    set_refresh_cookies(res, refresh_token)

    return res, 200


@bp.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
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

    # required fields first

    parent_email = user_data.get("parentEmail", None)
    username = user_data.get("username", None)
    dob = user_data.get("DOB", None)
    password = user_data.get("password", None)

    if parent_email is None:
        return json_error("parent email is required")

    if username is None:
        return json_error("username is required")

    if dob is None:
        return json_error("DOB is required")

    if password is None or len(password) < 8 or len(password) > 120:
        return json_error("invalid password length (between 8 and 120)")

    if Users.query.filter_by(username=username).first():
        return json_error("that username has been taken")

    new_u.parent_email = parent_email
    new_u.username = username
    new_u.password = hash_password(password)

    new_u.parent_first_name = user_data.get("parentFirstName")
    new_u.parent_last_name = user_data.get("parentLastName")
    new_u.student_first_name = user_data.get("studentFirstName")
    new_u.student_last_name = user_data.get("studentLastName")
    new_u.dob = dob
    new_u.student_email = user_data.get("studentEmail", None)
    new_u.found_us = user_data.get("foundUs", None)
    new_u.school_name = user_data.get("school_name", None)

    edit_cookie = request.cookies.get("edit", None)
    if edit_cookie is not None:
        try:
            new_u.cwhq_username = edit_cookie.split(".")[0]
        except IndexError:
            pass

    db.session.add(new_u)
    db.session.commit()

    if current_app.config["MG_LIST"]:
        try:
            new_u.add_to_mailing_list(current_app.config["MG_LIST"])
        except HTTPError as error:
            current_app.logger.exception(
                f"failed to add {new_u} to mailing list: {error}"
            )

    new_u.send_confirmation_email()
    new_u.send_welcome_email()

    return jsonify({"status": "success"})


@bp.route("/hello", methods=["GET"])
@jwt_required()
def hello_protected():
    identity = get_jwt_identity()
    user = get_current_user()

    return jsonify(
        {
            "status": "success",
            "message": f"Hello {user.student_first_name}! (id {identity})",
            "username": user.username,
            "email": user.parent_email,
            "firstname": user.student_first_name,
            "lastname": user.student_last_name,
            "rank": user.rank,
            "timeUntilNextRank": core.time_until_next_rank(),
        }
    )


@bp.route("/forgot", methods=["POST"])
@limiter.limit("3 per hour", key_func=get_remote_address)
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    if email is None:
        return jsonify(status="error", reason="email missing"), 400

    users = Users.query.filter_by(parent_email=email).all()

    if users is None or len(users) == 0:
        return jsonify(status="error", reason="no account with that email"), 400

    multiple_accounts = len(users) > 1

    for user in users:  # type: Users
        token = password_reset_token(user)

        rcpts = [user.parent_email]
        if user.student_email:
            rcpts.append(user.student_email)

        if user.student_first_name:
            name = user.student_first_name
        else:
            name = user.username

        msg = Message(
            subject="Reset your Code Challenge password",
            html=render_template(
                "challenge_password_reset.html",
                name=name,
                token=token,
                multiple=multiple_accounts,
            ),
            recipients=rcpts,
        )

        if current_app.config.get("TESTING", False):
            msg.extra_headers = {"X-Password-Reset-Token": token}

        mail.send(msg)

    return jsonify(
        status="success", reason="password reset email sent", multiple=multiple_accounts
    )


@bp.route("/reset-password", methods=["POST"])
@limiter.limit("10 per hour", key_func=get_remote_address)
def reset_password():
    data = request.get_json()
    password = data.get("password")
    token = data.get("token")

    if token is None or password is None:
        return json_error("missing token or password")

    if 8 > len(password) > 120:
        return json_error("invalid password length (between 8 and 120)")

    try:
        reset_password_from_token(token, password)
    except Exception:
        return json_error("password reset failed")

    return jsonify(status="success", reason="password reset successfully")


@bp.route("/<string:username>/exists", methods=["GET"])
def username_exists(username):
    exists = Users.query.filter_by(username=username).first() is not None
    return jsonify(status="success", exists=exists, username=username)


@bp.route("/validate", methods=["POST"])
def email_validation():
    if "email" not in request.json:
        return jsonify(status="error", reason="missing 'email' field"), 400

    mg_res = mg_validate(request.json["email"])

    return mg_res.json(), mg_res.status_code


@bp.route("/<string:username>/query", methods=["GET", "OPTIONS", "HEAD"])
@cors_allow
def user_query(username):
    user = Users.query.filter_by(cwhq_username=username).first()
    if user:
        response = jsonify(username=user.username, exists=True, rank=user.rank)
    else:
        response = jsonify(exists=False)

    return response


@bp.route("/count")
@cors_allow
def enrollment_count():
    return f"<h1>{core.user_count()} users</h1>", 200

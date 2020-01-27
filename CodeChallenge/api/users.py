from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_current_user, get_jwt_identity,
                                jwt_refresh_token_required, jwt_required,
                                set_access_cookies, set_refresh_cookies,
                                unset_jwt_cookies)
from flask_limiter.util import get_remote_address
from flask_mail import Message

from .. import core
from ..auth import (Users, hash_password, password_reset_token,
                    reset_password_from_token)
from ..limiter import limiter
from ..mail import mail
from ..mailgun import mg_list_add
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

    new_u.parentfirstname = user_data.get("parentFirstName")
    new_u.parentlastname = user_data.get("parentLastName")
    new_u.studentfirstname = user_data.get("studentFirstName")
    new_u.studentlastname = user_data.get("studentLastName")
    new_u.dob = dob
    new_u.student_email = user_data.get("studentEmail", None)

    new_u.active = True

    db.session.add(new_u)
    db.session.commit()

    if current_app.config["MG_LIST"] \
            and current_app.config["MG_PRIVATE_KEY"]:
        # add parent to mailing list
        mg_vars = dict(
            codeChallengeUsername=new_u.username,
            studentEmail=new_u.student_email,
            studentFirstName=new_u.studentfirstname,
            studentLastName=new_u.studentlastname,
            studentName=f"{new_u.studentfirstname} {new_u.studentlastname}",
            parentFirstName=new_u.parentfirstname,
            parentLastName=new_u.parentlastname,
            parentName=f"{new_u.parentfirstname} {new_u.parentlastname}",
            userId=new_u.id,
            studentDOB=new_u.dob,
            type=""
        )

        mg_vars["type"] = "parent"
        mg_list_add(new_u.parent_email,
                    f"{new_u.parentfirstname} {new_u.parentlastname}",
                    data=mg_vars)

        # if provided, also add student to mailing list
        if new_u.student_email:
            mg_vars["type"] = "student"
            mg_list_add(new_u.student_email,
                        f"{new_u.studentfirstname} {new_u.studentlastname}",
                        data=mg_vars)

    return jsonify({"status": "success"})


@bp.route("/hello", methods=["GET"])
@jwt_required
def hello_protected():
    identity = get_jwt_identity()
    user = get_current_user()

    return jsonify({"status": "success",
                    "message": f"Hello {user.studentfirstname}! (id {identity})",
                    "username": user.username,
                    "email": user.parent_email,
                    "firstname": user.studentfirstname,
                    "lastname": user.studentlastname,
                    "rank": user.rank,
                    "timeUntilNextRank": core.time_until_next_rank()})


@bp.route("/forgot", methods=["POST"])
@limiter.limit("3 per hour", key_func=get_remote_address)
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    if email is None:
        return jsonify(status="error", reason="email missing"), 400

    users = Users.query.filter_by(parent_email=email).all()

    if users is None or len(users) == 0:
        return jsonify(status="error",
                       reason="no account with that email"), 400

    for user in users:
        token = password_reset_token(user)
        msg = Message(subject="Password Reset",
                      body="You are receiving this message because a password "
                           "reset request has been issued for your account. If you "
                           "did not make this request, you can ignore this email. "
                           "To reset your password, use this link within 24 hours. "
                           f"\n\n{current_app.config['EXTERNAL_URL']}/reset-password?token={token}"
                           f"\n\nAccount Username: {user.username}",
                      recipients=[user.parent_email])

        if current_app.config.get("TESTING", False):
            msg.extra_headers = {"X-Password-Reset-Token": token}

        if len(users) > 1:
            msg.body += "\n\nNOTICE: Your email address matched multiple " \
                        "student accounts. Double check to make sure you " \
                        "are resetting the intended account, as an email " \
                        "was sent for all matching accounts."

        mail.send(msg)

    return jsonify(status="success", reason="password reset email sent", multiple=len(users) > 1)


@bp.route("/reset-password", methods=["POST"])
@limiter.limit("3 per hour", key_func=get_remote_address)
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

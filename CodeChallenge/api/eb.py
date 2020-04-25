from hmac import compare_digest

import requests
from flask import Blueprint, request, current_app, render_template
from flask_mail import Message

from .. import core
from ..mail import mail

bp = Blueprint("awsebapi", __name__, url_prefix="/api/v1/eb")


# used for ElasticBeanstalk health check
@bp.route("/health", methods=["GET"])
def eb_health_check():
    return "OK", 200


# POST request from an AWS Lambda function once per day
# any daily tasks should be placed here
@bp.route("/worker", methods=["POST"])
def worker():
    try:
        password = request.json["password"]
    except (TypeError, KeyError):
        return "", 400

    if not compare_digest(password,
                          current_app.config["WORKER_PASSWORD"]):
        return "", 401

    # send daily reminder emails only while challenge is active, up until the first day of the final challenge
    if 1 <= core.day_number() <= core.max_rank():
        msg = Message("New code challenge question is unlocked!",
                      sender=current_app.config["MAIL_DEFAULT_SENDER"],
                      recipients=[current_app.config["MG_LIST"]])

        msg.html = render_template("challenge_daily_email.html",
                                   name="%recipient_fname%",
                                   external_url=current_app.config["EXTERNAL_URL"])
        msg.extra_headers = {"List-Unsubscribe": "%unsubscribe_email%"}

        mail.send(msg)

    elif core.challenge_ended():
        # TODO: email everyone individually how many votes they have
        pass

    return "", 200

import hmac
import re
import time

import requests
from flask import Blueprint, request, jsonify, current_app, abort
from sqlalchemy import func

from .. import core
from ..auth import Users
from ..models import db

bp = Blueprint("slackapi", __name__, url_prefix="/api/v1/slack")

CMDRE = re.compile(r"^!([^ ]+)", re.I)


@bp.before_request
def slack_verify():
    ts = request.headers.get("X-Slack-Request-Timestamp")
    secret = bytes(current_app.config.get("SLACK_SIGNING_SECRET"), "utf8")
    body = request.data

    if abs(time.time() - int(ts)) > 60 * 5:
        abort(401)

    sig_basestring = bytes(f"v0:{ts}:", "utf8")
    sig_basestring += body

    my_sig = "v0=" + hmac.new(secret, sig_basestring, digestmod="SHA256").hexdigest()
    slack_sig = request.headers.get("X-Slack-Signature")
    if not hmac.compare_digest(my_sig, slack_sig):
        abort(401)


def post_message(channel, text):
    rv = requests.post("https://slack.com/api/chat.postMessage",
                       headers=dict(
                           Authorization="Bearer " + current_app.config["SLACK_OAUTH_TOKEN"]
                       ),
                       json=dict(
                           channel=channel,
                           text=text
                       ))

    rv.raise_for_status()


def handle_message(text, channel):
    match = CMDRE.search(text)

    if match is None:
        return

    command = match.group(1)

    if command == "status":
        rank = core.current_rank()
        resp = f"*Current Rank:* {rank if rank != -1 else '(challenge not started)'}\n"
        resp += f"*Max Rank:* {core.max_rank()}\n"
        resp += f"*Next Rank:* {core.time_until_next_rank()}\n"
        resp += f"*Total Users:* {core.user_count()}"

        post_message(channel, resp)

    if command == "foundus":
        found_us = db.session.query(Users.found_us,
                                    func.count(Users.found_us)) \
            .group_by(Users.found_us) \
            .order_by(Users.found_us) \
            .all()

        resp = ""
        for row in found_us:
            resp += f"*{row[0]}*: {row[1]}\n"

        post_message(channel, resp)


@bp.route("/event", methods=["POST"])
def slack_event():
    data = request.get_json()

    if "challenge" in data:
        return jsonify(challenge=data["challenge"])

    event = data["event"]
    if event["type"] == "message":
        handle_message(event["text"], event["channel"])

    return "", 200

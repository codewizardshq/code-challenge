from hmac import compare_digest

from flask import Blueprint, request, current_app, render_template
from flask_mail import Message
from ..models import Answer, Question, ranking, next_rank_up
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
        ballot_reminders()

    return "", 200


def make_vote_reminder(answer: Answer) -> Message:
    rcpts = [answer.user.parent_email]
    if answer.user.student_email:
        rcpts.append(answer.user.student_email)

    if answer.user.studentfirstname:
        name = answer.user.studentfirstname
    else:
        name = answer.user.username

    votes, rank = ranking(answer.id)
    up1votes, up1rank = next_rank_up(rank)
    diff = (up1votes - votes) + 1

    msg = Message(
        f"You're rank {rank} in the Dragon Quest!",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=rcpts
    )

    msg.html = render_template("challenge_daily_voting.html",
                               votes=votes,
                               rank=int(rank),
                               name=name,
                               username=answer.user.username,
                               away=diff)

    return msg


def ballot_reminders():
    # email everyone who qualified

    answers = Answer.query \
        .join(Question) \
        .filter(
            Question.rank == core.max_rank(),
            Answer.correct,
            Answer.disqualified.is_(None)
        ) \
        .all()

    for answer in answers:  # type: Answer
        try:
            msg = make_vote_reminder(answer)
        except TypeError:
            continue

        mail.send(msg)

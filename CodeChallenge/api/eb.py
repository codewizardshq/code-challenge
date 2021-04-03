from flask import Blueprint, current_app

from .. import core
from ..mailgun import mg_send
from ..models import Users

bp = Blueprint("awsebapi", __name__, url_prefix="/api/v1/eb")


# used for ElasticBeanstalk health check
@bp.route("/health", methods=["GET"])
def eb_health_check():
    return "OK", 200


@bp.route("/teacher", methods=["POST"])
def teacher_progress():
    """Send daily emails to teachers of their student's progress."""
    teachers = Users.query.filter_by(is_teacher=True).all()

    for teacher in teachers:  # type: Users
        body = teacher.render_progress_report()
        mg_send([teacher.parent_email], "Code Challenge Student Progress", body)

    return "", 200


@bp.route("/daily", methods=["POST"])
def daily_email():
    if current_app.config["DAILY_EMAILS"] and 1 <= core.day_number() <= core.max_rank():
        Users.fire_daily_reminder()
        return "OK", 200
    return "Challenge not active", 200

from flask import Blueprint

from CodeChallenge.decorators import challenge_active
from CodeChallenge.mailgun import mg_send
from CodeChallenge.models import Users

bp = Blueprint("awsebapi", __name__, url_prefix="/api/v1/eb")


# used for ElasticBeanstalk health check
@bp.route("/health", methods=["GET"])
def eb_health_check():
    return "OK", 200


@bp.route("/teacher", methods=["POST"])
@challenge_active
def teacher_progress():
    """Send daily emails to teachers of their student's progress."""
    for teacher in Users.query.filter_by(is_teacher=True).all():  # type: Users
        body = teacher.render_progress_report()
        mg_send([teacher.parent_email], "Code Challenge Student Progress", body)
    return "OK", 200


@bp.route("/daily", methods=["POST"])
@challenge_active
def daily_email():
    Users.fire_daily_reminder()
    return "OK", 200

from flask import Blueprint, abort, jsonify
from flask_jwt_extended import current_user, jwt_required

from CodeChallenge.mailgun import mg_lists
from CodeChallenge.models import Question

bp = Blueprint("adminApi", __name__, url_prefix="/api/v1/admin")


@bp.before_request
@jwt_required()
def require_admin():
    if not current_user.is_admin:
        abort(403)


@bp.route("/lists")
def mailing_lists():
    return jsonify(lists=mg_lists())


@bp.route("/sync", methods=["POST"])
def sync_questions():
    try:
        Question.sync_questions()
    except Exception as e:
        return jsonify(status="error", error=str(e)), 400

    return jsonify(status="success")

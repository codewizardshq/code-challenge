from flask import Blueprint, jsonify, current_app, request, abort
from flask_jwt_extended import jwt_required, get_current_user
from sqlalchemy.exc import IntegrityError

from .. import core
from ..models import Answer, db, Vote, Question

bp = Blueprint("voteapi", __name__, url_prefix="/api/v1/vote")


@bp.before_request
def time_gate():
    if not core.challenge_ended():
        r = jsonify(status="error",
                    reason="voting unavailable until code challenge ends")
        r.status_code = 403
        abort(r)


@bp.route("/check", methods=["GET"])
@jwt_required
def vote_check():
    """time_gate() will override this response if voting
    has not begun"""

    u = get_current_user()
    max_votes = current_app.config["MAX_VOTES"]
    casted = u.casted_votes()
    remaining = max_votes - casted
    votes = [v.id for v in u.votes()]

    return jsonify(status="success",
                   maxVotes=max_votes,
                   castedVotes=casted,
                   remainingVotes=remaining,
                   votes=votes,
                   reason="voting is open")


@bp.route("/ballot", methods=["GET"])
@jwt_required
def get_contestants():
    """Contestants are only qualified if they answered
    the max rank question and the initial answer is correct"""

    try:
        page = int(request.args.get("page", 1))
        per = int(request.args.get("per", 20))
    except ValueError:
        return jsonify(status="error",
                       reason="invalid 'page' or 'per' parameter"), 400

    max_rank = core.max_rank()

    p = Answer.query \
        .join(Answer.question) \
        .filter(Question.rank == max_rank,
                Answer.correct) \
        .paginate(page=page, per_page=per)

    contestants = []
    for ans in p.items:  # type: Answer
        contestants.append(dict(
            id=ans.id,
            text=ans.text,
            numVotes=len(ans.votes),
        ))

    return jsonify(
        items=contestants,
        totalItems=p.total,
        page=p.page,
        totalPages=p.pages,
        hasNext=p.has_next,
        nextNum=p.next_num,
        hasPrev=p.has_prev,
        prevNum=p.prev_num
    )


@bp.route("/<int:answer_id>/cast", methods=["POST"])
@jwt_required
def vote_cast(answer_id: int):
    """Cast a vote on an Answer"""
    u = get_current_user()

    max_rank = core.max_rank()

    ans = Answer.query \
        .join(Answer.question) \
        .filter(Answer.id == answer_id,
                Question.rank == max_rank,
                Answer.correct
                ).first()

    if ans is None:
        return jsonify(status="error",
                       reason="qualifying answer not found"), 400

    if u.casted_votes() == int(current_app.config["MAX_VOTES"]):
        return jsonify(status="error",
                       reason="you already have reached max votes"), 400

    v = Vote()
    v.answer_id = ans.id
    v.user_id = u.id

    try:
        db.session.add(v)
        db.session.commit()
    except IntegrityError:
        return jsonify(status="error",
                       reason="you already voted for that answer"), 400

    return jsonify(status="success",
                   reason="vote has been cast")


@bp.route("/<int:answer_id>/delete", methods=["DELETE"])
@jwt_required
def vote_delete(answer_id: int):
    u = get_current_user()
    v = Vote.query.filter_by(answer_id=answer_id,
                             user_id=u.id).first()
    if v is None:
        return jsonify(status="error",
                       reason="you did not vote for that answer"), 400

    db.session.delete(v)
    db.session.commit()

    return jsonify(status="success",
                   reason="vote successfully deleted")

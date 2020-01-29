from flask import Blueprint, jsonify, current_app, request, abort
from flask_jwt_extended import get_current_user, jwt_optional
from flask_mail import Message
from itsdangerous import URLSafeSerializer

from .. import core
from ..auth import Users
from ..mail import mail
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
def vote_check():
    return jsonify(status="success",
                   reason="voting is open")


@bp.route("/ballot", methods=["GET"])
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

        display = None
        if ans.user.studentfirstname \
                and ans.user.studentlastname:
            display = f"{ans.user.studentfirstname} " \
                      f"{ans.user.studentlastname[0]}."

        contestants.append(dict(
            id=ans.id,
            text=ans.text,
            numVotes=len(ans.votes),
            firstName=ans.user.studentfirstname,
            lastName=ans.user.studentlastname,
            username=ans.user.username,
            display=display
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
@jwt_optional
def vote_cast(answer_id: int):
    """Cast a vote on an Answer"""
    max_rank = core.max_rank()

    ans = Answer.query \
        .join(Answer.question) \
        .filter(Answer.id == answer_id,
                Question.rank == max_rank,
                Answer.correct) \
        .first()

    if ans is None:
        return jsonify(status="error",
                       reason="qualifying answer not found"), 400

    u = get_current_user()  # type: Users
    v = Vote()
    v.answer_id = ans.id

    if u is not None and u.student_email is not None:
        # user as a participant and we have a unique
        # email for this user.
        v.voter_email = u.student_email
        v.confirmed = True

        # delete any existing vote before adding a new one
        delete_votes = Vote.query \
            .filter(Vote.voter_email == v.voter_email) \
            .all()

        for d in delete_votes:
            db.session.delete(d)

    else:
        try:
            v.voter_email = request.json["email"]
        except (TypeError, KeyError):
            return jsonify(status="error",
                           message="no student email defined. an 'email' property "
                                   "is required on the JSON body."), 400

    if v.voter_email is None:
        return jsonify(status="error",
                       reason="voter email required. either log into your "
                              "existing Code Challenge account or provide "
                              "an email address"), 400

    db.session.add(v)
    db.session.commit()

    # only used if the user is not logged in
    if not v.confirmed:
        s = URLSafeSerializer(current_app.config["SECRET_KEY"])
        tok = s.dumps(v.id, "vote-confirmation")

        msg = Message(subject="Vote Confirmation",
                      body="Click the following link to confirm "
                           " your vote. You may only vote once. "
                           f"\n\n{current_app.config['EXTERNAL_URL']}/vote-confirmation?token={tok}",
                      recipients=[v.voter_email])

        if current_app.config.get("TESTING", False):
            msg.extra_headers = {"X-Vote-Confirmation-Token": tok}

        mail.send(msg)

        return jsonify(status="success",
                       reason="email confirmation needed")

    return jsonify(status="success",
                   reason="vote has been cast")


@bp.route("/confirm", methods=["POST"])
def vote_confirm():
    try:
        token = request.json["token"]
    except KeyError:
        return jsonify("'token' missing from JSON body"), 400

    s = URLSafeSerializer(current_app.config["SECRET_KEY"])

    valid, vote_id = s.loads_unsafe(token, "vote-confirmation")

    if not valid:
        return jsonify(status="error",
                       reason="token is not valid"), 400

    v = Vote.query.get(vote_id)
    delete_votes = Vote.query \
        .filter(Vote.voter_email == v.voter_email,
                Vote.id != v.id) \
        .all()

    # delete any other vote that was clicked
    for d in delete_votes:
        db.session.delete(d)

    v.confirmed = True

    db.session.commit()

    return jsonify(status="success",
                   reason="vote confirmed")

from flask import Blueprint, jsonify, current_app, request, abort, render_template
from flask_limiter.util import get_remote_address
from flask_mail import Message
from itsdangerous import URLSafeSerializer
from sqlalchemy import or_, func

from .. import core
from ..limiter import limiter
from ..auth import Users
from ..mail import mail
from ..mailgun import mg_validate
from ..models import Answer, db, Vote, Question, ranking

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
        desc = request.args.get("desc")
    except ValueError:
        return jsonify(status="error",
                       reason="invalid 'page' or 'per' parameter"), 400

    q = Answer.query.with_entities(
        Answer.id,
        Answer.text,
        func.count(Answer.votes),
        Users.studentfirstname,
        Users.studentlastname,
        Users.username,
        func.concat(Users.studentfirstname, func.right(Users.studentlastname, 1))
    ) \
        .join(Answer.question) \
        .join(Answer.user) \
        .outerjoin(Answer.votes) \
        .filter(Question.rank == core.max_rank(), Answer.correct) \
        .group_by(Answer.id)

    if desc is not None:
        q = q.order_by(func.count(Answer.votes).desc())
    else:
        q = q.order_by(Answer.id)

    p = q.paginate(page=page, per_page=per)

    return jsonify(
        items=p.items,
        totalItems=p.total,
        page=p.page,
        totalPages=p.pages,
        hasNext=p.has_next,
        nextNum=p.next_num,
        hasPrev=p.has_prev,
        prevNum=p.prev_num
    )


def normalize_email(email):

    local, domain = email.rsplit("@")

    if domain == "gmail.com":
        local = local.replace(".", "")

    if "+" in local:
        local = local.split("+")[0]

    return local + "@" + domain


@bp.route("/<int:answer_id>/cast", methods=["POST"])
@limiter.limit("4 per day", key_func=get_remote_address)
def vote_cast(answer_id: int):
    """Cast a vote on an Answer"""
    max_rank = core.max_rank()

    ans = Answer.query \
        .join(Answer.question) \
        .filter(Answer.id == answer_id,
                Question.rank == max_rank,
                Answer.correct) \
        .first()

    if ans.disqualified is not None:
        return jsonify(status="error",
                       reason=f"This user was disqualified: {ans.disqualified}"), 400

    if ans is None:
        return jsonify(status="error",
                       reason="qualifying answer not found"), 400

    v = Vote()
    v.confirmed = False
    v.answer_id = ans.id

    try:
        v.voter_email = normalize_email(request.json["email"])
    except (TypeError, KeyError, ValueError):
        return jsonify(status="error",
                       message="no student email defined. an 'email' property "
                               "is required on the JSON body."), 400

    if v.voter_email is None or v.voter_email == "":
        return jsonify(status="error",
                       reason="voter email required"), 400

    # see if you already voted for this
    if Vote.query.filter_by(answer_id=answer_id, voter_email=v.voter_email).all():
        return jsonify(status="error",
                       reason="you already voted for this one."), 400

    try:
        mg_res = mg_validate(v.voter_email)
    except:
        return jsonify(status="error",
                       reason="That email address doesn't pass our validation check.")

    validation = mg_res.json()

    if validation["risk"] in ("high", "medium"):
        return jsonify(status="error",
                       reason="refusing to allow vote: that email is rated as high risk"), 400

    if validation["result"] in ("undeliverable", "unknown"):
        return jsonify(status="error",
                       reason="we can't deliver email to that address"), 400

    db.session.add(v)
    db.session.commit()

    # only used if the user is not logged in
    s = URLSafeSerializer(current_app.config["SECRET_KEY"])
    tok = s.dumps(v.id, "vote-confirmation")

    msg = Message(subject="Vote Confirmation",
                  recipients=[v.voter_email])
    msg.html = render_template("challenge_vote_confirm.html", token=tok)

    if current_app.config.get("TESTING", False):
        msg.extra_headers = {"X-Vote-Confirmation-Token": tok}

    mail.send(msg)

    return jsonify(status="success",
                   reason="email confirmation needed")


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
    if not v:
        return jsonify(status="error",
                       reason="vote not found - try voting again, or contestant may have been disqualified.")

    if v.confirmed:
        return jsonify(status="success",
                       reason="vote already confirmed")

    delete_votes = Vote.query \
        .filter(Vote.voter_email == v.voter_email,
                Vote.id != v.id) \
        .all()

    # delete any other vote that was clicked
    for d in delete_votes:
        db.session.delete(d)

    v.confirmed = True

    db.session.commit()

    msg = Message(subject="Vote confirmation successful!",
                  recipients=[v.voter_email])

    votes, rank = v.ranking()

    msg.html = render_template("challenge_vote_submitted.html",
                               username=v.answer.user.username,
                               votes=int(votes),
                               rank=rank)

    mail.send(msg)

    return jsonify(status="success",
                   reason="vote confirmed")


@bp.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("q")
    try:
        page = int(request.args.get("page", 1))
        per = int(request.args.get("per", 20))
    except ValueError:
        return jsonify(status="error",
                       reason="invalid 'page' or 'per' parameter"), 400

    if keyword is None:
        return jsonify(status="error", reason="missing 'q' parameter"), 400

    keyword = f"%{keyword}%"

    p = Answer.query.with_entities(
        Answer.id,
        Answer.text,
        func.count(Answer.votes),
        Users.studentfirstname,
        Users.studentlastname,
        Users.username,
        func.concat(Users.studentfirstname, func.right(Users.studentlastname, 1))
    ) \
        .join(Answer.question) \
        .join(Answer.user) \
        .outerjoin(Answer.votes) \
        .filter(Question.rank == core.max_rank(), Answer.correct,
                or_(Users.username.ilike(keyword), Users.studentfirstname.ilike(keyword),
                Users.studentlastname.ilike(keyword))) \
        .group_by(Answer.id)\
        .paginate(page=page, per_page=per)

    return jsonify(
        items=p.items,
        totalItems=p.total,
        page=p.page,
        totalPages=p.pages,
        hasNext=p.has_next,
        nextNum=p.next_num,
        hasPrev=p.has_prev,
        prevNum=p.prev_num
    )

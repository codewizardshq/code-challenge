import os
from hashlib import blake2s
from hmac import compare_digest as str_cmp

import requests
from flask import Blueprint, current_app, jsonify, request, redirect, url_for, abort
from flask_jwt_extended import get_current_user, jwt_required

from .. import core
from ..auth import Users
from ..limiter import limiter, user_rank
from ..models import Answer, Question, db
from sqlalchemy import desc

bp = Blueprint("questionsapi", __name__, url_prefix="/api/v1/questions")


def json_error(reason, status=400):
    return jsonify({"status": "error", "reason": reason}, status=status)


@bp.before_request
def end_code_challenge():
    if core.challenge_ended() and request.path != "/api/v1/questions/leaderboard":
        r = jsonify(status="error", reason="code challenge has ended")
        r.status_code = 403
        abort(r)


@bp.route("/rank")
def get_rank():
    return jsonify(
        status="success",
        rank=core.current_rank(),
        maxRank=core.max_rank(),
        timeUntilNextRank=core.time_until_next_rank(),
        startsOn=core.friendly_starts_on(),
    )


@bp.route("/next", methods=["GET"])
@jwt_required()
def next_question():
    """Return next unanswered question up to the max rank"""

    current_rank = core.current_rank()

    if current_rank == -1:
        return (
            jsonify(
                status="error",
                reason="Code Challenge has not started yet",
                timeUntilNextRank=core.time_until_next_rank(),
            ),
            404,
        )

    user = get_current_user()

    if user.rank == current_rank:
        return (
            jsonify(
                status="error",
                reason="no more questions to answer",
                timeUntilNextRank=core.time_until_next_rank(),
            ),
            404,
        )

    rank = user.rank + 1

    if rank > current_rank:
        return jsonify(status="error", reason="problem with rank"), 500

    q = Question.query.filter(Question.rank == rank).first()  # type: Question

    if not q:
        return jsonify(status="error", reason=f"no questions for rank {rank!r}"), 404

    asset = None
    if q.asset:
        asset = q.write_asset()

    return (
        jsonify(
            status="success",
            question=q.title,
            input_type=q.input_type,
            hints=[q.hint1, q.hint2],
            rank=rank,
            asset=asset,
        ),
        200,
    )


def answer_limit_attempts():
    return current_app.config.get("ANSWER_ATTEMPT_LIMIT", "1 per 1 minutes")


@bp.route("/answer", methods=["POST"])
@jwt_required()
@limiter.limit(answer_limit_attempts, key_func=user_rank)
def answer_next_question():
    user = get_current_user()
    if core.current_rank() == user.rank:
        # all questions have been answered up to the current rank
        return (
            jsonify(
                status="error",
                reason="no more questions to answer",
                transition=None,
                correct=False,
            ),
            404,
        )

    next_rank = user.rank + 1
    if next_rank == core.max_rank():
        return redirect(url_for("questionsapi.answer_eval"))

    q = Question.query.filter_by(rank=next_rank).first()  # type: Question

    data = request.get_json()
    text = data["text"]

    try:
        correct = q.check_correct(data["text"])
    except TypeError:
        return jsonify(status="success", correct=False, transition=None)

    if not correct:
        return jsonify(status="success", correct=False, transition=None)

    user.rank += 1

    ans = Answer()
    ans.question_id = q.id
    ans.user_id = user.id

    ans.text = text
    ans.correct = True

    db.session.add(ans)

    transition = q.next_transition()

    db.session.commit()

    return jsonify(
        status="success",
        correct=True,
        transition=transition.serialize() if transition is not None else None,
    )


@bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    """ Returns all past questions and answers for the current user"""

    u = get_current_user()

    qna = []
    for ans in Answer.query.filter_by(user_id=u.id):  # type: Answer

        qna.append(
            dict(
                question=dict(
                    id=ans.question_id, title=ans.question.title, rank=ans.question.rank
                ),
                answered=ans.text,
                correct=ans.correct,
            )
        )

    return jsonify(qna)


@bp.route("/reset", methods=["DELETE"])
@jwt_required()
def reset_all():
    """ Reset rank for the current user """
    if current_app.config["ALLOW_RESET"]:

        u = get_current_user()
        u.rank = 0

        for ans in Answer.query.filter_by(user_id=u.id):  # type: Answer
            db.session.delete(ans)

        db.session.commit()

        return jsonify(status="success", reason="all answers and rank reset")

    return jsonify(status="error", reason="resetting not allowed at this time"), 403


@bp.route("/final", methods=["POST"])
@jwt_required()
def answer_eval():
    user = get_current_user()
    if core.current_rank() == user.rank:
        # all questions have been answered up to the current rank
        return (
            jsonify(
                status="error",
                reason="no more questions to answer",
                rank=user.rank,
                current_rank=core.current_rank(),
            ),
            404,
        )

    next_rank = user.rank + 1
    if next_rank != core.max_rank():
        print(f"user's next rank is {next_rank} but max rank is {core.max_rank()}")
        return (
            jsonify(status="error", reason="you can't answer the final question yet"),
            400,
        )

    q = Question.query.filter_by(rank=next_rank).first()  # type: Question

    try:
        code = request.get_json()["text"]
    except KeyError:
        return (
            jsonify(status="error", reason="missing 'text' property in JSON body"),
            400,
        )

    if q.answer in code:
        return (
            jsonify(
                status="error",
                reason="your solution may not contain the literal answer. you must submit written code to solve for "
                "the answer.",
            ),
            400,
        )

    try:
        language = request.json["language"]
    except KeyError:
        return (
            jsonify(status="error", reason="missing 'language' property in JSON body"),
            400,
        )

    if language not in ("js", "python"):
        return (
            jsonify(
                status="error",
                reason="unsupported language. valid choices are 'js' or 'python'",
            ),
            400,
        )

    # designated output variable for evaluation
    if language == "js":
        code += "\n\nconsole.log(output)"

    r = requests.post(
        current_app.config["SANDBOX_API_URL"], json={"code": code, "language": language}
    )

    if not r.ok:
        if r.status_code >= 500:
            return (
                jsonify(status="error", reason="server side error while evaluating JS"),
                500,
            )

    try:
        eval_data = r.json()
    except ValueError:
        return (
            jsonify(status="error", reason="response from sandbox API was not JSON"),
            500,
        )

    eval_error = eval_data["error"]
    eval_output = str(eval_data["output"]).rstrip()

    # any API error is an automatic failure
    if eval_error:
        return jsonify(
            status="success", correct=False, output=eval_output, js_error=eval_error
        )

    try:
        correct = str_cmp(eval_output, q.answer)
    except TypeError:
        return jsonify(correct=False, status="success")

    if request.json.get("checkOnly", False):
        return jsonify(correct=correct, status="success")

    ans = Answer.query.filter_by(user_id=user.id, question_id=q.id).first()

    if ans is None:
        ans = Answer()
        ans.question_id = q.id
        ans.user_id = user.id
        db.session.add(ans)

    ans.text = code
    ans.correct = correct

    if correct:
        user.rank += 1

    db.session.commit()

    return jsonify(status="success", correct=correct)


@bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    page = request.args.get("page", type=int) or 1
    per = request.args.get("per", type=int) or 20
    q = db.session.query(Users.username, Users.rank).order_by(desc(Users.rank))
    p = q.paginate(page, per_page=per)

    return jsonify(
        items=[{"username": i[0], "rank": i[1]} for i in p.items],
        totalItems=p.total,
        page=p.page,
        totalPages=p.pages,
        hasNext=p.has_next,
        nextNum=p.next_num,
        hasPrev=p.has_prev,
        prevNum=p.prev_num,
    )

import os
from hashlib import blake2s
from hmac import compare_digest as str_cmp

import requests
from flask import Blueprint, current_app, jsonify, request, redirect, url_for
from flask_jwt_extended import get_current_user, jwt_required

from .. import core
from ..limiter import limiter, user_rank
from ..models import Answer, Question, db

bp = Blueprint("questionsapi", __name__, url_prefix="/api/v1/questions")


def json_error(reason, status=400):
    return jsonify({"status": "error", "reason": reason}, status=status)


@bp.route("/rank", methods=["GET"])
def get_rank():
    return jsonify(status="success", rank=core.current_rank(),
                   maxRank=core.max_rank(),
                   timeUntilNextRank=core.time_until_next_rank(),
                   startsOn=core.friendly_starts_on())


@bp.route("/next", methods=["GET"])
@jwt_required
def next_question():
    """Return next unanswered question up to the max rank"""

    current_rank = core.current_rank()

    if current_rank == -1:
        return jsonify(status="error", reason="Code Challenge has not started yet",
                       timeUntilNextRank=core.time_until_next_rank()), 404

    user = get_current_user()

    if user.rank == current_rank:
        return jsonify(status="error",
                       reason="no more questions to answer",
                       timeUntilNextRank=core.time_until_next_rank()), 404

    rank = user.rank + 1

    if rank > current_rank:
        return jsonify(status="error",
                       reason="problem with rank"), 500

    q = Question.query.filter(Question.rank == rank).first()

    if not q:
        return jsonify(status="error",
                       reason=f"no questions for rank {rank!r}"), 404

    # make filename less predictable
    data = bytes(current_app.config["SECRET_KEY"] + str(q.rank), "ascii")
    filename = blake2s(data).hexdigest()

    asset = f"assets/{filename}{q.asset_ext}"
    asset_path = os.path.join(current_app.config["APP_DIR"], asset)

    if not os.path.isfile(asset_path):
        with open(asset_path, "wb") as fhandle:
            fhandle.write(q.asset)

    return jsonify(status="success",
                   question=q.title,
                   rank=rank,
                   asset=asset), 200


def answer_limit_attempts():
    return current_app.config.get("ANSWER_ATTEMPT_LIMIT", "3 per 30 minutes")


@bp.route("/answer", methods=["POST"])
@jwt_required
@limiter.limit(answer_limit_attempts, key_func=user_rank)
def answer_next_question():
    user = get_current_user()
    if core.current_rank() == user.rank:
        # all questions have been answered up to the current rank
        return jsonify({"status": "error",
                        "reason": "no more questions to answer"}), 404

    next_rank = user.rank + 1
    if next_rank == core.max_rank():
        return redirect(url_for("questionsapi.answer_eval"))

    q = Question.query.filter_by(rank=next_rank).first()  # type: Question

    data = request.get_json()
    text = data["text"]
    correct = str_cmp(text, q.answer)

    ans = Answer.query.filter_by(user_id=user.id, question_id=q.id).first()

    if ans is None:
        ans = Answer()
        ans.question_id = q.id
        ans.user_id = user.id
        db.session.add(ans)

    ans.text = text
    ans.correct = correct

    if correct:
        user.rank += 1

    db.session.commit()

    return jsonify({"status": "success", "correct": correct})


@bp.route("/final", methods=["POST"])
@jwt_required
def answer_eval():
    user = get_current_user()
    if core.current_rank() == user.rank:
        # all questions have been answered up to the current rank
        return jsonify(status="error",
                       reason="no more questions to answer",
                       rank=user.rank, current_rank=core.current_rank()), 404

    next_rank = user.rank + 1
    if next_rank != core.max_rank():
        print(f"next rank is {next_rank} but max rank is {core.max_rank()}")
        return jsonify(status="error",
                       reason="you can't answer the final question yet"), 400

    q = Question.query.filter_by(rank=next_rank).first()  # type: Question

    try:
        code = request.get_json()["text"]
    except KeyError:
        return jsonify(status="error",
                       reason="missing 'text' property in JSON body"), 400

    # designated output variable for evaluation
    code += ";output"
    r = requests.post(current_app.config["DUKTAPE_API"], json={"code": code})

    if not r.ok:
        if r.status_code >= 500:
            return jsonify(status="error",
                           reason="server side error while evaluating JS"), 500

    try:
        eval_data = r.json()
    except ValueError:
        return jsonify(status="error",
                       reason="response from duktape API was not JSON"), 500

    eval_error = eval_data["error"]
    eval_output = str(eval_data["output"])

    # any API error is an automatic failure
    if eval_error:
        return jsonify(status="success",
                       correct=False,
                       js_error=eval_error)

    correct = str_cmp(eval_output, q.answer)

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

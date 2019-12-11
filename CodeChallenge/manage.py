import os
import secrets
import shutil

from flask import current_app

from .models import Question, db


def add_question(title, answer, rank, asset) -> Question:

    q = Question.query.filter_by(rank=rank).first()

    if q is not None:
        raise ValueError(f"a question with rank {rank} already exists")

    ext = os.path.splitext(asset)[1]
    asset_dir = os.path.join(current_app.config["APP_DIR"], "assets")

    filename = secrets.token_urlsafe() + ext

    save_path = os.path.join(asset_dir, filename)

    shutil.copyfile(asset, save_path)

    q = Question()
    q.title = title
    q.answer = answer
    q.asset = filename
    q.rank = rank

    db.session.add(q)
    db.session.commit()

    return q


def del_question(question_id):

    q = Question.query.get(question_id)

    if q is None:
        return False

    if q.asset is not None:

        asset_dir = os.path.join(current_app.config["APP_DIR"], "assets")
        filename = os.path.join(asset_dir, q.asset)
        os.remove(filename)

    Question.query.filter_by(id=q.id).delete()

    return True

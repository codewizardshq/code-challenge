import os

from .models import Question, db


def add_question(title, answer, rank, asset, hint1=None, hint2=None) -> Question:

    q = Question.query.filter_by(rank=rank).first()

    if q is not None:
        raise ValueError(f"a question with rank {rank} already exists")

    q = Question()
    q.title = title
    q.answer = answer

    with open(asset, "rb") as fhandle:
        q.asset = fhandle.read()

    q.asset_ext = os.path.splitext(asset)[1]
    q.rank = rank
    q.hint1 = hint1
    q.hint2 = hint2

    db.session.add(q)
    db.session.commit()

    return q


def del_question(question_id):

    q = Question.query.get(question_id)

    if q is None:
        return False

    Question.query.filter_by(id=q.id).delete()

    return True

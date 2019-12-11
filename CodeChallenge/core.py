from datetime import datetime, timezone

from flask import current_app

from .models import Question, db


def current_rank() -> int:
    # yes, datetime has .utcnow() and .utcfromtimestamp() but those methods
    # create timezone unaware objects. this code needs to explicitly operate
    # on UTC time so this forces the timezone to be UTC.

    epoch = int(current_app.config["CODE_CHALLENGE_START"])
    start = datetime.fromtimestamp(epoch, timezone.utc)
    now = datetime.now(timezone.utc)

    if start > now:
        return -1

    delta = now - start

    return 1 if delta.days == 0 else delta.days


def add_question(title: str, asset: str, answer: str, rank: int):

    q = Question()
    q.title = title
    q.answer = answer
    q.rank = rank
    q.asset = asset

    db.session.add(q)
    db.session.commit()

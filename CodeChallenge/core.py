from datetime import datetime, timezone, timedelta, time

from flask import current_app
from sqlalchemy import func

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


def time_until_next_rank() -> str:

    epoch = int(current_app.config["CODE_CHALLENGE_START"])
    start = datetime.fromtimestamp(epoch, timezone.utc)
    now = datetime.now(timezone.utc)

    if start > now:
        diff = datetime.combine(start, time.min, now.tzinfo) - now
        return str(diff)

    tomorrow = now + timedelta(days=1)

    diff = datetime.combine(tomorrow, time.min, now.tzinfo) - now

    return str(diff)


def friendly_starts_on() -> str:
    """Formatted specifically for the landing page countdown jQuery plugin"""
    epoch = int(current_app.config["CODE_CHALLENGE_START"])
    start = datetime.fromtimestamp(epoch, timezone.utc)

    return start.strftime("%m/%d/%Y %H:%M%S UTC")


def max_rank() -> int:
    return db.session.query(func.max(Question.rank)).scalar()

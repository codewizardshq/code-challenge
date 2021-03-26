from datetime import datetime, timezone, timedelta

from flask import current_app
from sqlalchemy import func, not_

from .auth import Users
from .models import Question, db


def max_rank() -> int:
    return db.session.query(func.max(Question.rank)).scalar()


def day_number() -> int:
    epoch = int(current_app.config["CODE_CHALLENGE_START"])
    start = datetime.fromtimestamp(epoch, timezone.utc)
    now = datetime.now(timezone.utc)

    if start > now:
        return -1

    delta = now - start

    return delta.days + 1


def current_rank() -> int:
    # yes, datetime has .utcnow() and .utcfromtimestamp() but those methods
    # create timezone unaware objects. this code needs to explicitly operate
    # on UTC time so this forces the timezone to be UTC.

    day = day_number()
    mr = max_rank()

    if day <= mr:
        return day

    return mr


def time_until_next_rank() -> str:

    epoch = int(current_app.config["CODE_CHALLENGE_START"])
    start = datetime.fromtimestamp(epoch, timezone.utc)
    now = datetime.now(timezone.utc)
    next_date = start + timedelta(days=day_number())
    return str(next_date - now)


def friendly_starts_on() -> str:
    """Formatted specifically for the landing page countdown jQuery plugin"""
    epoch = int(current_app.config["CODE_CHALLENGE_START"])
    start = datetime.fromtimestamp(epoch, timezone.utc)

    return start.strftime("%m/%d/%Y %H:%M%S UTC")


def challenge_ended() -> bool:
    """" Determines if the Code Challenge has ended.  """
    days_past = day_number() - current_rank()
    if days_past >= current_app.config["CHALLENGE_ENDS"]:
        return True

    return False


def user_count() -> int:
    return (
        db.session.query(func.count(Users.id))
        .filter(
            Users.parent_email.notlike("%@codewizardshq.com"), not_(Users.is_teacher)
        )
        .scalar()
    )

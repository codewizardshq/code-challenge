from flask_limiter import Limiter
from flask_jwt_extended import get_current_user

limiter = Limiter()


def user_rank():
    user = get_current_user()
    return f"{user.id}.{user.rank}"

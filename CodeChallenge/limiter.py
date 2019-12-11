from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import get_current_user

limiter = Limiter(key_func=get_remote_address)


def user_rank():
    user = get_current_user()
    return f"{user.id}.{user.rank}"

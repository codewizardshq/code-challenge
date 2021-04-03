from functools import wraps

from flask import request, after_this_request, current_app, make_response

from CodeChallenge import core


def cors_allow(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        @after_this_request
        def add_header(response):
            if "Origin" in request.headers and request.headers["Origin"].endswith(
                ".codewizardshq.com"
            ):
                response.headers["Access-Control-Allow-Origin"] = "*"
                response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, HEAD"
                response.headers["Access-Control-Max-Age"] = "2629746"  # one month
            return response

        return f(*args, **kwargs)

    return wrapped


def challenge_active(f):
    """Requires the Code Challenge to be """

    @wraps(f)
    def wrapped(*args, **kwargs):

        if (
            current_app.config["DAILY_EMAILS"]
            and 1 <= core.day_number() <= core.max_rank()
        ):
            return f(*args, **kwargs)
        else:
            return "Challenge not active", 200

    return wrapped

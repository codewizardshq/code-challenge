from functools import wraps

from flask import request


def cors_allow(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        if request.headers["Origin"].endswith(".codewizardshq.com"):
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, HEAD"
            response.headers["Access-Control-Max-Age"] = "2629746"  # one month
        return response

    return wrapped

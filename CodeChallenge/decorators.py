from functools import wraps

from flask import request, after_this_request


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

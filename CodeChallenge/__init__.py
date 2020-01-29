import os
import re

import sentry_sdk
from flask import Flask, jsonify, make_response, send_from_directory
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import import_string

from . import core
from .api.eb import bp as eb_bp
from .api.questions import bp as questions_bp
from .api.users import bp as users_bp
from .api.vote import bp as vote_bp
from .auth import jwt
from .cli.clock import bp as clock_cli_bp
from .cli.db import bp as db_cli_bp
from .cli.questions import bp as q_cli_bp
from .cli.users import bp as users_cli_bp
from .limiter import limiter
from .mail import mail
from .manage import add_question, del_question  # NoQA
from .models import db, init_db  # NoQA

STATIC_FILES = re.compile(r"\.(ico|png|xml|json)$")

# Globally accessible libraries


def create_app(config):
    """Initialize the core application."""
    sentry_dsn = os.getenv("SENTRY_DSN")
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration()]
        )

    app = Flask(__name__)

    # prevent IP spoofing the rate limiter behind a reverse proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

    cfg = import_string(f"CodeChallenge.config.{config}")()
    app.config.from_object(__name__)
    app.config.from_object(cfg)

    # Initialize Plugins
    CORS(app)
    jwt.init_app(app)
    db.init_app(app)  # SQLAlchemy must be loaded before Marshmallow
    limiter.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(eb_bp)
    app.register_blueprint(users_cli_bp)
    app.register_blueprint(db_cli_bp)
    app.register_blueprint(q_cli_bp)
    app.register_blueprint(clock_cli_bp)
    app.register_blueprint(vote_bp)

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return make_response(
            jsonify(
                status="error",
                reason=f"rate limit exceeded ({e.description})"), 429)

    js_dir = os.path.join(app.config["DIST_DIR"], "js")
    css_dir = os.path.join(app.config["DIST_DIR"], "css")
    fonts_dir = os.path.join(app.config["DIST_DIR"], "fonts")
    images_dir = os.path.join(app.config["DIST_DIR"], "images")

    @app.route("/js/<path:path>")
    def send_js(path):
        return send_from_directory(js_dir, path)

    @app.route("/css/<path:path>")
    def send_css(path):
        return send_from_directory(css_dir, path)

    @app.route("/fonts/<path:path>")
    def send_fonts(path):
        return send_from_directory(fonts_dir, path)

    @app.route("/images/<path:path>")
    def send_images(path):
        return send_from_directory(images_dir, path)

    @app.route("/assets/<path:path>")
    def send_assets(path):
        return send_from_directory("assets", path)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):

        if STATIC_FILES.search(path):
            return send_from_directory(app.config["DIST_DIR"], path)

        return send_from_directory(app.config["DIST_DIR"], "index.html")

    return app

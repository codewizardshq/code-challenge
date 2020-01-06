from flask import Flask, jsonify, make_response, send_from_directory
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from .api.eb import bp as eb_bp
from .api.questions import bp as questions_bp
from .api.users import bp as users_bp
from .auth import jwt
from .cli.clock import bp as clock_cli_bp
from .cli.db import bp as db_cli_bp
from .cli.questions import bp as q_cli_bp
from .cli.users import bp as users_cli_bp
from .limiter import limiter
from .mail import mail
from .manage import add_question, del_question  # NoQA
from .models import db, init_db  # NoQA


# Globally accessible libraries


def create_app(config):
    """Initialize the core application."""

    app = Flask(__name__)

    # prevent IP spoofing the rate limiter behind a reverse proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

    app.config.from_object(__name__)
    app.config.from_object(f"CodeChallenge.config.{config}")

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

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return make_response(
            jsonify(
                status="error",
                reason=f"rate limit exceeded ({e.description})"), 429)

    @app.route("/js/<path:path>")
    def send_js(path):
        return send_from_directory("../dist/js", path)

    @app.route("/css/<path:path>")
    def send_css(path):
        return send_from_directory("../dist/css", path)

    @app.route("/fonts/<path:path>")
    def send_fonts(path):
        return send_from_directory("../dist/fonts", path)

    @app.route("/images/<path:path>")
    def send_images(path):
        return send_from_directory("../dist/images", path)

    @app.route("/assets/<path:path>")
    def send_assets(path):
        return send_from_directory("assets", path)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        return send_from_directory("../dist/", "index.html")

    return app

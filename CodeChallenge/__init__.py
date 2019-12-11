import click
from flask import Flask, jsonify, make_response, send_from_directory
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from .api.eb import bp as eb_bp
from .api.questions import bp as questions_bp
from .api.users import bp as users_bp
from .auth import create_user, jwt, reset_user
from .core import add_question  # NoQA
from .limiter import limiter
from .mail import mail
from .models import db, init_db

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

    # Command Line
    @app.cli.command("initdb")
    def initdb_cmd():
        init_db()
        print("database initialized")

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return make_response(
            jsonify(
                status="error",
                reason=f"rate limit exceeded ({e.description})"), 429)

    # create new user with a password
    @app.cli.command("create-user")
    @click.argument("email")
    @click.argument("password")
    def create_user_cmd(email, password):
        create_user(email, password)
        print("user created")

    # change user's password from their email address
    @app.cli.command("reset-user")
    @click.argument("email")
    @click.argument("password")
    def reset_user_cmd(email, password):
        reset_user(email, password)

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

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        return send_from_directory("../dist/", "index.html")

    return app

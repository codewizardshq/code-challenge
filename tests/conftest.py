import time

import pytest

import CodeChallenge


@pytest.fixture(scope="module")
def app():
    app = CodeChallenge.create_app("DefaultConfig")
    return app


@pytest.fixture(scope="module")
def client(app):

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["MAIL_SUPPRESS_SEND"] = True
    app.config["CODE_CHALLENGE_START"] = time.time()

    with app.test_client() as client:
        with app.app_context():
            CodeChallenge.init_db()
        yield client

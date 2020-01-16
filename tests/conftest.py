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
    app.config["MG_PRIVATE_KEY"] = 'key-e49d7f79a91021260574182a48a482e8'

    with app.test_client() as client:
        with app.app_context():
            CodeChallenge.init_db()
        yield client

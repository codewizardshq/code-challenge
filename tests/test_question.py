from datetime import datetime, timedelta, timezone
import time

import CodeChallenge
import pytest

app = CodeChallenge.create_app("DefaultConfig")


@pytest.fixture(scope="module")
def client_challenge_today():

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["CODE_CHALLENGE_START"] = time.time()

    with app.test_client() as client:
        with app.app_context():
            CodeChallenge.init_db()
            CodeChallenge.add_question("What is 2+2?", None, "4", 1)
            CodeChallenge.add_question("What is Pi?", None, "3.14", 2)
            CodeChallenge.add_question("What is 2 in binary?", None, "10", 3)
        yield client


@pytest.fixture(scope="module")
def client_challenge_future():
    now = datetime.now(timezone.utc)
    future = now + timedelta(days=2)

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["CODE_CHALLENGE_START"] = future.timestamp()

    with app.test_client() as client:
        with app.app_context():
            CodeChallenge.init_db()
        yield client


@pytest.fixture(scope="module")
def client_challenge_past():
    now = datetime.now(timezone.utc)
    past = now - timedelta(days=2)

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["CODE_CHALLENGE_START"] = past.timestamp()

    with app.test_client() as client:
        with app.app_context():
            CodeChallenge.init_db()
        yield client


def register(client, email, username, password, firstname, lastname):

    return client.post("/api/v1/users/register", json=dict(
        username=username, email=email, password=password,
        firstname=firstname, lastname=lastname
    ))


def login(client, email, password):
    return client.post("/api/v1/users/token/auth", json=dict(
        username=email,
        password=password
    ))


# registration only needs to be performed in the first test since all fixtures
# are using sqlite:///:memory:
def test_get_rank_today(client_challenge_today):
    """Code challenge started today so the current rank should be 1"""
    retval = register(client_challenge_today, "sam@codewizardshq.com",
                      "cwhqsam", "supersecurepassword", "Sam", "Hoffman")
    assert retval.status_code == 200

    retval = login(client_challenge_today,
                   "sam@codewizardshq.com",
                   "supersecurepassword")
    assert retval.status_code == 200

    retval = client_challenge_today.get("/api/v1/questions/rank")
    assert retval.status_code == 200
    assert retval.get_json()["rank"] == 1


def test_get_rank_future(client_challenge_future):
    """Code challenge starts in the future so the rank should be -1"""
    retval = login(client_challenge_future,
                   "sam@codewizardshq.com",
                   "supersecurepassword")
    assert retval.status_code == 200

    retval = client_challenge_future.get("/api/v1/questions/rank")
    assert retval.status_code == 200
    assert retval.get_json()["rank"] == -1


def test_get_rank_past(client_challenge_past):
    retval = login(client_challenge_past,
                   "sam@codewizardshq.com",
                   "supersecurepassword")
    assert retval.status_code == 200

    retval = client_challenge_past.get("/api/v1/questions/rank")
    assert retval.status_code == 200
    assert retval.get_json()["rank"] == 2


def test_get_rank1(client_challenge_past):
    retval = client_challenge_past.get("/api/v1/questions/next")
    assert retval.status_code == 200
    assert retval.get_json()["question"] == "What is 2+2?"
    assert retval.get_json()["rank"] == 1


def test_answer_rank1_correctly(client_challenge_past):
    retval = client_challenge_past.post("/api/v1/questions/answer", json=dict(
        text="4"
    ))

    assert retval.status_code == 200
    assert retval.get_json()["correct"] is True


def test_get_rank2(client_challenge_past):
    retval = client_challenge_past.get("/api/v1/questions/next")
    assert retval.status_code == 200
    assert retval.get_json()["question"] == "What is Pi?"
    assert retval.get_json()["rank"] == 2


def test_answer_rank2_incorrectly(client_challenge_past):
    retval = client_challenge_past.post("/api/v1/questions/answer", json=dict(
        text="incorrect"
    ))

    assert retval.status_code == 200
    assert retval.get_json()["correct"] is False


def test_answer_rank2_correctly(client_challenge_past):
    retval = client_challenge_past.post("/api/v1/questions/answer", json=dict(
        text="3.14"
    ))

    assert retval.status_code == 200
    assert retval.get_json()["correct"] is True


def test_get_rank3_404(client_challenge_past):
    retval = client_challenge_past.get("/api/v1/questions/next")
    assert retval.status_code == 404
    assert retval.get_json()["reason"] == "no more questions to answer"


def test_answer_rank3_404(client_challenge_past):
    retval = client_challenge_past.post("/api/v1/questions/answer", json=dict(
        text="10"
    ))

    assert retval.status_code == 404


# the previous test counts as 1 failed attempt at rank
def test_answer_exceed_attempts(client_challenge_past):
    for i in range(5):
        retval = client_challenge_past.post(
            "/api/v1/questions/answer",
            json=dict(text="10")
        )

        if i >= 2:
            assert retval.status_code == 429
        else:
            assert retval.status_code == 404
            assert "X-RateLimit-Remaining" in retval.headers

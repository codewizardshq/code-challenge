import os
import time
from datetime import datetime, timedelta, timezone

import pytest

import CodeChallenge

app = CodeChallenge.create_app("DefaultConfig")

NOW = datetime.now(timezone.utc)

CC_CLOSED = (NOW - timedelta(days=5)).timestamp()
CC_2D_PRIOR = (NOW - timedelta(days=2)).timestamp()
CC_4D_PRIOR = (NOW - timedelta(days=4)).timestamp()
CC_2D_FUTURE = (NOW + timedelta(days=2)).timestamp()


@pytest.fixture(scope="module")
def client_challenge_today():

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["CODE_CHALLENGE_START"] = time.time()
    app.config["ALLOW_RESET"] = True

    with app.test_client() as client:
        with app.app_context():
            CodeChallenge.init_db()
            CodeChallenge.add_question("What is 2+2?",
                                       "4", 1, "tests/2plus2.jpg")
            CodeChallenge.add_question("What is Pi?",
                                       "3.14", 2, "tests/2plus2.jpg")
            CodeChallenge.add_question("What is 2 in binary?",
                                       "10", 3, "tests/2plus2.jpg")
            CodeChallenge.add_question("Create a variable in JS with "
                                       "the value 10.",
                                       "10", 4, "tests/2plus2.jpg")
        yield client

        with app.app_context():
            CodeChallenge.del_question(1)
            CodeChallenge.del_question(2)
            CodeChallenge.del_question(3)


@pytest.fixture(scope="module")
def client_challenge_future():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["CODE_CHALLENGE_START"] = CC_2D_FUTURE

    with app.test_client() as client:
        with app.app_context():
            CodeChallenge.init_db()
        yield client


@pytest.fixture(scope="module")
def client_challenge_past():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["CODE_CHALLENGE_START"] = CC_2D_PRIOR

    with app.test_client() as client:
        with app.app_context():
            CodeChallenge.init_db()
        yield client


@pytest.fixture(scope="module")
def client_challenge_lastq():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["CODE_CHALLENGE_START"] = CC_4D_PRIOR

    with app.test_client() as client:
        with app.app_context():
            CodeChallenge.init_db()
        yield client


def register(client, email, username, password, firstname, lastname):

    return client.post("/api/v1/users/register", json=dict(
        username=username, parentEmail=email, password=password,
        parentFirstName=firstname, parentLastName=lastname, DOB="1994-04-13"
    ), follow_redirects=True)


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
                   "cwhqsam",
                   "supersecurepassword")
    assert retval.status_code == 200

    retval = client_challenge_today.get("/api/v1/questions/rank")
    assert retval.status_code == 200
    assert retval.get_json()["rank"] == 1


def test_get_rank_future(client_challenge_future):
    """Code challenge starts in the future so the rank should be -1"""
    retval = login(client_challenge_future,
                   "cwhqsam",
                   "supersecurepassword")
    assert retval.status_code == 200

    retval = client_challenge_future.get("/api/v1/questions/rank")
    assert retval.status_code == 200
    assert retval.get_json()["rank"] == -1


def test_get_rank_past(client_challenge_past):
    retval = login(client_challenge_past,
                   "cwhqsam",
                   "supersecurepassword")
    assert retval.status_code == 200

    retval = client_challenge_past.get("/api/v1/questions/rank")
    assert retval.status_code == 200
    assert retval.get_json()["rank"] == 2


def test_register_while_open(client_challenge_past):
    retval = register(client_challenge_past,
                      "codechallenge+sam@codewizardshq.com",
                      "cwhqsam2", "supersecurepassword",
                      "Sam", "Hoffman")

    assert retval.status_code == 200

    retval = client_challenge_past.get("/api/v1/questions/rank")
    assert retval.status_code == 200
    json = retval.get_json()
    assert json["rank"] == 2

    retval = client_challenge_past.get("/api/v1/questions/next")
    assert retval.status_code == 200
    assert retval.get_json()["rank"] == 1


def test_get_rank1(client_challenge_past):
    retval = client_challenge_past.get("/api/v1/questions/next")
    assert retval.status_code == 200
    assert retval.get_json()["question"] == "What is 2+2?"
    assert retval.get_json()["rank"] == 1

    retval = client_challenge_past.get("/api/v1/users/hello")
    data = retval.get_json()

    assert retval.status_code == 200
    assert data["rank"] == 0


def test_answer_rank1_correctly(client_challenge_past):
    retval = client_challenge_past.post("/api/v1/questions/answer", json=dict(
        text="4"
    ))

    assert retval.status_code == 200
    assert retval.get_json()["correct"] is True

    # check history
    retval = client_challenge_past.get("/api/v1/questions/history")
    history = retval.get_json()

    assert len(history) == 1
    assert "question" in history[0]
    assert history[0]["answered"] == "4"
    assert history[0]["correct"]

    # check rank
    retval = client_challenge_past.get("/api/v1/users/hello")
    data = retval.get_json()

    assert retval.status_code == 200
    assert data["rank"] == 1


def test_get_rank2(client_challenge_past):
    retval = client_challenge_past.get("/api/v1/questions/next")
    assert retval.status_code == 200
    assert retval.get_json()["question"] == "What is Pi?"
    assert retval.get_json()["rank"] == 2
    assert "asset" in retval.json


def test_answer_rank2_incorrectly(client_challenge_past):
    retval = client_challenge_past.post("/api/v1/questions/answer", json=dict(
        text="incorrect"
    ))

    assert retval.status_code == 200
    assert retval.get_json()["correct"] is False

    retval = client_challenge_past.get("/api/v1/users/hello")
    data = retval.get_json()

    assert retval.status_code == 200
    assert data["rank"] == 1


def test_answer_rank2_correctly(client_challenge_past):
    retval = client_challenge_past.post("/api/v1/questions/answer", json=dict(
        text="3.14"
    ))

    assert retval.status_code == 200
    assert retval.get_json()["correct"] is True

    retval = client_challenge_past.get("/api/v1/users/hello")
    data = retval.get_json()

    assert retval.status_code == 200
    assert data["rank"] == 2


def test_get_rank3_404(client_challenge_past):
    retval = client_challenge_past.get("/api/v1/questions/next")
    assert retval.status_code == 404
    json = retval.get_json()
    assert json["reason"] == "no more questions to answer"
    delta = json["timeUntilNextRank"]
    assert len(delta.split(":")) == 3


def test_answer_rank3_404(client_challenge_past):
    retval = client_challenge_past.post("/api/v1/questions/answer", json=dict(
        text="10"
    ))

    assert retval.status_code == 404


def test_answer_rank3_correctly(client_challenge_lastq):
    login(client_challenge_lastq,
          "cwhqsam",
          "supersecurepassword")

    rv = client_challenge_lastq.post(
        "/api/v1/questions/answer",
        json=dict(text="10")
    )

    assert rv.status_code == 200


def test_answer_exceed_attempts(client_challenge_past):
    for i in range(5):
        retval = client_challenge_past.post(
            "/api/v1/questions/answer",
            json=dict(text="10")
        )

        if i >= 3:
            assert retval.status_code == 429
        else:
            assert retval.status_code == 302
            assert "X-RateLimit-Remaining" in retval.headers


@pytest.mark.skipif(not os.getenv("SANDBOX_API_URL"), reason="envvar SANDBOX_API_URL is not set")
def test_answer_finalq_wrong(client_challenge_lastq):
    login(client_challenge_lastq,
          "cwhqsam",
          "supersecurepassword")

    rv = client_challenge_lastq.post("/api/v1/questions/final", json=dict(
        text="var output; output = 11",
        language="js"
    ))

    assert rv.status_code == 200
    assert rv.json["correct"] is False


@pytest.mark.skipif(not os.getenv("SANDBOX_API_URL"), reason="envvar SANDBOX_API_URL is not set")
def test_answer_finalq_right(client_challenge_lastq):
    login(client_challenge_lastq,
          "cwhqsam",
          "supersecurepassword")

    rv = client_challenge_lastq.post("/api/v1/questions/final", json=dict(
        text="var output; output = 10",
        language="js"
    ))

    assert rv.status_code == 200
    assert rv.json["correct"] is True


def test_leaderboard(client_challenge_past):

    # register a bunch of fake users

    for i in range(50):
        register(client_challenge_past,
                 f"sam{i}@codewizardshq.com",
                 f"cwhq_sam{i}",
                 "supersecure",
                 f"Sam{i}", f"Hoffman{i}")

    rv = client_challenge_past.get("/api/v1/questions/leaderboard?page=1&per=15")
    assert rv.status_code == 200
    assert len(rv.json["items"]) == 15
    assert rv.json["totalPages"] == 4

    item = rv.json["items"].pop()

    assert len(item) == 2
    assert type(item[0]) == str  # username
    assert type(item[1]) == int  # rank




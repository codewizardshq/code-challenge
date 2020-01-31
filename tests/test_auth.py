import CodeChallenge


def register(client, email, username, password, firstname, lastname):

    return client.post("/api/v1/users/register", json=dict(
        username=username, parentEmail=email, password=password,
        parentFirstName=firstname, parentLastName=lastname, DOB="1994-04-13",
        studentFirstName="Sheldon", studentLastName="Hoffman",
        studentEmail="samuelhoffman2@gmail.com"
    ), follow_redirects=True)


def test_registration_success(client):
    with CodeChallenge.mail.record_messages() as outbox:
        retval = register(client, "sam@codewizardshq.com", "cwhqsam",
                          "supersecurepassword", "Sam", "Hoffman")
        assert retval.get_json()["status"] == "success"
        assert len(outbox) == 2
        assert "Sheldon, your account has been created" in outbox[0].html
        assert "Welcome to Defeat the Dragon, Sheldon!" in outbox[1].html


def test_registration_failure_invalid_password(client):
    retval = register(client, "sam@codewizardshq.com", "SamHoffman",
                      "abc", "Sam", "Hoffman")
    assert retval.status_code == 400
    json = retval.get_json()

    assert json["status"] == "error"


def test_registration_username_in_use(client):
    retval = register(client, "sam+codechallenge@codewizardshq.com", "cwhqsam",
                      "supersecurepassword", "Sam", "Hoffman")
    assert retval.status_code == 400
    json = retval.get_json()
    assert json["status"] == "error"


def login(client, username, password):
    return client.post("/api/v1/users/token/auth", json=dict(
        username=username,
        password=password
    ))


def logout(client):
    return client.post("/api/v1/users/token/remove")


def test_login_success(client):
    retval = login(client, "cwhqsam", "supersecurepassword")
    assert retval.status_code == 200


def test_login_failure_bad_pass(client):
    retval = login(client, "cwhqsam", "elemenopee")
    assert retval.status_code != 200


def test_login_failure_bad_email(client):
    retval = login(client, "qwerty", "supersecurepassword")
    assert retval.status_code != 200


def test_jwt_user_loader_success(client):
    login(client, "cwhqsam", "supersecurepassword")
    retval = client.get("/api/v1/users/hello")
    json = retval.get_json()

    assert json["status"] == "success"
    assert json["username"] == "cwhqsam"
    assert json["email"] == "sam@codewizardshq.com"


def test_logout(client):
    logout(client)
    retval = client.get("/api/v1/users/hello")

    assert retval.status_code == 401


def test_forgot_password(client, app):

    with CodeChallenge.mail.record_messages() as outbox:
        retval = client.post("/api/v1/users/forgot", json=dict(
            email="sam@codewizardshq.com"
        ))
        assert retval.status_code == 200

        assert len(outbox) == 1
        msg = outbox[0]

        assert "X-Password-Reset-Token" in msg.extra_headers
        token = msg.extra_headers["X-Password-Reset-Token"]

        retval = client.post("/api/v1/users/reset-password", json=dict(
            token=token,
            password="evenmoresecurepassword"
        ))

        assert retval.status_code == 200


def test_user_exists(client):

    rv = client.get("/api/v1/users/cwhqsam/exists")
    assert rv.status_code == 200
    assert rv.json["exists"] is True
    assert rv.json["username"] == "cwhqsam"

    rv2 = client.get("/api/v1/users/foobar/exists")
    assert rv2.status_code == 200
    assert rv2.json["username"] == "foobar"
    assert rv2.json["exists"] is False

import json
from typing import List, Tuple, Optional

import requests
from flask import current_app, render_template


def __auth():
    return "api", current_app.config["MG_PRIVATE_KEY"]


def mg_list_add(email_address, name, data=None):
    """Add user to the configured Mailgun List"""
    list_name = current_app.config["MG_LIST"]

    if data is None:
        data = {}

    r = requests.post(
        f"https://api.mailgun.net/v3/lists/{list_name}/members",
        auth=__auth(),
        data=dict(
            subscribed=True,
            address=email_address,
            name=name,
            description="added from CodeChallenge registration",
            upsert=True,
            vars=json.dumps(data),
        ),
    )

    r.raise_for_status()
    return r


def mg_list_delete(list_address: str):
    """Delete the given Mailing List name from Mailgun."""
    response = requests.delete(
        f"https://api.mailgun.net/v3/lists/{list_address}",
        auth=__auth(),
    )

    if not response.ok and response.status_code != 404:
        response.raise_for_status()


def mg_validate(email_address):
    r = requests.get(
        "https://api.mailgun.net/v4/address/validate",
        auth=__auth(),
        params={"address": email_address},
    )

    r.raise_for_status()

    return r


File = Tuple[str, bytes]
Attachment = Tuple[str, File]
FileAttachments = List[Attachment]


def mg_send(
    to: List[str],
    subject: str,
    body: str,
    headers: dict = None,
    from_: str = None,
    attachments: FileAttachments = None,
) -> Optional[requests.Response]:
    data = {
        "from": from_,
        "to": to,
        "subject": subject,
        "html": body,
        "o:tracking": False,
        "o:tag": ["code-challenge"],
    }

    if current_app.config["TESTING"]:
        data["to"] = [current_app.config["TEST_EMAIL_RECIPIENT"]]

    if from_ is None:
        data["from"] = current_app.config["MAIL_DEFAULT_SENDER"]

    if headers is not None:
        for k, v in headers.items():
            data[f"h:{k}"] = v

    if current_app.config["MAIL_SUPPRESS_SEND"]:
        return None

    r = requests.post(
        "https://api.mailgun.net/v3/school.codewizardshq.com/messages",
        auth=__auth(),
        data=data,
        files=attachments,
    )

    r.raise_for_status()

    return r


def email_template(
    to: List[str], subject: str, template_name: str, **kwargs
) -> requests.Response:
    """Render an email template by name with the given context and send the body via Mailgun
    :param to: list of recipient email addresses
    :param subject: email subject
    :param template_name: relative HTML template name
    :param kwargs: values to pass to render_template()
    :return: Mailgun Response
    """
    body = render_template(template_name, **kwargs)
    return mg_send(to, subject, body)


def make_attachment(filename: str, data: bytes) -> Attachment:
    return "attachment", (filename, data)


def is_deliverable(email: str) -> bool:
    response = mg_validate(email)
    response.raise_for_status()
    return response.json()["result"] == "deliverable"


class UndeliverableEmail(Exception):
    pass


def raise_undeliverable(email: str):
    if not is_deliverable(email):
        raise UndeliverableEmail(email)


def mg_lists():
    """Fetch all Mailgun Mailing Lists."""
    response = requests.get(
        "https://api.mailgun.net/v3/lists/pages",
        auth=__auth(),
    )

    response.raise_for_status()

    return response.json()["items"]


def mg_bulk_add(list_name: str, users: list):
    response = requests.post(
        f"https://api.mailgun.net/v3/lists/{list_name}/members.json",
        auth=__auth(),
        data={"upsert": True, "members": json.dumps(users)},
    )
    response.raise_for_status()
    return response.json()


def mg_create_list(list_name: str):
    response = requests.post(
        "https://api.mailgun.net/v3/lists",
        auth=__auth(),
        data={"address": list_name, "description": "Code Challenge Participants"},
    )
    response.raise_for_status()
    return response.json()

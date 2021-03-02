import json
from typing import List

import requests
from flask import current_app, render_template


def __auth():
    return "api", current_app.config["MG_PRIVATE_KEY"]


def mg_list_add(email_address, name, data=None):
    """Add user to the configured Mailgun List"""
    list_name = current_app.config["MG_LIST"]

    if data is None:
        data = {}

    r = requests.post(f"https://api.mailgun.net/v3/lists/{list_name}/members",
                      auth=__auth(),
                      data=dict(
                          subscribed=True,
                          address=email_address,
                          name=name,
                          description="added from CodeChallenge registration",
                          upsert=True,
                          vars=json.dumps(data)
                      ))

    r.raise_for_status()
    return r


def mg_validate(email_address):
    r = requests.get(
        "https://api.mailgun.net/v4/address/validate",
        auth=__auth(),
        params={"address": email_address})

    r.raise_for_status()

    return r


def mg_send(to: List[str], subject: str, body: str, headers: dict = None) -> requests.Response:
    data = {
        "from": current_app.config["MAIL_DEFAULT_SENDER"],
        "to": to,
        "subject": subject,
        "html": body,
        "o:tracking": False,
        "o:tag": ["code-challenge"]
    }

    for k, v in headers.items():
        data[f"h:{k}"] = v

    r = requests.post(
        "https://api.mailgun.net/v3/school.codewizardshq.com/messages",
        auth=__auth(),
        data=data
    )

    r.raise_for_status()

    return r


def email_template(to: List[str], subject: str, template_name: str, **kwargs) -> requests.Response:
    """Render an email template by name with the given context and send the body via Mailgun
    :param to: list of recipient email addresses
    :param subject: email subject
    :param template_name: relative HTML template name
    :param kwargs: values to pass to render_template()
    :return: Mailgun Response
    """
    body = render_template(template_name, **kwargs)
    return mg_send(to, subject, body)

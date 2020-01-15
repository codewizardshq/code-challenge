import json

import requests
from flask import current_app


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


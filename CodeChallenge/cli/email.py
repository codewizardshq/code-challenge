import os.path

import click
from flask import Blueprint, current_app, render_template
from flask_mail import Message
from jinja2 import Environment, FileSystemLoader, meta

from ..mail import mail
from ..api.eb import make_vote_reminder, ballot_reminders
from ..models import Answer, Question
from ..auth import Users

bp = Blueprint("emailcli", __name__, cli_group="email")


def get_template_variables(filename):
    path = os.path.join(current_app.root_path, "templates")
    env = Environment(loader=FileSystemLoader(path))
    template_source = env.loader.get_source(env, filename)[0]
    parsed_content = env.parse(template_source)

    return meta.find_undeclared_variables(parsed_content)


@bp.cli.command("send")
@click.argument("to")
@click.argument("subject")
@click.argument("template")
def email_send(to, subject, template):
    msg = Message(subject=subject,
                  recipients=[to],
                  sender=current_app.config["MAIL_DEFAULT_SENDER"])
    msg.extra_headers = {"List-Unsubscribe": "%unsubscribe_email%"}

    filled_vars = {}
    for var_name in get_template_variables(template):
        try:
            filled_vars[var_name] = input(f"value for {var_name!r}: ")
        except KeyboardInterrupt:
            click.secho("\nsending canceled", fg="yellow")
            return

    msg.html = render_template(template, **filled_vars)

    mail.send(msg)

    click.secho("message sent", fg="green")


@bp.cli.command("vote-test")
@click.argument("username")
def voter_test(username):
    ans = Answer.query \
        .join(Answer.user) \
        .join(Answer.question) \
        .filter(
            Users.username == username,
            Question.rank == 22,
            Answer.correct
        ).first()

    if ans is None:
        click.secho("no answer found for that user", fg="red")
        return

    msg = make_vote_reminder(ans)
    print(msg.html)


@bp.cli.command("send-daily-votes")
def send_daily_votes():
    ballot_reminders()

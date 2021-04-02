import os.path

import click
from flask import Blueprint, current_app, render_template
from flask_mail import Message
from jinja2 import Environment, FileSystemLoader, meta
from CodeChallenge.mailgun import mg_list_delete, mg_bulk_add, mg_create_list
from CodeChallenge.models import Users
from ..mail import mail

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
    msg = Message(
        subject=subject,
        recipients=[to],
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
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


@bp.cli.command("build-list")
def build_mg_list():
    list_name = current_app.config["MG_LIST"]

    if list_name is None:
        click.secho("MG_LIST not set in config", fg="red", err=True)
        return

    page = 0
    size = 500

    click.secho(f"(re)creating list: {list_name}", fg="blue")

    try:
        mg_list_delete(list_name)
        mg_create_list(list_name)
    except Exception as e:
        click.secho(f"list recreation failed: {str(e)}", err=True, fg="red")
        return

    while True:
        offset = page * size
        click.secho(f"loading page {page} offset {offset}", fg="blue")

        click.secho(f"generating recipient-variables", fg="blue")
        members = []
        for user in Users.query.limit(size).offset(offset).all():
            members.extend(user.mg_member())

        click.secho(f"uploading batch to Mailgun")
        click.secho(str(mg_bulk_add(list_name, members)), fg="magenta")

        if len(members) < size:
            click.secho("no more pages to load", fg="yellow")
            break

        page += 1

    click.secho("Done", fg="green")

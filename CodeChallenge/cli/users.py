import click
from flask import Blueprint

from CodeChallenge.core import user_count
from ..auth import create_user, reset_user

bp = Blueprint("usercli", __name__, cli_group="users")


# create new user with a password
@bp.cli.command("create")
@click.argument("email")
@click.argument("username")
@click.argument("password")
def create_user_cmd(email, username, password):
    """Create a new user with an email and password for logging in."""
    create_user(email, username, password)
    print("user created")


# change user's password from their email address
@bp.cli.command("reset")
@click.argument("username")
def reset_user_cmd(username):
    """Manually reset a user's password."""
    password = click.prompt(
        "Enter new password", hide_input=True, confirmation_prompt=True
    )
    reset_user(username, password)


@bp.cli.command("count")
def user_count_cmd():
    click.echo(user_count())

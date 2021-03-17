import click
from flask import Blueprint

from CodeChallenge.models.user import create_user, reset_user

bp = Blueprint("user_cli", __name__, cli_group="users")


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
@click.argument("email")
@click.argument("password")
def reset_user_cmd(email, password):
    """Manually reset a user's password."""
    reset_user(email, password)

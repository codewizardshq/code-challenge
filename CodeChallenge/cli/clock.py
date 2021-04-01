import os
from datetime import datetime, timezone, timedelta

import click
import dotenv
from flask import Blueprint

from CodeChallenge import core

bp = Blueprint("clockcli", __name__, cli_group="clock")


def get_current_start():

    if not dotenv.load_dotenv(".flaskenv"):
        click.secho(".flaskenv file not found", fg="red")
        return

    current = os.getenv("CODE_CHALLENGE_START")

    if current is None:
        click.secho(
            "CODE_CHALLENGE_START is not set in .flaskenv. cannot add a day", fg="red"
        )
        return

    epoch = int(current)
    start = datetime.fromtimestamp(epoch, timezone.utc)

    return start


@bp.cli.command("set-rank")
@click.argument("rank", type=int)
def set_rank(rank):
    """Set CODE_CHALLENGE_START according to the desired rank."""
    max_rank = core.max_rank()
    if rank >= max_rank:
        click.secho(
            f"The rank cannot be set that high. The max rank is {max_rank}",
            err=True,
            color="red",
        )
        return
    ts = datetime.now() - timedelta(days=rank)

    click.secho(f"setting CODE_CHALLENGE_START={ts.timestamp()} ({ts})", fg="green")
    dotenv.set_key(".flaskenv", "CODE_CHALLENGE_START", str(int(ts.timestamp())))


@bp.cli.command("add-day")
def clock_add_day():

    start = get_current_start()

    start += timedelta(days=1)
    ts = str(int(start.timestamp()))
    dotenv.set_key(".flaskenv", "CODE_CHALLENGE_START", ts)

    click.secho(f"start date adjusted to {start}", fg="green")


@bp.cli.command("sub-day")
def clock_sub_day():

    start = get_current_start()

    start -= timedelta(days=1)

    ts = str(int(start.timestamp()))
    dotenv.set_key(".flaskenv", "CODE_CHALLENGE_START", ts)

    click.secho(f"start date adjusted to {start}", fg="green")


@bp.cli.command("set")
@click.argument("datestr")
@click.argument("timestr")
def clock_set(datestr, timestr):

    """Set CODE_CHALLENGE_START to a specific datetime.
    The date and time will be interpreted as UTC time

    The required date format is: YYYY-MM-DD HH:MM

    Example: flask clock set 2020-02-01 08:00"""

    try:
        start = datetime.strptime(f"{datestr} {timestr}", "%Y-%m-%d %H:%M")
    except ValueError:
        click.secho(
            "invalid date/time format.  format must be: YYYY-MM-DD HH:MM", fg="red"
        )
        return

    ts = str(int(start.timestamp()))
    dotenv.set_key(".flaskenv", "CODE_CHALLENGE_START", ts)

    click.secho(f"start date set to {start} ({ts})", fg="green")

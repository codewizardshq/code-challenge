from flask import Blueprint
from ..models import init_db

bp = Blueprint("dbcli", __name__, cli_group="db")


@bp.cli.command("init")
def initdb_cmd():
    """Create schema in database as defined in models.py"""
    init_db()
    print("database initialized")

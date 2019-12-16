from flask import Blueprint
from ..models import init_db, drop_all

bp = Blueprint("dbcli", __name__, cli_group="db")


@bp.cli.command("init")
def initdb_cmd():
    """Create schema in database as defined in models.py"""
    init_db()
    print("database initialized")


@bp.cli.command("dropall")
def dropall_cmd():
    """Drop all tables, deleting all data"""
    drop_all()
    print("all tables dropped")

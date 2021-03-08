from flask import Blueprint

from .. import core
from ..models import init_db, drop_all, BulkImport, db

import click

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


@bp.cli.command("doc-fetch")
@click.argument("doc_id")
def doc_fetch(doc_id: int) -> None:
    """Export the document column for a given BulkImport.id. Output file is
    saved in the current working directory as Bulk-Import-{id}.xlsx."""
    b = BulkImport.query.get(doc_id)  # type: BulkImport

    if b is None:
        click.secho("no such ID", color="red", err=True)
        return

    with open(f"Bulk-Import-{doc_id}.xlsx", "wb") as fd:
        fd.write(b.document)


@bp.cli.command("doc-import")
@click.argument("doc_id")
@click.argument("filename")
def doc_import(doc_id: int, filename: str) -> None:
    """Import an Excel spreadsheet to an existing BulkImport row, overwriting it's contents."""
    b = BulkImport.query.get(doc_id)  # type: BulkImport

    if b is None:
        click.secho("no such ID", color="red", err=True)
        return

    if not click.confirm("Are you sure you want to over-write this import?"):
        return

    with open(filename, "rb") as fd:
        b.document = fd.read()

    db.session.commit()


@bp.cli.command("run-import")
@click.argument("doc_id")
def run_import(doc_id: int):
    b = BulkImport.query.get(doc_id)  # type: BulkImport

    if b is None:
        click.secho("no such ID", color="red", err=True)
        return

    b.run_import()


@bp.cli.command("user-count")
def user_count():
    click.echo(core.user_count())

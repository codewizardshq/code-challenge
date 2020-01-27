import csv
import os.path
from io import StringIO, BytesIO

import click
import requests
from flask import Blueprint, current_app
from tabulate import tabulate

from ..manage import add_question, del_question
from ..models import Question, db

bp = Blueprint("questioncl", __name__, cli_group="q")


@bp.cli.command("add")
@click.argument("title")
@click.argument("answer")
@click.argument("rank")
@click.argument("asset")
def q_add(title, answer, rank, asset):
    """Add a new question to the database

    TITLE is the text for the title of the question
    ANSWER is the answer stored only in the database
    RANK is the day rank the queestion should be revealed on
    ASSET is a path to a file to upload for a question
    """

    asset = os.path.abspath(asset)
    qid = add_question(title, answer, rank, asset)

    click.echo(f"added question id {qid}")


@bp.cli.command("ls")
@click.option("--tablefmt", default="simple")
def q_ls(tablefmt):
    """List all questions in the database"""
    table = []

    for q in Question.query.all():  # type: Question
        table.append((q.id, q.title, q.answer, q.rank, f"{len(q.asset)} length blob", q.asset_ext))

    click.echo(tabulate(table,
                        ("id", "title", "answer", "rank", "asset", "asset_ext"),
                        tablefmt=tablefmt))

    if not table:
        click.echo("no questions in table")


@bp.cli.command("del")
@click.argument("qid")
def q_del(qid):
    """Delete a question by its ID (not rank)"""
    success = del_question(qid)
    if success:
        click.echo("question deleted")
    else:
        click.echo("-!- question not deleted")


@bp.cli.command("replace")
@click.argument("title")
@click.argument("answer")
@click.argument("rank")
@click.argument("asset")
def q_replace(title, answer, rank, asset):
    """Replace an existing rank's question.

    This basically deletes the previous rank then adds the new rank
    """
    oldq = Question.query.filter_by(rank=rank).first()

    if oldq is not None:
        success = del_question(oldq.id)

        if not success:
            print("error occurred while trying to delete original question")
            print(f"old question id was: {oldq.id}")
            return
    else:
        print(f"warning: there was no question for rank {rank} but I added "
              "that question anyway")

    add_question(title, answer, rank, asset)


@bp.cli.command("sync")
def q_sync():
    """Sync with a public Google Sheets Spreadsheet"""

    key = current_app.config.get("GOOGLE_API_KEY")
    file_id = current_app.config.get("SHEET_ID")

    if not key:
        click.secho("missing GOOGLE_API_KEY in config.py", fg="red")
        return

    if not file_id:
        click.secho("missing SHEET_ID in config.py", fg="red")
        return

    r = requests.get(f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=text%2Fcsv&key={key}')

    if not r.ok:
        click.secho(f"sheet download failed (status code {r.status_code})", fg="red")
        click.echo(r.text)
        return

    reader = csv.DictReader(StringIO(r.text))
    rows = list(reader)
    errors = []

    with click.progressbar(rows, label="synchronizing with CSV data ...") as bar:
        for i, row in enumerate(bar):

            if not all((row["rank"], row["title"],
                        row["answer"], row["asset"])):
                errors.append(f"invalid row {i} (missing rank/title/answer/asset)")
                continue

            try:
                rank = int(row["rank"])
            except ValueError:
                errors.append(f"invalid integer value for 'rank' column on row {i}")
                continue

            if not row["asset"].startswith("http"):
                errors.append(f"invalid asset URL on row {i}")

            q = Question.query.filter_by(rank=rank).first()

            if q is None:
                q = Question()
                q.rank = rank
                db.session.add(q)

            q.title = row["title"]
            q.answer = row["answer"]
            q.hint1 = row["hint1"]
            q.hint2 = row["hint2"]

            b = BytesIO()
            r2 = requests.get(row["asset"], stream=True)
            if not r2.ok:
                errors.append(f"failed to download asset for row {i+1}: {row['asset']}")
                return

            for chunk in r2.iter_content(1024):
                b.write(chunk)

            q.asset = b.getvalue()
            content_type = r2.headers.get("content-type")
            if "/" in content_type:
                q.asset_ext = "." + content_type.split("/")[1]
            else:
                errors.append(f"unknown content type for asset on rank {rank}. 'asset_ext' column will need to be set " 
                              f"manually in table. (Content-Type: {r2.headers['content-type']!r})")

    for message in errors:
        click.secho(message, fg="red")

    db.session.commit()

    click.secho("sync complete", fg="green")

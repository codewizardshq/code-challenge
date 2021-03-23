import csv
import os.path
from io import StringIO, BytesIO

import click
import requests
from flask import Blueprint, current_app
from tabulate import tabulate

from ..manage import add_question, del_question
from ..models import Question, db

bp = Blueprint("question_cli", __name__, cli_group="q")


@bp.cli.command("add")
@click.argument("title")
@click.argument("answer")
@click.argument("rank")
@click.argument("asset")
@click.argument("hint1")
@click.argument("hint2")
def q_add(title, answer, rank, asset, hint1, hint2):
    """Add a new question to the database

    TITLE is the text for the title of the question
    ANSWER is the answer stored only in the database
    RANK is the day rank the queestion should be revealed on
    ASSET is a path to a file to upload for a question
    HINT1 is a hint string
    HINT2 is a hint string
    """

    asset = os.path.abspath(asset)
    qid = add_question(title, answer, rank, asset, hint1, hint2)

    click.echo(f"added question id {qid}")


@bp.cli.command("ls")
@click.option("--tablefmt", default="simple")
def q_ls(tablefmt):
    """List all questions in the database"""
    table = []

    for q in Question.query.all():  # type: Question
        table.append(
            (
                q.id,
                q.title,
                q.answer,
                q.rank,
                f"{len(q.asset)} length blob",
                q.asset_ext,
            )
        )

    click.echo(
        tabulate(
            table,
            ("id", "title", "answer", "rank", "asset", "asset_ext"),
            tablefmt=tablefmt,
        )
    )

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
@click.argument("hint1")
@click.argument("hint2")
def q_replace(title, answer, rank, asset, hint1, hint2):
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
        print(
            f"warning: there was no question for rank {rank} but I added "
            "that question anyway"
        )

    add_question(title, answer, rank, asset)


@bp.cli.command("sync")
def q_sync():
    """Sync with a public Google Sheets Spreadsheet"""

    click.confirm(
        "Are you sure you want to sync with the current database? "
        f"({db.engine.url.username}@{db.engine.url.host}/{db.engine.url.database})",
        abort=True,
    )

    key = current_app.config.get("GOOGLE_API_KEY")
    file_id = current_app.config.get("SHEET_ID")

    if not key:
        click.secho("missing GOOGLE_API_KEY in config.py", fg="red")
        return

    if not file_id:
        click.secho("missing SHEET_ID in config.py", fg="red")
        return

    r = requests.get(
        f"https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=text%2Fcsv&key={key}"
    )

    if not r.ok:
        click.secho(f"sheet download failed (status code {r.status_code})", fg="red")
        click.echo(r.text)
        return

    reader = csv.DictReader(StringIO(r.text))
    rows = list(reader)
    errors = []

    with click.progressbar(rows, label="synchronizing with CSV data ...") as bar:
        for i, row in enumerate(bar):
            if not all(
                (
                    row["#"],
                    row["Question"],
                    row["Answer Type"],
                    row["Answer Input"],
                    row["Answer"],
                )
            ):
                errors.append(f"invalid row {i} (required column missing) {row!r}")
                continue

            try:
                rank = int(row["#"])
            except ValueError:
                errors.append(f"invalid integer value for '#' column on row {i}")
                continue

            if "asset" in row and row["asset"].startswith("http"):
                errors.append(f"invalid asset URL on row {i}")

            q = Question.query.filter_by(rank=rank).first()

            if q is None:
                q = Question()
                q.rank = rank
                db.session.add(q)

            assert row["Answer Type"] in ("strcmp", "regex")
            assert row["Answer Input"] in ("input", "textarea")

            q.title = row["Question"]
            q.answer = row["Answer"]
            q.hint1 = row["Hint 1"]
            q.hint2 = row["Hint 2"]
            q.match_type = (
                Question.MATCH_REGEXP
                if row["Answer Type"] == "regex"
                else Question.MATCH_STRCMP
            )
            q.input_type = (
                Question.INPUT_TEXT_AREA
                if row["Answer Input"] == "textarea"
                else Question.INPUT_TEXT_FIELD
            )

            if "asset" in row:
                b = BytesIO()
                r2 = requests.get(row["asset"], stream=True)
                if not r2.ok:
                    errors.append(
                        f"failed to download asset for row {i}: {row['asset']}"
                    )
                    continue

                for chunk in r2.iter_content(1024):
                    b.write(chunk)

                q.asset = b.getvalue()
                content_type = r2.headers.get("content-type")
                if "/" in content_type:
                    q.asset_ext = "." + content_type.split("/")[1]
                else:
                    errors.append(
                        f"unknown content type for asset on rank {rank}. 'asset_ext' column will need to be set "
                        f"manually in table. (Content-Type: {r2.headers['content-type']!r})"
                    )

    for message in errors:
        click.secho(message, fg="red")

    db.session.commit()

    click.secho("sync complete", fg="green")

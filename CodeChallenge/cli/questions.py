import click
from flask import Blueprint
from tabulate import tabulate

from ..manage import add_question, del_question
from ..models import Question

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

    qid = add_question(title, answer, rank, asset)

    click.echo(f"added question id {qid}")


@bp.cli.command("ls")
@click.option("--tablefmt", default="simple")
def q_ls(tablefmt):
    """List all questions in the database"""
    table = []

    for q in Question.query.all():
        table.append((q.id, q.title, q.answer, q.rank, q.asset))

    click.echo(tabulate(table,
                        ("id", "title", "answer", "rank", "asset"),
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
            print("error occured while trying to delete original question")
            print(f"old question id was: {oldq.id}")
            return
    else:
        print(f"warning: there was no question for rank {rank} but I added "
              "that question anyway")

    add_question(title, answer, rank, asset)

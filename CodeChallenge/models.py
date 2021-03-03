from typing import Tuple, List

from flask import request
from flask_sqlalchemy import SQLAlchemy
from tempfile import NamedTemporaryFile

db = SQLAlchemy()


def init_db():
    db.create_all()


def drop_all():
    db.drop_all()


def ranking(answer_id: int) -> Tuple[int, int]:
    return db.session.execute("""
        select rainv.num_votes, rainv.rank
        from (
                 select @rownum := @rownum + 1 as 'rank',
                        prequery.answer_id,
                        prequery.num_votes
                 from (select @rownum := 0) sqlvars,
                      (select answer_id,
                              count(*) as num_votes
                       from vote
                       group by answer_id
                       order by count(*) desc) prequery
             ) as rainv
        where answer_id = :answer_id
    """, {'answer_id': answer_id}).first()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5000), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    asset = db.Column(db.LargeBinary(length=(2 ** 32) - 1))
    asset_ext = db.Column(db.String(10))
    hint1 = db.Column(db.String(5000))
    hint2 = db.Column(db.String(5000))

    def __repr__(self):
        return '<Question %r>' % self.id


class Answer(db.Model):
    """Tracks a user answering a question"""
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer,
                            db.ForeignKey("question.id", ondelete="cascade"),
                            nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete="cascade"))
    text = db.Column(db.String(2000))
    correct = db.Column(db.Boolean)
    question = db.relationship("Question", lazy=True, uselist=False)
    user = db.relationship("Users", lazy=True, uselist=False)
    votes = db.relationship("Vote", cascade="all,delete",
                            lazy=True, uselist=True)
    disqualified = db.Column(db.String(255))

    def confirmed_votes(self) -> int:
        confirmed = 0
        for vote in self.votes:
            if vote.confirmed:
                confirmed += 1

        return confirmed


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer,
                          db.ForeignKey("answer.id", ondelete="cascade"),
                          nullable=False)
    answer = db.relationship("Answer", lazy=True, uselist=False)
    voter_email = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def existing_vote(email: str) -> bool:
        v = Vote.query.filter_by(voter_email=email).first()
        return v

    def ranking(self):
        return ranking(self.answer.id)


class BulkImport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False, default=1)
    sender = db.Column(db.String(80), nullable=False)
    document = db.Column(db.LargeBinary(length=(2 ** 32) - 1))
    subject = db.Column(db.String(200), nullable=False)
    in_reply_to = db.Column(db.String(200), nullable=False)

    @classmethod
    def from_request_files(cls, sender: str, subject: str, in_reply_to: str) -> List[int]:
        added = []  # type: List[int]
        for attachment in request.files.values():
            if attachment.content_type in (
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel") \
                    or attachment.filename.endswith(".xlsx") or attachment.filename.endswith(".xls"):
                bulk_import = cls()

                bulk_import.sender = sender
                bulk_import.document = attachment.stream.read()
                bulk_import.status = 1
                bulk_import.in_reply_to = in_reply_to
                bulk_import.subject = subject

                db.session.add(bulk_import)
                db.session.flush()
                added.append(bulk_import.id)

        db.session.commit()

        return added

    @classmethod
    def process_imports(cls):
        import pandas as pd

        pending = cls.query.filter_by(status=1)

        rows = []
        for item in pending:  # type: cls
            item.status = 2
            db.session.commit()

            fp = NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(item.document)
            fp.flush()
            fp.seek(0)

            df = pd.read_excel(fp.name)
            fp.close()

            rows.extend(df.values.tolist())

        return len(rows)



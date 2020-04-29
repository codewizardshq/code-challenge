from flask_sqlalchemy import SQLAlchemy
from typing import Tuple


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


def next_rank_up(rank: int) -> Tuple[int, int]:
    return db.session.execute("""
        select rainv.num_votes, rainv.rank
        from (
                 select @rownum := @rownum + 1 as 'rank',
                        prequery.num_votes
                 from (select @rownum := 0) sqlvars,
                      (select answer_id,
                              count(*) as num_votes
                       from vote
                       group by answer_id
                       order by count(*) desc) prequery
             ) as rainv
        where rainv.rank = :rank
    """, {'rank': rank - 1}).first()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5000), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    asset = db.Column(db.LargeBinary(length=(2**32)-1))
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


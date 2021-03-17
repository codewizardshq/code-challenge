from typing import Tuple

from CodeChallenge.models.connection import db


def ranking(answer_id: int) -> Tuple[int, int]:
    return db.session.execute(
        """
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
    """,
        {"answer_id": answer_id},
    ).first()


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(
        db.Integer, db.ForeignKey("answer.id", ondelete="cascade"), nullable=False
    )
    answer = db.relationship("Answer", lazy=True, uselist=False)
    voter_email = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def existing_vote(email: str) -> bool:
        v = Vote.query.filter_by(voter_email=email).first()
        return v

    def ranking(self):
        return ranking(self.answer.id)

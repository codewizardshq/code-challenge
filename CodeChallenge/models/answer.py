from CodeChallenge.models.connection import db


class Answer(db.Model):
    """Tracks a user answering a question"""

    id: int = db.Column(db.Integer, primary_key=True)

    question_id: int = db.Column(
        db.Integer, db.ForeignKey("question.id", ondelete="cascade"), nullable=False
    )
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    text: str = db.Column(db.String(2000))
    correct: bool = db.Column(db.Boolean)
    question = db.relationship("Question", lazy=True, uselist=False)
    # user = db.relationship("User", lazy=True, uselist=False, foreign_keys=[user_id])
    votes = db.relationship("Vote", cascade="all,delete", lazy=True, uselist=True)
    disqualified: str = db.Column(db.String(255))

    def confirmed_votes(self) -> int:
        confirmed = 0
        for vote in self.votes:
            if vote.confirmed:
                confirmed += 1

        return confirmed

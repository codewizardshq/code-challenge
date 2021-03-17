from CodeChallenge.models.connection import db
from hmac import compare_digest as str_cmp
import re


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5000), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    asset = db.Column(db.LargeBinary(length=(2 ** 32) - 1))
    asset_ext = db.Column(db.String(10))
    hint1 = db.Column(db.String(5000))
    hint2 = db.Column(db.String(5000))
    match_type = db.Column(db.Integer, nullable=False, default=1)

    MATCH_STRCMP = 1
    MATCH_REGEXP = 2

    def __repr__(self):
        return "<Question %r>" % self.id

    def check_correct(self, answer: str) -> bool:
        if answer is None:
            return False

        if self.match_type == Question.MATCH_STRCMP:
            return str_cmp(answer.casefold().strip(), self.answer.casefold())
        elif self.match_type == Question.MATCH_REGEXP:
            return re.search(self.answer, answer) is not None
        return False

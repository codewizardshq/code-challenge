from CodeChallenge.models import db


class Transition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    after_rank = db.Column(db.Integer, nullable=False)
    asset = db.Column(db.String(500), nullable=False)

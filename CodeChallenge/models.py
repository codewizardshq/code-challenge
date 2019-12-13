from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():
    db.create_all()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5000), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    rank = db.Column(db.Integer, nullable=False) 
    asset = db.Column(db.String(255))

    def __repr__(self):
        return '<Question %r>' % self.id


class Answer(db.Model):
    """Tracks a user answering a question"""
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer,
                            db.ForeignKey("question.id"),
                            nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    text = db.Column(db.String(2000))
    correct = db.Column(db.Boolean)

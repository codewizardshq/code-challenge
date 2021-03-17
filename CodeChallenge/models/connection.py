from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():
    db.create_all()


def drop_all():
    db.drop_all()

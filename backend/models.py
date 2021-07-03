import os
import sys
import time

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.exc import OperationalError
from flask_sqlalchemy import SQLAlchemy

database_name = "trivia"
PG_USER = os.environ.get("POSTGRES_USER")
PG_HOST = os.environ.get("POSTGRES_HOST")
PG_DB = os.environ.get("POSTGRES_DB")
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DB}"

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=DB_URI):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    try:
        db.create_all()
    # If Postgres isn't up, log the Exception and wait a few; the container
    # will restart automatically
    except OperationalError as e:
        print(e, file=sys.stderr)
        print("Waiting on Postgres initialization")
        time.sleep(5)


"""
Question

"""


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


"""
Category

"""


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }

import json
import os
import pdb
import unittest
from flask_sqlalchemy import SQLAlchemy

from trivia import create_app
from models import (
    setup_db,
    PG_USER,
    PG_PASSWORD,
    PG_HOST,
    Category,
    Question
)

TEST_QUESTION = "Who was the first woman to win a Nobel Prize (in 1903)?"
PG_DB = "trivia_test"
DB_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DB}"


class TriviaTestCase(unittest.TestCase):
    """
    Test class for trivia tests
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = PG_DB
        self.db_path = DB_URI
        setup_db(self.app, self.db_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            # print(self.app.url_map)

        new_question = Question(
            question=TEST_QUESTION,
            answer="Marie Curie",
            difficulty=3,
            category="4"
        )
        new_question.insert()

    def tearDown(self):
        questions = Question.query.filter(Question.question == TEST_QUESTION)
        for q in questions:
            q.delete()

    def get_endpoints_helper(self, endpoint, status_code=200):
        """
        {endpoint} should return 200
        """
        print(self.get_endpoints_helper.__doc__.format(endpoint=endpoint))
        res = self.client().get(endpoint)
        return res.status_code == status_code

    def test_categories_endpoint(self):
        self.assertTrue(self.get_endpoints_helper(endpoint="/categories"))

    def test_questions_endpoint(self):
        self.assertTrue(self.get_endpoints_helper(endpoint="/questions"))


if __name__ == "main":
    unittest.main()

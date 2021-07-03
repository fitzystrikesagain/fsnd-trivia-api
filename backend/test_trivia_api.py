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

        self.new_question = {
            "question": TEST_QUESTION,
            "answer": "Marie Curie",
            "difficulty": 3,
            "category": "4"
        }

        question = Question(
            question=self.new_question["question"],
            answer=self.new_question["answer"],
            difficulty=self.new_question["difficulty"],
            category=self.new_question["category"],
        )
        question.insert()
        self.test_question_id = question.id

    def tearDown(self):
        questions = Question.query.filter(Question.question == TEST_QUESTION)
        for q in questions:
            q.delete()

    def get_endpoints_helper(self, endpoint, status_code=200):
        """GET {endpoint} should return 200"""
        res = self.client().get(endpoint)
        return res.status_code == status_code

    def test_categories_endpoint(self):
        """GET /categories should return 200"""
        self.assertTrue(self.get_endpoints_helper(endpoint="/categories"))

    def test_questions_endpoint(self):
        """GET /questions should return 200"""
        self.assertTrue(self.get_endpoints_helper(endpoint="/questions"))

    def test_create_question(self):
        """POST /questions should return 200"""
        res = self.client().post("/questions", json=self.new_question)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["status"], "success")

    def test_delete_question(self):
        """DELETE /questions/<test_question_id> should return 200"""
        res = self.client().delete(f"/questions/{self.test_question_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["status"], "success")

    def test_search_endpoint(self):
        """POST /questions/search should return 200"""
        request = {"searchTerm": "foo"}
        res = self.client().post("/questions/search", json=request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["status"], "success")

    def test_search_functionality(self):
        """POST /questions/search should return the correct results"""
        request = {"searchTerm": "Nobel"}
        res = self.client().post("/questions/search", json=request)
        response = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["questions"][0]["answer"], "Marie Curie")

    def test_quiz_endpoint(self):
        """POST /quizzes should return 200"""
        data = {
            "previous_questions": [],
            "quiz_category": {"type": "History", "id": "3"}
        }
        res = self.client().post("/quizzes", json=data)
        response = res.json["question"]
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["status"], "success")
        self.assertEqual(response["question"], TEST_QUESTION)
        self.assertEqual(response["answer"], self.new_question["answer"])


if __name__ == "main":
    unittest.main()

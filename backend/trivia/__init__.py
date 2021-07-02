import os
import sys

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from ..models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET,PUT,PATCH,POST,DELETE,OPTIONS")
        return response

    @app.route("/categories", methods=["GET"])
    def get_categories():
        """
        Create an endpoint to handle GET requests for all available categories.
        """
        cat_list = Category.query.all()
        print([c.format() for c in cat_list])
        return jsonify({
            "status": "success",
            "categories": [c.format() for c in cat_list]
        })

    @app.route("/questions")
    def fetch_questions():
        """
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories
        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for
        three pages.
        Clicking on the page numbers should update the questions.
        """
        selection = Question.query.all()
        cat_obj_list = Category.query.all()
        categories = [c.type for c in cat_obj_list]
        current_questions = paginate_questions(request, selection)

        if not current_questions:
            abort(404)

        return jsonify({
            "status": "success",
            "questions": current_questions,
            "total_questions": len(selection),
            "current_category": 1,
            "categories": categories
        })

    @app.route("/questions/$<int:question_id>", methods=["GET"])
    def get_question_by_id(question_id):
        question = Question.query.get(question_id).format()
        return jsonify({
            "status": "success",
            "deleted": question
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question, the question
    will
    be removed. This removal will persist in the database and when you
    refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(404)
            question.delete()
            return jsonify({
                "status": "success",
                "deleted": question.id
            })
        except AttributeError as e:
            print(e, file=sys.stderr)
            abort(404)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def question_by_category(category_id):
        category_id += 1
        print(category_id, file=sys.stderr)
        questions = Question.query.filter(
            Question.category == category_id).all()
        print([q.format() for q in questions], file=sys.stderr)
        return jsonify({
            "status": "success",
            "questions": [q.format() for q in questions],
            "total_questions": len(questions),
            "current_category": category_id
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

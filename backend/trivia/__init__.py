import pdb
import random
import sys

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Question, Category

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
        return jsonify({
            "status": "success",
            "categories": [c.type for c in cat_list]
        })

    @app.route("/questions", methods=["GET"])
    def fetch_questions():
        """
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories
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

    @app.route("/questions/<int:question_id>", methods=["GET"])
    def get_question_by_id(question_id):
        question = Question.query.get(question_id).format()
        return jsonify({
            "status": "success",
            "question": question.format()
        })

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """
        Deletes a question from the database and trivia app
        """
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
            abort(404)

    @app.route("/questions", methods=["POST"])
    def create_question():
        """
        Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.
        """
        data = request.get_json()
        question = Question(
            question=data["question"],
            answer=data["answer"],
            difficulty=data["difficulty"],
            category=str(int(data["category"]) + 1)
        )
        question.insert()
        return jsonify({
            "status": "success",
            "data": question.format(),
        })

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        """
        Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        """
        pattern = f"%{request.get_json()['searchTerm']}%%"
        res = Question.query.filter(Question.question.ilike(pattern)).all()
        response = {
            "status": "success",
            "questions": [q.format() for q in res],
            "total_questions": len(res),
            "current_category": ""
        }
        return jsonify(response)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def question_by_category(category_id):
        """
        Create a GET endpoint to get questions based on category.
        """
        questions = Question.query.filter(
            Question.category == category_id).all()
        return jsonify({
            "status": "success",
            "questions": [q.format() for q in questions],
            "total_questions": len(questions),
            "current_category": category_id
        })

    @app.route("/quizzes", methods=["POST"])
    def start_quiz():
        """
        Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
        """
        try:
            data = request.get_json()
            print(data, file=sys.stderr)
            category_id = str(int(data["quiz_category"]["id"]) + 1)
            prev_questions = data["previous_questions"]
            all_questions = Question.query.filter(
                Question.category == category_id
            ).all()
            questions = [q for q in all_questions if q.id not in prev_questions]

            if questions:
                question = random.choice(questions).format()
                end = False
            else:
                question = None
                end = True

            return jsonify({
                "status": "success",
                "question": question,
                "forceEnd": end
            })
        except Exception as e:
            print(e, file=sys.stderr)
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

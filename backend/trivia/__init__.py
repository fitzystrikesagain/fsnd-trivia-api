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
        TEST: When you click the trash icon next to a question, the question
        will be removed. This removal will persist in the database and when you
        refresh the page.
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
        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of the last
        page of the questions list in the "List" tab.
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

    def search_questions():
        """
        @TODO:
        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
        """
        pass

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def question_by_category(category_id):
        """
        Create a GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.

        """
        category_id += 1
        questions = Question.query.filter(
            Question.category == category_id).all()
        return jsonify({
            "status": "success",
            "questions": [q.format() for q in questions],
            "total_questions": len(questions),
            "current_category": category_id
        })

    def start_quiz():
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
        pass

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

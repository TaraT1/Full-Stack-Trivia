import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#Bookshelf approach from course for pagination
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Done Set up CORS. Allow '*' for origins. 
  @TODO: Delete the sample route after completing the TODOs
  '''
  #CORS (Cross Origin Resources Sharing)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Done Use the after_request decorator to set Access-Control-Allow
  '''
  #CORS Headers (Ref: 3.4)
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
    return response

  '''
  @TODO: Done
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories') #incorporated from kbase not json serializable error
  def get_categories():
    categories = [category.format() for category in Category.query.all()]
    #categories = list(map(Category.format, Category.query.all()))

    if len(categories) == 0:
      abort(404) #resource not found
    
    return jsonify({
      "success": True,
      "categories": categories
    })
  '''
  @TODO: Done
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
    
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    #from def paginate_questions; Ref'd: load questions in kbase
    selection = Question.query.all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404) #resource not found 

    return jsonify({
      "questions": current_questions,
      "total_questions": len(selection)
    }) 

  '''
  Error: TypeError: Object of type InstrumentedAttribute is not JSON serializable
  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = [question.format() for question in Question.query.all()]
    #questions = list(map(Question.format, Question.query.all()))
    categories = [category.format() for category in Category.query.all()]
    #categories = list(map(Category.format, Category.query.all()))
    #categories = Category.query.all()
    
    if len(questions) == 0:
      abort(404) #resource not found
    
    #current category
    for question in questions:
      category = [Question.category]

    return jsonify({
      "questions": questions,
      "total_questions": len(questions), 
      "current_category": category,
      "categories": categories
    })
  '''

  '''
  #@TODO: Done
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  #**Delete question; check endpoint name in FE
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question=Question.query.filter(Question.id==question_id).one_or_none()
      

      if question is None:
        abort(404) #resource notfound
      
      #db actions
      db.session.delete(question_id)
      db.session.commit()
      
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'deleted': question_id,
        
      })

    except:
      abort(422) #unprocessable
      db.session.rollback()

    finally:
      db.session.close()
  

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  @app.route('/questions', methods=['POST'])
  def create_question:
    #From form: question, answer, difficulty, category, cat id, 
    # db.session.add()?
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
  }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
    }), 422

  return app

    
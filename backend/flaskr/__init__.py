import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

'''
#Bookshelf approach from course for pagination
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  #questions = {question.format() for question in selection}
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions
  '''

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

  #kbase Rahul Dev S Objects are not valid. At least it fucking works
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = {category.id: category.type for category in Category.query.all()}#.type?

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

  @app.route('/questions')#question?page (QuestionView.js)
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page-1) * 10
    end = start + 10
    questions = [question.format() for question in Question.query.all()]
    categories = {category.id: category.type for category in Category.query.all()}
    #get_by_category(id)

    if len(questions) == 0:
      abort(404) #resource not found 

    return jsonify({
      "success": True,
      "questions": questions[start:end],
      "total_questions": len(questions),
      "categories": categories,
      "current_category": None
    })
  
  '''
  #@TODO: Done
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  #**Delete question; check endpoint name in FE
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question_id = request.json.get('id')
    
    try:
      get_questions=Question.query.filter(Question.id==question_id).one_or_none()


      if question is None:
        abort(404) #resource notfound
      
      #db actions
      db.session.delete(question_id)
      db.session.commit()
      
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        "success": True,
        "deleted": question_id,
        
      })

    except:
      abort(422) #unprocessable
      db.session.rollback()

  '''
  @TODO: Done 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():
    #From form: question, answer, difficulty, category
    new_question = request.json.get('question')
    new_answer = request.json.get('answer')
    category = request.json.get('category') #category for question, not new cat
    difficulty = request.json.get('difficulty')
    
    # db.session.add()
    try:
      question = Question(question=new_question, answer=new_answer, category=category, difficuly=difficulty)
      question.insert()

      return jsonify({
        "question": new_question,
        "answer": new_answer,
        "category": category,
        "difficulty": difficulty
      })

    except:
      abort(422)


  '''
  @TODO: *CHECK
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def search_question(search_term):
    
    search_term = request.json.get('search_term')
    #query Question.question db for search term
    questions = Question.query.filter(search_term).all()#???
    total_questions = len(questions)
    current_category = Question(category) #for each question?
  
    if questions is None:
      abort(404) #resource not found
    
      for question in questions:
        return jsonify({
          "success": True,
          "questions": questions,
          "answer": answer,
          "category": category,
          "difficulty": difficulty
        })


  '''
  @TODO: *CHECK; c.f. questions end point
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  '''Testing@app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_by_category(category_id):
    category_id=request.json.get('category_id')
    #get_questions = {Question.query.filter(Question.category == category_id).all()}
    
    #using kbase keep getting error 422 
    selection = Question.query.filter(Question.category == category_id).all()
    #formatted_questions = {question.format() for question in selection}

    current_questions = paginate_questions(request, selection)
    

    if len(current_questions) is None:
      abort(404) #resource not found

    return jsonify({
      "success": True,
      "questions": current_questions,
      "total_questions": len(selection),
      "current_category": category_id

    })

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
  #@app.route('/questions', methods=['POST'])
  #def questions_to_play():
  #get random, unique questions w/i category based on parameters

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

    
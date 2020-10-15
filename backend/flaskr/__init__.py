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
  @TODO: DONE Set up CORS. Allow '*' for origins. 
  @TODO: Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: DONE Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
    return response

  '''
  @TODO: DONE. Works, imgs working 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  #Get categories. FE: FormView #20 Categories
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    #categories = {category.id: category.type for category in all_categories}
    formatted_categories = {} #dictionary
    for category in categories:
      formatted_categories[category.id] = category.type

    if len(categories) == 0:
      abort(404) #resource not found

    return jsonify({
      "success": True,
      "categories": formatted_categories,
      "total_categories": len(categories)
    })


  '''
  @TODO: Done, Works.  
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
    
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''


  #Get Questions. FE: QuestionView #24
  @app.route('/questions', methods=['GET']) #Qview: /questions?page=${this.state.page}
  def get_question():
    page = request.args.get('page', 1, type=int)
    start = (page-1) * 10
    end = start + 10
    questions = [question.format() for question in Question.query.all()]

    if len(questions) == 0:
      abort(404) 

    else:
      #categories = {category.id: category.type for category in all_categories}
      categories = Category.query.all()
      formatted_categories = {} #dictionary
      for category in categories:
        formatted_categories[category.id] = category.type
        
      return jsonify({
        "success": True,
        "questions": questions[start:end],
        "total_questions": len(questions),
        "categories": formatted_categories,
        "current_category": None
      })
  
  '''
  #@TODO: Done; Works
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  #Delete question; FE: Qview 105
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    #question_id = request.json.get('id') #id from QuestionView.js
    
    try:
      question=Question.query.filter(Question.id==question_id).one_or_none()

      if question is None:
        abort(404) #resource not found
      
      question.delete() 
      selection = Question.query.all()
      #current_questions = paginate_questions(request, selection)

      return jsonify({
        "success": True,
        "deleted": question_id,
        "total_questions": len(selection) 
      })

    except Exception as e:
      print("Exception: ",e)
      abort(422) #unprocessable

  '''
  @TODO: DONE works
  Create an endpoint to POST a new question, which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  #Add new question; FE: FormView #37. ToDo: invalidate if info missing
  @app.route('/questions/add', methods=['POST'])  
  def submit_question():
    #From form: question, answer, difficulty, category
    #body, etc. based on books example 

    data=request.get_json()#replace body w data for consistency 
    
    new_question=data.get('question')
    new_answer=data.get('answer')
    new_difficulty=data.get('difficulty')
    new_category=data.get('category') 

    #Note: category type or id. id is int, type is string
    
    try:
      add_question = Question(
        question=new_question, 
        answer=new_answer, 
        category=new_category, 
        difficulty=new_difficulty
        )

      add_question.insert() 

      return jsonify({
        "success": True,
        "question": new_question,
        "answer": new_answer,
        "difficulty": new_difficulty,
        "category": new_category
      })

    except Exception as e:
      print('Exception is >> ',e)
      #print(sys.exc_info())
      abort(422)

  '''
  @TODO: DONE *Working on backend & frontend!!!
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  #Search questions
  @app.route('/questions/search', methods=['POST'])
  def submit_search():
    search_term = request.json.get('searchTerm',None) 
    questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
    formatted_questions = [question.format() for question in questions]

    if len(questions) == 0:
      formatted_questions = [] 
      abort(404)

    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(questions),
      "current_category": None 
    })
  
  '''
  @TODO: DONE *works; c.f. questions end point
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  #Get questions by category
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_by_category(category_id):

    questions = Question.query.filter(Question.category == str(category_id)).all()
    formatted_questions = [question.format() for question in questions]

    if len(questions) == 0:
      abort(404) #resource not found
  
    else:
      return jsonify({
        "success": True,
        "questions": formatted_questions,
        "total_questions": len(Question.query.all()),
        "current_category": category_id 
        })

  '''
  @TODO: DONE, working
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  #Quiz - questions to play; FE: QuizView #50
  @app.route('/quizzes', methods=['POST'])
  def questions_to_play():
    data = request.get_json()
    
    category_id = int(data['quiz_category']['id']) 
    category = Category.query.get(category_id)
    previous_questions = data['previous_questions'] 

    try:
      #Get questions if category is not selected that have not been played; QuizView #105
      if category == None: 
        get_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

      #Get questions with selected category that have not been played
      else:
        get_questions = (Question.query.filter(Question.category==category_id).filter(Question.id.notin_(previous_questions)).all()) 

      questions = [question.format() for question in get_questions] 
      
      #Randomize order of questions, deliver 1 at a time
      if (len(questions) == 0):
        quest= None
      else:
        quest = questions[random.randrange(0, len(questions))] #rvu: can also use func.random() in your SQLAlchemy
      
      return jsonify({
        "question": quest,
        "success": True
      })      

    except Exception as e:
      print("Exception >> ", e )
      abort(422)

  '''
  @TODO: DONE
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def resource_not_found(error):
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

  @app.errorhandler(500)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
    }), 500

  return app

    

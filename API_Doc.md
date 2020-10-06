API Documentation
Inital Setup

(Stripe documentation model:)
Trivia API is organized around REST principles. Resource-oriented URLs, returns JSON encoded responses, and uses standard http respoonse codes, authentication, and verbs.

Locally hosted

Python 3.7, Virtual Enviornment. Pip dependencies install Flask and SQLAlchemy requirements listed in requirements.txt. Setup databse and run the server. Details are in backend Readme.md

Testing is in backend/test_flaskr.py

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

HTTP Status Code Summary
200: success

Errors
400: bad request
404: resource not found
422: unprocessable
500: internal server error

Sample curl request


Response

This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches list of questions. pagination for every 10 questions
- Request Arguments: category, difficulty
- Returns: list of questions, each with single keys, including categories, full list of categories
{ "success": True,
  "questions": questions[start:end],
  "total_questions": integer,
  "categories": string,
  "current_category": integer }




POST '/questions/add'
- Creates new question
- Arguments include question, answer, difficulty, and category
- Returns object

{ "success": True,
  "question": new_question,
  "answer": new_answer,
  "difficulty": new_difficulty,
  "category": new_category}

POST '/questions/search'
- Returns questions containing search term
- Request argument: search term
- Returns: list of questions, each with answer, single key, and category.

DELETE '/questions/<int:question_id>'
- Returns: 
      { "success": True,
        "deleted": question_id,
        "total_questions": integer}

GET '/categories/<int:category_id>/questions'
- Returns questions based on category
- Request Arguments: <int:category_id>

POST '/quizzes'
- 
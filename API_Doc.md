
#API Documentation

Trivia API is organized around REST principles. Resource-oriented URLs return JSON encoded responses and use standard http respoonse codes, authentication, and verbs.

- Completed the partial Flask and SQLAlchemy server provided by Udacity
- Defined and updated endpoints 
- Updated React frontend endpoints 
- Formatted data responses for React frontend consumption

##Inital Setup
Locally hosted, Trivia runs in a virtual environment in Python 3.7. 

### Backend
- Install Flask and SQLAlchemy requirements listed in ./backend/requirements.txt. 
- Setup databse and run the server. Details are in ./backend/README.md

### Frontend
This project depends on Nodejs and Node Package Manager. Details are in ./frontend/README.md.

### HTTP Status Code Summary
200: success

Errors
400: bad request
404: resource not found
422: unprocessable
500: internal server error

Sample curl request
Posts search term "title" for list of questions
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm”:”title”}’ http://127.0.0.1:5000/questions/search

### Endpoints
*GET '/categories'
*GET '/questions'
*GET '/categories/<int:category_id>/questions'
*POST '/questions/add'
*POST '/questions/search'
*POST '/quizzes'
*DELETE '/questions/<int:question_id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key and category string key:value pairs 
{ '1' : "Science",
  '2' : "Art",
  '3' : "Geography",
  '4' : "History",
  '5' : "Entertainment",
  '6' : "Sports"}

GET '/questions'
- Fetches list of questions with pagination for every 10 questions
- Request Arguments: category, difficulty
- Returns: paginated list of questions and full list of categories. Each question has single key and current category.
{ "success": True,
  "questions": list,
  "total_questions": integer,
  "categories": string,
  "current_category": integer }

GET '/categories/<int:category_id>/questions'
- Fetches list of questions given category
- Request Arguments: <int:category_id>
- Returns: list of questions in category, category_id, and total number of quiz questions
{ "success": True,
  "questions": list,
  "total_questions": integer,
  "current_category": integer }

POST '/questions/add'
- Creates new question
- Request arguments: question, answer, difficulty, and category
- Returns object
{ "success": True,
  "question": new_question,
  "answer": new_answer,
  "difficulty": integer,
  "category": integer}

POST '/questions/search'
- Returns questions containing search term
- Request argument: search term
- Returns: list of questions, each with answer, single key, and category.
{ "success": True,
  "questions": list, 
  "total_questions": integer,
  "current_category": integer }

DELETE '/questions/<int:question_id>'
- Deletes selected question
- Request Arguments: question_id
- Returns: confirmation that deletion was successful, the deleted question_id, and the total number of questions
{ "success": True,
  "deleted": question_id,
  "total_questions": integer }

POST '/quizzes'
- Gets randomized questions to play given category, avoiding previously played questions
- Request argument: category
- Returns list of randomized questions
{ "question": list,
  "success": True }
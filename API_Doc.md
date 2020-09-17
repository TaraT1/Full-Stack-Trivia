API Documentation
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
- Request Arguments:
- Returns: list of questions, each with single keys, including categories, full list of categories

DELETE '/questions/<int:question_id>'



POST '/questions'
- Creates new question
- Arguments include question, answer, difficulty, and category
- Returns

POST '/questions/search'
- Returns questions containing search term
- Request argument: search term
- Returns: list of questions, each with answer, single key, and category.

POST '/quizzes'
- 
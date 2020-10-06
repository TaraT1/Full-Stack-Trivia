import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            "question": "test ques", 
            "answer": "test ans", 
            "difficulty": 3, 
            "category": "3", 
            "id": 700
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):#success
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])
        

    def test_get_questions(self):#success
        res = self.client().get('/questions')
        data = json.loads(res.data) 
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        #self.assertTrue(data['current_category'])
        
    '''
    def test_delete_question(self):
        res = self.client().delete('/questions/700')
        data = json.loads(res.data) 

        question = Question.query.filter(Question.id == 700).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_404_question_not_exist(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
    '''

    def test_add_question(self): #success
        res=self.client().post('/questions/add', json=self.new_question)
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #'{"question": "test ques", "answer": "test ans", "difficulty": 3, "category": "3", "id": 700}' 
    '''
    def test_search_questions(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        #search object not found

    def test_get_questions_by_category(self):#success
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_question_by_cat(self): #get question by category
        res = self.client().get('/categories/<int:category_id>/questions')
        data = json.loads(res.data)
        
        #self.assertEqual(res.status_code, 404)

    def test_quizzes(self):
        res=self.client().post('/quizzes')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
    '''

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
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
    #Load category list
    def test_get_categories(self):#success
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])
        
    #Get question list
    def test_get_questions(self):#success
        res = self.client().get('/questions')
        data = json.loads(res.data) 
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        #self.assertTrue(data['current_category'])
        
    #Add question with complete information
    def test_add_question(self): #success
        res=self.client().post('/questions/add', json=self.new_question)
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        
    #Fail to add question w incomplete info
    def test_422_add_incomplete_question(self):
        res=self.client().post(
            '/questions/add', 
            json={
            'question': '', 
            'answer': '', 
            'difficutly': 3,
            'category': ''}
        )
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    #Test to delete existing quesstion
    def test_delete_question(self):#works
        res = self.client().delete('/questions/10')
        data = json.loads(res.data) 

        question = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    #Test failure of attempting to delete nonexistant question
    def test_422_question_not_exist(self):#success
        res = self.client().delete('/questions/800')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    #Test for loading questions given search term
    def test_search_questions(self):#success
        res = self.client().post(
            '/questions/search', 
            json={'searchTerm': 'artist'})
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    #Test for search term not found
    def test_404_search_not_found(self):#success
        res = self.client().post(
            '/questions/search', 
            json={'searchTerm': 'notfound'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    #Load questions by existing category
    def test_get_questions_by_category(self):#success
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    #Test for loading questions by invalid category
    def test_404_question_by_cat(self): #success
        res = self.client().get('/categories/120/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    #Test for loading questions by category
    def test_quiz_question_by_category(self):
        res=self.client().post(
            '/quizzes', 
            json={
                'quiz_category': {
                    'id': '2', 'type': 'Science'},
                'previous_questions': []
                })
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    #Test for loading questions for all categories
    def test_quiz_all_categories(self):
        res=self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'id': '1', 'type': 'Science',
                    'id': '2', 'type': 'Art',
                    'id': '3', 'type': 'Georaphy',
                    'id': '4', 'type': 'History',
                    'id': '5', 'type': 'Entertainment',
                    'id': '6', 'type': 'Sports'
                },
                'previous_questions': []
            })
        data = json.loads(res.data)
                
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    #Test for loading questions in category with previous questions
    def test_quiz_previous_questions(self):
        res=self.client().post(
            '/quizzes', 
            json={
                'quiz_category': {'id': '1', 'type': 'Science'},
                'previous_questions': [1, 2, 3]
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    #Test for loading questions with no category and previous questions           
    def test_quiz_no_category_previous_questions(self):
        res=self.client().post(
            '/quizzes', 
            json={
                'quiz_category': {'id': '0', 'type': ''},
                'previous_questions': [1, 2, 3]
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    
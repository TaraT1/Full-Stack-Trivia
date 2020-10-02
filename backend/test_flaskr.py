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
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])
        




    '''
    def test_get_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)
        
    def test_delete_question(self):
        res = self.client().delete('/questions/<int:question_id>')
        self.assertEqual(res.status_code, 200)


    def test_add_question(self):
        res=self.client().post('/questions/add')
        self.assertEqual(res.status_code, 200)

    def test_search_questions(self):
        res= self.client().post('/questions/search')
        self.assertEqual(res.status_code, 200)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/<int:category_id>/questions')
        self.assertEqual(res.status_code, 200)

    def test_quizzes(self):
        res=self.client().post('/quizzes')
        self.assertEqual(res.status_code, 200)
    '''


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
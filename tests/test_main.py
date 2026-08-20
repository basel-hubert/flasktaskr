# project/test_main.py


import os
import unittest

TEST_DB = 'test.db'
basedir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'project'))
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault(
    'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, TEST_DB))

from project import app, db
from project.models import User


class MainTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################


    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.assertEqual(app.debug, False)


    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    ########################
    #### helper methods ####
    ########################


    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)


    ###############
    #### tests ####
    ###############


    def test_404_error(self):
        response = self.app.get('/this-route-does-not-exist/')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Sorry. There\'s nothing here.', response.data)


    def test_500_error(self):
        bad_user = User(
            name='Jeremy',
            email='jeremy@realpython.com',
            password='django'
        )
        db.session.add(bad_user)
        db.session.commit()
        self.assertRaises(ValueError, self.login, 'Jeremy', 'django')
        try:
            response = self.login('Jeremy', 'django')
            self.assertEqual(response.status_code, 500)
        except ValueError:
            pass



if __name__ == '__main__':
    unittest.main()
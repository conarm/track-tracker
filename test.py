import os
import unittest
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class TestCase(unittest.TestCase):

    ########################
    #### helper methods ####
    ########################
    def register(self, username, email, password):
        return self.app.post(
            '/register',
            data=dict(username=username, email=email, password=password),
            follow_redirects=True
        )
    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_route_root(self):
       response = self.app.get('/',
                              follow_redirects=True)
       self.assertEqual(response.status_code, 200)

    def test_route_login(self):
       response = self.app.get('/login',
                              follow_redirects=True)
       self.assertEqual(response.status_code, 200)

    def test_route_top(self):
       response = self.app.get('/top',
                              follow_redirects=True)
       self.assertEqual(response.status_code, 200)

    def test_route_topreviews(self):
       response = self.app.get('/top-reviews',
                              follow_redirects=True)
       self.assertEqual(response.status_code, 200)

    def test_route_register(self):
       response = self.app.get('/register',
                              follow_redirects=True)
       self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = self.register('testuser', 'testemail@testemail.com', 'testPassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)
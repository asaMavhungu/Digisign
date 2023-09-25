import pytest
from flask import url_for

import sys
print(sys.path)

from project import create_app, db
from project.models import User


@pytest.fixture
def app():
	app = create_app()
	app.config['TESTING'] = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
	with app.app_context():
		db.create_all()
		yield app
		db.drop_all() # Clear database after test

@pytest.fixture
def client(app):
	return app.test_client()

def test_home_page(client):
	response = client.get('/')
	assert response.status_code == 200
	assert b'Home2' in response.data

def test_login_page(client):
	response = client.get('/login')
	assert response.status_code == 200
	assert b'Login' in response.data

def test_signup_and_login(app, client):
	with app.test_request_context():
		# Simulate signing up a user
		signup_data = {
			'email': 'testuser@example.com',
			'firstName': 'Test',
			'password1': 'testpassword',
			'password2': 'testpassword',
		}
		signup_response = client.post('/sign-up', data=signup_data, follow_redirects=True)
		assert signup_response.status_code == 200  # Assuming successful signup returns a 200 status code

		# Simulate logging in with the newly signed-up user
		login_response = client.post('/login', data={'email': signup_data['email'], 'password': signup_data['password1']})
		assert login_response.status_code == 302  # Redirect after successful login
		assert login_response.headers['Location'] == url_for('views.home')

def test__invalid_password_login(app, client):
	with app.test_request_context():
		# Simulate signing up a user
		signup_data = {
			'email': 'testuser@example.com',
			'firstName': 'Test',
			'password1': 'testpassword',
			'password2': 'testpassword',
		}
		signup_response = client.post('/sign-up', data=signup_data, follow_redirects=True)
		assert signup_response.status_code == 200  # Assuming successful signup returns a 200 status code

		# Simulate logging in with the newly signed-up user
		login_response = client.post('/login', data={'email': signup_data['email'], 'password': 'wrongpassword'})
		assert login_response.status_code == 200  # No redirect, wrong password



def test_invalid_email_login(client):
	response = client.post('/login', data={'email': 'testuser@example.com', 'password': 'wrongpassword'})
	assert response.status_code == 200
	assert b'Email does not exist.' in response.data
    

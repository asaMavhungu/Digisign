# test_app.py
import pytest
from flask.testing import FlaskClient
from project.app import app  # Import the Flask app instance from app.py

# Define a pytest fixture called "client"
@pytest.fixture
def client():
	app.config['TESTING'] = True  # Set TESTING configuration to True to enable testing mode
	client: FlaskClient = app.test_client()    # Create a test client for the Flask app
	yield client                  # Yield the test client to the test function
								 # (code below 'yield' will be executed after the test function)

# Define a test function called "test_hello"
def test_hello(client):
	response = client.get('/')  # Send a GET request to the root ('/') route using the test client
	assert response.status_code == 200  # Assert that the response status code is 200 (OK)
	assert b'Hello, World!' in response.data  # Assert that the response contains 'Hello, World!'

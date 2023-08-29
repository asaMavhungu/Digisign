
# api/__init__.py
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo

from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from api.models.User import User  # Import your User class
from datetime import timedelta  # Import timedelta from datetime
bcrypt = Bcrypt()


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pymongo import MongoClient

def createApp():

	app = Flask(__name__)

	# Initialize JWTManager with your Flask app
	jwt = JWTManager(app)

	app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Replace with your secret key
	app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Set token expiration time


	# Connect to MongoDB Atlas cluster
	uri = "mongodb+srv://asa:asas@cluster0.juh7xtg.mongodb.net/your_database?retryWrites=true&w=majority"
	client = MongoClient(uri)

	# Check if the connection is successful
	try:
		client.admin.command('ping')
		print("Connected to MongoDB Atlas cluster!")
	except Exception as e:
		print(e)

	# Initialize PyMongo with the app
	app.config['MONGO_URI'] = uri
	mongo = PyMongo(app)
	api = Api(app)


	# Import and add your UserResource here
	from .resources.user_signup_resource import UserSignupResource
	api.add_resource(UserSignupResource, '/user', '/user/<string:user_id>', resource_class_args=(mongo,))

	from .resources.user_login_resource import UserLoginResource
	api.add_resource(UserLoginResource, '/login', resource_class_args=(mongo,))

	from .resources.slide_resource import SlideResource
	api.add_resource(SlideResource, '/slides', '/slides/<string:slide_title>', resource_class_args=(mongo,))

	from .resources.department_resource import DepartmentResource
	api.add_resource(DepartmentResource, '/department', resource_class_args=(mongo,))



	return app, mongo


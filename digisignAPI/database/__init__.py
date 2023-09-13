from flask_pymongo import PyMongo

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

from flask import Flask
from pymongo import MongoClient
from flask_pymongo import PyMongo

class MongoDBClient:
	def __init__(self, uri):
		self.client = MongoClient(uri)
		self.db = self.client.get_database()

	def get_user(self, user_id):
		return self.db.users.find_one({'_id': user_id})

	def create_user(self, user_data):
		return self.db.users.insert_one(user_data).inserted_id

	# Add more methods for other database operations

def createMongoDatabase(module_name):
	app = Flask(module_name)

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

	# TODO use the mongo client class to encapsulate database interactions
	mongo_client = MongoDBClient(uri)
	return app, mongo

def createDatabaseSQL():
	
	from flask import Flask
	from flask_jwt_extended import JWTManager
	from flask_restful import Api
	from flask_sqlalchemy import SQLAlchemy

	app = Flask(__name__, static_folder='assets')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Replace with your SQLite database file path
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications

	# Initialize SQLAlchemy with the app
	db = SQLAlchemy(app)

	# Initialize JWTManager with your Flask app
	jwt = JWTManager(app)

	app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Replace with your secret key
	app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Set token expiration time

	api = Api(app)


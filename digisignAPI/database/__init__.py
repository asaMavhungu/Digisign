from flask_pymongo import PyMongo

# api/__init__.py
from flask import Flask, request, jsonify
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

from database.DatabaseClient import DatabaseClient

	# Add more methods for other database operations

def createMongoDatabase(module_name):
	app = Flask(module_name)

	# Connect to MongoDB Atlas cluster
	app.config['MONGO_URI'] = "mongodb+srv://asa:asas@cluster0.juh7xtg.mongodb.net/your_database?retryWrites=true&w=majority"
	mongo = PyMongo(app)

	"""
	TEST if the mongo app works. PASSED
		slides_collection = mongo.db.slides
		slides = list(slides_collection.find())
		tables = mongo.db.list_collection_names()
		slides_list = [slide for slide in slides]
		print(jsonify(slides_list))
	"""

	# TODO use the mongo client class to encapsulate database interactions
	db_client = DatabaseClient(mongo)
	return app, db_client

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


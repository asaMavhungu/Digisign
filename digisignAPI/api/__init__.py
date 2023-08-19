
# api/__init__.py
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo

from flask import request
from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from api.models.User import User  # Import your User class
bcrypt = Bcrypt()


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pymongo import MongoClient

def createApp():

	app = Flask(__name__)

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
	from .resources.user_resource import UserResource
	api.add_resource(UserResource, '/user', '/user/<string:user_id>', '/user/login', resource_class_args=(mongo,))

	return app, mongo

app, mongo = createApp()

def getApp():
	return app, mongo
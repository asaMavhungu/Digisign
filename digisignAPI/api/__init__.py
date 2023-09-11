
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


	# User login and stuff
	from .resources.user_resource import UserResource
	api.add_resource(UserResource, '/user', '/user/<string:username>', resource_class_args=(mongo,))

	# User reg and stuff
	from .resources.user_list_resource import UserListResource
	api.add_resource(UserListResource, '/users', resource_class_args=(mongo,))


	# Register SlideResource with endpoint /slides/<string:slide_title>
	from .resources.slide_resource import SlideResource
	api.add_resource(SlideResource, '/slides/<string:slide_title>', resource_class_args=(mongo,))

	# Register SlideList with endpoint /slides
	from .resources.slide_list_resource import SlideList 
	api.add_resource(SlideList, '/slides', resource_class_args=(mongo,))

	# Register DeviceResource with endpoint /devices/<string:device_name>
	from .resources.device_resource import DeviceResource
	api.add_resource(DeviceResource, '/devices/<string:device_name>', resource_class_args=(mongo,))

	# Register DeviceListResource with endpoint /devices
	from .resources.device_list_resource import DeviceListResource
	api.add_resource(DeviceListResource, '/devices', resource_class_args=(mongo,))

	# Register DepartmentResource with endpoint /departments/<string:department_id>
	from .resources.department_resource import DepartmentResource
	api.add_resource(DepartmentResource, '/departments/<string:department_id>', resource_class_args=(mongo,))

	# Register DepartmentListResource with endpoint /departments
	from .resources.department_list_resource import DepartmentListResource
	api.add_resource(DepartmentListResource, '/departments', resource_class_args=(mongo,))



	return app, mongo


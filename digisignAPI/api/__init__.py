
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

from database import createDatabase

from database import DatabaseClient


# TODO: check if all endpoint work as expected
# TODO: Redo the api spec

def createApi(app: Flask, db_client: DatabaseClient):

	#app, db_client  = createDatabase(module_name, databaseOption)

	# Initialize JWTManager with your Flask app
	jwt = JWTManager(app)

	app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Replace with your secret key
	app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Set token expiration time

# TODO use mongoClient class to handle database
	api = Api(app)

	"""
	# User login and stuff
	from .resources.user_resource import UserResource
	api.add_resource(UserResource, '/api/user', '/api/user/<string:username>', resource_class_args=(mongo_client,))

	# User reg and stuff
	from .resources.user_list_resource import UserListResource
	api.add_resource(UserListResource, '/api/users', resource_class_args=(mongo_client,))
	"""


	# Register UserResource with endpoint /api/users
	from .resources.user_resource import UserResource
	api.add_resource(UserResource, '/api/users', resource_class_args=(db_client,))

	# Register UserResource with login
	from .resources.user_login_resource import UserLoginResource
	api.add_resource(UserLoginResource, '/api/login', resource_class_args=(db_client,))


	# Register SlideResource with endpoint /slides/<string:slide_title>
	from .resources.slide_resource import SlideResource
	api.add_resource(SlideResource, '/api/slides/<string:slide_title>', resource_class_args=(db_client,))

	# Register SlideList with endpoint /slides
	from .resources.slide_list_resource import SlideList 
	api.add_resource(SlideList, '/api/slides', resource_class_args=(db_client,))

	# Register DeviceResource with endpoint /devices/<string:device_name>
	from .resources.device_resource import DeviceResource
	api.add_resource(DeviceResource, '/api/devices/<string:device_name>', resource_class_args=(db_client,))

	# Register DeviceListResource with endpoint /devices
	from .resources.device_list_resource import DeviceListResource
	api.add_resource(DeviceListResource, '/api/devices', resource_class_args=(db_client,))

	# Register DepartmentResource with endpoint /departments/<string:department_id>
	from .resources.department_resource import DepartmentResource
	api.add_resource(DepartmentResource, '/api/departments/<string:department_name>', resource_class_args=(db_client,))

	# Register DepartmentListResource with endpoint /departments
	from .resources.department_list_resource import DepartmentListResource
	api.add_resource(DepartmentListResource, '/api/departments', resource_class_args=(db_client,))



	return app, db_client


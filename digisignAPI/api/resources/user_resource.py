from flask import request, jsonify, current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Slide import Slide
from api.models.SlideFactory import SlideFactory
from api.models.Department import Department
from api.models.SlideFactory import SlideFactory
from api.models.Device import Device
from api.models.User import User
import hashlib

def hash_password(password):
	"""
	Hashes a password using SHA-256.

	:param password: The password to hash.
	:return: The hashed password.
	"""
	salt = b'some_salt_value'  # Replace with your actual salt value
	password_bytes = password.encode('utf-8')
	hashed_password = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
	return hashed_password.hex()


# Your User model or authentication logic (replace with your actual implementation)
from api.models.User import User  # Import your User model

# Request parser for user registration and update
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username')
user_parser.add_argument('password', type=str, required=False, help='Password')
user_parser.add_argument('email', type=str, required=False, help='Email')
user_parser.add_argument('verified', type=bool, required=False, default=False, help='User verification status')


user_fields = {
	'user_id': fields.String(attribute='user_id'),
	'username': fields.String,
	'email': fields.String,
	'password': fields.String,
}


class UserResource(Resource):
	
	"""
	Resource class for user registration, retrieval, update, and deletion.
	"""
	#@jwt_required()
	@marshal_with(user_fields)
	def get(self, user_name):
		#current_user = get_jwt_identity()
		#user_dict = User.find_by_username(current_user)  # Replace 'database_client' with your actual database client
		user_dict, code = User.find_by_name(user_name)
		if code == 200:
			user = User.from_dict(user_dict)
			return user, 200
		return {'message': 'User not found'}, 404
	
	def patch(self, user_name):
		"""
		Update a specific department by ID (partial update).
		"""
		args = user_parser.parse_args()
		user_db_dict, code = User.find_by_name(user_name)

		if code == 404:
			return {"message": "User not found"}, 404

		user = User.from_dict(user_db_dict)

		if 'username' in args:
			new_username = args['username']
			message, code = user.update_database_entry({"username" : new_username})

			return message, code
	
	def delete(self, user_name):
		user_db_dict, code = User.find_by_name(user_name)
		

		if code == 404:
			return {"message": "User not found"}, 404

		user = User.from_dict(user_db_dict)

		result, code  = user.delete_database_entry()

		return result, code
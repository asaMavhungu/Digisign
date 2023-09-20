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
user_parser.add_argument('password', type=str, required=True, help='Password')
user_parser.add_argument('email', type=str, required=True, help='Email')
user_parser.add_argument('verified', type=bool, required=False, default=False, help='User verification status')

class UserResource(Resource):
	
	"""
	Resource class for user registration, retrieval, update, and deletion.
	"""
	@jwt_required()
	def get(self):
		current_user = get_jwt_identity()
		user_dict = User.find_by_username(current_user)  # Replace 'database_client' with your actual database client
		if user_dict:
			return user_dict, 200
		return {'message': 'User not found'}, 404
	
	def post(self):
		print("======================POST=======================")
		args = user_parser.parse_args()
		username = args['username']
		password = args['password']
		email = args['email']
		verified = args['verified']

		# Check if the user exists
		existing_user = User.find_by_username(username)  # Replace 'database_client' with your actual database client

		if existing_user:
			return {'message': 'User with this username already exists'}, 400

		# Hash the password (you should use a password hashing library)
		# Replace 'hash_password' with your actual password hashing function
		hashed_password = hash_password(password)
		#TODO Bring hashing back
		hashed_password = password

		# Create a new user
		new_user = User(username, hashed_password, email, verified)

		# Save the user to the database
		user_id = new_user.save()  # Replace 'database_client' with your actual database client

		return {'message': 'User registered successfully', 'user_id': user_id}, 201

	@jwt_required()
	def put(self):
		current_user = get_jwt_identity()
		args = user_parser.parse_args()
		new_username = args['username']
		new_password = args['password']
		new_email = args['email']
		verified = args['verified']

		# Check if the new username exists
		existing_user = User.find_by_username(new_username)  # Replace 'database_client' with your actual database client

		if existing_user:
			return {'message': 'User with this username already exists'}, 400
		
		our_user = User.find_by_username(current_user)
		this_user = User.from_dict(our_user)

		# Hash the password (you should use a password hashing library)
		# Replace 'hash_password' with your actual password hashing function
		new_hashed_password = hash_password(new_password)

		this_user.password = new_hashed_password

		# Create a new user
		this_user.username = new_username
		this_user.email = new_email
		this_user.verified = verified

		# Save the user to the database
		user_id = this_user.save()  # Replace 'database_client' with your actual database client

		me = User.find_by_username(new_username)

		return this_user.to_dict(), 201

	@jwt_required()
	def patch(self):
		current_user = get_jwt_identity()
		args = user_parser.parse_args()
		username = args['username']
		password = args['password']
		email = args['email']
		verified = args['verified']

		# Check if the user exists
		existing_user = User.find_by_username(current_user)  # Replace 'database_client' with your actual database client
		this_user = User.from_dict(existing_user)

		if not existing_user:
			return {'message': 'User not found'}, 404

		# Hash the new password (if provided)
		if password:
			hashed_password = hash_password(password)
			this_user.password = hashed_password

		# if username:
			# this_user.username = username
		if email:
			this_user.email = email
		if verified:
			this_user.verified = verified

		# Update the user in the database
		user_id = this_user.save()  # Replace 'database_client' with your actual database client

		return {'message': 'User updated successfully', 'user_id': user_id}, 200

	@jwt_required()
	def delete(self):
		current_user = get_jwt_identity()
		existing_user = User.find_by_username(current_user)  # Replace 'database_client' with your actual database client
		this_user = User.from_dict(existing_user)

		if not existing_user:
			return {'message': 'User not found'}, 404

		this_user.delete()
		return {'message': 'User deleted successfully'}, 200



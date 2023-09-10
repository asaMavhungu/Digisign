# api/resources/user_resource.py
from flask import request
from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from api.models.User import User  # Import your User class
from flask import current_app as app
bcrypt = Bcrypt()

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("username", type=str, help="Username is required", required=True)
user_put_args.add_argument("email", type=str, help="Email is required", required=True)
user_put_args.add_argument("password", type=str, help="Password is required", required=True)

class UserSignupResource(Resource):
	
	def __init__(self, mongo):
		"""
		Constructor for the UserResource class.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		"""
		self.mongo = mongo

	def post(self):
		"""
		Endpoint for creating a new user.

		Parses user input, checks for username uniqueness, hashes the password,
		and saves the user to the database.

		:return: JSON response with the result of the user creation.
		"""
		args = user_put_args.parse_args()
		username = args["username"]
		email = args["email"]
		password = args["password"]

		# Check if the username is already taken
		if User.find_by_username(username, self.mongo):
			return {"message": "Username already exists"}, 400

		# Hash the password before saving it
		password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

		user = User(username, email, password_hash)
		user_id = user.save(self.mongo)
		return {"message": "User created", "user_id": user_id}, 201

	def get(self, username):
		"""
		Endpoint for retrieving user information by user ID.

		:param user_id: The unique identifier of the user.
		:return: JSON response with user information or a "User not found" message.
		"""
		user = User.find_by_username(username, self.mongo)
		if user:
			return user.to_dict()
		return {"message": "User not found"}, 404
	
	"""
	def login():
		args = user_put_args.parse_args()
		username = args["username"]
		password = args["password"]
		
		user = User.find_by_username(username, mongo)

		if user and bcrypt.check_password_hash(user["password_hash"], password):
			return {"message": "Login successful", "user_id": str(user["_id"])}, 200
		else:
			return {"message": "Invalid credentials"}, 401
	"""
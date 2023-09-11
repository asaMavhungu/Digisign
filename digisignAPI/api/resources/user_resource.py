from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request
from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from api.models.User import User
from flask import current_app as app

bcrypt = Bcrypt()

user_parser = reqparse.RequestParser()
user_parser.add_argument("email", type=str, help="Email address")
user_parser.add_argument("password", type=str, help="Password")

class UserResource(Resource):
	def __init__(self, mongo):
		self.mongo = mongo

	def get(self, username):
		"""
		Endpoint for retrieving user information by username.

		:param username: The username of the user.
		:return: JSON response with user information or a "User not found" message.
		"""
		user = User.find_by_username(username, self.mongo)
		if user:
			return user.to_dict()
		return {"message": "User not found"}, 404

	def post(self):
		args = user_parser.parse_args()
		username = args["username"]
		password = args["password"]

		# Find the user by username
		user = User.find_by_username(username, self.mongo)

		if user:
			# Verify the password
			if user.verify_password(password):
				# Create a JWT token
				access_token = create_access_token(identity=username)

				return {"message": "Login successful", "access_token": access_token}, 200
			else:
				return {"message": "Invalid password"}, 401
		else:
			return {"message": "User not found"}, 404

	@jwt_required()  # Requires authentication
	def patch(self, username):
		"""
		Partially update user information.

		:param username: The username of the user to update.
		:return: JSON response with the updated user information or an error message.
		"""
		current_username = get_jwt_identity()
		if current_username != username:
			return {"message": "You can only update your own user information"}, 403

		args = user_parser.parse_args()
		email = args.get("email")
		password = args.get("password")

		user = User.find_by_username(username, self.mongo)
		if not user:
			return {"message": "User not found"}, 404

		if email:
			user.email = email
		if password:
			# Hash and update the password
			user.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

		# Save the updated user
		user.save(self.mongo)

		return {"message": "User information updated successfully", **user.to_dict()}, 200

	@jwt_required()  # Requires authentication
	def put(self, username):
		"""
		Fully update user information.

		:param username: The username of the user to update.
		:return: JSON response with the updated user information or an error message.
		"""
		current_username = get_jwt_identity()
		if current_username != username:
			return {"message": "You can only update your own user information"}, 403

		args = user_parser.parse_args()
		email = args.get("email")
		password = args.get("password")

		user = User.find_by_username(username, self.mongo)
		if not user:
			return {"message": "User not found"}, 404

		user.email = email
		if password:
			# Hash and update the password
			user.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

		# Save the updated user
		user.save(self.mongo)

		return {"message": "User information updated successfully", **user.to_dict()}, 200

# Example protected resource that requires a valid JWT token
class ProtectedResource(Resource):
	@jwt_required() # so this means that to access this i need an access token?
	def get(self):
		# This resource is protected by JWT authentication
		current_user_id = get_jwt_identity() 
		return {"message": "This is a protected resource for user ID: " + current_user_id}, 200
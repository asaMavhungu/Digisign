from flask import request
from flask_restful import Resource
from database.DatabaseClient import DatabaseClient
from flask_jwt_extended import create_access_token
from api.models.User import User

class UserLoginResource(Resource):
	def __init__(self, db_client: DatabaseClient):
		self.db_client = db_client

	def post(self):
		data = request.get_json()
		username = data.get('username', None)
		password = data.get('password', None)

		if not username or not password:
			return {'message': 'Missing username or password'}, 400

		user_identity = User.get_user_identity(username, password, self.db_client)

		if user_identity:
			# Generate a JWT token for the user
			access_token = create_access_token(identity=user_identity)

			# Return the token to the client
			return {'message': 'Login successful', 'access_token': access_token}, 200

		return {'message': 'Invalid credentials'}, 401



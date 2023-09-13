from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.User import User

# Request parser for user data
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username of the user')
user_parser.add_argument('email', type=str, required=True, help='Email of the user')
user_parser.add_argument('password_hash', type=str, required=True, help='Password hash of the user')

# Define the fields for marshaling user data in responses
user_fields = {
	'_id': fields.String(attribute='_id'),
	'username': fields.String,
	'email': fields.String,
	'password_hash': fields.String,
}

class UserListResource(Resource):
	"""
	Resource class for managing collections of users.
	"""
	def __init__(self, mongo):
		self.mongo = mongo

	@marshal_with(user_fields)
	def get(self):
		"""
		Get a list of all users.
		Returns:
			List[User]: A list of all users.
		"""
		users_data = self.mongo.db.users.find()
		users = [User.from_dict(user_data) for user_data in users_data]
		return users, 200

	def post(self):
		"""
		Create a new user.
		"""
		args = user_parser.parse_args()
		username = args['username']
		email = args['email']
		password_hash = args['password_hash']

		if User.find_by_username(username, self.mongo):
			return {"message": f"User with username [{username}] already exists"}, 400

		user = User(username, email, password_hash)
		user_id = user.save(self.mongo)

		return {'message': 'User created', 'user_id': user_id}, 201

	def delete(self):
		"""
		Delete multiple users.

		Returns:
			dict: A message indicating the result of the deletion.
		"""
		data = request.get_json()
		if not data:
			return {"message": "No data provided in the request body"}, 400

		usernames = data.get("usernames", [])
		if not usernames:
			return {"message": "No usernames provided in the request"}, 400

		deleted_count = 0
		for username in usernames:
			user = User.find_by_username(username, self.mongo)
			if user:
				self.mongo.db.users.delete_one({'_id': user._id})
				deleted_count += 1

		return {"message": f"{deleted_count} users deleted"}, 200

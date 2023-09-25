from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from api.models.User import User  # Import your User model

signup_parser = reqparse.RequestParser()
signup_parser.add_argument('username', type=str, required=True, help='Username')
signup_parser.add_argument('email', type=str, required=True, help='Email')
signup_parser.add_argument('password', type=str, required=True, help='Password')

# Request parser for user data
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username')
user_parser.add_argument('password', type=str, required=True, help='Password')
user_parser.add_argument('email', type=str, required=True, help='Email')
user_parser.add_argument('verified', type=bool, required=False, default=False, help='User verification status')

# Define the fields for marshaling user data in responses
user_fields = {
	'user_id': fields.String(attribute='user_id'),
	'username': fields.String,
	'email': fields.String,
	'password': fields.String,
}


class UserListResource(Resource):


	@marshal_with(user_fields)
	def get(self):
		"""
		Get a list of all users.
		Returns:
			List[User]: A list of all users.
		"""

		users_data = User.getAll()
		if users_data:
			users = [User.from_dict(user_data) for user_data in users_data]
			return users, 200
		else:
			return {"message": "Users not found"}, 404
		
	def post(self):

		data = signup_parser.parse_args()
		username = data['username']
		email = data['email']
		password = data['password']

		# Check if the username or email is already in use
		if User.find_by_name(username)[0]:
			return {'message': 'Username or email already in use'}, 400

		# Create a new user
		new_user = User(username=username, email=email, password=password)
		result = new_user.create_database_entry()
		
		print("XXXXXX")
		print(result)

		if result:
			#access_token = create_access_token(identity=new_user.user_id)

			# Return the token and a success message
			return {'success': True, 'message': 'User registration successful'}, 201
		else:
			return {'success': False, 'message': 'User registration failed'}, 500
		
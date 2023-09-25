from flask import request
from flask_restful import Resource, reqparse
from api.models.User import User
from flask_jwt_extended import create_access_token


signup_parser = reqparse.RequestParser()
signup_parser.add_argument('username', type=str, required=True, help='Username')
signup_parser.add_argument('email', type=str, required=True, help='Email')
signup_parser.add_argument('password', type=str, required=True, help='Password')

class UserSignupResource(Resource):
	def post(self):

		print("XXXX")
		data = signup_parser.parse_args()
		username = data['username']
		email = data['email']
		password = data['password']

		print("2XXXX")

		user_dict, code = User.find_by_name(username)
		# Check if the username or email is already in use
		if code == 200:
			return {'message': 'Username or email already in use'}, 400

		# Create a new user
		new_user = User(username=username, email=email, password=password)
		result = new_user.create_database_entry()
		
		print(result)

		if result:
			#access_token = create_access_token(identity=new_user.user_id)

			# Return the token and a success message
			return {'success': True, 'message': 'User registration successful'}, 201
		else:
			return {'success': False, 'message': 'User registration failed'}, 500
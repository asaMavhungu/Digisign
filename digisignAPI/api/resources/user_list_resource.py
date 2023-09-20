from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from api.models.User import User  # Import your User model

# Request parser for user data
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username')
user_parser.add_argument('password', type=str, required=True, help='Password')
user_parser.add_argument('email', type=str, required=True, help='Email')
user_parser.add_argument('verified', type=bool, required=False, default=False, help='User verification status')

# Define the fields for marshaling user data in responses
user_fields = {
    'id': fields.String(attribute='_id'),
    'username': fields.String,
    'email': fields.String,
    'verified': fields.Boolean,
}

class UserListResource(Resource):


    @marshal_with(user_fields)
    def get(self):
        """
        Get a list of all users.
        Returns:
            List[User]: A list of all users.
        """

        users_data = User.get_all()
        if users_data:
            users = [User.from_dict(user_data) for user_data in users_data]
            return users, 200
        else:
            return {"message": "Users not found"}, 404
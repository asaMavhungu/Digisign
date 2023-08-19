from flask import request
from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from api.models.User import User
from flask import current_app as app

bcrypt = Bcrypt()

user_login_args = reqparse.RequestParser()
user_login_args.add_argument("username", type=str, help="Username is required", required=True)
user_login_args.add_argument("email", type=str, help="Email is required", required=True)
user_login_args.add_argument("password", type=str, help="Password is required", required=True)

class UserLoginResource(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def post(self):
        args = user_login_args.parse_args()
        username = args["username"]
        password = args["password"]

        # Find the user by username
        user_dict = User.find_by_username(username, self.mongo)

        if user_dict:
            # Verify the password
            stored_password_hash = user_dict.get('password_hash')
            if bcrypt.check_password_hash(stored_password_hash, password):
                return {"message": "Login successful", "user_id": str(user_dict['_id'])}, 200
            else:
                return {"message": "Invalid password"}, 401
        else:
            return {"message": "User not found"}, 404

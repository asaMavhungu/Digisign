from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request
from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from api.models.User import User
from flask import current_app as app

bcrypt = Bcrypt()

user_login_args = reqparse.RequestParser()
user_login_args.add_argument("username", type=str, help="Username is required", required=True)
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
                # Create a JWT token
                access_token = create_access_token(identity=str(user_dict['_id']))

                return {"message": "Login successful", "access_token": access_token}, 200
            else:
                return {"message": "Invalid password"}, 401
        else:
            return {"message": "User not found"}, 404

# Example protected resource that requires a valid JWT token
class ProtectedResource(Resource):
    @jwt_required() # so this means that to access this i need an access token?
    def get(self):
        # This resource is protected by JWT authentication
        current_user_id = get_jwt_identity() 
        return {"message": "This is a protected resource for user ID: " + current_user_id}, 200
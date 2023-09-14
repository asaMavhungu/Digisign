from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt

class User:
	def __init__(self, username, email, password_hash=None):
		"""
		Constructor for the User class.

		:param username: The username of the user.
		:param email: The email address of the user.
		:param password_hash: The hashed password of the user (default is None).
		"""
		self._id = None  # MongoDB ObjectId (optional)
		self.username = username
		self.email = email
		self.password_hash = password_hash  # You may want to store hashed passwords

	@classmethod
	def from_dict(cls, user_dict):
		"""
		Creates a User instance from a dictionary.

		:param user_dict: A dictionary containing user data.
		:return: An instance of the User class.
		"""
		user = cls(
			username=user_dict.get('username'),
			email=user_dict.get('email'),
			password_hash=user_dict.get('password_hash')
		)
		user._id = user_dict.get('_id')  # Optional ObjectId
		return user

	def to_dict(self):
		"""
		Converts the User instance to a dictionary.

		:return: A dictionary representation of the user instance.
		"""
		user_dict = {
			'_id': self._id,
			'username': self.username,
			'email': self.email,
			'password_hash': self.password_hash
		}
		return user_dict

	@staticmethod
	def find_by_username(username, mongo):
		"""
		Finds a user by their username in the database.

		:param username: The username to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: A user document from the database with the specified username or None if not found.
		"""
		user_data = mongo.db.users.find_one({'username': username})
		if user_data:
			return User.from_dict(user_data)
		return None

	@staticmethod
	def find_by_id(user_id, mongo):
		"""
		Finds a user by their unique user ID (ObjectId) in the database.

		:param user_id: The unique identifier of the user.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: A user document from the database with the specified user ID or None if not found.
		"""
		user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
		if user_data:
			return User.from_dict(user_data)
		return None

	def verify_password(self, password):
		"""
		Verify the user's password.

		:param password: The password to verify.
		:return: True if the password is correct, False otherwise.
		"""
		bcrypt = Bcrypt()
		if self.password_hash:
			return bcrypt.check_password_hash(self.password_hash, password)
		return False

	def save(self, mongo):
		"""
		Saves the user instance to the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: The unique identifier (_id) of the inserted user document.
		"""
		user_data = self.to_dict()
		result = mongo.db.users.insert_one(user_data)
		self._id = result.inserted_id  # Set the _id attribute to the inserted ObjectId
		return str(self._id)

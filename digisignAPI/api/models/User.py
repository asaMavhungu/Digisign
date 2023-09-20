from bson.objectid import ObjectId
import database.Database_utils as db_client
import hashlib


class User:
	def __init__(self, username: str, password: str, email: str, verified: bool = False):
		"""
		Constructor for the User class.

		:param username: The username of the user.
		:param password: The hashed password of the user.
		:param email: The email address of the user.
		:param verified: A boolean indicating whether the user is verified.
		"""
		self._id = None  # MongoDB ObjectId (optional)
		self.username = username
		self.password = password
		self.email = email
		self.verified = verified

	@classmethod
	def from_dict(cls, user_dict):
		"""
		Creates a User instance from a dictionary.

		:param user_dict: A dictionary containing user data.
		:return: An instance of the User class.
		"""
		user = cls(
			username=user_dict['username'],
			password=user_dict['password'],
			email=user_dict['email'],
			verified=user_dict.get('verified', False)
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
			'password': self.password,
			'email': self.email,
			'verified': self.verified
		}
		return user_dict

	@staticmethod
	def find_by_username(username: str) -> (dict | None):
		"""
		Finds a user by their username in the database.

		:param username: The username of the user to search for.
		:param database_client: An instance of DatabaseClient used for database operations.
		:return: User dict or None if not found.
		"""
		return db_client.get_one('users', 'username', username) # type: ignore

	@staticmethod
	def find_by_email(email: str) -> (dict | None):
		"""
		Finds a user by their email address in the database.

		:param email: The email address of the user to search for.
		:param database_client: An instance of DatabaseClient used for database operations.
		:return: User dict or None if not found.
		"""
		return db_client.get_one('users', 'email', email) # type: ignore

	def save(self):
		"""
		Saves the user instance to the database.

		:param database_client: The DatabaseClient instance for database operations.
		:return: The unique identifier (_id) of the inserted or updated user document.
		"""
		user_data = self.to_dict()
		print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
		print(user_data)
		print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
		if self._id:
			return db_client.update_entry('users', '_id', self._id, user_data)
		else:
			return db_client.insert_entry('users', user_data)

	@staticmethod
	def get_all():
		"""
		Get all users from the database.

		:param database_client: The DatabaseClient instance for database operations.
		:return: List of user dictionaries.
		"""
		return db_client.get_table('users')

	def delete(self):
		"""
		Deletes the user from the database.

		:param database_client: The DatabaseClient instance for database operations.
		:return: True if the user is deleted, False otherwise.
		"""
		if self._id:
			return db_client.delete_entry('users', 'username', self.username)
		return False
	
	@staticmethod
	def verify_credentials(username: str, password: str):
		"""
		Verifies user credentials against the database.

		:param username: The username of the user.
		:param password: The password provided by the user (not hashed).
		:param database_client: An instance of DatabaseClient used for database operations.
		:return: User dict if credentials are valid, None otherwise.
		"""
		user_dict = db_client.get_one('users', 'username', username)  # Fetch user by username

		if user_dict and User.check_password(password, user_dict['password']):# type: ignore
			return user_dict  # Return user data if credentials are valid 

		return None  # Return None if credentials are invalid

	@staticmethod
	def check_password(input_password: str, hashed_password: str) -> bool:
		"""
		Checks if the input password matches the hashed password.

		:param input_password: The input password provided by the user (not hashed).
		:param hashed_password: The hashed password stored in the database.
		:return: True if passwords match, False otherwise.
		"""
		# TODO BRING BACK HASHING
		return input_password == hashed_password
		# Hash the input password and compare it to the stored hashed password
		return User.hash_password(input_password) == hashed_password

	@staticmethod
	def hash_password(password: str) -> str:
		"""
		Hashes a password using SHA-256.

		:param password: The password to hash.
		:return: The hashed password.
		"""
		salt = b'some_salt_value'  # Replace with your actual salt value
		password_bytes = password.encode('utf-8')
		hashed_password = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
		return hashed_password.hex()
	
	@staticmethod
	def get_user_identity(username: str, password: str):
		"""
		Get the user's identity (e.g., username) based on credentials.

		:param username: The username provided by the user.
		:param password: The password provided by the user (not hashed).
		:param database_client: An instance of DatabaseClient used for database operations.
		:return: User identity (e.g., username) if credentials are valid, None otherwise.
		"""
		user_dict = db_client.get_one('users', 'username', username)

		if user_dict and User.check_password(password, user_dict['password']): # type: ignore
			return username

		return None



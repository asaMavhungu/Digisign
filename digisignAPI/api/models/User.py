import database.sql_utils as sql_client

class User:
	def __init__(self, username, user_id=None, email=None, password=None):
		"""
		Constructor for the User class.

		:param username: The username of the user.
		:param user_id: The user ID (optional).
		:param email: The email of the user (optional).
		:param password: The password of the user (optional).
		:param slide_ids: List of slide IDs associated with the user (optional).
		:param user_slide_ids: List of user slide IDs (optional).
		"""
		self.user_id: str | None = user_id
		self.username: str = username
		self.email: str | None = email
		self.password: str | None = password

	def __repr__(self):
		return f"<User(user_id={self.user_id}, username='{self.username}', email='{self.email}')>"

	def to_dict(self):
		return {
			'user_id': self.user_id,
			'username': self.username,
			'email': self.email,
			'password': self.password,
		}

	@classmethod
	def from_dict(cls, data):
		user_id = data.get('user_id')
		username = data.get('username')
		email = data.get('email')
		password = data.get('password')
		return cls(username, user_id=user_id, email=email, password=password)
	
	@staticmethod
	def get_user_identity(username, password):

		user_dict, code = sql_client.get_entry('users', {'username': username,})

		if code == 200:
			return User.from_dict(user_dict)  
		
		print(user_dict, code)

		return None

	@staticmethod
	def getAll():
		"""
		Get all the slides in the db
		"""
		result = sql_client.get_table_data('users')
		print(result)
		if result:
			return result
		
	@staticmethod
	def find_by_name(user_name: str):

		result, code = sql_client.get_entry('users', {'username': user_name,})

		return result, code
	
	def create_database_entry(self):
		result = sql_client.create_entry('users', data = {
			'username': self.username,  # Replace with your actual data
			'email': self.email,
			'password': self.password,
			# Add other fields as needed
		} )

		return result
	
	def update_database_entry(self, data: dict):

		if 'username' in data:
			self.department_name = data['username']
		result = sql_client.update_entry('users', 
				filter_dict={'user_id': self.user_id},
				data = data
			)
		
		return result
	
	def delete_database_entry(self):
		result = sql_client.delete_entry('users', 
				filter_dict={'user_id': self.user_id}
			)
		
		return result
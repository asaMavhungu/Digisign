from bson.objectid import ObjectId
from database.DatabaseClient import DatabaseClient


class Slide:
	def __init__(self, title: str, content: str, content_type: str, author_id: str):
		"""
		Constructor for the Slide class.

		:param title: The title of the slide.
		:param content: The content of the slide.
		:param author_id: The unique identifier of the author (user) of the slide.
		"""
		self._id = None  # MongoDB ObjectId (optional)
		self.title = title
		self.content = content
		self.content_type = content_type
		self.author_id = author_id
		self.departments = []  # List to store associated department names

	def add_department(self, department_name):
		"""
		Add a department ObjectId to the slide's list of associated departments.

		:param department_id: The ObjectId of the department to be associated with the slide.
		"""
		if department_name not in self.departments:
			self.departments.append(department_name)

	def remove_department(self, department_name):
		"""
		Remove a department ObjectId from the slide's list of associated departments.

		:param department_id: The ObjectId of the department to be disassociated from the slide.
		"""
		if department_name in self.departments:
			self.departments.remove(department_name)

	def clear_departments(self):
		self.departments = []

	@classmethod
	def from_dict(cls, slide_dict):
		"""
		Creates a Slide instance from a dictionary.

		:param slide_dict: A dictionary containing slide data.
		:return: An instance of the Slide or VideoSlide class, depending on content_type.
		"""
		slide = cls(
			title=slide_dict['title'],
			content=slide_dict['content'],
			content_type=slide_dict['content_type'],
			author_id=slide_dict['author_id']
		)
		slide._id = slide_dict.get('_id')  # Optional ObjectId
		slide.departments = slide_dict.get('departments', [])
		return slide

	def to_dict(self):
		"""
		Converts the Slide instance to a dictionary.

		:return: A dictionary representation of the slide instance.
		"""
		slide_dict = {
			'title': self.title,
			'content': self.content,
			'content_type': self.content_type,
			'author_id': self.author_id,
			'departments': self.departments,
		}
		return slide_dict

	def to_marshal_representation(self):
		"""
		Convert the Slide object to a marshal-like representation.
		"""
		return {
			'_id': self._id,
			'title': self.title,
			'content': self.content,
			'content_type': self.content_type,
			'author_id': self.author_id,
			'departments': self.departments,
		}

	@staticmethod
	def find_by_title(title: str, database_client: DatabaseClient) -> (dict | None):
		print("==========================")
		# TODO Remove redundancy of creating Slide object
		"""
		Finds slides by their title in the database.

		:param title: The title of the slide to search for.
		:param client: An instance of SlideClient used for database operations.
		:return: slide dict
		"""
		return database_client.get_one('slides', 'title', title)

	def save(self, database_client: DatabaseClient):
		"""
		Saves the slide instance to the database.

		:param slides_table: The table to update.
		:return: The unique identifier (_id) of the inserted or updated slide document.
		"""
		slide_data = self.to_dict()
		if self._id:
			return database_client.update_entry('slides', 'title', self.title, slide_data)
		else:
			return database_client.insert_entry('slides', slide_data)
		
	
	@staticmethod
	def getAll(database_client: DatabaseClient):
		"""
		Get all the slides in the db
		"""
		return database_client.get_table('slides')
	
	def delete_me(self, database_client: DatabaseClient):
		database_client.delete_entry('slides', 'title', self.title)

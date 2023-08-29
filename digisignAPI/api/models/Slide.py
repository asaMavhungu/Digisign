from flask_pymongo import PyMongo
from bson.objectid import ObjectId

class Slide:
	def __init__(self, title, content, author_id):
		"""
		Constructor for the Slide class.

		:param title: The title of the slide.
		:param content: The content of the slide.
		:param author_id: The unique identifier of the author (user) of the slide.
		"""
		self._id = None  # MongoDB ObjectId (optional)
		self.title = title
		self.content = content
		self.author_id = author_id
		self.departments = []  # List to store associated department ObjectIds

	def add_department(self, department_id):
		"""
		Add a department ObjectId to the slide's list of associated departments.

		:param department_id: The ObjectId of the department to be associated with the slide.
		"""
		self.departments.append(department_id)

	def remove_department(self, department_id):
		"""
		Remove a department ObjectId from the slide's list of associated departments.

		:param department_id: The ObjectId of the department to be disassociated from the slide.
		"""
		if department_id in self.departments:
			self.departments.remove(department_id)

	@classmethod
	def from_dict(cls, slide_dict):
		"""
		Creates a Slide instance from a dictionary.

		:param slide_dict: A dictionary containing slide data.
		:return: An instance of the Slide class.
		"""
		slide = cls(
			title=slide_dict['title'],
			content=slide_dict['content'],
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
			'author_id': self.author_id,
			'departments': self.departments
		}
		return slide_dict

	@staticmethod
	def find_by_id(slide_id, mongo):
		"""
		Finds a slide by its unique slide ID (ObjectId) in the database.

		:param slide_id: The unique identifier of the slide.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Slide class or None if not found.
		"""
		slide_data = mongo.db.slides.find_one({'_id': ObjectId(slide_id)})
		if slide_data:
			return Slide.from_dict(slide_data)
		return None

	@staticmethod
	def find_by_title(title, mongo):
		"""
		Finds slides by their title in the database.

		:param title: The title of the slide to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: A list of instances of the Slide class matching the title or an empty list if not found.
		"""
		slide_data = mongo.db.slides.find_one({'title': title})
		if slide_data:
			return Slide.from_dict(slide_data)
		return None

	def save(self, mongo):
		"""
		Saves the slide instance to the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: The unique identifier (_id) of the inserted or updated slide document.
		"""
		slide_data = self.to_dict()
		if self._id:
			# Update the existing slide document
			mongo.db.slides.update_one({'_id': self._id}, {'$set': slide_data})
			return self._id
		else:
			# Insert a new slide document
			result = mongo.db.slides.insert_one(slide_data)
			self._id = result.inserted_id
			return str(result.inserted_id)
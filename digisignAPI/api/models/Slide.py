from flask_pymongo import PyMongo
from bson.objectid import ObjectId

class Slide:
	def __init__(self, title, content, content_type, author_id):
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
		self.device_groups = []  # List to store associated device group names

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

	def add_device_group(self, device_group_name):
		"""
		Add a device group ObjectId to the slide's list of associated device groups.

		:param device_group_id: The ObjectId of the device group to be associated with the slide.
		"""
		if device_group_name not in self.device_groups:
			self.device_groups.append(device_group_name)

	def remove_device_group(self, device_group_name):
		"""
		Remove a device group ObjectId from the slide's list of associated device groups.

		:param device_group_id: The ObjectId of the device group to be disassociated from the slide.
		"""
		if device_group_name in self.device_groups:
			self.device_groups.remove(device_group_name)

	def clear_device_groups(self):
		self.device_groups = []

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
			content_type=slide_dict['content_type'],
			author_id=slide_dict['author_id']
		)
		slide._id = slide_dict.get('_id')  # Optional ObjectId
		slide.departments = slide_dict.get('departments', [])
		slide.device_groups = slide_dict.get('device_groups', []) # does this
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
			'device_groups': self.device_groups
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
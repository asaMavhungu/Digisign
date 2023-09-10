from flask_pymongo import PyMongo
from bson.objectid import ObjectId

class Department:
	def __init__(self, name):
		"""
		Constructor for the Department class.

		:param name: The name of the department.
		"""
		self._id = None  # MongoDB ObjectId (optional)
		self.name = name
		self.slides = []  # List to store associated slides
		self.devices = []  # List to store associated devices

	def add_slide(self, slide_name):
		"""
		Add a slide to the department.

		:param slide: The Slide name to associate with the department.
		"""
		self.slides.append(slide_name)

	def remove_slide(self, slide_name):
		"""
		Remove a slide from the department.

		:param slide: The Slide name to disassociate from the department.
		"""
		self.slides.remove(slide_name)

	def add_device(self, device_name):
		"""
		Add a device to the department.

		:param device: The Device name to associate with the department.
		"""
		self.devices.append(device_name)

	def remove_device(self, device_name):
		"""
		Remove a device from the department.

		:param device: The Device name to disassociate from the department.
		"""
		self.devices.remove(device_name)

	@classmethod
	def from_dict(cls, department_dict):
		"""
		Creates a Department instance from a dictionary.

		:param department_dict: A dictionary containing department data.
		:return: An instance of the Department class.
		"""
		department = cls(
			name=department_dict['name']
		)
		department._id = department_dict.get('_id')  # Optional ObjectId
		department.slides = department_dict.get('slides', [])
		department.devices = department_dict.get('devices', [])
		return department

	def to_dict(self):
		"""
		Converts the Department instance to a dictionary.

		:return: A dictionary representation of the department instance.
		"""
		department_dict = {
			'name': self.name,
			'slides': self.slides,  # Include associated slide ObjectIds
			'devices': self.devices  # Include associated device ObjectIds
		}
		return department_dict

	@staticmethod
	def find_by_id(department_id, mongo):
		"""
		Finds a department by its unique department ID (ObjectId) in the database.

		:param department_id: The unique identifier of the department.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Department class or None if not found.
		"""
		department_data = mongo.db.departments.find_one({'_id': ObjectId(department_id)})
		if department_data:
			return Department.from_dict(department_data)
		return None

	@staticmethod
	def find_by_name(department_name, mongo):
		"""
		Finds a department by its name in the database.

		:param department_name: The name of the department to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Department class or None if not found.
		"""
		department_data = mongo.db.departments.find_one({'name': department_name})
		if department_data:
			return Department.from_dict(department_data)
		return None

	def save(self, mongo):
		"""
		Saves the department instance to the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: The unique identifier (_id) of the inserted or updated department document.
		"""
		department_data = self.to_dict()
		if self._id:
			# Update the existing department document
			mongo.db.departments.update_one({'_id': self._id}, {'$set': department_data})
			return self._id
		else:
			# Insert a new department document
			result = mongo.db.departments.insert_one(department_data)
			self._id = result.inserted_id
		return str(self._id)

	def delete(self, mongo):
		"""
		Deletes the department from the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		"""
		if self._id:
			mongo.db.departments.delete_one({'_id': self._id})

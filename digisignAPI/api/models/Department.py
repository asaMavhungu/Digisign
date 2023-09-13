from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from database.DatabaseTable import DatabaseTable

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
	def find_by_id(department_id, department_table: DatabaseTable):
		"""
		Finds a department by its unique department ID (ObjectId) in the database.

		:param department_id: The unique identifier of the department.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Department class or None if not found.
		"""
		return department_table.find_by_id(department_id)

	@staticmethod
	def find_by_name(department_name: str, department_table: DatabaseTable):
		"""
		Finds a department by its name in the database.

		:param department_name: The name of the department to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Department class or None if not found.
		"""
		return department_table.find_by_title(department_name)

	def save(self, department_table: DatabaseTable):
		"""
		Saves the department instance to the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: The unique identifier (_id) of the inserted or updated department document.
		"""
		department_data = self.to_dict()
		if self._id:
			# Update the existing department document
			return department_table.update_one(self._id, department_data)
		else:
			# Insert a new department document
			return department_table.insert_one(department_data)

	@staticmethod
	def getAll(slides_table: DatabaseTable):
		"""
		Get all the slides in the db
		"""
		return slides_table.getData()
	
	def delete_me(self, slides_table: DatabaseTable):
		slides_table.delete_one(self._id) # type: ignore #TODO TYPE IGNORE HERER

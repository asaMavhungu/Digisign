

import database.Database_utils as db_client



class Device:
	def __init__(self, name, description):
		"""
		Constructor for the Device class.

		:param name: The name of the device.
		"""
		self._id = None  # MongoDB ObjectId (optional)
		self.name = name
		self.description = description
		self.slides = []  # List to store associated slides
		self.departments = []

	def add_slide(self, slide_name):
		"""
		Add a slide to the device.

		:param slide: The Slide object to associate with the device.
		"""
		self.slides.append(slide_name)

	def remove_slide(self, slide_name):
		"""
		Remove a slide from the device.

		:param slide: The Slide object to disassociate from the device.
		"""
		self.slides.remove(slide_name)
		
	def add_department(self, department_name):
		"""
		Add a device to the department.

		:param device: The department name to associate with the department.
		"""
		self.departments.append(department_name)

	def remove_department(self, department_name):
		"""
		Remove a device from the department.

		:param device: The department name to disassociate from the department.
		"""
		self.departments.remove(department_name)

	@classmethod
	def from_dict(cls, device_dict):
		"""
		Creates a Device instance from a dictionary.

		:param device_dict: A dictionary containing device data.
		:return: An instance of the Device class.
		"""
		device = cls(
			name=device_dict['name'],
			description=device_dict['description']
		)
		device._id = device_dict.get('_id')  # Optional ObjectId
		device.slides = device_dict.get('slides', [])
		device.departments = device_dict.get('departments', [])
		return device

	def to_dict(self):
		"""
		Converts the Device instance to a dictionary.

		:return: A dictionary representation of the device instance.
		"""
		device_dict = {
			'_id': self._id,
			'name': self.name,
			'description': self.description,
			'slides': self.slides,  # Include associated slide ObjectIds
			'departments': self.departments
		}
		return device_dict
	
	def to_marshal_representation(self):
		"""
		Convert the Device object to a marshal-like representation.
		"""
		return {
			'_id': self._id,
			'name': self.name,
			'description': self.description,
			'slides': self.slides,
			'departments': self.departments
		}

	@staticmethod
	def getAll():
		"""
		Get all the slides in the db
		"""
		return db_client.get_table('devices')

	@staticmethod
	def find_by_name(device_name):
		"""
		Finds devices by their name in the database.

		:param name: The name of the device to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: A list of instances of the Device class matching the name or an empty list if not found.
		"""
		return db_client.get_one('devices', 'name', device_name)

	def save(self):
		"""
		Saves the device instance to the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: The unique identifier (_id) of the inserted or updated device group document.
		"""
		device_data = self.to_dict()
		if self._id:
			# Update the existing device document
			return db_client.update_entry('devices', 'name', self.name, device_data)
		else:
			# Insert a new device document
			return db_client.insert_entry('devices', device_data)
	
	def delete_me(self):
		db_client.delete_entry('devices', 'name', self.name)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from database.DatabaseTable import DatabaseTable

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

	def add_slide(self, slide):
		"""
		Add a slide to the device.

		:param slide: The Slide object to associate with the device.
		"""
		self.slides.append(slide)

	def remove_slide(self, slide):
		"""
		Remove a slide from the device.

		:param slide: The Slide object to disassociate from the device.
		"""
		self.slides.remove(slide)
		

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
		return device

	def to_dict(self):
		"""
		Converts the Device instance to a dictionary.

		:return: A dictionary representation of the device instance.
		"""
		device_dict = {
			'name': self.name,
			'description': self.description,
			'slides': self.slides  # Include associated slide ObjectIds
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
		}


	@staticmethod
	def find_by_id(device_id, device_table: DatabaseTable):
		"""
		Finds a device by its unique device ID (ObjectId) in the database.

		:param device_id: The unique identifier of the device.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Device class or None if not found.
		"""
		return device_table.find_by_id(device_id)

	@staticmethod
	def find_by_name(device_name, device_table: DatabaseTable):
		"""
		Finds devices by their name in the database.

		:param name: The name of the device to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: A list of instances of the Device class matching the name or an empty list if not found.
		"""
		return device_table.find_by_title(device_name)

	def save(self, device_table: DatabaseTable):
		"""
		Saves the device instance to the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: The unique identifier (_id) of the inserted or updated device group document.
		"""
		device_data = self.to_dict()
		if self._id:
			# Update the existing device document
			return device_table.update_one(self._id, device_data)
		else:
			# Insert a new device document
			return device_table.insert_one(device_data)
	
	def delete(self, mongo):
		"""
		Deletes the device from the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		"""
		if self._id:
			mongo.db.devices.delete_one({'_id': self._id})

	def delete_me(self, device_table: DatabaseTable):
		device_table.delete_one(self._id) # type: ignore #TODO TYPE IGNORE HERER

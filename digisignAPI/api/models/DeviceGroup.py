from flask_pymongo import PyMongo
from bson.objectid import ObjectId

class DeviceGroup:
	def __init__(self, name, description):
		"""
		Constructor for the DeviceGroup class.

		:param name: The name of the device group.
		"""
		self._id = None  # MongoDB ObjectId (optional)
		self.name = name
		self.description = description
		self.slides = []  # List to store associated slides

	def add_slide(self, slide):
		"""
		Add a slide to the device group.

		:param slide: The Slide object to associate with the device group.
		"""
		self.slides.append(slide)

	def remove_slide(self, slide):
		"""
		Remove a slide from the device group.

		:param slide: The Slide object to disassociate from the device group.
		"""
		self.slides.remove(slide)
		

	@classmethod
	def from_dict(cls, device_group_dict):
		"""
		Creates a DeviceGroup instance from a dictionary.

		:param device_group_dict: A dictionary containing device group data.
		:return: An instance of the DeviceGroup class.
		"""
		device_group = cls(
			name=device_group_dict['name'],
			description=device_group_dict['description']
		)
		device_group._id = device_group_dict.get('_id')  # Optional ObjectId
		device_group.slides = device_group_dict.get('slides', [])
		return device_group

	def to_dict(self):
		"""
		Converts the DeviceGroup instance to a dictionary.

		:return: A dictionary representation of the device group instance.
		"""
		device_group_dict = {
			'name': self.name,
			'description': self.description,
			'slides': self.slides  # Include associated slide ObjectIds
		}
		return device_group_dict

	@staticmethod
	def find_by_id(device_group_id, mongo):
		"""
		Finds a device group by its unique device group ID (ObjectId) in the database.

		:param device_group_id: The unique identifier of the device group.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the DeviceGroup class or None if not found.
		"""
		device_group_data = mongo.db.device_groups.find_one({'_id': ObjectId(device_group_id)})
		if device_group_data:
			return DeviceGroup.from_dict(device_group_data)
		return None

	@staticmethod
	def find_by_name(name, mongo):
		"""
		Finds device groups by their name in the database.

		:param name: The name of the device group to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: A list of instances of the DeviceGroup class matching the name or an empty list if not found.
		"""
		device_group_data = mongo.db.device_groups.find_one({'name': name})
		if device_group_data:
			return DeviceGroup.from_dict(device_group_data)
		return None

	def save(self, mongo):
		"""
		Saves the device group instance to the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: The unique identifier (_id) of the inserted or updated device group document.
		"""
		device_group_data = self.to_dict()
		if self._id:
			# Update the existing device group document
			mongo.db.device_groups.update_one({'_id': self._id}, {'$set': device_group_data})
			return self._id
		else:
			# Insert a new device group document
			result = mongo.db.device_groups.insert_one(device_group_data)
			self._id = result.inserted_id
		return str(self._id)
	
	def delete(self, mongo):
		"""
		Deletes the device group from the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		"""
		if self._id:
			mongo.db.device_groups.delete_one({'_id': self._id})

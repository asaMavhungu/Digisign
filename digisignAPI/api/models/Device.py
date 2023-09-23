

import database.Database_utils as db_client
import database.sql_utils as sql_client


class Device:
	def __init__(self, device_id, device_name, department_id):
		self.device_id = device_id
		self.device_name = device_name
		self.department_id = department_id
		self.slides_assigned = []  # List to hold assigned Slide objects

	def __repr__(self):
		return f"<Device(device_id={self.device_id}, device_name='{self.device_name}', department_id={self.department_id}, slides_assigned={self.slides_assigned})>"

	@classmethod
	def from_dict(cls, data):
		device_id = data.get("device_id")
		device_name = data.get("device_name")
		department_id = data.get("department_id")

		assignments = data.get("assignments", [])
		slide_ids = [assignment["slide_id"] for assignment in assignments]

		device = cls(device_id, device_name, department_id)
		device.slides_assigned = slide_ids

		return device
	
	@staticmethod
	def getAll():
		"""
		Get all the slides in the db
		"""
		return sql_client.get_table_data('devices')

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
	def getAll2():
		"""
		Get all the slides in the db
		"""
		return sql_client.get_table_data('devices')
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
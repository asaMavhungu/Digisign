

import database.Database_utils as db_client
import database.sql_utils as sql_client


class Device:
	def __init__(self, device_name, device_id=None, department_id=None, slide_ids=None):
		"""
		Constructor for the Device class.

		:param device_id: The ID of the device.
		:param device_name: The name of the device.
		:param department_id: The ID of the department to which the device belongs.
		:param slide_ids: List of slide IDs assigned to this device (optional).
		"""
		self.device_id: str | None = device_id
		self.device_name: str = device_name
		self.department_id: str | None = department_id
		self.slide_ids = slide_ids or []

	def __repr__(self):
		return f"<Device(device_id={self.device_id}, device_name='{self.device_name}', department_id={self.department_id}, slide_ids={self.slide_ids})>"
	
	
	@staticmethod
	def find_by_name(device_name: str):
		"""
		Finds a department by its name in the database.

		:param department_name: The name of the department to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Department class or None if not found.
		"""
		result, code = sql_client.get_entry('devices', {'device_name': device_name,})
		if code == 404:
			return result, code
		
		device_dict = {
			'device_id': result['device_id'],
			'device_name': result['device_name'],
			'department_id': result['department_id'],
			'slide_ids': [assignment['assignment_id'] for assignment in result['assignments']]
		}

		return device_dict, code
	
	
	@classmethod
	def from_dict(cls, data):
		device_id = data.get("device_id")
		device_name = data.get("device_name")
		department_id = data.get("department_id")
		slide_ids = data.get("slide_ids", [])

		return cls(device_name, device_id, department_id, slide_ids)

	def to_dict(self):
		return {
			"device_id": self.device_id,
			"device_name": self.device_name,
			"department_id": self.department_id,
			"slide_ids": self.slide_ids
		}
	
	@classmethod
	def extract_mult_devices_info(cls, data_list):
		devices = []

		for data in data_list:
			device_id = data.get("device_id")
			device_name = data.get("device_name")
			department_id = data.get("department_id")
			assignments_data = data.get("assignments", [])

			slide_ids = [str(assignment.get("slide_id")) for assignment in assignments_data]

			device_info = {
				"device_id": device_id,
				"device_name": device_name,
				"department_id": department_id,
				"slide_ids": slide_ids
			}

			devices.append(device_info)

		return devices
	
	@classmethod
	def extract_device_info(cls, data):

		device_id = data.get("device_id")
		device_name = data.get("device_name")
		department_id = data.get("department_id")
		slide_ids = data.get("slide_ids", [])

		device_info = {
			"device_id": device_id,
			"device_name": device_name,
			"department_id": department_id,
			"slide_ids": slide_ids
		}

		return device_info
	

	@staticmethod
	def getAll():
		"""
		Get all the slides in the db
		"""
		return sql_client.get_table_data('devices')
	
	def create_database_entry(self):
		result = sql_client.create_entry('devices', data = {
			'device_name': self.device_name,  # Replace with your actual data
			# Add other fields as needed
		} )

		return result
	
	def update_database_entry(self, data: dict):

		if 'department_name' in data:
			self.department_name = data['device_name']
		result = sql_client.update_entry('devices', 
				filter_dict={'device_name': self.device_name},
				data = data
			)
		
		return result
	
	def delete_database_entry(self):
		result = sql_client.delete_entry('devices', 
				filter_dict={'device_name': self.device_name}
			)
		
		return result

	def to_dict_depracated(self):
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
	def getAll_depracated():
		"""
		Get all the slides in the db
		"""
		return sql_client.get_table_data('devices')
		return db_client.get_table('devices')

	@staticmethod
	def find_by_name_depracated(device_name):
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


import database.Database_utils as db_client
import database.sql_utils as sql_client


class Device:
	def __init__(self, device_name, device_id=None, department_id=None, slide_ids=None, slide_names=None, slide_urls=None):
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
		self.slide_names = slide_names or []
		self.slide_urls = slide_urls or []

	def __repr__(self):
		return f"<Device(device_id={self.device_id}, device_name='{self.device_name}', department_id={self.department_id}, slide_ids={self.slide_ids}, slide_names={self.slide_names}, slide_urls={self.slide_urls})>"
	
	
	@staticmethod
	def find_by_name(device_name: str):
		"""
		Finds a department by its name in the database.

		:param department_name: The name of the department to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Department class or None if not found.
		"""
		result, code = sql_client.get_entry('devices', {'device_name': device_name,})
		print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
		print(result)
		if code == 404:
			return result, code
		
		#TODO 'result' is ALWAYS in an expected format

		device_dict = {
			'device_id': result['device_id'],
			'device_name': result['device_name'],
			'department_id': result['department_id'],
			'slide_ids': [assignment['assignment_id'] for assignment in result['assignments']], #type: ignore
			'slide_names': [assignment['slide_name'] for assignment in result['assignments']], #type: ignore
			'slide_urls': [assignment['slide_url'] for assignment in result['assignments']] #type: ignore
		}

		return device_dict, code
	
	
	@classmethod
	def from_dict(cls, data):
		device_id = data.get("device_id")
		device_name = data.get("device_name")
		department_id = data.get("department_id")
		slide_ids = data.get("slide_ids", [])
		slide_names = data.get("slide_names", [])
		slide_urls = data.get("slide_urls", [])

		return cls(device_name=device_name, device_id=device_id, department_id=department_id, slide_ids=slide_ids, slide_names=slide_names, slide_urls=slide_urls)

	def to_dict(self):
		return {
			"device_id": self.device_id,
			"device_name": self.device_name,
			"department_id": self.department_id,
			"slide_ids": self.slide_ids,
			"slide_names": self.slide_names,
			"slide_urls": self.slide_urls
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
		#TODO FIX DEVICES. the getone is showing slide_assignment id
		device_id = data.get("device_id")
		device_name = data.get("device_name")
		department_id = data.get("department_id")
		slide_ids = data.get("slide_ids", [])
		slide_names = data.get("slide_names", [])
		slide_urls = data.get("slide_urls", [])

		device_info = {
			"device_id": device_id,
			"device_name": device_name,
			"department_id": department_id,
			"slide_ids": slide_ids,
			"slide_names": slide_names,
			"slide_urls": slide_urls
		}

		return device_info
	

	@staticmethod
	def getAll():
		"""
		Get all the slides in the db
		"""
		result = sql_client.get_table_data('devices')

		if result:
			return result
	
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

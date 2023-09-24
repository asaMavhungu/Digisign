from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import database.Database_utils as db_client
import database.sql_utils as sql_client

class Department:
	def __init__(self, department_name, department_id=None, slide_ids=None, slide_names=None, device_ids=None, device_names=None, shared_slide_ids=None, shared_slide_names=None):
		"""
		Constructor for the Department class.

		:param department_name: The name of the department.
		:param department_id: The department ID (optional).
		:param slides: List of dictionaries with 'id' and 'name' fields (optional).
		:param devices: List of dictionaries with 'id' and 'name' fields (optional).
		:param shared_slides: List of dictionaries with 'sharing_id' (or other relevant fields) (optional).
		"""
		self.department_id: str | None = department_id
		self.department_name: str = department_name
		self.slide_ids = slide_ids or []
		self.slide_names = slide_names or []
		self.device_ids = device_ids or []
		self.device_names = device_names or []
		self.shared_slide_ids = shared_slide_ids or []
		self.shared_slide_names = shared_slide_names or []

	@classmethod
	def from_dict(cls, data):
		department_id = data.get("department_id")
		department_name = data.get("department_name")
		slide_ids = data.get("slide_ids", [])
		slide_names = data.get("slide_names", [])
		shared_slide_ids = data.get("shared_slide_ids", [])
		shared_slide_names = data.get("shared_slide_names", [])
		device_ids = data.get("device_ids", [])
		device_names = data.get("device_names", [])
		
		return cls(department_name, department_id=department_id, slide_ids=slide_ids, slide_names=slide_names, device_names=device_names, shared_slide_ids=shared_slide_ids, shared_slide_names=shared_slide_names, device_ids=device_ids)

	def to_dict(self):
		return {
			"department_id": self.department_id,
			"department_name": self.department_name,
			"slide_ids": self.slide_ids,
			"slide_names": self.slide_names,
			"shared_slide_ids": self.shared_slide_ids,
			"shared_slide_names": self.shared_slide_names,
			"device_ids": self.device_ids,
			"device_names": self.device_names
		}

	def __repr__(self):
		return f"Department(department_id={self.department_id}, department_name='{self.department_name}', slide_names={self.slide_names}, shared_slide_names={self.shared_slide_names}, device_ids={self.device_ids}, device_names={self.device_names})"

	@staticmethod
	def getAll():
		"""
		Get all the slides in the db
		"""
		result = sql_client.get_table_data('departments')
		if result:
			return result
	
	@staticmethod
	def find_by_name(department_name: str):

		result, code = sql_client.get_entry('departments', {'department_name': department_name,})

		if code == 404:
			return result, code
		
		# TODO 'result' is ALWAYS in an expected format
		
		department_dict = {
			'department_id': result['department_id'],
			'department_name': result['department_name'],
			'slide_ids': [slide['slide_id'] for slide in result['slides']], # type: ignore
			'slide_names': [slide['slide_name'] for slide in result['slides']], # type: ignore
			'shared_slide_ids': [shared_slide['slide_id'] for shared_slide in result['shared_slides']], # type: ignore
			'shared_slide_names': [shared_slide['slide_name'] for shared_slide in result['shared_slides']], # type: ignore
			'device_ids': [device['device_id'] for device in result['devices']], # type: ignore
			'device_names': [device['device_name'] for device in result['devices']] # type: ignore
		}
		
		return department_dict, code
			
	@classmethod
	def extract_mult_departments_info(cls, data: list[dict]):
		department_info = []
		asa= True

		for entry in data:
			department_id = entry['department_id']
			department_name = entry['department_name']

			# Collect slide IDs, shared slide IDs, and device IDs
			slide_ids = []
			shared_slide_ids = []
			device_ids = []

			for slide in entry['slides']:
				slide_ids.append(slide['slide_id'])

			for shared_slide in entry['shared_slides']:
				shared_slide_ids.append(shared_slide['slide_id'])

			for device in entry['devices']:
				device_ids.append(device['device_id'])

			# Create a department entry in the desired format
			department_entry = {
				"department_id": department_id,
				"department_name": department_name,
				"slide_ids": slide_ids,
				"shared_slide_ids": shared_slide_ids,
				"device_ids": device_ids
			}

			department_info.append(department_entry)

		return department_info
	

	@classmethod
	def extract_department_info(cls, data):
		department_id = data.get("department_id")
		department_name = data.get("department_name")

		slide_ids = data.get("slide_ids", [])
		slide_names = data.get("slide_names", [])
		shared_slide_ids = data.get("shared_slide_ids", [])
		shared_slide_names = data.get("shared_slide_names", [])
		device_ids = data.get("device_ids", [])
		device_names = data.get("device_names", [])

		print("QQQQQQQQQQQQQQQQQQQQQQQ")
		print(data)

		return {
			"department_id": department_id,
			"department_name": department_name,
			"slide_ids": slide_ids,
			"slide_names": slide_names,
			"shared_slide_ids": shared_slide_ids,
			"shared_slide_names": shared_slide_names,
			"device_ids": device_ids,
			"device_names": device_names
		}
	
	def create_database_entry(self):
		result = sql_client.create_entry('departments', data = {
			'department_name': self.department_name,  # Replace with your actual data
			# Add other fields as needed
		} )

		return result
	
	def update_database_entry(self, data: dict):

		if 'department_name' in data:
			self.department_name = data['department_name']
		result = sql_client.update_entry('departments', 
				filter_dict={'department_id': self.department_id},
				data = data
			)
		
		return result
	
	def delete_database_entry(self):
		result = sql_client.delete_entry('departments', 
				filter_dict={'department_id': self.department_id}
			)
		
		return result

	def assign_devices(self, device_ids:list):
		result = sql_client.assign_devices_to_departments(department_id=self.department_id, device_ids=device_ids)

		return result

	def unassign_device(self, device_id: str):
		result = sql_client.disassociate_device_from_department(department_id=self.department_id, device_id=device_id)

		return result
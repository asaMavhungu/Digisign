from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import database.Database_utils as db_client
import database.sql_utils as sql_client

class Department:
	def __init__(self, department_name, department_id=None, slides=None, devices=None, shared_slides=None):
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
		self.slides = slides or []
		self.devices = devices or []
		self.shared_slides = shared_slides or []

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
	def from_db_query(cls, data):
		"""
		Create and populate a Department instance from database query data.

		:param data: The data retrieved from the database query.
		:return: A Department instance.
		"""
		department_name = data.get("department_name")
		department_id = data.get("department_id")
		slides = [{"id": slide.get("slide_id"), "name": slide.get("slide_name")} for slide in data.get("slides", [])]
		devices = [{"id": device.get("device_id"), "name": device.get("device_name")} for device in data.get("devices", [])]
		
		shared_slides = []
		for shared_slide_data in data.get("shared_slides", []):
			shared_slide = {
				"sharing_id": str(shared_slide_data.get("sharing_id")),
				"slide_id": str(shared_slide_data.get("slide_id")),
				"to_department": {
					"department_id": str(shared_slide_data.get("to_department", {}).get("department_id")),
					"department_name": shared_slide_data.get("to_department", {}).get("department_name"),
				},
				"from_department": {
					"department_id": str(shared_slide_data.get("from_department", {}).get("department_id")),
					"department_name": shared_slide_data.get("from_department", {}).get("department_name"),
				},
			}
			shared_slides.append(shared_slide)

		print(shared_slides)

		return cls(department_name, department_id=department_id, slides=slides, devices=devices, shared_slides=shared_slides)

	@classmethod
	def from_dict(cls, department_dict):
		"""
		Creates a Department instance from a dictionary.

		:param department_dict: A dictionary containing department data.
		:return: An instance of the Department class.
		"""
		print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
		print(department_dict)
		print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
		department = cls(
			department_name=department_dict['department_name']
		)
		department.department_id = department_dict.get('department_id')  # Optional ObjectId
		department.slides = department_dict.get('slides', [])
		department.devices = department_dict.get('devices', [])
		return department

	def to_dict(self):
		"""
		Converts the Department instance to a dictionary.

		:return: A dictionary representation of the department instance.
		"""
		department_dict = {
			'department_id': self.department_id,
			'department_name': self.department_name,
			'slides': self.slides,  # Include associated slide ObjectIds
			'devices': self.devices  # Include associated device ObjectIds
		}
		return department_dict

	@staticmethod
	def find_by_name(department_name: str):
		"""
		Finds a department by its name in the database.

		:param department_name: The name of the department to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Department class or None if not found.
		"""
		return sql_client.get_entry('departments', {'department_name': department_name,})
		return db_client.get_one('departments', 'department_name', department_name)

	def save(self):
		"""
		Saves the department instance to the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: The unique identifier (_id) of the inserted or updated department document.
		"""
		department_data = self.to_dict()
		if self.department_id:
			# Update the existing department document
			return db_client.update_entry('departments', 'department_name', self.department_name, department_data)
		else:
			# Insert a new department document
			return db_client.insert_entry('departments', department_data)

	@staticmethod
	def getAll():
		"""
		Get all the slides in the db
		"""
		print("CHECK 2")
		return sql_client.get_table_data('departments')
		return db_client.get_table('departments')
	
	def delete_me(self):
		# TODO FIXXXX
		slides_table.delete_one(self.department_id) # type: ignore #TODO TYPE IGNORE HERER

	def get_slides(self):
		return self.slides
	
	def get_devices(self):
		return self.devices

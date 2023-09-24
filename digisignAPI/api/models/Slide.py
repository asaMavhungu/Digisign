from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import database.Database_utils as db_client
import database.sql_utils as sql_client

class Slide:
	def __init__(self, slide_name, slide_url=None, slide_id=None, department_id=None, current_user_id=None, device_ids=None):
		"""
		Constructor for the Slide class.

		:param slide_name: The name of the slide.
		:param slide_id: The slide ID (optional).
		:param department_id: The department ID (optional).
		:param current_user_id: The current user ID (optional).
		:param device_ids: List of device IDs assigned to this slide (optional).
		"""
		self.slide_id = slide_id
		self.slide_name = slide_name
		self.slide_url = slide_url
		self.department_id = department_id
		self.current_user_id = current_user_id
		self.device_ids = device_ids or []

	def __repr__(self):
		return f"<Slide(slide_id={self.slide_id}, slide_name='{self.slide_name}', slide_url='{self.slide_url}', department_id={self.department_id}, current_user_id={self.current_user_id}, device_ids={self.device_ids})>"

	def to_dict(self):
		return {
			'slide_id': self.slide_id,
			'slide_name': self.slide_name,
			'slide_url': self.slide_url,
			'department_id': self.department_id,
			'current_user_id': self.current_user_id,
			'device_ids': self.device_ids
		}
	
	@classmethod
	def from_dict(cls, data):
		slide_id = data.get('slide_id')
		slide_name = data.get('slide_name')
		slide_url = data.get('slide_url')
		department_id = data.get('department_id')
		current_user_id = data.get('current_user_id')
		device_ids = data.get('device_ids', [])


		# Create a new Slide instance with the extracted data
		return cls(
			slide_id=slide_id,
			slide_name=slide_name,
			slide_url=slide_url,
			department_id=department_id,
			current_user_id=current_user_id,
			device_ids=device_ids
		)	

	@classmethod
	def extract_slide_info(cls, data):
		slide_id = data.get("slide_id")
		slide_name = data.get("slide_name")
		slide_url = data.get("slide_url")
		department_id = data.get("department_id")
		current_user_id = data.get("current_user_id")
		
		# Extract the device IDs from the 'assignments' list
		assignments_data = data.get("assignments", [])
		device_ids = [str(assignment.get("device_id")) for assignment in assignments_data]

		return {
			'slide_id': slide_id,
			'slide_name': slide_name,
			'slide_url': slide_url,
			'department_id': department_id,
			'current_user_id': current_user_id,
			'device_ids': device_ids,  # Store the list of assigned device IDs
		}

	
	@classmethod
	def extract_mult_slide_info(cls, data: list[dict]):
		department_info = []

		for slide_data in data:
			slide_id = slide_data.get("slide_id")
			slide_name = slide_data.get("slide_name")
			slide_url = slide_data.get("slide_url")
			department_id = slide_data.get("department_id")
			current_user_id = slide_data.get("current_user_id")
			
			# Extract the device IDs from the 'assignments' list
			assignments_data = slide_data.get("assignments", [])
			device_ids = [str(assignment.get("device_id")) for assignment in assignments_data]

			department_info.append({
			'slide_id': slide_id,
			'slide_name': slide_name,
			'slide_url': slide_url,
			'department_id': department_id,
			'current_user_id': current_user_id,
			'device_ids': device_ids,  # Store the list of assigned device IDs
		})

		return department_info
	

	@staticmethod
	def getAll():
		"""
		Get all the slides in the db
		"""
		result = sql_client.get_table_data('slides')
		if result:
			#print(result)
			return result
		
	@staticmethod
	def find_by_name(slide_name: str):
		result, code = sql_client.get_entry('slides', {'slide_name': slide_name,})

		if code == 404:
			return result, code
		
		# TODO 'result' is ALWAYS in an expected format
		print("TTTTTTTTTTTTTTTTTTTTTTTTTTT")
		print(result)
		print("TTTTTTTTTTTTTTTTTTTTTTTTTTT")

		return result, code
	
	def create_database_entry(self):
		result = sql_client.create_entry('slides', data = {
			'slide_name': self.slide_name,  # Replace with your actual data
			'slide_url': self.slide_url,
		} )

		return result
	
	def update_database_entry(self, data: dict):

		if 'slide_name' in data:
			self.department_name = data['slide_name']
		result = sql_client.update_entry('slides', 
				filter_dict={'slide_id': self.slide_id},
				data = data
			)
		
		return result
	
	def delete_database_entry(self):
		result = sql_client.delete_entry('slides', 
				filter_dict={'slide_id': self.slide_id}
			)
		
		return result
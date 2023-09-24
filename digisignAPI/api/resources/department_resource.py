from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields, marshal
from bson.objectid import ObjectId
from api.models.Department import Department
from api.models.Slide import Slide
from api.models.Device import Device


# Request parsers for department data
department_parser = reqparse.RequestParser()
department_parser.add_argument('department_name', type=str, required=True, help='Name of the department')
department_parser.add_argument('slides', type=list, location='json', help='Departments associated with the slide')
department_parser.add_argument('devices', type=list, location='json', help='Devices associated with the slide')

# Define the fields for marshaling department data in responses
department_fields = {
    "department_id": fields.String,
    "department_name": fields.String,
    #"slide_ids": fields.List(fields.String),
	"slide_names": fields.List(fields.String),
    #"device_ids": fields.List(fields.String),
	"device_names": fields.List(fields.String),
    #"shared_slide_ids": fields.List(fields.String),
	"shared_slide_names": fields.List(fields.String),
}

class DepartmentResource(Resource):
	"""
	Resource class for managing individual departments.
	"""


	#@marshal_with(department_fields)
	def get(self, department_name):
		"""
		Get details of a specific department by ID.
		"""
		department_dict, code = Department.find_by_name(department_name)
		print(department_dict)
		if code == 200:
			department_json = Department.extract_department_info(department_dict)
			department = Department.from_dict(department_json)
			responce  = marshal(department.to_dict(), department_fields)
			return responce, 200
		return {"message": "Department not found"}, 404
	
	def patch(self, department_name):
		"""
		Update a specific department by ID (partial update).
		"""
		args = department_parser.parse_args()
		department_dict, code = Department.find_by_name(department_name)
		

		if code == 404:
			return {"message": "Department not found"}, 404
		
		department = Department.from_dict(department_dict)
		
		if 'department_name' in args:

			new_name = args['department_name']
			old_name = department.department_name

			message, code = department.update_database_entry({"department_name": new_name})

			return message, code
		
	def delete(self, department_name):
		department_db_dict, code = Department.find_by_name(department_name)
		

		if code == 404:
			return {"message": "Department not found"}, 404
	
		department_dict = Department.extract_department_info(department_db_dict)

		department = Department.from_dict(department_dict)

		result, code  = department.delete_database_entry()

		return result, code
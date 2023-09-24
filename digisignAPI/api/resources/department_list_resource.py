from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Department import Department
from api.models.Slide import Slide
from api.models.Device import Device

# Request parsers for department data
department_parser = reqparse.RequestParser()
department_parser.add_argument('department_name', type=str, required=True, help='Name of the department')
department_parser.add_argument('slides', type=list, location='json', help='Departments associated with the slide')
department_parser.add_argument('devices', type=list, location='json', help='Devices associated with the slide')


department_fields = {
    "department_id": fields.String,
    "department_name": fields.String,
    "slide_ids": fields.List(fields.String),
    "device_ids": fields.List(fields.String),
    "shared_slide_ids": fields.List(fields.String),
}

class DepartmentListResource(Resource):
	"""
	Resource class for managing collections of departments.
	"""

	@marshal_with(department_fields)
	def get(self):
		"""
		Get a list of all departments.
		Returns:
			List[Department]: A list of all departments.
		"""
		departments_data = Department.getAll()
		if departments_data is not None:
			dep_dicts = Department.extract_mult_departments_info(departments_data)
			departments = [Department.from_dict(department_dict) for department_dict in dep_dicts]
			return departments, 200
		else:
			return {"message": "Departments not found"}, 404	

	def post(self):
		"""
		Create a new department.
		"""
		args = department_parser.parse_args()
		name = args['department_name']

		department = Department(name)

		responce , code = department.create_database_entry()

		#TODO Send success bool to front-end, ignore error for typed python error
		if code == 200:
			responce['success'] = True #type: ignore
		else:
			responce['success'] = False #type: ignore
		return responce
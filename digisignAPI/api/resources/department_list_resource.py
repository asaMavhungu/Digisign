from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Department import Department

# Request parsers for department data
department_parser = reqparse.RequestParser()
department_parser.add_argument('name', type=str, required=True, help='Name of the department')

# Define the fields for marshaling department data in responses
department_fields = {
	'_id': fields.String(attribute='_id'),
	'name': fields.String,
	'slides': fields.List(fields.String),
	'devices': fields.List(fields.String),
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
		print("CHECK 1")
		departments_data = Department.getAll()
		if departments_data is not None:
			departments = [Department.from_dict(department_data).to_dict() for department_data in departments_data]
			return departments, 200
		else:
			return {"message": "Departments not found"}, 404	

	def post(self):
		"""
		Create a new department.
		"""
		args = department_parser.parse_args()
		name = args['name']

		if Department.find_by_name(name):
			return {"message": f"Department named '{name}' already exists"}, 400

		department = Department(name)

		department_id = department.save()

		return {'message': 'Department created', 'department_id': department_id}, 201

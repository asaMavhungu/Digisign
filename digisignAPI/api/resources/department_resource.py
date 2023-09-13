from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Department import Department
from database.MongoDBClient import MongoDBClient
from database.DatabaseTable import DatabaseTable

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

class DepartmentResource(Resource):
	"""
	Resource class for managing individual departments.
	"""
	def __init__(self, dbClient: MongoDBClient):
		self.slide_table: DatabaseTable = dbClient.SlidesTable
		self.department_table: DatabaseTable = dbClient.DepartmentTable


	@marshal_with(department_fields)
	def get(self, department_name):
		"""
		Get details of a specific department by ID.
		"""
		department_dict = Department.find_by_name(department_name, self.department_table)
		if department_dict:
			return department_dict, 200
		return {"message": "Department not found"}, 404

	def patch(self, department_name):
		"""
		Update a specific department by ID (partial update).
		"""
		args = department_parser.parse_args()
		department_dict = Department.find_by_name(department_name, self.department_table)
		department = Department.from_dict(department_dict)

		if not department:
			return {"message": "Department not found"}, 404

		if 'name' in args:
			department.name = args['name']

		department_id = department.save(self.department_table)

		return {'message': 'Department updated', 'department_id': department_id}, 200

	def put(self, department_name):
		"""
		Update a specific department by ID (full update).
		"""
		args = department_parser.parse_args()
		name = args['name']

		department_dict = Department.find_by_name(department_name, self.department_table)
		department = Department.from_dict(department_dict)

		if not department:
			return {"message": "Department not found"}, 404

		department.name = name
		department.save(self.department_table)

		return {'message': 'Department updated', 'department_id': department_name}, 200

	def delete(self, department_name):
		"""
		Delete a department by its ID.

		Args:
			department_id (str): The ID of the department to delete.

		Returns:
			dict: A message indicating the result of the deletion.
		"""
		department_dict = Department.find_by_name(department_name, self.department_table)
		department = Department.from_dict(department_dict)
		if department:
			# Delete the department from the database
			department.delete_me(self.department_table)
			return {"message": f"Department '{department_name}' deleted"}, 200
		else:
			return {"message": "Department not found"}, 404
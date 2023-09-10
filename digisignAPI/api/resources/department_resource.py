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

class DepartmentResource(Resource):
	"""
	Resource class for managing individual departments.
	"""
	def __init__(self, mongo):
		self.mongo = mongo

	@marshal_with(department_fields)
	def get(self, department_id):
		"""
		Get details of a specific department by ID.
		"""
		department = Department.find_by_id(department_id, self.mongo)
		if department:
			return department.to_dict(), 200
		return {"message": "Department not found"}, 404

	def patch(self, department_id):
		"""
		Update a specific department by ID (partial update).
		"""
		args = department_parser.parse_args()
		department = Department.find_by_id(department_id, self.mongo)

		if not department:
			return {"message": "Department not found"}, 404

		if 'name' in args:
			department.name = args['name']

		department.save(self.mongo)

		return {'message': 'Department updated', 'department_id': department_id}, 200

	def put(self, department_id):
		"""
		Update a specific department by ID (full update).
		"""
		args = department_parser.parse_args()
		name = args['name']

		department = Department.find_by_id(department_id, self.mongo)

		if not department:
			return {"message": "Department not found"}, 404

		department.name = name
		department.save(self.mongo)

		return {'message': 'Department updated', 'department_id': department_id}, 200

	def delete(self, department_id):
		"""
		Delete a department by its ID.

		Args:
			department_id (str): The ID of the department to delete.

		Returns:
			dict: A message indicating the result of the deletion.
		"""
		department = Department.find_by_id(department_id, self.mongo)
		if department:
			# Delete the department from the database
			self.mongo.db.departments.delete_one({'_id': department._id})
			return {"message": f"Department '{department_id}' deleted"}, 200
		else:
			return {"message": "Department not found"}, 404
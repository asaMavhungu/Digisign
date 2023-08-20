from flask import request
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from api.models.Department import Department

# Define request parsers
department_parser = reqparse.RequestParser()
department_parser.add_argument('name', type=str, required=True, help='Name of the department')

class DepartmentResource(Resource):
	
	def __init__(self, mongo):
		self.mongo = mongo
		
	def post(self):
		args = department_parser.parse_args()
		name = args['name']

		# Create a new department instance
		department = Department(name)

		# Save the department to the database
		department_id = department.save(self.mongo)

		return {'message': 'Department created', 'department_id': department_id}, 201
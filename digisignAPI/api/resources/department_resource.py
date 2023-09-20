from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Department import Department
from api.models.Slide import Slide


# Request parsers for department data
department_parser = reqparse.RequestParser()
department_parser.add_argument('name', type=str, required=True, help='Name of the department')
department_parser.add_argument('slides', type=list, location='json', help='Departments associated with the slide')
department_parser.add_argument('devices', type=list, location='json', help='Devices associated with the slide')

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


	@marshal_with(department_fields)
	def get(self, department_name):
		"""
		Get details of a specific department by ID.
		"""
		department_dict = Department.find_by_name(department_name)
		if department_dict:
			return department_dict, 200
		return {"message": "Department not found"}, 404

	def patch(self, department_name):
		"""
		Update a specific department by ID (partial update).
		"""
		args = department_parser.parse_args()
		department_dict = Department.find_by_name(department_name)
		

		if not department_dict:
			return {"message": "Department not found"}, 404
		

		department = Department.from_dict(department_dict)
		#if 'name' in args:
			#department.name = args['name']

		if 'slides' in args:
			new_slides = args.get('slides', [])

			old_slides = department.get_slides()

			for slide_name in old_slides:
				slide_data = Slide.find_by_title(slide_name)

				slide = Slide.from_dict(slide_data)
				slide.remove_department(department_name)

				slide.save()

			for slide_name in new_slides:
				slide_data = Slide.find_by_title(slide_name)
				
				if not slide_data:
					return {'message': f'slide [{slide_name}] doesnt exist'}, 400
				
				slide = Slide.from_dict(slide_data)
				slide.add_department(department.name)
				department.add_slide(slide.title)
				slide.save()

		department_id = department.save()

		return {'message': 'Department updated', 'department_id': department_id}, 200

	def put(self, department_name):
		"""
		Update a specific department by ID (full update).
		"""
		args = department_parser.parse_args()
		name = args['name']

		department_dict = Department.find_by_name(department_name)
		department = Department.from_dict(department_dict)

		if not department:
			return {"message": "Department not found"}, 404

		department.name = name
		department.save()

		return {'message': 'Department updated', 'department_id': department_name}, 200

	def delete(self, department_name):
		"""
		Delete a department by its ID.

		Args:
			department_id (str): The ID of the department to delete.

		Returns:
			dict: A message indicating the result of the deletion.
		"""
		department_dict = Department.find_by_name(department_name)
		department = Department.from_dict(department_dict)
		if department:
			# Delete the department from the database
			department.delete_me()
			return {"message": f"Department '{department_name}' deleted"}, 200
		else:
			return {"message": "Department not found"}, 404
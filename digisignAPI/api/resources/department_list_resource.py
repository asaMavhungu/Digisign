from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Department import Department
from api.models.Slide import Slide
from api.models.Device import Device

# Request parsers for department data
department_parser = reqparse.RequestParser()
department_parser.add_argument('name', type=str, required=True, help='Name of the department')
department_parser.add_argument('slides', type=list, location='json', help='Departments associated with the slide')
department_parser.add_argument('devices', type=list, location='json', help='Devices associated with the slide')


department_fields3 = {
	'department_id': fields.String,
	'department_name': fields.String,
	'slides': fields.List(fields.Nested({'id': fields.String, 'name': fields.String})),
	'devices': fields.List(fields.Nested({'id': fields.String, 'name': fields.String})),
}

class DepartmentListResource(Resource):
	"""
	Resource class for managing collections of departments.
	"""

	@marshal_with(department_fields3)
	def get(self):
		"""
		Get a list of all departments.
		Returns:
			List[Department]: A list of all departments.
		"""
		departments_data = Department.getAll()
		if departments_data is not None:
			print(departments_data)
			#return departments_data, 200
			departments = [Department.from_db_query(department_data) for department_data in departments_data]
			return departments, 200
		else:
			return {"message": "Departments not found"}, 404	

	def post(self):
		"""
		Create a new department.
		"""
		args = department_parser.parse_args()
		name = args['name']

		department = Department(name)

		result = department.create_database_entry()
		print(result)
		return result

	def post_deprecated(self):
		"""
		Create a new department.
		"""
		args = department_parser.parse_args()
		name = args['name']

		if Department.find_by_name(name):
			return {"message": f"Department named '{name}' already exists"}, 400

		department = Department(name)

		if 'slides' in args:
			slides = args.get('slides', [])

			if slides is None:
				slides = []

			for slide_name in slides:
				slide_data = Slide.find_by_title(slide_name)
				
				if not slide_data:
					return {'message': f'slide [{slide_name}] doesnt exist'}, 400
				
				slide = Slide.from_dict(slide_data)
				slide.add_department(department.name)
				department.add_slide(slide.title)
				slide.save()

			if 'devices' in args:
				devices = args.get('slides', [])

				if devices is None:
					devices = []

				for device_name in devices:
					device_data = Device.find_by_name(device_name)

					if not device_data:
						return {'message': f'Device [{device_name}] doesnt exist'}, 400
					
					device = Device.from_dict(device_data)
					department.add_device(device.name)
					




		department_id = department.save()

		return {'message': 'Department created', 'department_id': department_id}, 201

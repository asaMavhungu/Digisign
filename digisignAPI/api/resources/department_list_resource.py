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

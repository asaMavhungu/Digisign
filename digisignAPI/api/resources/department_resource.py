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

# Define the fields for marshaling department data in responses
department_fields = {
    "department_id": fields.String,
    "department_name": fields.String,
    "slide_ids": fields.List(fields.String),
    "device_ids": fields.List(fields.String),
    "shared_slide_ids": fields.List(fields.String),
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
		department_dict, code = Department.find_by_name(department_name)
		if code == 200:
			#print(department_dict)
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
			print(department_dict)
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
			department_json = Department.extract_department_info(department_dict)
			department = Department.from_dict(department_json)
			print(department)
			return department, 200
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

	def patch_deprecated(self, department_name):
		"""
		Update a specific department by ID (partial update).
		"""
		args = department_parser.parse_args()
		department_dict, code = Department.find_by_name(department_name)
		

		if code == 200:
			return {"message": "Department not found"}, 404
		

		department = Department.from_dict(department_dict)
		#if 'name' in args:
			#department.name = args['name']

		if 'slides' in args:
			print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
			new_slides: list = args.get('slides', [])
			# This sometimes give back NONE
			if new_slides is None:
				new_slides = []

			# TODO This was a refrence to the lisy in the object not a copy
			#old_slides = department.get_slides()
			old_slides = list(department.get_slides())
			print(old_slides)
			print(new_slides)

			for slide_name in old_slides:
				print(slide_name + "         " + str(len(old_slides)))
				slide_data = Slide.find_by_title(slide_name)

				slide = Slide.from_dict(slide_data)
				
				slide.remove_department(department_name)
				print(f"slide [{slide.title}] remved department [{department_name}]")
				department.remove_slide(slide_name)

				slide.save()

			for slide_name in new_slides:
				slide_data = Slide.find_by_title(slide_name)
				
				if not slide_data:
					return {'message': f'slide [{slide_name}] doesnt exist'}, 400
				
				slide = Slide.from_dict(slide_data)
				
				slide.add_department(department.name)
				department.add_slide(slide.title)
				
				slide.save()

			if 'devices' in args:
				new_devices = args.get('devices', [])

				if new_devices is None:
					new_devices = []

				# TODO This was a refrence to the lisy in the object not a copy
				#old_devices = department.get_devices()
				old_devices = list(department.get_devices())

				for device_name in old_devices:
					#slide_data = Slide.find_by_title(slide_name)
					device_data = Device.find_by_name(device_name)

					#slide = Slide.from_dict(slide_data)
					device =  Device.from_dict(device_data)
					
					#slide.remove_department(department_name)
					#department.remove_slide(slide_name)

					device.remove_department(department_name)
					department.remove_device(device_name)

					device.save()

				for device_name in new_devices:
					device_data = Device.find_by_name(device_name)

					if not device_data:
						return {'message': f'Device [{device_name}] doesnt exist'}, 400
					
					device = Device.from_dict(device_data)

					department.add_device(device.name)
					device.add_department(department_name)

					device.save()

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

	def delete_depracated(self, department_name):
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
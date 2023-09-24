from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from api.models.Device import Device  # Updated import
from api.models.Slide import Slide
from api.models.Department import Department
from api.models.SlideFactory import SlideFactory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# Request parsers for creating and updating devices
device_parser = reqparse.RequestParser()
device_parser.add_argument('device_name', type=str, required=True, help='Name of the device')
device_parser.add_argument('department_name', type=str, required=True, help='Name of the department')
device_parser.add_argument('description', type=str, required=False, help='Description of the device')
device_parser.add_argument('slides', type=list, location='json', help='Slides associated with the device')

device_parser_patch = reqparse.RequestParser()
device_parser_patch.add_argument('name', type=str, required=False, help='Name of the device')
device_parser_patch.add_argument('description', type=str, required=False, help='Description of the device')
device_parser_patch.add_argument('slides', type=list, location='json', help='Slides associated with the device')

# Fields to marshal device data in responses
device_fields = {
    'device_id': fields.String,
    'device_name': fields.String,
    'department_id': fields.String,
    'slide_ids': fields.List(fields.String),  # Assuming slide_id is a string
}

class DeviceListResource(Resource):

	@marshal_with(device_fields)
	#@jwt_required()
	def get(self):
		"""
		Get a list of all devices.

		Returns:
			list: A list of all devices.
			int: HTTP status code.
		"""
		devices_data = Device.getAll()

		if devices_data is not None:	
			dev_dicts = Device.extract_mult_devices_info(devices_data)
			devices = [Device.from_dict(dev_dict) for dev_dict in dev_dicts]  # Updated model name
			return devices, 200
		else:
			return {"message": "Departments not found"}, 404	

	#@marshal_with(device_fields)
	def post(self):
		"""
		Create a new device.

		Returns:
			dict: The created device information.
			int: HTTP status code.
		"""
		print(" ard 1 ZZZZZZZZZZZZZZZZZZZZZZZZZZ")
		args = device_parser.parse_args()
		print("ard 2 ZZZZZZZZZZZZZZZZZZZZZZZZZZ")
		name = args['device_name']
		department_name = args['department_name']

		device = Device(name)

		responce, code = device.create_database_entry()

		responce['success'] = False


		# Couldnt create, abort
		if code== 401:
			return responce, code

		device, code = Device.device_from_name(device.device_name)


		responce['success'] = True #type: ignore
		#TODO connect this device to the department
		department_dict, code = Department.find_by_name(department_name)
		print(department_dict)

		if code == 404:
			return responce, code
		
		department_json = Department.extract_department_info(department_dict)
		department = Department.from_dict(department_json)

		print(device)
		responce_for_assign, code = department.assign_devices([device.device_id])

		print(responce, code)

		if code == 404:
			return responce_for_assign, code
		
		return responce



		#TODO Send success bool to front-end, ignore error for typed python error
		if code == 200:
			print("gg ZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
			responce['success'] = True #type: ignore
			#TODO connect this device to the department
			department_dict, code = Department.find_by_name(department_name)
			print(department_dict)
			print("2 ZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
			if code == 200:
				department_json = Department.extract_department_info(department_dict)
				department = Department.from_dict(department_json)
				print("3 ZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
				print(device)
				responce_for_assign, code = department.assign_devices([device.device_id]) #type: ignore

				if code == 400:
					return responce_for_assign

				print(responce)

				return responce

		else:
			responce['success'] = False #type: ignore
		return responce
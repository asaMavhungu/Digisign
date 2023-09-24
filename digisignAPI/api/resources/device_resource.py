from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from api.models.Device import Device
from api.models.Department  import Department
from api.models.Slide import Slide
from api.models.SlideFactory import SlideFactory

# Request parsers for creating and updating devices
device_parser = reqparse.RequestParser()
device_parser.add_argument('device_name', type=str, required=True, help='Name of the device')
device_parser.add_argument('description', type=str, required=False, help='Description of the device')
device_parser.add_argument('slides', type=list, location='json', help='Slides associated with the device')
device_parser.add_argument('departments', type=list, location='json', help='departments associated with the device')

device_parser_patch = reqparse.RequestParser()
device_parser_patch.add_argument('device_name', type=str, required=False, help='Name of the device')
device_parser_patch.add_argument('description', type=str, required=False, help='Description of the device')
device_parser_patch.add_argument('slides', type=list, location='json', help='Slides associated with the device')
device_parser_patch.add_argument('departments', type=list, location='json', help='departments associated with the device')

# Fields to marshal device data in responses
device_fields = {
    'device_id': fields.String,
    'device_name': fields.String,
    'department_id': fields.String,
    'slide_ids': fields.List(fields.String),  # Assuming slide_id is a string
	'slide_names': fields.List(fields.String),  # Assuming slide_id is a string
	'slide_urls': fields.List(fields.String),  # Assuming slide_id is a string
}

class DeviceResource(Resource):

	@marshal_with(device_fields)
	def get(self, device_name):
		"""
		Get details of a specific device by its name.

		Args:
			device_name (str): The name of the device.

		Returns:
			dict: The device information.
			int: HTTP status code.
		"""
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		device_dict, code = Device.find_by_name(device_name)
		print("========================")
		if code == 200:
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
			print(device_dict)
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
			device_json = Device.extract_device_info(device_dict)
			print(device_json)
			device = Device.from_dict(device_json)
			print(device)
			return device, 200
		return {"message": "Device not found"}, 404

	def patch(self, device_name):
		"""
		Partially update an existing device.

		Args:
			device_name (str): The name of the device to update.

		Returns:
			dict: The updated device information.
			int: HTTP status code.
		"""
		args = device_parser_patch.parse_args()

		device_dict, code = Device.find_by_name(device_name)

		if code == 404:
			return {"message": "Department not found"}, 404
		
		if 'device_name' in args:
			new_name = args['device_name']

			device_json = Device.extract_device_info(device_dict)
			device = Device.from_dict(device_json)

			message, code = device.update_database_entry({"device_name": new_name})

			return message, code
		if code == 200:
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
			print(device_dict)
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
			device_json = Device.extract_device_info(device_dict)
			print(device_json)
			device = Device.from_dict(device_json)
			print(device)
			
			return device, 200
		return {"message": "Device not found"}, 404
	
	def delete(self, device_name):
		device_dict, code = Device.find_by_name(device_name)

		if code == 404:
			return {"message": "Department not found"}, 404

		device_json = Device.extract_device_info(device_dict)
		device = Device.from_dict(device_json)
		# TODO ADD departnment name to device

		responce, code = device.delete_database_entry()

		print(responce)
		print(device)
		print("WWWWWWWWWWWWWWWWWWWWWWWWW")
		department_name = device_json['department_name']

		responce['success'] = False


		# Couldnt create, abort
		if code != 200:
			return responce, code

		responce['success'] = True #type: ignore
		#TODO connect this device to the department
		print(responce['department_name'])
		department_dict, code = Department.find_by_name(department_name)
		print(department_dict)

		if code == 404:
			return responce, code
		
		department_json = Department.extract_department_info(department_dict)
		department = Department.from_dict(department_json)

		print(device)
		responce_for_assign, code = department.unassign_device(device.device_id)

		print(responce, code)

		if code == 404:
			return responce_for_assign, code
		
		return responce
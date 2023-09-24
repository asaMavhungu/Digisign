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
		args = device_parser.parse_args()
		name = args['device_name']

		device = Device(name)

		responce, code = device.create_database_entry()

		#TODO Send success bool to front-end, ignore error for typed python error
		if code == 200:
			responce['success'] = True #type: ignore
		else:
			responce['success'] = False #type: ignore
		return responce
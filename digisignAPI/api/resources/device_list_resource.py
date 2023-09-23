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
device_parser.add_argument('description', type=str, required=True, help='Description of the device')
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
		print(devices_data[0])
		if devices_data is not None:	
			dev_dicts = Device.extract_mult_devices_info(devices_data)
			print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW------------")
			print(dev_dicts[0])
			print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW------------")
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

		result = device.create_database_entry()
		print(result)
		return result
	
		if Device.find_by_name(name):
			return {"message": f"Device named '{name}' already exists"}, 400

		device = Device(name, description)

	
		for slide_title in slides:
			slide_dict = Slide.find_by_title(slide_title)

			if slide_dict:
				device.add_slide(slide_title)
			else:
				return {"message": f"Slide '{slide_title}' not found"}, 404

		device_id = device.save()

		return {'message': 'Device created', 'device_id': device_id}, 201

	def delete(self):
		"""
		Delete multiple devices by their names.

		Returns:
			dict: A message indicating the deletion status.
			int: HTTP status code.
		"""
		args = request.get_json()
		device_names = args.get('device_names', [])  # Updated parameter name

		if not device_names:
			return {"message": "No device names specified for deletion"}, 400

		deleted_devices = []
		not_found_devices = []

		for device_name in device_names:
			device_data = Device.find_by_name(device_name)

			if device_data:
				device = Device.from_dict(device_data)
				device.delete_me()
				deleted_devices.append(device_name)
			else:
				not_found_devices.append(device_name)

		if deleted_devices:
			message = f"Devices [{', '.join(deleted_devices)}] deleted successfully."
		else:
			message = "No devices were deleted."

		if not_found_devices:
			message += f" Devices [{', '.join(not_found_devices)}] not found and were not deleted."

		return {"message": message}, 200

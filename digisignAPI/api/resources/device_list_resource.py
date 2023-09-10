from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from api.models.Device import Device  # Updated import
from api.models.Slide import Slide
from api.models.Department import Department

# Request parsers for creating and updating devices
device_parser = reqparse.RequestParser()
device_parser.add_argument('name', type=str, required=True, help='Name of the device')
device_parser.add_argument('description', type=str, required=True, help='Description of the device')
device_parser.add_argument('slides', type=list, location='json', help='Slides associated with the device')

device_parser_patch = reqparse.RequestParser()
device_parser_patch.add_argument('name', type=str, required=False, help='Name of the device')
device_parser_patch.add_argument('description', type=str, required=False, help='Description of the device')
device_parser_patch.add_argument('slides', type=list, location='json', help='Slides associated with the device')

# Fields to marshal device data in responses
device_fields = {
	'_id': fields.String(attribute='_id'),
	'name': fields.String,
	'description': fields.String,
	'slides': fields.List(fields.String),
}

class DeviceListResource(Resource):
	def __init__(self, mongo):
		self.mongo = mongo

	@marshal_with(device_fields)
	def get(self):
		"""
		Get a list of all devices.

		Returns:
			list: A list of all devices.
			int: HTTP status code.
		"""
		devices_data = self.mongo.db.devices.find()  # Updated collection name
		devices = [Device.from_dict(device_data) for device_data in devices_data]  # Updated model name
		return devices, 200

	#@marshal_with(device_fields)
	def post(self):
		"""
		Create a new device.

		Returns:
			dict: The created device information.
			int: HTTP status code.
		"""
		args = device_parser.parse_args()
		name = args['name']
		description = args['description']
		slides = args.get('slides', [])

		if Device.find_by_name(name, self.mongo):
			return {"message": f"Device named '{name}' already exists"}, 400

		device = Device(name, description)

	
		for slide_title in slides:
			slide = Slide.find_by_title(slide_title, self.mongo)

			if slide:
				device.add_slide(slide.title)
			else:
				return {"message": f"Slide '{slide_title}' not found"}, 404

		device_id = device.save(self.mongo)

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
			device = Device.find_by_name(device_name, self.mongo)

			if device:
				device.delete(self.mongo)
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

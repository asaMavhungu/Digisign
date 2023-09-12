from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from api.models.Device import Device
from api.models.Slide import Slide
from api.models.SlideFactory import SlideFactory

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

class DeviceResource(Resource):
	def __init__(self, mongo):
		self.mongo = mongo

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
		device = Device.find_by_name(device_name, self.mongo)
		if device:
			return device, 200
		return {"message": "Device not found"}, 404

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
			slide_dict = Slide.find_by_title(slide_title, self.mongo)
			slide = SlideFactory.slide_from_dict(slide_dict)

			if slide:
				device.add_slide(slide.title)
			else:
				return {"message": f"Slide '{slide_title}' not found"}, 404

		device_id = device.save(self.mongo)

		return {'message': 'Device created', 'device_id': device_id}, 201

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
		device = Device.find_by_name(device_name, self.mongo)

		if not device:
			return {"message": "Device not found"}, 404

		if 'slides' in args:
			new_slides = args.get('slides', [])
			device.slides = []  # Clear existing slides

			for slide_title in new_slides:
				slide_dict = Slide.find_by_title(slide_title, self.mongo)
				slide = SlideFactory.slide_from_dict(slide_dict)

				if slide:
					device.add_slide(slide.title)
				else:
					return {"message": f"Slide '{slide_title}' not found"}, 404

		if 'description' in args and args['description']:
			device.description = args['description']

		if 'name' in args and args['name']:
			device.name = args['name']

		device.save(self.mongo)

		return {'message': 'Device partially updated', 'device_name': device_name}, 200
	
	def put(self, device_name):
		"""
		Replace an existing device with new data using the PUT method.

		Args:
			device_name (str): The name of the device to replace.

		Returns:
			dict: The replaced device information.
			int: HTTP status code.
		"""
		args = device_parser.parse_args()  # Use the same parser as for creating a new device
		name = args['name']
		description = args['description']
		slides = args.get('slides', [])

		existing_device = Device.find_by_name(device_name, self.mongo)

		if not existing_device:
			return {"message": "Device not found"}, 404

		# Create a new device with the provided data
		new_device = Device(name, description)

		for slide_title in slides:
			slide_dict = Slide.find_by_title(slide_title, self.mongo)
			slide = SlideFactory.slide_from_dict(slide_dict)

			if slide:
				new_device.add_slide(slide.title)
			else:
				return {"message": f"Slide '{slide_title}' not found"}, 404

		# Delete the existing device and replace it with the new one
		self.mongo.db.devices.delete_one({'_id': existing_device._id})
		device_id = new_device.save(self.mongo)

		return {'message': 'Device replaced', 'device_id': device_id}, 200


	def delete(self, device_name):
		"""
		Delete a device by its name.

		Args:
			device_name (str): The name of the device to delete.

		Returns:
			dict: A message confirming the deletion.
			int: HTTP status code.
		"""
		device = Device.find_by_name(device_name, self.mongo)

		if device:
			# Delete the device from the database
			self.mongo.db.devices.delete_one({'_id': device._id})
			return {"message": f"Device '{device_name}' deleted"}, 200
		else:
			return {"message": "Device not found"}, 404

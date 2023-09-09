from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from api.models.DeviceGroup import DeviceGroup
from api.models.Slide import Slide

device_group_parser = reqparse.RequestParser()
device_group_parser.add_argument('name', type=str, required=True, help='Name of the device group')
device_group_parser.add_argument('description', type=str, required=True, help='Description of the device group')
device_group_parser.add_argument('slides', type=list, location='json', help='Slides associated with the device group')

device_group_parser_patch = reqparse.RequestParser()
device_group_parser_patch.add_argument('name', type=str, required=False, help='Name of the device group')
device_group_parser_patch.add_argument('description', type=str, required=False, help='Description of the device group')
device_group_parser_patch.add_argument('slides', type=list, location='json', help='Slides associated with the device group')

device_group_fields = {
	'_id': fields.String(attribute='_id'),
	'name': fields.String,
	'description': fields.String,
	'slides': fields.List(fields.String),
}

# TODO: Finish implementing device groups

class DeviceGroupResource(Resource):
	def __init__(self, mongo):
		self.mongo = mongo

	@marshal_with(device_group_fields)
	def get(self, device_group_name):
		"""
		Get details of a specific device group by its name.

		Args:
			device_group_name (str): The name of the device group.

		Returns:
			dict: The device group information.
			int: HTTP status code.
		"""
		device_group = DeviceGroup.find_by_name(device_group_name, self.mongo)
		if device_group:
			return device_group, 200
		return {"message": "Device group not found"}, 404

	@marshal_with(device_group_fields)
	def post(self):
		"""
		Create a new device group.

		Returns:
			dict: The created device group information.
			int: HTTP status code.
		"""
		args = device_group_parser.parse_args()
		name = args['name']
		description = args['description']
		slides = args.get('slides', [])

		if DeviceGroup.find_by_name(name, self.mongo):
			return {"message": f"Device group named '{name}' already exists"}, 400

		device_group = DeviceGroup(name, description)

		for slide_title in slides:
			slide = Slide.find_by_title(slide_title, self.mongo)

			if slide:
				device_group.add_slide(slide.title)
			else:
				return {"message": f"Slide '{slide_title}' not found"}, 404

		device_group_id = device_group.save(self.mongo)

		return {'message': 'Device group created', 'device_group_id': device_group_id}, 201

	@marshal_with(device_group_fields)
	def patch(self, device_group_name):
		"""
		Update an existing device group.

		Args:
			device_group_name (str): The name of the device group to update.

		Returns:
			dict: The updated device group information.
			int: HTTP status code.
		"""
		args = device_group_parser_patch.parse_args()
		device_group = DeviceGroup.find_by_name(device_group_name, self.mongo)

		if not device_group:
			return {"message": "Device group not found"}, 404

		if 'slides' in args:
			args = device_group_parser.parse_args()
			new_slides = args.get('slides', [])

			for slide_title in new_slides:
				slide = Slide.find_by_title(slide_title, self.mongo)

				if slide:
					device_group.add_slide(slide.title)
				else:
					return {"message": f"Slide '{slide_title}' not found"}, 404

		if 'description' in args and args['description']:
			device_group.description = args['description']

		if 'name' in args and args['name']:
			device_group.name = args['name']

		device_group.save(self.mongo)

		return {'message': 'Device group updated', 'device_group_name': device_group_name}, 200

	def delete(self, device_group_name):
		"""
		Delete a device group by its name.

		Args:
			device_group_name (str): The name of the device group to delete.

		Returns:
			dict: A message confirming the deletion.
			int: HTTP status code.
		"""
		device_group = DeviceGroup.find_by_name(device_group_name, self.mongo)

		if device_group:
			# Delete the device group from the database
			self.mongo.db.device_groups.delete_one({'_id': device_group._id})
			return {"message": f"Device group '{device_group_name}' deleted"}, 200
		else:
			return {"message": "Device group not found"}, 404

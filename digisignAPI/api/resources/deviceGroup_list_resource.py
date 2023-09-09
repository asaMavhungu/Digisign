from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from api.models.DeviceGroup import DeviceGroup
from api.models.Slide import Slide
from api.models.Department import Department

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

class DeviceGroupListResource(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    @marshal_with(device_group_fields)
    def get(self):
        """
        Get a list of all device groups.

        Returns:
            list: A list of all device groups.
            int: HTTP status code.
        """
        device_groups_data = self.mongo.db.device_groups.find()
        device_groups = [DeviceGroup.from_dict(device_group_data) for device_group_data in device_groups_data]
        return device_groups, 200

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

    def delete(self):
        """
        Delete multiple device groups by their names.

        Returns:
            dict: A message indicating the deletion status.
            int: HTTP status code.
        """
        args = request.get_json()
        group_names = args.get('group_names', [])

        if not group_names:
            return {"message": "No device group names specified for deletion"}, 400

        deleted_groups = []
        not_found_groups = []

        for group_name in group_names:
            device_group = DeviceGroup.find_by_name(group_name, self.mongo)

            if device_group:
                device_group.delete(self.mongo)
                deleted_groups.append(group_name)
            else:
                not_found_groups.append(group_name)

        if deleted_groups:
            message = f"Device groups [{', '.join(deleted_groups)}] deleted successfully."
        else:
            message = "No device groups were deleted."

        if not_found_groups:
            message += f" Device groups [{', '.join(not_found_groups)}] not found and were not deleted."

        return {"message": message}, 200
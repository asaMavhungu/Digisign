from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Slide import Slide
from api.models.Device import Device
from api.models.SlideFactory import SlideFactory
from api.models.Department import Department
from api.models.SlideFactory import SlideFactory
from api.models.ImageSlide import ImageSlide


# Request parsers for slide data
slide_parser = reqparse.RequestParser()
slide_parser.add_argument('slide_name', type=str, required=True, help='Name of the slide')
slide_parser.add_argument('device_name', type=str, required=True, help='Name of the device')

# Define the fields for marshaling slide data in responses
# Define a fields dictionary to specify how to serialize the Slide object
slide_fields = {
    'slide_name': fields.String(attribute='slide_name'),
    'device_name': fields.String(attribute='device_name'),

}


class SlideDeviceResource(Resource):
		
	def post(self):
		args = slide_parser.parse_args()
		slide_name = args['slide_name']
		device_name = args['device_name']

		slide = Slide(slide_name=slide_name)

		responce['success'] = False # type: ignore

		slide, code = Slide.slide_from_name(slide.slide_name)

		# slide will be found
		responce['success'] = True # type: ignore

		device_dict, code = Device.find_by_name(device_name=device_name)
		
		device = Device.from_dict(device_dict)

		print(device)
		print(slide)

		print("UUUUUUUUUUUUUUUUUUUUUUUUUUUU")
		responce, code = slide.assign_to_device(device_id=device.device_id) #type: ignore
		print(responce, code)
		print("UUUUUUUUUUUUUUUUUUUUUUUUUUUU")
		slide = Slide.slide_from_name(slide.slide_name) #type: ignore
		print(responce, code)
		print(slide)

		if code == 404:
			return responce, code
		
		return responce, code

	def delete(self, slide_name):

		args = slide_parser.parse_args()
		slide_name = args['slide_name']
		device_name = args['device_name']

		slide_db_dict, code = Slide.find_by_name(slide_name)
		
		if code == 404:
			return {"message": "Slide not found"}, 404
		
	
		slide_dict = Slide.extract_slide_info(slide_db_dict)

		slide = Slide.from_dict(slide_dict)

		device_dict, code = Device.find_by_name(device_name=device_name)
		
		device = Device.from_dict(device_dict)

		# Device will HAVE id
		result, code = slide.unassign_from_device(device.device_id) #type: ignore

		print(slide)

		return result, code
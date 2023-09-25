from flask import request, jsonify
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Slide import Slide
from api.models.Department import Department
from api.models.SlideFactory import SlideFactory
from api.models.User import User
from api.models.Device import Device
import json


# Request parsers for slide data
slide_parser = reqparse.RequestParser()
slide_parser.add_argument('slide_name', type=str, required=True, help='Title of the slide')
slide_parser.add_argument('slide_url', type=str, required=True, help='URL of the slide')
slide_parser.add_argument('device_name', type=str, required=True, help='Name of associated device')
slide_parser.add_argument('slide_duration', type=str, required=True, help='Duration of the slide')

# Define the fields for marshaling slide data in responses
slide_fields = {
    'slide_id': fields.String(attribute='slide_id'),
    'slide_name': fields.String(attribute='slide_name'),
	'slide_url': fields.String(attribute='slide_url'),
    'department_id': fields.String(attribute='department_id'),
    'current_user_id': fields.String(attribute='current_user_id'),
    'device_ids': fields.List(fields.String)
}

class SlideList(Resource):
	"""
	Resource class for managing collections of slides.
	"""

	@marshal_with(slide_fields)
	def get(self):
		"""
		Get a list of all slides.
		Returns:
			List[Slide]: A list of all slides.
		"""
		slides_data = Slide.getAll()
		#return {"message": "Departments not found"}, 400
		if slides_data is not None:
			slide_dicts = Slide.extract_mult_slide_info(slides_data)
			slides = [Slide.from_dict(slide_dict) for slide_dict in slide_dicts]
			print(slides[0])
			return slides, 200
		else:
			return {"message": "Departments not found"}, 404		
	
	#@marshal_with(slide_fields)
	def post(self):
		args = slide_parser.parse_args()
		slide_name = args['slide_name']
		slide_url = args['slide_url']
		device_name = args['device_name']
		slide_durarion = args['slide_duration']

		slide = Slide(slide_name=slide_name, slide_url=slide_url, slide_duration=slide_durarion)

		responce, code = slide.create_database_entry()

		responce['success'] = False # type: ignore

		# Couldnt create, abort
		if code== 401:
			return responce, code
		
		# Slide is bound to be found as it was succesfully entered
		slide, code = Slide.slide_from_name(slide.slide_name)

		# slide will be found
		responce['success'] = True # type: ignore

		device_dict, code = Device.find_by_name(device_name=device_name)
		
		device = Device.from_dict(device_dict)

		print(device)
		print(slide)

		print("UUUUUUUUUUUUUUUUUUUUUUUUUUUU")
		responce_for_assign, code = slide.assign_to_device(device_id=device.device_id) #type: ignore
		print(responce_for_assign, code)
		print("UUUUUUUUUUUUUUUUUUUUUUUUUUUU")
		slide = Slide.slide_from_name(slide.slide_name) #type: ignore
		print(responce, code)
		print(slide)

		if code == 404:
			return responce_for_assign, code
		
		return responce


		
		#TODO Send success bool to front-end, ignore error for typed python error
		if code == 200:
			responce['success'] = True #type: ignore
		else:
			responce['success'] = False #type: ignore
		return responce

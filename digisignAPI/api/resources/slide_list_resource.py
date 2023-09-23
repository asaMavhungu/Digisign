from flask import request, jsonify
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Slide import Slide
from api.models.Department import Department
from api.models.SlideFactory import SlideFactory
from api.models.User import User
import json


# Request parsers for slide data
slide_parser = reqparse.RequestParser()
slide_parser.add_argument('slide_name', type=str, required=True, help='Title of the slide')
slide_parser.add_argument('user_id', type=str, required=False, help='Author ID of the slide')
slide_parser.add_argument('department_id', type=str, required=False, help='image of the slide')
slide_parser.add_argument('slide_type', type=str, required=False, help='Type of content of the slide') 
slide_parser.add_argument('departments', type=list, location='json', help='Departments associated with the slide')

# Define the fields for marshaling slide data in responses
slide_fields = {
    'slide_id': fields.String(attribute='slide_id'),
    'slide_name': fields.String(attribute='slide_name'),
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
			return slides, 200
		else:
			return {"message": "Departments not found"}, 404		
	
	@marshal_with(slide_fields)
	def post(self):
		args = slide_parser.parse_args()
		slide_name = args['slide_name']

		slide = Slide(slide_name)

		result = slide.create_database_entry()
		print(result)
		return result
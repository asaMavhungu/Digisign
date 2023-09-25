from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Slide import Slide
from api.models.SlideFactory import SlideFactory
from api.models.Department import Department
from api.models.SlideFactory import SlideFactory
from api.models.ImageSlide import ImageSlide


# Request parsers for slide data
slide_parser = reqparse.RequestParser()
slide_parser.add_argument('slide_name', type=str, required=True, help='Title of the slide')
slide_parser.add_argument('user_id', type=str, required=False, help='Author ID of the slide')
slide_parser.add_argument('department_id', type=str, required=False, help='image of the slide')
slide_parser.add_argument('slide_type', type=str, required=False, help='Type of content of the slide') 
slide_parser.add_argument('departments', type=list, location='json', help='Departments associated with the slide')

# Define the fields for marshaling slide data in responses
# Define a fields dictionary to specify how to serialize the Slide object
slide_fields = {
    'slide_id': fields.String(attribute='slide_id'),
    'slide_name': fields.String(attribute='slide_name'),
    'department_id': fields.String(attribute='department_id'),
    'current_user_id': fields.String(attribute='current_user_id'),
    'device_ids': fields.List(fields.String),
}


class SlideResource(Resource):
	"""
	Resource class for managing individual slides.
	"""

	@marshal_with(slide_fields)
	def get(self, slide_name):
		"""
		Get details of a specific slide by title.
		"""
		slide_dict, code = Slide.find_by_name(slide_name)
		if code == 200:
			slide_json = Slide.extract_slide_info(slide_dict)
			slide = Slide.from_dict(slide_json)
			return slide, 200
		return {"message": "Slide not found"}, 404
	
	def patch(self, slide_name):

		args = slide_parser.parse_args()
		slide_dict, code = Slide.find_by_name(slide_name)

		if code == 404:
			return {"message": "Slide not found"}, 404
		
		slide = Slide.from_dict(slide_dict)

		if 'slide_name' in args:
			new_name = args['slide_name']
			old_name = slide.slide_name

			message, code = slide.update_database_entry({"slide_name": new_name})

			return message, code
		pass

	def delete(self, slide_name):
		slide_db_dict, code = Slide.find_by_name(slide_name)
		
		if code == 404:
			return {"message": "Slide not found"}, 404
	
		slide_dict = Slide.extract_slide_info(slide_db_dict)

		slide = Slide.from_dict(slide_dict)

		# Dissassociate the slide from its devices
		for device_id in slide.device_ids:
			responce = slide.unassign_from_device(device_id)
			print(responce)

		# delete the device
		result, code  = slide.delete_database_entry()



		return result, code
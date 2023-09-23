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
slide_parser.add_argument('title', type=str, required=True, help='Title of the slide')
slide_parser.add_argument('image_url', type=str, required=True, help='image of the slide')
slide_parser.add_argument('slide_type', type=str, required=True, help='Type of content of the slide') 
slide_parser.add_argument('author_id', type=str, required=True, help='Author ID of the slide')
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
		

	def post_deprecated(self):
		"""
		Create a new slide.
		"""
		args = slide_parser.parse_args()
		title = args['title']
		image_url = args['image_url']
		slide_type = args['slide_type']
		author_id = args['author_id']
		departments = args.get('departments', [])

		user_dict = User.find_by_username(author_id)

		if not user_dict:
			return {"message": f"User [{author_id}] does not exist"}, 400
		
		user = User.from_dict(user_dict)

		if Slide.find_by_title(title):
			return {"message": f"Slide titled [{title}] already exists"}, 400

		slide_dict = {
			'title' : title,
			'slide_type' : slide_type,
			'author_id' : user.username,
			'image_url' : image_url
		}
		slide_factory = SlideFactory()
		slide = slide_factory.create_slide(slide_dict)

		if slide:
			pass

			for department_name in departments:
				department_data = Department.find_by_name(department_name)

				if department_data:
					department = Department.from_dict(department_data)
					slide.add_department(department.name)
					department.add_slide(slide.title)
					department.save()
				else:
					return {"message": f"Department [{department_name}] not found"}, 404

			slide_id = slide.save()

			return {'message': 'Slide created', 'slide_id': slide_id}, 201
		
		return {'message': 'Slide NOT created'}, 400
	
	def delete_deprecated(self):
		"""
		Delete multiple slides.

		Returns:
			dict: A message indicating the result of the deletion.
		"""
		data = request.get_json()
		if not data:
			return {"message": "No data provided in the request body"}, 400

		slide_titles = data.get("slide_titles", [])
		if not slide_titles:
			return {"message": "No slide titles provided in the request"}, 400

		deleted_count = 0
		for slide_title in slide_titles:
			slide_dict = Slide.find_by_title(slide_title)

			if slide_dict is None:
				return {"message": f" slide '{slide_title}' not found"}, 400
			
			slide_factory = SlideFactory()
			slide = slide_factory.create_slide(slide_dict)

			if slide:
				slide.delete_me()
				deleted_count += 1

		return {"message": f"{deleted_count} slides deleted"}, 200

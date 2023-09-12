from flask import request, jsonify
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Slide import Slide
from api.models.Department import Department
from api.models.SlideFactory import SlideFactory
import json

# Request parsers for slide data
slide_parser = reqparse.RequestParser()
slide_parser.add_argument('title', type=str, required=True, help='Title of the slide')
slide_parser.add_argument('content', type=str, required=True, help='Content of the slide')
slide_parser.add_argument('content_type', type=str, required=True, help='Type of content of the slide') 
slide_parser.add_argument('author_id', type=str, required=True, help='Author ID of the slide')
slide_parser.add_argument('image_url', type=str, required=False, help='URL of image slide')
slide_parser.add_argument('video_url', type=str, required=False, help='URL of video slide')
slide_parser.add_argument('departments', type=list, location='json', help='Departments associated with the slide')

# Define the fields for marshaling slide data in responses
slide_fields = {
	'_id': fields.String(attribute='_id'),
	'title': fields.String,
	'content': fields.String,
	'content_type': fields.String,
	'author_id': fields.String,
	'departments': fields.List(fields.String),
}

class SlideList(Resource):
	"""
	Resource class for managing collections of slides.
	"""
	def __init__(self, mongo):
		self.mongo = mongo

	@marshal_with(slide_fields)
	def get(self):
		"""
		Get a list of all slides.
		Returns:
			List[Slide]: A list of all slides.
		"""
		slides_data = self.mongo.db.slides.find()
		slides = [SlideFactory.slide_from_dict(slide_data) for slide_data in slides_data]
		return slides, 200

	def post(self):
		"""
		Create a new slide.
		"""
		args = slide_parser.parse_args()
		title = args['title']
		content = args['content']
		content_type = args['content_type']
		author_id = args['author_id']
		image_url = args['image_url']
		video_url = args['video_url']
		departments = args.get('departments', [])

		if Slide.find_by_title(title, self.mongo):
			return {"message": f"Slide titled [{title}] already exists"}, 400

		slide = SlideFactory.create_slide(title, content, content_type, author_id, image_url, video_url)

		if slide:
			pass

			for department_name in departments:
				department = Department.find_by_name(department_name, self.mongo)

				if department:
					slide.add_department(department.name)
				else:
					return {"message": f"Department [{department_name}] not found"}, 404

			slide_id = slide.save(self.mongo)

			return {'message': 'Slide created', 'slide_id': slide_id}, 201
		
		return {'message': 'Slide NOT created'}, 400
	
	def delete(self):
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
			slide_dict = Slide.find_by_title(slide_title, self.mongo)
			slide = SlideFactory.slide_from_dict(slide_dict)
			if slide:
				self.mongo.db.slides.delete_one({'_id': slide._id})
				deleted_count += 1

		return {"message": f"{deleted_count} slides deleted"}, 200

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
slide_parser.add_argument('title', type=str, required=True, help='Title of the slide')
slide_parser.add_argument('image_rul', type=str, required=True, help='image_rul of the slide')
slide_parser.add_argument('slide_type', type=str, required=True, help='Type of content of the slide') 
slide_parser.add_argument('author_id', type=str, required=True, help='Author ID of the slide')
slide_parser.add_argument('departments', type=list, location='json', help='Departments associated with the slide')

slide_parser_patch = reqparse.RequestParser()
slide_parser_patch.add_argument('title', type=str, required=False, help='Title of the slide')
slide_parser_patch.add_argument('content', type=str, required=False, help='Content of the slide')
slide_parser_patch.add_argument('slide_type', type=str, required=False, help='Type of content of the slide') 
slide_parser_patch.add_argument('author_id', type=str, required=False, help='Author ID of the slide')
slide_parser_patch.add_argument('departments', type=list, location='json', help='Departments associated with the slide')

# Define the fields for marshaling slide data in responses
slide_fields = {
	'_id': fields.String(attribute='_id'),
	'title': fields.String,
	'image_url': fields.String,
	'slide_type': fields.String,
	'author_id': fields.String,
	'departments': fields.List(fields.String),
}

class SlideResource(Resource):
	"""
	Resource class for managing individual slides.
	"""


	def get(self, slide_title):
		"""
		Get details of a specific slide by title.
		"""
		slide_dict = Slide.find_by_title(slide_title)
		if slide_dict:
			return slide_dict, 200
		return {"message": "Slide not found"}, 404

	def patch(self, slide_title):
		"""
		Update a specific slide by title (partial update).
		"""
		args = slide_parser_patch.parse_args()
		slide_dict = Slide.find_by_title(slide_title)

		if not slide_dict:
			return {"message": "Slide not found"}, 404
		
		slide_factory = SlideFactory()
		slide = slide_factory.create_slide(slide_dict)

		if 'departments' in args:
			args = slide_parser_patch.parse_args()
			new_departments = args.get('departments', [])

			old_departments = slide.get_departments()

			for department_name in old_departments:
				department_data = Department.find_by_name(department_name)

				department = Department.from_dict(department_data)
				department.remove_slide(slide_title)

				department.save

			for department_name in new_departments:
				department_data = Department.find_by_name(department_name)

				if department_data:
					department = Department.from_dict(department_data)
					slide.add_department(department.name)
					department.add_slide(slide.title)
					department.save()
				else:
					return {"message": f"Department [{department_name}] not found"}, 404

		if 'content' in args and args['content']:
			if isinstance(slide, ImageSlide):
				slide.add_image_url = args['content']

		# TODO add changing names
		#if 'title' in args and args['title']:
			#slide.title = args['title']

		slide.save()
		

		return {'message': 'Slide updated', 'slide_title': slide_title}, 200
	
	def delete(self, slide_title):
		"""
		Delete a slide by its title.

		Args:
			slide_title (str): The title of the slide to delete.

		Returns:
			dict: A message indicating the result of the deletion.
		"""
		slide_dict = Slide.find_by_title(slide_title)

		if not slide_dict:
			return {"message": "Slide not found"}, 404
		
		slide_factory = SlideFactory()
		slide = slide_factory.create_slide(slide_dict)

		if slide:
			slide.delete_me()
			return {"message": f"Slide '{slide_title}' deleted"}, 200
		else:
			return {"message": "Slide not found"}, 404

"""
	def put(self, slide_title):
"""
		#Update a specific slide by title (full update).
"""
		args = slide_parser.parse_args()
		title = args['title']
		content = args['content']
		content_type = args['content_type']
		author_id = args['author_id']
		departments = args.get('departments', [])

		slide_dict = Slide.find_by_title(slide_title)
		slide = SlideFactory.slide_from_dict(slide_dict)

		if not slide:
			return {"message": "Slide not found"}, 404

		slide.title = title
		slide.content = content
		slide.content_type = content_type
		slide.author_id = author_id

		slide.clear_departments()

		for department_name in departments:
			department_data = Department.find_by_name(department_name)

			if department_data:
				department = Department.from_dict(department_data)
				slide.add_department(department.name)
				department.add_slide(slide.title)
				department.save()
			else:
				return {"message": f"Department [{department_name}] not found"}, 404

		slide.save()

		return {'message': 'Slide updated', 'slide_title': slide_title}, 200
	
"""
	

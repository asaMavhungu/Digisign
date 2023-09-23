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
			new_name = args[slide_name]
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

		result, code  = slide.delete_database_entry()

		return result, code

	def patch_depracated(self, slide_title):
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
				slide.remove_department(department_name)
				
				department.save()

			for department_name in new_departments:
				department_data = Department.find_by_name(department_name)

				if department_data:
					department = Department.from_dict(department_data)
					
					slide.add_department(department.name)
					department.add_slide(slide.title)
					
					department.save()
				else:
					return {"message": f"Department [{department_name}] not found"}, 404

		if 'image_url' in args and args['image_url']:
			print("TTTTTTTTTTTTTTTTTTTTTTTTTTT")
			if isinstance(slide, ImageSlide):
				new_url = args['image_url']
				slide.add_image_url(new_url)
				print("VBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
				slide.save()

		# TODO add changing names
		#if 'title' in args and args['title']:
			#slide.title = args['title']

		print()

		slide.save()
		

		return {'message': 'Slide updated', 'slide_title': slide_title}, 200
	
	def delete_deprecated(self, slide_title):
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
	

from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
from bson.objectid import ObjectId
from api.models.Slide import Slide
from api.models.Department import Department

slide_parser = reqparse.RequestParser()
slide_parser.add_argument('title', type=str, required=True, help='Title of the slide')
slide_parser.add_argument('content', type=str, required=True, help='Content of the slide')
slide_parser.add_argument('author_id', type=str, required=True, help='Author ID of the slide')
slide_parser.add_argument('departments', type=list, location='json', help='Departments associated with the slide')

slide_parser_patch = reqparse.RequestParser()
slide_parser_patch.add_argument('title', type=str, required=False, help='Title of the slide')
slide_parser_patch.add_argument('content', type=str, required=False, help='Content of the slide')
slide_parser_patch.add_argument('author_id', type=str, required=False, help='Author ID of the slide')
slide_parser_patch.add_argument('departments', type=list, location='json', help='Departments associated with the slide')

slide_fields = {
	'_id': fields.String(attribute='_id'),
	'title': fields.String,
	'content': fields.String,
	'author_id': fields.String,
	'departments': fields.List(fields.String),
}

class SlideResource(Resource):
	def __init__(self, mongo):
		self.mongo = mongo

	@marshal_with(slide_fields)
	def get(self, slide_title):
		slide = Slide.find_by_title(slide_title, self.mongo)
		if slide:
			return slide, 200
		return {"message": "Slide not found"}, 404

	@marshal_with(slide_fields)
	def post(self):
		args = slide_parser.parse_args()
		title = args['title']
		content = args['content']
		author_id = args['author_id']
		departments = args.get('departments', [])

		if Slide.find_by_title(title, self.mongo):
			return {"message": f"Slide titled [{title}] already exists"}, 400

		slide = Slide(title, content, author_id)

		for department_name in departments:
			department = Department.find_by_name(department_name, self.mongo)

			if department:
				slide.add_department(department.name)
			else:
				return {"message": f"Department [{department_name}] not found"}, 404

		slide_id = slide.save(self.mongo)

		return {'message': 'Slide created', 'slide_id': slide_id}, 201

	@marshal_with(slide_fields)
	def patch(self, slide_title):
		args = slide_parser_patch.parse_args()
		slide = Slide.find_by_title(slide_title, self.mongo)

		if not slide:
			return {"message": "Slide not found"}, 404

		if 'departments' in args:
			args = slide_parser.parse_args()
			new_departments = args.get('departments', [])

			if not isinstance(new_departments, list):
				return {"message": "Invalid 'departments' format, expected a list"}, 400

			for department_name in new_departments:
				department = Department.find_by_name(department_name, self.mongo)

				if department:
					slide.add_department(department.name)
				else:
					return {"message": f"Department [{department_name}] not found"}, 404

		if 'content' in args and args['content']:
			slide.content = args['content']

		if 'title' in args and args['title']:
			slide.title = args['title']

		slide.save(self.mongo)

		return {'message': 'Slide updated', 'slide_title': slide_title}, 200

	@marshal_with(slide_fields)
	def put(self, slide_title):
		args = slide_parser.parse_args()
		title = args['title']
		content = args['content']
		author_id = args['author_id']
		departments = args.get('departments', [])

		slide = Slide.find_by_title(slide_title, self.mongo)

		if not slide:
			return {"message": "Slide not found"}, 404

		slide.title = title
		slide.content = content
		slide.author_id = author_id

		slide.clear_departments()

		for department_name in departments:
			department = Department.find_by_name(department_name, self.mongo)

			if department:
				slide.add_department(department.name)
			else:
				return {"message": f"Department [{department_name}] not found"}, 404

		slide.save(self.mongo)

		return {'message': 'Slide updated', 'slide_title': slide_title}, 200

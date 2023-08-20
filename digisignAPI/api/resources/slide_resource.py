from flask import request
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from api.models.Slide import Slide


# Define request parsers
department_parser = reqparse.RequestParser()
department_parser.add_argument('name', type=str, required=True, help='Name of the department')

slide_parser = reqparse.RequestParser()
slide_parser.add_argument('title', type=str, required=True, help='Title of the slide')
slide_parser.add_argument('content', type=str, required=True, help='Content of the slide')
slide_parser.add_argument('author_id', type=str, required=True, help='Author ID of the slide')


class SlideResource(Resource):

	def __init__(self, mongo):
		self.mongo = mongo

	def post(self):
		args = slide_parser.parse_args()
		title = args['title']
		content = args['content']
		author_id = args['author_id']
		
		# Create a new slide instance
		slide = Slide(title, content, author_id)

		# Save the slide to the database
		slide_id = slide.save(self.mongo)

		return {'message': 'Slide created', 'slide_id': slide_id}, 201

# Add API routes for adding departments and slides


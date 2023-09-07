from flask import request
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from api.models.Slide import Slide
from api.models.Department import Department


# Define request parsers
#department_parser = reqparse.RequestParser()
#department_parser.add_argument('name', type=str, required=True, help='Name of the department')

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


class SlideResource(Resource):

	def __init__(self, mongo):
		self.mongo = mongo

	def get(self, slide_title):
		slide = Slide.find_by_title(slide_title, self.mongo)
		#print(type(slide))
		#user = User.from_dict(userDict)
		if slide:
			print(slide.to_dict())
			return slide.to_dict(), 200
			#return user.to_dict()
		return {"message": "Slide not found"}, 404

	def post(self):
		args = slide_parser.parse_args()
		title = args['title']
		content = args['content']
		author_id = args['author_id']
		departments = args.get('departments', [])
		
		# Create a new slide instance

		if Slide.find_by_title(title, self.mongo):
			return {"message": f"Slide titled [{title}] already exists"}, 400

		slide = Slide(title, content, author_id)

		for department_name in departments:
			department = Department.find_by_name(department_name, self.mongo)

			if department:
				# Associate the department with the slide
				slide.add_department(department.name)
			else:
				return {"message": f"Department [{department_name}] not found"}, 404

		# Save the slide to the database
		slide_id = slide.save(self.mongo)

		return {'message': 'Slide created', 'slide_id': slide_id}, 201

	def patch(self, slide_title):
		args = slide_parser_patch.parse_args()	

		# Find the slide by slide_id
		slide = Slide.find_by_title(slide_title, self.mongo)

		if not slide:
			return {"message": "Slide not found"}, 404

		if 'departments' in args:
			args = slide_parser.parse_args()
			new_departments = args.get('departments', [])
			print(new_departments)
			# Ensure that new_departments is a list
			if not isinstance(new_departments, list):
				return {"message": "Invalid 'departments' format, expected a list"}, 400
			# Create or retrieve the department (you should have a Department class)
			
			for department_name in new_departments:
				department = Department.find_by_name(department_name, self.mongo)

				if department:
					# Associate the department with the slide
					slide.add_department(department.name)
				else:
					return {"message": f"Department [{department_name}] not found"}, 404
	
		if 'content' in args and args['content']:
			slide.content = args['content']

		if 'title' in args and args['title']:
			slide.title = args['title']

		slide.save(self.mongo)

		return {'message': 'Slide updated', 'slide_title': slide_title}, 200	

		
	
	def put(self, slide_title):
		args = slide_parser.parse_args()
		title = args['title']
		content = args['content']
		author_id = args['author_id']
		departments = args.get('departments', [])

		print(departments)

		slide = Slide.find_by_title(slide_title, self.mongo)

		if not slide:
			return {"message": "Slide not found"}, 404
		
		# Update the slide attributes
		slide.title = title
		slide.content = content
		slide.author_id = author_id

		slide.clear_departments()

		for department_name in departments:
			department = Department.find_by_name(department_name, self.mongo)

			if department:
				# Associate the department with the slide
				slide.add_department(department.name)
			else:
				return {"message": f"Department [{department_name}] not found"}, 404

		# Save the updated slide
		slide.save(self.mongo)
	
		return {'message': 'Slide updated', 'slide_title': slide_title}, 200
	
# Add API routes for adding departments and slides


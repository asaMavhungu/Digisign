from flask_pymongo import PyMongo
from bson.objectid import ObjectId

class DatabaseTable():

	def __init__(self, collection):
		self.collection = collection

	def getData(self):
		slides_data = self.collection.find()
		return slides_data

	def insert_one(self, slide_data: dict):
		result = self.collection.insert_one(slide_data)
		self._id = result.inserted_id
		return str(result.inserted_id)
	
	def update_one(self, slide_id, slide_data: dict):
		# Update the existing slide document
		self.collection.update_one({'_id': slide_id}, {'$set': slide_data})
		return self._id
	
	def delete_one(self, slide_id: str):
		self.collection.delete_one({'_id': slide_id})

	def find_by_id(self, slide_id: str) -> (dict | None):
		"""
		Finds a slide by its unique slide ID (ObjectId) in the database.

		:param slide_id: The unique identifier of the slide.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: slide data or None if not found.
		"""
		slide_data = self.collection.find_one({'_id': ObjectId(slide_id)})
		if slide_data:
			return slide_data
		return None

	def find_by_title(self, title: str) -> (dict | None):
		# TODO Remove redundancy of creating Slide object
		"""
		Finds slides by their title in the database.

		:param title: The title of the slide to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: slide data of Slide class matching the title or an empty list if not found.
		"""
		slide_data = self.collection.find_one({'title': title})
		if slide_data:
			return slide_data
		return None
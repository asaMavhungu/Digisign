
from flask import Flask
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from api.models.Department import Department

from database.DatabaseTable import DatabaseTable


class MongoDBClient:
	def __init__(self, uri):
		self.client = MongoClient(uri)
		self.db = self.client.get_database()

		self.SlidesTable = DatabaseTable(self.db.slides)
		self.DepartmentTable = DatabaseTable(self.db.departments)
		self.DeviceTable = DatabaseTable(self.db.devices)

		try:
			self.client.admin.command('ping')
			print("Connected to MongoDB Atlas cluster!")
		except Exception as e:
			print(e)


	def get_user(self, user_id):
		return self.db.users.find_one({'_id': user_id})

	def create_user(self, user_data):
		return self.db.users.insert_one(user_data).inserted_id
	
	def find_department_by_id(self, department_id):
		"""
		Finds a department by its unique department ID (ObjectId) in the database.

		:param department_id: The unique identifier of the department.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Department class or None if not found.
		"""
		department_data = self.db.departments.find_one({'_id': ObjectId(department_id)})
		if department_data:
			return Department.from_dict(department_data)
		return None
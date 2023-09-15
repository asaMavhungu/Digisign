from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from database.mongoDatabase import MongoDatabase
from tinydb import TinyDB
from database.tinyDatabase import TinyDatabase

class DatabaseClient():

	def __init__(self, conn: PyMongo | TinyDB, database_option: str = 'mongo'):
		self.connection = conn
		self.database = MongoDatabase()

		if database_option == 'mongo':
			self.database = MongoDatabase()
		
		elif database_option == 'tinyDB':
			self.database = TinyDatabase()
		
		pass

	def get_table(self, table_name: str):
		return self.database.get_table(self.connection, table_name)

	def get_one(self, table_name: str, field_name: str, field_value: str):
		return self.database.get_one(self.connection, table_name, field_name, field_value)
	
	def insert_entry(self, table_name: str, entry_data: dict):
		return self.database.insert_entry(self.connection, table_name, entry_data)
	
	def update_entry(self, table_name: str, field_name: str, field_value: str, update_data: dict):
		return self.database.update_entry(self.connection, table_name, field_name, field_value, update_data)
	
	def delete_entry(self, table_name: str, field_name: str, field_value: str):
		return self.database.delete_entry(self.connection, table_name, field_name, field_value)
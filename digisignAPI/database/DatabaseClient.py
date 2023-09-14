from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from database.mongoDatabase import MongoDatabase

class DatabaseClient():

	def __init__(self, conn: MongoClient):
		self.connection = conn
		pass

	def get_table(self, table_name: str):
		return MongoDatabase.get_table(self.connection, table_name)

	def get_one(self, table_name: str, entry_name: str):
		return MongoDatabase.get_one(self.connection, table_name, entry_name)
	
	def insert_entry(self, table_name: str, entry_data: dict):
		return MongoDatabase.insert_entry(self.connection, table_name, entry_data)
	
	def update_entry(self, table_name: str, entry_name: str, update_data: dict):
		return MongoDatabase.update_entry(self.connection, table_name, entry_name, update_data)
	
	def delete_entry(self, table_name: str, entry_name: str):
		return MongoDatabase.delete_entry(self.connection, table_name, entry_name)
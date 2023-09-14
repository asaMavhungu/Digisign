

from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, jsonify
from pymongo.database import Database
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId



class MongoDatabase:
	def __init__(self):
		# TODO Properly make this an interface
		pass

	@staticmethod
	def get_table(conn: PyMongo, table_name: str):
		"""
		Retrieve all documents from a specified collection.

		Args:
			conn (PyMongo instance)
			table_name (str): The name of the collection (table) to retrieve documents from.

		Returns:
			pymongo.cursor.Cursor: A cursor object that can be used to iterate over the documents.
			(Iterable container of python dictionaries)

		Raises:
			CollectionNotFoundError: If the specified collection does not exist.

		Example:
			To retrieve all documents from the "slides" collection:
			>>> cursor = getTable(my_connection, "slides")
			>>> for document in cursor:
			>>>     print(document)
		"""
		# TODO Type checking turned off because of NONE
		tables = conn.db.list_collection_names() # type: ignore
		if table_name in tables:
			collection = conn.db[table_name.lower()] # type: ignore
			cursor = collection.find()
			return cursor

	@staticmethod
	def get_one(conn: PyMongo, table_name: str, field_name: str, field_value: str):
		"""
		Retrieve a single document from a specified collection based on a custom field and its value.

		Args:
			conn (PyMongo): A PyMongo instance for connecting to the MongoDB server.
			table_name (str): The name of the collection (table) to retrieve the document from.
			field_name (str): The name of the field to search for.
			field_value (str): The value of the field to search for.

		Returns:
			dict or None: A dictionary representing the retrieved document if found, or None if not found.

		Raises:
			CollectionNotFoundError: If the specified collection does not exist.

		Example:
			To retrieve a specific document with a custom field "name" equal to "example_slide" from the "slides" collection:
			>>> slide = get_one(my_connection, "slides", "name", "example_slide")
			>>> if slide:
			>>>     print(slide)
			>>> else:
			>>>     print("Slide not found.")
		"""
		# TODO Type checking turned off because of NONE
		# Ensure table_name is lowercase for case-insensitive matching
		table_name = table_name.lower()

		tables = conn.db.list_collection_names() # type: ignore

		if table_name in tables:

			# Access the database and the specified collection
			db = conn.db
			collection = conn.db[table_name.lower()] # type: ignore 

			# Construct the query to find the document based on the custom field
			query = {field_name: field_value}

			# Retrieve the document using find_one
			document = collection.find_one(query)
			if document and "_id" in document:
				document["_id"] = str(document["_id"])
				print("*****************================================****************")
			return document

	@staticmethod
	def insert_entry(conn: PyMongo, table_name: str, entry_data: dict):
		"""
		Insert a new document into a specified collection.

		Args:
			conn (MongoClient): A MongoClient instance for connecting to the MongoDB server.
			table_name (str): The name of the collection (table) to insert the document into.
			entry_data (dict): A dictionary representing the data to be inserted.

		Returns:
			str: The unique identifier (_id) of the inserted document.

		Raises:
			CollectionNotFoundError: If the specified collection does not exist.

		Example:
			To insert a new document into the "slides" collection:
			>>> data = {'_id': 'new_slide', 'title': 'New Slide', 'content': 'This is a new slide.'}
			>>> entry_id = insert_entry(my_connection, "slides", data)
			>>> print(f"Inserted document ID: {entry_id}")
		"""
		# Check if the requested table_name exists
		# TODO Type checking turned off because of NONE
		tables = conn.db.list_collection_names() # type: ignore
		if table_name in tables:
			collection = conn.db[table_name.lower()] # type: ignore
			result = collection.insert_one(entry_data)
			return str(result.inserted_id)



	@staticmethod
	def update_entry(conn: PyMongo, table_name: str, field_name: str, field_value: str, update_data: dict):
		"""
		Update an existing document in a specified collection.

		Args:
			conn (MongoClient): A MongoClient instance for connecting to the MongoDB server.
			table_name (str): The name of the collection (table) to update the document in.
			entry_name (str): The identifier or name of the entry/document to update.
			update_data (dict): A dictionary representing the data to be updated.

		Returns:
			str: The unique identifier (_id) of the updated document.

		Raises:
			CollectionNotFoundError: If the specified collection does not exist.

		Example:
			To update an existing document named "existing_slide" in the "slides" collection:
			>>> data = {'title': 'Updated Slide Title'}
			>>> entry_id = update_entry(my_connection, "slides", "existing_slide", data)
			>>> print(f"Updated document ID: {entry_id}")
		"""
		# Check if the requested table_name exists
		# TODO Type checking turned off because of NONE
		tables = conn.db.list_collection_names() # type: ignore
		if table_name in tables:
			collection = conn.db[table_name.lower()] # type: ignore
			query = {field_name: field_value}
			document = collection.find_one(query)
			if document:
				result = collection.update_one(query, {'$set': update_data})
				if result.modified_count > 0:
					return True
				else:
					return False

	@staticmethod
	def delete_entry(conn: PyMongo, table_name: str, field_name: str, field_value: str):
		"""
		Delete an existing document from a specified collection.

		Args:
			conn (MongoClient): A MongoClient instance for connecting to the MongoDB server.
			table_name (str): The name of the collection (table) to delete the document from.
			entry_name (str): The identifier or name of the entry/document to delete.

		Returns:
			bool: True if the document was successfully deleted, False otherwise.

		Raises:
			CollectionNotFoundError: If the specified collection does not exist.

		Example:
			To delete an existing document named "existing_slide" from the "slides" collection:
			>>> result = delete_entry(my_connection, "slides", "existing_slide")
			>>> if result:
			>>>     print("Document deleted.")
			>>> else:
			>>>     print("Document not found or could not be deleted.")
		"""
		# Check if the requested table_name exists
		# TODO Type checking turned off because of NONE
		tables = conn.db.list_collection_names() # type: ignore
		if table_name in tables:
			collection = conn.db[table_name.lower()] # type: ignore
			query = {field_name: field_value}
			result = collection.delete_one(query)
			if result.deleted_count > 0:
				return True
			else:
				return False  # Document with the specified entry_name not found
		




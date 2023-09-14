

from flask import Flask
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from api.models.Department import Department


class MongoDatabase:
	def __init__(self):
		# TODO Properly make this an interface
		pass

	@staticmethod
	def get_table(conn: MongoClient, table_name: str):
		"""
		Retrieve all documents from a specified collection.

		Args:
			conn (MongoClient): A MongoClient instance for connecting to the MongoDB server.
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
		tables = conn.db.list_collection_names()
		if table_name in tables:
			collection = conn.db[table_name.lower()]
			cursor = collection.find()
			return cursor
		else:
			# Table not found
			raise CollectionNotFoundError(f"Collection '{table_name}' not found.")
		
	@staticmethod
	def get_one(conn: MongoClient, table_name: str, entry_name: str):
		"""
		Retrieve a single document from a specified collection based on its entry_name.

		Args:
			conn (MongoClient): A MongoClient instance for connecting to the MongoDB server.
			table_name (str): The name of the collection (table) to retrieve the document from.
			entry_name (str): The identifier or name of the entry/document to retrieve.

		Returns:
			dict or None: A dictionary representing the retrieved document if found, or None if not found.

		Raises:
			CollectionNotFoundError: If the specified collection does not exist.

		Example:
			To retrieve a specific document named "example_slide" from the "slides" collection:
			>>> slide = getOne(my_connection, "slides", "example_slide")
			>>> if slide:
			>>>     print(slide)
			>>> else:
			>>>     print("Slide not found.")

			Note:
				- The method converts the `table_name` to lowercase to ensure case-insensitive matching.
				- If the `table_name` matches known collections, it retrieves the document.
				- The `type: ignore` comment is used to suppress type hint errors related to the return value of find_one.
		"""
		tables = conn.db.list_collection_names()
		if table_name in tables:
			collection = conn.db[table_name.lower()]
			#TODO the type ignore is to remove the type error. want to remove ambiguity of the 'UNKNOWN' type return by find_one
			doc: dict = collection.find_one(entry_name) # type: ignore 
			return doc
		else:
			# Table not found
			raise CollectionNotFoundError(f"Collection '{table_name}' not found.")
		

	@staticmethod
	def insert_entry(conn: MongoClient, table_name: str, entry_data: dict):
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
		tables = conn.db.list_collection_names()
		if table_name in tables:
			collection = conn.db[table_name.lower()]
			result = collection.insert_one(entry_data)
			return str(result.inserted_id)
		else:
			# If the table_name doesn't match any known collection, raise the exception
			raise CollectionNotFoundError(f"Collection '{table_name}' not found.")

	@staticmethod
	def update_entry(conn: MongoClient, table_name: str, entry_name: str, update_data: dict):
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
		tables = conn.db.list_collection_names()
		if table_name in tables:
			collection = conn.db[table_name.lower()]
			result = collection.update_one({'_id': entry_name}, {'$set': update_data})
			if result.modified_count > 0:
				return entry_name
			else:
				return None  # Document with the specified entry_name not found
		else:
			# If the table_name doesn't match any known collection, raise the exception
			raise CollectionNotFoundError(f"Collection '{table_name}' not found.")

	@staticmethod
	def delete_entry(conn: MongoClient, table_name: str, entry_name: str):
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
		tables = conn.db.list_collection_names()
		if table_name in tables:
			collection = conn.db[table_name.lower()]
			result = collection.delete_one({'_id': entry_name})
			if result.deleted_count > 0:
				return True
			else:
				return False  # Document with the specified entry_name not found
		else:
			# If the table_name doesn't match any known collection, raise the exception
			raise CollectionNotFoundError(f"Collection '{table_name}' not found.")
		


class CollectionNotFoundError(Exception):
	"""Just for the Exception thing"""
	#TODO FIX exception handling
	pass

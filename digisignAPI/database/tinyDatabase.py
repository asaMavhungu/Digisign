from flask import Flask
from tinydb import TinyDB, Query

"""
app = Flask(__name__)

# Create a TinyDB instance and specify the data file
db = TinyDB('data.json')

users_table = db.table('users')
products_table = db.table('products')


@app.route('/add_user', methods=['POST'])
def add_user():
	user_data = {'name': 'Alice', 'age': 25}
	users_table.insert(user_data)
	return 'User added successfully'
"""


from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, jsonify
from pymongo.database import Database
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId

def insert_with_unique_id(table, data):
	# Define your custom ID field name
	id_field = "_id"

	# Check if the table is empty
	if not table:
		max_id = 0
	else:
		# Get the maximum existing ID in the table
		max_id = max(table.all(), key=lambda x: x.get(id_field, 0)).get(id_field, 0)


	# Generate a new unique ID
	new_id = max_id + 1

	# Check if the generated ID is unique
	while table.contains(Query()[id_field] == new_id):
		new_id += 1

	# Add the ID to the data and insert it into the table
	data[id_field] = new_id
	table.insert(data)

	return new_id


class TinyDatabase:
	def __init__(self):
		pass

	@staticmethod
	def get_table(conn: TinyDB, table_name: str):
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
		db = conn
		tables = db.tables()
		print(tables)
		if table_name in tables:
			collection = db.table(table_name)
			print(collection)
			return collection

	@staticmethod
	def get_one(conn: TinyDB, table_name: str, field_name: str, field_value: str):
		"""
		Retrieve a single document from a specified collection based on a custom field and its value.

		Args:
			conn (TinyDB): A TinyDB instance representing the database.
			table_name (str): The name of the collection (table) to retrieve the document from.
			field_name (str): The name of the field to search for.
			field_value (str): The value of the field to match.

		Returns:
			dict or None: A dictionary representing the retrieved document if found, or None if not found.

		Example:
			To retrieve a specific document from the "departments" collection where the "name" field is "Department A":
			>>> department = get_one(my_db, "departments", "name", "Department A")
			>>> if department:
			>>>     print(department)
			>>> else:
			>>>     print("Entry not found.")
		"""
		# TODO Type checking turned off because of NONE
		# Ensure table_name is lowercase for case-insensitive matching
		table_name = table_name.lower()
		db = conn

		tables = db.tables()
		print(tables)

		if table_name in tables:

			# Access the database and the specified collection
			collection = db.table(table_name)


			query = Query()
			document = collection.get(query[field_name] == field_value)
			# TODO May return a container
			if document and "_id" in document:
				document["_id"] = str(document["_id"]) # type: ignore
				print("*****************================================****************")
			return document

	@staticmethod
	def insert_entry(conn: TinyDB, table_name: str, entry_data: dict):
		"""
		Insert a new document into a specified collection.

		Args:
			db (TinyDB): The TinyDB instance.
			table_name (str): The name of the collection (table) to insert the document into.
			entry_data (dict): A dictionary representing the data to be inserted.

		Returns:
			int: The unique identifier (document ID) of the inserted document.

		Example:
			To insert a new document into the "departments" collection:
			>>> data = {'name': 'Department X', 'description': 'New department'}
			>>> entry_id = insert_entry(my_db, "departments", data)
			>>> print(f"Inserted document ID: {entry_id}")
		"""
		# Check if the requested table_name exists
		db = conn
		tables = db.tables()
		print(tables)
		print(conn)

		collection = db.table(table_name)
		#entry_id = collection.insert(entry_data)
		entry_id = insert_with_unique_id(collection, entry_data)
		return entry_id



	@staticmethod
	def update_entry(conn: TinyDB, table_name: str, field_name: str, field_value: str, update_data: dict):
		"""
		Update an existing document in a specified collection based on a custom field and its value.

		Args:
			db (TinyDB): The TinyDB instance.
			table_name (str): The name of the collection (table) to update the document in.
			field_name (str): The name of the field to search for.
			field_value (str): The value to match in the specified field.
			update_data (dict): A dictionary representing the data to be updated.

		Returns:
			bool: True if the document was successfully updated, False otherwise.

		Example:
			To update an existing document in the "departments" collection where the "name" field is "Department X":
			>>> filter_field = "name"
			>>> filter_value = "Department X"
			>>> data = {'description': 'Updated department description'}
			>>> success = update_entry(my_db, "departments", filter_field, filter_value, data)
			>>> if success:
			>>>     print("Document updated successfully.")
			>>> else:
			>>>     print("Document not found or update failed.")
		"""
		# Check if the requested table_name exists
		# TODO Type checking turned off because of NONE
		db = conn
		tables = db.tables()
		if table_name in tables:
			table = db.table(table_name)
			query_class = Query()
			query = query_class[field_name] == field_value
			if table.contains(query):
				table.update(update_data, query)
				return True
			else:
				return False

	@staticmethod
	def delete_entry(conn: TinyDB, table_name: str, field_name: str, field_value: str):
		"""
		Delete a document from a specified collection based on a custom field and its value.

		Args:
			db (TinyDB): The TinyDB instance.
			table_name (str): The name of the collection (table) to delete the document from.
			field_name (str): The name of the field to search for.
			field_value (str): The value to match in the specified field.

		Returns:
			bool: True if the document was successfully deleted, False otherwise.

		Example:
			To delete a document from the "departments" collection where the "name" field is "Department X":
			>>> filter_field = "name"
			>>> filter_value = "Department X"
			>>> success = delete_entry(my_db, "departments", filter_field, filter_value)
			>>> if success:
			>>>     print("Document deleted successfully.")
			>>> else:
			>>>     print("Document not found or delete failed.")
		"""
		# Check if the requested table_name exists
		db = conn
		tables = db.tables()
		if table_name in tables:
			table = db.table(table_name)
			query_class = Query()
			query = query_class[field_name] == field_value
			if table.contains(query):
				table.remove(query)
				return True
			else:
				return False
		
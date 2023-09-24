from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from database.sql_models import User, Department, Device, Slide, SharedSlide, SlideAssignment
from sqlalchemy.exc import NoResultFound


Base = automap_base()

engine = create_engine('sqlite:///my_database.db')
#Session = sessionmaker(bind=engine)
#session = Session()
#ses

Base.prepare(autoload_with=engine)

from sqlalchemy import create_engine, inspect

# Create the SQLite database engine
engine = create_engine('sqlite:///my_database.db')

# Create an Inspector to inspect the database structure
inspector = inspect(engine)

# Get the table name of the Department model
table_name = Department.__table__.name

# Get information about the Department table
table_info = inspector.get_columns(table_name)

# Print the attributes (columns) of the Department table
print(f"Attributes of table '{table_name}':")
for column in table_info:
	print(column['name'])

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

def model_instance_to_json(instance, include_relationships=True):
	my_dict = {}
	for column in instance.__table__.columns:
		key = f"{column.name}"
		val = f"{getattr(instance, column.name)}"
		my_dict[key] = val

	if include_relationships:
		for relationship in instance.__mapper__.relationships:
			rel_name = relationship.key
			related_records = getattr(instance, rel_name)
			if related_records is not None:
				if relationship.uselist:
					my_dict[rel_name] = [model_instance_to_json(record, include_relationships=False) for record in related_records]
				else:
					my_dict[rel_name] = model_instance_to_json(related_records, include_relationships=False)

	return my_dict

def get_table_class_deprecated(table_name, base):
	"""Retrieve an SQLAlchemy model class by table name."""
	print(Base.classes)
	if table_name in base.classes:
		return base.classes[table_name]
	else:
		raise ValueError(f"Table '{table_name}' not found in the database.")
	
def get_table_class(table_name: str):
	return eval(table_name.capitalize()[:-1])

def get_slide_name_by_id(slide_id):
	# Create a session
	Session = sessionmaker(bind=engine)
	session = Session()

	try:
		# Query the Slide table for the slide_name based on slide_id
		slide = session.query(Slide).filter_by(slide_id=slide_id).first()

		if slide:
			return slide.slide_name
		else:
			return None  # Return None if no slide with the given slide_id is found
	finally:
		session.close()  # Close the session to release resources


def get_table_data(table_name):
	# Create the SQLite database engine
	engine = create_engine('sqlite:///my_database.db')

	# Create a session
	Session = sessionmaker(bind=engine)
	session = Session()

	# Get the corresponding table class based on the table name
	table_class = get_table_class(table_name)

	if table_class is None:
		session.close()
		print({"error": f"Table '{table_name}' not found."})
		return

	# List of known relationship attributes (customize as needed)
	KNOWN_RELATIONSHIPS = ['slides', 'shared_slides', 'devices', 'department', 'assignments', 'current_user']
	KNOWN_RELATIONSHIPS = ['slides', 'shared_slides', 'devices', 'assignments', 'shared_departments', 'department', 'current_user']

	# Query all entries from the table
	table_class = get_table_class(table_name)
	entries = session.query(table_class).all()


	# Serialize the entries to a list of dictionaries
	entry_dicts = []
	for entry in entries:
		entry_dict = model_instance_to_json(entry)


		# Include information about relationships
		for attr_name in KNOWN_RELATIONSHIPS:
			if hasattr(table_class, attr_name):
				related_records = getattr(entry, attr_name)
				if isinstance(related_records, list):
					related_records_list = [model_instance_to_json(record) for record in related_records]
					entry_dict[attr_name] = related_records_list
				#else:
					#entry_dict[attr_name] = model_instance_to_json(related_records)

		entry_dicts.append(entry_dict)

	# Convert the list of dictionaries to JSON
	table_data = json.dumps(entry_dicts, default=str, indent=2)

	# Close the session
	session.close()

	#print("XXXXXXXXXXXXXXXXXXXXXXXXXXX")
	#print(entry_dicts)
	#print("XXXXXXXXXXXXXXXXXXXXXXXXXXX")

	return entry_dicts
	return table_data


from sqlalchemy.orm import Session

def create_entry(table_name, data):
	"""Create a new entry in the specified table with the provided data."""
	session = Session(bind=engine)
	try:
		table_class = get_table_class(table_name)
		new_entry = table_class(**data)
		session.add(new_entry)
		session.commit()
		return {"message": f"{table_name} entry created successfully.", "entry": model_instance_to_json(new_entry)} , 200
	except Exception as e:
		session.rollback()
		return {"error": f"Failed to create {table_name} entry: {str(e)}"}, 401
	finally:
		session.close()

def get_entry_deprecated(table_name, filter_dict):
	"""Get an entry from the specified table based on a filter dictionary."""
	session = Session(bind=engine)
	try:
		table_class = get_table_class(table_name)
		try:
			print("found $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
			print(filter_dict)
			entry = session.query(table_class).filter_by(**filter_dict).one()
			print("found $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
			return model_instance_to_json(entry)
		except NoResultFound:
			return {"error": f"No {table_name} entry found matching the filter."}
	finally:
		session.close()
		
def get_entry(table_name, filter_dict):
	"""Get an entry from the specified table based on a filter dictionary."""
	session = Session(bind=engine)
	try:
		table_class = get_table_class(table_name)
		try:
			entry = session.query(table_class).filter_by(**filter_dict).one()
			# Create a dictionary representation of the entry
			entry_dict = model_instance_to_json(entry)

			print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
			if hasattr(table_class, 'shared_slides'):
				for shared_slide in entry_dict.get('shared_slides', []):
					shared_slide['slide_name'] = get_slide_name_by_id(shared_slide['slide_id'])
				pass

			print(entry_dict)
			return entry_dict , 200

			# Include information about relationships (slides and devices)
			if hasattr(table_class, 'slides'):
				entry_dict['slides'] = [{'slide_id': slide.slide_id, 'slide_name': slide.slide_name} for slide in entry.slides]

			if hasattr(table_class, 'devices'):
				entry_dict['devices'] = [{'device_id': device.device_id, 'device_name': device.device_name} for device in entry.devices]
			if hasattr(table_class, 'shared_slides'):
				shared_slide_info = []
				for shared_slide in entry.shared_slides:
					shared_slide_info.append({
						'sharing_id': shared_slide.sharing_id,
						'to_department': {
							'department_id': shared_slide.to_department.department_id,
							'department_name': shared_slide.to_department.department_name
						},
						'from_department': {
							'department_id': shared_slide.from_department.department_id,
							'department_name': shared_slide.from_department.department_name
						},
						'slide_id': shared_slide.slide.slide_id
					})
				entry_dict['shared_slides'] = shared_slide_info
			print(entry_dict)
			print("CCCCCCCCCCCCCCCCCCCCCCCC")
			return entry_dict , 200
		except NoResultFound:
			return {"error": f"No {table_name} entry found matching the filter."} , 404
	finally:
		session.close()

def update_entry(table_name, filter_dict, data):
	"""Update an entry in the specified table based on a filter dictionary with the provided data."""
	session = Session(bind=engine)
	try:
		table_class = get_table_class(table_name)
		try:
			entry = session.query(table_class).filter_by(**filter_dict).one()
			for key, value in data.items():
				setattr(entry, key, value)
			session.commit()
			return {"message": f"{table_name} entry updated successfully.", "entry": model_instance_to_json(entry)}, 200
		except NoResultFound:
			return {"error": f"No {table_name} entry found matching the filter."}, 301
	except Exception as e:
		session.rollback()
		return {"error": f"Failed to update {table_name} entry: {str(e)}"}, 401
	finally:
		session.close()

def delete_entry(table_name, filter_dict):
	"""Delete an entry from the specified table based on a filter dictionary."""
	session = Session(bind=engine)
	try:
		table_class = get_table_class(table_name)
		try:
			entry = session.query(table_class).filter_by(**filter_dict).one()
			session.delete(entry)
			session.commit()
			return {"message": f"{table_name} entry deleted successfully."} , 200
		except NoResultFound:
			return {"error": f"No {table_name} entry found matching the filter."} , 301
	except Exception as e:
		session.rollback()
		return {"error": f"Failed to delete {table_name} entry: {str(e)}"}, 401
	finally:
		session.close()


# Example usage:
if __name__ == "__main__":
	table_name_to_query = "devices"  # Replace with the table name you want to query
	result = get_table_data(table_name_to_query)
	print(result)


	# Define the data for the new device
	new_device_data = {
		"device_name": "New Device Name",
		"department_id": 1,  # Replace with the actual department ID to which this device belongs
	}

	# Call the create_entry function to create the new device
	result = create_entry("devices", new_device_data)

	result = get_table_data(table_name_to_query)
	print(result)
	# Print the result
	print(result)

	# Specify the ID of the device you want to retrieve
	device_id_to_retrieve = 1  # Replace with the actual device ID you want to retrieve

	# Call the get_entry function to retrieve the device by ID
	# Example usage of get_entry with a filter dictionary
	filter_dict = {"device_name": "Device 2"}  # Replace with your filter criteria
	result = get_entry("devices", filter_dict)
	print(result)

	# Example usage of update_entry with a filter dictionary
	filter_dict = {"device_name": "Device 2"}  # Replace with your filter criteria
	update_data = {"device_name": "updated device name"}  # Replace with the data you want to update
	result = update_entry("devices", filter_dict, update_data)
	print(result)

	# Example usage of delete_entry with a filter dictionary
	print("asa")
	filter_dict = {"device_name": "Device 2"}  # Replace with your filter criteria
	result = delete_entry("devices", filter_dict)
	print(result)
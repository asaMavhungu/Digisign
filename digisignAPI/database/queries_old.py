from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.sql_models import User, Department, Device, Slide, SharedSlide, SlideAssignment
from sqlalchemy.exc import IntegrityError

# Function to create a user
def create_user(username, email, password):
	engine = create_engine('sqlite:///my_database.db')
	Session = sessionmaker(bind=engine)
	session = Session()

	try:
		new_user = User(username=username, email=email, password=password)
		session.add(new_user)
		session.commit()
		print("User created successfully.")
	except IntegrityError as e:  # Catch IntegrityError
		session.rollback()
		print(f"Error: Username '{username}' already exists.")
	except Exception as e:
		session.rollback()
		print(f"Error: {e}")
	finally:
		session.close()
		engine.dispose()

# Function to create departments
def create_departments(department_names):
	engine = create_engine('sqlite:///my_database.db')
	Session = sessionmaker(bind=engine)
	session = Session()

	try:
		departments = [Department(department_name=name) for name in department_names]
		session.add_all(departments)
		session.commit()
		print("Departments created successfully.")
	except IntegrityError as e:
		session.rollback()
		print(f"Error: {e}")
	except Exception as e:
		session.rollback()
		print(f"Error: {e}")
	finally:
		session.close()
		engine.dispose()

# Function to create devices
def create_devices(device_names):
	engine = create_engine('sqlite:///my_database.db')
	Session = sessionmaker(bind=engine)
	session = Session()

	try:
		devices = [Device(device_name=name) for name in device_names]
		session.add_all(devices)
		session.commit()
		print("Devices created successfully.")
	except IntegrityError as e:
		session.rollback()
		print(f"Error: {e}")
	except Exception as e:
		session.rollback()
		print(f"Error: {e}")
	finally:
		session.close()
		engine.dispose()

# Function to create slides
def create_slides(slide_data):
	engine = create_engine('sqlite:///my_database.db')
	Session = sessionmaker(bind=engine)
	session = Session()

	try:
		slides = [Slide(slide_name=data['name'], department_id=data['department_id'], current_user_id=data['user_id']) for data in slide_data]
		session.add_all(slides)
		session.commit()
		print("Slides created successfully.")
	except IntegrityError as e:
		session.rollback()
		print(f"Error: {e}")
	except Exception as e:
		session.rollback()
		print(f"Error: {e}")
	finally:
		session.close()
		engine.dispose()

# Function to assign devices to departments
def assign_devices_to_departments(department_id, device_ids):
	engine = create_engine('sqlite:///my_database.db')  # Replace with your actual database URL
	Session = sessionmaker(bind=engine)
	session = Session()

	department = session.query(Department).filter_by(department_id=department_id).first()
	if department:
		devices = session.query(Device).filter(Device.device_id.in_(device_ids)).all()
		department.devices.extend(devices)
		session.commit()
		
		# Refresh the department object to reflect the updated devices relationship
		session.refresh(department)
	else:
		print("Department not found.")

	session.close()
	engine.dispose()

# Function to assign slides to a device
def assign_slides_to_device(device_id, slide_ids):
	engine = create_engine('sqlite:///my_database.db')  # Replace with your actual database URL
	Session = sessionmaker(bind=engine)
	session = Session()

	for slide_id in slide_ids:
		slide_assignment = SlideAssignment(slide_id=slide_id, device_id=device_id)
		session.add(slide_assignment)

	session.commit()
	engine.dispose()

def disassociate_device_from_department(device_id, department_id):
	engine = create_engine('sqlite:///my_database.db')  # Replace with your actual database URL
	Session = sessionmaker(bind=engine)
	session = Session()

	try:
		# Retrieve the device and department objects
		device = session.query(Device).filter_by(device_id=device_id).first()
		department = session.query(Department).filter_by(department_id=department_id).first()

		if device and department:
			# Remove the device from the department's list of devices
			department.devices.remove(device)

			# Commit the changes to the database
			session.commit()
			return True
		else:
			return False  # Device or department not found
	except Exception as e:
		session.rollback()
		raise e
	finally:
		session.close()

def disassociate_slide_from_device(slide_id, device_id):
	engine = create_engine('sqlite:///my_database.db')  # Replace with your actual database URL
	Session = sessionmaker(bind=engine)
	session = Session()

	try:
		# Retrieve the slide and device objects
		slide = session.query(Slide).filter_by(slide_id=slide_id).first()
		device = session.query(Device).filter_by(device_id=device_id).first()

		if slide and device:
			# Remove the slide from the device's list of assigned slides
			device.assignments = [assignment for assignment in device.assignments if assignment.slide_id != slide_id]

			# Commit the changes to the database
			session.commit()
			return True
		else:
			return False  # Slide or device not found
	except Exception as e:
		session.rollback()
		raise e
	finally:
		session.close()

# Function to share slides with other departments
def share_slides_with_departments(from_department_id, to_department_id, slide_ids):
	engine = create_engine('sqlite:///my_database.db')  # Replace with your actual database URL
	Session = sessionmaker(bind=engine)
	session = Session()

	for slide_id in slide_ids:
		shared_slide = SharedSlide(from_department_id=from_department_id, to_department_id=to_department_id, slide_id=slide_id)
		session.add(shared_slide)

	session.commit()
	engine.dispose()


if __name__ == "__main__":
	# Replace with your actual data as needed
	print()
create_user("john_doe", "john@example.com", "password123")

department_names = ["Department 1", "Department 2"]
create_departments(department_names)

device_names = ["Device 1", "Device 2", "Device 3"]
create_devices(device_names)

slide_data = [
	{"name": "Slide 1", "department_id": 1, "user_id": 1},
	{"name": "Slide 2", "department_id": 2, "user_id": 1},
	{"name": "Slide 3", "department_id": 1, "user_id": 1}
]
create_slides(slide_data)

# Assign devices to departments
assign_devices_to_departments(1, [1, 2])  # Assign Device 1 and Device 2 to Department 1
assign_devices_to_departments(2, [3])     # Assign Device 3 to Department 2

# Share slides with other departments
share_slides_with_departments(1, 2, [1])  # Share Slide 1 from Department 1 with Department 2
share_slides_with_departments(2, 1, [2])  # Share Slide 2 from Department 2 with Department 1


device_id = 1
slide_ids = [1, 2, 3]

assign_slides_to_device(device_id, slide_ids)

device_id = 2
slide_ids = [2, 3]
assign_slides_to_device(device_id, slide_ids)
# Close the connection
#engine.dispose()

# Create an engine and session as usual
engine = create_engine('sqlite:///my_database.db')  # Replace with your actual database URL
Session = sessionmaker(bind=engine)
session = Session()

# Query the departments and retrieve their associated devices
departments_with_devices = session.query(Department).all()

for department in departments_with_devices:
	print(f"Department: {department.department_name}")
	print("Devices:")
	for device in department.devices:
		print(f"- {device.device_name}")

devices = session.query(Device).all()
print()
print()
for device in devices:
	print(f"Device: {device.device_name}")
	print("Deps:")
	#for dep in device.department:
	print(f"- {device.department.department_name}")

print()
print()
# Define the device name you want to query for
device_name_to_query = "Device 1"

# Query for the device by its unique attribute (device_name)
device = session.query(Device).filter(Device.device_name == device_name_to_query).first()

if device:
	# Access the associated slides through the 'assignments' relationship
	associated_slides = device.assignments

	if associated_slides:
		print(f"Slides associated with {device_name_to_query}:")
		for slide_assignment in associated_slides:
			slide = slide_assignment.slide
			if slide is None:
				print(f"Error: Associated slide does not exist in Slides Table")
			else:
				print(f"Slide ID: {slide.slide_id}, Slide Name: {slide.slide_name}")
	else:
		print(f"No slides associated with {device_name_to_query}")
else:
	print(f"No device found with the name {device_name_to_query}")

# Close the session
session.close()
# Close the session and engine
session.close()
engine.dispose()
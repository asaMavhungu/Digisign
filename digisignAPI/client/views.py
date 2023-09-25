from flask import Blueprint, render_template, request, flash, send_file, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)



@views.route('/docs', methods=['GET'])
def docs():
	return send_file("client/ApiSpecs/redoc-static.html")


@views.route('/', methods=['GET'])
def home():
	# Assuming 'image.jpg' is the name of your file in the 'uploads' directory
	return send_file("client/html/home.html")

@views.route('/signin', methods=['GET'])
def signin():
	return send_file("client/html/login.html")

@views.route('/devices', methods=['GET'])
def devices():
	return send_file("client/html/all-devices.html")

@views.route('/departments', methods=['GET'])
def departments_all():
	return send_file("client/html/all-departments.html")

@views.route('/department/', methods=['GET'])
def department():
	return send_file("client/html/department-devices.html")

@views.route('/slides/', methods=['GET'])
def device_slides():
	return send_file("client/html/device-slides.html")

@views.route('/device-slide-test/', methods=['GET'])
def device_slides_test():
	return send_file("client/html/device-slide-testview.html")

@views.route('/watch/', methods=['GET'])
def device_watch():
	return send_file("client/html/device-slide-watch.html")


@views.route('/signup', methods=['GET'])
def test():
	return send_file("client/html/signup.html")

@views.route('/slides', methods=['GET'])
def slides():
	return send_file("client/html/all-slides.html")

@views.route('/login', methods=['GET'])
def login():
	return send_file("client/html/login.html")



@views.route('/deps_num', methods=['GET'])
def departments():
	return send_file("client/html/department.html")



@views.route('/deps/addDep', methods=['GET'])
def add_department():
	return send_file("client/html/add_department.html")

@views.route('/uploadPage', methods=['GET'])
def upload():
	return send_file("client/html/uploadpage.html")


@views.route('/uploads/<filename>')
def serve_image(filename: str):
	print(filename)
	filename = filename.replace(" ", "_")
	return send_from_directory('uploads', filename)

@views.route('statics/<filename>')
def serve_static(filename):
	return send_from_directory("client/statics", filename)

@views.route('/upload', methods=['POST'])
def upload_file():
	uploaded_file = request.files['file']

	if uploaded_file.filename != '':
		# Get the directory of this views.py file
		current_directory = os.path.dirname(__file__)

		# Navigate to the directory containing main.py
		parent_directory = os.path.dirname(current_directory)

		# Specify the relative path to the "uploads" directory
		file_directory = os.path.join(parent_directory, 'uploads')

		# Create the "uploads" directory if it doesn't exist
		if not os.path.exists(file_directory):
			os.makedirs(file_directory)

		# Build the absolute path for the uploaded file
		file_path_relative = os.path.join('uploads', secure_filename(uploaded_file.filename))
		file_path_absolute = os.path.abspath(os.path.join(file_directory, secure_filename(uploaded_file.filename)))

		print("Absolute path:", file_path_absolute)

		# Save the uploaded file
		uploaded_file.save(file_path_absolute)

		# Do any additional processing you need here

		return jsonify({"message": "File uploaded successfully"})
	else:
		return jsonify({"message": "File uploaded successfully"})
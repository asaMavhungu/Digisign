from flask import Blueprint, render_template, request, flash, send_file

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
	return send_file("client/ApiSpecs/redoc-static.html")


@views.route('/devices', methods=['GET'])
def devices():
	return send_file("client/html/ten.html")

@views.route('/signup', methods=['GET'])
def test():
	return send_file("client/html/signup.html")

@views.route('/slides', methods=['GET'])
def slides():
	return send_file("client/html/slides.html")

@views.route('/login', methods=['GET'])
def login():
	return send_file("client/html/login.html")

@views.route('/signin', methods=['GET'])
def signin():
	return send_file("client/html/signin.html")

@views.route('/deps', methods=['GET'])
def departments():
	return send_file("client/html/department.html")

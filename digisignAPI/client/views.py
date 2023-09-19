from flask import Blueprint, render_template, request, flash, send_file

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
	return send_file("client/ApiSpecs/redoc-static.html")


@views.route('/devices', methods=['GET'])
def devices():
	return send_file("client/html/ten.html")

@views.route('/test', methods=['GET'])
def test():
	return send_file("client/html/carousel.html")

@views.route('/slides', methods=['GET'])
def slides():
	return send_file("client/html/slides.html")

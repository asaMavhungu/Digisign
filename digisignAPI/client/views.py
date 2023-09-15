from flask import Blueprint, render_template, request, flash, send_file

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
	return send_file("client/html/asa.html")

@views.route('/devices', methods=['GET'])
def devices():
	return send_file("client/html/ten.html")

@views.route('/test', methods=['GET'])
def test():
	return send_file("client/html/carousel.html")
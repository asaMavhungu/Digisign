from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Slide, VideoSlide
from . import db
import json

views = Blueprint('views', __name__)

def get_time_interval(slide):
	# Present the slide for the calculated time interval
	if isinstance(slide, VideoSlide):
		time_interval = calculate_video_length(slide.video_url)
	else:
		time_interval = slide.time_interval

def calculate_video_length(video_url):
	#TODO add logic to get video length from url
	return 120 


@views.route('/')
def home():
	return render_template("home.html", user=current_user)

@views.route('/slides', methods=['GET', 'POST'])
@login_required
def slides():
	if request.method == 'POST':
		slide = request.form.get('slide')

		if len(slide) < 1: # type: ignore
			flash('Slide is too short', category='error')
		else:
			new_slide = Slide(data=slide, user_id=current_user.id) # type: ignore
			db.session.add(new_slide)
			db.session.commit()
			flash('Slide added', category='success')
	return render_template("slideshow.html", user=current_user)

@views.route('/slides', methods=['GET', 'POST'])
@login_required
def edit_slide():
	#TODO Add functionality to edit slides
	return 'Edit page'

@views.route('/delete-slide', methods=['POST'])
@login_required
def delete_slide():
	slide_id = request.form.get('id')  # Get the value of the 'id' field from the form data
	
	if slide_id is None:
		return 'No slide ID provided'

	slide = Slide.query.get_or_404(slide_id)

	try:
		db.session.delete(slide)
		db.session.commit()
		return redirect(url_for('views.home'))
	except:
		return 'There was a problem deleting the slide'
	

@views.route('/weather', methods=['GET', 'POST'])
def weather():
	 
	return render_template("weather.html", user = current_user)

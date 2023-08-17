from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Slide
from . import db
import json

views = Blueprint('views', __name__)


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

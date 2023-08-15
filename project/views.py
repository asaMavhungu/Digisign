from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Slide
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/')
@login_required
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
def delete_slide():
	slide = json.loads(request.data)
	slideId = slide['slideId']
	slide = Slide.query.get(slideId)
	if slide:
		if slide.user_id == current_user.id: #if the deleter is the owner # type: ignore
			db.session.delete(slide)
			db.session.commit()
	
	return jsonify({})
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from typing import Optional

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		user = User.query.filter_by(email=email).first()

		if user:
			if check_password_hash(user.password, password): # type: ignore
				flash('Logged in successfully', category='success')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Incorrect password, try again', category='error')
		else:
			flash('Email does not exist.', category='error')


	data = request.form
	print(data)
	return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		email: Optional[str] = request.form.get('email')
		firstName: Optional[str] = request.form.get('firstName')
		password1: Optional[str] = request.form.get('password1')
		password2: Optional[str] = request.form.get('password2')

		user = User.query.filter_by(email=email).first()

		if user:
			flash('Email already exists', category='error')
		elif len(email) < 4: # type: ignore
			flash("Email must be greater than 3 characters", category='error')
		elif len(firstName) < 2: # type: ignore
			flash("Firstname must be greater than 2 characters", category='error')
		elif password1 != password2: # type: ignore
			flash("Passwords don\'t match", category='error')
		elif len(password1) < 7: # type: ignore
			flash("Password must be greater than 6 characters", category='error')
		else:
			new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256')) # type: ignore
			db.session.add(new_user)
			db.session.commit()
			flash("Account created", category='success')
			login_user(new_user, remember=True)
			return redirect(url_for('views.home'))

	data = request.form
	print(data)
	return render_template("sign_up.html", user=current_user)
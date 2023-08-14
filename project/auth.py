from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	data = request.form
	print(data)
	return render_template("login.html")

@auth.route('/logout')
def logout():
	return "<h1>logged out</h1>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		email: Optional[str] = request.form.get('email')
		firstName: Optional[str] = request.form.get('firstName')
		password1: Optional[str] = request.form.get('password1')
		password2: Optional[str] = request.form.get('password2')

		if len(email) < 4: # type: ignore
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
			return redirect(url_for('views.home'))

	data = request.form
	print(data)
	return render_template("sign_up.html")
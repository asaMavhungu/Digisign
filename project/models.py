from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Slide(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	data = db.Column(db.String(150))
	slideType = db.Column(db.String(50))
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key relationship
	time_interval = db.Column(db.Integer, default=8)
	valid_media = db.Column(db.Boolean, default=False)

class VideoSlide(Slide):
	video_url = db.Column(db.String(150))

class ImageSlide(Slide):
	caption = db.Column(db.String(150))
	image_url = db.Column(db.String(150))

class WebpageSlide(Slide):
	webpage_url = db.Column(db.String(150))

class NewsFeedSlide(Slide):
	newsfeed_url = db.Column(db.String(150))
	
class WeatherSlide(Slide):
	location = db.Column(db.String(150))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	firstName = db.Column(db.String(150))
	slides = db.relationship('Slide')

department_admins = db.Table('department_admins',
    db.Column('department_id', db.Integer, db.ForeignKey('department.id'), primary_key=True),
    db.Column('admin_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    admins = db.relationship('User', secondary=department_admins, backref='departments')

class Admin(User):
	admin_permission = db.Column(db.Boolean, default=False)

class Device(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150))
	location = db.Column(db.String(150))
	status = db.Column(db.String(50), default='Active')
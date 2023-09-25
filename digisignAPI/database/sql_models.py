from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Department(Base):
	__tablename__ = 'departments'

	department_id = Column(Integer, primary_key=True)
	department_name = Column(String, unique=True)
	slides = relationship("Slide", back_populates="department")
	shared_slides = relationship("SharedSlide", 
								 primaryjoin="Department.department_id == SharedSlide.from_department_id",
								 back_populates="from_department")

	devices = relationship("Device", back_populates="department")

class User(Base):
	__tablename__ = 'users'

	user_id = Column(Integer, primary_key=True)
	username = Column(String, unique=True)
	email = Column(String)
	password = Column(String)  

class Slide(Base):
	__tablename__ = 'slides'

	slide_id = Column(Integer, primary_key=True)
	slide_name = Column(String, unique=True)
	slide_url = Column(String)
	slide_duration = Column(Integer)
	department_id = Column(Integer, ForeignKey('departments.department_id'))
	current_user_id = Column(Integer, ForeignKey('users.user_id')) 
	department = relationship("Department", back_populates="slides")
	assignments = relationship("SlideAssignment", back_populates="slide")
	current_user = relationship("User")  # Relationship to the user who owns the slide

class Device(Base):
	__tablename__ = 'devices'

	device_id = Column(Integer, primary_key=True)
	device_name = Column(String, unique=True)
	department_id = Column(Integer, ForeignKey('departments.department_id'))  
	assignments = relationship("SlideAssignment", back_populates="device")
	department = relationship("Department", back_populates="devices") 

class SlideAssignment(Base):
	__tablename__ = 'slide_assignment'

	assignment_id = Column(Integer, primary_key=True)
	slide_id = Column(Integer, ForeignKey('slides.slide_id'))
	device_id = Column(Integer, ForeignKey('devices.device_id'))
	slide = relationship("Slide", back_populates="assignments")
	device = relationship("Device", back_populates="assignments")

class SharedSlide(Base):
	__tablename__ = 'shared_slides'

	sharing_id = Column(Integer, primary_key=True)
	from_department_id = Column(Integer, ForeignKey('departments.department_id'))
	to_department_id = Column(Integer, ForeignKey('departments.department_id'))
	slide_id = Column(Integer, ForeignKey('slides.slide_id'))
	from_department = relationship("Department", foreign_keys=[from_department_id], back_populates="shared_slides")
	to_department = relationship("Department", foreign_keys=[to_department_id])
	slide = relationship("Slide")

class UserSlide(Base):
	__tablename__ = 'user_slides'

	user_slide_id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.user_id'))
	slide_id = Column(Integer, ForeignKey('slides.slide_id'))
	# Add timestamps for slide creation and last edit
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	last_edited_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
	user = relationship("User")
	slide = relationship("Slide")

# Create the SQLite database and tables
engine = create_engine('sqlite:///my_database.db') 
Base.metadata.create_all(engine)

# Close the connection
engine.dispose()
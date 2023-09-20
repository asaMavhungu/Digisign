from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from .Slide import Slide
from .ImageSlide import ImageSlide

class SlideFactory:

	def __init__(self):
		pass
	
	def create_slide(self, slide_dict: dict):

		if slide_dict['type'] == 'generic':
			return Slide.from_dict(slide_dict)
		elif slide_dict['type'] == 'image':
			return ImageSlide.from_dict(slide_dict)
		
		# TODO FIX HERE, JUST TO REMOVE THE 'NONE' ERRORS
		return Slide.from_dict(slide_dict)
		return None
		


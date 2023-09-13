from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from .Slide import Slide
from .ImageSlide import ImageSlide

class SlideFactory:
	@classmethod
	def create_slide(cls, title, content, content_type, author_id, image_url=None, video_url=None):
		"""
		Create a slide instance based on content_type.

		:param title: The title of the slide.
		:param content: The content of the slide.
		:param content_type: The type of content ('image', 'video', or other).
		:param author_id: The unique identifier of the author (user) of the slide.
		:param image_url: The URL of the image (optional, used for image slides).
		:param video_url: The URL of the video (optional, used for video slides).
		:return: An instance of the appropriate slide class.
		"""
		if content_type == 'image':
			return ImageSlide(title, content, author_id, image_url)
		return None
		
	@classmethod
	def slide_from_dict(cls, slide_dict):
		"""
		Create a slide instance from a dictionary.

		:param slide_dict: A dictionary containing slide data.
		:return: An instance of the appropriate slide class.
		"""
		if not slide_dict:
			return None
		content_type = slide_dict.get('content_type', 'generic')
		if content_type == 'image':
			return ImageSlide.from_dict(slide_dict)
		return None
		


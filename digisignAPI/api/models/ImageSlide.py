from .Slide import Slide
from bson.objectid import ObjectId
	
class ImageSlide(Slide):
	def __init__(self, title, content, author_id, image_url):
		"""
		Constructor for the ImageSlide class.

		:param title: The title of the image slide.
		:param content: The content of the image slide.
		:param author_id: The unique identifier of the author (user) of the image slide.
		:param image_url: The URL of the image.
		"""
		super().__init__(title, content, "image", author_id)  # Call the constructor of the base class
		self.image_url = image_url

	def to_dict(self):
		"""
		Converts the ImageSlide instance to a dictionary.

		:return: A dictionary representation of the image slide instance.
		"""
		slide_dict = super().to_dict()  # Call the base class method to get the common slide properties
		slide_dict['image_url'] = self.image_url
		return slide_dict
	
	@classmethod
	def from_dict(cls, slide_dict):
		slide = cls(
			title=slide_dict['title'],
			content=slide_dict['content'],
			author_id=slide_dict['author_id'],
			image_url=slide_dict['image_url']
		)
		slide.content_type = 'image'
		slide._id = slide_dict.get('_id')  # Optional ObjectId
		slide.departments = slide_dict.get('departments', [])
		return slide
	
	@staticmethod
	def find_by_id(slide_id, mongo):
		"""
		Finds a slide by its unique slide ID (ObjectId) in the database.

		:param slide_id: The unique identifier of the slide.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Slide class or None if not found.
		"""
		slide_data = mongo.db.slides.find_one({'_id': ObjectId(slide_id)})
		if slide_data:
			return ImageSlide.from_dict(slide_data)
		return None
	
	@staticmethod
	def find_by_title(title, mongo):
		"""
		Finds slides by their title in the database.

		:param title: The title of the slide to search for.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: A list of instances of the Slide class matching the title or an empty list if not found.
		"""
		slide_data = mongo.db.slides.find_one({'title': title})
		if slide_data:
			return ImageSlide.from_dict(slide_data)
		return None
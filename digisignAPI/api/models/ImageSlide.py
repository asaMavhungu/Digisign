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
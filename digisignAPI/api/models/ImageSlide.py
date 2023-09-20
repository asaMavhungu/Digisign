from .Slide import Slide
	
class ImageSlide(Slide):

	def __init__(self, title: str, author_id: str, departments: list, image_url: str):
		"""
		Constructor for the ImageSlide class.

		:param title: The title of the image slide.
		:param content: The content of the image slide.
		:param author_id: The unique identifier of the author (user) of the image slide.
		:param image_url: The URL of the image.
		"""
		super().__init__(title, author_id, departments) 
		self.slide_type = 'image'
		self.image_url = image_url

	def to_dict(self):
		"""
		Converts the ImageSlide instance to a dictionary.

		:return: A dictionary representation of the image slide instance.
		"""
		slide_dict = super().to_dict()  
		slide_dict['image_url'] = self.image_url
		return slide_dict
	
	@classmethod
	def from_dict(cls, slide_dict):
		slide = cls(
			title=slide_dict['title'],
			author_id=slide_dict['author_id'],
			image_url=slide_dict['image_url'],
			departments = slide_dict.get('departments', [])
		)

		slide._id = slide_dict.get('_id')  # Optional ObjectId

		return slide
	
	def add_image_url(self, url: str):
		self.image_url = url
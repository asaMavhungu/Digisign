from models.Slide import Slide
	
class VideoSlide(Slide):
	def __init__(self, title, content, author_id, video_url):
		"""
		Constructor for the VideoSlide class.

		:param title: The title of the video slide.
		:param content: The content of the video slide.
		:param author_id: The unique identifier of the author (user) of the video slide.
		:param video_url: The URL of the video.
		"""
		super().__init__(title, content, "video", author_id)  # Call the constructor of the base class
		self.video_url = video_url

	def to_dict(self):
		"""
		Converts the VideoSlide instance to a dictionary.

		:return: A dictionary representation of the video slide instance.
		"""
		slide_dict = super().to_dict()  # Call the base class method to get the common slide properties
		slide_dict['image_url'] = self.video_url
		return slide_dict
	
	@classmethod
	def from_dict(cls, slide_dict):
		slide = cls(
			title=slide_dict['title'],
			content=slide_dict['content'],
			author_id=slide_dict['author_id'],
			video_url=slide_dict['video_url']
		)
		slide.content_type = 'video'
		slide._id = slide_dict.get('_id')  # Optional ObjectId
		slide.departments = slide_dict.get('departments', [])
		return slide
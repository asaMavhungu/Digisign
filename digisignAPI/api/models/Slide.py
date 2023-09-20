from bson.objectid import ObjectId
import database.Database_utils as db_client


class Slide:
	def __init__(self, title: str, author_id: str, departments: list):
		"""
		Constructor for the Slide class.

		:param title: The title of the slide.
		:param content: The content of the slide.
		:param author_id: The unique identifier of the author (user) of the slide.
		"""
		self._id = None 
		self.title = title
		self.slide_type = "generic"
		self.author_id = author_id
		self.departments = departments

	def add_department(self, department_name):
		"""
		Add a department ObjectId to the slide's list of associated departments.

		:param department_id: The ObjectId of the department to be associated with the slide.
		"""
		if department_name not in self.departments:
			self.departments.append(department_name)

	def remove_department(self, department_name):
		"""
		Remove a department ObjectId from the slide's list of associated departments.

		:param department_id: The ObjectId of the department to be disassociated from the slide.
		"""
		if department_name in self.departments:
			self.departments.remove(department_name)

	def clear_departments(self):
		self.departments = []

	@classmethod
	def from_dict(cls, slide_dict):
		"""
		Creates a Slide instance from a dictionary.

		:param slide_dict: A dictionary containing slide data.
		:return: An instance of the Slide or VideoSlide class, depending on content_type.
		"""
		slide = cls(
			title=slide_dict['title'],
			author_id=slide_dict['author_id'],
			departments = slide_dict.get('departments', [])
		)
		slide._id = slide_dict.get('_id')  # Optional ObjectId
		return slide

	def to_dict(self):
		"""
		Converts the Slide instance to a dictionary.

		:return: A dictionary representation of the slide instance.
		"""
		slide_dict = {
			'title': self.title,
			'slide_type': self.slide_type,
			'author_id': self.author_id,
			'departments': self.departments,
		}
		return slide_dict

	def to_marshal_representation(self) -> dict[str, str | list[str] | None]:
		"""
		Convert the Slide object to a marshal-like representation.
		"""
		return {
			'_id': self._id,
			'title': self.title,
			'slide_type': self.slide_type,
			'author_id': self.author_id,
			'departments': self.departments,
		}

	@staticmethod
	def find_by_title(title: str) -> (dict | None):
		print("==========================")
		# TODO Remove redundancy of creating Slide object
		# TODO Bring back redundancy
		"""
		Finds slides by their title in the database.

		:param title: The title of the slide to search for.
		:param client: An instance of SlideClient used for database operations.
		:return: slide dict
		"""
		return db_client.get_one('slides', 'title', title) # type: ignore

	def save(self):
		"""
		Saves the slide instance to the database.

		:param slides_table: The table to update.
		:return: The unique identifier (_id) of the inserted or updated slide document.
		"""
		slide_data = self.to_dict()
		if self._id:
			return db_client.update_entry('slides', 'title', self.title, slide_data)
		else:
			return db_client.insert_entry('slides', slide_data)
		
	
	@staticmethod
	def getAll():
		"""
		Get all the slides in the db
		"""
		return db_client.get_table('slides')
	
	def delete_me(self):
		db_client.delete_entry('slides', 'title', self.title)

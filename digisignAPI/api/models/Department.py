from bson.objectid import ObjectId

class Department:
	def __init__(self, name):
		"""
		Constructor for the Department class.

		:param name: The name of the department.
		"""
		self._id = None  # MongoDB ObjectId (optional)
		self.name = name
		self.slides = []  # List to store associated slide ObjectIds

	def add_slide(self, slide_id):
		"""
		Add a slide ObjectId to the department's list of associated slides.

		:param slide_id: The ObjectId of the slide to be associated with the department.
		"""
		self.slides.append(slide_id)

	def remove_slide(self, slide_id):
		"""
		Remove a slide ObjectId from the department's list of associated slides.

		:param slide_id: The ObjectId of the slide to be disassociated from the department.
		"""
		if slide_id in self.slides:
			self.slides.remove(slide_id)

	@classmethod
	def from_dict(cls, department_dict):
		"""
		Creates a Department instance from a dictionary.

		:param department_dict: A dictionary containing department data.
		:return: An instance of the Department class.
		"""
		department = cls(department_dict['name'])
		department._id = department_dict.get('_id')  # Optional ObjectId
		department.slides = department_dict.get('slides', [])
		return department

	def to_dict(self):
		"""
		Converts the Department instance to a dictionary.

		:return: A dictionary representation of the department instance.
		"""
		department_dict = {
			'name': self.name,
			'slides': self.slides
		}
		if self._id:
			department_dict['_id'] = self._id
		return department_dict

	@staticmethod
	def find_by_id(department_id, mongo):
		"""
		Finds a department by its unique department ID (ObjectId) in the database.

		:param department_id: The unique identifier of the department.
		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: An instance of the Department class or None if not found.
		"""
		department_data = mongo.db.departments.find_one({'_id': ObjectId(department_id)})
		if department_data:
			return Department.from_dict(department_data)
		return None

	def save(self, mongo):
		"""
		Saves the department instance to the database.

		:param mongo: An instance of Flask-PyMongo used for database operations.
		:return: The unique identifier (_id) of the inserted or updated department document.
		"""
		department_data = self.to_dict()
		if self._id:
			# Update the existing department document
			mongo.db.departments.update_one({'_id': self._id}, {'$set': department_data})
			return self._id
		else:
			# Insert a new department document
			result = mongo.db.departments.insert_one(department_data)
			self._id = result.inserted_id
			return str(result.inserted_id)


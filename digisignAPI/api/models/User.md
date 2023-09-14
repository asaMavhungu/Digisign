# User Class Documentation

The `User` class represents a user entity in your application. It provides methods for creating, retrieving, and saving user data.

## Constructor

### `__init__(self, username, email, password_hash=None)`

- **Parameters:**
  - `username` (str): The username of the user.
  - `email` (str): The email address of the user.
  - `password_hash` (str, optional): The hashed password of the user (default is `None`). You may want to store hashed passwords for security reasons.

## Class Methods

### `from_dict(cls, user_dict)`

- **Parameters:**
  - `user_dict` (dict): A dictionary containing user data.

- **Returns:** An instance of the `User` class created from the provided dictionary.

## Instance Methods

### `to_dict(self)`

- **Returns:** A dictionary representation of the user instance, including `username`, `email`, and `password_hash`.

### `save(self, mongo)`

- **Parameters:**
  - `mongo` (PyMongo): An instance of Flask-PyMongo used for database operations.

- **Description:** Saves the user instance to the database.

- **Returns:** The unique identifier (`_id`) of the inserted user document.

## Static Methods

### `find_by_username(username, mongo)`

- **Parameters:**
  - `username` (str): The username to search for.
  - `mongo` (PyMongo): An instance of Flask-PyMongo used for database operations.

- **Returns:** A user document from the database with the specified username or `None` if not found.

### `find_by_id(user_id, mongo)`

- **Parameters:**
  - `user_id` (str): The unique identifier of the user.
  - `mongo` (PyMongo): An instance of Flask-PyMongo used for database operations.

- **Returns:** A user document from the database with the specified user ID (ObjectId) or `None` if not found.

## Usage

You can use the `User` class to create, retrieve, and save user data in your application. It includes methods for converting user data to and from dictionaries and for interacting with a MongoDB database using Flask-PyMongo.

Make sure to adapt this documentation to your specific use case and include it in your project's documentation for reference. Additionally, consider adding error handling and validation to the class methods to ensure data integrity and security in your application.

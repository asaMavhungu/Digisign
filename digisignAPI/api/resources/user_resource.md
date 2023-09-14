# User Resource API Documentation

This documentation outlines the endpoints and operations available in the User Resource API.

## Create a User (POST)

- **URL:** `/api/user`
- **Method:** `POST`
- **Request Body:**

    ```json
    {
        "username": "user123",
        "email": "user@example.com",
        "password": "password123"
    }
    ```

- **Description:** Creates a new user with the provided username, email, and password. The password is hashed before saving.

- **Response:**
  - `201 Created` if the user is successfully created:

    ```json
    {
        "message": "User created",
        "user_id": "user_id_here"
    }
    ```

  - `400 Bad Request` if the username already exists:

    ```json
    {
        "message": "Username already exists"
    }
    ```

## Get User by ID (GET)

- **URL:** `/api/user/<user_id>`
- **Method:** `GET`
- **URL Parameters:**
  - `user_id` (string) - The unique identifier of the user.

- **Description:** Retrieves user information by their unique user ID.

- **Response:**
  - `200 OK` if the user is found:

    ```json
    {
        "username": "user123",
        "email": "user@example.com",
        "password": "hashed_password_here"
    }
    ```

  - `404 Not Found` if the user with the provided ID does not exist:

    ```json
    {
        "message": "User not found"
    }
    ```

## Request Body

- `username` (string, required): The username of the user.
- `email` (string, required): The email address of the user.
- `password` (string, required): The user's password.

## Notes

- The user's password is hashed before being stored in the database using the Bcrypt library.
- The `UserResource` class is used to define the behavior of the user-related endpoints.
- MongoDB (referred to as `self.mongo`) appears to be used as the database for storing user information.
- This code assumes that you have a `User` class defined in `api.models.User` with methods like `find_by_username`, `find_by_id`, and `save` for handling user-related database operations.

Please make sure to adapt this documentation to your specific use case and add any additional details as needed. Additionally, consider adding error handling and validation for your API endpoints to enhance its robustness.

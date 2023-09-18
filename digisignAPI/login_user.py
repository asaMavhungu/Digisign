import requests

def test_user_login(api_url, username, password):
    """
    Test user login API.

    Args:
        api_url (str): The URL of the user login API endpoint.
        username (str): The username to use for login.
        password (str): The password to use for login.

    Returns:
        dict: The JSON response from the API.
    """
    try:
        data = {
            'username': username,
            'password': password
        }

        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Login failed with status code {response.status_code}:")
            print(response.text)
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Define the API endpoint URL for user login
    api_url = 'http://localhost:5000/api/login'  # Replace with your API endpoint

    # Test user login with valid credentials
    login_response = test_user_login(api_url, 'new_user', 'password123')
    print("Login Response:", login_response)

    # Test user login with invalid credentials
    invalid_login_response = test_user_login(api_url, 'invalid_username', 'invalid_password')
    print("Invalid Login Response:", invalid_login_response)

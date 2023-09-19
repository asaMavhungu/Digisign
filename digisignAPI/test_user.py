import requests

def test_api(method, api_url, data=None, access_token=None):
    """
    Test an API endpoint using the specified HTTP method with an access token.

    Args:
        method (str): The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE').
        api_url (str): The URL of the API endpoint.
        data (dict): The data to send in the request body for POST or PUT requests.
        access_token (str): The JWT access token.

    Returns:
        dict: The JSON response from the API.
    """
    try:
        headers = {}
        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'

        if method == 'GET':
            response = requests.get(api_url, headers=headers)
        elif method == 'POST':
            response = requests.post(api_url, json=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(api_url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(api_url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            print(f"API request failed with status code {response.status_code}:")
            print(response.text)
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    


# Example usage:
if __name__ == "__main__":
    # Define the API endpoint URL
    api_url = 'http://localhost:5000/api/users'  # Replace with your API endpoint

    # Replace 'your_access_token' with the actual access token obtained during login
    access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NTExNDQxNiwianRpIjoiZjk1OTgyNGUtNTIzNy00NDQ4LThlYTAtYzljMjJkYzA3OTAxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im5ld191c2VyIiwibmJmIjoxNjk1MTE0NDE2LCJleHAiOjE2OTUxMTUzMTZ9.AQJl5mHXfX8L63toF1z-N6s4D0u4RF0zQlh9NTU2EjI'
    # Test a GET request with the access token
    get_response = test_api('GET', api_url, access_token=access_token)
    print("GET Response:", get_response)

    # Test a POST request with data and the access token
    post_data = {
        'username': 'asa',
        'password': 'asa',
        'email': 'asa@example.com',
        'verified': True
    }

    post_response = test_api('POST', api_url, data=post_data, access_token=access_token)
    print("POST Response:", post_response)

    # Test a PUT request with data and the access token
    put_data = {
        'username': 'updated_user',
        'password': 'new_password123',
        'email': 'updated_user@example.com',
        'verified': True
    }
    put_response = test_api('PUT', api_url, data=put_data, access_token=access_token)
    print("PUT Response:", put_response)
'''
    # Test a DELETE request with the access token
    #delete_response = test_api('DELETE', api_url, access_token=access_token)
    #print("DELETE Response:", delete_response)
'''
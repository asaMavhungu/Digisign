import requests
import json




def postRequest(endpoint, json_data):
	# Set the headers to indicate that you're sending JSON data
	headers = {
		"Content-Type": "application/json"
	}


	# Send a POST request with JSON data in the request body
	response = requests.post(base_url + endpoint, data=json.dumps(json_data), headers=headers)

	# Check the response status code
	if response.status_code == 200:
		# If the status code is 200, the request was successful
		print("Request was successful")
		# Print the response content as-is
		print("Response content:")
		print(response.text)
	else:
		# If the status code is not 200, there was an error
		print(f"Request failed with status code {response.status_code}")
		# You can print the error message if available
		print("Error message:", response.text)

def deleteRequest(endpoint):
	# Set the headers to indicate that you're sending JSON data
	headers = {
		"Content-Type": "application/json"
	}


	# Send a POST request with JSON data in the request body
	response = requests.delete(base_url + endpoint)

	# Check the response status code
	if response.status_code == 200:
		# If the status code is 200, the request was successful
		print("Request was successful")
		# Print the response content as-is
		print("Response content:")
		print(response.text)
	else:
		# If the status code is not 200, there was an error
		print(f"Request failed with status code {response.status_code}")
		# You can print the error message if available
		print("Error message:", response.text)

def getRequest(endpoint):
	# Set the headers to indicate that you're sending JSON data
	headers = {
		"Content-Type": "application/json"
	}


	# Send a POST request with JSON data in the request body
	response = requests.get(base_url + endpoint)

	# Check the response status code
	if response.status_code == 200:
		# If the status code is 200, the request was successful
		print("Request was successful")
		# Print the response content as-is
		print("Response content:")
		print(response.text)
	else:
		# If the status code is not 200, there was an error
		print(f"Request failed with status code {response.status_code}")
		# You can print the error message if available
		print("Error message:", response.text)


# Define the base URL of your Flask API
base_url = 'http://127.0.0.1:5000'

# Define the endpoint you want to test for the POST request
endpoint = '/api/slides'

# Define the JSON data you want to send in the request body
json_data = {
  "title": "ASASAS",
  "content": "Pic of luffy",
  "content_type": "image",
	"image_url":  "https://rare-gallery.com/thumbnail/1375167-luffy-sun-god-nika-gear-5-one-piece-4k-pc-wallpaper.jpg",
  "author_id": "asa",
  "departments": []
}

postRequest(endpoint, json_data)
getRequest(endpoint)
deleteRequest('/api/slides/ASASAS')
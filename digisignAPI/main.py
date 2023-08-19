
# main.py
from api.resources.user_resource import UserResource
from api import app, mongo

if __name__ == "__main__":
	app.run(debug=True)
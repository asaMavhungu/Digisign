from client import createApp
from database import createMongoDatabase
from api import createApi

if __name__ == "__main__":

	app, DB_CLIENT = createApi(__name__)

	#app = createApp()

	app.run(debug=True)
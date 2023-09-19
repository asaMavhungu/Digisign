from client import createClient
from database import createMongoDatabase
from api import createApi
from database import createDatabase
from flask import Flask

import argparse



if __name__ == "__main__":

	import json

	with open('db.json', 'r') as file:
		data = json.load(file)

	#app, DB_CLIENT = createApi(__name__)

	# Create an Argument Parser
	parser = argparse.ArgumentParser(description='Example script with a flag that accepts a value.')

	# Add a Flag with a Value
	parser.add_argument('--db', type=str, help='Specify the database type (e.g., mongoDB, tinyDB).')

	# Parse the Command-Line Arguments
	args = parser.parse_args()

	database = 'tinyDB'

	# Access and Use the Flag with a Value
	if args.db:
		print(f"Database type specified: {args.db}")
		if args.db in ['mongoDB', 'tinyDB']:
			database = args.db
			print(f"Using the {database} Database")
		else:
			print("Database chosen not in options ['mongoDB', 'tinyDB']")
	else:
		print("No database type specified. Usind default of tinyDB")

	#app = createApp(database)

	app = Flask(__name__)

	app, db_client = createDatabase(app, database)

	app, db_client = createApi(app, db_client)

	app = createClient(app)

	#print(json.dumps(data, indent=4))

	app.run(debug=True)

# main.py
from api import createApp

if __name__ == "__main__":
	app, mongo = createApp()
	app.run(debug=True)
from flask import Flask, render_template

# Create the Flask application
app : Flask = Flask(__name__)

# Route for the home page
@app.route('/')
def hello() -> str:
	return 'Hello, World!'

@app.route("/home")
def home() -> str:
	return render_template("index.html")

@app.route("/sit")
def computerScience() -> str:
	return render_template("cs.html")


if __name__ == '__main__':
	# Run the application on localhost and port 5000
	app.run(host='0.0.0.0', port=5000)

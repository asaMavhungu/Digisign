from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Route for the home page
@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    # Run the application on localhost and port 5000
    app.run(host='0.0.0.0', port=5000)

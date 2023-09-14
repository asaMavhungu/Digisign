from flask import Flask
from tinydb import TinyDB, Query

app = Flask(__name__)

# Create a TinyDB instance and specify the data file
db = TinyDB('data.json')

users_table = db.table('users')
products_table = db.table('products')


@app.route('/add_user', methods=['POST'])
def add_user():
    user_data = {'name': 'Alice', 'age': 25}
    users_table.insert(user_data)
    return 'User added successfully'

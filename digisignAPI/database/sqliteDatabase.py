from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)

# Define a base class for all your table classes
class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Define your table classes
class Entry1(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)

class Entry2(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)

# Create the database tables
db.create_all()

# General API Routes
@app.route('/create_entry/<table_name>', methods=['POST'])
def create_entry(table_name):
    data = request.get_json()
    if table_name == 'entry1':
        entry = Entry1(**data)
    elif table_name == 'entry2':
        entry = Entry2(**data)
    else:
        return jsonify({'message': 'Table not found'}), 404
    
    entry.save()
    return jsonify({'message': 'Entry created successfully'}), 201

@app.route('/get_entries/<table_name>', methods=['GET'])
def get_entries(table_name):
    if table_name == 'entry1':
        entries = Entry1.query.all()
    elif table_name == 'entry2':
        entries = Entry2.query.all()
    else:
        return jsonify({'message': 'Table not found'}), 404
    
    entry_list = [{'id': entry.id, **entry.__dict__} for entry in entries]
    return jsonify(entry_list)

@app.route('/update_entry/<table_name>/<int:id>', methods=['PUT'])
def update_entry(table_name, id):
    data = request.get_json()
    
    if table_name == 'entry1':
        entry = Entry1.query.get(id)
    elif table_name == 'entry2':
        entry = Entry2.query.get(id)
    else:
        return jsonify({'message': 'Table not found'}), 404
    
    if not entry:
        return jsonify({'message': 'Entry not found'}), 404

    entry.update(**data)
    return jsonify({'message': 'Entry updated successfully'})

@app.route('/delete_entry/<table_name>/<int:id>', methods=['DELETE'])
def delete_entry(table_name, id):
    if table_name == 'entry1':
        entry = Entry1.query.get(id)
    elif table_name == 'entry2':
        entry = Entry2.query.get(id)
    else:
        return jsonify({'message': 'Table not found'}), 404
    
    if not entry:
        return jsonify({'message': 'Entry not found'}), 404

    entry.delete()
    return jsonify({'message': 'Entry deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

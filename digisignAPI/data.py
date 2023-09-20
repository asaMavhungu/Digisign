import json

with open('db.json', 'r') as file:
	data = json.load(file)

print(json.dumps(data, indent=4))
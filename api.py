from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['scrapper']
collection = db['commissioners']


# Define route to retrieve commissioner data
@app.route('/commissioners', methods=['GET'])
def get_commissioners():
    commissioners = []
    for commissioner in collection.find():
        commissioners.append({
            'name': commissioner['name'],
            'role': commissioner['role'],
            'company': commissioner['company'],
            'address': commissioner['address'],
            'address2': commissioner['address2'],
            'myTeamsLink': commissioner['myTeamsLink'],
            'team': commissioner['team']
        })
    return jsonify(commissioners)


if __name__ == '__main__':
    app.run(debug=True)

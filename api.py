from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['scrapper']
collection = db['commissioners']
organizationsCollection = db['organizations']
rolesCollection = db['roles']


# Define route to retrieve commissioner data
@app.route('/commissioners', methods=['GET'])
def get_commissioners():
    commissioners = []
    for commissioner in collection.find():
        commissioners.append({
            'name': commissioner['name'],
            'role': commissioner['role'],
            'organization': commissioner['organization'],
            'image': commissioner['image'],
            'profileLink': commissioner['profileLink'],
            'address': commissioner['address'],
            'address2': commissioner['address2'],
            'myTeamsLink': commissioner['myTeamsLink'],
            'team': commissioner['team']
        })
    return jsonify(commissioners)


@app.route('/roles', methods=['GET'])
def get_roles():
    roles = []
    for role in rolesCollection.find():
        print(role)
        roles.append({
            'name': role['name']
        })
    print(roles)
    return jsonify(roles)


@app.route('/organizations', methods=['GET'])
def get_organztions():
    organizations = []
    for organization in organizationsCollection.find():
        organizations.append({
            'name': organization['name']
        })
    return jsonify(organizations)


if __name__ == '__main__':
    app.run(debug=True)

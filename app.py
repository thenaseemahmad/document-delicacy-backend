from dotenv import dotenv_values, load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
import os
load_dotenv()


app = Flask(__name__)
CORS(app)

#Register a user with username and password
@app.route("/registeruser",methods=['POST'])
def registeruser():
    # new user detail that needs to saved in db
    print(request)
    user = {
        "_id": uuid.uuid4().hex,
        "fullname": request.args.get("fullname"),
        "email": request.args.get("newuseremail"),
        "password": request.args.get("newuserpass")
    }
    #mongodb atlas instance
    mongodb_username = quote_plus(os.getenv('MONDODBUSER'))
    mongodb_password = quote_plus(os.getenv('MONGODBPASS'))
    mongo_altas_uri = "mongodb+srv://" + mongodb_username + ":" + mongodb_password + "@cluster0.c9xlloe.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongo_altas_uri)
    db = client['userDB']
    if (db['users'].find_one({"email":user["email"]})):
        return jsonify({"error":"a user with the same email already exist"})
    db['users'].insert_one(user)
    return jsonify(user), 200

#User login
@app.route("/home",methods=['POST'])
def hello_post():
    # journals = db["users"]
    # registered_user_id = journals.insert_one(this_user).inserted_id
    # this is how to access params variables
    # name = request.args.get('name')
    # age = request.args.get('age')
    # this is how to access headers variables in flask
    # cred = request.headers.get('Authorization')
    # content_type = request.headers.get('Content-type')
    # getting application/json type of body variable
    # data = request.json
    # print(data['joke'])
    # print(alljournals)
    #this is how to access params variables
    name = request.args.get('name')
    age = request.args.get('age')
    #this is how to access headers variables in flask
    cred = request.headers.get('Authorization')
    content_type = request.headers.get('Content-type')
    data = request.json
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
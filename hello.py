from dotenv import dotenv_values
from flask import Flask, request
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
config = dotenv_values(".env")

app = Flask(__name__)

@app.route("/home",methods=['GET'])
def hello_world():
    username = quote_plus('thenaseemahmad')
    password = quote_plus('etnNQFNmLfLhNECS')
    altasuri = "mongodb+srv://"+username+":"+password+"@cluster0.c9xlloe.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(altasuri)
    db = client["journalDB"]
    journals = db["journals"]
    #alljournals = journals.find_one()
    for jour in journals.find():
        print(jour)
    #this is how to access params variables
    #name = request.args.get('name')
    #age = request.args.get('age')
    #this is how to access headers variables in flask
    #cred = request.headers.get('Authorization')
    #content_type = request.headers.get('Content-type')
    #getting application/json type of body variable
    #data = request.json
    #print(data['joke'])
    #print(alljournals)
    return 'alljournals'

@app.route("/home",methods=['POST'])
def hello_post():
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
from dotenv import dotenv_values, load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
import os
from datetime import datetime
from user import users
load_dotenv()


app = Flask(__name__)
CORS(app)
mongodb_username = quote_plus(os.getenv('MONGODBUSER'))
mongodb_password = quote_plus(os.getenv('MONGODBPASS'))
mongodb = quote_plus(os.getenv('MONGODB'))
mongo_altas_uri = "mongodb+srv://" + mongodb_username + ":" + mongodb_password + "@cluster0.c9xlloe.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_altas_uri)
db = client[mongodb]

#Register a user with username and password
@app.route("/registeruser",methods=['POST'])
def registeruser():
    # new user detail that needs to saved in db
    print(request)
    #this can be replaced by user class file as well
    user = {
         "_id": uuid.uuid4().hex,
         "fullname": request.args.get("userfullname"),
         "email": request.args.get("useremail"),
         "password": request.args.get("userpassword"),
         "register_req_timestamp": datetime.now()
     }
    #user = users(uuid.uuid4().hex,request.args.get("fullname"),request.args.get("newuseremail"),request.args.get("newuserpass"),datetime.now())
    #mongodb atlas instance

    if (db['users'].find_one({"email":user['email']})):
        # | operator here is used to merge two python dictionaries together
        return jsonify({"register_status":"failed","register_status_message":"a user with the same email already exist"} | user), 200
    else:
        db['users'].insert_one(user)
        #print(jsonify({"register_status":"success","register_status_message":"user registered successfully"} | user))
        return jsonify({"register_status":"success","register_status_message":"user registered successfully"} | user), 200

#User login route
@app.route("/userlogin",methods=['GET'])
def userlogin():
    useremail=request.args.get('useremail')
    userpassword = request.args.get('userpassword')
    if(db['users'].find_one({"email":useremail})):
        return jsonify({"user_found":True}, 200)
    else:
        return jsonify({"user_found":False}, 200)

#Create a new model route
@app.route("/createmodel",methods=['POST'])
def createmodel():
    model={"_id": uuid.uuid4().hex,
           "created_by":request.args.get('modelcreator'),
           "model_name":request.args.get('modelname'),
           "model_type":request.args.get('modeltype'),
           "created_on":datetime.now(),
           "modified_by":request.args.get('modifiedby')
           }
    if(db['models'].find_one({"model_name":request.args.get('modelname')})):
        #Existing model with the same name found
        return jsonify({"status":False,"status_message":'Existing model with the same name found'} | model)
    else:
        db['models'].insert_one(model);
        return jsonify({"status":False,"status_message":"model created successfully"} | model)

@app.route("/createentity",methods=['POST'])
def createentity():
    entity={
        "_id": uuid.uuid4().hex,
        "model_name":request.args.get('modelname'),
        "entity_name":request.args.get('entityname'),
        "created_on":datetime.now()
    }
    if(db['entities'].find_one({"model_name":entity['model_name'],'entity_name':entity['entity_name']})):
        return jsonify({'status':False,'status_message':'Duplicate entities for a given model is not permissible'})
    else:
        db['entities'].insert_one(entity)
        return jsonify({'status':True,'status_message':'Entity has been created successfully'}|entity)
@app.route("/cratecollection",methods=['POST'])
def createcollection():
    collection={"_id": uuid.uuid4().hex,
                "model_name":request.args.get('modelname'),
                "collection_name":request.args.get('collectionname'),
                "created_on":datetime.now()
                }
    if(db['collections'].find_one({'model_name':collection['model_name'],'collection_name':collection['collection_name']})):
        return jsonify({'status':False,'status_message':'Duplicate collections are not allowed'})
    else:
        db['collections'].insert_one(collection)
        return jsonify({'status':True,'status_message':'Collection created successfully'}|collection)

@app.route('/uploaddocument',methods=['POST'])
def createdocument():
    document={
        "_id": uuid.uuid4().hex,
        "collection_name":request.args.get('collectionname'),
        "document_name":request.args.get('docname'),
        "document_size":request.args.get('docsize'),
        "document_content":request.args.get('doccontent'),
        "created_on":datetime.now()
    }
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
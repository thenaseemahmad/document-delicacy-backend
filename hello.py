from flask import Flask, request

app = Flask(__name__)

@app.route("/home")
def hello_world():
    #this is how to access params variables
    name = request.args.get('name')
    age = request.args.get('age')
    return name+"<p>, World!</p>"+age

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
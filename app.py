from flask import Flask, request, jsonify
from bson.json_util import dumps
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

from pymongo import MongoClient
import json
import os

MONGO_URL = os.environ["MONGOLAB_URI"]
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/sal";


app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)

# client = MongoClient(MONGOLAB_URI)
# db = client["sal"]
# law = db.laws

@app.route('/')
def home():
    return MONGO_URL

@app.route('/search')
def search():
    q = request.args.get('q', '')
    measure_type = request.args.get('type','L')
    x = dumps(mongo.db.command('text', 'laws', search=q))
    return x

if __name__ == '__main__':
    app.run(debug=True)
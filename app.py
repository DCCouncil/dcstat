from flask import Flask, request, jsonify
from bson.json_util import dumps

app = Flask(__name__)

from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client["sal"]
law = db.laws

@app.route('/')
def home():
    return "Hello!"

@app.route('/search')
def search():
    q = request.args.get('q', '')
    measure_type = request.args.get('type','L')
    x = dumps(db.command('text', 'laws', search=q))
    return x

if __name__ == '__main__':
    app.run(debug=True)
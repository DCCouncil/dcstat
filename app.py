from flask import Flask, request, jsonify, render_template
from bson.json_util import dumps
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

from pymongo import MongoClient
import json
import os

MONGO_URL = os.environ.get("MONGOLAB_URI")
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/sal";


app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)

# client = MongoClient(MONGOLAB_URI)
# db = client["sal"]
# law = db.laws

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    measure_type = request.args.get('type','L')
    x = dumps(mongo.db.command('text', 'laws', search=q))
    return x

port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
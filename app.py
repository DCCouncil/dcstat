from flask import Flask, request, jsonify, render_template, redirect
from bson.json_util import dumps
from flask.ext.pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

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
    return render_template('home.html')

@app.route('/browse')
def browse():
    # measures = json.load(open('data/metadata.json','r'))
    # quarters = json.load(open('data/quarters.json','r'))
    # return render_template('browse.html', quarters=quarters, measures=measures)
    return render_template('browsestatic.html')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    results = []
    if q != '':
        results = json.loads(dumps(mongo.db.command('text', 'laws', search=q)['results']))
    return render_template('search.html', results=results)


@app.route('/view/<name>')
def view(name=None):
    m = mongo.db.laws.find_one({"name":name + '.pdf'})
    return render_template('view.html', m=m)

@app.route('/get/<name>')
def get(name=None):
    m = mongo.db.laws.find_one({"name":name + '.pdf'})
    print m
    if m == None:
        return redirect('/')
    return redirect('https://s3.amazonaws.com/dcstat/public/' + m["name"])

@app.route('/api/search/')
def api_search():
    q = request.args.get('q', '')
    measure_type = request.args.get('type','L')
    x = dumps(mongo.db.command('text', 'laws', search=q))
    return x

@app.route('/api/measures/<measure>/')
def api_measure(measure=None):
    # print measure
    measure = measure + '.pdf'
    print measure
    m = dumps(mongo.db.laws.find_one({'name':measure}))
    return m

port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
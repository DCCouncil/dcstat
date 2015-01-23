import os
from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client["sal"]
law = db.laws

files = []
for (dirpath, dirnames, filenames) in os.walk('json'):
    files.extend(filenames)
    break

for f in files:
    with open('json/' + f) as fp:
        law.insert(json.load(fp))
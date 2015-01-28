from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client["sal"]
law = db.laws

db.laws.ensure_index([('text', 'text'), ('title', 'text')], name="search_index");
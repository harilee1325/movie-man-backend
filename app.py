from flask import Flask, request, jsonify
import json as simplejson
import json
from pymongo import MongoClient
from bson.json_util import dumps
import random

client = MongoClient('mongodb://Harilee:harilee1329@haridatabase-shard-00-00-egsq3.mongodb.net:27017,haridatabase-shard-00-01-egsq3.mongodb.net:27017,haridatabase-shard-00-02-egsq3.mongodb.net:27017/test?ssl=true&replicaSet=hariDatabase-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.db


app = Flask(__name__)

# route to clear collections
@app.route("/")
def hello():
    db.user_profile_movie_man.remove()
    return "Welcome to Movie Man!"
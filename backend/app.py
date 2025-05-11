from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["awakenedfit"]
users = db["users"]

@app.route('/api/message')
def message():
    return jsonify({"message": "AwakenedFit Backend Ready!"})

if __name__ == '__main__':
    app.run(debug=True)

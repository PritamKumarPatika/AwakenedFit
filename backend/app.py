from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from routes.progress_routes import progress_bp
# Register routes
from routes.auth_routes import auth_bp

import sys
import os
sys.path.append(os.path.dirname(__file__))


# Load env
load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(progress_bp)

# MongoDB setup
mongo = MongoClient(os.getenv("MONGO_URI"))
db = mongo["awakenedfit"]

# Attach DB to app context
app.config["DB"] = db


app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route('/')
def index():
    return {"status": "AwakenedFit backend running"}



if __name__ == '__main__':
    app.run(debug=True)

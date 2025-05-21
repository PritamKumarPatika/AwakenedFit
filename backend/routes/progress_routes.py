# backend/routes/progress_routes.py

from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from db import db


progress_bp = Blueprint("progress", __name__)

@progress_bp.route("/api/progress/log", methods=["POST"])
def log_user_progress():
    data = request.json
    # Validate incoming data (you can extend this for better validation)
    if not all(key in data for key in ["user_id", "exercise_id", "sets", "reps", "feedback"]):
        return jsonify({"message": "Missing required fields"}), 400
    
    # Insert progress into MongoDB
    result = db.progress.insert_one({
        "user_id": ObjectId(data["user_id"]),
        "exercise_id": ObjectId(data["exercise_id"]),
        "sets": data["sets"],
        "reps": data["reps"],
        "feedback": data["feedback"],
        "date": datetime.utcnow()  # Corrected datetime
    })
    return jsonify({"message": "Progress logged successfully", "id": str(result.inserted_id)}), 200

@progress_bp.route("/api/progress/<user_id>", methods=["GET"])
def get_user_progress(user_id):
    try:
        progress = list(db.progress.find({"user_id": ObjectId(user_id)}))
        for p in progress:
            p["_id"] = str(p["_id"])  # Convert ObjectId to string for JSON serialization
        return jsonify(progress), 200
    except Exception as e:
        return jsonify({"message": "Error fetching progress", "error": str(e)}), 500

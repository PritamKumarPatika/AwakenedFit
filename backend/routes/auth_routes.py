from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
import bcrypt
import re

from utils.jwt_utils import generate_token, decode_token
from models.models import create_user, get_user_by_email

auth_bp = Blueprint("auth", __name__)

def get_authenticated_user(request, db):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    payload = decode_token(token)
    if not payload:
        return None
    return db["users"].find_one({"_id": ObjectId(payload["user_id"])})

# Email and password validation
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_strong_password(password):
    return len(password) >= 6 and any(c.isdigit() for c in password)

# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    db = current_app.config["DB"]

    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email"}), 400

    if not is_strong_password(data["password"]):
        return jsonify({"error": "Weak password"}), 400

    if get_user_by_email(db, data["email"]):
        return jsonify({"error": "Email already registered"}), 409

    hashed_pw = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    user_id = create_user(db, {
        "username": data["username"],
        "email": data["email"],
        "password_hash": hashed_pw,
        "avatar_url": data.get("avatar_url", "")
    })

    token = generate_token(user_id.inserted_id)
    return jsonify({"message": "User registered", "token": token})

# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    db = current_app.config["DB"]

    user = get_user_by_email(db, data["email"])
    if not user or not bcrypt.checkpw(data["password"].encode(), user["password_hash"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user["_id"])
    return jsonify({"message": "Login successful", "token": token})

from bson.objectid import ObjectId
from bson import ObjectId
from datetime import datetime


def get_user_model(db):
    return db["users"]

def get_exercise_model(db):
    return db["exercises"]

def get_progress_model(db):
    return db["progress"]

# Example structure reference
def create_user(db, data):
    users = get_user_model(db)
    return users.insert_one({
        "username": data["username"],
        "email": data["email"],
        "password_hash": data["password_hash"],
        "rank": "E",
        "xp": 0,
        "streaks": 0,
        "avatar_url": data.get("avatar_url", "")
    })

def get_user_by_email(db, email):
    return get_user_model(db).find_one({"email": email})

def log_progress(db, user_id, exercise_id, sets_done, reps_done, feedback):
    return db.progress.insert_one({
        "user_id": ObjectId(user_id),
        "exercise_id": ObjectId(exercise_id),
        "date": datetime.utcnow(),
        "sets": sets_done,
        "reps": reps_done,
        "feedback": feedback
    })

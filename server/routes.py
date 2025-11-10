from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import Camper, Activity, Signup

bp = Blueprint("api", __name__)


def validation_error_response(errors):
    return jsonify({"errors": errors}), 400
    
# --- HOME ROUTE ---
@bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Camping Fun API!"}), 200

# --- CAMPERS ---
@bp.route("/campers", methods=["GET"])
def list_campers():
    campers = Camper.query.all()
    return jsonify([c.to_dict() for c in campers]), 200

@bp.route("/campers/<int:id>", methods=["GET"])
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    return jsonify(camper.to_dict_with_signups()), 200

@bp.route("/campers", methods=["POST"])
def create_camper():
    data = request.get_json() or {}
    name = data.get("name")
    age = data.get("age")

    errors = []
    if not name:
        errors.append("name is required")
    if not isinstance(age, int):
        errors.append("age must be an integer")
    else:
        if age < 8 or age > 18:
            errors.append("age must be between 8 and 18")

    if errors:
        return validation_error_response(errors)

    camper = Camper(name=name, age=age)
    db.session.add(camper)
    db.session.commit()
    return jsonify(camper.to_dict()), 201

@bp.route("/campers/<int:id>", methods=["PATCH"])
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    data = request.get_json() or {}
    errors = []

    if "name" in data:
        name = data.get("name")
        if not name:
            errors.append("name is required")
        else:
            camper.name = name

    if "age" in data:
        age = data.get("age")
        if not isinstance(age, int):
            errors.append("age must be an integer")
        else:
            if age < 8 or age > 18:
                errors.append("age must be between 8 and 18")
            else:
                camper.age = age

    if errors:
        return validation_error_response(errors)

    db.session.commit()
    return jsonify(camper.to_dict()), 202

# --- ACTIVITIES ---
@bp.route("/activities", methods=["GET"])
def list_activities():
    activities = Activity.query.all()
    return jsonify([a.to_dict() for a in activities]), 200

@bp.route("/activities/<int:id>", methods=["DELETE"])
def delete_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404

    db.session.delete(activity)
    db.session.commit()
    # 204 No Content with empty body
    return ("", 204)

# --- SIGNUPS ---
@bp.route("/signups", methods=["POST"])
def create_signup():
    data = request.get_json() or {}
    camper_id = data.get("camper_id")
    activity_id = data.get("activity_id")
    time = data.get("time")

    errors = []

    # Validate presence and types
    camper = None
    activity = None

    if camper_id is None:
        errors.append("camper_id is required")
    else:
        camper = Camper.query.get(camper_id)
        if not camper:
            errors.append("camper must exist")

    if activity_id is None:
        errors.append("activity_id is required")
    else:
        activity = Activity.query.get(activity_id)
        if not activity:
            errors.append("activity must exist")

    if not isinstance(time, int):
        errors.append("time must be an integer")
    else:
        if time < 0 or time > 23:
            errors.append("time must be between 0 and 23")

    if errors:
        return validation_error_response(errors)

    signup = Signup(camper_id=camper_id, activity_id=activity_id, time=time)
    db.session.add(signup)
    db.session.commit()

    # Return signup with nested camper and activity
    # reload to ensure relationships available
    signup = Signup.query.get(signup.id)
    return jsonify(signup.to_dict()), 201

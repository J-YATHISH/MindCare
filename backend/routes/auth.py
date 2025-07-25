from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
#from models.models import db, User, TherapistProfile

auth_bp = Blueprint("auth", __name__)

# -------------------------------
# Register User or Therapist
# -------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # "user" or "therapist"

    if not all([email, password, role]):
        return jsonify({"error": "Missing fields"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    new_user = User(email=email, password=hashed_pw, role=role)
    db.session.add(new_user)
    db.session.commit()

    # If therapist, create an empty profile
    if role == "therapist":
        profile = TherapistProfile(user_id=new_user.id)
        db.session.add(profile)
        db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

# -------------------------------
# Login
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }), 200

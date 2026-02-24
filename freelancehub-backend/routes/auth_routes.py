from flask import Blueprint, request, jsonify
from app import mongo, bcrypt
from utils.jwt_utils import generate_token

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed_pw = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = {
        "email": data["email"],
        "password": hashed_pw,
        "role": data.get("role", "client"),  # freelancer/client/admin
        "status": "active"
    }

    mongo.db.users.insert_one(user)
    return jsonify({"msg": "User created"}), 201


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = mongo.db.users.find_one({"email": data["email"]})

    if not user or not bcrypt.check_password_hash(
        user["password"], data["password"]
    ):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = generate_token(user)
    return jsonify({"token": token})
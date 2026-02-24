from flask import Blueprint, request, jsonify, current_app
from app import mongo, bcrypt
from utils.jwt_utils import generate_token
from bson import ObjectId

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'client')  # freelancer, client, admin

    if not email or not password:
        return jsonify({'msg': 'email and password required'}), 400

    if mongo.db.users.find_one({'email': email}):
        return jsonify({'msg': 'email already registered'}), 409

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        'email': email,
        'password': pw_hash,
        'role': role,
        'status': 'active',
    }
    res = mongo.db.users.insert_one(user)
    user['_id'] = res.inserted_id

    token = generate_token(user)
    return jsonify({'msg': 'registered', 'token': token}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'email and password required'}), 400

    user = mongo.db.users.find_one({'email': email})
    if not user:
        return jsonify({'msg': 'invalid credentials'}), 401

    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'msg': 'invalid credentials'}), 401

    # status check
    if user.get('status') == 'blocked':
        return jsonify({'msg': 'account blocked'}), 403

    token = generate_token(user)
    return jsonify({'msg': 'logged in', 'token': token})
import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId

user_bp = Blueprint('users', __name__)


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': ObjectId(uid)}, {'password': 0})
    if not user:
        return jsonify({'msg': 'not found'}), 404
    user['_id'] = str(user['_id'])
    return jsonify(user)


@user_bp.route('/profile', methods=['POST'])
@jwt_required()
def create_profile():
    uid = get_jwt_identity()
    data = request.form.to_dict()
    skills = request.form.get('skills', '')

    profile = {
        'user_id': uid,
        'bio': data.get('bio'),
        'skills': [s.strip() for s in skills.split(',')] if skills else [],
        'portfolio': data.get('portfolio', []),
        'status': 'pending',
    }

    # CV upload
    file = request.files.get('cv')
    if file:
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'cvs')
        os.makedirs(upload_dir, exist_ok=True)
        filename = f"{uid}_{file.filename}"
        path = os.path.join(upload_dir, filename)
        file.save(path)
        profile['cv_path'] = path

    mongo.db.profiles.insert_one(profile)
    return jsonify({'msg': 'profile submitted'})


@user_bp.route('/cv/<filename>', methods=['GET'])
def download_cv(filename):
    folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'cvs')
    return send_from_directory(folder, filename, as_attachment=True)
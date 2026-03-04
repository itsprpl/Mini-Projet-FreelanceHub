import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from bson import ObjectId

user_bp = Blueprint('users', __name__)


'''
GET /api/users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3MjAxMjg1NCwianRpIjoiY2ZiMGVjOWQtNzk4NS00M2MwLWFkM2UtMzBiMzdiNjdjZTRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY5OWVjNTBhNjQzN2YwNDIzNWFkOTU3ZiIsIm5iZiI6MTc3MjAxMjg1NCwiY3NyZiI6IjllMWJmNjExLWFhNzAtNDI0Ny1iNjg1LTk4MTdiMTY5MjVlNyIsImV4cCI6MTc3MjAxMzc1NCwicm9sZSI6ImZyZWVsYW5jZXIifQ.VappwIDZy6lfbEuF4u9DubZixuYFGvWq6CDsmdn8AHw
'''


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': ObjectId(uid)}, {'password': 0})
    if not user:
        return jsonify({'msg': 'not found'}), 404
    user['_id'] = str(user['_id'])
    return jsonify(user)



'''

POST /api/users/profile

request.form = {
  "bio": "Backend developer",
  "skills": "Python,Flask,MongoDB",
  "portfolio": "https://github.com/me"
}


curl -X POST http://localhost:5000/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "bio=Backend developer" \
  -F "skills=Python,Flask,MongoDB" \
  -F "portfolio=https://github.com/me" \
  -F "cv=@/path/to/cv.pdf"

'''
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
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId

gig_bp = Blueprint('gigs', __name__)


@gig_bp.route('/', methods=['POST'])
@jwt_required()
def create_gig():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    doc = {
        'freelancer_id': uid,
        'title': data.get('title'),
        'description': data.get('description'),
        'price': data.get('price'),
        'tags': data.get('tags', []),
        'status': 'pending'
    }
    res = mongo.db.gigs.insert_one(doc)
    return jsonify({'msg': 'gig submitted', 'id': str(res.inserted_id)}), 201


@gig_bp.route('/', methods=['GET'])
def list_gigs():
    # public only approved gigs
    q = {'status': 'approved'}
    docs = list(mongo.db.gigs.find(q))
    for d in docs:
        d['_id'] = str(d['_id'])
    return jsonify(docs)


@gig_bp.route('/<gig_id>', methods=['GET'])
def get_gig(gig_id):
    gig = mongo.db.gigs.find_one({'_id': ObjectId(gig_id)})
    if not gig:
        return jsonify({'msg': 'not found'}), 404
    gig['_id'] = str(gig['_id'])
    return jsonify(gig)
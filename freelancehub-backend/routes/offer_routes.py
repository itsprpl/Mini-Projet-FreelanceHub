from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId

offer_bp = Blueprint('offers', __name__)


@offer_bp.route('/', methods=['POST'])
@jwt_required()
def create_offer():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    doc = {
        'client_id': uid,
        'title': data.get('title'),
        'description': data.get('description'),
        'budget': data.get('budget'),
        'deadline': data.get('deadline'),
        'created_at': data.get('created_at')
    }
    res = mongo.db.offers.insert_one(doc)
    return jsonify({'msg': 'offer created', 'id': str(res.inserted_id)}), 201


@offer_bp.route('/<offer_id>/proposals', methods=['POST'])
@jwt_required()
def send_proposal(offer_id):
    uid = get_jwt_identity()
    data = request.get_json() or {}
    prop = {
        'offer_id': offer_id,
        'freelancer_id': uid,
        'amount': data.get('amount'),
        'message': data.get('message')
    }
    mongo.db.proposals.insert_one(prop)
    return jsonify({'msg': 'proposal sent'})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo

message_bp = Blueprint('messages', __name__)


@message_bp.route('/', methods=['POST'])
@jwt_required()
def send_message():
    sender = get_jwt_identity()
    data = request.get_json() or {}
    msg = {
        'sender': sender,
        'receiver': data.get('receiver'),
        'content': data.get('content'),
        'created_at': data.get('created_at')
    }
    mongo.db.messages.insert_one(msg)
    return jsonify({'msg': 'message sent'})


@message_bp.route('/conversations/<user_id>', methods=['GET'])
@jwt_required()
def get_conversation(user_id):
    me = get_jwt_identity()
    q = {'$or': [
        {'sender': me, 'receiver': user_id},
        {'sender': user_id, 'receiver': me}
    ]}
    msgs = list(mongo.db.messages.find(q))
    for m in msgs:
        m['_id'] = str(m['_id'])
    return jsonify(msgs)
import os
import uuid
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from bson import ObjectId

store_bp = Blueprint('store', __name__)


@store_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    # Multipart: product metadata + file
    uid = get_jwt_identity()
    data = request.form.to_dict()

    product = {
        'seller_id': uid,
        'name': data.get('name'),
        'version': data.get('version'),
        'license': data.get('license'),
        'price': float(data.get('price', 0)),
        'status': 'pending'
    }

    file = request.files.get('file')
    if file:
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products')
        os.makedirs(upload_dir, exist_ok=True)
        token = uuid.uuid4().hex
        filename = f"{token}_{file.filename}"
        path = os.path.join(upload_dir, filename)
        file.save(path)
        product['file_path'] = path
        product['download_token'] = token

    res = mongo.db.products.insert_one(product)
    return jsonify({'msg': 'product submitted', 'id': str(res.inserted_id)})


@store_bp.route('/', methods=['GET'])
def list_products():
    docs = list(mongo.db.products.find({'status': 'approved'}))
    for d in docs:
        d['_id'] = str(d['_id'])
    return jsonify(docs)


@store_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    p = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not p:
        return jsonify({'msg': 'not found'}), 404
    p['_id'] = str(p['_id'])
    return jsonify(p)


@store_bp.route('/<product_id>/buy', methods=['POST'])
@jwt_required()
def buy_product(product_id):
    # simulate purchase: create order record and return download token
    uid = get_jwt_identity()
    p = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not p or p.get('status') != 'approved':
        return jsonify({'msg': 'product not available'}), 404

    order = {
        'product_id': product_id,
        'buyer_id': uid,
        'seller_id': p.get('seller_id'),
        'price': p.get('price'),
    }
    res = mongo.db.orders.insert_one(order)
    return jsonify({'msg': 'purchase simulated', 'download_token': p.get('download_token')})


@store_bp.route('/download/<token>', methods=['GET'])
def download_by_token(token):
    p = mongo.db.products.find_one({'download_token': token})
    if not p:
        return jsonify({'msg': 'invalid token'}), 404
    folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products')
    filename = os.path.basename(p['file_path'])
    return send_from_directory(folder, filename, as_attachment=True)
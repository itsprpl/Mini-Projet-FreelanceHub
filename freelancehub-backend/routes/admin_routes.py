from flask import Blueprint, jsonify, request
from utils.decorators import admin_required
from extensions import mongo
from bson import ObjectId

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/pending/profiles', methods=['GET'])
@admin_required
def pending_profiles():
    docs = list(mongo.db.profiles.find({'status': 'pending'}))
    for d in docs:
        d['_id'] = str(d['_id'])
    return jsonify(docs)


@admin_bp.route('/profiles/<profile_id>/approve', methods=['POST'])
@admin_required
def approve_profile(profile_id):
    mongo.db.profiles.update_one({'_id': ObjectId(profile_id)}, {'$set': {'status': 'approved'}})
    return jsonify({'msg': 'profile approved'})


@admin_bp.route('/gigs/<gig_id>/approve', methods=['POST'])
@admin_required
def approve_gig(gig_id):
    mongo.db.gigs.update_one({'_id': ObjectId(gig_id)}, {'$set': {'status': 'approved'}})
    return jsonify({'msg': 'gig approved'})


@admin_bp.route('/products/<product_id>/approve', methods=['POST'])
@admin_required
def approve_product(product_id):
    mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': {'status': 'approved'}})
    return jsonify({'msg': 'product approved'})


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def stats():
    users = mongo.db.users.count_documents({})
    gigs = mongo.db.gigs.count_documents({})
    products = mongo.db.products.count_documents({})
    offers = mongo.db.offers.count_documents({})
    return jsonify({'users': users, 'gigs': gigs, 'products': products, 'offers': offers})
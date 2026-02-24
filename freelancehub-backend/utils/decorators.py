from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') != role and claims.get('role') != 'admin':
                return jsonify({'msg': 'Forbidden: insufficient role'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'msg': 'Admin only'}), 403
        return fn(*args, **kwargs)
    return wrapper
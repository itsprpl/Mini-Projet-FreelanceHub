# FreelanceHub Backend (Flask + MongoDB)

This repository contains a complete starter backend for the FreelanceHub mini-project (Ionic frontend expected). It implements authentication with roles, freelancer profiles, gigs, offers/proposals, simple messaging, a digital-store with simulated purchases and downloads, and an admin dashboard for validation.

---

## Project structure

```
freelancehub-backend/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
├── scripts/
│   └── seed_db.py
├── utils/
│   ├── jwt_utils.py
│   └── decorators.py
├── routes/
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── gig_routes.py
│   ├── offer_routes.py
│   ├── message_routes.py
│   ├── store_routes.py
│   └── admin_routes.py
├── storage/                # runtime (CVs, product files)
│   ├── cvs/
│   └── products/
└── tests/                  # optional tests (not included)
```

---

### requirements.txt

```text
Flask==2.3.2
Flask-PyMongo==2.3.0
Flask-Bcrypt==1.0.1
Flask-JWT-Extended==4.5.0
python-dotenv==1.0.0
pymongo==4.7.0
flask-cors==3.0.10
```

---

### .env.example

```
FLASK_ENV=development
FLASK_DEBUG=1
MONGO_URI=mongodb://localhost:27017/freelancehub
JWT_SECRET_KEY=replace_this_with_a_secure_random_string
UPLOAD_FOLDER=storage
```

---

### config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/freelancehub')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change-me')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'storage')
    JSONIFY_PRETTYPRINT_REGULAR = False
```

---

### app.py

```python
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.gig_routes import gig_bp
    from routes.offer_routes import offer_bp
    from routes.store_routes import store_bp
    from routes.message_routes import message_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(gig_bp, url_prefix='/api/gigs')
    app.register_blueprint(offer_bp, url_prefix='/api/offers')
    app.register_blueprint(store_bp, url_prefix='/api/store')
    app.register_blueprint(message_bp, url_prefix='/api/messages')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    @app.route('/')
    def index():
        return jsonify({'ok': True, 'msg': 'FreelanceHub API'})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
```

---

## utils/jwt_utils.py

```python
from flask_jwt_extended import create_access_token


def generate_token(user_doc):
    # user_doc is a dict-like document from MongoDB
    identity = str(user_doc.get('_id'))
    additional = {'role': user_doc.get('role', 'client')}
    token = create_access_token(identity=identity, additional_claims=additional)
    return token
```

---

## utils/decorators.py

```python
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
```

---

## routes/auth_routes.py

```python
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
```

---

## routes/user_routes.py

```python
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
```

---

## routes/gig_routes.py

```python
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
```

---

## routes/offer_routes.py

```python
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
```

---

## routes/message_routes.py

```python
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
```

---

## routes/store_routes.py

```python
import os
import uuid
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
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
```

---

## routes/admin_routes.py

```python
from flask import Blueprint, jsonify, request
from utils.decorators import admin_required
from app import mongo
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
```

---

## scripts/seed_db.py (optional quick seeder)

```python
from app import create_app, mongo
from bson import ObjectId

app = create_app()
with app.app_context():
    db = mongo.db
    db.users.insert_one({'email': 'admin@fh.com', 'password': 'pwd', 'role': 'admin', 'status': 'active'})
    print('seeded admin (note: password not hashed in this simple seeder)')
```

---

## README.md (run instructions)

````markdown
# FreelanceHub Backend

## Setup

1. Create a python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # windows: .venv\Scripts\activate
```
````

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and set `JWT_SECRET_KEY` and `MONGO_URI`.

4. Start MongoDB (local or Atlas) and ensure `MONGO_URI` is reachable.

5. Run the app

```bash
python app.py
```

Default server: `http://localhost:5000`

## Notes

- Upload files are stored in `storage/` by default.
- Admin endpoints require a JWT token whose `role` claim is `admin`.
- This is a starter backend designed to satisfy the project MVP and to be extended during sprints.

```

---

# Next steps I can do for you (pick any):

- Add Swagger / OpenAPI documentation for all endpoints.
- Add unit tests and Postman collection.
- Implement WebSocket (Socket.IO) real-time messaging.
- Add pagination, search, and filters for gigs and products.
- Add Dockerfile and docker-compose for local dev (Mongo + Flask).

---

End of backend starter.

(If you want any of the optional features or want me to adapt endpoints to a specific Ionic client schema, tell me which one and I will update the project.)
```

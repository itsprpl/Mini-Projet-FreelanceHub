from app import create_app, mongo
from bson import ObjectId

app = create_app()
with app.app_context():
    db = mongo.db
    db.users.insert_one({'email': 'admin@fh.com', 'password': 'pwd', 'role': 'admin', 'status': 'active'})
    print('seeded admin (note: password not hashed in this simple seeder)')
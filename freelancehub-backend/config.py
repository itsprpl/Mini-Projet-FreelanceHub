import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/freelancehub')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change-me')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'storage')
    JSONIFY_PRETTYPRINT_REGULAR = False
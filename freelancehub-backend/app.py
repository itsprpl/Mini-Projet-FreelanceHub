from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register routes
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.gig_routes import gig_bp
    from routes.offer_routes import offer_bp
    from routes.store_routes import store_bp
    from routes.message_routes import message_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(gig_bp, url_prefix="/api/gigs")
    app.register_blueprint(offer_bp, url_prefix="/api/offers")
    app.register_blueprint(store_bp, url_prefix="/api/store")
    app.register_blueprint(message_bp, url_prefix="/api/messages")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import mongo, bcrypt, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    # init extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # register routes
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
    app.run(debug=True)
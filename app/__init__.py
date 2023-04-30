from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from config import Config

db = MongoEngine()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.hospital import hospital_routes
    from app.routes.nurse import nurse_routes

    app.register_blueprint(hospital_routes)
    app.register_blueprint(nurse_routes)

    return app

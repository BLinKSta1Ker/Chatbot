from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes import chat_bp
from app.auth import auth_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

    jwt = JWTManager(app)  # Initialize JWT

    app.register_blueprint(auth_bp)  # Register Auth Routes
    app.register_blueprint(chat_bp)  # Register Chat Routes

    return app
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager  # Import JWTManager
from app.routes import chat_bp
from app.auth import auth_bp
from app.config import Config  # Import Config

def create_app():
    app = Flask(__name__)

    # Load configuration (includes JWT_SECRET_KEY)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

    # Initialize JWT
    jwt = JWTManager(app)  # 🔹 FIX: Initialize JWTManager

    # Initialize Rate Limiter
    limiter = Limiter(
        get_remote_address,  
        app=app,
        default_limits=["50 per minute"],
        storage_uri="memory://"
    )

    # Register blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)

    return app
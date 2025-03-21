from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.routes import chat_bp
from app.auth import auth_bp
from app.admin import admin_bp

def create_app():
    app = Flask(__name__)

    # Initialize JWT
    app.config["JWT_SECRET_KEY"] = "supersecret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hour
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]
    jwt = JWTManager(app) 

    # Initialize Rate Limiter
    limiter = Limiter(
        get_remote_address,  # Rate limit per IP
        app=app,
        default_limits=["50 per minute"],  # Limit each IP to 50 requests per minute
        storage_uri="memory://"  # Use in-memory store
    )

    # Register blueprints with rate limiting
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
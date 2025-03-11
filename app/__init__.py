from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.routes import chat_bp
from app.auth import auth_bp  # Import authentication routes

def create_app():
    app = Flask(__name__)

    # Initialize Rate Limiter
    limiter = Limiter(
        get_remote_address,  # Rate limit per IP
        app=app,
        default_limits=["50 per minute"],  # Limit each IP to 50 requests per minute
        storage_uri="memory://"  # Use in-memory store (can be Redis for production)
    )

    # Register blueprints with rate limiting
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)

    return app
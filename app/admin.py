from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import chat_collection

admin_bp = Blueprint("admin", __name__)

def is_admin(user_id):
    """Check if a user is an admin."""
    user = chat_collection.find_one({"user_id": user_id}, {"is_admin": 1})
    return user and user.get("is_admin", False)


@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_chat_statistics():
    """Retrieve chatbot statistics (total users, total messages)."""
    identity = get_jwt_identity()
    
    if not is_admin(identity):
        return jsonify({"error": "Unauthorized"}), 403

    total_users = chat_collection.count_documents({})
    total_chats = chat_collection.aggregate([{"$unwind": "$history"}, {"$count": "total"}])
    
    return jsonify({
        "total_users": total_users,
        "total_chats": list(total_chats)
    })


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    """List all registered users."""
    identity = get_jwt_identity()
    
    if not is_admin(identity):
        return jsonify({"error": "Unauthorized"}), 403

    users = chat_collection.distinct("user_id")
    return jsonify({"users": users})


@admin_bp.route("/delete_user", methods=["DELETE"])
@jwt_required()
def delete_user():
    """Delete a user from the system."""
    identity = get_jwt_identity()
    
    if not is_admin(identity):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Missing username"}), 400

    result = chat_collection.delete_one({"user_id": username})
    
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": f"User {username} deleted successfully"}), 200
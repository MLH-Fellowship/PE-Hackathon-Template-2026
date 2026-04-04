from datetime import datetime

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

from app.models.user import User

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
def create_user():
    """Create a new user with username and email."""
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is required"), 400

    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify(error="username and email are required"), 400

    # Check if username already exists
    if User.select().where(User.username == username).exists():
        return jsonify(error="Username already exists"), 409

    # Check if email already exists
    if User.select().where(User.email == email).exists():
        return jsonify(error="Email already exists"), 409

    # Create the new user
    user = User.create(
        username=username,
        email=email,
        created_at=datetime.now()
    )

    return jsonify(model_to_dict(user)), 201


@users_bp.route("/users", methods=["GET"])
def list_users():
    """List all users."""
    users = User.select().order_by(User.id)
    return jsonify([model_to_dict(u) for u in users])


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user by ID."""
    try:
        user = User.get_by_id(user_id)
        return jsonify(model_to_dict(user))
    except User.DoesNotExist:
        return jsonify(error="User not found"), 404

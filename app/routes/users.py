from flask import Blueprint, jsonify, request
from peewee import IntegrityError

from app.models.users import User

users_bp = Blueprint("users", __name__, url_prefix="/users/v1/api/users")


def serialize_user(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
        "is_active": user.is_active,
    }


@users_bp.get("/")
def list_users():
    users = User.select().order_by(User.id)
    return jsonify({
        "data": [serialize_user(user) for user in users]
    }), 200


@users_bp.get("/<int:user_id>")
def get_user(user_id):
    user = User.get_or_none(User.id == user_id)

    if user is None or not user.is_active:
        return jsonify({
            "error": {
                "code": "NOT_FOUND",
                "message": "User not found"
            }
        }), 404

    return jsonify({"data": serialize_user(user)}), 200


@users_bp.post("/")
def create_user():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "Request body must be valid JSON"
            }
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "name, email, and password are required"
            }
        }), 400

    try:
        user = User.create(
            name=name,
            email=email,
            password_hash=password,
        )
    except IntegrityError:
        return jsonify({
            "error": {
                "code": "CONFLICT",
                "message": "email already exists"
            }
        }), 409

    return jsonify({"data": serialize_user(user)}), 201


@users_bp.patch("/<int:user_id>")
def update_user(user_id):
    user = User.get_or_none(User.id == user_id)

    if user is None or not user.is_active:
        return jsonify({
            "error": {
                "code": "NOT_FOUND",
                "message": "User not found"
            }
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "Request body must be valid JSON"
            }
        }), 400

    name = data.get("name")
    email = data.get("email")

    if name is None and email is None:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "At least one updatable field is required"
            }
        }), 400

    if name is not None:
        user.name = name

    if email is not None:
        user.email = email

    try:
        user.save()
    except IntegrityError:
        return jsonify({
            "error": {
                "code": "CONFLICT",
                "message": "email already exists"
            }
        }), 409

    return jsonify({"data": serialize_user(user)}), 200


@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    user = User.get_or_none(User.id == user_id)

    if user is None or not user.is_active:
        return jsonify({
            "error": {
                "code": "NOT_FOUND",
                "message": "User not found"
            }
        }), 404

    user.is_active = False
    user.save()

    return jsonify({
        "message": "User deleted successfully"
    }), 200
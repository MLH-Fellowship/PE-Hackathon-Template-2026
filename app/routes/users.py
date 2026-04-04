import csv
import io
from datetime import datetime
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from peewee import chunked
from app.database import db
from app.models.user import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    users = User.select().paginate(page, per_page)
    return jsonify([model_to_dict(u) for u in users])

@users_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = User.get_by_id(id)
        return jsonify(model_to_dict(user))
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    
    if not data or not isinstance(data.get('username'), str) or not isinstance(data.get('email'), str):
        return jsonify({"error": "Invalid data"}), 400
    
    try:
        user = User.create(
            username=data['username'],
            email=data['email'],
            created_at=datetime.now()
        )
        return jsonify(model_to_dict(user)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        user = User.get_by_id(id)
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    user.save()
    return jsonify(model_to_dict(user))

@users_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.get_by_id(id)
        user.delete_instance()
        return jsonify({"message": "Deleted"}), 200
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

@users_bp.route("/users/bulk", methods=["POST"])
def bulk_upload_users():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    content = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(content))
    
    rows = []
    for row in reader:
        rows.append({
            'id': int(row['id']),
            'username': row['username'],
            'email': row['email'],
            'created_at': row['created_at']
        })
    
    with db.atomic():
        for batch in chunked(rows, 100):
            User.insert_many(batch).execute()
    
    return jsonify({"count": len(rows)}), 201
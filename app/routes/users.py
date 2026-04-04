import csv
import io

from flask import Blueprint, request, jsonify, abort
from peewee import chunked
from playhouse.shortcuts import model_to_dict

from app.database import db
from app.models.user import User

users_bp = Blueprint("users", __name__)


@users_bp.route("/users/bulk", methods=["POST"])
def bulk_import_users():
    if "file" not in request.files:
        abort(400, description="Missing 'file' field")

    file = request.files["file"]
    if not file.filename or not file.filename.endswith(".csv"):
        abort(400, description="Invalid file type")

    content = file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)

    with db.atomic():
        User.delete().execute()
        for batch in chunked(rows, 100):
            User.insert_many(batch).execute()

    return jsonify({"imported": len(rows)}), 200


@users_bp.route("/users", methods=["GET"])
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    total = User.count()
    offset = (page - 1) * per_page
    users = User.select().limit(per_page).offset(offset)

    return jsonify([model_to_dict(u) for u in users])
    except Exception as e:
        abort(400, description=str(e))

    return jsonify(model_to_dict(user)), 201


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = User.get_by_id(user_id)
    except User.DoesNotExist:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Invalid JSON")

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]

    user.save()
    return jsonify(model_to_dict(user))

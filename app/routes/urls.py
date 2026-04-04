import csv
import io
import random
import string
from datetime import datetime
from flask import Blueprint, jsonify, request, redirect
from playhouse.shortcuts import model_to_dict
from peewee import chunked
from app.database import db
from app.models import Url

urls_bp = Blueprint("urls", __name__)

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

@urls_bp.route("/urls", methods=["GET"])
def list_urls():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    user_id = request.args.get('user_id', type=int)
    query = Url.select()
    if user_id:
        query = query.where(Url.user_id == user_id)
    urls = query.paginate(page, per_page)
    return jsonify([model_to_dict(u) for u in urls])

@urls_bp.route("/urls/<int:id>", methods=["GET"])
def get_url(id):
    try:
        url = Url.get_by_id(id)
        return jsonify(model_to_dict(url))
    except Url.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404

@urls_bp.route("/urls", methods=["POST"])
def create_url():
    data = request.get_json()
    if not data or not data.get('original_url'):
        return jsonify({"error": "original_url required"}), 400
    short_code = data.get('short_code') or generate_short_code()
    while Url.select().where(Url.short_code == short_code).exists():
        short_code = generate_short_code()
    url = Url.create(
        user_id=data.get('user_id'),
        short_code=short_code,
        original_url=data['original_url'],
        title=data.get('title'),
        is_active=data.get('is_active', True),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    return jsonify(model_to_dict(url)), 201

@urls_bp.route("/urls/<int:id>", methods=["PUT"])
def update_url(id):
    try:
        url = Url.get_by_id(id)
    except Url.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404
    data = request.get_json()
    if 'original_url' in data:
        url.original_url = data['original_url']
    if 'title' in data:
        url.title = data['title']
    if 'is_active' in data:
        url.is_active = data['is_active']
    url.updated_at = datetime.now()
    url.save()
    return jsonify(model_to_dict(url))

@urls_bp.route("/urls/<int:id>", methods=["DELETE"])
def delete_url(id):
    try:
        url = Url.get_by_id(id)
        url.delete_instance()
        return jsonify({"message": "Deleted"}), 200
    except Url.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404

@urls_bp.route("/urls/bulk", methods=["POST"])
def bulk_upload_urls():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    content = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(content))
    rows = []
    for row in reader:
        rows.append({
            'id': int(row['id']),
            'user_id': int(row['user_id']),
            'short_code': row['short_code'],
            'original_url': row['original_url'],
            'title': row['title'],
            'is_active': row['is_active'] == 'TRUE',
            'created_at': row['created_at'],
            'updated_at': row['updated_at']
        })
    with db.atomic():
        for batch in chunked(rows, 100):
            Url.insert_many(batch).execute()
    return jsonify({"count": len(rows)}), 201

@urls_bp.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    try:
        url = Url.get(Url.short_code == short_code)
        if not url.is_active:
            return jsonify({"error": "URL is inactive"}), 410
        return redirect(url.original_url, code=302)
    except Url.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404

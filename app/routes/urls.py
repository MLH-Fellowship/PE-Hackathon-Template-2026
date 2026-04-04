import random
import string

from flask import Blueprint, request, jsonify, abort
from playhouse.shortcuts import model_to_dict

from app.models.url import Url
from app.models.user import User
from app.utils.events import create_event

urls_bp = Blueprint("urls", __name__)


def generate_short_code(length=6):
    while True:
        code = "".join(random.choices(string.ascii_letters + string.digits, k=length))
        if not Url.select().where(Url.short_code == code).exists():
            return code


def format_url(url):
    d = model_to_dict(url)
    d["user_id"] = d.pop("user")
    return d


@urls_bp.route("/urls", methods=["POST"])
def create_url():
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Invalid JSON")

    user_id = data.get("user_id")
    original_url = data.get("original_url")
    title = data.get("title")

    if not user_id or not isinstance(user_id, int):
        abort(400, description="user_id must be an integer")
    if not original_url or not isinstance(original_url, str):
        abort(400, description="original_url must be a string")
    if not title or not isinstance(title, str):
        abort(400, description="title must be a string")

    try:
        User.get_by_id(user_id)
    except User.DoesNotExist:
        abort(400, description="User not found")

    short_code = generate_short_code()

    url = Url.create(
        user_id=user_id,
        short_code=short_code,
        original_url=original_url,
        title=title,
        is_active=True,
    )

    create_event(
        url.id,
        user_id,
        "created",
        {
            "short_code": short_code,
            "original_url": original_url,
        },
    )

    return jsonify(format_url(url)), 201


@urls_bp.route("/urls", methods=["GET"])
def list_urls():
    query = Url.select()

    if "id" in request.args:
        query = query.where(Url.id == request.args.get("id", type=int))
    if "user_id" in request.args:
        query = query.where(Url.user_id == request.args.get("user_id", type=int))
    if "short_code" in request.args:
        query = query.where(Url.short_code == request.args["short_code"])
    if "original_url" in request.args:
        query = query.where(Url.original_url == request.args["original_url"])
    if "is_active" in request.args:
        val = request.args["is_active"].lower()
        query = query.where(Url.is_active == (val == "true"))

    return jsonify([format_url(u) for u in query])


@urls_bp.route("/urls/<int:url_id>", methods=["GET"])
def get_url(url_id):
    try:
        url = Url.get_by_id(url_id)
    except Url.DoesNotExist:
        abort(404)
    return jsonify(format_url(url))


@urls_bp.route("/urls/<int:url_id>", methods=["PUT"])
def update_url(url_id):
    try:
        url = Url.get_by_id(url_id)
    except Url.DoesNotExist:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Invalid JSON")

    if "title" in data:
        url.title = data["title"]
        create_event(
            url.id,
            url.user_id,
            "updated",
            {
                "field": "title",
                "new_value": data["title"],
            },
        )

    if "is_active" in data:
        url.is_active = data["is_active"]
        create_event(
            url.id,
            url.user_id,
            "updated",
            {
                "field": "is_active",
                "new_value": data["is_active"],
            },
        )

    url.save()
    return jsonify(format_url(url))

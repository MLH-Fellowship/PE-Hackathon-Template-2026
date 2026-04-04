import random
import string
from datetime import datetime
import json

from flask import Blueprint, jsonify, request

from app.models.user import User
from app.models.url import Url
from app.models.event import Event

url_creation_bp = Blueprint("url_creation", __name__)


def generate_short_code(length=6):
    """Generate a random short code."""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        # Make sure it doesn't already exist
        if not Url.select().where(Url.short_code == code).exists():
            return code


@url_creation_bp.route("/shorten", methods=["POST"])
def shorten_url():
    """
    Create a shortened URL.

    Request body:
        - user_id: ID of the user creating the URL
        - original_url: The URL to shorten
        - title: A title/description for the URL

    Returns:
        - short_code: The generated short code
        - short_url: The full shortened URL
        - original_url: The original URL
        - title: The provided title
    """
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is required"), 400

    user_id = data.get("user_id")
    original_url = data.get("original_url")
    title = data.get("title")

    # Validate required fields
    if not user_id:
        return jsonify(error="user_id is required"), 400
    if not original_url:
        return jsonify(error="original_url is required"), 400
    if not title:
        return jsonify(error="title is required"), 400

    # Verify user exists
    try:
        user = User.get_by_id(user_id)
    except User.DoesNotExist:
        return jsonify(error="User not found"), 404

    # Generate unique short code
    short_code = generate_short_code()
    now = datetime.now()

    # Create the URL record
    url = Url.create(
        user_id=user,
        short_code=short_code,
        original_url=original_url,
        title=title,
        is_active=True,
        created_at=now,
        updated_at=now
    )

    # Log the creation event
    Event.create(
        url_id=url,
        user_id=user,
        event_type="created",
        timestamp=now,
        details=json.dumps({
            "short_code": short_code,
            "original_url": original_url
        })
    )

    # Build the shortened URL
    short_url = f"{request.host_url}{short_code}"

    return jsonify({
        "id": url.id,
        "short_code": short_code,
        "short_url": short_url,
        "original_url": original_url,
        "title": title,
        "created_at": url.created_at.isoformat()
    }), 201

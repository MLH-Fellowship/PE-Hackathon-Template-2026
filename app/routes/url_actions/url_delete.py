from datetime import datetime
import json

from flask import Blueprint, jsonify, request

from app.models.user import User
from app.models.url import Url
from app.models.event import Event

url_delete_bp = Blueprint("url_delete", __name__)


@url_delete_bp.route("/delete", methods=["POST"])
def delete_url():
    """
    Delete a URL by user_id and title.

    Request body:
        - user_id: ID of the user requesting deletion
        - title: The title of the URL to delete

    Returns:
        - Confirmation of deletion
    """
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is required"), 400

    user_id = data.get("user_id")
    title = data.get("title")

    # Validate required fields
    if not user_id:
        return jsonify(error="user_id is required"), 400
    if not title:
        return jsonify(error="title is required"), 400

    # Verify user exists
    try:
        user = User.get_by_id(user_id)
    except User.DoesNotExist:
        return jsonify(error="User not found"), 404

    # Find the URL by title and user_id
    try:
        url = Url.get((Url.title == title) & (Url.user_id == user_id))
    except Url.DoesNotExist:
        return jsonify(error="URL not found with that title for this user"), 404

    # Store URL info for response before deletion
    deleted_url_info = {
        "url_id": url.id,
        "short_code": url.short_code,
        "original_url": url.original_url,
        "title": url.title
    }

    # Delete all events associated with this URL
    events_deleted = Event.delete().where(Event.url_id == url.id).execute()

    # Delete the URL
    url.delete_instance()

    return jsonify({
        "message": "URL deleted successfully",
        "deleted_url": deleted_url_info,
        "events_deleted": events_deleted
    }), 200

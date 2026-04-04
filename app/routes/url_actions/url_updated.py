from datetime import datetime
import json

from flask import Blueprint, jsonify, request

from app.models.user import User
from app.models.url import Url
from app.models.event import Event

url_updated_bp = Blueprint("url_updated", __name__)

# Fields that are allowed to be updated
ALLOWED_FIELDS = ["title", "is_active", "original_url"]


@url_updated_bp.route("/update", methods=["POST"])
def update_url():
    """
    Update a specific field of a URL.

    Request body:
        - user_id: ID of the user making the change
        - url_id: ID of the URL to update
        - field: The field to update (title, is_active, or original_url)
        - new_value: The new value for the field

    Returns:
        - Confirmation with updated URL details
    """
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is required"), 400

    user_id = data.get("user_id")
    url_id = data.get("url_id")
    field = data.get("field")
    new_value = data.get("new_value")

    # Validate required fields
    if not user_id:
        return jsonify(error="user_id is required"), 400
    if not url_id:
        return jsonify(error="url_id is required"), 400
    if not field:
        return jsonify(error="field is required"), 400
    if new_value is None:
        return jsonify(error="new_value is required"), 400

    # Validate field is allowed
    if field not in ALLOWED_FIELDS:
        return jsonify(
            error=f"Invalid field. Allowed fields: {', '.join(ALLOWED_FIELDS)}"
        ), 400

    # Verify user exists
    try:
        user = User.get_by_id(user_id)
    except User.DoesNotExist:
        return jsonify(error="User not found"), 404

    # Verify URL exists
    try:
        url = Url.get_by_id(url_id)
    except Url.DoesNotExist:
        return jsonify(error="URL not found"), 404

    # Store old value for event logging
    old_value = getattr(url, field)

    # Update the field
    setattr(url, field, new_value)
    url.updated_at = datetime.now()
    url.save()

    # Log the update event
    Event.create(
        url_id=url,
        user_id=user,
        event_type="updated",
        timestamp=datetime.now(),
        details=json.dumps({
            "field": field,
            "old_value": str(old_value),
            "new_value": str(new_value)
        })
    )

    return jsonify({
        "message": "URL updated successfully",
        "url_id": url.id,
        "field": field,
        "old_value": str(old_value),
        "new_value": str(new_value),
        "updated_at": url.updated_at.isoformat()
    }), 200

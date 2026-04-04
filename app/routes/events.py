from flask import Blueprint, jsonify, request

from app.models.events import Event

events_bp = Blueprint("events", __name__, url_prefix="/events/v1/api/events")


def serialize_event(event):
    return {
        "id": event.id,
        "url_id": event.url_id,
        "user_id": event.user_id,
        "event_type": event.event_type,
        "timestamp": event.timestamp.isoformat(),
        "details": event.details,
        "created_at": event.created_at.isoformat(),
        "updated_at": event.updated_at.isoformat(),
    }


@events_bp.get("/")
def list_events():
    events = Event.select().order_by(Event.id)
    return jsonify({
        "data": [serialize_event(event) for event in events]
    }), 200


@events_bp.post("/")
def create_event():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "Request body must be valid JSON"
            }
        }), 400

    url_id = data.get("url_id")
    event_type = data.get("event_type")

    if not url_id or not event_type:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "url_id and event_type are required"
            }
        }), 400

    event = Event.create(
        url_id=url_id,
        user_id=data.get("user_id"),
        event_type=event_type,
        details=data.get("details"),
    )

    return jsonify({"data": serialize_event(event)}), 201
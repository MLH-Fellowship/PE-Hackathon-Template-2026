import json

from flask import Blueprint, jsonify
from playhouse.shortcuts import model_to_dict

from app.models.event import Event

events_bp = Blueprint("events", __name__)


@events_bp.route("/events", methods=["GET"])
def list_events():
    events = Event.select()
    result = []
    for e in events:
        d = model_to_dict(e)
        d["url_id"] = d.pop("url")
        d["user_id"] = d.pop("user")
        try:
            d["details"] = json.loads(d["details"])
        except (json.JSONDecodeError, TypeError):
            d["details"] = {}
        result.append(d)
    return jsonify(result)

import json
from datetime import datetime

from app.models.event import Event


def create_event(url_id, user_id, event_type, details_dict):
    Event.create(
        url_id=url_id,
        user_id=user_id,
        event_type=event_type,
        timestamp=datetime.utcnow(),
        details=json.dumps(details_dict),
    )

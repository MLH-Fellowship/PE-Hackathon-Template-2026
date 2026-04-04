import csv
import json
from datetime import datetime

from app import create_app
from app.database import db
from app.models.events import Event

app = create_app()

with app.app_context():
    with db.connection_context():

        # optional: clear table before seeding
        Event.delete().execute()

        with open("seed/events.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            count = 0

            for row in reader:
                Event.create(
                    id=int(row["id"]),
                    url_id=int(row["url_id"]),
                    user_id=int(row["user_id"]) if row["user_id"] else None,
                    event_type=row["event_type"],
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    details=json.loads(row["details"]) if row["details"] else None,
                )
                count += 1

            print(f"Inserted {count} events")
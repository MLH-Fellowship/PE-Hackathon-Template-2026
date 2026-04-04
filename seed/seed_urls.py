import csv
from datetime import datetime

from app import create_app
from app.database import db
from app.models.urls import Url


def convert_string_to_bool(boolStringValue):
    return str(boolStringValue).strip().lower() == "true"


app = create_app()

with app.app_context():
    with db.connection_context():
        # optional: clear old rows first
        Url.delete().execute()

        with open("seed/urls.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            insertedCount = 0

            for row in reader:
                Url.create(
                    id=int(row["id"]),
                    user_id=int(row["user_id"]) if row["user_id"] else None,
                    short_code=row["short_code"],
                    original_url=row["original_url"],
                    title=row["title"],
                    is_active=convert_string_to_bool(row["is_active"]),
                    created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
                    updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
                )
                insertedCount += 1

            print(f"Inserted {insertedCount} urls")
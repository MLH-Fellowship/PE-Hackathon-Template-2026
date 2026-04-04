"""Load seed data from CSV files in data/ into the database."""

import csv
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from peewee import PostgresqlDatabase, chunked

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import db


def _init_db() -> None:
    database = PostgresqlDatabase(
        os.environ.get("DATABASE_NAME", "hackathon_db"),
        host=os.environ.get("DATABASE_HOST", "localhost"),
        port=int(os.environ.get("DATABASE_PORT", 5432)),
        user=os.environ.get("DATABASE_USER", "postgres"),
        password=os.environ.get("DATABASE_PASSWORD", "postgres"),
    )
    db.initialize(database)


def _load_csv(filepath: str) -> list[dict]:
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))


def seed() -> None:
    data_dir = Path(__file__).resolve().parents[1] / "data"

    from app.models.user import User
    from app.models.url import Url
    from app.models.event import Event

    # Load users
    users_file = data_dir / "users.csv"
    if users_file.exists():
        rows = _load_csv(str(users_file))
        with db.atomic():
            for batch in chunked(rows, 100):
                User.insert_many(batch).execute()
        print(f"Loaded {len(rows)} users")

    # Load urls
    urls_file = data_dir / "urls.csv"
    if urls_file.exists():
        rows = _load_csv(str(urls_file))
        for row in rows:
            row["is_active"] = row["is_active"] == "True"
        with db.atomic():
            for batch in chunked(rows, 100):
                Url.insert_many(batch).execute()
        print(f"Loaded {len(rows)} urls")

    # Load events
    events_file = data_dir / "events.csv"
    if events_file.exists():
        rows = _load_csv(str(events_file))
        with db.atomic():
            for batch in chunked(rows, 100):
                Event.insert_many(batch).execute()
        print(f"Loaded {len(rows)} events")


if __name__ == "__main__":
    load_dotenv()
    _init_db()
    db.connect(reuse_if_open=True)
    try:
        seed()
    finally:
        if not db.is_closed():
            db.close()

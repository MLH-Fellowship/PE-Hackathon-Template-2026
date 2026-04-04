# PYTHONPATH=. uv run scripts/load_csv.py to load the csv files into db

import csv
import os

from peewee import chunked

from app import create_app
from app.database import db
from app.models import User, Url, Event

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_DIR = os.path.join(BASE_DIR, "res")


def load_csv(filepath):
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def main():
    app = create_app()

    with app.app_context():
        db.drop_tables([Event, Url, User])
        db.create_tables([Event, Url, User])

        users = load_csv(os.path.join(RES_DIR, "users.csv"))
        with db.atomic():
            for batch in chunked(users, 100):
                User.insert_many(batch).execute()
        print(f"  Loaded {len(users)} users")

        urls = load_csv(os.path.join(RES_DIR, "urls.csv"))
        with db.atomic():
            for batch in chunked(urls, 100):
                Url.insert_many(batch).execute()
        print(f"  Loaded {len(urls)} urls")

        events = load_csv(os.path.join(RES_DIR, "events.csv"))
        with db.atomic():
            for batch in chunked(events, 100):
                Event.insert_many(batch).execute()
        print(f"  Loaded {len(events)} events")


if __name__ == "__main__":
    main()

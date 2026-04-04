import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from peewee import PostgresqlDatabase
from peewee_migrate import Router

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


def main() -> None:
    load_dotenv()
    _init_db()

    parser = argparse.ArgumentParser(description="Run peewee migrations")
    parser.add_argument("command", choices=["up", "down", "create"])
    parser.add_argument("name", nargs="?", default="auto")
    args = parser.parse_args()

    router = Router(db, migrate_dir="migrations")
    db.connect(reuse_if_open=True)
    try:
        if args.command == "up":
            router.run()
        elif args.command == "down":
            router.rollback()
        else:
            router.create(args.name)
    finally:
        if not db.is_closed():
            db.close()


if __name__ == "__main__":
    main()

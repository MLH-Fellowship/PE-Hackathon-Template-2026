import csv
from peewee import chunked
from app.database import db


def load_csv(filepath, model):
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with db.atomic():
        for batch in chunked(rows, 100):
            model.insert_many(batch).execute()




from datetime import datetime

from peewee import CharField, DateTimeField

from app.database import BaseModel


class User(BaseModel):
    username = CharField(unique=True)
    email = CharField()
    created_at = DateTimeField(default=datetime.utcnow)

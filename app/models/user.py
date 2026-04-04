from datetime import datetime

from peewee import AutoField, CharField, DateTimeField

from app.database import BaseModel


class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True)
    email = CharField(unique=True)
    created_at = DateTimeField(default=datetime.now())

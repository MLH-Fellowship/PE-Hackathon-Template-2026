from peewee import CharField, DateTimeField

from app.database import BaseModel


class User(BaseModel):
    username = CharField()
    email = CharField()
    created_at = DateTimeField()

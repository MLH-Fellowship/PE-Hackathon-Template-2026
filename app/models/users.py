from peewee import AutoField, CharField, DateTimeField

from app.database import BaseModel


class User(BaseModel):
    id = AutoField(primary_key=True)
    username = CharField()
    email = CharField()
    created_at = DateTimeField()

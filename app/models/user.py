from peewee import AutoField, CharField, DateTimeField

from app.database import BaseModel


class User(BaseModel):
    id = AutoField()
    username = CharField()
    email = CharField()
    created_at = DateTimeField()

    class Meta:
        table_name = "users"

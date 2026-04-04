from peewee import CharField, DateTimeField, ForeignKeyField, BooleanField

from app.database import BaseModel
from app.models.user import User


class Url(BaseModel):
    user = ForeignKeyField(User, backref="urls")
    short_code = CharField()
    original_url = CharField()
    title = CharField()
    is_active = BooleanField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

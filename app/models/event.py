from peewee import CharField, DateTimeField, ForeignKeyField, TextField

from app.database import BaseModel
from app.models.url import Url
from app.models.user import User


class Event(BaseModel):
    url = ForeignKeyField(Url, backref="events")
    user = ForeignKeyField(User, backref="events")
    event_type = CharField()
    timestamp = DateTimeField()
    details = TextField()

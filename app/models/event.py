from datetime import datetime

from peewee import AutoField, CharField, DateTimeField, ForeignKeyField, TextField

from app.database import BaseModel
from app.models.url import Url
from app.models.user import User


class Event(BaseModel):
    id = AutoField()
    url = ForeignKeyField(Url, backref="events")
    user = ForeignKeyField(User, backref="events")
    event_type = CharField()
    timestamp = DateTimeField(default=datetime.now())
    details = TextField()

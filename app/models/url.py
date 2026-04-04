from datetime import datetime

from peewee import CharField, DateTimeField, IntegerField, TextField

from app.database import BaseModel


class Url(BaseModel):
    original_url = TextField()
    short_code = CharField(max_length=12, unique=True, index=True)
    created_at = DateTimeField(default=datetime.utcnow)
    visits = IntegerField(default=0)

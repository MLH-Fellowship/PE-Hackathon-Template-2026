from datetime import datetime

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    TextField,
)

from app.database import BaseModel
from app.models.user import User


class Url(BaseModel):
    user = ForeignKeyField(User, backref="urls", null=True)
    short_code = CharField(max_length=12, unique=True, index=True)
    original_url = TextField()
    title = CharField(null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

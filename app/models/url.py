from datetime import datetime

from peewee import AutoField, CharField, DateTimeField, ForeignKeyField, BooleanField

from app.database import BaseModel
from app.models.user import User


class Url(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="urls")
    short_code = CharField(unique=True)
    original_url = CharField()
    title = CharField()
    is_active = BooleanField()
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

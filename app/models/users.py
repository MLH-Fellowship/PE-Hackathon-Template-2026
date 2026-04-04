from datetime import datetime
from peewee import AutoField, BooleanField, CharField, DateTimeField

from app.database import BaseModel


class User(BaseModel):
    id = AutoField()
    name = CharField(max_length=100)
    email = CharField(max_length=255, unique=True)
    password_hash = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)

    class Meta:
        table_name = "users"

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

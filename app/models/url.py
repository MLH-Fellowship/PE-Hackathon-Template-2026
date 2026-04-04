from peewee import AutoField, CharField, TextField, BooleanField, DateTimeField, ForeignKeyField

from app.database import BaseModel
from app.models.user import User


class Url(BaseModel):
    id = AutoField()
    user_id = ForeignKeyField(User, backref="urls", column_name="user_id")
    short_code = CharField()
    original_url = TextField()
    title = CharField()
    is_active = BooleanField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "urls"

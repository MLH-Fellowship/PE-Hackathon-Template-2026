from peewee import *
from datetime import datetime
from app.database import BaseModel


class Url(BaseModel):
    id = AutoField()
    user_id = CharField(max_length=100)
    shortcode = CharField(max_length=255, unique=True)
    original_url = TextField()
    title = CharField(max_length=255, null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "urls"

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Url, self).save(*args, **kwargs)

    def __str__(self):
        return self.shortcode

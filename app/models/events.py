from peewee import *
from datetime import datetime
from app.database import BaseModel


class Event(BaseModel):
    id = AutoField()
    url_id = CharField(max_length=255)
    user_id = TextField(null=True)
    event_type = CharField(max_length=100)
    timestamp = DateTimeField(default=datetime.now)
    details = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "events"
        order_by = ("-created_at",)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.event_type} - {self.url_id}"

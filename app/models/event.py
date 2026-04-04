from peewee import CharField, DateTimeField, ForeignKeyField, AutoField, TextField
from app.database import BaseModel
from app.models.user import User
from app.models.url import Url

class Event(BaseModel):
    id = AutoField()
    url_id = ForeignKeyField(Url, backref='events', column_name='url_id')
    user_id = ForeignKeyField(User, backref='events', column_name='user_id')
    event_type = CharField()
    timestamp = DateTimeField()
    details = TextField(null=True)

    class Meta:
        table_name = 'events'
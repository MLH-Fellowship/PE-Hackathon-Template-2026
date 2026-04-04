from peewee import CharField, DateTimeField, AutoField
from app.database import BaseModel

class User(BaseModel):
    id = AutoField()
    username = CharField()
    email = CharField(unique=True)
    created_at = DateTimeField()

    class Meta:
        table_name = 'users'
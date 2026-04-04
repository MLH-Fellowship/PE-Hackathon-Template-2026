from peewee import CharField, DateTimeField, BooleanField, ForeignKeyField, AutoField
from app.database import BaseModel
from app.models.user import User

class Url(BaseModel):
    id = AutoField()
    user_id = ForeignKeyField(User, backref='urls', column_name='user_id')
    short_code = CharField(unique=True, max_length=10)
    original_url = CharField()
    title = CharField(null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'urls'
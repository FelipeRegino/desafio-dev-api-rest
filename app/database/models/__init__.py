from playhouse.signals import Model
from app.database.provider import DatabaseProvider

db = DatabaseProvider().get_database()

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db
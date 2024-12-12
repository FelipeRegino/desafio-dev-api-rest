from datetime import datetime

from peewee import CharField, UUIDField, ForeignKeyField, DecimalField, DateTimeField, Check

from app.database.models import BaseModel
from app.database.models.holder import Holder


class DockAccount(BaseModel):
    id = UUIDField(unique=True, primary_key=True)
    holder = ForeignKeyField(Holder, backref="accounts")
    number = CharField()
    agency = CharField()
    balance = DecimalField(constraints=[Check("balance >= 0")])
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True, default=None)
    status = CharField(default="ACTIVE")

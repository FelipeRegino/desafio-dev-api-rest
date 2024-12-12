from peewee import CharField, BooleanField

from app.database.models import BaseModel


class Holder(BaseModel):
    cpf = CharField(unique=True, primary_key=True)
    name = CharField()
    status = BooleanField(default=True)

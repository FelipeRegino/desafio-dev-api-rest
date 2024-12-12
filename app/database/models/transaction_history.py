from datetime import datetime

from peewee import CharField, UUIDField, ForeignKeyField, DecimalField, DateTimeField
from playhouse.signals import post_save

from app.database.models import BaseModel
from app.database.models.dock_account import DockAccount
from app.repositories.dock_account_repository import DockAccountRepository

class TransactionHistory(BaseModel):
    id = UUIDField(unique=True, primary_key=True)
    dock_account = ForeignKeyField(DockAccount, backref="transactions")
    type = CharField()
    amount = DecimalField()
    created_at = DateTimeField(default=datetime.now)

@post_save(sender=TransactionHistory)
def on_save_handler(model_class, instance, created):
    _repository = DockAccountRepository()
    _repository.make_transaction(
        dock_account=instance.dock_account, amount=instance.amount, transaction_type=instance.type
    )

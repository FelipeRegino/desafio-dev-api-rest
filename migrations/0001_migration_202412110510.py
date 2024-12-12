# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Holder(peewee.Model):
    cpf = CharField(max_length=255, primary_key=True, unique=True)
    name = CharField(max_length=255)
    status = BooleanField(default=True)
    class Meta:
        table_name = "holder"


@snapshot.append
class DockAccount(peewee.Model):
    id = UUIDField(primary_key=True, unique=True)
    holder = snapshot.ForeignKeyField(backref='accounts', index=True, model='holder')
    number = CharField(max_length=255)
    agency = CharField(max_length=255)
    balance = DecimalField(auto_round=False, constraints=[SQL('CHECK (balance >= 0)')], decimal_places=5, max_digits=10, rounding='ROUND_HALF_EVEN')
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True)
    status = CharField(default='ACTIVE', max_length=255)
    class Meta:
        table_name = "dockaccount"


@snapshot.append
class TransactionHistory(peewee.Model):
    id = UUIDField(primary_key=True, unique=True)
    dock_account = snapshot.ForeignKeyField(backref='transactions', index=True, model='dockaccount')
    type = CharField(max_length=255)
    amount = DecimalField(auto_round=False, decimal_places=5, max_digits=10, rounding='ROUND_HALF_EVEN')
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "transactionhistory"



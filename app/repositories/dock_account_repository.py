from decimal import Decimal

from fastapi import HTTPException

from app.database.models.dock_account import DockAccount
from app.interfaces.dock_account import DockAccountInterface
from app.interfaces.enum import TransactionType


class DockAccountRepository:
    def __init__(self):
        self._model = DockAccount

    def insert(self, dock_account: DockAccountInterface) -> DockAccountInterface:
        inserted_dock_account = self._model.create(**dock_account.model_dump())
        return DockAccountInterface.build(dock_account=inserted_dock_account)

    def get_by_id(self, _id: str, **filters) -> DockAccountInterface:
        dock_account = self._model.select().where(self._model.id == _id)
        if filters:
            dock_account = dock_account.filter(**filters)
        dock_account = dock_account.first()
        if not dock_account:
            raise HTTPException(status_code=404, detail="DockAccount not found")
        return DockAccountInterface.build(dock_account=dock_account)

    def update(self, dock_account: DockAccountInterface):
        dock_account_to_update = self._model.select().where(self._model.id == dock_account.id).first()
        if not dock_account_to_update:
            raise HTTPException(status_code=404, detail="DockAccount not found")
        dock_account_to_update.update(**dock_account.model_dump()).where(self._model.id == dock_account.id).execute()
        return dock_account

    @staticmethod
    def make_transaction(dock_account: DockAccount, amount: Decimal, transaction_type: TransactionType):
        if transaction_type == TransactionType.deposit:
            dock_account.balance += amount
            dock_account.save()
        elif transaction_type == TransactionType.withdrawal:
            dock_account.balance -= amount
            dock_account.save()
        else:
            raise HTTPException(status_code=422, detail="Invalid transaction")
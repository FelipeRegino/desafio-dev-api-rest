from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from fastapi import HTTPException
from peewee import fn

from app.database.models.transaction_history import TransactionHistory
from app.interfaces import BetweenDateFilter
from app.interfaces.enum import TransactionType
from app.interfaces.transaction_history import TransactionHistoryInterface


class TransactionHistoryRepository:
    def __init__(self):
        self._model = TransactionHistory

    def insert(self, transaction_history: TransactionHistoryInterface) -> TransactionHistoryInterface:
        inserted_transaction_history = self._model.create(**transaction_history.model_dump())
        return TransactionHistoryInterface.build(inserted_transaction_history)

    def get_by_id(self, _id: str, **filters) -> TransactionHistoryInterface:
        transaction_history = self._model.select().where(self._model.id == _id)
        if filters:
            transaction_history = transaction_history.filter(**filters)
        transaction_history = transaction_history.first()
        if not transaction_history:
            raise HTTPException(status_code=404, detail="TransactionHistory not found")
        return TransactionHistoryInterface.build(transaction_history)

    def get(
            self, dock_account_id: str, between_filter: Optional[BetweenDateFilter] = None, **filters
    ) -> List[TransactionHistoryInterface]:
        transaction_history = self._model.select().where(self._model.dock_account == dock_account_id)
        if between_filter:
            transaction_history = transaction_history.where(
                self._model.created_at.between(between_filter.start_date, between_filter.end_date)
            )
        if filters:
            transaction_history = transaction_history.filter(**filters)
        if not transaction_history:
            raise HTTPException(status_code=404, detail="TransactionHistory not found")
        return [TransactionHistoryInterface.build(x) for x in transaction_history]

    def daily_withdrawal_amount(self, dock_account_id: str) -> Decimal:
        amount = (self._model.select(fn.SUM(self._model.amount))
                               .where(self._model.dock_account == dock_account_id)
                               .where(self._model.created_at.between(datetime.now().replace(hour=00, minute=00),
                                                                     datetime.now()))
                               .filter(type=TransactionType.withdrawal.value))
        return amount.scalar() or 0

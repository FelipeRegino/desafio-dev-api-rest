from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from app.interfaces import BetweenDateFilter
from app.interfaces.enum import AccountStatus, TransactionType
from app.interfaces.transaction_history import TransactionHistoryInterface
from app.repositories.dock_account_repository import DockAccountRepository
from app.repositories.transaction_history_repository import TransactionHistoryRepository
from app.utils.validator import withdrawal_validation


class TransactionHistoryService:
    def __init__(self):
        self._repository = TransactionHistoryRepository()
        self._dock_account_repository = DockAccountRepository()

    def get_transaction_history(
            self, dock_account_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ):
        between_filter = None
        if start_date:
            between_filter = BetweenDateFilter(
                start_date=start_date,
                end_date=end_date if end_date else datetime.now()
            )
        transaction_history = self._repository.get(dock_account_id=dock_account_id, between_filter=between_filter)
        return transaction_history

    def create(self, transaction_history: TransactionHistoryInterface):
        dock_account = self._dock_account_repository.get_by_id(_id=transaction_history.dock_account,
                                                               status=AccountStatus.active.value)
        if not dock_account:
            raise HTTPException(status_code=422, detail="DockAccount cannot make transactions")

        if transaction_history.type == TransactionType.withdrawal:
            withdrawal_validation(dock_account=dock_account, amount=transaction_history.amount)

        new_transaction_history = self._repository.insert(transaction_history=transaction_history)
        return new_transaction_history

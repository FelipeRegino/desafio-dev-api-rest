from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field

from app.database.models.transaction_history import TransactionHistory
from app.interfaces.enum import TransactionType


class TransactionHistoryInterface(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    dock_account: UUID4
    type: TransactionType
    amount: Decimal
    created_at: datetime = datetime.now()

    @classmethod
    def build(cls, transaction: TransactionHistory):
        return cls(
            id=transaction.id,
            dock_account=transaction.dock_account.id,
            type=transaction.type,
            amount=transaction.amount,
            created_at=transaction.created_at
        )

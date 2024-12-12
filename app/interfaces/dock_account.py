import re
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field, field_validator

from app.database.models.dock_account import DockAccount
from app.interfaces.enum import AccountStatus


class DockAccountInterface(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    holder: str
    number: str
    agency: str
    balance: Decimal = 0.0
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    status: AccountStatus = AccountStatus.active

    @classmethod
    def build(cls, dock_account: DockAccount):
        return cls(
            id=dock_account.id,
            holder=dock_account.holder.cpf,
            number=dock_account.number,
            agency=dock_account.agency,
            balance=dock_account.balance,
            created_at=dock_account.created_at,
            updated_at=dock_account.updated_at,
            status=dock_account.status
        )

class UpdateDockAccountRequest(BaseModel):
    id: str
    cpf: str

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        return re.sub("[^0-9]", "", v)

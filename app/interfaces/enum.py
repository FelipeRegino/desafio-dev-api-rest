from enum import StrEnum


class AccountStatus(StrEnum):
    active = "ACTIVE"
    closed = "CLOSED"
    blocked = "BLOCKED"

class TransactionType(StrEnum):
    deposit = "DEPOSIT"
    withdrawal = "WITHDRAWAL"

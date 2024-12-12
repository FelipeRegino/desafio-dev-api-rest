from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from fastapi import HTTPException

from app.config.settings import get_settings
from app.interfaces.holder import HolderInterface
from app.repositories.holder_repository import HolderRepository
from app.services.transaction_history import TransactionHistoryService
from app.repositories.transaction_history_repository import TransactionHistoryRepository
from app.repositories.dock_account_repository import DockAccountRepository
from app.interfaces.transaction_history import TransactionHistoryInterface
from app.interfaces.dock_account import DockAccountInterface
from app.interfaces.enum import TransactionType, AccountStatus

holder_repository = HolderRepository()
_holder = holder_repository.insert(HolderInterface(cpf="80627244092", name="Test Holder"))

@pytest.fixture
def holder():
    return _holder

@pytest.fixture
def settings():
    return get_settings()

@pytest.fixture
def service():
    return TransactionHistoryService()

@pytest.fixture
def transaction_history_repository():
    return TransactionHistoryRepository()

@pytest.fixture
def dock_account_repository():
    return DockAccountRepository()

def test_get_transaction_history_by_account(service, transaction_history_repository, dock_account_repository, holder):
    # Create an account and transactions history entries
    dock_account = dock_account_repository.insert(DockAccountInterface(
        holder=holder.cpf,
        agency="0001",
        number="123456",
        status=AccountStatus.active
    ))
    transaction_history_repository.insert(TransactionHistoryInterface(
        dock_account=dock_account.id,
        type=TransactionType.deposit,
        amount=Decimal(100),
    ))
    transaction_history_repository.insert(TransactionHistoryInterface(
        dock_account=dock_account.id,
        type=TransactionType.withdrawal,
        amount=Decimal(30),
    ))

    # Retrieve transaction history for the account
    history = service.get_transaction_history(dock_account_id=dock_account.id)

    # Verify the history contains the transactions
    assert history is not None
    assert len(history) == 2
    assert history[0].dock_account == dock_account.id

def test_get_transaction_history_with_filters(service, transaction_history_repository, dock_account_repository, holder):
    # Create an account and transactions history entries
    dock_account = dock_account_repository.insert(DockAccountInterface(
        holder=holder.cpf,
        agency="0001",
        number="123456",
        status=AccountStatus.active
    ))
    transaction_history_repository.insert(TransactionHistoryInterface(
        dock_account=dock_account.id,
        type=TransactionType.deposit,
        amount=Decimal(100),
        created_at=datetime.now() - timedelta(days=2)
    ))
    transaction_history_repository.insert(TransactionHistoryInterface(
        dock_account=dock_account.id,
        type=TransactionType.withdrawal,
        amount=Decimal(30),
    ))

    # Retrieve transaction history for the account
    history = service.get_transaction_history(
        dock_account_id=dock_account.id,
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now()
    )

    # Verify the history contains the transactions
    assert history is not None
    assert len(history) == 1
    assert history[0].dock_account == dock_account.id

def test_create_transaction_deposit(service, transaction_history_repository, dock_account_repository, holder):
    # Create an account and prepare a valid deposit transaction
    dock_account = dock_account_repository.insert(DockAccountInterface(
        holder=holder.cpf,
        agency="0001",
        number="123456",
        status=AccountStatus.active
    ))
    transaction = TransactionHistoryInterface(
        dock_account=dock_account.id,
        type=TransactionType.deposit,
        amount=Decimal(200.0),
    )

    # Create the deposit transaction
    created_transaction = service.create(transaction)

    # Verify the deposit transaction was created correctly
    assert created_transaction is not None
    assert created_transaction.dock_account == transaction.dock_account
    assert created_transaction.type == transaction.type
    assert created_transaction.amount == transaction.amount

def test_create_transaction_withdrawal(service, transaction_history_repository, dock_account_repository, holder):
    # Create an account with sufficient balance and prepare a withdrawal transaction
    dock_account = dock_account_repository.insert(DockAccountInterface(
        holder=holder.cpf,
        agency="0001",
        number="123456",
        balance=Decimal(100.0),
        status=AccountStatus.active
    ))
    transaction = TransactionHistoryInterface(
        dock_account=dock_account.id,
        type=TransactionType.withdrawal,
        amount=Decimal(50.0),
    )

    # Create the withdrawal transaction
    created_transaction = service.create(transaction)

    # Verify the withdrawal transaction was created correctly
    assert created_transaction is not None
    assert created_transaction.dock_account == transaction.dock_account
    assert created_transaction.type == transaction.type
    assert created_transaction.amount == transaction.amount

def test_create_transaction_withdrawal_insufficient_balance(
        service, transaction_history_repository, dock_account_repository, holder
):
    # Create an account with low balance and prepare a withdrawal transaction
    dock_account = dock_account_repository.insert(DockAccountInterface(
        holder=holder.cpf,
        agency="0001",
        number="123456",
        balance=Decimal(100.0),
        status=AccountStatus.active
    ))
    transaction = TransactionHistoryInterface(
        dock_account=dock_account.id,
        type=TransactionType.withdrawal,
        amount=Decimal(500.0)
    )

    # Ensure an HTTP 422 error is raised for insufficient balance
    with pytest.raises(HTTPException) as exc:
        service.create(transaction)
    assert exc.value.status_code == 422
    assert "DockAccount has no sufficient balance" in exc.value.detail

def test_create_transaction_withdrawal_negative_amount(service, dock_account_repository, holder):
    # Create an account and prepare a withdrawal transaction with a negative amount
    dock_account = dock_account_repository.insert(DockAccountInterface(
        holder=holder.cpf,
        agency="0001",
        number="123456",
        balance=Decimal(100.0),
        status=AccountStatus.active
    ))
    transaction = TransactionHistoryInterface(
        dock_account=dock_account.id,
        type=TransactionType.withdrawal,
        amount=Decimal(-50.0),
    )

    # Ensure an HTTP 422 error is raised for a negative amount
    with pytest.raises(HTTPException) as exc:
        service.create(transaction)
    assert exc.value.status_code == 422
    assert "Invalid withdrawal amount" in exc.value.detail

def test_create_transaction_withdrawal_exceeds_limit(service, dock_account_repository, settings, holder):
    # Create an account and prepare a withdrawal transaction exceeding daily limit
    dock_account = dock_account_repository.insert(DockAccountInterface(
        holder=holder.cpf,
        agency="0001",
        number="123456",
        balance=Decimal(10000.0),
        status=AccountStatus.active
    ))
    transaction = TransactionHistoryInterface(
        dock_account=dock_account.id,
        type=TransactionType.withdrawal,
        amount=settings.maximum_daily_limit + 1,
    )

    # Ensure an HTTP 422 error is raised for exceeding daily limit
    with pytest.raises(HTTPException) as exc:
        service.create(transaction)
    assert exc.value.status_code == 422
    assert "Daily withdrawal limit exceeded" in exc.value.detail

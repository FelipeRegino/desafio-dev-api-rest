import pytest
from fastapi import HTTPException

from app.database.models.dock_account import DockAccount
from app.database.models.holder import Holder
from app.interfaces.dock_account import DockAccountInterface
from app.interfaces.holder import HolderInterface
from app.repositories.transaction_history_repository import TransactionHistoryRepository
from app.database.models.transaction_history import TransactionHistory
from app.interfaces.transaction_history import TransactionHistoryInterface
from app.interfaces.enum import TransactionType
from decimal import Decimal

_holder_interface = HolderInterface(cpf="43237036005", name="Test Holder")
_holder = Holder.create(**_holder_interface.model_dump())
_dock_account_interface = DockAccountInterface(
    holder=_holder.cpf,
    number="123456789",
    agency="001",
    balance=Decimal("100.0")
)
_dock_account = DockAccount.create(**_dock_account_interface.model_dump())

@pytest.fixture
def mock_transaction_history():
    return TransactionHistoryInterface(
        dock_account=_dock_account.id,
        amount=Decimal("150.0"),
        type=TransactionType.deposit,
    )

@pytest.fixture
def repository():
    return TransactionHistoryRepository()

@pytest.fixture
def setup_database(mock_transaction_history):
    # Delete the mock_transaction_history instance before and after each test
    TransactionHistory.delete().where(TransactionHistory.id == mock_transaction_history.id).execute()

    yield  # Allow the test to run

    TransactionHistory.delete().where(TransactionHistory.id == mock_transaction_history.id).execute()

def test_insert_success(setup_database, repository, mock_transaction_history):
    # Call the insert method
    result = repository.insert(mock_transaction_history)

    # Validate the result
    assert result.dock_account == mock_transaction_history.dock_account
    assert result.amount == mock_transaction_history.amount
    assert result.type == mock_transaction_history.type

def test_get_by_id_success(setup_database, repository, mock_transaction_history):
    # Insert the transaction history to simulate an existing entry
    TransactionHistory.create(**mock_transaction_history.model_dump())

    # Call the get_by_id method
    result = repository.get_by_id(_id=mock_transaction_history.id)

    # Validate the result
    assert result.dock_account == mock_transaction_history.dock_account
    assert result.amount == mock_transaction_history.amount
    assert result.type == mock_transaction_history.type

def test_get_by_id_not_found(setup_database, repository):
    # Call the get_by_id method and expect an HTTPException
    with pytest.raises(HTTPException) as ex:
        repository.get_by_id(_id="acd3a4fe-d1db-4ae9-87cc-0cb7f2e3147a")

    # Validate the exception
    assert ex.value.status_code == 404
    assert ex.value.detail == "TransactionHistory not found"

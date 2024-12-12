import pytest
from fastapi.testclient import TestClient

from app.database.models.dock_account import DockAccount
from app.database.models.holder import Holder
from app.database.models.transaction_history import TransactionHistory
from app.http_server import app
from app.interfaces.dock_account import DockAccountInterface
from app.interfaces.enum import TransactionType
from app.interfaces.holder import HolderInterface
from app.interfaces.transaction_history import TransactionHistoryInterface
from decimal import Decimal

client = TestClient(app)
_holder_interface = HolderInterface(cpf="98056698078", name="Test Holder")
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
def setup_database(mock_transaction_history):
    # Delete any existing transaction history before and after each test
    TransactionHistory.delete().where(TransactionHistory.id == mock_transaction_history.id).execute()

    yield  # Allow the test to run

    TransactionHistory.delete().where(TransactionHistory.id == mock_transaction_history.id).execute()

def test_get_transaction_history_success(setup_database, mock_transaction_history):
    # Create a transaction history in the database
    TransactionHistory.create(**mock_transaction_history.model_dump())

    # Call the GET /transaction/{dock_dock_account} endpoint
    response = client.get(f"/transaction/{mock_transaction_history.dock_account}")

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["dock_account"] == mock_transaction_history.dock_account

def test_get_transaction_history_filtered_success(setup_database, mock_transaction_history):
    # Create a transaction history in the database
    TransactionHistory.create(**mock_transaction_history.model_dump())

    # Call the GET /transaction/{dock_dock_account} endpoint with date filters
    response = client.get(
        f"/transaction/{mock_transaction_history.dock_account}",
        params={"start_date": "2023-01-01T00:00:00", "end_date": "2023-01-02T00:00:00"}
    )

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["dock_account"] == mock_transaction_history.dock_account

def test_get_transaction_history_not_found():
    # Call the GET /transaction/{dock_dock_account} endpoint for a non-existing account
    response = client.get("/transaction/999999")

    # Validate the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction history not found"

def test_create_transaction_history_success(setup_database, mock_transaction_history):
    # Call the POST /transaction endpoint
    response = client.post("/transaction", json=mock_transaction_history.model_dump())

    # Validate the response
    assert response.status_code == 201
    data = response.json()
    assert data["dock_account"] == mock_transaction_history.dock_account
    assert data["amount"] == str(mock_transaction_history.amount)

def test_create_transaction_history_invalid():
    # Call the POST /transaction endpoint with invalid data
    response = client.post("/transaction", json={"dock_account": "", "amount": "-100.0"})

    # Validate the response
    assert response.status_code == 422

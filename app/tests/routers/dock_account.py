import pytest
from fastapi.testclient import TestClient
from app.database.models.dock_account import DockAccount
from app.database.models.holder import Holder
from app.http_server import app
from app.interfaces.dock_account import DockAccountInterface
from decimal import Decimal

from app.interfaces.enum import AccountStatus
from app.interfaces.holder import HolderInterface

client = TestClient(app)
_holder_interface = HolderInterface(cpf="18038771036", name="Test Holder")
_holder = Holder.create(**_holder_interface.model_dump())

@pytest.fixture
def mock_dock_account():
    return DockAccountInterface(
        holder=_holder.id,
        number="123456789",
        agency="001",
        balance=Decimal("100.0"),
    )

@pytest.fixture
def setup_database(mock_dock_account):
    # Delete any existing DockAccount before and after each test
    DockAccount.delete().where(DockAccount.holder == mock_dock_account.holder).execute()

    yield  # Allow the test to run

    DockAccount.delete().where(DockAccount.holder == mock_dock_account.holder).execute()

def test_get_dock_account_success(setup_database, mock_dock_account):
    # Create a DockAccount in the database
    DockAccount.create(**mock_dock_account.model_dump())

    # Call the GET /dock_account/{cpf} endpoint
    response = client.get(f"/dock_account/{mock_dock_account.holder}")

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["holder"] == mock_dock_account.holder

def test_get_dock_account_by_id_success(setup_database, mock_dock_account):
    # Create a DockAccount in the database
    DockAccount.create(**mock_dock_account.model_dump())

    # Call the GET /dock_account/{cpf}/{_id} endpoint
    response = client.get(f"/dock_account/{mock_dock_account.holder}/{mock_dock_account.id}")

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(mock_dock_account.id)
    assert data["holder"] == mock_dock_account.holder

def test_create_dock_account_success(setup_database, mock_dock_account):
    # Call the POST /dock_account endpoint
    response = client.post("/dock_account", json={"cpf": mock_dock_account.holder})

    # Validate the response
    assert response.status_code == 201
    data = response.json()
    assert data["holder"] == mock_dock_account.holder

def test_get_dock_account_not_found():
    # Call the GET /dock_account/{cpf} endpoint for a non-existing CPF
    response = client.get("/dock_account/nonexistent_holder")

    # Validate the response
    assert response.status_code == 404
    assert response.json()["detail"] == "DockAccount not found"

def test_close_dock_account_success(setup_database, mock_dock_account):
    # Create a DockAccount in the database
    DockAccount.create(**mock_dock_account.model_dump())

    # Call the /close endpoint
    response = client.post(f"/dock_account/{mock_dock_account.id}/close")

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CLOSED"

def test_block_dock_account_success(setup_database, mock_dock_account):
    # Create a DockAccount in the database
    DockAccount.create(**mock_dock_account.model_dump())

    # Call the /block endpoint
    response = client.post(f"/dock_account/{mock_dock_account.id}/block")

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "BLOCKED"

def test_unblock_dock_account_success(setup_database, mock_dock_account):
    # Create a DockAccount in the database and set it to blocked
    dock_account = DockAccount.create(**mock_dock_account.model_dump())
    dock_account.status = AccountStatus.blocked
    dock_account.save()

    # Call the /unblock endpoint
    response = client.post(f"/dock_account/{mock_dock_account.id}/unblock")

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ACTIVE"

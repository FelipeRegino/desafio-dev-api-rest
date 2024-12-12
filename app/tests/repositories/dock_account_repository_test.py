import pytest
from fastapi import HTTPException

from app.database.models.holder import Holder
from app.interfaces.holder import HolderInterface
from app.repositories.dock_account_repository import DockAccountRepository
from app.database.models.dock_account import DockAccount
from app.interfaces.dock_account import DockAccountInterface
from decimal import Decimal
from app.interfaces.enum import AccountStatus

_holder_interface = HolderInterface(cpf="70312641036", name="Test Holder")
_holder = Holder.create(**_holder_interface.model_dump())

@pytest.fixture
def mock_dock_account():
    return DockAccountInterface(
        holder=_holder.cpf,
        number="123456789",
        agency="001",
        balance=Decimal("100.0")
    )

@pytest.fixture
def repository():
    return DockAccountRepository()

@pytest.fixture
def setup_database(mock_dock_account):
    # Delete the mock_dock_account instance before and after each test
    DockAccount.delete().where(DockAccount.id == mock_dock_account.id).execute()

    yield  # Allow the test to run

    DockAccount.delete().where(DockAccount.id == mock_dock_account.id).execute()

def test_insert_success(setup_database, repository, mock_dock_account):
    # Call the insert method
    result = repository.insert(mock_dock_account)

    # Validate the result
    assert result.holder == mock_dock_account.holder
    assert result.number == mock_dock_account.number
    assert result.agency == mock_dock_account.agency
    assert result.status == AccountStatus.active

def test_get_by_id_success(setup_database, repository, mock_dock_account):
    # Insert the DockAccount to simulate an existing entry
    DockAccount.create(**mock_dock_account.model_dump())

    # Call the get_by_id method
    result = repository.get_by_id(_id=mock_dock_account.id)

    # Validate the result
    assert result.holder == mock_dock_account.holder
    assert result.number == mock_dock_account.number
    assert result.agency == mock_dock_account.agency
    assert result.balance == mock_dock_account.balance

def test_get_by_id_not_found(setup_database, repository):
    # Call the get_by_id method and expect an HTTPException
    with pytest.raises(HTTPException) as ex:
        repository.get_by_id(_id="acd3a4fe-d1db-4ae9-87cc-0cb7f2e3147a")

    # Validate the exception
    assert ex.value.status_code == 404
    assert ex.value.detail == "DockAccount not found"

import pytest
from fastapi import HTTPException

from app.services.dock_account import DockAccountService
from app.repositories.dock_account_repository import DockAccountRepository
from app.repositories.holder_repository import HolderRepository
from app.interfaces.dock_account import DockAccountInterface, UpdateDockAccountRequest
from app.interfaces.holder import HolderInterface
from app.interfaces.enum import AccountStatus
from app.utils.generator import generate_random_account_number, generate_random_agency_number


@pytest.fixture
def service():
    return DockAccountService()

@pytest.fixture
def dock_account_repository():
    return DockAccountRepository()

@pytest.fixture
def holder_repository():
    return HolderRepository()

def test_get_dock_account(service, holder_repository):
    # Create a holder for testing
    holder = holder_repository.insert(HolderInterface(cpf="57057797044", name="Test Holder"))

    # Create accounts associated with the test Holder
    service.create(cpf=holder.cpf)
    service.create(cpf=holder.cpf)
    # Retrieve accounts associated with the provided CPF
    accounts = service.get_dock_account(holder.cpf)

    # Verify accounts are returned and have the correct CPF
    assert accounts is not None
    assert all(account.holder == holder.cpf for account in accounts)

def test_get_dock_account_by_id(service, holder_repository):
    # Create a holder for testing
    holder = holder_repository.insert(HolderInterface(cpf="40799678023", name="Test Holder"))

    # Create accounts associated with the test Holder
    created_account = service.create(cpf=holder.cpf)

    # Retrieve the account by ID
    account = service.get_dock_account_by_id(holder.cpf, created_account.id)

    # Ensure the returned account matches the expected ID and CPF
    assert account is not None
    assert account.id == created_account.id
    assert account.holder == holder.cpf

def test_create_dock_account(service, holder_repository):
    # Create a holder to associate with the new account
    holder = holder_repository.insert(HolderInterface(cpf="87561081090", name="Test Holder"))

    # Create a new account for the holder
    account = service.create(holder.cpf)

    # Verify the account was created with the correct details
    assert account is not None
    assert account.holder == holder.cpf
    assert account.agency is not None
    assert account.number is not None

def test_close_account(service, holder_repository):
    # Create a holder for testing
    holder = holder_repository.insert(HolderInterface(cpf="18826761060", name="Test Holder"))

    # Create a new account for the holder
    account = service.create(holder.cpf)

    # Close the account
    service.close(request=UpdateDockAccountRequest(id=str(account.id), cpf=holder.cpf))

    # Verify the account status is updated to CLOSED
    account = service.get_dock_account_by_id(holder.cpf, account.id)
    assert account.status == AccountStatus.closed

def test_close_account_already_closed(service, dock_account_repository, holder_repository):
    # Create a holder for testing
    holder = holder_repository.insert(HolderInterface(cpf="84148708050", name="Test Holder"))

    # Create a new account for the holder
    dock_account = DockAccountInterface(
            holder=holder.cpf,
            number=generate_random_account_number(),
            agency=generate_random_agency_number(),
            status=AccountStatus.closed
    )
    dock_account_repository.insert(dock_account=dock_account)

    # Ensure an HTTP 422 error is raised for already closed accounts
    with pytest.raises(HTTPException) as exc:
        service.close(request=UpdateDockAccountRequest(id=str(dock_account.id), cpf=holder.cpf))
    assert exc.value.status_code == 422
    assert "DockAccount is already closed" in exc.value.detail

def test_block_account(service, dock_account_repository, holder_repository):
    # Create a holder for testing
    holder = holder_repository.insert(HolderInterface(cpf="99529026030", name="Test Holder"))

    # Create a new account for the holder
    account = service.create(holder.cpf)

    # Block the account
    service.block(request=UpdateDockAccountRequest(id=str(account.id), cpf=holder.cpf))

    # Verify the account status is updated to BLOCKED
    account = dock_account_repository.get_by_id(_id=account.id, holder=holder.cpf)
    assert account.status == AccountStatus.blocked

def test_block_account_already_blocked(service, dock_account_repository, holder_repository):
    # Create a holder for testing
    holder = holder_repository.insert(HolderInterface(cpf="63093991013", name="Test Holder"))

    # Create a new account for the holder
    dock_account = DockAccountInterface(
            holder=holder.cpf,
            number=generate_random_account_number(),
            agency=generate_random_agency_number(),
            status=AccountStatus.blocked
    )
    dock_account_repository.insert(dock_account=dock_account)

    # Ensure an HTTP 422 error is raised for already blocked accounts
    with pytest.raises(HTTPException) as exc:
        service.block(request=UpdateDockAccountRequest(id=str(dock_account.id), cpf=holder.cpf))
    assert exc.value.status_code == 422
    assert "DockAccount is already blocked" in exc.value.detail

def test_unblock_account(service, dock_account_repository, holder_repository):
    # Create a holder for testing
    holder = holder_repository.insert(HolderInterface(cpf="84629845054", name="Test Holder"))

    # Create a new account for the holder
    dock_account = DockAccountInterface(
            holder=holder.cpf,
            number=generate_random_account_number(),
            agency=generate_random_agency_number(),
            status=AccountStatus.blocked
    )
    dock_account_repository.insert(dock_account=dock_account)

    # Unblock the account
    service.unblock(request=UpdateDockAccountRequest(id=str(dock_account.id), cpf=holder.cpf))

    # Verify the account status is updated to ACTIVE
    account = dock_account_repository.get_by_id(_id=dock_account.id, holder=holder.cpf)
    assert account.status == AccountStatus.active

def test_unblock_account_not_blocked(service, dock_account_repository, holder_repository):
    # Create a holder for testing
    holder = holder_repository.insert(HolderInterface(cpf="06713950094", name="Test Holder"))

    # Create a new account for the holder
    dock_account = DockAccountInterface(
            holder=holder.cpf,
            number=generate_random_account_number(),
            agency=generate_random_agency_number(),
            status=AccountStatus.active
    )
    dock_account_repository.insert(dock_account=dock_account)

    # Ensure an HTTP 422 error is raised for non-blocked accounts
    with pytest.raises(HTTPException) as exc:
        service.unblock(request=UpdateDockAccountRequest(id=str(dock_account.id), cpf=holder.cpf))
    assert exc.value.status_code == 422
    assert "DockAccount is already unblocked" in exc.value.detail

def test_create_invalid_cpf(service):
    # Provide an invalid CPF for account creation
    cpf = "000000000000"

    # Ensure an HTTP 404 error is raised for not found Holder
    with pytest.raises(HTTPException) as exc:
        service.create(cpf)
    assert exc.value.status_code == 404
    assert "Holder not found" in exc.value.detail
